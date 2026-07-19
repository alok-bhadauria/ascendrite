from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.base import PyObjectId, MongoBaseModel

class LearningExperienceStartRequest(BaseModel):
    resource_id: str
    experience_type: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningStepSubmitRequest(BaseModel):
    step_data: Dict[str, Any]

class LearningExperienceCompleteRequest(BaseModel):
    score: Optional[float] = None
    response_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningExperienceResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    session_id: Optional[PyObjectId] = None
    resource_id: str
    experience_type: str
    status: str
    state: Dict[str, Any] = Field(default_factory=dict)
    start_time: datetime
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
