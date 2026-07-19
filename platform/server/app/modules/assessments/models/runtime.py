from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AssessmentResponseItem(BaseModel):
    question_id: str
    selected_option_index: Optional[int] = None
    selected_option_indices: Optional[List[int]] = None
    text_response: Optional[str] = None
    bool_response: Optional[bool] = None
    code_response: Optional[str] = None
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    elapsed_seconds: Optional[int] = None
    confidence_level: Optional[int] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AssessmentSessionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    assessment_id: str
    status: SessionStatus = SessionStatus.ACTIVE
    responses: List[AssessmentResponseItem] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
