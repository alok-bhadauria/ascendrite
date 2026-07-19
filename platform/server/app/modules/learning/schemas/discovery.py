from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DiscoverableResource(BaseModel):
    resource_id: str
    resource_type: str  # "subject", "syllabus", "module", "topic", "content", "assessment"
    title: str
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
