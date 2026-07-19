from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from app.models.base import MongoBaseModel, PyObjectId
from app.modules.creator.models.draft import ValidationStatus

class DraftCreateRequest(BaseModel):
    resource_type: str
    content: Dict[str, Any]

class DraftUpdateRequest(BaseModel):
    content: Dict[str, Any]

class DraftResourceResponse(MongoBaseModel):
    id: PyObjectId = Field(..., alias="_id")
    resource_type: str
    resource_id: Optional[str] = None
    content: Dict[str, Any]
    validation_status: ValidationStatus
    validation_errors: List[str]
    created_by: PyObjectId
