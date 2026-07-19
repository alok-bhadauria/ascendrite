import pytest
from datetime import datetime, timezone
from bson import ObjectId
from fastapi import status
from pymongo import MongoClient
from app.main import app
from app.api.v1.dependencies import get_current_principal
from app.core.authorization.principal import AuthenticatedPrincipal

@pytest.fixture
def mock_creator():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b3333",
        identity_type="user",
        role="Contributor",
        capabilities=["creator:read", "creator:write", "asset:read", "asset:write"]
    )

@pytest.fixture
def seed_creator_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]
    db["subjects"].drop()
    db["topics"].drop()
    db["knowledge_contents"].drop()
    db["creator_drafts"].drop()
    db["creator_asset_attachments"].drop()
    db["creator_publishing_workflows"].drop()
    db["assets"].drop()

    # Seed subject
    db["subjects"].insert_one({
        "_id": "sub-123",
        "name": "Physics",
        "code": "PHYS101",
        "description": "Intro to Physics",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    # Seed asset
    db["assets"].insert_one({
        "_id": "asset-abc",
        "owner_id": "60c72b2f9b1d8e2b8c8b3333",
        "owner_type": "user",
        "filename": "diagram.png",
        "content_type": "image/png",
        "size": 1024,
        "checksum": "dummy",
        "storage_key": "dummy",
        "status": "uploaded",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    })

    yield db
    mongo_client.close()

def test_draft_workspace_crud(client, mock_creator, seed_creator_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_creator

    # 1. Create Valid Draft
    response = client.post("/api/v1/creator/drafts/", json={
        "resource_type": "topic",
        "content": {
            "name": "Newtonian Gravity",
            "subject_id": "sub-123",
            "description": "Study of classical mechanics gravity rules."
        }
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()["data"]
    draft_id = data["_id"]
    assert data["resource_type"] == "topic"
    assert data["content"]["name"] == "Newtonian Gravity"
    assert data["validation_status"] == "pending"

    # 2. Get Draft
    response = client.get(f"/api/v1/creator/drafts/{draft_id}")
    assert response.status_code == status.HTTP_200_OK

    # 3. Update Draft
    response = client.put(f"/api/v1/creator/drafts/{draft_id}", json={
        "content": {
            "name": "Newtonian Mechanics",
            "subject_id": "sub-123",
            "description": "Updated gravity rules."
        }
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["content"]["name"] == "Newtonian Mechanics"

    # 4. Duplicate Draft
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/duplicate")
    assert response.status_code == status.HTTP_200_OK
    assert "(Copy)" in response.json()["data"]["content"]["name"]

    # 5. Validate Valid Draft
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/validate")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["validation_status"] == "valid"

    # 6. Validate Invalid Draft (missing subject_id)
    response = client.post("/api/v1/creator/drafts/", json={
        "resource_type": "topic",
        "content": {
            "name": "Invalid Topic"
        }
    })
    invalid_id = response.json()["data"]["_id"]
    response = client.post(f"/api/v1/creator/drafts/{invalid_id}/validate")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["validation_status"] == "invalid"
    assert len(response.json()["data"]["validation_errors"]) > 0

    app.dependency_overrides.clear()

def test_asset_attachments(client, mock_creator, seed_creator_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_creator

    # Create draft
    response = client.post("/api/v1/creator/drafts/", json={
        "resource_type": "topic",
        "content": {"name": "Gravity", "subject_id": "sub-123"}
    })
    draft_id = response.json()["data"]["_id"]

    # Attach asset
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/assets/attach?asset_id=asset-abc")
    assert response.status_code == status.HTTP_201_CREATED

    # Get attachments
    response = client.get(f"/api/v1/creator/drafts/{draft_id}/assets")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["asset_id"] == "asset-abc"

    # Detach asset
    response = client.delete(f"/api/v1/creator/drafts/{draft_id}/assets/detach?asset_id=asset-abc")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    app.dependency_overrides.clear()

def test_publishing_pipeline_workflow(client, mock_creator, seed_creator_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_creator

    # Create valid draft
    response = client.post("/api/v1/creator/drafts/", json={
        "resource_type": "topic",
        "content": {
            "name": "Gravity Waves",
            "subject_id": "sub-123",
            "description": "General Relativity space curvature"
        }
    })
    draft_id = response.json()["data"]["_id"]

    # Submit for review
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/submit-review")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "ready_for_review"

    # Approve draft
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/approve")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "approved"

    # Publish draft
    response = client.post(f"/api/v1/creator/drafts/{draft_id}/publish")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["status"] == "published"

    # Check published database entry
    published_id = response.json()["data"]["history"][-1]["notes"].split(": ")[-1]
    published_topic = seed_creator_db["topics"].find_one({"_id": published_id})
    assert published_topic is not None
    assert published_topic["name"] == "Gravity Waves"

    app.dependency_overrides.clear()
