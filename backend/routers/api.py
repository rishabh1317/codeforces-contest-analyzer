import logging

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import database
import models
import schemas
from services.cache_service import (
    get_cached_rating_history,
    get_cached_submissions,
    get_user_info_cached,
    get_user_profile,
)
from services.contest_analytics import analyze_contest_performance
from services.rating_predictor import predict_rating_growth
from services.recommendation_engine import recommend_problems_async
from services.topic_analyzer import analyze_topics, rival_tag_stats, tag_analysis_list

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api",
    tags=["api"],
)

PLATFORM = "codeforces"


async def get_contest_participants(contest_id: int, db: Session) -> int:
    cached = (
        db.query(models.ContestCache)
        .filter(models.ContestCache.contest_id == contest_id)
        .first()
    )
    if cached:
        return cached.total_participants

    from services.codeforces import get_contest_participants_from_api

    count = await get_contest_participants_from_api(contest_id)
    if count > 1:
        db.add(models.ContestCache(contest_id=contest_id, total_participants=count))
        db.commit()
    return count


def _topic_to_weak_topic(t: dict) -> schemas.WeakTopic:
    return schemas.WeakTopic(
        topic=t["topic"],
        attempted=t["attempted"],
        solved=t["solved"],
        success_rate=t["success_rate"],
        avg_problem_rating=t.get("avg_problem_rating"),
        relative_performance_score=t.get("relative_performance_score"),
    )


@router.get("/users/{handle}/dashboard", response_model=schemas.UserDashboardResponse)
async def get_user_dashboard(handle: str, db: Session = Depends(database.get_db)):
    handle = handle.strip()
    try:
        user = await get_user_profile(handle, PLATFORM, db)
        submissions = await get_cached_submissions(handle, PLATFORM, db)
        rating_history = await get_cached_rating_history(handle)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Dashboard fetch failed for %s", handle)
        raise HTTPException(status_code=502, detail=str(e))

    topic_result = analyze_topics(submissions, user.rating)
    tag_list = tag_analysis_list(submissions)
    contest_stats = analyze_contest_performance(rating_history, submissions)
    problems = await recommend_problems_async(submissions, user.rating)
    prediction = predict_rating_growth(rating_history, user.rating)

    last_10 = rating_history[-10:] if rating_history else []
    percentile_items = []
    for chg in last_10:
        contest_id = chg.get("contestId")
        rank = chg.get("rank")
        if not contest_id or not rank:
            continue
        total = await get_contest_participants(contest_id, db)
        pct = max(0.0, min(100.0, (1.0 - rank / total) * 100))
        percentile_items.append(
            schemas.ContestPercentileItem(
                contest_id=contest_id,
                contest_name=chg.get("contestName", ""),
                rank=rank,
                old_rating=chg.get("oldRating", 0),
                new_rating=chg.get("newRating", 0),
                total_participants=total,
                percentile=round(pct, 2),
            )
        )

    weak_topics = [_topic_to_weak_topic(t) for t in topic_result["weak_topics"]]
    strongest = [_topic_to_weak_topic(t) for t in topic_result["strongest_topics"]]
    weakest = [_topic_to_weak_topic(t) for t in topic_result["weakest_topics"]]

    topic_recs = [
        f"Practice {r['tag']} — success rate {round(r['ac_rate'] * 100)}%, target difficulty {r['suggested_difficulty']}"
        for r in topic_result["recommendations"]
    ]

    analysis = schemas.AnalysisResponse(
        handle=handle,
        total_submissions=topic_result["total_submissions"],
        weak_topics=weak_topics,
        strongest_topics=strongest,
        weakest_topics=weakest,
        recommendations=[
            schemas.Recommendation(**r) for r in topic_result["recommendations"]
        ],
        topic_recommendations=topic_recs,
    )

    return schemas.UserDashboardResponse(
        handle=handle,
        rating=user.rating,
        max_rating=user.max_rating,
        analysis=analysis,
        tag_analysis=[schemas.TagAnalysisItem(**t) for t in tag_list],
        percentile=percentile_items,
        contest_analytics=schemas.ContestAnalyticsResponse(**contest_stats),
        problem_recommendations=[schemas.ProblemRecommendation(**p) for p in problems],
        rating_prediction=schemas.RatingPredictionResponse(**prediction),
    )


