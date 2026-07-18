from fastapi import Depends, HTTPException, Request, status, BackgroundTasks
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

# Runtime Infrastructure Imports
from app.core.runtime.events.base import EventDispatcher
from app.core.runtime.events.dispatcher import LocalEventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.audit.service import MongoAuditService
from app.core.runtime.activity.base import ActivityService
from app.core.runtime.activity.service import MongoActivityService
from app.core.runtime.notification.base import NotificationService
from app.core.runtime.notification.dispatcher import NotificationDispatcher
from app.core.runtime.notification.channels import InAppChannel, MockEmailChannel, MockSMSChannel, MockPushChannel
from app.core.runtime.tasks.base import BackgroundTaskService
from app.core.runtime.tasks.providers import FastAPIBackgroundTaskProvider
from app.core.runtime.tasks.scheduler import BackgroundTaskScheduler

# Asset Platform Imports
from app.infrastructure.storage.manager import StorageManager
from app.modules.assets.repositories.base import AssetRepository
from app.modules.assets.repositories.asset import MongoAssetRepository
from app.modules.assets.services.base import AssetService
from app.modules.assets.services.service import MongoAssetService

# Singleton Internal Application Event Dispatcher
event_dispatcher_instance = LocalEventDispatcher()

def get_event_dispatcher() -> EventDispatcher:
    return event_dispatcher_instance

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

def get_storage_manager(provider: StorageProvider = Depends(get_storage_provider)) -> StorageManager:
    return StorageManager(provider)

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

# ------------------------------------------------------------------------------
# Stage 2.3 Shared Runtime Services Dependencies
# ------------------------------------------------------------------------------

async def get_audit_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> AuditService:
    return MongoAuditService(db)

async def get_activity_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> ActivityService:
    return MongoActivityService(db)

async def get_notification_service(db: AsyncIOMotorDatabase = Depends(get_database)) -> NotificationService:
    channels = [
        InAppChannel(db),
        MockEmailChannel(),
        MockSMSChannel(),
        MockPushChannel()
    ]
    return NotificationDispatcher(channels)

def get_background_task_service(background_tasks: BackgroundTasks) -> BackgroundTaskService:
    provider = FastAPIBackgroundTaskProvider(background_tasks)
    return BackgroundTaskScheduler(provider)

# ------------------------------------------------------------------------------
# Stage 2.4 Asset & Media Platform Dependencies
# ------------------------------------------------------------------------------

async def get_asset_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> AssetRepository:
    return MongoAssetRepository(db)

async def get_asset_service(
    repo: AssetRepository = Depends(get_asset_repository),
    storage_mgr: StorageManager = Depends(get_storage_manager),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> AssetService:
    return MongoAssetService(repo, storage_mgr, event_dispatcher, audit_service, activity_service)
