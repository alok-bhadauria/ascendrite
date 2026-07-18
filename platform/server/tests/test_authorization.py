import pytest
from fastapi import status, Depends
from fastapi.testclient import TestClient

from app.main import app
from app.core.authorization.capabilities import Capability
from app.core.authorization.guards import RequireCapability

from app.core.authorization.principal import AuthenticatedPrincipal

# Register temporary test routes on the main app for validation
@app.get("/api/v1/test/student-only")
def route_student_only(principal: AuthenticatedPrincipal = Depends(RequireCapability(Capability.LEARNING_READ))):
    return {"status": "success", "user_id": principal.id}

@app.get("/api/v1/test/admin-only")
def route_admin_only(principal: AuthenticatedPrincipal = Depends(RequireCapability(Capability.SYSTEM_ADMIN))):
    return {"status": "success", "user_id": principal.id}

def test_capability_based_authorization(client: TestClient):
    # 1. Register a Student user
    signup_student = {
        "email": "student_auth@example.com",
        "password": "securePassword123",
        "first_name": "Auth",
        "last_name": "Student"
    }
    client.post("/api/v1/auth/signup", json=signup_student)
    
    # Login Student
    login_student_res = client.post("/api/v1/auth/login", json={
        "email": signup_student["email"],
        "password": signup_student["password"]
    }).json()
    student_token = login_student_res["data"]["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}

    # 2. Assert Student can access Student-only endpoint (LEARNING_READ)
    res_stud = client.get("/api/v1/test/student-only", headers=student_headers)
    assert res_stud.status_code == status.HTTP_200_OK
    assert res_stud.json()["status"] == "success"

    # 3. Assert Student is rejected from Admin-only endpoint (SYSTEM_ADMIN)
    res_admin_rej = client.get("/api/v1/test/admin-only", headers=student_headers)
    assert res_admin_rej.status_code == status.HTTP_403_FORBIDDEN
    assert "Missing required capability context" in res_admin_rej.json()["error"]["message"]
