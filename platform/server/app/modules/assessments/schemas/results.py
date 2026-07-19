from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.base import MongoBaseModel, PyObjectId

class AssessmentResultResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    assessment_id: str
    session_id: str
    score: float
    passed: bool
    duration_seconds: int
    evaluation_details: Dict[str, Any]
    strengths: List[str]
    weaknesses: List[str]
    completed_at: datetime
    metadata: Dict[str, Any]
