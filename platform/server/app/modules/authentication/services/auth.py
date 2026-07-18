import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Tuple
from fastapi import status
from jose import jwt, JWTError

from app.core.config import settings
from app.core.errors import AppException, UnauthorizedException
from app.core.security import verify_password, get_password_hash
from app.modules.users.models.user import UserModel
from app.modules.users.models.identity import UserIdentityModel
from app.modules.users.repositories.user import UserRepository
from app.modules.users.repositories.identity import UserIdentityRepository
from app.modules.authentication.models.session import SessionModel
from app.modules.authentication.repositories.session import SessionRepository

logger = logging.getLogger(__name__)

def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        identity_repo: UserIdentityRepository,
        session_repo: SessionRepository
    ):
        self.user_repo = user_repo
        self.identity_repo = identity_repo
        self.session_repo = session_repo

    async def register_user(self, email: str, password: str, first_name: str, last_name: str) -> UserModel:
        normalized_email = email.lower().strip()
        
        # Check uniqueness
        existing_user = await self.user_repo.get_by_email(normalized_email)
        if existing_user:
            raise AppException(
                message="A user with this email address already exists.",
                code="CONFLICT_EMAIL_DUPLICATE",
                status_code=status.HTTP_409_CONFLICT
            )

        # Create Profile
        new_user = UserModel(
            email=normalized_email,
            first_name=first_name,
            last_name=last_name,
            role="Student"
        )
        created_user = await self.user_repo.create(new_user)

        # Create Identity Credentials
        pwd_hash = get_password_hash(password)
        new_identity = UserIdentityModel(
            user_id=created_user.id,
            provider="local",
            provider_user_id=normalized_email,
            password_hash=pwd_hash
        )
        await self.identity_repo.create(new_identity)

        logger.info(f"User identity and profile registered: user_id={created_user.id}")
        return created_user

    async def login_user(
        self,
        email: str,
        password: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[UserModel, str, str]:
        normalized_email = email.lower().strip()
        
        # 1. Fetch identity credentials
        identity = await self.identity_repo.get_by_provider_id("local", normalized_email)
        
        # Generic error message to prevent account enumeration
        generic_error = AppException(
            message="Invalid email or password credentials.",
            code="AUTH_INVALID_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
        
        if not identity:
            logger.warning(f"Login failed: Identity not found for email: {normalized_email}")
            raise generic_error

        # 2. Check Lockout State
        now = datetime.now(timezone.utc)
        locked_until = ensure_utc(identity.locked_until)
        if locked_until and locked_until > now:
            logger.warning(f"Login rejected: Account is locked out: {normalized_email}")
            raise AppException(
                message="Account has been temporarily locked out due to multiple failed login attempts.",
                code="AUTH_ACCOUNT_LOCKED",
                status_code=status.HTTP_423_LOCKED
            )

        # 3. Verify Password
        if not verify_password(password, identity.password_hash):
            identity.failed_login_attempts += 1
            if identity.failed_login_attempts >= 5:
                identity.locked_until = now + timedelta(minutes=15)
                logger.warning(f"Lockout triggered for user identity: {normalized_email}")
            await self.identity_repo.update(identity.id, identity)
            raise generic_error

        # 4. Reset lockouts on success
        identity.failed_login_attempts = 0
        identity.locked_until = None
        identity.last_login_at = now
        await self.identity_repo.update(identity.id, identity)

        # 5. Fetch Profile
        user = await self.user_repo.get_by_id(identity.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("Account is inactive or disabled.")

        # 6. Create Stateful Session & JWTs
        token_family_id = str(uuid.uuid4())
        refresh_token_id = str(uuid.uuid4())
        
        # Access token expiration (e.g. 15m)
        access_exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        # Refresh token expiration (e.g. 7 days)
        refresh_exp = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)

        access_payload = {"exp": access_exp, "sub": str(user.id), "type": "access"}
        refresh_payload = {
            "exp": refresh_exp,
            "sub": str(user.id),
            "jti": refresh_token_id,
            "family": token_family_id,
            "type": "refresh"
        }

        access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        session = SessionModel(
            user_id=str(user.id),
            token_family_id=token_family_id,
            refresh_token_id=refresh_token_id,
            device_name=user_agent,
            ip_address=ip_address,
            expires_at=refresh_exp,
            last_seen_at=now
        )
        await self.session_repo.create(session)

        return user, access_token, refresh_token

    async def refresh_tokens(
        self,
        refresh_token: str,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> Tuple[str, str]:
        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            jti: str = payload.get("jti")
            family: str = payload.get("family")
            token_type: str = payload.get("type")
            if token_type != "refresh" or not user_id or not jti or not family:
                raise UnauthorizedException("Invalid refresh token payload parameters.")
        except JWTError:
            raise UnauthorizedException("Invalid refresh token signature or expired payload.")

        # 1. Fetch Session
        session = await self.session_repo.get_by_refresh_token_id(jti)
        now = datetime.now(timezone.utc)

        # 2. Replay/Theft Detection:
        if not session:
            # Replay Detected! Revoke everything in this token family immediately.
            await self.session_repo.revoke_family(family, "replay_attack_detected")
            logger.critical(f"SECURITY BREACH: Refresh token replay attack detected! Family revoked: {family}")
            raise UnauthorizedException("Session reuse or theft detected. All active family tokens revoked.")

        if session.is_revoked:
            await self.session_repo.revoke_family(family, "family_compromised")
            raise UnauthorizedException("Session has been compromised or revoked.")

        expires_at = ensure_utc(session.expires_at)
        if expires_at < now:
            raise UnauthorizedException("Refresh session has expired.")

        # 3. Rotate Refresh Token
        new_refresh_token_id = str(uuid.uuid4())
        refresh_exp = now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        access_exp = now + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

        new_access_payload = {"exp": access_exp, "sub": str(user_id), "type": "access"}
        new_refresh_payload = {
            "exp": refresh_exp,
            "sub": str(user_id),
            "jti": new_refresh_token_id,
            "family": family,
            "type": "refresh"
        }

        new_access_token = jwt.encode(new_access_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        new_refresh_token = jwt.encode(new_refresh_payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        # Revoke current token usage
        session.is_revoked = True
        session.revoked_reason = "rotated"
        await self.session_repo.update(session.id, session)

        # Create rotated session state
        new_session = SessionModel(
            user_id=str(user_id),
            token_family_id=family,
            refresh_token_id=new_refresh_token_id,
            device_name=user_agent or session.device_name,
            ip_address=ip_address or session.ip_address,
            expires_at=refresh_exp,
            last_seen_at=now
        )
        await self.session_repo.create(new_session)

        return new_access_token, new_refresh_token

    async def logout_user(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            jti: str = payload.get("jti")
            family: str = payload.get("family")
            if jti:
                session = await self.session_repo.get_by_refresh_token_id(jti)
                if session:
                    session.is_revoked = True
                    session.revoked_reason = "logout"
                    await self.session_repo.update(session.id, session)
                if family:
                    await self.session_repo.revoke_family(family, "logout")
        except JWTError:
            pass

    async def get_active_sessions(self, user_id: str) -> List[SessionModel]:
        return await self.session_repo.get_active_by_user_id(user_id)

    async def terminate_session(self, user_id: str, session_id: str):
        session = await self.session_repo.get_by_id(session_id)
        if not session or session.user_id != user_id:
            raise AppException("Session not found or forbidden access.", code="NOT_FOUND_SESSION", status_code=status.HTTP_404_NOT_FOUND)
        
        session.is_revoked = True
        session.revoked_reason = "revoked_by_user"
        await self.session_repo.update(session.id, session)

    async def terminate_other_sessions(self, user_id: str, active_refresh_token: str):
        try:
            payload = jwt.decode(active_refresh_token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            family: str = payload.get("family")
            if family:
                await self.session_repo.revoke_others(user_id, family, "revoked_by_user")
        except JWTError:
            raise UnauthorizedException("Invalid active refresh token context.")

    async def change_password(self, user_id: str, current_pass: str, new_pass: str):
        identity = await self.identity_repo.get_by_user_id(user_id)
        if not identity or not verify_password(current_pass, identity.password_hash):
            raise AppException("Invalid current password entered.", code="AUTH_INVALID_PASSWORD", status_code=status.HTTP_400_BAD_REQUEST)
        
        identity.password_hash = get_password_hash(new_pass)
        await self.identity_repo.update(identity.id, identity)
        
        # Revoke all active sessions for this user on password update (RFC Security standards)
        sessions = await self.session_repo.get_active_by_user_id(user_id)
        for s in sessions:
            s.is_revoked = True
            s.revoked_reason = "password_changed"
            await self.session_repo.update(s.id, s)
