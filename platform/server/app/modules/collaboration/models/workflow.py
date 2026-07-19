from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class CollaborationAssignmentModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    resource_id: str
    resource_type: str
    assignee_id: PyObjectId
    assigned_by: PyObjectId
    status: str = "assigned"  # assigned | in_progress | completed

class CollaborationCommentModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    resource_id: str
    author_id: PyObjectId
    content: str
