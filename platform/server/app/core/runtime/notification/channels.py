import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.runtime.notification.base import NotificationChannel

logger = logging.getLogger(__name__)

class InAppNotificationRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recipient_id: str
    title: str
    body: str
    is_read: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)

class InAppChannel(NotificationChannel):
    """In-App delivery channel persisting message feed items to MongoDB"""
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["in_app_notifications"]

    @property
    def name(self) -> str:
        return "in_app"

    async def deliver(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        record = InAppNotificationRecord(
            recipient_id=recipient_id,
            title=title,
            body=body,
            metadata=metadata or {}
        )
        await self.collection.insert_one(record.model_dump())
        return True

class MockEmailChannel(NotificationChannel):
    """Logging-based email simulation channel"""
    @property
    def name(self) -> str:
        return "email"

    async def deliver(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        logger.info(f"[MockEmail] Delivery to {recipient_id}: Title: '{title}', Body: '{body}'")
        return True

class MockSMSChannel(NotificationChannel):
    """Logging-based SMS simulation channel"""
    @property
    def name(self) -> str:
        return "sms"

    async def deliver(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        logger.info(f"[MockSMS] Delivery to {recipient_id}: Title: '{title}', Body: '{body}'")
        return True

class MockPushChannel(NotificationChannel):
    """Logging-based Push Notification simulation channel"""
    @property
    def name(self) -> str:
        return "push"

    async def deliver(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        logger.info(f"[MockPush] Delivery to {recipient_id}: Title: '{title}', Body: '{body}'")
        return True
