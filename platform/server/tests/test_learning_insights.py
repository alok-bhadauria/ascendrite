import pytest
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import status

from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext

from app.modules.learning.schemas.insights import (
    LearningHistoryItem,
    EducationalRecommendation,
    WeakAreaResponse,
    LearnerDashboardResponse
)
from app.modules.learning.services.insights import LearningInsightsService

@pytest.fixture
def mock_learner():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )

@pytest.fixture
def seed_insights_db():
    # Setup pymongo sync client to seed DB
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clean
    db["learning_sessions"].delete_many({})
    db["learning_attempts"].delete_many({})
    db["learning_experiences"].delete_many({})
    db["progress"].delete_many({})
    db["knowledge_contents"].delete_many({})

    user_id = ObjectId("60c72b2f9b1d8e2b8c8b4567")

    # 1. Seed Content
    db["knowledge_contents"].insert_one({
        "_id": "content-notes-1",
        "topic_id": "topic-math-limits",
        "category": "notes",
        "title": "Limits Intro",
        "body": "Body content",
        "status": "published",
        "created_by": "admin"
    })
    db["knowledge_contents"].insert_one({
        "_id": "content-quiz-1",
        "topic_id": "topic-math-limits",
        "category": "quiz",
        "title": "Limits Quiz",
        "body": "Quiz content",
        "status": "published",
        "created_by": "admin"
    })

    # 2. Seed Sessions
    db["learning_sessions"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b0001"),
        "user_id": user_id,
        "status": "closed",
        "start_time": datetime.now(timezone.utc) - timedelta(hours=2),
        "end_time": datetime.now(timezone.utc) - timedelta(hours=1),
        "created_at": datetime.now(timezone.utc) - timedelta(hours=2),
        "updated_at": datetime.now(timezone.utc) - timedelta(hours=1)
    })

    # 3. Seed Experiences
    db["learning_experiences"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b0002"),
        "user_id": user_id,
        "resource_id": "content-notes-1",
        "experience_type": "notes",
        "status": "active",
        "state": {"current_step": 1},
        "start_time": datetime.now(timezone.utc) - timedelta(minutes=30),
        "created_at": datetime.now(timezone.utc) - timedelta(minutes=30),
        "updated_at": datetime.now(timezone.utc) - timedelta(minutes=30)
    })

    # 4. Seed Attempts (one failed assessment to trigger retry recommendation)
    db["learning_attempts"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b0003"),
        "user_id": user_id,
        "resource_id": "content-quiz-1",
        "resource_type": "quiz",
        "status": "completed",
        "score": 0.5,  # < 0.7 -> weak/failed
        "start_time": datetime.now(timezone.utc) - timedelta(hours=1, minutes=30),
        "end_time": datetime.now(timezone.utc) - timedelta(hours=1, minutes=20),
        "created_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=30),
        "updated_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=20)
    })

    # 5. Seed Progress
    db["progress"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b0004"),
        "user_id": user_id,
        "subject_id": "subj-math",
        "completed_topics": [
            {
                "topic_id": "topic-math-limits",
                "status": "reviewed",  # Reviewed status to trigger review recommendation
                "review_count": 2,
                "quiz_score": 0.5,
                "confidence_score": 0.6,
                "duration_seconds": 600,
                "completed_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=20),
                "last_attempt_at": datetime.now(timezone.utc) - timedelta(hours=1, minutes=20),
                "last_attempt_id": "60c72b2f9b1d8e2b8c8b0003"
            }
        ],
        "created_at": datetime.now(timezone.utc) - timedelta(hours=2),
        "updated_at": datetime.now(timezone.utc) - timedelta(hours=1)
    })

    yield db
    mongo_client.close()

@pytest.mark.anyio
async def test_learning_insights_service(seed_insights_db):
    test_client = AsyncIOMotorClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = test_client["ascendrite"]

    service = LearningInsightsService(db)

    learner = AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read"]
    )
    context = RuntimeContext(correlation_id="corr-insights-1", principal=learner)

    # 1. Test Dashboard
    dash = await service.get_dashboard(context)
    assert dash.total_sessions_count == 1
    assert dash.total_attempts_count == 1
    assert dash.needs_review_count == 1
    assert dash.next_study_topic_id == "content-notes-1"  # Derived from active experience

    # 2. Test Recommendations
    recs = await service.get_recommendations(context)
    assert len(recs) >= 2
    types = [r.type for r in recs]
    assert "resume_experience" in types
    assert "review_weakness" in types or "retry_assessment" in types

    # 3. Test Weak Areas
    weaks = await service.get_weak_areas(context)
    assert len(weaks) == 1
    assert weaks[0].topic_id == "topic-math-limits"
    assert weaks[0].average_score == 0.5

    # 4. Test History
    history = await service.get_history(context)
    assert len(history) >= 4  # Merge of sessions, attempts, and experiences events
    event_types = [h.event_type for h in history]
    assert "session_start" in event_types
    assert "experience_start" in event_types
    assert "attempt_complete" in event_types

    test_client.close()

def test_insights_endpoints(client, mock_learner, seed_insights_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_learner

    # Dashboard endpoint
    response = client.get("/api/v1/learning/insights/dashboard")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["total_sessions_count"] == 1
    assert response.json()["data"]["next_study_topic_id"] == "content-notes-1"

    # History endpoint
    response = client.get("/api/v1/learning/insights/history?limit=10")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) >= 4

    # Recommendations endpoint
    response = client.get("/api/v1/learning/insights/recommendations")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) >= 2

    # Weak areas endpoint
    response = client.get("/api/v1/learning/insights/weak-areas")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["topic_id"] == "topic-math-limits"

    app.dependency_overrides.clear()
