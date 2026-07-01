from datetime import date
from typing import List, Optional
from pydantic import Field
from models.base import AuditModel, PyObjectId, MongoBaseModel

class EducationDetail(MongoBaseModel):
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None

class SocialLinks(MongoBaseModel):
    github: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None

class UserPreferences(MongoBaseModel):
    theme: str = "dark"
    notifications_enabled: bool = True

class UserModel(AuditModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str
    password_hash: Optional[str] = None  # Nullable to support direct Google OAuth SSO
    first_name: str
    last_name: str
    role: str = "Student"  # Student | Contributor | Admin
    
    # Enriched Profile Fields
    profile_picture_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: str = ""
    education: List[EducationDetail] = Field(default_factory=list)
    social_links: SocialLinks = Field(default_factory=SocialLinks)
    skills: List[str] = Field(default_factory=list)
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    
    # Third-Party Auth & State Flags
    google_id: Optional[str] = None
    is_active: bool = True
