"""Contest performance analytics from rating history and submissions."""

from datetime import datetime
from typing import Any, Dict, List, Optional


def analyze_contest_performance(
    rating_history: List[Dict[str, Any]],
    submissions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    if not rating_history:
        return _empty_contest_analytics()

    rating_timeline = []
    rank_timeline = []
    rating_changes = []

    for entry in rating_history:
        old_rating = entry.get("oldRating", 0)
        new_rating = entry.get("newRating", 0)
        rank = entry.get("rank", 0)
        contest_name = entry.get("contestName", "")
        rating_change = new_rating - old_rating

        rating_timeline.append(
            {
                "contest_name": contest_name,
                "rating": new_rating,
                "old_rating": old_rating,
                "rating_change": rating_change,
            }
        )
        rank_timeline.append(
            {
                "contest_name": contest_name,
                "rank": rank,
            }
        )
        rating_changes.append(rating_change)

    total_contests = len(rating_history)
    positive_contests = sum(1 for c in rating_changes if c > 0)
    negative_contests = sum(1 for c in rating_changes if c < 0)

    # Contest frequency — average days between contests
    contest_dates = []
    for entry in rating_history:
        ts = entry.get("ratingUpdateTimeSeconds")
        if ts:
            contest_dates.append(datetime.utcfromtimestamp(ts))

    avg_days_between = 0.0
    if len(contest_dates) >= 2:
        contest_dates.sort()
        gaps = [
            (contest_dates[i] - contest_dates[i - 1]).days
            for i in range(1, len(contest_dates))
        ]
        avg_days_between = round(sum(gaps) / len(gaps), 1)

    # Consistency — std dev of rating changes (lower = more consistent)
    if len(rating_changes) >= 2:
        mean_change = sum(rating_changes) / len(rating_changes)
        variance = sum((c - mean_change) ** 2 for c in rating_changes) / len(
            rating_changes
        )
        consistency_score = round(max(0, 100 - (variance ** 0.5) * 2), 2)
    else:
        consistency_score = 50.0

    # Rating growth
    first_rating = rating_history[0].get("newRating", 0)
    current_rating = rating_history[-1].get("newRating", 0)
    total_growth = current_rating - first_rating
    contests_per_year = (
        round(total_contests / max(1, len(contest_dates) / 365), 1)
        if contest_dates
        else 0.0
    )

    upsolve_stats = _compute_upsolve_stats(submissions, rating_history)

    return {
        "total_contests": total_contests,
        "current_rating": current_rating,
        "max_rating": max(e.get("newRating", 0) for e in rating_history),
        "total_rating_growth": total_growth,
        "avg_rating_change": round(
            sum(rating_changes) / len(rating_changes), 2
        ),
        "positive_contests": positive_contests,
        "negative_contests": negative_contests,
        "consistency_score": consistency_score,
        "avg_days_between_contests": avg_days_between,
        "contests_per_year": contests_per_year,
        "rating_timeline": rating_timeline,
        "rank_timeline": rank_timeline,
        "upsolve_count": upsolve_stats["upsolve_count"],
        "upsolve_rate": upsolve_stats["upsolve_rate"],
        "summary": _build_summary(
            total_growth, consistency_score, positive_contests, total_contests
        ),
    }


def _compute_upsolve_stats(
    submissions: List[Dict[str, Any]],
    rating_history: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Problems solved outside contest window (upsolves)."""
    if not submissions or not rating_history:
        return {"upsolve_count": 0, "upsolve_rate": 0.0}

    contest_ids = {e.get("contestId") for e in rating_history if e.get("contestId")}
    upsolve_count = 0
    total_solved = 0

    seen = set()
    for sub in submissions:
        if sub.get("verdict") != "OK":
            continue
        problem = sub.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        if not contest_id or not index:
            continue
        key = f"{contest_id}-{index}"
        if key in seen:
            continue
        seen.add(key)
        total_solved += 1
        if contest_id not in contest_ids:
            upsolve_count += 1

    rate = round(upsolve_count / total_solved, 4) if total_solved else 0.0
    return {"upsolve_count": upsolve_count, "upsolve_rate": rate}


def _build_summary(
    growth: int, consistency: float, positive: int, total: int
) -> str:
    parts = []
    if growth > 200:
        parts.append("Strong rating growth trajectory")
    elif growth > 0:
        parts.append("Steady upward rating trend")
    elif growth < -100:
        parts.append("Rating has declined — focus on consistency")

    if consistency >= 70:
        parts.append("Highly consistent contest performance")
    elif consistency < 40:
        parts.append("Volatile contest results — stabilize with targeted practice")

    if total > 0:
        win_rate = positive / total
        if win_rate >= 0.6:
            parts.append("Majority of contests show rating gains")

    return ". ".join(parts) if parts else "Limited contest data available"


def _empty_contest_analytics() -> Dict[str, Any]:
    return {
        "total_contests": 0,
        "current_rating": None,
        "max_rating": None,
        "total_rating_growth": 0,
        "avg_rating_change": 0,
        "positive_contests": 0,
        "negative_contests": 0,
        "consistency_score": 0,
        "avg_days_between_contests": 0,
        "contests_per_year": 0,
        "rating_timeline": [],
        "rank_timeline": [],
        "upsolve_count": 0,
        "upsolve_rate": 0,
        "summary": "No contest history available",
    }
