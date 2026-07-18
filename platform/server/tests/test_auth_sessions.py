import pytest
import time
from fastapi import status
from app.core.config import settings

def test_user_flow(client):
    email = "newuser@example.com"
    password = "securePassword123"

    # 1. Sign Up
    signup_payload = {
        "email": email,
        "password": password,
        "first_name": "Test",
        "last_name": "User"
    }
    response = client.post("/api/v1/auth/signup", json=signup_payload)
    assert response.status_code == status.HTTP_201_CREATED
    signup_data = response.json()
    assert signup_data["success"] is True
    user_id = signup_data["data"]["id"]

    # 2. Login
    login_payload = {"email": email, "password": password}
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    login_data = response.json()
    assert login_data["success"] is True
    access_token = login_data["data"]["access_token"]
    refresh_token = login_data["data"]["refresh_token"]

    # 3. List Active Sessions
    # Set cookies explicitly for testing
    client.cookies.set("access_token", access_token)
    client.cookies.set("refresh_token", refresh_token)
    response = client.get("/api/v1/auth/sessions")
    assert response.status_code == status.HTTP_200_OK
    sessions_data = response.json()
    assert sessions_data["success"] is True
    assert len(sessions_data["data"]) == 1
    session_id = sessions_data["data"][0]["id"]

    # 4. Refresh Token Rotation
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == status.HTTP_200_OK
    refresh_data = response.json()
    assert refresh_data["success"] is True
    new_access_token = refresh_data["data"]["access_token"]
    new_refresh_token = refresh_data["data"]["refresh_token"]

    # 5. Token Replay Attack Detection
    # Attempting to refresh again using the OLD refresh token
    client.cookies.set("refresh_token", refresh_token)
    response = client.post("/api/v1/auth/refresh")
    # Should trigger revocation of the entire family and return 401
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Verify that the new refresh token is also revoked
    client.cookies.set("refresh_token", new_refresh_token)
    response = client.post("/api/v1/auth/refresh")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_lockout_mechanism(client):
    email = "lockoutuser@example.com"
    password = "securePassword123"

    # Register
    signup_payload = {
        "email": email,
        "password": password,
        "first_name": "Lock",
        "last_name": "Out"
    }
    client.post("/api/v1/auth/signup", json=signup_payload)

    # Trigger 5 login failures
    login_payload = {"email": email, "password": "wrongpassword"}
    for _ in range(5):
        response = client.post("/api/v1/auth/login", json=login_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # 6th attempt (even with CORRECT password) should be locked out
    correct_login_payload = {"email": email, "password": password}
    response = client.post("/api/v1/auth/login", json=correct_login_payload)
    assert response.status_code == status.HTTP_423_LOCKED

def test_password_change_flow(client):
    email = "pwdchange@example.com"
    password = "securePassword123"

    # Signup
    signup_payload = {
        "email": email,
        "password": password,
        "first_name": "Pwd",
        "last_name": "Change"
    }
    client.post("/api/v1/auth/signup", json=signup_payload)

    # Login
    login_payload = {"email": email, "password": password}
    login_res = client.post("/api/v1/auth/login", json=login_payload).json()
    access_token = login_res["data"]["access_token"]

    # Change password
    client.cookies.set("access_token", access_token)
    change_payload = {
        "current_password": password,
        "new_password": "brandNewPassword321"
    }
    response = client.post("/api/v1/auth/password/change", json=change_payload)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Login with old password should fail
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Login with new password should succeed
    response = client.post("/api/v1/auth/login", json={"email": email, "password": "brandNewPassword321"})
    assert response.status_code == status.HTTP_200_OK
