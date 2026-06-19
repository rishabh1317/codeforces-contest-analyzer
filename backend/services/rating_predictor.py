"""Statistical rating growth predictor using linear regression on contest history."""

from typing import Any, Dict, List, Optional


def predict_rating_growth(
    rating_history: List[Dict[str, Any]],
    user_rating: Optional[int] = None,
) -> Dict[str, Any]:
    if not rating_history or len(rating_history) < 3:
        current = user_rating or (
            rating_history[-1].get("newRating") if rating_history else 1200
        )
        return {
            "current_rating": current,
            "predicted_rating_low": current,
            "predicted_rating_high": current + 50,
            "predicted_rating_mid": current + 25,
            "confidence_score": 0.2,
            "contests_analyzed": len(rating_history),
            "trend": "insufficient_data",
            "suggested_improvements": [
                "Participate in more rated contests for accurate predictions",
                "Solve problems consistently between contests",
            ],
        }

    ratings = [e.get("newRating", 0) for e in rating_history]
    n = len(ratings)

    # Linear regression: rating = a + b * contest_index
    x_vals = list(range(n))
    x_mean = sum(x_vals) / n
    y_mean = sum(ratings) / n

    numerator = sum((x_vals[i] - x_mean) * (ratings[i] - y_mean) for i in range(n))
    denominator = sum((x_vals[i] - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        slope = 0.0
    else:
        slope = numerator / denominator

    intercept = y_mean - slope * x_mean

    # Predict 3 contests ahead
    future_indices = [n, n + 1, n + 2]
    predictions = [intercept + slope * idx for idx in future_indices]
    predicted_mid = int(round(predictions[1]))

    # Confidence from R² and data volume
    if denominator > 0:
        predicted_at_i = [intercept + slope * x_vals[i] for i in range(n)]
        ss_res = sum((ratings[i] - predicted_at_i[i]) ** 2 for i in range(n))
        ss_tot = sum((ratings[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
    else:
        r_squared = 0

    data_factor = min(1.0, n / 20)
    confidence = round(min(0.95, max(0.15, r_squared * 0.6 + data_factor * 0.4)), 2)

    # Prediction range using residual std
    residuals = []
    for i in range(n):
        predicted = intercept + slope * x_vals[i]
        residuals.append(ratings[i] - predicted)

    if len(residuals) >= 2:
        res_std = (sum(r ** 2 for r in residuals) / len(residuals)) ** 0.5
    else:
        res_std = 50

    margin = int(round(res_std * (1.5 - confidence)))
    predicted_low = max(800, predicted_mid - margin)
    predicted_high = min(4000, predicted_mid + margin)

    trend = "stable"
    if slope > 15:
        trend = "strong_growth"
    elif slope > 5:
        trend = "growing"
    elif slope < -10:
        trend = "declining"

    improvements = _suggest_improvements(slope, n, ratings)

    return {
        "current_rating": ratings[-1],
        "predicted_rating_low": predicted_low,
        "predicted_rating_high": predicted_high,
        "predicted_rating_mid": predicted_mid,
        "confidence_score": confidence,
        "contests_analyzed": n,
        "trend": trend,
        "monthly_growth_estimate": round(slope * 2, 1),
        "suggested_improvements": improvements,
    }


def _suggest_improvements(
    slope: float, contest_count: int, ratings: List[int]
) -> List[str]:
    suggestions = []

    if contest_count < 10:
        suggestions.append(
            "Increase contest frequency to 2-3 rated contests per month"
        )

    if slope < 5:
        suggestions.append(
            "Focus on upsolving contest problems within 48 hours after each contest"
        )
        suggestions.append(
            "Target weak topics with problems 100-200 points below your rating"
        )
    elif slope > 20:
        suggestions.append(
            "Maintain momentum — attempt harder problems to sustain growth"
        )

    recent_changes = []
    if len(ratings) >= 5:
        recent_changes = [
            ratings[i] - ratings[i - 1] for i in range(len(ratings) - 4, len(ratings))
        ]
        if sum(recent_changes) < 0:
            suggestions.append(
                "Recent rating dip detected — review mistakes from last 3 contests"
            )

    if not suggestions:
        suggestions.append("Continue balanced practice across all major topics")

    return suggestions[:4]
