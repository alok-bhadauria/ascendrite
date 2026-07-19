import pytest
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_learner():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4567",
        identity_type="user",
        role="Student",
        capabilities=["learning:read", "learning:write"]
    )

def test_learning_endpoints_flow(client, mock_learner):
    # 1. Override dependencies to use mock learner
    app.dependency_overrides[get_current_principal] = lambda: mock_learner

    # Start Session
    response = client.post("/api/v1/learning/sessions/start", json={"metadata": {"agent": "pytest"}})
    assert response.status_code == status.HTTP_201_CREATED
    sess_data = response.json()
    assert sess_data["success"] is True
    session_id = sess_data["data"]["_id"]
    assert sess_data["data"]["status"] == "active"

    # Get Active Session
    response = client.get("/api/v1/learning/sessions/active")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["_id"] == session_id

    # Start Attempt
    response = client.post("/api/v1/learning/attempts/start", json={
        "session_id": session_id,
        "resource_id": "topic-limits-1",
        "resource_type": "topic",
        "metadata": {"source": "e2e"}
    })
    assert response.status_code == status.HTTP_201_CREATED
    attempt_data = response.json()
    attempt_id = attempt_data["data"]["_id"]
    assert attempt_data["data"]["status"] == "in_progress"

    # Complete Attempt
    response = client.post(f"/api/v1/learning/attempts/{attempt_id}/complete", json={
        "score": 0.85,
        "response_data": {"correct_answers": 8}
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "completed"
    assert response.json()["data"]["score"] == 0.85

    # Close Session
    response = client.post(f"/api/v1/learning/sessions/{session_id}/close")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "closed"

    # Clean up overrides
    app.dependency_overrides.clear()
