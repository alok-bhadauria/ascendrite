import pytest
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_contributor():
    return AuthenticatedPrincipal(
        id="contrib-123",
        identity_type="user",
        role="Contributor",
        capabilities=["knowledge:read", "knowledge:write", "knowledge:publish"]
    )

@pytest.fixture
def mock_student():
    return AuthenticatedPrincipal(
        id="student-999",
        identity_type="user",
        role="Student",
        capabilities=["knowledge:read"]
    )

def test_academic_endpoints_crud_flow(client, mock_contributor, mock_student):
    # 1. Inject Contributor Principal override
    app.dependency_overrides[get_current_principal] = lambda: mock_contributor

    # Create Subject
    subject_payload = {
        "name": "Distributed Systems",
        "code": "CS401",
        "description": "Consistency models and consensus",
        "category": "core-cs"
    }
    response = client.post("/api/v1/academic/subjects", json=subject_payload)
    assert response.status_code == status.HTTP_201_CREATED
    subj_data = response.json()
    assert subj_data["success"] is True
    subject_id = subj_data["data"]["_id"]

    # List Subjects
    response = client.get("/api/v1/academic/subjects")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) > 0

    # Create Syllabus
    syllabus_payload = {
        "subject_id": subject_id,
        "name": "B.Tech Distributed Systems 2026",
        "version": "2026.1",
        "description": "Syllabus curriculum"
    }
    response = client.post("/api/v1/academic/syllabuses", json=syllabus_payload)
    assert response.status_code == status.HTTP_201_CREATED
    syllabus_id = response.json()["data"]["_id"]

    # Create Module
    module_payload = {
        "syllabus_id": syllabus_id,
        "name": "Consensus",
        "order": 1,
        "description": "Paxos and Raft consensus protocols"
    }
    response = client.post("/api/v1/academic/modules", json=module_payload)
    assert response.status_code == status.HTTP_201_CREATED
    module_id = response.json()["data"]["_id"]

    # Create Topic
    topic_payload = {
        "module_id": module_id,
        "name": "Raft Leader Election",
        "order": 1,
        "description": "How leaders are elected in Raft"
    }
    response = client.post("/api/v1/academic/topics", json=topic_payload)
    assert response.status_code == status.HTTP_201_CREATED
    topic_id = response.json()["data"]["_id"]

    # Create Content (starts as Draft)
    content_payload = {
        "topic_id": topic_id,
        "category": "notes",
        "title": "Raft Leader Election Safety",
        "body": "Terms, randomized timeouts, and split votes."
    }
    response = client.post("/api/v1/knowledge-content", json=content_payload)
    assert response.status_code == status.HTTP_201_CREATED
    content_id = response.json()["data"]["_id"]
    assert response.json()["data"]["status"] == "draft"

    # 2. Inject Student Principal override
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # Verify student cannot retrieve Draft content (Fails with 403)
    response = client.get(f"/api/v1/knowledge-content/{content_id}")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # 3. Inject Contributor Principal override to Publish
    app.dependency_overrides[get_current_principal] = lambda: mock_contributor

    response = client.post(f"/api/v1/knowledge-content/{content_id}/publish", json={"status": "published"})
    assert response.status_code == status.HTTP_200_OK

    # 4. Inject Student Principal override
    app.dependency_overrides[get_current_principal] = lambda: mock_student

    # Verify student can retrieve Published content (Succeeds)
    response = client.get(f"/api/v1/knowledge-content/{content_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "published"

    # Search platform for the keyword
    response = client.get("/api/v1/search?q=Raft")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) > 0

    # Clean up overrides
    app.dependency_overrides.clear()
