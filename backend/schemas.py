from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class UserBase(BaseModel):
    handle: str
    platform: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    rating: Optional[int] = None
    max_rating: Optional[int] = None

    class Config:
        from_attributes = True

class WeakTopic(BaseModel):
    topic: str
    attempted: int
    solved: int
    success_rate: float

class AnalysisResponse(BaseModel):
    handle: str
    total_submissions: int
    weak_topics: List[WeakTopic]
    recommendations: List[Dict[str, Any]]
