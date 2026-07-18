import uuid
import logging
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.runtime.activity.base import ActivityService, ActivityRecord
from app.core.runtime.context import RuntimeContext

logger = logging.getLogger(__name__)

class MongoActivityService(ActivityService):
    """MongoDB adapter persisting user-facing activity feeds"""
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["activity_logs"]

    async def log(
        self,
        type: str,
        title: str,
        description: str,
        context: RuntimeContext,
        metadata: Dict[str, Any]
    ) -> None:
        if not context.principal or context.principal.identity_type != "user":
            logger.warning(f"Skipping user activity log for non-user principal: {context.principal}")
            return

        record = ActivityRecord(
            id=str(uuid.uuid4()),
            user_id=context.principal.id,
            type=type,
            title=title,
            description=description,
            correlation_id=context.correlation_id,
            metadata=metadata
        )
        try:
            await self.collection.insert_one(record.model_dump())
            logger.info(f"User activity feed logged: user_id={context.principal.id}, type={type}")
        except Exception as e:
            logger.error(f"Failed to persist user activity feed to MongoDB: {e}", exc_info=True)
