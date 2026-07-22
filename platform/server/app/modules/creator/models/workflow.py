from datetime import datetime, timezone
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    READY_FOR_REVIEW = "ready_for_review"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class PublishingWorkflowModel(AuditModel):
    """Represents a draft's publishing lifecycle containing moderation reviews, status flags, and timeline transition histories."""

    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    draft_id: PyObjectId
    status: WorkflowStatus = WorkflowStatus.DRAFT
    reviewer_id: Optional[str] = None
    notes: Optional[str] = None
    history: List[Dict[str, Any]] = Field(default_factory=list)  # Transition entries: {"from_status": str, "to_status": str, "changed_at": str, "changed_by": str, "notes": str}
