from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from app.models.base import MongoBaseModel, PyObjectId
from app.modules.assessments.models.assessment import AssessmentType, AssessmentQuestionRef

class AssessmentCreate(BaseModel):
    title: str
    description: str
    assessment_type: AssessmentType
    topic_id: str
    questions: List[AssessmentQuestionRef] = Field(default_factory=list)
    duration_minutes: Optional[int] = None
    passing_score: Optional[float] = None
    visibility: str = "active"
    publication_status: str = "draft"
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AssessmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assessment_type: Optional[AssessmentType] = None
    topic_id: Optional[str] = None
    questions: Optional[List[AssessmentQuestionRef]] = None
    duration_minutes: Optional[int] = None
    passing_score: Optional[float] = None
    visibility: Optional[str] = None
    publication_status: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AssessmentResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    title: str
    description: str
    assessment_type: AssessmentType
    topic_id: str
    questions: List[AssessmentQuestionRef]
    duration_minutes: Optional[int] = None
    passing_score: Optional[float] = None
    visibility: str
    publication_status: str
    metadata: Dict[str, Any]
