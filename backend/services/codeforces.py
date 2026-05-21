import httpx
from typing import Dict, Any, List

from fastapi import HTTPException

CODEFORCES_API_URL = "https://codeforces.com/api"


async def get_user_info(handle: str) -> Dict[str, Any]:
    url = f"{CODEFORCES_API_URL}/user.info?handles={handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and len(data.get("result", [])) > 0:
                return data["result"][0]
            else:
                raise HTTPException(status_code=502, detail="Codeforces API error: " + data.get("comment", "Unknown error"))
        else:
            raise HTTPException(status_code=502, detail=f"Codeforces API returned status {response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Codeforces API unavailable: {str(e)}")

async def get_user_submissions(handle: str) -> List[Dict[str, Any]]:
    url = f"{CODEFORCES_API_URL}/user.status?handle={handle}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return data.get("result", [])
            else:
                raise HTTPException(status_code=502, detail="Codeforces API error: " + data.get("comment", "Unknown error"))
        else:
            raise HTTPException(status_code=502, detail=f"Codeforces API returned status {response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Codeforces API unavailable: {str(e)}")
