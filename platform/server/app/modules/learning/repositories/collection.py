from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.learning.models.collection import LearningCollectionModel
from app.repositories.base import BaseRepository

class LearningCollectionRepository(BaseRepository[LearningCollectionModel], ABC):
    @abstractmethod
    async def get_by_user(self, user_id: Any) -> List[LearningCollectionModel]:
        pass

    @abstractmethod
    async def get_by_user_and_type(self, user_id: Any, collection_type: str) -> Optional[LearningCollectionModel]:
        pass

class MongoLearningCollectionRepository(LearningCollectionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["learning_collections"]

    def _to_db_doc(self, model: LearningCollectionModel) -> dict:
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

    async def get_by_id(self, id: Any) -> Optional[LearningCollectionModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return LearningCollectionModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_user(self, user_id: Any) -> List[LearningCollectionModel]:
        try:
            cursor = self.collection.find({"user_id": self._to_query_id(user_id)})
            return [LearningCollectionModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_by_user_and_type(self, user_id: Any, collection_type: str) -> Optional[LearningCollectionModel]:
        try:
            doc = await self.collection.find_one({
                "user_id": self._to_query_id(user_id),
                "collection_type": collection_type
            })
            return LearningCollectionModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[LearningCollectionModel]:
        cursor = self.collection.find()
        return [LearningCollectionModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: LearningCollectionModel) -> LearningCollectionModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: LearningCollectionModel) -> Optional[LearningCollectionModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0
