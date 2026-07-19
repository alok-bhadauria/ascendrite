import pytest
from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status

from app.main import app
from app.api.v1.dependencies import get_current_principal, get_event_dispatcher, get_audit_service, get_activity_service
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext
from app.core.errors import ForbiddenException, AppException

# Models
from app.modules.learning.models.experience import LearningExperienceModel, ExperienceStatus
from app.modules.learning.models.progress import LearningStatus
from app.modules.learning.models.learning_attempt import AttemptStatus

# Repositories & Services
from app.modules.learning.repositories.mongo import (
    MongoLearningSessionRepository,
    MongoLearningAttemptRepository,
    MongoLearningExperienceRepository
)
from app.modules.learning.repositories.progress import MongoProgressRepository
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService
from app.modules.learning.services.progress import ProgressService
from app.modules.learning.services.experience import LearningExperienceService

@pytest.fixture
def mock_learner():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )

@pytest.mark.anyio
async def test_learning_experience_flow(client):
    # Initialize database client local to current event loop
    test_client = AsyncIOMotorClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = test_client["ascendrite"]

    # 1. Initialize Repositories
    session_repo = MongoLearningSessionRepository(db)
    attempt_repo = MongoLearningAttemptRepository(db)
    progress_repo = MongoProgressRepository(db)
    exp_repo = MongoLearningExperienceRepository(db)

    # 2. Clear collections
    await db["learning_sessions"].delete_many({})
    await db["learning_attempts"].delete_many({})
    await db["learning_experiences"].delete_many({})
    await db["progress"].delete_many({})
    await db["knowledge_contents"].delete_many({})
    await db["topics"].delete_many({})

    # 3. Setup core telemetry services
    event_disp = get_event_dispatcher()
    audit_serv = await get_audit_service(db)
    activity_serv = await get_activity_service(db)

    # 4. Initialize services
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
    exp_serv = LearningExperienceService(
        repo=exp_repo,
        db=db,
        session_service=session_serv,
        attempt_service=attempt_serv,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    # Setup Principal Contexts
    learner = AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )
    ctx_learner = RuntimeContext(correlation_id="corr-exp-1", principal=learner)

    unauth = AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4568",
        identity_type="user",
        role="Student",
        capabilities=[]
    )
    ctx_unauth = RuntimeContext(correlation_id="corr-exp-2", principal=unauth)

    # Seed Knowledge content in DB to satisfy resource check
    content_id = "content-notes-abc"
    await db["knowledge_contents"].insert_one({
        "_id": content_id,
        "topic_id": "topic-math-101",
        "category": "notes",
        "title": "Calculus Limits Notes",
        "body": "Markdown text content",
        "status": "published",
        "created_by": "admin"
    })

    # Seed parent curriculum elements to satisfy progress hierarchy tracing
    await db["subjects"].insert_one({
        "_id": "subj-math",
        "name": "Mathematics",
        "code": "MATH101",
        "status": "active"
    })
    await db["syllabuses"].insert_one({
        "_id": "syl-math-2026",
        "subject_id": "subj-math",
        "name": "Syllabus 2026",
        "status": "active"
    })
    await db["modules"].insert_one({
        "_id": "mod-calculus",
        "syllabus_id": "syl-math-2026",
        "name": "Calculus Module",
        "status": "active"
    })
    await db["topics"].insert_one({
        "_id": "topic-math-101",
        "module_id": "mod-calculus",
        "name": "Limits and Continuity",
        "status": "active"
    })

    # --------------------------------------------------------------------------
    # TEST 1: CAPABILITY ENFORCEMENT & RESOURCE VERIFICATION
    # --------------------------------------------------------------------------
    with pytest.raises(ForbiddenException):
        await exp_serv.start_experience(ctx_unauth, content_id, "notes")

    # Resource not found error
    with pytest.raises(AppException) as exc:
        await exp_serv.start_experience(ctx_learner, "invalid-resource-id", "notes")
    assert exc.value.status_code == 404

    # --------------------------------------------------------------------------
    # TEST 2: LIFECYCLE & ATTEMPT INTEGRATION
    # --------------------------------------------------------------------------
    
    # 1. Start session (Passive session participation)
    session = await session_serv.start_session(ctx_learner)

    # 2. Start Experience
    exp = await exp_serv.start_experience(ctx_learner, content_id, "notes")
    assert exp.id is not None
    assert exp.status == ExperienceStatus.ACTIVE
    assert str(exp.session_id) == str(session.id)
    assert exp.state["current_step"] == 0

    # 3. Submit Step (advancing workflow state)
    exp = await exp_serv.submit_experience_step(ctx_learner, str(exp.id), {"current_step": 2, "scroll_percentage": 50})
    assert exp.state["current_step"] == 2
    assert exp.state["scroll_percentage"] == 50

    # 4. Complete Experience
    completed = await exp_serv.complete_experience(
        context=ctx_learner,
        experience_id=str(exp.id),
        score=0.9,
        response_data={"pages_read": [1, 2]}
    )
    assert completed.status == ExperienceStatus.COMPLETED

    # 5. Assert Attempt got logged successfully
    attempts = await attempt_repo.list_by_user("60c72b2f9b1d8e2b8c8b4567")
    assert len(attempts) == 1
    assert attempts[0].status == AttemptStatus.COMPLETED
    assert attempts[0].score == 0.9

    # 6. Assert Progress updated dynamically based on completed attempt evidence
    progress = await progress_repo.get_by_user_and_subject("60c72b2f9b1d8e2b8c8b4567", "subj-math")
    assert len(progress.completed_topics) == 1
    assert progress.completed_topics[0].status == LearningStatus.MASTERED

    # Clean up client
    test_client.close()


def test_experience_endpoints_flow(client, mock_learner):
    from pymongo import MongoClient
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]
    db["knowledge_contents"].delete_many({})
    db["knowledge_contents"].insert_one({
        "_id": "content-notes-abc",
        "topic_id": "topic-math-101",
        "category": "notes",
        "title": "Calculus Limits Notes",
        "body": "Markdown text content",
        "status": "published",
        "created_by": "admin"
    })
    mongo_client.close()

    app.dependency_overrides[get_current_principal] = lambda: mock_learner

    # 1. Start Experience (using TestClient)
    response = client.post("/api/v1/learning/experiences/start", json={
        "resource_id": "content-notes-abc",
        "experience_type": "notes",
        "metadata": {"source": "postman"}
    })
    assert response.status_code == status.HTTP_201_CREATED
    exp_data = response.json()["data"]
    exp_id = exp_data["_id"]
    assert exp_data["status"] == "active"

    # 2. Get Active Experiences
    response = client.get("/api/v1/learning/experiences/active")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["_id"] == exp_id

    # 3. Submit Step
    response = client.post(f"/api/v1/learning/experiences/{exp_id}/step", json={
        "step_data": {"page": 3}
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["state"]["page"] == 3

    # 4. Abandon Experience
    response = client.post(f"/api/v1/learning/experiences/{exp_id}/abandon")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "abandoned"

    app.dependency_overrides.clear()
