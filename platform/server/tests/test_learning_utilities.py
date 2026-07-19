import pytest
from datetime import datetime, timezone, timedelta
from bson import ObjectId
from pymongo import MongoClient
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_student():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4444",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )

@pytest.fixture
def seed_utilities_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clear
    db["learning_collections"].delete_many({})
    db["learning_goals"].delete_many({})
    db["learning_attempts"].delete_many({})
    db["topics"].delete_many({})

    # Seed Topic
    db["topics"].insert_one({
        "_id": "topic-deriv-303",
        "subject_id": "math-deriv",
        "module_id": "deriv-basics",
        "name": "Derivatives Advanced Part 2",
        "description": "Derivatives details Part 2",
        "order": 3,
        "is_active": True
    })

    # Seed an attempt to populate "Recently Accessed"
    db["learning_attempts"].insert_one({
        "user_id": ObjectId("60c72b2f9b1d8e2b8c8b4444"),
        "resource_id": "topic-deriv-303",
        "resource_type": "topic",
        "status": "completed",
        "score": 0.9,
        "start_time": datetime.now(timezone.utc) - timedelta(minutes=10),
        "end_time": datetime.now(timezone.utc) - timedelta(minutes=5)
    })

    yield db
    mongo_client.close()

def test_learning_utilities_flow(client, mock_student, seed_utilities_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # 1. Create collection
    response = client.post("/api/v1/learning/utilities/collections", json={
        "collection_type": "bookmarks",
        "name": "Math Bookmarks"
    })
    assert response.status_code == status.HTTP_201_CREATED
    col_id = response.json()["data"]["_id"]

    # 2. Add resource
    response = client.post(f"/api/v1/learning/utilities/collections/{col_id}/resources", json={
        "resource_id": "topic-deriv-303",
        "resource_type": "topic"
    })
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]["resources"]) == 1

    # 3. Create learning goal
    response = client.post("/api/v1/learning/utilities/goals", json={
        "target_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
        "topic_ids": ["topic-deriv-303"]
    })
    assert response.status_code == status.HTTP_201_CREATED
    goal_id = response.json()["data"]["_id"]

    # 4. Update goal status
    response = client.put(f"/api/v1/learning/utilities/goals/{goal_id}/status?status=achieved")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "achieved"

    # 5. Get recently accessed
    response = client.get("/api/v1/learning/utilities/recent/accessed")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1

    # 6. Get recently completed
    response = client.get("/api/v1/learning/utilities/recent/completed")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1

    app.dependency_overrides.clear()
