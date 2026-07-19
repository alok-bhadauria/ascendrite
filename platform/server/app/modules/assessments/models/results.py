from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class AssessmentResultModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    assessment_id: str
    session_id: str
    score: float  # percentage score: 0.0 to 1.0
    passed: bool
    duration_seconds: int
    evaluation_details: Dict[str, Any] = Field(default_factory=dict)  # question_id -> correctness evaluation doc
    strengths: List[str] = Field(default_factory=list)  # list of tags/skills successfully answered
    weaknesses: List[str] = Field(default_factory=list)  # list of tags/skills missed
    completed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
