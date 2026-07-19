from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from app.models.base import AuditModel, PyObjectId

class MembershipRole(str, Enum):
    OWNER = "owner"
    COLLABORATOR = "collaborator"
    REVIEWER = "reviewer"

class MembershipStatus(str, Enum):
    ACTIVE = "active"
    INVITED = "invited"
    REJECTED = "rejected"

class TeamModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    description: Optional[str] = None
    owner_id: PyObjectId

class TeamMembershipModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    team_id: PyObjectId
    user_id: PyObjectId
    role: MembershipRole = MembershipRole.COLLABORATOR
    status: MembershipStatus = MembershipStatus.INVITED
    invited_by: Optional[PyObjectId] = None
