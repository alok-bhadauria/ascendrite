import logging
from typing import List, Optional
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.assets.services.base import AssetService
from app.modules.knowledge.models.content import KnowledgeContentModel, PublicationState
from app.modules.knowledge.repositories.base import KnowledgeContentRepository
from app.modules.knowledge.services.base import AcademicStructureService, KnowledgeContentService

logger = logging.getLogger(__name__)

class MongoKnowledgeContentService(KnowledgeContentService):
    def __init__(
        self,
        repo: KnowledgeContentRepository,
        academic_service: AcademicStructureService,
        asset_service: AssetService,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService,
        search_service=None
    ):
        self.repo = repo
        self.academic_service = academic_service
        self.asset_service = asset_service
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self.activity_service = activity_service
        self.search_service = search_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    def _validate_visibility(self, content: KnowledgeContentModel, context: RuntimeContext) -> None:
        if content.status == PublicationState.PUBLISHED:
            # Accessible to anyone with read capability
            self._require_capability(context, "knowledge:read")
            return

        # Draft or Archived: Requires knowledge:write OR must be the author
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied for unpublished content.")

        is_author = (content.created_by == context.principal.id)
        has_write = ("knowledge:write" in context.principal.capabilities or context.principal.role == "Admin")

        if not (is_author or has_write):
            raise ForbiddenException("You are not authorized to view this unpublished content.")

    async def _validate_assets(self, assets: List[str], context: RuntimeContext) -> None:
        for asset_id in assets:
            try:
                await self.asset_service.get_asset_metadata(asset_id, context)
            except Exception as e:
                logger.error(f"Asset validation failed for ID '{asset_id}': {e}")
                raise AppException(
                    f"Referenced asset '{asset_id}' is invalid, inactive, or unauthorized.",
                    code="INVALID_ASSET_REFERENCE",
                    status_code=400
                )

    async def create_content(
        self,
        topic_id: str,
        category: str,
        title: str,
        body: str,
        assets: List[str],
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        self._require_capability(context, "knowledge:write")
        # Validate parent topic exists
        await self.academic_service.get_topic(topic_id, context)

        # Validate assets
        await self._validate_assets(assets, context)

        content = KnowledgeContentModel(
            topic_id=topic_id,
            category=category,
            title=title,
            body=body,
            assets=assets,
            created_by=context.principal.id
        )
        created = await self.repo.create(content)

        # Sync index search if search_service is present
        if self.search_service:
            await self.search_service.index_content(created)

        await self.event_dispatcher.dispatch(Event(name="ContentCreated", payload={"content_id": created.id}, context=context))
        await self.audit_service.log("knowledge.content.create", f"content:{created.id}", "success", context, metadata={})
        await self.activity_service.log("content_create", f"Created Content: {title}", f"Category: {category}", context, metadata={})
        return created

    async def get_content(self, content_id: str, context: RuntimeContext) -> KnowledgeContentModel:
        content = await self.repo.get_by_id(content_id)
        if not content or content.status == PublicationState.DELETED:
            raise AppException(f"Knowledge Content '{content_id}' not found.", code="NOT_FOUND", status_code=404)
        
        self._validate_visibility(content, context)
        return content

    async def update_content(
        self,
        content_id: str,
        title: str,
        body: str,
        assets: List[str],
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        self._require_capability(context, "knowledge:write")
        content = await self.get_content(content_id, context)

        # Validate assets
        await self._validate_assets(assets, context)

        content.title = title
        content.body = body
        content.assets = assets
        updated = await self.repo.update(content_id, content)

        if self.search_service:
            await self.search_service.index_content(updated)

        await self.audit_service.log("knowledge.content.update", f"content:{content_id}", "success", context, metadata={})
        return updated

    async def list_content_by_topic(self, topic_id: str, context: RuntimeContext) -> List[KnowledgeContentModel]:
        # Validate parent topic exists
        await self.academic_service.get_topic(topic_id, context)

        raw_list = await self.repo.list_by_topic(topic_id)
        
        # Enforce visibility rules
        filtered = []
        for content in raw_list:
            try:
                self._validate_visibility(content, context)
                filtered.append(content)
            except ForbiddenException:
                pass
        return filtered

    async def delete_content(self, content_id: str, context: RuntimeContext) -> KnowledgeContentModel:
        self._require_capability(context, "knowledge:write")
        content = await self.get_content(content_id, context)

        content.status = PublicationState.DELETED
        updated = await self.repo.update(content_id, content)

        if self.search_service:
            await self.search_service.remove_content(content_id)

        await self.event_dispatcher.dispatch(Event(name="ContentDeleted", payload={"content_id": content_id}, context=context))
        await self.audit_service.log("knowledge.content.delete", f"content:{content_id}", "success", context, metadata={})
        await self.activity_service.log("content_delete", f"Deleted Content: {content.title}", "", context, metadata={})
        return updated

    async def transition_publication_state(
        self,
        content_id: str,
        new_status: PublicationState,
        context: RuntimeContext
    ) -> KnowledgeContentModel:
        self._require_capability(context, "knowledge:publish")
        content = await self.get_content(content_id, context)

        old_status = content.status
        content.status = new_status
        updated = await self.repo.update(content_id, content)

        if self.search_service:
            if new_status == PublicationState.DELETED:
                await self.search_service.remove_content(content_id)
            else:
                await self.search_service.index_content(updated)

        # Side effects
        event_name = "ContentPublished" if new_status == PublicationState.PUBLISHED else "ContentArchived"
        await self.event_dispatcher.dispatch(Event(name=event_name, payload={"content_id": content_id, "old_status": old_status.value, "new_status": new_status.value}, context=context))
        await self.audit_service.log("knowledge.content.publish", f"content:{content_id}", "success", context, {"old_status": old_status.value, "new_status": new_status.value})
        await self.activity_service.log("content_publish", f"Transitioned: {content.title}", f"New status: {new_status.value}", context, metadata={})

        return updated
