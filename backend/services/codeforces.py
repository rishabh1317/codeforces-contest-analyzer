import httpx
import time
from typing import Dict, Any, List

from fastapi import HTTPException
from config import settings

_cache = {}
CACHE_TTL = 300

def get_cached(key: str):
    if key in _cache:
        val, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return val
    return None

def set_cached(key: str, val: Any):
    _cache[key] = (val, time.time())


async def get_user_info(handle: str) -> Dict[str, Any]:
    cache_key = f"user:{handle}"
    cached_val = get_cached(cache_key)
    if cached_val is not None:
        return cached_val

    url = f"{settings.cf_api_base}/user.info?handles={handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and len(data.get("result", [])) > 0:
                result = data["result"][0]
                set_cached(cache_key, result)
                return result
            else:
                raise HTTPException(status_code=502, detail="Codeforces API error: " + data.get("comment", "Unknown error"))
        else:
            raise HTTPException(status_code=502, detail=f"Codeforces API returned status {response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Codeforces API unavailable: {str(e)}")

async def get_user_submissions(handle: str) -> List[Dict[str, Any]]:
    cache_key = f"submissions:{handle}"
    cached_val = get_cached(cache_key)
    if cached_val is not None:
        return cached_val

    url = f"{settings.cf_api_base}/user.status?handle={handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                result = data.get("result", [])
                set_cached(cache_key, result)
                return result
            else:
                raise HTTPException(status_code=502, detail="Codeforces API error: " + data.get("comment", "Unknown error"))
        else:
            raise HTTPException(status_code=502, detail=f"Codeforces API returned status {response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Codeforces API unavailable: {str(e)}")

async def get_user_rating_history(handle: str) -> List[Dict[str, Any]]:
    cache_key = f"rating_history:{handle}"
    cached_val = get_cached(cache_key)
    if cached_val is not None:
        return cached_val

    url = f"{settings.cf_api_base}/user.rating?handle={handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                result = data.get("result", [])
                set_cached(cache_key, result)
                return result
            else:
                raise HTTPException(status_code=502, detail="Codeforces API error: " + data.get("comment", "Unknown error"))
        else:
            raise HTTPException(status_code=502, detail=f"Codeforces API returned status {response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Codeforces API unavailable: {str(e)}")

async def get_contest_participants_from_api(contest_id: int) -> int:
    url = f"{settings.cf_api_base}/contest.standings?contestId={contest_id}&from=1&count=1"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                contest = data.get("result", {}).get("contest", {})
                return contest.get("participantsCount", 1)
        return 1
    except Exception:
        return 1


async def get_problemset() -> List[Dict[str, Any]]:
    cache_key = "problemset:all"
    cached_val = get_cached(cache_key)
    if cached_val is not None:
        return cached_val

    url = f"{settings.cf_api_base}/problemset.problems"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                problems = data.get("result", {}).get("problems", [])
                set_cached(cache_key, problems)
                return problems
        return []
    except httpx.RequestError:
        return []
