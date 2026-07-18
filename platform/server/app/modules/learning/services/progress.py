import logging
from datetime import datetime, timezone
from typing import Optional
from app.modules.learning.models.progress import ProgressModel, TopicProgress
from app.modules.learning.schemas.progress import TopicProgressLog, SubjectProgressResponse, TopicProgressResponse
from app.modules.learning.repositories.progress import ProgressRepository
from app.modules.knowledge.services.curriculum import curriculum_service

logger = logging.getLogger(__name__)

class ProgressService:
    def __init__(self, progress_repo: ProgressRepository):
        self.progress_repo = progress_repo

    async def get_or_create_progress(self, user_id: str, subject_id: str) -> ProgressModel:
        """Retrieve existing progress tracking model or initialize a new document"""
        progress = await self.progress_repo.get_by_user_and_subject(user_id, subject_id)
        if not progress:
            progress = ProgressModel(
                user_id=user_id,
                subject_id=subject_id,
                completed_topics=[]
            )
            progress = await self.progress_repo.create(progress)
        return progress

    async def log_topic_progress(
        self, user_id: str, subject_id: str, log_data: TopicProgressLog
    ) -> Optional[ProgressModel]:
        """Record completed topic progress, updating aggregate scores and durations"""
        subject = curriculum_service.get_subject(subject_id)
        if not subject:
            logger.warning(f"Failed to log progress: Subject '{subject_id}' not found.")
            return None

        progress = await self.get_or_create_progress(user_id, subject_id)
        
        # Check if topic already logged
        existing = None
        for item in progress.completed_topics:
            if item.topic_id == log_data.topic_id:
                existing = item
                break

        if existing:
            # Update values incrementally
            existing.duration_seconds += log_data.duration_seconds
            existing.quiz_score = max(existing.quiz_score, log_data.quiz_score)
            existing.completed_at = datetime.now(timezone.utc)
        else:
            # Log new completion
            new_completion = TopicProgress(
                topic_id=log_data.topic_id,
                duration_seconds=log_data.duration_seconds,
                quiz_score=log_data.quiz_score,
                completed_at=datetime.now(timezone.utc)
            )
            progress.completed_topics.append(new_completion)

        progress.last_active_at = datetime.now(timezone.utc)
        progress.updated_at = datetime.now(timezone.utc)
        
        return await self.progress_repo.update(progress.id, progress)

    async def get_subject_progress_response(self, user_id: str, subject_id: str) -> Optional[SubjectProgressResponse]:
        """Compute structural metrics and build client progress payloads"""
        subject = curriculum_service.get_subject(subject_id)
        if not subject:
            return None

        progress = await self.get_or_create_progress(user_id, subject_id)
        
        # Calculate total count of topics in syllabus
        total_topics = 0
        for mod in subject.get("modules", []):
            total_topics += len(mod.get("topics", []))

        completion_pct = 0.0
        if total_topics > 0:
            completion_pct = (len(progress.completed_topics) / total_topics) * 100.0

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
