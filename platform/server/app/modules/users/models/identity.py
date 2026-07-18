from datetime import datetime
from typing import Optional
from pydantic import Field
from app.models.base import AuditModel, PyObjectId

class UserIdentityModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    provider: str = "local"  # local | google | github
    provider_user_id: str   # Normalized email or OAuth sub ID
    password_hash: Optional[str] = None
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
