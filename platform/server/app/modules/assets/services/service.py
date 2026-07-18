import hashlib
import uuid
import logging
from typing import List, Optional
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.infrastructure.storage.manager import StorageManager
from app.modules.assets.models.asset import AssetModel, AssetStatus
from app.modules.assets.repositories.base import AssetRepository
from app.modules.assets.services.base import AssetService

logger = logging.getLogger(__name__)

class MongoAssetService(AssetService):
    """
    MongoDB service coordinator executing asset storage transactions 
    and publishing runtime telemetry updates.
    """
    def __init__(
        self,
        repo: AssetRepository,
        storage_mgr: StorageManager,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.repo = repo
        self.storage_mgr = storage_mgr
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self.activity_service = activity_service

    def _validate_ownership(self, asset: AssetModel, context: RuntimeContext, action: str) -> None:
        if not context.principal:
            raise ForbiddenException(f"Anonymous context is not authorized to {action} this asset.")

        if context.principal.role == "Admin":
            return

        if asset.owner_id != context.principal.id:
            raise ForbiddenException(f"Principal context is not authorized to {action} this asset.")

    async def upload_asset(
        self,
        filename: str,
        content_type: str,
        data: bytes,
        context: RuntimeContext
    ) -> AssetModel:
        if not context.principal:
            raise ForbiddenException("Anonymous requests cannot upload assets.")

        asset_id = str(uuid.uuid4())
        owner_id = context.principal.id
        owner_type = context.principal.identity_type

        # Verify checksum hash
        checksum = hashlib.sha256(data).hexdigest()
        
        # Enforce storage key layout via intermediate manager
        storage_key = self.storage_mgr.generate_storage_key(owner_id, asset_id, filename)
        
        # Save physical binary
        self.storage_mgr.store_object(storage_key, data, content_type)

        asset = AssetModel(
            id=asset_id,
            owner_id=owner_id,
            owner_type=owner_type,
            filename=filename,
            content_type=content_type,
            size=len(data),
            checksum=checksum,
            storage_key=storage_key
        )
        
        created_asset = await self.repo.create(asset)

        # Publish event
        evt = Event(
            name="AssetUploaded",
            payload={"asset_id": asset_id, "owner_id": owner_id, "size": len(data)},
            context=context
        )
        await self.event_dispatcher.dispatch(evt)

        # Audit trace
        await self.audit_service.log(
            action="asset.upload",
            resource=f"asset:{asset_id}",
            status="success",
            context=context,
            metadata={"filename": filename, "checksum": checksum}
        )

        # Activity timeline record
        await self.activity_service.log(
            type="asset_upload",
            title=f"Uploaded file: {filename}",
            description=f"Saved asset to storage key: {storage_key}",
            context=context,
            metadata={"asset_id": asset_id}
        )

        return created_asset

    async def retrieve_asset_binary(self, asset_id: str, context: RuntimeContext) -> bytes:
        asset = await self.repo.get_by_id(asset_id)
        if not asset or asset.status == AssetStatus.DELETED:
            raise AppException(f"Asset '{asset_id}' not found.", code="NOT_FOUND_ASSET", status_code=404)

        self._validate_ownership(asset, context, "retrieve")
        return self.storage_mgr.retrieve_object(asset.storage_key)

    async def get_asset_metadata(self, asset_id: str, context: RuntimeContext) -> AssetModel:
        asset = await self.repo.get_by_id(asset_id)
        if not asset or asset.status == AssetStatus.DELETED:
            raise AppException(f"Asset '{asset_id}' not found.", code="NOT_FOUND_ASSET", status_code=404)

        self._validate_ownership(asset, context, "read metadata")
        return asset

    async def transition_asset_lifecycle(
        self,
        asset_id: str,
        new_status: AssetStatus,
        context: RuntimeContext
    ) -> AssetModel:
        asset = await self.repo.get_by_id(asset_id)
        if not asset or asset.status == AssetStatus.DELETED:
            raise AppException(f"Asset '{asset_id}' not found.", code="NOT_FOUND_ASSET", status_code=404)

        self._validate_ownership(asset, context, f"transition to {new_status.value}")

        old_status = asset.status
        asset.status = new_status
        updated_asset = await self.repo.update(asset_id, asset)

        if new_status == AssetStatus.DELETED:
            evt = Event(
                name="AssetDeleted",
                payload={"asset_id": asset_id, "owner_id": asset.owner_id},
                context=context
            )
            await self.event_dispatcher.dispatch(evt)

            await self.audit_service.log(
                action="asset.delete",
                resource=f"asset:{asset_id}",
                status="success",
                context=context,
                metadata={"old_status": old_status.value}
            )

            await self.activity_service.log(
                type="asset_delete",
                title=f"Deleted file: {asset.filename}",
                description="Logical soft deletion applied successfully.",
                context=context,
                metadata={"asset_id": asset_id}
            )

        return updated_asset

    async def get_owner_assets(self, owner_id: str, context: RuntimeContext) -> List[AssetModel]:
        if not context.principal:
            raise ForbiddenException("Anonymous context is not authorized.")
        if context.principal.role != "Admin" and context.principal.id != owner_id:
            raise ForbiddenException("Not authorized to list this owner's assets.")

        assets = await self.repo.get_by_owner(owner_id)
        return [a for a in assets if a.status != AssetStatus.DELETED]
