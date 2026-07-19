from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field
from app.models.base import AuditModel, PyObjectId

class AttemptStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class LearningAttemptModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    session_id: Optional[PyObjectId] = None
    resource_id: str
    resource_type: str  # topic | content | quiz | practice | notes etc. (generic)
    status: AttemptStatus = AttemptStatus.IN_PROGRESS
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    score: Optional[float] = None
    response_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
