"""Topic strength/weakness analysis from Codeforces submissions."""

from typing import Any, Dict, List, Optional, Tuple


def _build_tag_stats(submissions: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    tag_data: Dict[str, Dict[str, Any]] = {}

    for sub in submissions:
        verdict = sub.get("verdict", "")
        problem = sub.get("problem", {})
        tags = problem.get("tags", [])
        rating = problem.get("rating")
        is_solved = verdict == "OK"

        for tag in tags:
            if tag not in tag_data:
                tag_data[tag] = {"attempted": 0, "solved": 0, "ratings": []}
            tag_data[tag]["attempted"] += 1
            if is_solved:
                tag_data[tag]["solved"] += 1
            if rating is not None:
                tag_data[tag]["ratings"].append(rating)

    return tag_data


def _relative_performance(
    ac_rate: float, avg_difficulty: Optional[float], user_rating: Optional[int]
) -> float:
    """Score combining success rate and difficulty relative to user rating."""
    if user_rating is None or avg_difficulty is None:
        return round(ac_rate * 100, 2)

    difficulty_factor = avg_difficulty / max(user_rating, 800)
    # Higher difficulty with good AC rate = stronger performance
    score = ac_rate * 50 + min(difficulty_factor, 2.0) * 25
    return round(min(100.0, score), 2)


def analyze_topics(
    submissions: List[Dict[str, Any]],
    user_rating: Optional[int] = None,
    min_attempts: int = 3,
) -> Dict[str, Any]:
    if not submissions:
        return {
            "total_submissions": 0,
            "topics": [],
            "strongest_topics": [],
            "weakest_topics": [],
            "weak_topics": [],
            "recommendations": [],
        }

    tag_data = _build_tag_stats(submissions)
    topics: List[Dict[str, Any]] = []

    for tag, data in tag_data.items():
        attempted = data["attempted"]
        solved = data["solved"]
        ac_rate = solved / attempted if attempted else 0.0
        avg_difficulty = (
            int(sum(data["ratings"]) / len(data["ratings"])) if data["ratings"] else None
        )
        rel_score = _relative_performance(ac_rate, avg_difficulty, user_rating)

        topics.append(
            {
                "topic": tag,
                "attempted": attempted,
                "solved": solved,
                "success_rate": round(ac_rate, 4),
                "avg_problem_rating": avg_difficulty,
                "relative_performance_score": rel_score,
            }
        )

    qualified = [t for t in topics if t["attempted"] >= min_attempts]
    pool = qualified if qualified else topics

    strongest = sorted(
        pool,
        key=lambda t: (t["relative_performance_score"], t["success_rate"], t["solved"]),
        reverse=True,
    )[:5]

    weakest = sorted(
        pool,
        key=lambda t: (t["relative_performance_score"], -t["attempted"]),
    )[:5]

    weak_filter = [
        t
        for t in qualified
        if t["success_rate"] < 0.6 and t["attempted"] >= min_attempts
    ]
    weak_topics = sorted(weak_filter, key=lambda t: t["success_rate"])[:10]

    recommendations = _build_topic_recommendations(weak_topics, user_rating)

    return {
        "total_submissions": len(submissions),
        "topics": topics,
        "strongest_topics": strongest,
        "weakest_topics": weakest,
        "weak_topics": weak_topics,
        "recommendations": recommendations,
    }


def _build_topic_recommendations(
    weak_topics: List[Dict[str, Any]], user_rating: Optional[int]
) -> List[Dict[str, Any]]:
    recommendations = []
    base = user_rating or 1200

    for item in weak_topics[:5]:
        tag = item["topic"]
        ac_rate = item["success_rate"]
        avg_rating = item.get("avg_problem_rating")

        if avg_rating is not None:
            ref = avg_rating
        else:
            ref = base

        if ac_rate < 0.2:
            suggested = ref - 200
        elif ac_rate < 0.4:
            suggested = ref - 100
        elif ac_rate < 0.6:
            suggested = ref
        else:
            suggested = ref + 100

        suggested = int(round(suggested / 100.0) * 100)
        suggested = max(800, min(3500, suggested))

        recommendations.append(
            {
                "tag": tag,
                "ac_rate": round(ac_rate, 4),
                "suggested_difficulty": suggested,
                "action": f"Practice {tag} (Suggested Diff: {suggested})",
                "suggested_url": f"https://codeforces.com/problemset?tags={tag}",
            }
        )

    return recommendations


def tag_analysis_list(submissions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flat tag list for heatmap — all tags, sorted by AC rate ascending."""
    tag_data = _build_tag_stats(submissions)
    result = []

    for tag, data in tag_data.items():
        ac_rate = data["solved"] / data["attempted"] if data["attempted"] else 0.0
        avg_diff = (
            int(sum(data["ratings"]) / len(data["ratings"])) if data["ratings"] else 0
        )
        result.append(
            {
                "tag": tag,
                "total": data["attempted"],
                "solved": data["solved"],
                "ac_rate": round(ac_rate, 2),
                "avg_difficulty": avg_diff,
            }
        )

    result.sort(key=lambda x: x["ac_rate"])
    return result


def rival_tag_stats(submissions: List[Dict[str, Any]]) -> Tuple[List[Dict], List[Dict], int]:
    tag_data = _build_tag_stats(submissions)
    solved_problems = set()

    for sub in submissions:
        if sub.get("verdict") == "OK":
            problem = sub.get("problem", {})
            if problem.get("contestId") and problem.get("index"):
                solved_problems.add(f"{problem['contestId']}-{problem['index']}")

    stats = []
    for tag, data in tag_data.items():
        ac_rate = data["solved"] / data["attempted"] if data["attempted"] else 0.0
        stats.append(
            {
                "tag": tag,
                "solved": data["solved"],
                "attempted": data["attempted"],
                "ac_rate": round(ac_rate, 4),
            }
        )

    strong_candidates = [s for s in stats if s["attempted"] >= 3] or stats
    weak_candidates = [s for s in stats if s["attempted"] >= 3] or stats

    strongest = sorted(
        strong_candidates, key=lambda x: (x["ac_rate"], x["solved"]), reverse=True
    )[:3]
    weakest = sorted(
        weak_candidates, key=lambda x: (x["ac_rate"], -x["attempted"])
    )[:3]

    return strongest, weakest, len(solved_problems)