@router.get("/users/{handle}/tag-analysis", response_model=List[schemas.TagAnalysisItem])
async def get_tag_analysis(handle: str, db: Session = Depends(database.get_db)):
    handle = handle.strip()
    try:
        submissions = await get_cached_submissions(handle, PLATFORM, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return [schemas.TagAnalysisItem(**t) for t in tag_analysis_list(submissions)]


@router.get("/users/{handle}/percentile", response_model=List[schemas.ContestPercentileItem])
async def get_percentile(handle: str, db: Session = Depends(database.get_db)):
    handle = handle.strip()
    try:
        rating_history = await get_cached_rating_history(handle)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    last_10 = rating_history[-10:] if rating_history else []
    result = []
    for chg in last_10:
        contest_id = chg.get("contestId")
        rank = chg.get("rank")
        if not contest_id or not rank:
            continue
        total = await get_contest_participants(contest_id, db)
        pct = max(0.0, min(100.0, (1.0 - rank / total) * 100))
        result.append(
            schemas.ContestPercentileItem(
                contest_id=contest_id,
                contest_name=chg.get("contestName", ""),
                rank=rank,
                old_rating=chg.get("oldRating", 0),
                new_rating=chg.get("newRating", 0),
                total_participants=total,
                percentile=round(pct, 2),
            )
        )
    return result


@router.get(
    "/users/{handle}/contest-analytics",
    response_model=schemas.ContestAnalyticsResponse,
)
async def get_contest_analytics(handle: str, db: Session = Depends(database.get_db)):
    handle = handle.strip()
    rating_history = await get_cached_rating_history(handle)
    submissions = await get_cached_submissions(handle, PLATFORM, db)
    stats = analyze_contest_performance(rating_history, submissions)
    return schemas.ContestAnalyticsResponse(**stats)


@router.get(
    "/users/{handle}/recommendations",
    response_model=List[schemas.ProblemRecommendation],
)
async def get_recommendations(
    handle: str,
    limit: int = Query(10, ge=1, le=25),
    db: Session = Depends(database.get_db),
):
    handle = handle.strip()
    user = await get_user_profile(handle, PLATFORM, db)
    submissions = await get_cached_submissions(handle, PLATFORM, db)
    problems = await recommend_problems_async(submissions, user.rating, limit=limit)
    return [schemas.ProblemRecommendation(**p) for p in problems]


@router.get(
    "/users/{handle}/rating-prediction",
    response_model=schemas.RatingPredictionResponse,
)
async def get_rating_prediction(handle: str, db: Session = Depends(database.get_db)):
    handle = handle.strip()
    user = await get_user_profile(handle, PLATFORM, db)
    rating_history = await get_cached_rating_history(handle)
    prediction = predict_rating_growth(rating_history, user.rating)
    return schemas.RatingPredictionResponse(**prediction)


async def _build_rival_stats(handle: str, db: Session) -> schemas.RivalStats:
    user_info = await get_user_info_cached(handle)
    submissions = await get_cached_submissions(handle, PLATFORM, db)
    rating_history = await get_cached_rating_history(handle)
    contest_stats = analyze_contest_performance(rating_history, submissions)

    strongest, weakest, solved_count = rival_tag_stats(submissions)
    growth = contest_stats.get("total_rating_growth", 0)

    return schemas.RivalStats(
        handle=handle,
        rating=user_info.get("rating"),
        max_rating=user_info.get("maxRating"),
        rank=user_info.get("rank"),
        total_contests=len(rating_history) if rating_history else 0,
        problems_solved=solved_count,
        strongest_tags=[
            schemas.RivalTagInfo(tag=x["tag"], ac_rate=round(x["ac_rate"], 2))
            for x in strongest
        ],
        weakest_tags=[
            schemas.RivalTagInfo(tag=x["tag"], ac_rate=round(x["ac_rate"], 2))
            for x in weakest
        ],
        rating_growth=growth,
        consistency_score=contest_stats.get("consistency_score"),
    )


def _comparison_insights(r1: schemas.RivalStats, r2: schemas.RivalStats) -> List[str]:
    insights = []
    if r1.rating and r2.rating:
        diff = r1.rating - r2.rating
        if abs(diff) >= 100:
            leader = r1.handle if diff > 0 else r2.handle
            insights.append(f"{leader} leads by {abs(diff)} rating points")

    if r1.rating_growth is not None and r2.rating_growth is not None:
        if r1.rating_growth > r2.rating_growth + 100:
            insights.append(f"{r1.handle} shows stronger long-term rating growth")
        elif r2.rating_growth > r1.rating_growth + 100:
            insights.append(f"{r2.handle} shows stronger long-term rating growth")

    if r1.consistency_score and r2.consistency_score:
        if r1.consistency_score > r2.consistency_score + 15:
            insights.append(f"{r1.handle} has more consistent contest performance")
        elif r2.consistency_score > r1.consistency_score + 15:
            insights.append(f"{r2.handle} has more consistent contest performance")

    if r1.problems_solved > r2.problems_solved * 1.5:
        insights.append(f"{r1.handle} has solved significantly more problems")
    elif r2.problems_solved > r1.problems_solved * 1.5:
        insights.append(f"{r2.handle} has solved significantly more problems")

    return insights[:5]


@router.get("/compare", response_model=schemas.RivalComparisonResponse)
async def compare_rivals(
    handle1: str = Query(..., min_length=1),
    handle2: str = Query(..., min_length=1),
    db: Session = Depends(database.get_db),
):
    handle1 = handle1.strip()
    handle2 = handle2.strip()
    try:
        rival1 = await _build_rival_stats(handle1, db)
        rival2 = await _build_rival_stats(handle2, db)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    return schemas.RivalComparisonResponse(
        rival1=rival1,
        rival2=rival2,
        insights=_comparison_insights(rival1, rival2),
    )
