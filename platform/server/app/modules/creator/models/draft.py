from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class ValidationStatus(str, Enum):
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"

class DraftResourceModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    resource_type: str  # "topic", "content", "question", "assessment"
    resource_id: Optional[str] = None  # links to published production entity once published
    content: Dict[str, Any] = Field(default_factory=dict)
    validation_status: ValidationStatus = ValidationStatus.PENDING
    validation_errors: List[str] = Field(default_factory=list)
    created_by: PyObjectId
