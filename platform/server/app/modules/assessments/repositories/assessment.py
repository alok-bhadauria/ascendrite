from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.assessments.models.assessment import AssessmentModel
from app.repositories.base import BaseRepository

class AssessmentRepository(BaseRepository[AssessmentModel], ABC):
    @abstractmethod
    async def get_by_topic(self, topic_id: str) -> List[AssessmentModel]:
        pass

class MongoAssessmentRepository(AssessmentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["assessments"]

    def _to_db_doc(self, model: AssessmentModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        # Convert user_id / session_id if needed, but assessment doesn't track user ids directly in model
        return doc

    def _to_query_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def get_by_id(self, id: Any) -> Optional[AssessmentModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return AssessmentModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_topic(self, topic_id: str) -> List[AssessmentModel]:
        try:
            cursor = self.collection.find({"topic_id": topic_id})
            return [AssessmentModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[AssessmentModel]:
        cursor = self.collection.find()
        return [AssessmentModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: AssessmentModel) -> AssessmentModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: AssessmentModel) -> Optional[AssessmentModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0
