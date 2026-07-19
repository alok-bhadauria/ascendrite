import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.modules.collaboration.models.activity import CollaborationActivityModel, CollaborationNotificationModel
from app.modules.collaboration.repositories.activity import CollaborationActivityRepository, CollaborationNotificationRepository

logger = logging.getLogger(__name__)

class CollaborationActivityService:
    def __init__(
        self,
        activity_repo: CollaborationActivityRepository,
        notification_repo: CollaborationNotificationRepository
    ):
        self.activity_repo = activity_repo
        self.notification_repo = notification_repo

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

    async def log_activity(
        self,
        team_id: Optional[str],
        resource_id: str,
        resource_type: str,
        action_type: str,
        description: str,
        context: RuntimeContext
    ) -> CollaborationActivityModel:
        actor_id = self._to_db_id(context.principal.id)
        db_team_id = self._to_db_id(team_id) if team_id else None

        activity = CollaborationActivityModel(
            team_id=db_team_id,
            resource_id=resource_id,
            resource_type=resource_type,
            actor_id=actor_id,
            action_type=action_type,
            description=description,
            created_at=datetime.now(timezone.utc)
        )
        return await self.activity_repo.create(activity)

    async def get_activities(self, resource_id: str, context: RuntimeContext) -> List[CollaborationActivityModel]:
        self._require_capability(context, "collab:read")
        return await self.activity_repo.get_by_resource(resource_id)

    async def create_notification(
        self,
        recipient_id: str,
        event_type: str,
        payload: Dict[str, Any]
    ) -> CollaborationNotificationModel:
        db_recipient_id = self._to_db_id(recipient_id)
        notification = CollaborationNotificationModel(
            recipient_id=db_recipient_id,
            event_type=event_type,
            payload=payload,
            is_read=False,
            created_at=datetime.now(timezone.utc)
        )
        return await self.notification_repo.create(notification)

    async def get_notifications(self, context: RuntimeContext) -> List[CollaborationNotificationModel]:
        self._require_capability(context, "collab:read")
        recipient_id = self._to_db_id(context.principal.id)
        return await self.notification_repo.get_by_recipient(recipient_id)

    async def mark_notification_as_read(self, notification_id: str, context: RuntimeContext) -> bool:
        self._require_capability(context, "collab:write")
        
        notification = await self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise AppException("Notification not found.", code="NOT_FOUND", status_code=404)

        if str(notification.recipient_id) != str(context.principal.id):
            raise ForbiddenException("You cannot modify another user's notifications.")

        notification.is_read = True
        await self.notification_repo.update(notification_id, notification)
        return True
