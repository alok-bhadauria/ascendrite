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

# ------------------------------------------------------------------------------
# Phase 3: Curriculum Structure, Content, Discovery and Publishing Imports
# ------------------------------------------------------------------------------
from app.modules.knowledge.repositories.base import (
    SubjectRepository, SyllabusRepository, ModuleRepository, TopicRepository, KnowledgeContentRepository
)
from app.modules.knowledge.repositories.mongo import (
    MongoSubjectRepository, MongoSyllabusRepository, MongoModuleRepository, MongoTopicRepository, MongoKnowledgeContentRepository
)
from app.modules.knowledge.services.base import AcademicStructureService, KnowledgeContentService
from app.modules.knowledge.services.academic import MongoAcademicStructureService
from app.modules.knowledge.services.content import MongoKnowledgeContentService

# Phase 3 Search Platform Imports
from app.core.search.base import SearchProvider
from app.core.search.mongo import MongoSearchProvider
from app.core.search.service import SearchService

# ------------------------------------------------------------------------------
# Phase 4: Learning Domain Foundation Imports
# ------------------------------------------------------------------------------
from app.modules.learning.repositories.base import LearningSessionRepository, LearningAttemptRepository, LearningExperienceRepository
from app.modules.learning.repositories.mongo import MongoLearningSessionRepository, MongoLearningAttemptRepository, MongoLearningExperienceRepository
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService
from app.modules.learning.services.progress import ProgressService
from app.modules.learning.services.experience import LearningExperienceService
from app.modules.learning.services.insights import LearningInsightsService

# ------------------------------------------------------------------------------
# Phase 5: Education & Assessment Platform Imports
# ------------------------------------------------------------------------------
from app.modules.assessments.repositories.question import QuestionRepository, MongoQuestionRepository
from app.modules.assessments.repositories.assessment import AssessmentRepository, MongoAssessmentRepository
from app.modules.assessments.services.content import AssessmentContentService
from app.modules.assessments.repositories.runtime import AssessmentSessionRepository, MongoAssessmentSessionRepository
from app.modules.assessments.services.runtime import AssessmentRuntimeService
from app.modules.assessments.repositories.results import AssessmentResultRepository, MongoAssessmentResultRepository
from app.modules.assessments.services.evaluation import AssessmentEvaluationService

from app.modules.learning.repositories.collection import LearningCollectionRepository, MongoLearningCollectionRepository
from app.modules.learning.repositories.goal import LearningGoalRepository, MongoLearningGoalRepository
from app.modules.learning.services.utilities import LearningUtilitiesService
from app.modules.learning.services.discovery import DiscoveryService

# ------------------------------------------------------------------------------
# Phase 6: Creator, Collaboration & Administration Platform Imports
# ------------------------------------------------------------------------------
from app.modules.creator.repositories.draft import DraftResourceRepository, MongoDraftResourceRepository
from app.modules.creator.services.workspace import ContentWorkspaceService
from app.modules.creator.repositories.attachment import AssetAttachmentRepository, MongoAssetAttachmentRepository
from app.modules.creator.services.attachment import AssetAttachmentService
from app.modules.creator.repositories.workflow import PublishingWorkflowRepository, MongoPublishingWorkflowRepository
from app.modules.creator.services.pipeline import PublishingPipelineService

# ------------------------------------------------------------------------------
# Phase 6 Collaboration Platform Imports
# ------------------------------------------------------------------------------
from app.modules.collaboration.repositories.team import TeamRepository, MongoTeamRepository, TeamMembershipRepository, MongoTeamMembershipRepository
from app.modules.collaboration.services.team import TeamService
from app.modules.collaboration.repositories.workflow import CollaborationAssignmentRepository, MongoCollaborationAssignmentRepository, CollaborationCommentRepository, MongoCollaborationCommentRepository
from app.modules.collaboration.services.workflow import CollaborationWorkflowService
from app.modules.collaboration.repositories.activity import CollaborationActivityRepository, MongoCollaborationActivityRepository, CollaborationNotificationRepository, MongoCollaborationNotificationRepository
from app.modules.collaboration.services.activity import CollaborationActivityService

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

from app.core.runtime.context import RuntimeContext

async def get_runtime_context(
    request: Request,
    principal: AuthenticatedPrincipal = Depends(get_current_principal)
) -> RuntimeContext:
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("User-Agent")
    return RuntimeContext(
        correlation_id=correlation_id,
        principal=principal,
        ip_address=ip_address,
        user_agent=user_agent
    )

# ------------------------------------------------------------------------------
# Phase 3 Dependencies
# ------------------------------------------------------------------------------

async def get_subject_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> SubjectRepository:
    return MongoSubjectRepository(db)

async def get_syllabus_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> SyllabusRepository:
    return MongoSyllabusRepository(db)

async def get_module_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> ModuleRepository:
    return MongoModuleRepository(db)

async def get_topic_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> TopicRepository:
    return MongoTopicRepository(db)

async def get_search_provider(db: AsyncIOMotorDatabase = Depends(get_database)) -> SearchProvider:
    return MongoSearchProvider(db)

