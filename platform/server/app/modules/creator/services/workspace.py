import logging
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.modules.creator.models.draft import DraftResourceModel, ValidationStatus
from app.modules.creator.repositories.draft import DraftResourceRepository

logger = logging.getLogger(__name__)

class ContentWorkspaceService:
    def __init__(
        self,
        repo: DraftResourceRepository,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService
    ):
        self.repo = repo
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    def _to_db_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def create_draft(
        self,
        resource_type: str,
        content: Dict[str, Any],
        context: RuntimeContext
    ) -> DraftResourceModel:
        self._require_capability(context, "creator:write")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        allowed_types = ["topic", "content", "question", "assessment"]
        if resource_type not in allowed_types:
            raise AppException(f"Unsupported draft resource type: '{resource_type}'.", code="INVALID_TYPE", status_code=400)

        draft = DraftResourceModel(
            resource_type=resource_type,
            content=content,
            validation_status=ValidationStatus.PENDING,
            validation_errors=[],
            created_by=db_user_id
        )
        created = await self.repo.create(draft)

        await self.event_dispatcher.dispatch(Event(
            name="DraftCreated",
            payload={"draft_id": str(created.id), "resource_type": resource_type},
            context=context
        ))
        await self.audit_service.log("creator.draft.create", f"draft:{created.id}", "success", context, {})
        return created

    async def get_draft(self, draft_id: str, context: RuntimeContext) -> DraftResourceModel:
        self._require_capability(context, "creator:read")
        draft = await self.repo.get_by_id(draft_id)
        if not draft:
            raise AppException(f"Draft '{draft_id}' not found.", code="NOT_FOUND", status_code=404)
        return draft

    async def update_draft(
        self,
        draft_id: str,
        content: Dict[str, Any],
        context: RuntimeContext
    ) -> DraftResourceModel:
        self._require_capability(context, "creator:write")
        draft = await self.get_draft(draft_id, context)

        draft.content = content
        draft.validation_status = ValidationStatus.PENDING
        draft.validation_errors = []
        draft.updated_at = datetime.now(timezone.utc)

        updated = await self.repo.update(draft_id, draft)
        if not updated:
            raise AppException("Failed to update draft.", code="UPDATE_FAILED", status_code=500)

        await self.audit_service.log("creator.draft.update", f"draft:{draft_id}", "success", context, {})
        return updated

    async def duplicate_draft(self, draft_id: str, context: RuntimeContext) -> DraftResourceModel:
        self._require_capability(context, "creator:write")
        draft = await self.get_draft(draft_id, context)

        # Append suffix to title/name if it exists in content
        dup_content = dict(draft.content)
        for name_key in ["title", "name"]:
            if name_key in dup_content:
                dup_content[name_key] = f"{dup_content[name_key]} (Copy)"

        dup = DraftResourceModel(
            resource_type=draft.resource_type,
            content=dup_content,
            validation_status=ValidationStatus.PENDING,
            validation_errors=[],
            created_by=self._to_db_id(context.principal.id)
        )
        created = await self.repo.create(dup)
        await self.audit_service.log("creator.draft.duplicate", f"draft:{created.id}", "success", context, {})
        return created

    async def archive_draft(self, draft_id: str, context: RuntimeContext) -> bool:
        self._require_capability(context, "creator:write")
        deleted = await self.repo.delete(draft_id)
        if deleted:
            await self.audit_service.log("creator.draft.archive", f"draft:{draft_id}", "success", context, {})
        return deleted

    async def validate_draft(self, draft_id: str, context: RuntimeContext) -> DraftResourceModel:
        self._require_capability(context, "creator:read")
        draft = await self.get_draft(draft_id, context)

        errors = []
        c = draft.content

        # 1. Topic Validations
        if draft.resource_type == "topic":
            if not c.get("name"):
                errors.append("Required field 'name' is missing.")
            if not c.get("subject_id"):
                errors.append("Required field 'subject_id' is missing.")
            else:
                # Verify subject exists in published DB
                subject = await self.db["subjects"].find_one({"_id": c["subject_id"]})
                if not subject:
                    errors.append(f"Referenced subject '{c['subject_id']}' not found.")

        # 2. Content Validations
        elif draft.resource_type == "content":
            if not c.get("title"):
                errors.append("Required field 'title' is missing.")
            if not c.get("body"):
                errors.append("Required field 'body' is missing.")
            if not c.get("topic_id"):
                errors.append("Required field 'topic_id' is missing.")
            else:
                # Verify topic exists
                topic = await self.db["topics"].find_one({"_id": c["topic_id"]})
                if not topic:
                    errors.append(f"Referenced topic '{c['topic_id']}' not found.")

        # 3. Question Validations
        elif draft.resource_type == "question":
            if not c.get("title"):
                errors.append("Required field 'title' is missing.")
            if not c.get("statement"):
                errors.append("Required field 'statement' is missing.")
            if not c.get("question_type"):
                errors.append("Required field 'question_type' is missing.")
            if "evaluation_definition" not in c:
                errors.append("Required field 'evaluation_definition' is missing.")

        # 4. Assessment Validations
        elif draft.resource_type == "assessment":
            if not c.get("title"):
                errors.append("Required field 'title' is missing.")
            if not c.get("topic_id"):
                errors.append("Required field 'topic_id' is missing.")
            else:
                topic = await self.db["topics"].find_one({"_id": c["topic_id"]})
                if not topic:
                    errors.append(f"Referenced topic '{c['topic_id']}' not found.")

        draft.validation_errors = errors
        draft.validation_status = ValidationStatus.VALID if not errors else ValidationStatus.INVALID
        draft.updated_at = datetime.now(timezone.utc)

        await self.repo.update(draft_id, draft)
        return draft
