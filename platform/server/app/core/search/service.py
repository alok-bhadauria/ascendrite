from typing import List, Optional
from app.core.runtime.context import RuntimeContext
from app.core.errors import ForbiddenException
from app.core.search.base import SearchDocument, SearchProvider

class SearchService:
    def __init__(self, provider: SearchProvider):
        self.provider = provider

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    async def search(self, query: str, doc_type: Optional[str] = None, context: RuntimeContext = None) -> List[SearchDocument]:
        if context:
            self._require_capability(context, "knowledge:read")
        return await self.provider.search(query, doc_type)

    async def index_subject(self, subject) -> None:
        doc = SearchDocument(
            id=subject.id,
            doc_type="subject",
            title=subject.name,
            body=f"{subject.code} - {subject.description}",
            metadata={"category": subject.category, "status": subject.status.value}
        )
        await self.provider.index_document(doc)

    async def remove_subject(self, subject_id: str) -> None:
        await self.provider.remove_document(subject_id, "subject")

    async def index_content(self, content) -> None:
        doc = SearchDocument(
            id=content.id,
            doc_type="content",
            title=content.title,
            body=content.body,
            metadata={"category": content.category, "topic_id": content.topic_id, "status": content.status.value}
        )
        await self.provider.index_document(doc)

    async def remove_content(self, content_id: str) -> None:
        await self.provider.remove_document(content_id, "content")
