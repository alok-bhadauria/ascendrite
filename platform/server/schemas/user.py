from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class EducationDetailSchema(BaseModel):
    institution: str = Field(..., min_length=1, max_length=100)
    degree: Optional[str] = Field(default=None, max_length=100)
    field_of_study: Optional[str] = Field(default=None, max_length=100)
    graduation_year: Optional[int] = Field(default=None, ge=1900, le=2100)

class SocialLinksSchema(BaseModel):
    github: Optional[str] = Field(default=None, max_length=200)
    linkedin: Optional[str] = Field(default=None, max_length=200)
    twitter: Optional[str] = Field(default=None, max_length=200)

class UserPreferencesSchema(BaseModel):
    theme: str = Field(default="dark", max_length=50)
    notifications_enabled: bool = True

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    profile_picture_url: Optional[str] = None
    date_of_birth: Optional[date] = None
    bio: Optional[str] = Field(default=None, max_length=500)
    education: Optional[List[EducationDetailSchema]] = None
    social_links: Optional[SocialLinksSchema] = None
    skills: Optional[List[str]] = None
    preferences: Optional[UserPreferencesSchema] = None

class UserResponse(UserBase):
    id: str
    role: str
    profile_picture_url: Optional[str]
    date_of_birth: Optional[date]
    bio: str
    education: List[EducationDetailSchema]
    social_links: SocialLinksSchema
    skills: List[str]
    preferences: UserPreferencesSchema
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
