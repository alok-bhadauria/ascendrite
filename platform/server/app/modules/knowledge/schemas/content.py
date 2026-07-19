from pydantic import BaseModel, Field
from typing import List
from app.modules.knowledge.models.content import PublicationState

class KnowledgeContentCreate(BaseModel):
    topic_id: str
    category: str  # notes | revision | interview
    title: str
    body: str
    assets: List[str] = Field(default_factory=list)

class KnowledgeContentUpdate(BaseModel):
    title: str
    body: str
    assets: List[str] = Field(default_factory=list)

class PublicationStateTransition(BaseModel):
    status: PublicationState
