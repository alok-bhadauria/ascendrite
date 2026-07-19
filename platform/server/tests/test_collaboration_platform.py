import pytest
from datetime import datetime, timezone
from bson import ObjectId
from pymongo import MongoClient
from fastapi import status
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_team_owner():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b3333",
        identity_type="user",
        role="Contributor",
        capabilities=["collab:read", "collab:write"]
    )

@pytest.fixture
def mock_team_member():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b4444",
        identity_type="user",
        role="Contributor",
        capabilities=["collab:read", "collab:write"]
    )

@pytest.fixture
def seed_collab_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]
    db["users"].delete_many({})
    db["collaboration_teams"].drop()
    db["collaboration_team_memberships"].drop()
    db["collaboration_assignments"].drop()
    db["collaboration_comments"].drop()
    db["collaboration_activities"].drop()
    db["collaboration_notifications"].drop()

    # Seed users
    db["users"].insert_many([
        {
            "_id": ObjectId("60c72b2f9b1d8e2b8c8b3333"),
            "email": "owner@ascendrite.com",
            "hashed_password": "dummy",
            "name": "Owner User",
            "role": "Contributor",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        },
        {
            "_id": ObjectId("60c72b2f9b1d8e2b8c8b4444"),
            "email": "collaborator@ascendrite.com",
            "hashed_password": "dummy",
            "name": "Collaborator User",
            "role": "Contributor",
            "is_active": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])

    yield db
    mongo_client.close()

def test_team_setup_and_invitation(client, mock_team_owner, mock_team_member, seed_collab_db):
    # 1. Create Team
    app.dependency_overrides[get_current_principal] = lambda: mock_team_owner
    response = client.post("/api/v1/collaboration/teams?name=ContentDevs&description=Physics%20Creators")
    assert response.status_code == status.HTTP_201_CREATED
    team_data = response.json()["data"]
    team_id = team_data["id"]
    assert team_data["name"] == "ContentDevs"

    # 2. Invite Member
    response = client.post(f"/api/v1/collaboration/teams/{team_id}/invite?user_id=60c72b2f9b1d8e2b8c8b4444&role=collaborator")
    assert response.status_code == status.HTTP_200_OK
    membership_id = response.json()["data"]["id"]
    assert response.json()["data"]["status"] == "invited"

    # 3. Accept Invitation (as the invited member)
    app.dependency_overrides[get_current_principal] = lambda: mock_team_member
    response = client.post(f"/api/v1/collaboration/invitations/{membership_id}/accept")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "active"

    # 4. Transfer Ownership (back as team owner)
    app.dependency_overrides[get_current_principal] = lambda: mock_team_owner
    response = client.post(f"/api/v1/collaboration/teams/{team_id}/transfer?new_owner_id=60c72b2f9b1d8e2b8c8b4444")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["owner_id"] == "60c72b2f9b1d8e2b8c8b4444"

    app.dependency_overrides.clear()

def test_collaboration_assignments_and_comments(client, mock_team_owner, seed_collab_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_team_owner

    # 1. Create Assignment
    response = client.post("/api/v1/collaboration/assignments?resource_id=draft-123&resource_type=topic&assignee_id=60c72b2f9b1d8e2b8c8b4444")
    assert response.status_code == status.HTTP_201_CREATED
    ass_id = response.json()["data"]["id"]
    assert response.json()["data"]["status"] == "assigned"

    # 2. Update Status
    response = client.put(f"/api/v1/collaboration/assignments/{ass_id}/status?status=in_progress")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "in_progress"

    # 3. Post Comment
    response = client.post("/api/v1/collaboration/comments?resource_id=draft-123&content=Needs%20validation%20checks")
    assert response.status_code == status.HTTP_201_CREATED

    # 4. Get Comments
    response = client.get("/api/v1/collaboration/comments?resource_id=draft-123")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["content"] == "Needs validation checks"

    app.dependency_overrides.clear()

def test_collaboration_activity_and_notifications(client, mock_team_owner, seed_collab_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_team_owner

    # 1. Log activity directly in repository to test timelines
    seed_collab_db["collaboration_activities"].insert_one({
        "team_id": None,
        "resource_id": "draft-123",
        "resource_type": "topic",
        "actor_id": ObjectId("60c72b2f9b1d8e2b8c8b3333"),
        "action_type": "commented",
        "description": "Posted validation feedback comment",
        "created_at": datetime.now(timezone.utc)
    })

    response = client.get("/api/v1/collaboration/activity?resource_id=draft-123")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["action_type"] == "commented"

    # 2. Add Notification
    seed_collab_db["collaboration_notifications"].insert_one({
        "recipient_id": ObjectId("60c72b2f9b1d8e2b8c8b3333"),
        "event_type": "assignment_assigned",
        "payload": {"task_name": "Review physics questions"},
        "is_read": False,
        "created_at": datetime.now(timezone.utc)
    })

    # Get notifications
    response = client.get("/api/v1/collaboration/notifications")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    notif_id = response.json()["data"][0]["id"]

    # Mark as read
    response = client.post(f"/api/v1/collaboration/notifications/{notif_id}/read")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    app.dependency_overrides.clear()
