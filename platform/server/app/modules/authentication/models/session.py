from datetime import datetime
from typing import Optional
from pydantic import Field
from app.models.base import AuditModel, PyObjectId

class SessionModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    token_family_id: str
    refresh_token_id: str
    device_name: Optional[str] = None
    ip_address: Optional[str] = None
    is_revoked: bool = False
    revoked_reason: Optional[str] = None
    expires_at: datetime
    last_seen_at: datetime
