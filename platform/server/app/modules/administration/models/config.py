from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from app.models.base import MongoBaseModel

class PlatformConfigModel(MongoBaseModel):
    id: str = Field(default="global", alias="_id")
    maintenance_mode: bool = False
    allowed_domains: List[str] = Field(default_factory=list)
    feature_flags: Dict[str, bool] = Field(default_factory=dict)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
