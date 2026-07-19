import pytest
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from bson import ObjectId
from app.core.errors import ForbiddenException, AppException
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext
from app.api.v1.dependencies import get_event_dispatcher, get_audit_service, get_activity_service

# Import domain models
from app.modules.learning.models.progress import ProgressModel, TopicProgress, LearningStatus
from app.modules.learning.models.learning_session import LearningSessionModel, SessionStatus
from app.modules.learning.models.learning_attempt import LearningAttemptModel, AttemptStatus

# Import repositories
from app.modules.learning.repositories.mongo import (
    MongoLearningSessionRepository,
    MongoLearningAttemptRepository
)
from app.modules.learning.repositories.progress import MongoProgressRepository

# Import services
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService
from app.modules.learning.services.progress import ProgressService

@pytest.mark.anyio
async def test_learning_foundation_flow(client):
    # Initialize database client local to current event loop
    test_client = AsyncIOMotorClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = test_client["ascendrite"]

    # 1. Initialize Repositories
    session_repo = MongoLearningSessionRepository(db)
    attempt_repo = MongoLearningAttemptRepository(db)
    progress_repo = MongoProgressRepository(db)

    # 2. Initialize Telemetry & Event Dispatcher
    event_disp = get_event_dispatcher()
    audit_serv = await get_audit_service(db)
    activity_serv = await get_activity_service(db)

    # 3. Initialize Services
    progress_serv = ProgressService(
        progress_repo=progress_repo,
        db=db,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    session_serv = LearningSessionService(
        repo=session_repo,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    attempt_serv = LearningAttemptService(
        repo=attempt_repo,
        progress_service=progress_serv,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    # 4. Setup Contexts
    learner = AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )
    ctx_learner = RuntimeContext(correlation_id="corr-learning-1", principal=learner)

    unauthorized_user = AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4568",
        identity_type="user",
        role="Student",
        capabilities=[]  # No learning capabilities
    )
    ctx_unauth = RuntimeContext(correlation_id="corr-learning-2", principal=unauthorized_user)

    # --------------------------------------------------------------------------
    # TEST 1: CAPABILITY ENFORCEMENT & SESSION LIFECYCLE
    # --------------------------------------------------------------------------

    # Attempt to start session without capability (Fails)
    with pytest.raises(ForbiddenException):
        await session_serv.start_session(context=ctx_unauth)

    # Start Session with capability (Succeeds)
    session = await session_serv.start_session(context=ctx_learner, metadata={"client": "web"})
    assert session.id is not None
    assert session.status == SessionStatus.ACTIVE
    assert session.metadata["client"] == "web"

    # Get active session (Succeeds)
    active = await session_serv.get_active_session(context=ctx_learner)
    assert active is not None
    assert str(active.id) == str(session.id)

    # Close Session (Succeeds)
    closed = await session_serv.close_session(str(session.id), context=ctx_learner)
    assert closed.status == SessionStatus.CLOSED
    assert closed.end_time is not None

    # Verify no active session remains
    active_now = await session_serv.get_active_session(context=ctx_learner)
    assert active_now is None

    # --------------------------------------------------------------------------
    # TEST 2: LEARNING RESOURCE ATTEMPTS
    # --------------------------------------------------------------------------

    # Start attempt
    attempt = await attempt_serv.start_attempt(
        session_id=str(session.id),
        resource_id="topic-math-101",
        resource_type="topic",
        context=ctx_learner,
        metadata={"mode": "study"}
    )
    assert attempt.id is not None
    assert attempt.status == AttemptStatus.IN_PROGRESS
    assert attempt.resource_type == "topic"

    # Create parent Topic hierarchy in test DB to resolve subject successfully
    from app.modules.knowledge.models.academic import SubjectModel, SyllabusModel, ModuleModel, TopicModel, StructuralState
    
    # Mock academic hierarchy entries
    await db["subjects"].insert_one({
        "_id": "subj-math",
        "name": "Mathematics",
        "code": "MATH101",
        "description": "Calculus and Algebra",
        "category": "core",
        "status": "active",
        "created_by": "admin"
    })
    await db["syllabuses"].insert_one({
        "_id": "syl-math-2026",
        "subject_id": "subj-math",
        "name": "Math Syllabus",
        "version": "1.0",
        "description": "Standard Syllabus",
        "status": "active",
        "created_by": "admin"
    })
    await db["modules"].insert_one({
        "_id": "mod-calculus",
        "syllabus_id": "syl-math-2026",
        "name": "Calculus Module",
        "order": 1,
        "description": "Calculus Module Description",
        "status": "active",
        "created_by": "admin"
    })
    await db["topics"].insert_one({
        "_id": "topic-math-101",
        "module_id": "mod-calculus",
        "name": "Limits and Continuity",
        "order": 1,
        "description": "Topic Description",
        "status": "active",
        "created_by": "admin"
    })

    # Complete attempt (Succeeds)
    completed_attempt = await attempt_serv.complete_attempt(
        attempt_id=str(attempt.id),
        score=0.95,
        response_data={"correct": 19, "total": 20},
        context=ctx_learner,
        metadata={"reviewed": True}
    )
    assert completed_attempt.status == AttemptStatus.COMPLETED
    assert completed_attempt.duration_seconds is not None
    assert completed_attempt.score == 0.95

    # --------------------------------------------------------------------------
    # TEST 3: EVIDENCE AGGREGATION & PROGRESS LIFECYCLE
    # --------------------------------------------------------------------------

    # Fetch updated progress document
    progress = await progress_serv.get_or_create_progress("60c72b2f9b1d8e2b8c8b4567", "subj-math")
    assert len(progress.completed_topics) == 1
    
    topic_prog = progress.completed_topics[0]
    assert topic_prog.topic_id == "topic-math-101"
    # Score 0.95 maps status to MASTERED on first attempt
    assert topic_prog.status == LearningStatus.MASTERED
    assert topic_prog.confidence_score > 0.0
    assert topic_prog.review_count == 1
    assert topic_prog.last_attempt_id == str(completed_attempt.id)

    # Log a second attempt to increment reviews
    attempt2 = await attempt_serv.start_attempt(
        session_id=None,
        resource_id="topic-math-101",
        resource_type="topic",
        context=ctx_learner
    )
    # Complete second attempt
    completed2 = await attempt_serv.complete_attempt(
        attempt_id=str(attempt2.id),
        score=1.0,
        response_data=None,
        context=ctx_learner
    )
    
    progress2 = await progress_serv.get_or_create_progress("60c72b2f9b1d8e2b8c8b4567", "subj-math")
    topic_prog2 = progress2.completed_topics[0]
    assert topic_prog2.review_count == 2
    assert topic_prog2.quiz_score == 1.0

    # --------------------------------------------------------------------------
    # TEST 4: BACKWARD COMPATIBILITY
    # --------------------------------------------------------------------------
    
    # Save a legacy progress model document (missing status, confidence, review_count, last_attempt_id)
    await db["progress"].delete_many({})
    await db["progress"].insert_one({
        "user_id": ObjectId("60c72b2f9b1d8e2b8c8b4567"),
        "subject_id": "subj-math",
        "completed_topics": [
            {
                "topic_id": "topic-math-101",
                "completed_at": datetime.now(timezone.utc),
                "duration_seconds": 120,
                "quiz_score": 0.8
            }
        ],
        "last_active_at": datetime.now(timezone.utc),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    # Retrieve progress via ProgressRepository (Succeeds - Pydantic parses defaults)
    compat_progress = await progress_repo.get_by_user_and_subject("60c72b2f9b1d8e2b8c8b4567", "subj-math")
    assert compat_progress is not None
    assert len(compat_progress.completed_topics) == 1
    
    compat_item = compat_progress.completed_topics[0]
    assert compat_item.status == LearningStatus.COMPLETED  # defaults
    assert compat_item.confidence_score == 0.0  # defaults
    assert compat_item.review_count == 1  # defaults
    assert compat_item.duration_seconds == 120

    # Clean up test client
    test_client.close()
