from enum import Enum

class Capability(str, Enum):
    """
    Platform-wide Capability registry.
    Naming Convention: <resource>:<action> (e.g. 'knowledge:read', 'system:admin').
    """
    # User Profile/Identity
    USER_READ_SELF = "user:read_self"
    USER_UPDATE_SELF = "user:update_self"
    USER_READ_ALL = "user:read_all"
    USER_WRITE_ALL = "user:write_all"

    # Knowledge Base / Curriculum
    KNOWLEDGE_READ = "knowledge:read"
    KNOWLEDGE_WRITE = "knowledge:write"

    # Progress/Learning trackers
    LEARNING_READ = "learning:read"
    LEARNING_WRITE = "learning:write"

    # Quiz / Assessment evaluations
    ASSESSMENT_READ = "assessment:read"
    ASSESSMENT_WRITE = "assessment:write"
    ASSESSMENT_GRADE = "assessment:grade"

    # Generative AI features
    AI_QUERY = "ai:query"
    AI_ADMIN = "ai:admin"

    # Operational telemetry & system settings
    SYSTEM_TELEMETRY = "system:telemetry"
    SYSTEM_ADMIN = "system:admin"
