import uuid
import logging
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.runtime.audit.base import AuditService, AuditRecord
from app.core.runtime.context import RuntimeContext

logger = logging.getLogger(__name__)

class MongoAuditService(AuditService):
    """MongoDB adapter persisting system audit traces"""
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["audit_logs"]

    async def log(
        self,
        action: str,
        resource: str,
        status: str,
        context: RuntimeContext,
        metadata: Dict[str, Any]
    ) -> None:
        actor_id = context.principal.id if context.principal else "anonymous"
        actor_type = context.principal.identity_type if context.principal else "anonymous"

        record = AuditRecord(
            id=str(uuid.uuid4()),
            actor_id=actor_id,
            actor_type=actor_type,
            action=action,
            resource=resource,
            status=status,
            correlation_id=context.correlation_id,
            metadata={
                **metadata,
                "ip_address": context.ip_address,
                "user_agent": context.user_agent
            }
        )
        try:
            await self.collection.insert_one(record.model_dump())
            logger.info(f"Audit trace recorded: actor={actor_id}, action={action}")
        except Exception as e:
            logger.error(f"Failed to persist audit log to MongoDB: {e}", exc_info=True)
