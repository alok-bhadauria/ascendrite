from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import Field
from app.models.base import AuditModel, PyObjectId, MongoBaseModel

class LearningStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REVIEWED = "reviewed"
    MASTERED = "mastered"

class TopicProgress(MongoBaseModel):
    topic_id: str
    status: LearningStatus = LearningStatus.COMPLETED
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    duration_seconds: int = 0
    quiz_score: float = 0.0
    confidence_score: float = 0.0
    review_count: int = 1
    last_attempt_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_attempt_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ProgressModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    subject_id: str
    completed_topics: List[TopicProgress] = Field(default_factory=list)
    last_active_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
