from datetime import datetime, timezone
from typing import Optional, Any, Dict
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.learning.models.learning_attempt import LearningAttemptModel, AttemptStatus
from app.modules.learning.repositories.base import LearningAttemptRepository
from app.modules.learning.services.progress import ProgressService

def _calculate_duration(start: datetime, end: datetime) -> int:
    def _to_aware(dt: datetime) -> datetime:
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    return max(0, int((_to_aware(end) - _to_aware(start)).total_seconds()))

class LearningAttemptService:
    def __init__(
        self,
        repo: LearningAttemptRepository,
        progress_service: ProgressService,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.repo = repo
        self.progress_service = progress_service
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

    async def start_attempt(
        self,
        session_id: Optional[str],
        resource_id: str,
        resource_type: str,
        context: RuntimeContext,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LearningAttemptModel:
        self._require_capability(context, "learning:write")
        user_id = context.principal.id

        attempt = LearningAttemptModel(
            user_id=user_id,
            session_id=session_id,
            resource_id=resource_id,
            resource_type=resource_type,
            status=AttemptStatus.IN_PROGRESS,
            start_time=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        created = await self.repo.create(attempt)

        await self.event_dispatcher.dispatch(Event(name="LearningAttemptStarted", payload={"attempt_id": str(created.id)}, context=context))
        await self.audit_service.log("learning.attempt.start", f"attempt:{created.id}", "success", context, metadata={})
        return created

    async def get_attempt(self, attempt_id: str, context: RuntimeContext) -> LearningAttemptModel:
        self._require_capability(context, "learning:read")
        attempt = await self.repo.get_by_id(attempt_id)
        if not attempt:
            raise AppException(f"Learning Attempt '{attempt_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(attempt.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this attempt.")
        return attempt

    async def complete_attempt(
        self,
        attempt_id: str,
        score: Optional[float],
        response_data: Optional[Dict[str, Any]],
        context: RuntimeContext,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LearningAttemptModel:
        self._require_capability(context, "learning:write")
        attempt = await self.get_attempt(attempt_id, context)

        if attempt.status != AttemptStatus.IN_PROGRESS:
            return attempt

        attempt.status = AttemptStatus.COMPLETED
        attempt.end_time = datetime.now(timezone.utc)
        attempt.duration_seconds = _calculate_duration(attempt.start_time, attempt.end_time)
        attempt.score = score
        attempt.response_data = response_data
        if metadata:
            attempt.metadata.update(metadata)

        updated = await self.repo.update(attempt_id, attempt)

        # Emit Completed Event
        await self.event_dispatcher.dispatch(Event(
            name="LearningAttemptCompleted",
            payload={"attempt_id": attempt_id, "resource_id": attempt.resource_id, "resource_type": attempt.resource_type},
            context=context
        ))
        await self.audit_service.log("learning.attempt.complete", f"attempt:{attempt_id}", "success", context, metadata={})
        await self.activity_service.log("attempt_complete", f"Completed attempt on {attempt.resource_type}", f"Resource: {attempt.resource_id}", context, metadata={})

        # Record Evidence in Progress
        await self.progress_service.record_attempt_evidence(updated, context)

        return updated

    async def abandon_attempt(self, attempt_id: str, context: RuntimeContext) -> LearningAttemptModel:
        self._require_capability(context, "learning:write")
        attempt = await self.get_attempt(attempt_id, context)

        if attempt.status != AttemptStatus.IN_PROGRESS:
            return attempt

        attempt.status = AttemptStatus.ABANDONED
        attempt.end_time = datetime.now(timezone.utc)
        attempt.duration_seconds = _calculate_duration(attempt.start_time, attempt.end_time)

        updated = await self.repo.update(attempt_id, attempt)

        await self.event_dispatcher.dispatch(Event(name="LearningAttemptAbandoned", payload={"attempt_id": attempt_id}, context=context))
        await self.audit_service.log("learning.attempt.abandon", f"attempt:{attempt_id}", "success", context, metadata={})
        return updated
