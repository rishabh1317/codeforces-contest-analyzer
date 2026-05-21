from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas, database
from services.codeforces import get_user_submissions, get_user_info
from services.analyzer import analyze_submissions, generate_recommendations

router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
)

from datetime import datetime, timedelta
import models
import json

@router.get("/{platform}/{handle}", response_model=schemas.AnalysisResponse)
async def get_analysis(platform: str, handle: str, db: Session = Depends(database.get_db)):
    if platform.lower() != "codeforces":
        raise HTTPException(status_code=400, detail="Only Codeforces is supported currently")

    # Check for user in DB
    user = db.query(models.User).filter(models.User.handle == handle, models.User.platform == platform).first()
    now = datetime.utcnow()

    # Use AnalysisCache for full JSON caching
    cache = db.query(models.AnalysisCache).filter(
        models.AnalysisCache.handle == handle,
        models.AnalysisCache.platform == platform
    ).first()
    submissions = []
    cache_valid = False
    if cache and (now - cache.last_updated) < timedelta(minutes=5):
        try:
            submissions = json.loads(cache.cached_json)
            cache_valid = True
        except Exception:
            submissions = []
            cache_valid = False

    if not cache_valid:
        # Fetch from API
        user_info = await get_user_info(handle)
        if not user_info:
            raise HTTPException(status_code=404, detail="Codeforces user not found")
        submissions = await get_user_submissions(handle)
        # Update or create user in DB (for rating, etc.)
        if not user:
            user = models.User(
                handle=handle,
                platform=platform,
                rating=user_info.get("rating"),
                max_rating=user_info.get("maxRating"),
                last_updated=now
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        else:
            user.rating = user_info.get("rating")
            user.max_rating = user_info.get("maxRating")
            user.last_updated = now
            db.commit()
        # Update or create cache
        if cache:
            cache.cached_json = json.dumps(submissions)
            cache.last_updated = now
        else:
            cache = models.AnalysisCache(
                handle=handle,
                platform=platform,
                cached_json=json.dumps(submissions),
                last_updated=now
            )
            db.add(cache)
        db.commit()

    if not submissions:
        return schemas.AnalysisResponse(
            handle=handle,
            total_submissions=0,
            weak_topics=[],
            recommendations=[]
        )

    # Run analysis
    analysis_results = analyze_submissions(submissions)
    recommendations = generate_recommendations(analysis_results["weak_topics"])
    return schemas.AnalysisResponse(
        handle=handle,
        total_submissions=analysis_results["total_submissions"],
        weak_topics=analysis_results["weak_topics"],
        recommendations=recommendations
    )
