from typing import List, Optional
from pydantic import BaseModel

class AuthenticatedPrincipal(BaseModel):
    """
    Abstract representation of an authenticated client context.
    Allows authorization evaluator to check permissions for humans, AI agents, 
    service accounts, and automation workers via the same unified API.
    """
    id: str
    identity_type: str  # user | ai_agent | service_account
    role: str
    capabilities: List[str]
