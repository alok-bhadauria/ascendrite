import asyncio
import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient

from app.core.errors import ForbiddenException, AppException
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.runtime.context import RuntimeContext
from app.infrastructure.storage.manager import StorageManager
from app.infrastructure.storage.rustfs import get_rustfs
from app.modules.assets.models.asset import AssetStatus
from app.modules.assets.repositories.asset import MongoAssetRepository
from app.modules.assets.services.service import MongoAssetService
from app.api.v1.dependencies import get_event_dispatcher, get_audit_service, get_activity_service

@pytest.mark.anyio
async def test_asset_lifecycle_flow(client):
    # Initialize a test-specific Motor client bound to the active test event loop with admin credentials
    test_client = AsyncIOMotorClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = test_client["ascendrite"]

    # Initialize Services
    repo = MongoAssetRepository(db)
    storage_provider = get_rustfs()
    storage_mgr = StorageManager(storage_provider)
    event_disp = get_event_dispatcher()
    audit_serv = await get_audit_service(db)
    activity_serv = await get_activity_service(db)

    asset_service = MongoAssetService(
        repo=repo,
        storage_mgr=storage_mgr,
        event_dispatcher=event_disp,
        audit_service=audit_serv,
        activity_service=activity_serv
    )

    # 1. Setup Student Principal A Context
    student_a = AuthenticatedPrincipal(
        id="student-a-id",
        identity_type="user",
        role="Student",
        capabilities=["knowledge:read"]
    )
    ctx_a = RuntimeContext(
        correlation_id="corr-asset-upload-123",
        principal=student_a,
        ip_address="127.0.0.1",
        user_agent="Firefox"
    )

    # 2. Upload Asset
    binary_content = b"pdf-content-bytes-data-stream"
    asset = await asset_service.upload_asset(
        filename="lecture_notes.pdf",
        content_type="application/pdf",
        data=binary_content,
        context=ctx_a
    )

    assert asset.id is not None
    assert asset.owner_id == "student-a-id"
    assert asset.filename == "lecture_notes.pdf"
    assert asset.content_type == "application/pdf"
    assert asset.size == len(binary_content)
    assert asset.status == AssetStatus.UPLOADED

    # 3. Retrieve Asset (Owner Access)
    retrieved_data = await asset_service.retrieve_asset_binary(asset.id, ctx_a)
    assert retrieved_data == b"mock-binary-data"  # Mock returns get_object boundary mock bytes

    # 4. Retrieve Asset (Unauthorized student access - Forbidden)
    student_b = AuthenticatedPrincipal(
        id="student-b-id",
        identity_type="user",
        role="Student",
        capabilities=[]
    )
    ctx_b = RuntimeContext(correlation_id="corr-unauthorized", principal=student_b)

    with pytest.raises(ForbiddenException):
        await asset_service.retrieve_asset_binary(asset.id, ctx_b)

    # 5. Retrieve Asset (Admin override access)
    admin_principal = AuthenticatedPrincipal(
        id="admin-id",
        identity_type="user",
        role="Admin",
        capabilities=["system:admin"]
    )
    ctx_admin = RuntimeContext(correlation_id="corr-admin-override", principal=admin_principal)
    
    admin_retrieved_data = await asset_service.retrieve_asset_binary(asset.id, ctx_admin)
    assert admin_retrieved_data == b"mock-binary-data"

    # 6. Delete Asset (Lifecycle Transition to DELETED)
    deleted_asset = await asset_service.transition_asset_lifecycle(
        asset_id=asset.id,
        new_status=AssetStatus.DELETED,
        context=ctx_a
    )
    assert deleted_asset.status == AssetStatus.DELETED

    # 7. Assert Deleted Asset is inaccessible via normal lookups
    with pytest.raises(AppException) as excinfo:
        await asset_service.retrieve_asset_binary(asset.id, ctx_a)
    assert excinfo.value.status_code == 404

    # 8. Verify Runtime Integration side-effects via sync MongoClient
    sync_client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    sync_db = sync_client["ascendrite"]
    
    # Audit log check
    audit_rec = sync_db["audit_logs"].find_one({"action": "asset.upload"})
    assert audit_rec is not None
    assert audit_rec["actor_id"] == "student-a-id"
    assert audit_rec["resource"] == f"asset:{asset.id}"

    # Activity log check
    activity_rec = sync_db["activity_logs"].find_one({"type": "asset_upload"})
    assert activity_rec is not None
    assert activity_rec["user_id"] == "student-a-id"

    sync_client.close()
