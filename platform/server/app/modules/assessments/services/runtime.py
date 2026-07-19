import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.modules.assessments.models.runtime import AssessmentSessionModel, AssessmentResponseItem, SessionStatus
from app.modules.assessments.repositories.runtime import AssessmentSessionRepository
from app.modules.assessments.services.content import AssessmentContentService

logger = logging.getLogger(__name__)

class AssessmentRuntimeService:
    def __init__(
        self,
        repo: AssessmentSessionRepository,
        content_service: AssessmentContentService,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        evaluation_service: Optional[Any] = None
    ):
        self.repo = repo
        self.content_service = content_service
        self.db = db
        self.event_dispatcher = event_dispatcher
        self.audit_service = audit_service
        self._evaluation_service = evaluation_service

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

    def set_evaluation_service(self, evaluation_service: Any) -> None:
        self._evaluation_service = evaluation_service

    async def start_session(
        self,
        assessment_id: str,
        context: RuntimeContext
    ) -> AssessmentSessionModel:
        self._require_capability(context, "assessment:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # 1. Retrieve Assessment and check it exists
        assessment = await self.content_service.get_assessment(assessment_id, context)

        # 2. Check for active session (Resume pattern)
        active = await self.repo.get_active_session_by_user(db_user_id, assessment_id)
        if active:
            # Enforce time limit verification on resume as well
            if assessment.duration_minutes:
                start_time = active.start_time.replace(tzinfo=timezone.utc) if active.start_time.tzinfo is None else active.start_time
                limit_time = start_time + timedelta(minutes=assessment.duration_minutes)
                if datetime.now(timezone.utc) > limit_time:
                    # Automatically close active session as completed (timeout)
                    return await self.submit_session(str(active.id), context)
            return active

        # 3. Create new session
        session = AssessmentSessionModel(
            user_id=db_user_id,
            assessment_id=assessment_id,
            status=SessionStatus.ACTIVE,
            responses=[],
            start_time=datetime.now(timezone.utc)
        )
        created = await self.repo.create(session)

        await self.event_dispatcher.dispatch(Event(
            name="AssessmentSessionStarted",
            payload={"session_id": str(created.id), "assessment_id": assessment_id},
            context=context
        ))
        await self.audit_service.log("assessment.session.start", f"session:{created.id}", "success", context, {})
        return created

    async def get_session(self, session_id: str, context: RuntimeContext) -> AssessmentSessionModel:
        self._require_capability(context, "assessment:read")
        session = await self.repo.get_by_id(session_id)
        if not session:
            raise AppException(f"Assessment session '{session_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(session.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this assessment session.")
        return session

    async def submit_answer(
        self,
        session_id: str,
        response_item: AssessmentResponseItem,
        context: RuntimeContext
    ) -> AssessmentSessionModel:
        self._require_capability(context, "assessment:read")
        session = await self.get_session(session_id, context)

        if session.status != SessionStatus.ACTIVE:
            raise AppException("Cannot submit answer to a closed session.", code="INVALID_STATE", status_code=400)

        # 1. Verify timing limits
        assessment = await self.content_service.get_assessment(session.assessment_id, context)
        if assessment.duration_minutes:
            start_time = session.start_time.replace(tzinfo=timezone.utc) if session.start_time.tzinfo is None else session.start_time
            limit_time = start_time + timedelta(minutes=assessment.duration_minutes)
            if datetime.now(timezone.utc) > limit_time:
                # Close assessment due to timeout automatically
                return await self.submit_session(session_id, context)

        # 2. Verify question exists in the assessment questions list
        question_ids = [q.question_id for q in assessment.questions]
        if response_item.question_id not in question_ids:
            raise AppException(f"Question '{response_item.question_id}' not part of assessment '{session.assessment_id}'.", code="INVALID_QUESTION", status_code=400)

        # 3. Add or update response
        response_item.submitted_at = datetime.now(timezone.utc)
        
        # Remove previous response for this question if it exists
        session.responses = [r for r in session.responses if r.question_id != response_item.question_id]
        session.responses.append(response_item)
        session.updated_at = datetime.now(timezone.utc)

        updated = await self.repo.update(session_id, session)
        if not updated:
            raise AppException("Failed to update session answer.", code="UPDATE_FAILED", status_code=500)
        return updated

    async def cancel_session(self, session_id: str, context: RuntimeContext) -> AssessmentSessionModel:
        self._require_capability(context, "assessment:read")
        session = await self.get_session(session_id, context)

        if session.status != SessionStatus.ACTIVE:
            return session

        session.status = SessionStatus.CANCELLED
        session.end_time = datetime.now(timezone.utc)
        session.updated_at = datetime.now(timezone.utc)

        updated = await self.repo.update(session_id, session)
        if not updated:
            raise AppException("Failed to cancel session.", code="UPDATE_FAILED", status_code=500)

        await self.event_dispatcher.dispatch(Event(
            name="AssessmentSessionCancelled",
            payload={"session_id": session_id},
            context=context
        ))
        await self.audit_service.log("assessment.session.cancel", f"session:{session_id}", "success", context, {})
        return updated

    async def submit_session(self, session_id: str, context: RuntimeContext) -> AssessmentSessionModel:
        self._require_capability(context, "assessment:read")
        session = await self.get_session(session_id, context)

        if session.status != SessionStatus.ACTIVE:
            return session

        session.status = SessionStatus.COMPLETED
        session.end_time = datetime.now(timezone.utc)
        session.updated_at = datetime.now(timezone.utc)

        updated = await self.repo.update(session_id, session)
        if not updated:
            raise AppException("Failed to complete session.", code="UPDATE_FAILED", status_code=500)

        await self.event_dispatcher.dispatch(Event(
            name="AssessmentSessionCompleted",
            payload={"session_id": session_id},
            context=context
        ))
        await self.audit_service.log("assessment.session.complete", f"session:{session_id}", "success", context, {})

        # 4. Trigger evaluation if service is available
        if self._evaluation_service:
            # We run it synchronously or trigger grading workflow asynchronously (here sync is perfect)
            await self._evaluation_service.evaluate_session(session_id, context)

        return updated
