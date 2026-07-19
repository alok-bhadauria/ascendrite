from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.base import MongoBaseModel, PyObjectId
from app.modules.assessments.models.runtime import AssessmentResponseItem, SessionStatus

class AssessmentSessionStartRequest(BaseModel):
    assessment_id: str

class AnswerSubmitRequest(BaseModel):
    question_id: str
    selected_option_index: Optional[int] = None
    selected_option_indices: Optional[List[int]] = None
    text_response: Optional[str] = None
    bool_response: Optional[bool] = None
    code_response: Optional[str] = None
    elapsed_seconds: Optional[int] = None
    confidence_level: Optional[int] = None

class AssessmentSessionResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    assessment_id: str
    status: SessionStatus
    responses: List[AssessmentResponseItem]
    start_time: datetime
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any]
