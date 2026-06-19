"""Personalized problem recommendation engine."""

from typing import Any, Dict, List, Optional, Set

from services.codeforces import get_problemset
from services.topic_analyzer import analyze_topics


def _solved_problem_keys(submissions: List[Dict[str, Any]]) -> Set[str]:
    keys: Set[str] = set()
    for sub in submissions:
        if sub.get("verdict") != "OK":
            continue
        problem = sub.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        if contest_id and index:
            keys.add(f"{contest_id}-{index}")
    return keys


def _recently_attempted_keys(
    submissions: List[Dict[str, Any]], limit: int = 50
) -> Set[str]:
    keys: Set[str] = set()
    for sub in submissions[:limit]:
        problem = sub.get("problem", {})
        contest_id = problem.get("contestId")
        index = problem.get("index")
        if contest_id and index:
            keys.add(f"{contest_id}-{index}")
    return keys


async def recommend_problems_async(
    submissions: List[Dict[str, Any]],
    user_rating: Optional[int],
    limit: int = 10,
) -> List[Dict[str, Any]]:
    if not submissions:
        return []

    analysis = analyze_topics(submissions, user_rating)
    weak_tags = [t["topic"] for t in analysis["weakest_topics"][:5]]
    if not weak_tags:
        weak_tags = [t["topic"] for t in analysis["topics"][:3]]

    solved = _solved_problem_keys(submissions)
    recent = _recently_attempted_keys(submissions)
    base_rating = user_rating or 1200

    problemset = await get_problemset()
    if not problemset:
        return _fallback_tag_recommendations(analysis, limit)

    candidates: List[Dict[str, Any]] = []

    for problem in problemset:
        contest_id = problem.get("contestId")
        index = problem.get("index")
        if not contest_id or not index:
            continue

        key = f"{contest_id}-{index}"
        if key in solved or key in recent:
            continue

        rating = problem.get("rating")
        if rating is None:
            continue

        tags = problem.get("tags", [])
        tag_overlap = len(set(tags) & set(weak_tags))
        if tag_overlap == 0:
            continue

        ideal = base_rating - 100
        rating_distance = abs(rating - ideal)
        weakness_bonus = tag_overlap * 150
        score = weakness_bonus - rating_distance + (rating / 10)

        matched = [t for t in tags if t in weak_tags]
        reason_parts = []
        if matched:
            reason_parts.append(f"Weak area: {', '.join(matched[:2])}")
        if rating <= base_rating:
            reason_parts.append("Difficulty matches your level")
        else:
            reason_parts.append("Stretch problem for growth")

        candidates.append(
            {
                "contest_id": contest_id,
                "index": index,
                "name": problem.get("name", ""),
                "rating": rating,
                "tags": tags,
                "url": f"https://codeforces.com/problemset/problem/{contest_id}/{index}",
                "reason": "; ".join(reason_parts),
                "difficulty_progression": _progression_label(rating, base_rating),
                "score": score,
            }
        )

    candidates.sort(key=lambda x: x["score"], reverse=True)

    return [
        {
            "contest_id": c["contest_id"],
            "index": c["index"],
            "name": c["name"],
            "rating": c["rating"],
            "tags": c["tags"],
            "url": c["url"],
            "reason": c["reason"],
            "difficulty_progression": c["difficulty_progression"],
        }
        for c in candidates[:limit]
    ]


def _progression_label(problem_rating: int, user_rating: int) -> str:
    delta = problem_rating - user_rating
    if delta <= -200:
        return "foundation"
    if delta <= 0:
        return "comfortable"
    if delta <= 150:
        return "growth"
    return "challenge"


def _fallback_tag_recommendations(
    analysis: Dict[str, Any], limit: int
) -> List[Dict[str, Any]]:
    results = []
    for rec in analysis.get("recommendations", [])[:limit]:
        results.append(
            {
                "contest_id": None,
                "index": None,
                "name": f"Practice {rec['tag']} problems",
                "rating": rec["suggested_difficulty"],
                "tags": [rec["tag"]],
                "url": rec["suggested_url"],
                "reason": f"Low success rate ({round(rec['ac_rate'] * 100)}%) on {rec['tag']}",
                "difficulty_progression": "foundation",
            }
        )
    return results
