from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import database
import schemas
from services.cache_service import get_cached_submissions, get_user_profile
from services.topic_analyzer import analyze_topics

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)


@router.get("/{platform}/{handle}", response_model=schemas.AnalysisResponse)
async def get_analysis(
    platform: str, handle: str, db: Session = Depends(database.get_db)
):
    if platform.lower() != "codeforces":
        raise HTTPException(status_code=400, detail="Only Codeforces is supported")

    handle = handle.strip()
    try:
        user = await get_user_profile(handle, platform.lower(), db)
        submissions = await get_cached_submissions(handle, platform.lower(), db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    if not submissions:
        return schemas.AnalysisResponse(
            handle=handle,
            total_submissions=0,
            weak_topics=[],
            strongest_topics=[],
            weakest_topics=[],
            recommendations=[],
            topic_recommendations=[],
        )

    result = analyze_topics(submissions, user.rating)

    def to_weak(t):
        return schemas.WeakTopic(
            topic=t["topic"],
            attempted=t["attempted"],
            solved=t["solved"],
            success_rate=t["success_rate"],
            avg_problem_rating=t.get("avg_problem_rating"),
            relative_performance_score=t.get("relative_performance_score"),
        )

    topic_recs = [
        f"Practice {r['tag']} — success rate {round(r['ac_rate'] * 100)}%, target difficulty {r['suggested_difficulty']}"
        for r in result["recommendations"]
    ]

    return schemas.AnalysisResponse(
        handle=handle,
        total_submissions=result["total_submissions"],
        weak_topics=[to_weak(t) for t in result["weak_topics"]],
        strongest_topics=[to_weak(t) for t in result["strongest_topics"]],
        weakest_topics=[to_weak(t) for t in result["weakest_topics"]],
        recommendations=[schemas.Recommendation(**r) for r in result["recommendations"]],
        topic_recommendations=topic_recs,
    )
