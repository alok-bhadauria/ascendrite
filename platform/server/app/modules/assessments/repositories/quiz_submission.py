from abc import abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.assessments.models.quiz_submission import QuizSubmissionModel
from app.repositories.base import BaseRepository

class QuizSubmissionRepository(BaseRepository[QuizSubmissionModel]):
    @abstractmethod
    async def get_by_user(self, user_id: Any) -> List[QuizSubmissionModel]:
        pass

    @abstractmethod
    async def get_by_user_and_topic(self, user_id: Any, topic_id: str) -> List[QuizSubmissionModel]:
        pass

class MongoQuizSubmissionRepository(QuizSubmissionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["quiz_submissions"]

    async def get_by_id(self, id: Any) -> Optional[QuizSubmissionModel]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            return QuizSubmissionModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_user(self, user_id: Any) -> List[QuizSubmissionModel]:
        try:
            cursor = self.collection.find({"user_id": ObjectId(user_id)})
            return [QuizSubmissionModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_by_user_and_topic(self, user_id: Any, topic_id: str) -> List[QuizSubmissionModel]:
        try:
            cursor = self.collection.find({
                "user_id": ObjectId(user_id),
                "topic_id": topic_id
            })
            return [QuizSubmissionModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[QuizSubmissionModel]:
        cursor = self.collection.find()
        return [QuizSubmissionModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: QuizSubmissionModel) -> QuizSubmissionModel:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: QuizSubmissionModel) -> Optional[QuizSubmissionModel]:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.replace_one({"_id": ObjectId(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
