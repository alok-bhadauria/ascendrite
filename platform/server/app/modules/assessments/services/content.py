import logging
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.assessments.models.question import QuestionModel
from app.modules.assessments.models.assessment import AssessmentModel
from app.modules.assessments.repositories.question import QuestionRepository
from app.modules.assessments.repositories.assessment import AssessmentRepository

logger = logging.getLogger(__name__)

class AssessmentContentService:
    def __init__(
        self,
        question_repo: QuestionRepository,
        assessment_repo: AssessmentRepository,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.question_repo = question_repo
        self.assessment_repo = assessment_repo
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self.activity_service = activity_service

    def _require_capability(self, context: RuntimeContext, capability: str) -> None:
        if not context.principal:
            raise ForbiddenException("Anonymous access is denied.")
        if context.principal.role == "Admin":
            return
        if capability not in context.principal.capabilities:
            raise ForbiddenException(f"Principal context is missing required capability: '{capability}'.")

    async def _verify_topic_exists(self, topic_id: str) -> None:
        topic_doc = await self.db["topics"].find_one({"_id": topic_id})
        if not topic_doc:
            raise AppException(f"Referenced topic '{topic_id}' not found.", code="NOT_FOUND", status_code=404)

    # --- Question Bank Operations ---

    async def create_question(self, question: QuestionModel, context: RuntimeContext) -> QuestionModel:
        self._require_capability(context, "assessment:write")
        
        # Verify topic if provided in metadata
        topic_id = question.metadata.get("topic_id")
        if topic_id:
            await self._verify_topic_exists(topic_id)

        created = await self.question_repo.create(question)
        
        await self.event_dispatcher.dispatch(Event(
            name="QuestionCreated",
            payload={"question_id": str(created.id)},
            context=context
        ))
        await self.audit_service.log("assessment.question.create", f"question:{created.id}", "success", context, {})
        return created

    async def get_question(self, question_id: str, context: RuntimeContext) -> QuestionModel:
        self._require_capability(context, "assessment:read")
        question = await self.question_repo.get_by_id(question_id)
        if not question:
            raise AppException(f"Question '{question_id}' not found.", code="NOT_FOUND", status_code=404)
        return question

    async def update_question(self, question_id: str, update_data: dict, context: RuntimeContext) -> QuestionModel:
        self._require_capability(context, "assessment:write")
        question = await self.get_question(question_id, context)

        # Merge updates
        for key, val in update_data.items():
            if val is not None:
                setattr(question, key, val)

        if "metadata" in update_data and update_data["metadata"]:
            topic_id = update_data["metadata"].get("topic_id")
            if topic_id:
                await self._verify_topic_exists(topic_id)

        updated = await self.question_repo.update(question_id, question)
        if not updated:
            raise AppException(f"Failed to update question '{question_id}'.", code="UPDATE_FAILED", status_code=500)

        await self.audit_service.log("assessment.question.update", f"question:{question_id}", "success", context, {})
        return updated

    # --- Assessment Definition Operations ---

    async def create_assessment(self, assessment: AssessmentModel, context: RuntimeContext) -> AssessmentModel:
        self._require_capability(context, "assessment:write")
        
        # Verify parent topic exists
        await self._verify_topic_exists(assessment.topic_id)

        # Verify referenced questions exist in DB
        for ref in assessment.questions:
            q = await self.question_repo.get_by_id(ref.question_id)
            if not q:
                raise AppException(f"Referenced question '{ref.question_id}' does not exist.", code="INVALID_QUESTION_REFERENCE", status_code=400)

        created = await self.assessment_repo.create(assessment)

        await self.event_dispatcher.dispatch(Event(
            name="AssessmentCreated",
            payload={"assessment_id": str(created.id), "title": created.title},
            context=context
        ))
        await self.audit_service.log("assessment.definition.create", f"assessment:{created.id}", "success", context, {})
        return created

    async def get_assessment(self, assessment_id: str, context: RuntimeContext) -> AssessmentModel:
        self._require_capability(context, "assessment:read")
        assessment = await self.assessment_repo.get_by_id(assessment_id)
        if not assessment:
            raise AppException(f"Assessment '{assessment_id}' not found.", code="NOT_FOUND", status_code=404)
        return assessment

    async def update_assessment(self, assessment_id: str, update_data: dict, context: RuntimeContext) -> AssessmentModel:
        self._require_capability(context, "assessment:write")
        assessment = await self.get_assessment(assessment_id, context)

        # Merge updates
        for key, val in update_data.items():
            if val is not None:
                setattr(assessment, key, val)

        if "topic_id" in update_data and update_data["topic_id"]:
            await self._verify_topic_exists(update_data["topic_id"])

        if "questions" in update_data and update_data["questions"]:
            for ref in assessment.questions:
                q = await self.question_repo.get_by_id(ref.question_id)
                if not q:
                    raise AppException(f"Referenced question '{ref.question_id}' does not exist.", code="INVALID_QUESTION_REFERENCE", status_code=400)

        updated = await self.assessment_repo.update(assessment_id, assessment)
        if not updated:
            raise AppException(f"Failed to update assessment '{assessment_id}'.", code="UPDATE_FAILED", status_code=500)

        await self.audit_service.log("assessment.definition.update", f"assessment:{assessment_id}", "success", context, {})
        return updated
