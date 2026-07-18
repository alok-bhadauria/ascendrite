import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class AssetStatus(str, Enum):
    UPLOADED = "uploaded"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"

class AssetModel(BaseModel):
    """
    Metadata persistent document structure for digital assets.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), alias="_id")
    owner_id: str
    owner_type: str  # user | ai_agent | service_account
    filename: str
    content_type: str
    size: int
    checksum: str
    checksum_algorithm: str = "sha256"
    storage_provider: str = "rustfs"
    storage_bucket: str = "ascendrite-assets"
    storage_key: str
    status: AssetStatus = AssetStatus.UPLOADED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Reserved Extension Metadata
    logical_location: Optional[str] = None
    media_dimensions: Optional[Dict[str, int]] = None
    duration_seconds: Optional[float] = None
    thumbnail_storage_key: Optional[str] = None
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
