from fastapi import Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, Field
from typing import List

from app.core.routing import APIRouter
from app.api.v1.dependencies import get_auth_service, get_current_user
from app.modules.users.schemas.user import UserCreate, UserLogin, UserResponse
from app.modules.users.models.user import UserModel
from app.modules.authentication.services.auth import AuthService

router = APIRouter()

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

class SessionResponse(BaseModel):
    id: str
    device_name: str
    ip_address: str
    expires_at: str
    last_seen_at: str
    is_active: bool

@router.post("/signup", status_code=status.HTTP_201_CREATED, tags=["Identity"])
async def signup(user_data: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    """Register a new platform user profile and credential entity"""
    user = await auth_service.register_user(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name
    )
    return UserResponse(
        id=str(user.id),
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        is_active=user.is_active
    )

@router.post("/login", tags=["Identity"])
async def login(
    response: Response,
    request: Request,
    login_data: UserLogin,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Authenticate user and establish stateful cookie and token sessions"""
    user_agent = request.headers.get("User-Agent", "Unknown")
    ip_address = request.client.host if request.client else "Unknown"
    
    user, access_token, refresh_token = await auth_service.login_user(
        email=login_data.email,
        password=login_data.password,
        user_agent=user_agent,
        ip_address=ip_address
    )

    # Set cookies for web frontends
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set True in production SSL setup
        samesite="lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax"
    )

    return {
        "user": UserResponse(
            id=str(user.id),
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=user.role,
            is_active=user.is_active
        ),
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@router.post("/refresh", tags=["Identity"])
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Rotate refresh token and issue new access token"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        # Check header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            refresh_token = auth_header.split(" ")[1]

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing.")

    user_agent = request.headers.get("User-Agent", "Unknown")
    ip_address = request.client.host if request.client else "Unknown"

    access_token, new_refresh_token = await auth_service.refresh_tokens(
        refresh_token=refresh_token,
        user_agent=user_agent,
        ip_address=ip_address
    )

    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax")
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, secure=False, samesite="lax")

    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token
    }

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["Identity"])
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Logout user and revoke refresh token families"""
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        await auth_service.logout_user(refresh_token)
    
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

@router.get("/sessions", response_model=List[SessionResponse], tags=["Identity"])
async def list_sessions(
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """List all active sessions and locations for current user"""
    sessions = await auth_service.get_active_sessions(str(current_user.id))
    return [
        SessionResponse(
            id=str(s.id),
            device_name=s.device_name or "Unknown",
            ip_address=s.ip_address or "Unknown",
            expires_at=s.expires_at.isoformat(),
            last_seen_at=s.last_seen_at.isoformat(),
            is_active=not s.is_revoked
        )
        for s in sessions
    ]

@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Identity"])
async def revoke_session(
    session_id: str,
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Revoke/terminate specific device session by ID"""
    await auth_service.terminate_session(str(current_user.id), session_id)

@router.delete("/sessions/revoke/other", status_code=status.HTTP_204_NO_CONTENT, tags=["Identity"])
async def revoke_other_sessions(
    request: Request,
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Revoke all other active sessions for current user"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Active refresh session context is missing.")
    await auth_service.terminate_other_sessions(str(current_user.id), refresh_token)

@router.post("/password/change", status_code=status.HTTP_204_NO_CONTENT, tags=["Identity"])
async def change_password(
    data: PasswordChangeRequest,
    current_user: UserModel = Depends(get_current_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Update current user account password"""
    await auth_service.change_password(str(current_user.id), data.current_password, data.new_password)
