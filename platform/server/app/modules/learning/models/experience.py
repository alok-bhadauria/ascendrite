from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any
from pydantic import Field
from app.models.base import AuditModel, PyObjectId

class ExperienceStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"

class LearningExperienceModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    session_id: Optional[PyObjectId] = None
    resource_id: str
    experience_type: str  # notes | revision | practice | quiz | interview etc. (generic)
    status: ExperienceStatus = ExperienceStatus.ACTIVE
    state: Dict[str, Any] = Field(default_factory=dict)
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
