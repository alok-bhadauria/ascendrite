from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
from typing import List
from jose import jwt
import httpx

from app.core.routing import APIRouter
from app.core.config import settings
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

@router.get("/me", response_model=UserResponse, tags=["Identity"])
async def get_me(current_user: UserModel = Depends(get_current_user)):
    """Retrieve active user profile details from the session context"""
    return UserResponse(
        id=str(current_user.id),
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        role=current_user.role,
        is_active=current_user.is_active
    )

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
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE
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

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE
    )

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

@router.get("/google/login", tags=["OAuth"])
async def google_login():
    """Redirect user to Google's OAuth consent screen"""
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth settings are not configured on the server."
        )
    
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        "response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"
        "&scope=openid%20email%20profile"
        "&access_type=offline"
        "&prompt=consent"
    )
    return RedirectResponse(url=google_auth_url)

@router.get("/google/callback", tags=["OAuth"])
async def google_callback(
    request: Request,
    response: Response,
    code: str = None,
    error: str = None,
    auth_service: AuthService = Depends(get_auth_service)
):
    """Receive code redirect from Google, verify profile, and set authorization cookies"""
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth authorization failed: {error}"
        )
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing OAuth verification code from Google."
        )

    # 1. Exchange authorization code for ID/access tokens
    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code"
            }
        )
        if token_res.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Google token exchange failed: {token_res.text}"
            )
        
        token_data = token_res.json()
        id_token = token_data.get("id_token")
        if not id_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google OAuth response did not include a valid id_token."
            )

    # 2. Decode Google ID Token (which is a JWT)
    try:
        user_info = jwt.get_unverified_claims(id_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to decode Google user profile info: {str(e)}"
        )

    email = user_info.get("email")
    sub = user_info.get("sub")
    first_name = user_info.get("given_name", "OAuth")
    last_name = user_info.get("family_name", "User")

    if not email or not sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google profile payload is missing mandatory email or unique subject identifier."
        )

    # 3. Authenticate or register the user profile
    user_agent = request.headers.get("User-Agent", "Unknown")
    ip_address = request.client.host if request.client else "Unknown"

    try:
        user, access_token, refresh_token = await auth_service.login_or_register_oauth(
            provider="google",
            provider_user_id=sub,
            email=email,
            first_name=first_name,
            last_name=last_name,
            user_agent=user_agent,
            ip_address=ip_address
        )
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication pipeline registration failure: {str(ex)}"
        )

    # 4. Redirect back to frontend portal homepage /learn
    frontend_host = request.headers.get("Origin") or "http://localhost:5173"
    if "localhost:5173" not in frontend_host and "127.0.0.1:5173" not in frontend_host:
        frontend_host = "http://localhost:5173"
    
    redirect_response = RedirectResponse(url=f"{frontend_host}/learn")

    # Set cookies directly on redirect_response with path="/"
    redirect_response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE,
        path="/"
    )
    redirect_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=settings.SECURITY_COOKIE_HTTPONLY,
        secure=settings.SECURITY_COOKIE_SECURE,
        samesite=settings.SECURITY_COOKIE_SAMESITE,
        path="/"
    )
    
    return redirect_response
