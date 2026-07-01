from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class TopicProgressLog(BaseModel):
    topic_id: str
    duration_seconds: int = Field(default=0, ge=0)
    quiz_score: float = Field(default=0.0, ge=0.0, le=100.0)

class TopicProgressResponse(BaseModel):
    topic_id: str
    completed_at: datetime
    duration_seconds: int
    quiz_score: float

class SubjectProgressResponse(BaseModel):
    subject_id: str
    completion_percentage: float
    completed_topics: List[TopicProgressResponse]
    last_active_at: datetime

    class Config:
        from_attributes = True
