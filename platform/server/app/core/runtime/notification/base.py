from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class NotificationChannel(ABC):
    """Abstract interface representing a physical notification delivery channel"""
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def deliver(
        self,
        recipient_id: str,
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        pass

class NotificationService(ABC):
    """Interface boundary for sending notifications across channels"""
    @abstractmethod
    async def send(
        self,
        recipient_id: str,
        channels: List[str],
        title: str,
        body: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        pass
