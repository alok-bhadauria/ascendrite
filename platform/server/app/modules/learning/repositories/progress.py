from abc import abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.learning.models.progress import ProgressModel
from app.repositories.base import BaseRepository

class ProgressRepository(BaseRepository[ProgressModel]):
    @abstractmethod
    async def get_by_user_and_subject(self, user_id: Any, subject_id: str) -> Optional[ProgressModel]:
        pass

def _to_db_doc(model) -> dict:
    doc = model.model_dump(by_alias=True, exclude={"id"})
    if "user_id" in doc and doc["user_id"] is not None:
        val = doc["user_id"]
        if isinstance(val, str) and ObjectId.is_valid(val):
            doc["user_id"] = ObjectId(val)
        elif not isinstance(val, ObjectId):
            try:
                doc["user_id"] = ObjectId(str(val))
            except Exception:
                pass
    return doc

def _to_query_id(val: Any) -> Any:
    if isinstance(val, str) and ObjectId.is_valid(val):
        return ObjectId(val)
    return val

class MongoProgressRepository(ProgressRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["progress"]

    async def get_by_id(self, id: Any) -> Optional[ProgressModel]:
        try:
            doc = await self.collection.find_one({"_id": _to_query_id(id)})
            return ProgressModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_user_and_subject(self, user_id: Any, subject_id: str) -> Optional[ProgressModel]:
        try:
            doc = await self.collection.find_one({
                "user_id": _to_query_id(user_id),
                "subject_id": subject_id
            })
            return ProgressModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[ProgressModel]:
        cursor = self.collection.find()
        return [ProgressModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: ProgressModel) -> ProgressModel:
        doc = _to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: ProgressModel) -> Optional[ProgressModel]:
        doc = _to_db_doc(entity)
        result = await self.collection.replace_one({"_id": _to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": _to_query_id(id)})
        return result.deleted_count > 0
