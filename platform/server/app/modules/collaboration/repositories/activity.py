from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.collaboration.models.activity import CollaborationActivityModel, CollaborationNotificationModel
from app.repositories.base import BaseRepository

class CollaborationActivityRepository(BaseRepository[CollaborationActivityModel], ABC):
    @abstractmethod
    async def get_by_resource(self, resource_id: str) -> List[CollaborationActivityModel]:
        pass

class MongoCollaborationActivityRepository(CollaborationActivityRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["collaboration_activities"]

    def _to_db_doc(self, model: CollaborationActivityModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["team_id", "actor_id"]:
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

    async def get_by_id(self, id: Any) -> Optional[CollaborationActivityModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return CollaborationActivityModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_resource(self, resource_id: str) -> List[CollaborationActivityModel]:
        try:
            cursor = self.collection.find({"resource_id": resource_id}).sort("created_at", -1)
            return [CollaborationActivityModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[CollaborationActivityModel]:
        cursor = self.collection.find().sort("created_at", -1)
        return [CollaborationActivityModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: CollaborationActivityModel) -> CollaborationActivityModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: CollaborationActivityModel) -> Optional[CollaborationActivityModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0


class CollaborationNotificationRepository(BaseRepository[CollaborationNotificationModel], ABC):
    @abstractmethod
    async def get_by_recipient(self, recipient_id: Any) -> List[CollaborationNotificationModel]:
        pass

class MongoCollaborationNotificationRepository(CollaborationNotificationRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["collaboration_notifications"]

    def _to_db_doc(self, model: CollaborationNotificationModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["recipient_id"]:
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

    async def get_by_id(self, id: Any) -> Optional[CollaborationNotificationModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return CollaborationNotificationModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_recipient(self, recipient_id: Any) -> List[CollaborationNotificationModel]:
        try:
            cursor = self.collection.find({"recipient_id": self._to_query_id(recipient_id)}).sort("created_at", -1)
            return [CollaborationNotificationModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_all(self) -> List[CollaborationNotificationModel]:
        cursor = self.collection.find().sort("created_at", -1)
        return [CollaborationNotificationModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: CollaborationNotificationModel) -> CollaborationNotificationModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: CollaborationNotificationModel) -> Optional[CollaborationNotificationModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0
