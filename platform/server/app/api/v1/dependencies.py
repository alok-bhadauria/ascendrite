from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.infrastructure.database.mongodb import get_database
from app.modules.users.models.user import UserModel
from app.modules.users.repositories.user import MongoUserRepository, UserRepository
from app.modules.users.repositories.identity import MongoUserIdentityRepository, UserIdentityRepository
from app.modules.authentication.repositories.session import MongoSessionRepository, SessionRepository
from app.modules.learning.repositories.progress import MongoProgressRepository, ProgressRepository
from app.modules.assessments.repositories.quiz_submission import MongoQuizSubmissionRepository, QuizSubmissionRepository
from app.modules.authentication.services.auth import AuthService
from app.infrastructure.storage.base import StorageProvider
from app.infrastructure.storage.rustfs import get_rustfs
from app.core.authorization.principal import AuthenticatedPrincipal

async def get_user_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserRepository:
    return MongoUserRepository(db)

async def get_identity_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> UserIdentityRepository:
    return MongoUserIdentityRepository(db)

async def get_session_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> SessionRepository:
    return MongoSessionRepository(db)

async def get_progress_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ProgressRepository:
    return MongoProgressRepository(db)

async def get_quiz_submission_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> QuizSubmissionRepository:
    return MongoQuizSubmissionRepository(db)

async def get_auth_service(
    user_repo: UserRepository = Depends(get_user_repository),
    identity_repo: UserIdentityRepository = Depends(get_identity_repository),
    session_repo: SessionRepository = Depends(get_session_repository)
) -> AuthService:
    return AuthService(user_repo, identity_repo, session_repo)

def get_storage_provider() -> StorageProvider:
    """Framework-native dependency injection provider for storage services"""
    return get_rustfs()

async def get_current_user(
    request: Request,
    user_repo: UserRepository = Depends(get_user_repository)
) -> UserModel:
    """Resolve active user session from HttpOnly cookies or Bearer Authorization headers"""
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials not found in request headers/cookies."
        )

    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        if user_id is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token context."
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token has expired or is invalid."
        )

    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account associated with this token was not found."
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated."
        )
    return user

async def get_current_principal(
    current_user: UserModel = Depends(get_current_user)
) -> AuthenticatedPrincipal:
    """Resolve AuthenticatedPrincipal context from active UserModel"""
    from app.core.authorization.evaluator import resolve_capabilities
    caps = resolve_capabilities(current_user.role)
    return AuthenticatedPrincipal(
        id=str(current_user.id),
        identity_type="user",
        role=current_user.role,
        capabilities=caps
    )
