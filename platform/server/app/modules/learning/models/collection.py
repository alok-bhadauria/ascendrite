from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class LearningCollectionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    collection_type: str  # bookmarks | favorites | study_list
    name: str
    resources: List[Dict[str, Any]] = Field(default_factory=list)  # List of {"resource_id": str, "resource_type": str, "added_at": str}
    metadata: Dict[str, Any] = Field(default_factory=dict)
