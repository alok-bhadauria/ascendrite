import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.core.runtime.context import RuntimeContext

class AuditRecord(BaseModel):
    """
    System-facing security and operations trace document layout.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actor_id: str
    actor_type: str
    action: str
    resource: str
    status: str
    correlation_id: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AuditService(ABC):
    """Interface boundary for logging platform security audits"""
    @abstractmethod
    async def log(
        self,
        action: str,
        resource: str,
        status: str,
        context: RuntimeContext,
        metadata: Dict[str, Any]
    ) -> None:
        pass
