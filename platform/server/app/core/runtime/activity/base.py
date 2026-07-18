import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.core.runtime.context import RuntimeContext

class ActivityRecord(BaseModel):
    """
    User-facing activity feed document layout.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    user_id: str
    type: str
    title: str
    description: str
    correlation_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ActivityService(ABC):
    """Interface boundary for logging user activities"""
    @abstractmethod
    async def log(
        self,
        type: str,
        title: str,
        description: str,
        context: RuntimeContext,
        metadata: Dict[str, Any]
    ) -> None:
        pass
