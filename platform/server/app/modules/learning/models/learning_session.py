from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field
from app.models.base import AuditModel, PyObjectId

class SessionStatus(str, Enum):
    ACTIVE = "active"
    CLOSED = "closed"

class LearningSessionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    status: SessionStatus = SessionStatus.ACTIVE
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
