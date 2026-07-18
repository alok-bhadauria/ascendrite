from fastapi import Depends
from app.core.errors import ForbiddenException
from app.core.authorization.capabilities import Capability
from app.core.authorization.principal import AuthenticatedPrincipal
from app.core.authorization.evaluator import evaluate_capability
from app.api.v1.dependencies import get_current_user

async def get_current_principal(
    current_user = Depends(get_current_user)
) -> AuthenticatedPrincipal:
    """FastAPI dependency converting active UserModel into AuthenticatedPrincipal context"""
    from app.core.authorization.evaluator import resolve_capabilities
    caps = resolve_capabilities(current_user.role)
    return AuthenticatedPrincipal(
        id=str(current_user.id),
        identity_type="user",
        role=current_user.role,
        capabilities=caps
    )

class RequireCapability:
    """Route guard injecting capability-based permission evaluations"""
    def __init__(self, capability: Capability):
        self.capability = capability

    def __call__(
        self,
        principal: AuthenticatedPrincipal = Depends(get_current_principal)
    ) -> AuthenticatedPrincipal:
        if not evaluate_capability(principal.capabilities, self.capability):
            raise ForbiddenException(
                message=f"Missing required capability context: '{self.capability.value}'"
            )
        return principal
