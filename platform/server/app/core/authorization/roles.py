from typing import Dict, List
from app.core.authorization.capabilities import Capability

# Reusable bundles mapping user roles to specific sets of capability scopes
ROLE_BUNDLES: Dict[str, List[Capability]] = {
    "Student": [
        Capability.USER_READ_SELF,
        Capability.USER_UPDATE_SELF,
        Capability.KNOWLEDGE_READ,
        Capability.LEARNING_READ,
        Capability.LEARNING_WRITE,
        Capability.ASSESSMENT_READ,
        Capability.ASSESSMENT_WRITE,
        Capability.AI_QUERY,
        Capability.SYSTEM_TELEMETRY,
    ],
    "Contributor": [
        Capability.USER_READ_SELF,
        Capability.USER_UPDATE_SELF,
        Capability.KNOWLEDGE_READ,
        Capability.KNOWLEDGE_WRITE,
        Capability.KNOWLEDGE_PUBLISH,
        Capability.LEARNING_READ,
        Capability.LEARNING_WRITE,
        Capability.ASSESSMENT_READ,
        Capability.ASSESSMENT_WRITE,
        Capability.AI_QUERY,
        Capability.SYSTEM_TELEMETRY,
    ],
    "Admin": [
        *list(Capability)  # Receives all system permissions
    ],
    "AIAgent": [
        Capability.KNOWLEDGE_READ,
        Capability.LEARNING_READ,
        Capability.AI_QUERY,
        Capability.SYSTEM_TELEMETRY,
    ],
    "ServiceAccount": [
        Capability.KNOWLEDGE_READ,
        Capability.SYSTEM_TELEMETRY,
    ]
}
