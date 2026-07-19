from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class LearningHistoryItem(BaseModel):
    event_type: str  # "session_start", "session_close", "attempt_complete", "experience_start", "experience_complete", etc.
    timestamp: datetime
    description: str
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    score: Optional[float] = None

class EducationalRecommendation(BaseModel):
    type: str  # "resume_experience", "continue_topic", "retry_assessment", "review_weakness"
    title: str
    reason: str
    resource_id: str
    resource_type: str

class WeakAreaResponse(BaseModel):
    topic_id: str
    average_score: float
    attempts_count: int
    recommendation: str

class LearnerDashboardResponse(BaseModel):
    next_study_topic_id: Optional[str] = None
    last_active_session_id: Optional[str] = None
    last_attempt_at: Optional[datetime] = None
    mastered_topics_count: int = 0
    needs_review_count: int = 0
    total_sessions_count: int = 0
    total_attempts_count: int = 0
