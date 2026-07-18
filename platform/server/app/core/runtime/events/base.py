import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Awaitable
from pydantic import BaseModel, Field
from app.core.runtime.context import RuntimeContext

class Event(BaseModel):
    """
    Platform-wide internal application event schema contract.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    payload: Dict[str, Any] = Field(default_factory=dict)
    context: RuntimeContext

class EventDispatcher(ABC):
    """Abstract internal event publisher dispatcher contract"""
    @abstractmethod
    async def dispatch(self, event: Event) -> None:
        pass
