import pytest
from bson import ObjectId
from pymongo import MongoClient
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_student():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b5555",
        identity_type="user",
        role="Student",
        capabilities=["learning:read"]
    )

@pytest.fixture
def seed_discovery_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clear
    db["topics"].delete_many({})
    db["knowledge_contents"].delete_many({})
    db["assessments"].delete_many({})

    # Topic
    db["topics"].insert_one({
        "_id": "topic-limit-5",
        "subject_id": "math-limits",
        "module_id": "limits-basics",
        "name": "Limits Introduction Part 5",
        "description": "Calculus limits",
        "order": 5,
        "is_active": True
    })

    # Content
    db["knowledge_contents"].insert_one({
        "_id": "content-limits-5",
        "topic_id": "topic-limit-5",
        "category": "notes",
        "title": "Notes on calculus limits",
        "body": "Limits definition and theorems",
        "status": "published",
        "created_by": "admin",
        "metadata": {
            "difficulty": "easy"
        }
    })

    # Assessment
    db["assessments"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b5001"),
        "title": "Calculus quiz",
        "description": "Quiz covering calculus basics",
        "assessment_type": "quiz",
        "topic_id": "topic-limit-5",
        "questions": [],
        "visibility": "active",
        "publication_status": "published",
        "metadata": {
            "difficulty": "medium"
        }
    })

    yield db
    mongo_client.close()

def test_learning_discovery_flow(client, mock_student, seed_discovery_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # 1. Search by keyword
    response = client.get("/api/v1/learning/discovery/search?query=calculus")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) >= 2

    # 2. Search with filters
    response = client.get("/api/v1/learning/discovery/search?query=calculus&resource_type=content&difficulty=easy")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["resource_type"] == "content"

    # 3. Related resources query
    response = client.get("/api/v1/learning/discovery/related?resource_id=content-limits-5&resource_type=content")
    assert response.status_code == status.HTTP_200_OK
    # Should find the assessment on the same topic
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["resource_type"] == "assessment"

    # 4. Explore resources
    response = client.get("/api/v1/learning/discovery/explore")
    assert response.status_code == status.HTTP_200_OK
    assert "recently_added" in response.json()["data"]

    app.dependency_overrides.clear()
