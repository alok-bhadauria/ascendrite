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
        id="60c72b2f9b1d8e2b8c8b3333",
        identity_type="user",
        role="Student",
        capabilities=["assessment:read", "assessment:write", "learning:read", "learning:write"]
    )

@pytest.fixture
def seed_results_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clear
    db["questions"].delete_many({})
    db["assessments"].delete_many({})
    db["assessment_sessions"].delete_many({})
    db["assessment_results"].delete_many({})
    db["learning_sessions"].delete_many({})
    db["learning_attempts"].delete_many({})
    db["progress"].delete_many({})
    db["topics"].delete_many({})

    # Topic
    db["topics"].insert_one({
        "_id": "topic-deriv-202",
        "subject_id": "math-deriv",
        "module_id": "deriv-basics",
        "name": "Derivatives Advanced",
        "description": "Derivatives details",
        "order": 2,
        "is_active": True
    })

    # Question
    db["questions"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b3001"),
        "question_type": "MCQ",
        "title": "Derivative of 3x^2",
        "statement": "What is the derivative of 3x^2?",
        "explanation": "Power rule gives 6x.",
        "options": ["3x", "6x", "6", "x^3"],
        "evaluation_definition": {
            "correct_option_index": 1
        },
        "visibility": "active",
        "publication_status": "published",
        "version": 1,
        "metadata": {
            "topic_id": "topic-deriv-202",
            "skills": ["power-rule"]
        }
    })

    # Assessment
    db["assessments"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b3002"),
        "title": "Power Rule Quiz",
        "description": "Quiz on power rule",
        "assessment_type": "quiz",
        "topic_id": "topic-deriv-202",
        "questions": [
            {
                "question_id": "60c72b2f9b1d8e2b8c8b3001",
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

    # Active learning session
    db["learning_sessions"].insert_one({
        "_id": ObjectId("60c72b2f9b1d8e2b8c8b3003"),
        "user_id": ObjectId("60c72b2f9b1d8e2b8c8b3333"),
        "status": "active",
        "start_time": datetime.now(timezone.utc),
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    yield db
    mongo_client.close()

def test_assessment_evaluation_and_results_flow(client, mock_student, seed_results_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # 1. Start Session
    response = client.post("/api/v1/assessments/sessions/start", json={
        "assessment_id": "60c72b2f9b1d8e2b8c8b3002"
    })
    s_id = response.json()["data"]["_id"]

    # 2. Submit Correct Answer
    response = client.post(f"/api/v1/assessments/sessions/{s_id}/answer", json={
        "question_id": "60c72b2f9b1d8e2b8c8b3001",
        "selected_option_index": 1
    })

    # 3. Submit Session (Triggers evaluation automatically)
    response = client.post(f"/api/v1/assessments/sessions/{s_id}/submit")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "completed"

    # 4. Fetch Result
    response = client.get(f"/api/v1/assessments/results/session/{s_id}")
    assert response.status_code == status.HTTP_200_OK
    res_data = response.json()["data"]
    assert res_data["score"] == 1.0
    assert res_data["passed"] is True
    assert "power-rule" in res_data["strengths"]

    app.dependency_overrides.clear()
