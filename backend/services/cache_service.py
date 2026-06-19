"""Unified caching layer for Codeforces user data."""

import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

import models
from services.codeforces import (
    get_user_info,
    get_user_rating_history,
    get_user_submissions,
)

logger = logging.getLogger(__name__)

CACHE_TTL_MINUTES = 5


async def get_cached_submissions(
    handle: str, platform: str, db: Session
) -> List[Dict[str, Any]]:
    now = datetime.utcnow()
    cache = (
        db.query(models.AnalysisCache)
        .filter(
            models.AnalysisCache.handle == handle,
            models.AnalysisCache.platform == platform,
        )
        .first()
    )

    if cache and (now - cache.last_updated) < timedelta(minutes=CACHE_TTL_MINUTES):
        try:
            return json.loads(cache.cached_json)
        except json.JSONDecodeError:
            logger.warning("Invalid cache JSON for handle=%s", handle)

    submissions = await get_user_submissions(handle)
    payload = json.dumps(submissions)

    if cache:
        cache.cached_json = payload
        cache.last_updated = now
    else:
        db.add(
            models.AnalysisCache(
                handle=handle,
                platform=platform,
                cached_json=payload,
                last_updated=now,
            )
        )
    db.commit()
    return submissions


async def get_user_profile(handle: str, platform: str, db: Session) -> models.User:
    now = datetime.utcnow()
    user = (
        db.query(models.User)
        .filter(models.User.handle == handle, models.User.platform == platform)
        .first()
    )
    user_info = await get_user_info(handle)

    if not user:
        user = models.User(
            handle=handle,
            platform=platform,
            rating=user_info.get("rating"),
            max_rating=user_info.get("maxRating"),
            last_updated=now,
        )
        db.add(user)
    else:
        user.rating = user_info.get("rating")
        user.max_rating = user_info.get("maxRating")
        user.last_updated = now

    db.commit()
    db.refresh(user)
    return user


async def get_cached_rating_history(handle: str) -> List[Dict[str, Any]]:
    return await get_user_rating_history(handle)


async def get_user_info_cached(handle: str) -> Dict[str, Any]:
    return await get_user_info(handle)
