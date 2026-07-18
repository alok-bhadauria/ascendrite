from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool
