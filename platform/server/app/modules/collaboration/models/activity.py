from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import MongoBaseModel, PyObjectId

class CollaborationActivityModel(MongoBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    team_id: Optional[PyObjectId] = None
    resource_id: str
    resource_type: str
    actor_id: PyObjectId
    action_type: str  # assigned | commented | status_updated
    description: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CollaborationNotificationModel(MongoBaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    recipient_id: PyObjectId
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    is_read: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
