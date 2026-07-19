from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.base import MongoBaseModel, PyObjectId

class CollectionCreateRequest(BaseModel):
    collection_type: str
    name: str

class CollectionResourceAddRequest(BaseModel):
    resource_id: str
    resource_type: str

class LearningCollectionResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    collection_type: str
    name: str
    resources: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class GoalCreateRequest(BaseModel):
    target_date: datetime
    topic_ids: List[str]

class LearningGoalResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    user_id: PyObjectId
    target_date: datetime
    topic_ids: List[str]
    status: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
