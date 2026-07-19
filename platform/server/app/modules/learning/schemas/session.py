from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from app.models.base import PyObjectId, MongoBaseModel

class LearningSessionStartRequest(BaseModel):
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningSessionResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningAttemptStartRequest(BaseModel):
    session_id: Optional[str] = None
    resource_id: str
    resource_type: str  # generic type
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningAttemptCompleteRequest(BaseModel):
    score: Optional[float] = None
    response_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class LearningAttemptResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    session_id: Optional[PyObjectId] = None
    resource_id: str
    resource_type: str
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    score: Optional[float] = None
    response_data: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
