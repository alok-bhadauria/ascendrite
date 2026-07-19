from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class LearningGoalModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    target_date: datetime
    topic_ids: List[str] = Field(default_factory=list)
    status: str = "pending"  # pending | achieved | missed
    metadata: Dict[str, Any] = Field(default_factory=dict)
