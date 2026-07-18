from typing import List
from app.core.authorization.capabilities import Capability
from app.core.authorization.roles import ROLE_BUNDLES

def resolve_capabilities(role: str) -> List[str]:
    """Resolve the explicit list of permission strings bound to a given role name"""
    caps = ROLE_BUNDLES.get(role, [])
    return [c.value for c in caps]

def evaluate_capability(principal_capabilities: List[str], required_capability: Capability) -> bool:
    """Check if the principal context possesses the requested capability"""
    return required_capability.value in principal_capabilities
