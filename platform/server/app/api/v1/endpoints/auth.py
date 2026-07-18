from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Response, status
import httpx
from pydantic import BaseModel
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.modules.users.models.user import UserModel
from app.modules.users.schemas.user import UserCreate, UserLogin, UserResponse
from app.modules.authentication.services.auth import AuthService
from app.api.v1.dependencies import get_user_repository, get_current_user
from app.modules.users.repositories.user import UserRepository

router = APIRouter()

class GoogleLoginRequest(BaseModel):
    id_token: str

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, user_repo: UserRepository = Depends(get_user_repository)):
    """Register a new student account using standard credentials validation"""
    auth_service = AuthService(user_repo)
    user = await auth_service.register_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user account with this email address already exists."
        )
    return user

@router.post("/login")
async def login(
    response: Response,
    login_data: UserLogin,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Authenticate credentials and establish HttpOnly secure session cookies"""
    auth_service = AuthService(user_repo)
    user = await auth_service.authenticate_user(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email address or password."
        )
    
    access_token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE,
        max_age=settings.JWT_EXPIRE_MINUTES * 60
    )
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }

@router.post("/logout")
async def logout(response: Response):
    """Invalidate session cache and delete HttpOnly cookies"""
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    """Fetch the active user context profile details"""
    return current_user

@router.post("/google")
async def google_login(
    response: Response,
    payload: GoogleLoginRequest,
    user_repo: UserRepository = Depends(get_user_repository)
):
    """Authenticate via Google SSO credentials and establish session context"""
    try:
        # Query Google API tokeninfo endpoint
        async with httpx.AsyncClient() as client:
            google_resp = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={payload.id_token}",
                timeout=5.0
            )
            if google_resp.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Google OAuth token."
                )
            google_info = google_resp.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google authentication service connection failure: {e}"
        )
        
    google_id = google_info.get("sub")
    email = google_info.get("email")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email scope was not returned by Google authorization context."
        )
        
    user = await user_repo.get_by_email(email)
    if not user:
        # Register new Google SSO user
        new_user = UserModel(
            email=email.lower(),
            password_hash=None,
            first_name=google_info.get("given_name", "Google"),
            last_name=google_info.get("family_name", "User"),
            role="Student",
            google_id=google_id,
            profile_picture_url=google_info.get("picture")
        )
        user = await user_repo.create(new_user)
    else:
        # Link Google ID to existing profile if missing
        if not user.google_id:
            user.google_id = google_id
            await user_repo.update(user.id, user)
            
    access_token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE,
        max_age=settings.JWT_EXPIRE_MINUTES * 60
    )
    
    return {
        "message": "Google Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.model_validate(user)
    }
