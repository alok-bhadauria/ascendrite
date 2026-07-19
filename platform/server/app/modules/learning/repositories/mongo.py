from typing import List, Optional, Any
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.learning.models.learning_session import LearningSessionModel, SessionStatus
from app.modules.learning.models.learning_attempt import LearningAttemptModel
from app.modules.learning.repositories.base import LearningSessionRepository, LearningAttemptRepository

def _to_db_doc(model) -> dict:
    doc = model.model_dump(by_alias=True, exclude={"id"})
    # Ensure ObjectId types are preserved as ObjectIds in MongoDB
    for key in ["user_id", "session_id"]:
        if key in doc and doc[key] is not None:
            val = doc[key]
            if isinstance(val, str) and ObjectId.is_valid(val):
                doc[key] = ObjectId(val)
            elif not isinstance(val, ObjectId):
                try:
                    doc[key] = ObjectId(str(val))
                except Exception:
                    pass
    return doc

def _to_query_id(val: Any) -> Any:
    if isinstance(val, str) and ObjectId.is_valid(val):
        return ObjectId(val)
    return val

class MongoLearningSessionRepository(LearningSessionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["learning_sessions"]

    async def create(self, session: LearningSessionModel) -> LearningSessionModel:
        doc = _to_db_doc(session)
        result = await self.collection.insert_one(doc)
        session.id = str(result.inserted_id)
        return session

    async def get_by_id(self, session_id: Any) -> Optional[LearningSessionModel]:
        try:
            doc = await self.collection.find_one({"_id": _to_query_id(session_id)})
            return LearningSessionModel(**doc) if doc else None
        except Exception:
            return None

    async def update(self, session_id: Any, session: LearningSessionModel) -> Optional[LearningSessionModel]:
        try:
            doc = _to_db_doc(session)
            result = await self.collection.replace_one({"_id": _to_query_id(session_id)}, doc)
            if result.matched_count:
                return session
            return None
        except Exception:
            return None

    async def get_active_session_by_user(self, user_id: Any) -> Optional[LearningSessionModel]:
        try:
            doc = await self.collection.find_one({
                "user_id": _to_query_id(user_id),
                "status": SessionStatus.ACTIVE.value
            })
            return LearningSessionModel(**doc) if doc else None
        except Exception:
            return None


class MongoLearningAttemptRepository(LearningAttemptRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["learning_attempts"]

    async def create(self, attempt: LearningAttemptModel) -> LearningAttemptModel:
        doc = _to_db_doc(attempt)
        result = await self.collection.insert_one(doc)
        attempt.id = str(result.inserted_id)
        return attempt

    async def get_by_id(self, attempt_id: Any) -> Optional[LearningAttemptModel]:
        try:
            doc = await self.collection.find_one({"_id": _to_query_id(attempt_id)})
            return LearningAttemptModel(**doc) if doc else None
        except Exception:
            return None

    async def update(self, attempt_id: Any, attempt: LearningAttemptModel) -> Optional[LearningAttemptModel]:
        try:
            doc = _to_db_doc(attempt)
            result = await self.collection.replace_one({"_id": _to_query_id(attempt_id)}, doc)
            if result.matched_count:
                return attempt
            return None
        except Exception:
            return None

    async def list_by_user(self, user_id: Any) -> List[LearningAttemptModel]:
        try:
            cursor = self.collection.find({"user_id": _to_query_id(user_id)})
            docs = await cursor.to_list(length=100)
            return [LearningAttemptModel(**doc) for doc in docs]
        except Exception:
            return []

    async def list_by_session(self, session_id: Any) -> List[LearningAttemptModel]:
        try:
            cursor = self.collection.find({"session_id": _to_query_id(session_id)})
            docs = await cursor.to_list(length=100)
            return [LearningAttemptModel(**doc) for doc in docs]
        except Exception:
            return []

    async def get_last_attempt(self, user_id: Any, resource_id: str) -> Optional[LearningAttemptModel]:
        try:
            doc = await self.collection.find_one(
                {"user_id": _to_query_id(user_id), "resource_id": resource_id},
                sort=[("start_time", -1)]
            )
            return LearningAttemptModel(**doc) if doc else None
        except Exception:
            return None
