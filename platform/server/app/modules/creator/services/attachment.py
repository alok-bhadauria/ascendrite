import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.audit.base import AuditService
from app.modules.assets.services.base import AssetService
from app.modules.creator.models.attachment import AssetAttachmentModel
from app.modules.creator.repositories.attachment import AssetAttachmentRepository
from app.modules.creator.repositories.draft import DraftResourceRepository

logger = logging.getLogger(__name__)

class AssetAttachmentService:
    def __init__(
        self,
        repo: AssetAttachmentRepository,
        draft_repo: DraftResourceRepository,
        asset_service: AssetService,
        db: AsyncIOMotorDatabase,
        audit_service: AuditService
    ):
        self.repo = repo
        self.draft_repo = draft_repo
        self.asset_service = asset_service
        self.db = db
        self.audit_service = audit_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    def _to_db_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def attach_asset(
        self,
        draft_id: str,
        asset_id: str,
        context: RuntimeContext
    ) -> AssetAttachmentModel:
        self._require_capability(context, "creator:write")
        db_draft_id = self._to_db_id(draft_id)

        # 1. Verify draft exists
        draft = await self.draft_repo.get_by_id(draft_id)
        if not draft:
            raise AppException(f"Draft '{draft_id}' not found.", code="NOT_FOUND", status_code=404)

        # 2. Verify asset exists in asset platform
        try:
            asset = await self.asset_service.get_asset_metadata(asset_id, context)
        except Exception:
            raise AppException(f"Referenced asset '{asset_id}' not found in the asset platform.", code="NOT_FOUND", status_code=404)

        # 3. Check duplicate link
        link = await self.repo.get_link(db_draft_id, asset_id)
        if link:
            return link

        # 4. Create attachment
        attachment = AssetAttachmentModel(
            draft_id=db_draft_id,
            asset_id=asset_id,
            attached_at=datetime.now(timezone.utc)
        )
        created = await self.repo.create(attachment)

        await self.audit_service.log("creator.asset.attach", f"draft:{draft_id}", "success", context, {"asset_id": asset_id})
        return created

    async def detach_asset(
        self,
        draft_id: str,
        asset_id: str,
        context: RuntimeContext
    ) -> bool:
        self._require_capability(context, "creator:write")
        db_draft_id = self._to_db_id(draft_id)

        link = await self.repo.get_link(db_draft_id, asset_id)
        if not link:
            return False

        deleted = await self.repo.delete(str(link.id))
        if deleted:
            await self.audit_service.log("creator.asset.detach", f"draft:{draft_id}", "success", context, {"asset_id": asset_id})
        return deleted

    async def get_attachments(self, draft_id: str, context: RuntimeContext) -> List[AssetAttachmentModel]:
        self._require_capability(context, "creator:read")
        db_draft_id = self._to_db_id(draft_id)
        return await self.repo.get_by_draft(db_draft_id)
