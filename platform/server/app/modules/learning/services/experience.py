from datetime import datetime, timezone
from typing import Optional, Any, Dict, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.learning.models.experience import LearningExperienceModel, ExperienceStatus
from app.modules.learning.repositories.base import LearningExperienceRepository
from app.modules.learning.services.session import LearningSessionService
from app.modules.learning.services.attempt import LearningAttemptService

class LearningExperienceService:
    def __init__(
        self,
        repo: LearningExperienceRepository,
        db: AsyncIOMotorDatabase,
        session_service: LearningSessionService,
        attempt_service: LearningAttemptService,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.repo = repo
        self.db = db
        self.session_service = session_service
        self.attempt_service = attempt_service
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

    async def _verify_resource_exists(self, resource_id: str, experience_type: str) -> None:
        # Cross-domain check to verify the Knowledge resource exists
        try:
            if experience_type in ["notes", "revision", "interview"]:
                doc = await self.db["knowledge_contents"].find_one({"_id": resource_id})
                if not doc:
                    raise AppException(f"Educational content resource '{resource_id}' not found.", code="NOT_FOUND", status_code=404)
            elif experience_type == "topic":
                doc = await self.db["topics"].find_one({"_id": resource_id})
                if not doc:
                    raise AppException(f"Topic resource '{resource_id}' not found.", code="NOT_FOUND", status_code=404)
        except AppException:
            raise
        except Exception as e:
            # Open-ended generic fallback if resource type is custom (e.g. Flashcards, Lab)
            pass

    async def start_experience(
        self,
        context: RuntimeContext,
        resource_id: str,
        experience_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> LearningExperienceModel:
        self._require_capability(context, "learning:write")
        user_id = context.principal.id

        # Verify target resource exists in Knowledge Domain
        await self._verify_resource_exists(resource_id, experience_type)

        # Deactivate any active experience of the same type first
        active_exp = await self.repo.get_active_experience_by_user(user_id, experience_type)
        if active_exp:
            await self.abandon_experience(context, str(active_exp.id))

        # Check if there is an active session to participate in
        active_sess = await self.session_service.get_active_session(context)
        session_id = active_sess.id if active_sess else None

        experience = LearningExperienceModel(
            user_id=user_id,
            session_id=session_id,
            resource_id=resource_id,
            experience_type=experience_type,
            status=ExperienceStatus.ACTIVE,
            state={"current_step": 0},
            start_time=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        created = await self.repo.create(experience)

        await self.event_dispatcher.dispatch(Event(
            name="LearningExperienceStarted",
            payload={"experience_id": str(created.id), "experience_type": experience_type},
            context=context
        ))
        await self.audit_service.log("learning.experience.start", f"experience:{created.id}", "success", context, metadata={})
        return created

    async def get_active_experiences(self, context: RuntimeContext) -> List[LearningExperienceModel]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        
        # Pull all active experiences of any type for the user
        db_user_id = ObjectId(user_id) if isinstance(user_id, str) and ObjectId.is_valid(user_id) else user_id
        cursor = self.db["learning_experiences"].find({
            "user_id": db_user_id,
            "status": ExperienceStatus.ACTIVE.value
        })
        docs = await cursor.to_list(length=50)
        return [LearningExperienceModel(**doc) for doc in docs]

    async def get_experience(self, experience_id: str, context: RuntimeContext) -> LearningExperienceModel:
        self._require_capability(context, "learning:read")
        exp = await self.repo.get_by_id(experience_id)
        if not exp:
            raise AppException(f"Learning Experience '{experience_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(exp.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this experience.")
        return exp

    async def submit_experience_step(
        self,
        context: RuntimeContext,
        experience_id: str,
        step_data: Dict[str, Any]
    ) -> LearningExperienceModel:
        self._require_capability(context, "learning:write")
        exp = await self.get_experience(experience_id, context)

        if exp.status != ExperienceStatus.ACTIVE:
            raise AppException("Cannot submit step for a closed experience.", code="INVALID_STATE", status_code=400)

        # Merge step progress parameters into state object (keeping it lightweight)
        exp.state.update(step_data)
        exp.updated_at = datetime.now(timezone.utc)

        updated = await self.repo.update(experience_id, exp)
        
        await self.event_dispatcher.dispatch(Event(
            name="LearningExperienceStepSubmitted",
            payload={"experience_id": experience_id, "step_data": step_data},
            context=context
        ))
        return updated

    async def complete_experience(
        self,
        context: RuntimeContext,
        experience_id: str,
        score: Optional[float] = None,
        response_data: Optional[Dict[str, Any]] = None
    ) -> LearningExperienceModel:
        self._require_capability(context, "learning:write")
        exp = await self.get_experience(experience_id, context)

        if exp.status != ExperienceStatus.ACTIVE:
            return exp

        exp.status = ExperienceStatus.COMPLETED
        exp.end_time = datetime.now(timezone.utc)
        if response_data:
            exp.state.update({"response_data": response_data})

        updated = await self.repo.update(experience_id, exp)

        # 1. Trigger Logging Attempt (Stage 4.1 Abstraction)
        attempt = await self.attempt_service.start_attempt(
            session_id=str(exp.session_id) if exp.session_id else None,
            resource_id=exp.resource_id,
            resource_type=exp.experience_type,
            context=context,
            metadata={"experience_id": experience_id}
        )
        
        # Advance attempt to completed state which triggers progress updating
        await self.attempt_service.complete_attempt(
            attempt_id=str(attempt.id),
            score=score,
            response_data=response_data,
            context=context
        )

        # 2. Side effects
        await self.event_dispatcher.dispatch(Event(
            name="LearningExperienceCompleted",
            payload={"experience_id": experience_id, "resource_id": exp.resource_id, "score": score},
            context=context
        ))
        await self.audit_service.log("learning.experience.complete", f"experience:{experience_id}", "success", context, metadata={})
        await self.activity_service.log("experience_complete", f"Completed {exp.experience_type} experience", f"Resource: {exp.resource_id}", context, metadata={})

        return updated

    async def abandon_experience(self, context: RuntimeContext, experience_id: str) -> LearningExperienceModel:
        self._require_capability(context, "learning:write")
        exp = await self.get_experience(experience_id, context)

        if exp.status != ExperienceStatus.ACTIVE:
            return exp

        exp.status = ExperienceStatus.ABANDONED
        exp.end_time = datetime.now(timezone.utc)

        updated = await self.repo.update(experience_id, exp)

        # Log an abandoned attempt to preserve learner history logs
        attempt = await self.attempt_service.start_attempt(
            session_id=str(exp.session_id) if exp.session_id else None,
            resource_id=exp.resource_id,
            resource_type=exp.experience_type,
            context=context,
            metadata={"experience_id": experience_id}
        )
        await self.attempt_service.abandon_attempt(
            attempt_id=str(attempt.id),
            context=context
        )

        # Side effects
        await self.event_dispatcher.dispatch(Event(
            name="LearningExperienceAbandoned",
            payload={"experience_id": experience_id, "resource_id": exp.resource_id},
            context=context
        ))
        await self.audit_service.log("learning.experience.abandon", f"experience:{experience_id}", "success", context, metadata={})

        return updated
