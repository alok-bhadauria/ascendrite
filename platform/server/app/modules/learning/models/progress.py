from datetime import datetime, timezone
from typing import List, Optional
from pydantic import Field
from app.models.base import AuditModel, PyObjectId, MongoBaseModel

class TopicProgress(MongoBaseModel):
    topic_id: str
    completed_at: datetime = datetime.now(timezone.utc)
    duration_seconds: int = 0
    quiz_score: float = 0.0

class ProgressModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    subject_id: str
    completed_topics: List[TopicProgress] = Field(default_factory=list)
    last_active_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