def get_search_service(provider: SearchProvider = Depends(get_search_provider)) -> SearchService:
    return SearchService(provider)

async def get_academic_structure_service(
    subject_repo: SubjectRepository = Depends(get_subject_repository),
    syllabus_repo: SyllabusRepository = Depends(get_syllabus_repository),
    module_repo: ModuleRepository = Depends(get_module_repository),
    topic_repo: TopicRepository = Depends(get_topic_repository),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service),
    db: AsyncIOMotorDatabase = Depends(get_database),
    search_service: SearchService = Depends(get_search_service)
) -> AcademicStructureService:
    return MongoAcademicStructureService(
        subject_repo, syllabus_repo, module_repo, topic_repo,
        event_dispatcher, audit_service, activity_service,
        db_ref=db, search_service=search_service
    )

async def get_knowledge_content_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> KnowledgeContentRepository:
    return MongoKnowledgeContentRepository(db)

async def get_knowledge_content_service(
    repo: KnowledgeContentRepository = Depends(get_knowledge_content_repository),
    academic_service: AcademicStructureService = Depends(get_academic_structure_service),
    asset_service: AssetService = Depends(get_asset_service),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service),
    search_service: SearchService = Depends(get_search_service)
) -> KnowledgeContentService:
    return MongoKnowledgeContentService(
        repo, academic_service, asset_service,
        event_dispatcher, audit_service, activity_service,
        search_service=search_service
    )

# ------------------------------------------------------------------------------
# Phase 4 Dependency Providers
# ------------------------------------------------------------------------------

async def get_learning_session_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> LearningSessionRepository:
    return MongoLearningSessionRepository(db)

async def get_learning_attempt_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> LearningAttemptRepository:
    return MongoLearningAttemptRepository(db)

