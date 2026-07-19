import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.runtime.context import RuntimeContext
from app.core.runtime.events.base import Event
from app.core.runtime.events.dispatcher import EventDispatcher
from app.core.runtime.audit.base import AuditService
from app.core.runtime.activity.base import ActivityService
from app.modules.learning.models.progress import ProgressModel, TopicProgress, LearningStatus
from app.modules.learning.models.learning_attempt import LearningAttemptModel
from app.modules.learning.schemas.progress import TopicProgressLog, SubjectProgressResponse, TopicProgressResponse
from app.modules.learning.repositories.progress import ProgressRepository
from app.core.errors import ForbiddenException, AppException

logger = logging.getLogger(__name__)

class ProgressService:
    def __init__(
        self,
        progress_repo: ProgressRepository,
        db: AsyncIOMotorDatabase,
        event_dispatcher: EventDispatcher,
        audit_service: AuditService,
        activity_service: ActivityService
    ):
        self.progress_repo = progress_repo
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

    async def get_or_create_progress(self, user_id: str, subject_id: str) -> ProgressModel:
        progress = await self.progress_repo.get_by_user_and_subject(user_id, subject_id)
        if not progress:
            progress = ProgressModel(
                user_id=user_id,
                subject_id=subject_id,
                completed_topics=[]
            )
            progress = await self.progress_repo.create(progress)
        return progress

    async def record_attempt_evidence(self, attempt: LearningAttemptModel, context: RuntimeContext) -> Optional[ProgressModel]:
        self._require_capability(context, "learning:write")
        user_id = str(attempt.user_id)

        # Resolve subject_id and topic_id from attempt resources
        subject_id, topic_id = await self._resolve_ids(attempt)
        if not subject_id or not topic_id:
            logger.warning(f"Could not resolve subject or topic for attempt resource: {attempt.resource_id}")
            return None

        progress = await self.get_or_create_progress(user_id, subject_id)

        existing = None
        for item in progress.completed_topics:
            if item.topic_id == topic_id:
                existing = item
                break

        attempt_duration = attempt.duration_seconds or 0
        attempt_score = attempt.score or 0.0

        if existing:
            # Increment attempt counts and update times
            existing.duration_seconds += attempt_duration
            existing.quiz_score = max(existing.quiz_score, attempt_score)
            existing.review_count += 1
            existing.last_attempt_at = attempt.end_time or datetime.now(timezone.utc)
            existing.last_attempt_id = str(attempt.id)

            # Generic status progression
            if existing.status == LearningStatus.NOT_STARTED or existing.status == LearningStatus.IN_PROGRESS:
                existing.status = LearningStatus.COMPLETED
            elif existing.status == LearningStatus.COMPLETED:
                existing.status = LearningStatus.REVIEWED

            # Mastery threshold checks
            if existing.review_count >= 3 or attempt_score >= 0.9:
                existing.status = LearningStatus.MASTERED

            # Confidence score updates
            existing.confidence_score = min(
                1.0,
                0.4 + (0.05 * existing.review_count) + (0.45 * (existing.quiz_score))
            )
        else:
            # First completion log
            new_status = LearningStatus.COMPLETED if attempt_score >= 0.5 else LearningStatus.IN_PROGRESS
            if attempt_score >= 0.9:
                new_status = LearningStatus.MASTERED

            confidence = min(1.0, 0.4 + 0.45 * attempt_score)

            new_completion = TopicProgress(
                topic_id=topic_id,
                status=new_status,
                completed_at=attempt.end_time or datetime.now(timezone.utc),
                duration_seconds=attempt_duration,
                quiz_score=attempt_score,
                confidence_score=confidence,
                review_count=1,
                last_attempt_at=attempt.end_time or datetime.now(timezone.utc),
                last_attempt_id=str(attempt.id)
            )
            progress.completed_topics.append(new_completion)

        progress.last_active_at = datetime.now(timezone.utc)
        progress.updated_at = datetime.now(timezone.utc)

        updated = await self.progress_repo.update(progress.id, progress)

        # Trigger events
        await self.event_dispatcher.dispatch(Event(
            name="LearningProgressUpdated",
            payload={"user_id": user_id, "subject_id": subject_id, "topic_id": topic_id},
            context=context
        ))
        await self.audit_service.log("learning.progress.update", f"progress:{progress.id}", "success", context, metadata={})

        return updated

    async def get_subject_progress_response(self, user_id: str, subject_id: str, context: RuntimeContext) -> Optional[SubjectProgressResponse]:
        self._require_capability(context, "learning:read")

        # Verify subject exists
        subject_doc = await self.db["subjects"].find_one({"_id": subject_id})
        if not subject_doc:
            return None

        progress = await self.get_or_create_progress(user_id, subject_id)

        # Calculate total count of topics in subject syllabus
        syllabus_cursor = self.db["syllabuses"].find({"subject_id": subject_id, "status": "active"})
        syllabuses = await syllabus_cursor.to_list(length=50)
        
        total_topics = 0
        for syl in syllabuses:
            module_cursor = self.db["modules"].find({"syllabus_id": syl["_id"], "status": "active"})
            modules = await module_cursor.to_list(length=100)
            for mod in modules:
                topic_count = await self.db["topics"].count_documents({"module_id": mod["_id"], "status": "active"})
                total_topics += topic_count

        completion_pct = 0.0
        completed_count = sum(1 for t in progress.completed_topics if t.status in [LearningStatus.COMPLETED, LearningStatus.REVIEWED, LearningStatus.MASTERED])
        if total_topics > 0:
            completion_pct = (completed_count / total_topics) * 100.0

        completed_resp = [
            TopicProgressResponse(
                topic_id=item.topic_id,
                completed_at=item.completed_at,
                duration_seconds=item.duration_seconds,
                quiz_score=item.quiz_score
            )
            for item in progress.completed_topics
        ]

        return SubjectProgressResponse(
            subject_id=subject_id,
            completion_percentage=round(completion_pct, 2),
            completed_topics=completed_resp,
            last_active_at=progress.last_active_at
        )

    async def _resolve_ids(self, attempt: LearningAttemptModel):
        try:
            topic_id = None
            if attempt.resource_type == "topic":
                topic_id = attempt.resource_id
            else:
                # Try finding in knowledge_contents
                content_doc = await self.db["knowledge_contents"].find_one({"_id": attempt.resource_id})
                if content_doc:
                    topic_id = content_doc.get("topic_id")
                else:
                    # Fallback to direct topic lookup
                    topic_doc = await self.db["topics"].find_one({"_id": attempt.resource_id})
                    if topic_doc:
                        topic_id = attempt.resource_id

            if not topic_id:
                return None, None

            topic_doc = await self.db["topics"].find_one({"_id": topic_id})
            if not topic_doc:
                return None, None
            module_id = topic_doc.get("module_id")

            module_doc = await self.db["modules"].find_one({"_id": module_id})
            if not module_doc:
                return None, None
            syllabus_id = module_doc.get("syllabus_id")

            syllabus_doc = await self.db["syllabuses"].find_one({"_id": syllabus_id})
            if not syllabus_doc:
                return None, None
            subject_id = syllabus_doc.get("subject_id")

            return subject_id, topic_id
        except Exception:
            return None, None
