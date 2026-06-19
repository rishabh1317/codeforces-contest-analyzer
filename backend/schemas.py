from pydantic import BaseModel, Field
from typing import List, Optional


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
    avg_problem_rating: Optional[int] = None
    relative_performance_score: Optional[float] = None


class Recommendation(BaseModel):
    tag: str
    ac_rate: float
    suggested_difficulty: int
    action: str
    suggested_url: str


class TagAnalysisItem(BaseModel):
    tag: str
    total: int
    solved: int
    ac_rate: float
    avg_difficulty: int


class ContestPercentileItem(BaseModel):
    contest_id: int
    contest_name: str
    rank: int
    old_rating: int
    new_rating: int
    total_participants: int
    percentile: float


class RivalTagInfo(BaseModel):
    tag: str
    ac_rate: float


class RivalStats(BaseModel):
    handle: str
    rating: Optional[int] = None
    max_rating: Optional[int] = None
    rank: Optional[str] = None
    total_contests: int
    problems_solved: int
    strongest_tags: List[RivalTagInfo]
    weakest_tags: List[RivalTagInfo]
    rating_growth: Optional[int] = None
    consistency_score: Optional[float] = None


class RivalComparisonResponse(BaseModel):
    rival1: RivalStats
    rival2: RivalStats
    insights: List[str] = []


class ProblemRecommendation(BaseModel):
    contest_id: Optional[int] = None
    index: Optional[str] = None
    name: str
    rating: Optional[int] = None
    tags: List[str] = []
    url: str
    reason: str
    difficulty_progression: str


class RatingTimelineItem(BaseModel):
    contest_name: str
    rating: int
    old_rating: int
    rating_change: int


class RankTimelineItem(BaseModel):
    contest_name: str
    rank: int


class ContestAnalyticsResponse(BaseModel):
    total_contests: int
    current_rating: Optional[int] = None
    max_rating: Optional[int] = None
    total_rating_growth: int
    avg_rating_change: float
    positive_contests: int
    negative_contests: int
    consistency_score: float
    avg_days_between_contests: float
    contests_per_year: float
    rating_timeline: List[RatingTimelineItem]
    rank_timeline: List[RankTimelineItem]
    upsolve_count: int
    upsolve_rate: float
    summary: str


class RatingPredictionResponse(BaseModel):
    current_rating: int
    predicted_rating_low: int
    predicted_rating_high: int
    predicted_rating_mid: int
    confidence_score: float
    contests_analyzed: int
    trend: str
    monthly_growth_estimate: float = 0.0
    suggested_improvements: List[str]


class AnalysisResponse(BaseModel):
    handle: str
    total_submissions: int
    weak_topics: List[WeakTopic]
    strongest_topics: List[WeakTopic] = []
    weakest_topics: List[WeakTopic] = []
    recommendations: List[Recommendation]
    topic_recommendations: List[str] = []


class UserDashboardResponse(BaseModel):
    handle: str
    rating: Optional[int] = None
    max_rating: Optional[int] = None
    analysis: AnalysisResponse
    tag_analysis: List[TagAnalysisItem]
    percentile: List[ContestPercentileItem]
    contest_analytics: ContestAnalyticsResponse
    problem_recommendations: List[ProblemRecommendation]
    rating_prediction: RatingPredictionResponse