async def get_progress_service(
    progress_repo: ProgressRepository = Depends(get_progress_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> ProgressService:
    return ProgressService(
        progress_repo=progress_repo,
        db=db,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        activity_service=activity_service
    )

async def get_learning_session_service(
    repo: LearningSessionRepository = Depends(get_learning_session_repository),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> LearningSessionService:
    return LearningSessionService(
        repo=repo,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        activity_service=activity_service
    )

async def get_learning_attempt_service(
    repo: LearningAttemptRepository = Depends(get_learning_attempt_repository),
    progress_service: ProgressService = Depends(get_progress_service),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> LearningAttemptService:
    return LearningAttemptService(
        repo=repo,
        progress_service=progress_service,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        activity_service=activity_service
    )

async def get_learning_experience_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> LearningExperienceRepository:
    return MongoLearningExperienceRepository(db)

async def get_learning_experience_service(
    repo: LearningExperienceRepository = Depends(get_learning_experience_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    session_service: LearningSessionService = Depends(get_learning_session_service),
    attempt_service: LearningAttemptService = Depends(get_learning_attempt_service),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> LearningExperienceService:
    return LearningExperienceService(
        repo=repo,
        db=db,
        session_service=session_service,
        attempt_service=attempt_service,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        activity_service=activity_service
    )

async def get_learning_insights_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> LearningInsightsService:
    return LearningInsightsService(db)

async def get_question_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> QuestionRepository:
    return MongoQuestionRepository(db)

async def get_assessment_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> AssessmentRepository:
    return MongoAssessmentRepository(db)

async def get_assessment_content_service(
    question_repo: QuestionRepository = Depends(get_question_repository),
    assessment_repo: AssessmentRepository = Depends(get_assessment_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    activity_service: ActivityService = Depends(get_activity_service)
) -> AssessmentContentService:
    return AssessmentContentService(
        question_repo=question_repo,
        assessment_repo=assessment_repo,
        db=db,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        activity_service=activity_service
    )

async def get_assessment_session_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> AssessmentSessionRepository:
    return MongoAssessmentSessionRepository(db)

async def get_assessment_result_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> AssessmentResultRepository:
    return MongoAssessmentResultRepository(db)

async def get_assessment_evaluation_service(
    repo: AssessmentResultRepository = Depends(get_assessment_result_repository),
    session_repo: AssessmentSessionRepository = Depends(get_assessment_session_repository),
    question_repo: QuestionRepository = Depends(get_question_repository),
    assessment_repo: AssessmentRepository = Depends(get_assessment_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    attempt_service: LearningAttemptService = Depends(get_learning_attempt_service),
    session_service: LearningSessionService = Depends(get_learning_session_service)
) -> AssessmentEvaluationService:
    return AssessmentEvaluationService(
        repo=repo,
        session_repo=session_repo,
        question_repo=question_repo,
        assessment_repo=assessment_repo,
        db=db,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        attempt_service=attempt_service,
        session_service=session_service
    )

async def get_assessment_runtime_service(
    repo: AssessmentSessionRepository = Depends(get_assessment_session_repository),
    content_service: AssessmentContentService = Depends(get_assessment_content_service),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service),
    evaluation_service: AssessmentEvaluationService = Depends(get_assessment_evaluation_service)
) -> AssessmentRuntimeService:
    srv = AssessmentRuntimeService(
        repo=repo,
        content_service=content_service,
        db=db,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service,
        evaluation_service=evaluation_service
    )
    return srv

async def get_learning_collection_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> LearningCollectionRepository:
    return MongoLearningCollectionRepository(db)

async def get_learning_goal_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> LearningGoalRepository:
    return MongoLearningGoalRepository(db)

async def get_learning_utilities_service(
    collection_repo: LearningCollectionRepository = Depends(get_learning_collection_repository),
    goal_repo: LearningGoalRepository = Depends(get_learning_goal_repository),
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> LearningUtilitiesService:
    return LearningUtilitiesService(
        collection_repo=collection_repo,
        goal_repo=goal_repo,
        db=db
    )

async def get_discovery_service(
    db: AsyncIOMotorDatabase = Depends(get_database)
) -> DiscoveryService:
    return DiscoveryService(db)

# ------------------------------------------------------------------------------
# Phase 6: Creator platform dependency providers
# ------------------------------------------------------------------------------

async def get_draft_resource_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> DraftResourceRepository:
    return MongoDraftResourceRepository(db)

async def get_creator_workspace_service(
    repo: DraftResourceRepository = Depends(get_draft_resource_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service)
) -> ContentWorkspaceService:
    return ContentWorkspaceService(repo, db, event_dispatcher, audit_service)

async def get_asset_attachment_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> AssetAttachmentRepository:
    return MongoAssetAttachmentRepository(db)

async def get_creator_asset_service(
    repo: AssetAttachmentRepository = Depends(get_asset_attachment_repository),
    draft_repo: DraftResourceRepository = Depends(get_draft_resource_repository),
    asset_service: AssetService = Depends(get_asset_service),
    db: AsyncIOMotorDatabase = Depends(get_database),
    audit_service: AuditService = Depends(get_audit_service)
) -> AssetAttachmentService:
    return AssetAttachmentService(repo, draft_repo, asset_service, db, audit_service)

async def get_publishing_workflow_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> PublishingWorkflowRepository:
    return MongoPublishingWorkflowRepository(db)

async def get_creator_pipeline_service(
    repo: PublishingWorkflowRepository = Depends(get_publishing_workflow_repository),
    workspace_service: ContentWorkspaceService = Depends(get_creator_workspace_service),
    knowledge_content_service: KnowledgeContentService = Depends(get_knowledge_content_service),
    assessment_content_service: AssessmentContentService = Depends(get_assessment_content_service),
    db: AsyncIOMotorDatabase = Depends(get_database),
    event_dispatcher: EventDispatcher = Depends(get_event_dispatcher),
    audit_service: AuditService = Depends(get_audit_service)
) -> PublishingPipelineService:
    return PublishingPipelineService(
        repo=repo,
        workspace_service=workspace_service,
        knowledge_content_service=knowledge_content_service,
        assessment_content_service=assessment_content_service,
        db=db,
        event_dispatcher=event_dispatcher,
        audit_service=audit_service
    )

# ------------------------------------------------------------------------------
# Phase 6 Collaboration Platform dependency providers
# ------------------------------------------------------------------------------

async def get_collaboration_team_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> TeamRepository:
    return MongoTeamRepository(db)

async def get_collaboration_membership_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> TeamMembershipRepository:
    return MongoTeamMembershipRepository(db)

async def get_collaboration_team_service(
    repo: TeamRepository = Depends(get_collaboration_team_repository),
    membership_repo: TeamMembershipRepository = Depends(get_collaboration_membership_repository),
    db: AsyncIOMotorDatabase = Depends(get_database),
    audit_service: AuditService = Depends(get_audit_service)
) -> TeamService:
    return TeamService(repo, membership_repo, db, audit_service)

async def get_collaboration_assignment_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> CollaborationAssignmentRepository:
    return MongoCollaborationAssignmentRepository(db)

async def get_collaboration_comment_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> CollaborationCommentRepository:
    return MongoCollaborationCommentRepository(db)

async def get_collaboration_workflow_service(
    assignment_repo: CollaborationAssignmentRepository = Depends(get_collaboration_assignment_repository),
    comment_repo: CollaborationCommentRepository = Depends(get_collaboration_comment_repository),
    audit_service: AuditService = Depends(get_audit_service)
) -> CollaborationWorkflowService:
    return CollaborationWorkflowService(assignment_repo, comment_repo, audit_service)

async def get_collaboration_activity_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> CollaborationActivityRepository:
    return MongoCollaborationActivityRepository(db)

async def get_collaboration_notification_repository(db: AsyncIOMotorDatabase = Depends(get_database)) -> CollaborationNotificationRepository:
    return MongoCollaborationNotificationRepository(db)

async def get_collaboration_activity_service(
    activity_repo: CollaborationActivityRepository = Depends(get_collaboration_activity_repository),
    notification_repo: CollaborationNotificationRepository = Depends(get_collaboration_notification_repository)
) -> CollaborationActivityService:
    return CollaborationActivityService(activity_repo, notification_repo)





