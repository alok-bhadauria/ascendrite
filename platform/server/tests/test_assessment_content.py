import pytest
from bson import ObjectId
from pymongo import MongoClient
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_admin():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b1111",
        identity_type="user",
        role="Admin",
        capabilities=["assessment:write", "assessment:read"]
    )

@pytest.fixture
def seed_content_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]

    # Clear
    db["questions"].delete_many({})
    db["assessments"].delete_many({})
    db["topics"].delete_many({})

    # Seed Topic
    db["topics"].insert_one({
        "_id": "topic-limits-101",
        "subject_id": "math-limits",
        "module_id": "limits-basics",
        "name": "Limits Introduction",
        "description": "Basics of limits",
        "order": 1,
        "is_active": True
    })

    yield db
    mongo_client.close()

def test_question_crud_and_validation(client, mock_admin, seed_content_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_admin

    # 1. Create Question
    payload = {
        "question_type": "MCQ",
        "title": "Solve limit of x^2 as x->2",
        "statement": "What is the limit of f(x) = x^2 as x approaches 2?",
        "explanation": "Substitute x=2 into x^2 to get 4.",
        "options": ["2", "4", "8", "Undefined"],
        "evaluation_definition": {
            "correct_option_index": 1
        },
        "metadata": {
            "topic_id": "topic-limits-101",
            "difficulty": "easy",
            "tags": ["calculus", "limits"]
        }
    }
    response = client.post("/api/v1/assessments/content/questions", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    q_data = response.json()["data"]
    q_id = q_data["_id"]
    assert q_data["title"] == "Solve limit of x^2 as x->2"

    # 2. Get Question
    response = client.get(f"/api/v1/assessments/content/questions/{q_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["question_type"] == "MCQ"

    # 3. Create Assessment with Question reference
    assessment_payload = {
        "title": "Calculus Limits Quiz",
        "description": "Test your basic limits concepts",
        "assessment_type": "quiz",
        "topic_id": "topic-limits-101",
        "questions": [
            {
                "question_id": q_id,
                "order": 1,
                "marks": 2.0,
                "weight": 1.0,
                "is_mandatory": True
            }
        ],
        "duration_minutes": 15,
        "passing_score": 0.5
    }
    response = client.post("/api/v1/assessments/content/definitions", json=assessment_payload)
    assert response.status_code == status.HTTP_201_CREATED
    a_data = response.json()["data"]
    a_id = a_data["_id"]
    assert a_data["title"] == "Calculus Limits Quiz"

    # 4. Get Assessment
    response = client.get(f"/api/v1/assessments/content/definitions/{a_id}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]["questions"]) == 1

    app.dependency_overrides.clear()
