import logging
from typing import Any, Dict, List, Optional
from app.core.runtime.notification.base import NotificationService, NotificationChannel

logger = logging.getLogger(__name__)

class NotificationDispatcher(NotificationService):
    """
    Coordinates routing and delivery of notifications across active channels.
    Channels are replaceable without modifying the dispatcher context.
    """
    def __init__(self, channels: List[NotificationChannel]):
        self._channels: Dict[str, NotificationChannel] = {c.name: c for c in channels}

    async def send(
        self,
        recipient_id: str,
        channels: List[str],
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        for channel_name in channels:
            channel = self._channels.get(channel_name)
            if not channel:
                logger.warning(f"Notification channel not found: '{channel_name}'")
                continue
            try:
                success = await channel.deliver(recipient_id, title, body, metadata)
                if success:
                    logger.info(f"Notification sent successfully: channel={channel_name}, recipient={recipient_id}")
                else:
                    logger.warning(f"Notification delivery reports failure: channel={channel_name}, recipient={recipient_id}")
            except Exception as e:
                logger.error(
                    f"Failed to dispatch notification via '{channel_name}' for '{recipient_id}': {e}",
                    exc_info=True
                )
