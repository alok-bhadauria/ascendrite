from datetime import datetime, timezone
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class AssetAttachmentModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    draft_id: PyObjectId
    asset_id: str
    attached_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
