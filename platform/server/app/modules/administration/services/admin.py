import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.audit.base import AuditService
from app.modules.administration.models.config import PlatformConfigModel
from app.modules.administration.repositories.config import PlatformConfigRepository

logger = logging.getLogger(__name__)

class AdministrationService:
    def __init__(
        self,
        repo: PlatformConfigRepository,
        db: AsyncIOMotorDatabase,
        audit_service: AuditService
    ):
        self.repo = repo
        self.db = db
        self.audit_service = audit_service

    def _require_admin_role(self, context: RuntimeContext) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        # Enforce that only users with role Admin can perform administrative functions
        if context.principal.role != "Admin":
            raise ForbiddenException("Only administrators can perform this action.")

    async def get_platform_config(self, context: RuntimeContext) -> PlatformConfigModel:
        self._require_admin_role(context)
        config = await self.repo.get_by_id("global")
        if not config:
            # Seed default configuration
            config = PlatformConfigModel(
                id="global",
                maintenance_mode=False,
                allowed_domains=["*"],
                feature_flags={"new_search_indexer": True}
            )
            await self.repo.create(config)
        return config

    async def update_platform_config(
        self,
        config_data: Dict[str, Any],
        context: RuntimeContext
    ) -> PlatformConfigModel:
        self._require_admin_role(context)
        
        config = await self.get_platform_config(context)
        if "maintenance_mode" in config_data:
            config.maintenance_mode = config_data["maintenance_mode"]
        if "allowed_domains" in config_data:
            config.allowed_domains = config_data["allowed_domains"]
        if "feature_flags" in config_data:
            config.feature_flags = config_data["feature_flags"]
        config.updated_at = datetime.now(timezone.utc)

        await self.repo.update("global", config)
        await self.audit_service.log("admin.config.update", "config:global", "success", context, {})
        return config

    async def get_administrative_dashboard_stats(self, context: RuntimeContext) -> Dict[str, Any]:
        self._require_admin_role(context)

        # Dynamic aggregation metrics over various core collection structures
        user_count = await self.db["users"].count_documents({})
        team_count = await self.db["collaboration_teams"].count_documents({})
        topic_count = await self.db["topics"].count_documents({})
        content_count = await self.db["knowledge_contents"].count_documents({})
        assessment_count = await self.db["assessments"].count_documents({})
        backlog_count = await self.db["creator_publishing_workflows"].count_documents({"status": "ready_for_review"})
        asset_count = await self.db["assets"].count_documents({})

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "users": user_count,
            "teams": team_count,
            "published_topics": topic_count,
            "published_contents": content_count,
            "published_assessments": assessment_count,
            "review_backlog": backlog_count,
            "total_assets": asset_count
        }
