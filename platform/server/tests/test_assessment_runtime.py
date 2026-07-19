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
        id="60c72b2f9b1d8e2b8c8b2222",
        identity_type="user",
        role="Student",
        capabilities=["assessment:read", "assessment:write"]
    )

@pytest.fixture
def seed_runtime_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clear
    db["questions"].delete_many({})
    db["assessments"].delete_many({})
    db["assessment_sessions"].delete_many({})
    db["topics"].delete_many({})

    # Topic
    db["topics"].insert_one({
        "_id": "topic-deriv-101",
        "subject_id": "math-deriv",
        "module_id": "deriv-basics",
        "name": "Derivatives",
        "description": "Derivatives intro",
        "order": 1,
        "is_active": True
    })

    # Question
    db["questions"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b2001"),
        "question_type": "MCQ",
        "title": "Derivative of 2x",
        "statement": "What is the derivative of 2x?",
        "explanation": "Power rule gives 2.",
        "options": ["1", "2", "x", "2x"],
        "evaluation_definition": {
            "correct_option_index": 1
        },
        "visibility": "active",
        "publication_status": "published",
        "version": 1,
        "metadata": {
            "topic_id": "topic-deriv-101"
        }
    })

    # Assessment
    db["assessments"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b2002"),
        "title": "Derivatives Quiz",
        "description": "Quiz on derivatives",
        "assessment_type": "quiz",
        "topic_id": "topic-deriv-101",
        "questions": [
            {
                "question_id": "60c72b2f9b1d8e2b8c8b2001",
                "order": 1,
                "marks": 1.0,
                "weight": 1.0,
                "is_mandatory": True
            }
        ],
        "duration_minutes": 10,
        "passing_score": 0.7,
        "visibility": "active",
        "publication_status": "published",
        "metadata": {}
    })

    yield db
    mongo_client.close()

def test_assessment_session_workflow(client, mock_student, seed_runtime_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # 1. Start Session
    response = client.post("/api/v1/assessments/sessions/start", json={
        "assessment_id": "60c72b2f9b1d8e2b8c8b2002"
    })
    assert response.status_code == status.HTTP_201_CREATED
    s_data = response.json()["data"]
    s_id = s_data["_id"]
    assert s_data["status"] == "active"

    # 2. Submit Answer
    response = client.post(f"/api/v1/assessments/sessions/{s_id}/answer", json={
        "question_id": "60c72b2f9b1d8e2b8c8b2001",
        "selected_option_index": 1,
        "elapsed_seconds": 30,
        "confidence_level": 4
    })
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]["responses"]) == 1

    # 3. Cancel Session
    response = client.post(f"/api/v1/assessments/sessions/{s_id}/cancel")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "cancelled"

    app.dependency_overrides.clear()
