from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchDocument(BaseModel):
    id: str = Field(..., alias="_id")
    doc_type: str  # subject | syllabus | module | topic | content
    title: str
    body: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        populate_by_name = True
        json_encoders = {
            # Standard encoders if needed
        }

class SearchProvider(ABC):
    @abstractmethod
    async def index_document(self, doc: SearchDocument) -> None:
        pass

    @abstractmethod
    async def remove_document(self, doc_id: str, doc_type: str) -> None:
        pass

    @abstractmethod
    async def search(self, query: str, doc_type: Optional[str] = None) -> List[SearchDocument]:
        pass
