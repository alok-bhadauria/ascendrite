from datetime import datetime, timezone
from typing import Optional, Any, Dict
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.learning.models.learning_session import LearningSessionModel, SessionStatus
from app.modules.learning.repositories.base import LearningSessionRepository

class LearningSessionService:
    def __init__(
        self,
        repo: LearningSessionRepository,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.repo = repo
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

    async def start_session(self, context: RuntimeContext, metadata: Optional[Dict[str, Any]] = None) -> LearningSessionModel:
        self._require_capability(context, "learning:write")
        user_id = context.principal.id

        # Deactivate any existing active session first
        active = await self.repo.get_active_session_by_user(user_id)
        if active:
            active.status = SessionStatus.CLOSED
            active.end_time = datetime.now(timezone.utc)
            await self.repo.update(active.id, active)
            await self.event_dispatcher.dispatch(Event(name="LearningSessionClosed", payload={"session_id": str(active.id)}, context=context))
            await self.audit_service.log("learning.session.close", f"session:{active.id}", "success", context, metadata={})

        session = LearningSessionModel(
            user_id=user_id,
            status=SessionStatus.ACTIVE,
            start_time=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        created = await self.repo.create(session)

        # Triggers side effects
        await self.event_dispatcher.dispatch(Event(name="LearningSessionStarted", payload={"session_id": str(created.id)}, context=context))
        await self.audit_service.log("learning.session.start", f"session:{created.id}", "success", context, metadata={})
        await self.activity_service.log("session_start", f"Started Learning Session", "", context, metadata={})
        return created

    async def get_active_session(self, context: RuntimeContext) -> Optional[LearningSessionModel]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        return await self.repo.get_active_session_by_user(user_id)

    async def close_session(self, session_id: str, context: RuntimeContext) -> LearningSessionModel:
        self._require_capability(context, "learning:write")
        session = await self.repo.get_by_id(session_id)
        if not session:
            raise AppException(f"Learning Session '{session_id}' not found.", code="NOT_FOUND", status_code=404)

        # Security check: verify owner
        if str(session.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this learning session.")

        if session.status == SessionStatus.CLOSED:
            return session

        session.status = SessionStatus.CLOSED
        session.end_time = datetime.now(timezone.utc)
        updated = await self.repo.update(session_id, session)

        # Side effects
        await self.event_dispatcher.dispatch(Event(name="LearningSessionClosed", payload={"session_id": session_id}, context=context))
        await self.audit_service.log("learning.session.close", f"session:{session_id}", "success", context, metadata={})
        await self.activity_service.log("session_close", f"Closed Learning Session", "", context, metadata={})
        return updated
