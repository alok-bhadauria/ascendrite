from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class AssessmentType(str, Enum):
    QUIZ = "quiz"
    PRACTICE = "practice"
    CODING_CHALLENGE = "coding_challenge"
    ASSIGNMENT = "assignment"
    INTERVIEW = "interview"

class AssessmentQuestionRef(BaseModel):
    question_id: str
    order: int
    marks: float = 1.0
    weight: float = 1.0
    section: Optional[str] = None
    is_mandatory: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AssessmentModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    description: str
    assessment_type: AssessmentType
    topic_id: str
    questions: List[AssessmentQuestionRef] = Field(default_factory=list)
    duration_minutes: Optional[int] = None
    passing_score: Optional[float] = None
    visibility: str = "active"  # active | inactive
    publication_status: str = "draft"  # draft | published
    metadata: Dict[str, Any] = Field(default_factory=dict)
