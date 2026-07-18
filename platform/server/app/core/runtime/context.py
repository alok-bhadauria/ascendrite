from typing import Optional
from pydantic import BaseModel
from app.core.authorization.principal import AuthenticatedPrincipal

class RuntimeContext(BaseModel):
    """
    Shared context representation across the platform runtime layers.
    Maintains correlation ID boundaries, IP coordinates, and authenticated Principal.
    """
    correlation_id: str
    principal: Optional[AuthenticatedPrincipal] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
