from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.errors import ForbiddenException, AppException
from app.core.runtime.context import RuntimeContext
from app.modules.learning.models.collection import LearningCollectionModel
from app.modules.learning.models.goal import LearningGoalModel
from app.modules.learning.repositories.collection import LearningCollectionRepository
from app.modules.learning.repositories.goal import LearningGoalRepository

class LearningUtilitiesService:
    def __init__(
        self,
        collection_repo: LearningCollectionRepository,
        goal_repo: LearningGoalRepository,
        db: AsyncIOMotorDatabase
    ):
        self.collection_repo = collection_repo
        self.goal_repo = goal_repo
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

    # --- Collections (Bookmarks/Favorites) ---

    async def create_collection(
        self,
        collection_type: str,
        name: str,
        context: RuntimeContext
    ) -> LearningCollectionModel:
        self._require_capability(context, "learning:write")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # Check if collection of same type and name exists
        existing = await self.collection_repo.get_by_user_and_type(db_user_id, collection_type)
        if existing and existing.name == name:
            return existing

        col = LearningCollectionModel(
            user_id=db_user_id,
            collection_type=collection_type,
            name=name,
            resources=[]
        )
        return await self.collection_repo.create(col)

    async def get_collections(self, context: RuntimeContext) -> List[LearningCollectionModel]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)
        return await self.collection_repo.get_by_user(db_user_id)

    async def add_to_collection(
        self,
        collection_id: str,
        resource_id: str,
        resource_type: str,
        context: RuntimeContext
    ) -> LearningCollectionModel:
        self._require_capability(context, "learning:write")
        col = await self.collection_repo.get_by_id(collection_id)
        if not col:
            raise AppException(f"Collection '{collection_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(col.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this collection.")

        # Avoid duplicates
        if not any(r.get("resource_id") == resource_id for r in col.resources):
            col.resources.append({
                "resource_id": resource_id,
                "resource_type": resource_type,
                "added_at": datetime.now(timezone.utc).isoformat()
            })
            col.updated_at = datetime.now(timezone.utc)
            updated = await self.collection_repo.update(collection_id, col)
            if not updated:
                raise AppException("Failed to add resource to collection.", code="UPDATE_FAILED", status_code=500)
            return updated
        return col

    async def remove_from_collection(
        self,
        collection_id: str,
        resource_id: str,
        context: RuntimeContext
    ) -> LearningCollectionModel:
        self._require_capability(context, "learning:write")
        col = await self.collection_repo.get_by_id(collection_id)
        if not col:
            raise AppException(f"Collection '{collection_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(col.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this collection.")

        col.resources = [r for r in col.resources if r.get("resource_id") != resource_id]
        col.updated_at = datetime.now(timezone.utc)
        updated = await self.collection_repo.update(collection_id, col)
        if not updated:
            raise AppException("Failed to remove resource from collection.", code="UPDATE_FAILED", status_code=500)
        return updated

    # --- Planner Goals ---

    async def create_goal(
        self,
        target_date: datetime,
        topic_ids: List[str],
        context: RuntimeContext
    ) -> LearningGoalModel:
        self._require_capability(context, "learning:write")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # Verify target topics exist
        for topic_id in topic_ids:
            topic_doc = await self.db["topics"].find_one({"_id": topic_id})
            if not topic_doc:
                raise AppException(f"Topic '{topic_id}' not found.", code="NOT_FOUND", status_code=404)

        goal = LearningGoalModel(
            user_id=db_user_id,
            target_date=target_date,
            topic_ids=topic_ids,
            status="pending"
        )
        return await self.goal_repo.create(goal)

    async def get_goals(self, context: RuntimeContext) -> List[LearningGoalModel]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)
        return await self.goal_repo.get_by_user(db_user_id)

    async def update_goal_status(
        self,
        goal_id: str,
        status: str,
        context: RuntimeContext
    ) -> LearningGoalModel:
        self._require_capability(context, "learning:write")
        goal = await self.goal_repo.get_by_id(goal_id)
        if not goal:
            raise AppException(f"Goal '{goal_id}' not found.", code="NOT_FOUND", status_code=404)

        if str(goal.user_id) != str(context.principal.id):
            raise ForbiddenException("Principal does not own this goal.")

        goal.status = status
        goal.updated_at = datetime.now(timezone.utc)
        updated = await self.goal_repo.update(goal_id, goal)
        if not updated:
            raise AppException("Failed to update goal.", code="UPDATE_FAILED", status_code=500)
        return updated

    # --- Recently Accessed & Completed ---

    async def get_recently_accessed(self, context: RuntimeContext, limit: int = 10) -> List[Dict[str, Any]]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # Retrieve latest experiences or attempts representing recent activity
        cursor = self.db["learning_attempts"].find({"user_id": db_user_id}).sort("start_time", -1).limit(limit)
        attempts = await cursor.to_list(length=limit)

        recent = []
        seen = set()
        for a in attempts:
            res_id = a.get("resource_id")
            res_type = a.get("resource_type")
            key = f"{res_type}:{res_id}"
            if key not in seen:
                seen.add(key)
                recent.append({
                    "resource_id": res_id,
                    "resource_type": res_type,
                    "accessed_at": a.get("start_time").isoformat() if a.get("start_time") else None
                })
        return recent

    async def get_recently_completed(self, context: RuntimeContext, limit: int = 10) -> List[Dict[str, Any]]:
        self._require_capability(context, "learning:read")
        user_id = context.principal.id
        db_user_id = self._to_db_id(user_id)

        # Retrieve completed learning attempts
        cursor = self.db["learning_attempts"].find({
            "user_id": db_user_id,
            "status": "completed"
        }).sort("end_time", -1).limit(limit)
        attempts = await cursor.to_list(length=limit)

        completed = []
        seen = set()
        for a in attempts:
            res_id = a.get("resource_id")
            res_type = a.get("resource_type")
            key = f"{res_type}:{res_id}"
            if key not in seen:
                seen.add(key)
                completed.append({
                    "resource_id": res_id,
                    "resource_type": res_type,
                    "completed_at": a.get("end_time").isoformat() if a.get("end_time") else None,
                    "score": a.get("score")
                })
        return completed
