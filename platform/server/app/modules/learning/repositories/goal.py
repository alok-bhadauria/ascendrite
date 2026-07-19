from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.learning.models.goal import LearningGoalModel
from app.repositories.base import BaseRepository

class LearningGoalRepository(BaseRepository[LearningGoalModel], ABC):
    @abstractmethod
    async def get_by_user(self, user_id: Any) -> List[LearningGoalModel]:
        pass

class MongoLearningGoalRepository(LearningGoalRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["learning_goals"]

    def _to_db_doc(self, model: LearningGoalModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["user_id"]:
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

    def _to_query_id(self, val: Any) -> Any:
        if isinstance(val, str) and ObjectId.is_valid(val):
            return ObjectId(val)
        return val

    async def get_by_id(self, id: Any) -> Optional[LearningGoalModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return LearningGoalModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_user(self, user_id: Any) -> List[LearningGoalModel]:
        try:
            cursor = self.collection.find({"user_id": self._to_query_id(user_id)})
            return [LearningGoalModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[LearningGoalModel]:
        cursor = self.collection.find()
        return [LearningGoalModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: LearningGoalModel) -> LearningGoalModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: LearningGoalModel) -> Optional[LearningGoalModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0
