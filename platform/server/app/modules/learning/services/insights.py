from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.modules.learning.schemas.insights import (
    LearningHistoryItem,
    EducationalRecommendation,
    WeakAreaResponse,
    LearnerDashboardResponse
)
from app.modules.learning.models.progress import LearningStatus
from app.modules.learning.models.experience import ExperienceStatus

class LearningInsightsService:
    """Provides analytical dashboard data and metrics aggregation for student learning records and achievements."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

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

    async def get_dashboard(self, context: RuntimeContext) -> LearnerDashboardResponse:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # 1. Total counts
        total_sessions = await self.db["learning_sessions"].count_documents({"user_id": db_user_id})
        total_attempts = await self.db["learning_attempts"].count_documents({"user_id": db_user_id})

        # 2. Progress summaries
        cursor = self.db["progress"].find({"user_id": db_user_id})
        progress_docs = await cursor.to_list(length=100)

        mastered_count = 0
        needs_review_count = 0
        for doc in progress_docs:
            for item in doc.get("completed_topics", []):
                status = item.get("status")
                if status == LearningStatus.MASTERED.value:
                    mastered_count += 1
                elif status == LearningStatus.REVIEWED.value:
                    needs_review_count += 1

        # 3. Last active attempt/session
        last_attempt_doc = await self.db["learning_attempts"].find_one(
            {"user_id": db_user_id},
            sort=[("start_time", -1)]
        )
        last_session_doc = await self.db["learning_sessions"].find_one(
            {"user_id": db_user_id},
            sort=[("start_time", -1)]
        )

        last_attempt_at = last_attempt_doc.get("end_time") or last_attempt_doc.get("start_time") if last_attempt_doc else None
        last_session_id = str(last_session_doc["_id"]) if last_session_doc else None

        # 4. Next study topic resolution
        # Check active experience first
        active_exp = await self.db["learning_experiences"].find_one(
            {"user_id": db_user_id, "status": ExperienceStatus.ACTIVE.value},
            sort=[("start_time", -1)]
        )
        
        next_topic_id = None
        if active_exp:
            next_topic_id = active_exp.get("resource_id")
        else:
            # Fallback to latest incomplete progress topic
            incomplete_topic = None
            for doc in progress_docs:
                for item in doc.get("completed_topics", []):
                    if item.get("status") == LearningStatus.IN_PROGRESS.value:
                        incomplete_topic = item.get("topic_id")
                        break
                if incomplete_topic:
                    break
            next_topic_id = incomplete_topic

        # If still None, pick latest attempt resource_id if it was a topic
        if not next_topic_id and last_attempt_doc:
            if last_attempt_doc.get("resource_type") == "topic":
                next_topic_id = last_attempt_doc.get("resource_id")

        return LearnerDashboardResponse(
            next_study_topic_id=next_topic_id,
            last_active_session_id=last_session_id,
            last_attempt_at=last_attempt_at,
            mastered_topics_count=mastered_count,
            needs_review_count=needs_review_count,
            total_sessions_count=total_sessions,
            total_attempts_count=total_attempts
        )

    async def get_history(self, context: RuntimeContext, limit: int = 50) -> List[LearningHistoryItem]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        history: List[LearningHistoryItem] = []

        # 1. Fetch sessions
        sessions_cursor = self.db["learning_sessions"].find({"user_id": db_user_id}).sort("start_time", -1).limit(limit)
        sessions = await sessions_cursor.to_list(length=limit)
        for s in sessions:
            history.append(LearningHistoryItem(
                event_type="session_start",
                timestamp=s["start_time"],
                description="Started learning session",
                resource_id=str(s["_id"])
            ))
            if s.get("end_time"):
                history.append(LearningHistoryItem(
                    event_type="session_close",
                    timestamp=s["end_time"],
                    description="Closed learning session",
                    resource_id=str(s["_id"])
                ))

        # 2. Fetch attempts
        attempts_cursor = self.db["learning_attempts"].find({"user_id": db_user_id}).sort("start_time", -1).limit(limit)
        attempts = await attempts_cursor.to_list(length=limit)
        for a in attempts:
            status = a.get("status")
            desc = f"Completed attempt on {a.get('resource_type')}" if status == "completed" else f"Attempt on {a.get('resource_type')} {status}"
            history.append(LearningHistoryItem(
                event_type="attempt_complete" if status == "completed" else "attempt_abandoned",
                timestamp=a.get("end_time") or a.get("start_time"),
                description=desc,
                resource_id=a.get("resource_id"),
                resource_type=a.get("resource_type"),
                score=a.get("score")
            ))

        # 3. Fetch experiences
        exps_cursor = self.db["learning_experiences"].find({"user_id": db_user_id}).sort("start_time", -1).limit(limit)
        exps = await exps_cursor.to_list(length=limit)
        for e in exps:
            history.append(LearningHistoryItem(
                event_type="experience_start",
                timestamp=e["start_time"],
                description=f"Started {e.get('experience_type')} experience",
                resource_id=e.get("resource_id"),
                resource_type=e.get("experience_type")
            ))
            if e.get("end_time"):
                history.append(LearningHistoryItem(
                    event_type="experience_complete" if e.get("status") == "completed" else "experience_abandoned",
                    timestamp=e["end_time"],
                    description=f"Closed {e.get('experience_type')} experience ({e.get('status')})",
                    resource_id=e.get("resource_id"),
                    resource_type=e.get("experience_type")
                ))

        # Sort combined list by timestamp descending and apply limit
        history.sort(key=lambda x: x.timestamp, reverse=True)
        return history[:limit]

    async def get_recommendations(self, context: RuntimeContext) -> List[EducationalRecommendation]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        recommendations: List[EducationalRecommendation] = []

        # Rule 1: Active experiences that are incomplete
        active_exp = await self.db["learning_experiences"].find_one(
            {"user_id": db_user_id, "status": ExperienceStatus.ACTIVE.value},
            sort=[("start_time", -1)]
        )
        if active_exp:
            recommendations.append(EducationalRecommendation(
                type="resume_experience",
                title="Resume Interrupted Study",
                reason=f"You have an active {active_exp.get('experience_type')} session. Click here to pick up where you left off.",
                resource_id=active_exp.get("resource_id"),
                resource_type=active_exp.get("experience_type")
            ))

        # Rule 2: In-progress or reviewed topics
        cursor = self.db["progress"].find({"user_id": db_user_id})
        progress_docs = await cursor.to_list(length=100)
        for doc in progress_docs:
            for item in doc.get("completed_topics", []):
                status = item.get("status")
                topic_id = item.get("topic_id")
                if status == LearningStatus.IN_PROGRESS.value:
                    recommendations.append(EducationalRecommendation(
                        type="continue_topic",
                        title="Continue Topic Learning",
                        reason=f"You started this topic but have not finished all material yet.",
                        resource_id=topic_id,
                        resource_type="topic"
                    ))
                elif status == LearningStatus.REVIEWED.value:
                    recommendations.append(EducationalRecommendation(
                        type="review_weakness",
                        title="Review Recommended",
                        reason=f"Revisit this concept to refresh your knowledge and improve retention.",
                        resource_id=topic_id,
                        resource_type="topic"
                    ))

        # Rule 3: Unsuccessful assessments (score < 0.7)
        attempts_cursor = self.db["learning_attempts"].find({
            "user_id": db_user_id,
            "status": "completed",
            "score": {"$lt": 0.7}
        }).sort("start_time", -1).limit(5)
        unsuccessful = await attempts_cursor.to_list(length=5)
        for u in unsuccessful:
            # Avoid duplicate recommendations for the same resource
            if not any(r.resource_id == u.get("resource_id") for r in recommendations):
                recommendations.append(EducationalRecommendation(
                    type="retry_assessment",
                    title="Retry Assessment",
                    reason=f"Your latest score on this {u.get('resource_type')} was {int(u.get('score')*100)}%. Try again to improve mastery.",
                    resource_id=u.get("resource_id"),
                    resource_type=u.get("resource_type")
                ))

        return recommendations

    async def get_weak_areas(self, context: RuntimeContext) -> List[WeakAreaResponse]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # Retrieve completed attempts to analyze score trends
        attempts_cursor = self.db["learning_attempts"].find({
            "user_id": db_user_id,
            "status": "completed",
            "score": {"$exists": True, "$ne": None}
        })
        attempts = await attempts_cursor.to_list(length=200)

        # Group scores by resource
        resource_stats: Dict[str, Dict[str, Any]] = {}
        for a in attempts:
            res_id = a.get("resource_id")
            score = a.get("score")
            res_type = a.get("resource_type")
            if res_id not in resource_stats:
                resource_stats[res_id] = {"scores": [], "type": res_type}
            resource_stats[res_id]["scores"].append(score)

        weak_areas: List[WeakAreaResponse] = []
        for res_id, stats in resource_stats.items():
            scores = stats["scores"]
            avg_score = sum(scores) / len(scores) if scores else 1.0
            
            # Map resource back to its topic ID
            topic_id = res_id
            if stats["type"] != "topic":
                content_doc = await self.db["knowledge_contents"].find_one({"_id": res_id})
                if content_doc:
                    topic_id = content_doc.get("topic_id")

            # Weakness criteria: average score < 0.7 OR latest score < 0.7
            if avg_score < 0.7 or (scores and scores[-1] < 0.7):
                # Avoid duplicates in weak areas list
                if not any(w.topic_id == topic_id for w in weak_areas):
                    weak_areas.append(WeakAreaResponse(
                        topic_id=topic_id,
                        average_score=round(avg_score, 2),
                        attempts_count=len(scores),
                        recommendation=f"Review weak concept gaps. Focus on assessments for this topic to target improvement."
                    ))

        return weak_areas
