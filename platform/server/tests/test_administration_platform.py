import pytest
from datetime import datetime, timezone
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
        capabilities=[]
    )

@pytest.fixture
def mock_non_admin():
    return AuthenticatedPrincipal(
        id="60c72b2f9b1d8e2b8c8b2222",
        identity_type="user",
        role="Contributor",
        capabilities=[]
    )

@pytest.fixture
def seed_admin_db():
    mongo_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = mongo_client["ascendrite"]
    db["platform_configs"].drop()
    db["users"].delete_many({})
    db["collaboration_teams"].drop()
    db["topics"].drop()
    db["knowledge_contents"].drop()
    db["assessments"].drop()
    db["creator_publishing_workflows"].drop()
    db["assets"].drop()

    # Seed data
    db["users"].insert_one({"_id": ObjectId("60c72b2f9b1d8e2b8c8b1111"), "role": "Admin"})
    db["collaboration_teams"].insert_one({"_id": ObjectId(), "name": "Team A"})
    db["topics"].insert_one({"_id": "topic-123", "name": "Topic A"})
    db["knowledge_contents"].insert_one({"_id": ObjectId(), "title": "Content A"})
    db["assessments"].insert_one({"_id": ObjectId(), "title": "Assessment A"})
    db["creator_publishing_workflows"].insert_one({"_id": ObjectId(), "status": "ready_for_review"})
    db["assets"].insert_one({
        "_id": "asset-123",
        "owner_id": "owner-123",
        "owner_type": "user",
        "filename": "img.png",
        "content_type": "image/png",
        "size": 100,
        "checksum": "dummy",
        "storage_key": "dummy",
        "status": "uploaded"
    })

    yield db
    mongo_client.close()

def test_platform_config_crud(client, mock_admin, seed_admin_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_admin

    # 1. Get default config
    response = client.get("/api/v1/admin/config")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["maintenance_mode"] is False

    # 2. Update config
    response = client.put("/api/v1/admin/config", json={
        "maintenance_mode": True,
        "feature_flags": {"new_search_indexer": False}
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["maintenance_mode"] is True
    assert response.json()["data"]["feature_flags"]["new_search_indexer"] is False

    app.dependency_overrides.clear()

def test_administrative_dashboard(client, mock_admin, seed_admin_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_admin

    # Fetch dashboard metrics
    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == status.HTTP_200_OK
    metrics = response.json()["data"]
    assert metrics["users"] == 1
    assert metrics["teams"] == 1
    assert metrics["published_topics"] == 1
    assert metrics["published_contents"] == 1
    assert metrics["published_assessments"] == 1
    assert metrics["review_backlog"] == 1
    assert metrics["total_assets"] == 1

    app.dependency_overrides.clear()

def test_non_admin_forbidden(client, mock_non_admin, seed_admin_db):
    app.dependency_overrides[get_current_principal] = lambda: mock_non_admin

    response = client.get("/api/v1/admin/config")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = client.get("/api/v1/admin/dashboard")
    assert response.status_code == status.HTTP_403_FORBIDDEN

    app.dependency_overrides.clear()
