from typing import Optional
from pydantic import Field, EmailStr
from platform.server.models.base import AuditModel, PyObjectId

class UserModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    password_hash: str
    first_name: str
    last_name: str
    role: str = "Student" # Student | Contributor | Admin
