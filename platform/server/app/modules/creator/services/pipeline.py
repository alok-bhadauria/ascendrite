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
from app.modules.creator.models.workflow import PublishingWorkflowModel, WorkflowStatus
from app.modules.creator.models.draft import ValidationStatus
from app.modules.creator.repositories.workflow import PublishingWorkflowRepository
from app.modules.creator.services.workspace import ContentWorkspaceService

# Domain services imports
from app.modules.knowledge.services.base import KnowledgeContentService
from app.modules.knowledge.models.content import KnowledgeContentModel
from app.modules.assessments.services.content import AssessmentContentService
from app.modules.assessments.models.question import QuestionModel
from app.modules.assessments.models.assessment import AssessmentModel

logger = logging.getLogger(__name__)

class PublishingPipelineService:
    def __init__(
        self,
        repo: PublishingWorkflowRepository,
        workspace_service: ContentWorkspaceService,
        knowledge_content_service: KnowledgeContentService,
        assessment_content_service: AssessmentContentService,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService
    ):
        self.repo = repo
        self.workspace_service = workspace_service
        self.knowledge_content_service = knowledge_content_service
        self.assessment_content_service = assessment_content_service
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

    async def _get_or_create_workflow(self, draft_id: str, context: RuntimeContext) -> PublishingWorkflowModel:
        db_draft_id = self._to_db_id(draft_id)
        wf = await self.repo.get_by_draft(db_draft_id)
        if not wf:
            wf = PublishingWorkflowModel(
                draft_id=db_draft_id,
                status=WorkflowStatus.DRAFT,
                history=[]
            )
            wf = await self.repo.create(wf)
        return wf

    async def get_workflow_by_draft(self, draft_id: str, context: RuntimeContext) -> PublishingWorkflowModel:
        self._require_capability(context, "creator:read")
        return await self._get_or_create_workflow(draft_id, context)

    async def submit_for_review(self, draft_id: str, notes: str, context: RuntimeContext) -> PublishingWorkflowModel:
        self._require_capability(context, "creator:write")
        
        # 1. Validate the draft structure
        draft = await self.workspace_service.validate_draft(draft_id, context)
        if draft.validation_status != ValidationStatus.VALID:
            raise AppException(f"Cannot submit draft for review. Structural validation failed: {draft.validation_errors}", code="VALIDATION_FAILED", status_code=400)

        wf = await self._get_or_create_workflow(draft_id, context)
        if wf.status not in [WorkflowStatus.DRAFT, WorkflowStatus.READY_FOR_REVIEW]:
            raise AppException(f"Invalid workflow status transition from '{wf.status}' to 'ready_for_review'.", code="INVALID_TRANSITION", status_code=400)

        old_status = wf.status
        wf.status = WorkflowStatus.READY_FOR_REVIEW
        wf.notes = notes
        wf.history.append({
            "from_status": old_status.value,
            "to_status": WorkflowStatus.READY_FOR_REVIEW.value,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "changed_by": str(context.principal.id),
            "notes": notes
        })
        wf.updated_at = datetime.now(timezone.utc)

        await self.repo.update(str(wf.id), wf)
        await self.audit_service.log("creator.publish.submit", f"draft:{draft_id}", "success", context, {})
        return wf

    async def approve_draft(self, draft_id: str, notes: str, context: RuntimeContext) -> PublishingWorkflowModel:
        self._require_capability(context, "creator:write")
        
        wf = await self._get_or_create_workflow(draft_id, context)
        if wf.status != WorkflowStatus.READY_FOR_REVIEW:
            raise AppException(f"Cannot approve draft unless it is ready for review. Current status: '{wf.status}'.", code="INVALID_STATE", status_code=400)

        old_status = wf.status
        wf.status = WorkflowStatus.APPROVED
        wf.reviewer_id = str(context.principal.id)
        wf.notes = notes
        wf.history.append({
            "from_status": old_status.value,
            "to_status": WorkflowStatus.APPROVED.value,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "changed_by": str(context.principal.id),
            "notes": notes
        })
        wf.updated_at = datetime.now(timezone.utc)

        await self.repo.update(str(wf.id), wf)
        await self.audit_service.log("creator.publish.approve", f"draft:{draft_id}", "success", context, {})
        return wf

    async def reject_draft(self, draft_id: str, notes: str, context: RuntimeContext) -> PublishingWorkflowModel:
        self._require_capability(context, "creator:write")
        
        wf = await self._get_or_create_workflow(draft_id, context)
        if wf.status != WorkflowStatus.READY_FOR_REVIEW:
            raise AppException(f"Cannot reject draft unless it is ready for review.", code="INVALID_STATE", status_code=400)

        old_status = wf.status
        wf.status = WorkflowStatus.DRAFT  # Return to draft
        wf.notes = notes
        wf.history.append({
            "from_status": old_status.value,
            "to_status": WorkflowStatus.DRAFT.value,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "changed_by": str(context.principal.id),
            "notes": notes
        })
        wf.updated_at = datetime.now(timezone.utc)

        await self.repo.update(str(wf.id), wf)
        await self.audit_service.log("creator.publish.reject", f"draft:{draft_id}", "success", context, {})
        return wf

    async def publish_draft(self, draft_id: str, context: RuntimeContext) -> PublishingWorkflowModel:
        self._require_capability(context, "creator:write")
        
        wf = await self._get_or_create_workflow(draft_id, context)
        if wf.status != WorkflowStatus.APPROVED:
            raise AppException(f"Cannot publish draft unless it is approved. Current status: '{wf.status}'.", code="INVALID_STATE", status_code=400)

        draft = await self.workspace_service.get_draft(draft_id, context)

        # Coordinate domain-specific publication
        published_id = None
        c = draft.content

        # 1. Publish Knowledge Content
        if draft.resource_type == "content":
            if draft.resource_id:
                # Update existing
                await self.knowledge_content_service.update_content(draft.resource_id, c, context)
                published_id = draft.resource_id
            else:
                # Create new
                content_model = KnowledgeContentModel(**c)
                created = await self.knowledge_content_service.create_content(content_model, context)
                published_id = str(created.id)

        # 2. Publish Assessment Question
        elif draft.resource_type == "question":
            if draft.resource_id:
                await self.assessment_content_service.update_question(draft.resource_id, c, context)
                published_id = draft.resource_id
            else:
                question_model = QuestionModel(**c)
                created = await self.assessment_content_service.create_question(question_model, context)
                published_id = str(created.id)

        # 3. Publish Assessment Definition
        elif draft.resource_type == "assessment":
            if draft.resource_id:
                await self.assessment_content_service.update_assessment(draft.resource_id, c, context)
                published_id = draft.resource_id
            else:
                assessment_model = AssessmentModel(**c)
                created = await self.assessment_content_service.create_assessment(assessment_model, context)
                published_id = str(created.id)

        # 4. Publish Topic
        elif draft.resource_type == "topic":
            if draft.resource_id:
                await self.db["topics"].update_one({"_id": draft.resource_id}, {"$set": c})
                published_id = draft.resource_id
            else:
                # Generate unique ID for topic
                topic_id = c.get("_id") or c.get("id") or f"topic-{ObjectId()}"
                c["_id"] = topic_id
                c["is_active"] = c.get("is_active", True)
                await self.db["topics"].insert_one(c)
                published_id = topic_id

        # Update draft reference
        draft.resource_id = published_id
        await self.workspace_service.repo.update(draft_id, draft)

        # Transition workflow to published
        old_status = wf.status
        wf.status = WorkflowStatus.PUBLISHED
        wf.history.append({
            "from_status": old_status.value,
            "to_status": WorkflowStatus.PUBLISHED.value,
            "changed_at": datetime.now(timezone.utc).isoformat(),
            "changed_by": str(context.principal.id),
            "notes": f"Resource successfully published with ID: {published_id}"
        })
        wf.updated_at = datetime.now(timezone.utc)

        await self.repo.update(str(wf.id), wf)

        await self.event_dispatcher.dispatch(Event(
            name="ResourcePublished",
            payload={"draft_id": draft_id, "resource_id": published_id, "resource_type": draft.resource_type},
            context=context
        ))
        await self.audit_service.log("creator.publish.execute", f"draft:{draft_id}", "success", context, {"resource_id": published_id})
        return wf
