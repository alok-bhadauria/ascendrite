from abc import abstractmethod
from typing import Any, List, Optional
from datetime import datetime, timezone
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.authentication.models.session import SessionModel
from app.repositories.base import BaseRepository

class SessionRepository(BaseRepository[SessionModel]):
    @abstractmethod
    async def get_by_refresh_token_id(self, refresh_token_id: str) -> Optional[SessionModel]:
        pass

    @abstractmethod
    async def get_active_by_user_id(self, user_id: str) -> List[SessionModel]:
        pass

    @abstractmethod
    async def revoke_family(self, token_family_id: str, reason: str) -> bool:
        pass

    @abstractmethod
    async def revoke_others(self, user_id: str, active_token_family_id: str, reason: str) -> bool:
        pass

class MongoSessionRepository(SessionRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["sessions"]

    async def get_by_id(self, id: Any) -> Optional[SessionModel]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            return SessionModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[SessionModel]:
        cursor = self.collection.find({})
        return [SessionModel(**doc) for doc in await cursor.to_list(length=100)]

    async def get_by_refresh_token_id(self, refresh_token_id: str) -> Optional[SessionModel]:
        doc = await self.collection.find_one({"refresh_token_id": refresh_token_id})
        return SessionModel(**doc) if doc else None

    async def get_active_by_user_id(self, user_id: str) -> List[SessionModel]:
        cursor = self.collection.find({
            "user_id": user_id,
            "is_revoked": False,
            "expires_at": {"$gt": datetime.now(timezone.utc)}
        })
        return [SessionModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: SessionModel) -> SessionModel:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: SessionModel) -> Optional[SessionModel]:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.replace_one({"_id": ObjectId(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0

    async def revoke_family(self, token_family_id: str, reason: str) -> bool:
        result = await self.collection.update_many(
            {"token_family_id": token_family_id, "is_revoked": False},
            {"$set": {
                "is_revoked": True,
                "revoked_reason": reason,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        return result.modified_count > 0

    async def revoke_others(self, user_id: str, active_token_family_id: str, reason: str) -> bool:
        result = await self.collection.update_many(
            {
                "user_id": user_id,
                "token_family_id": {"$ne": active_token_family_id},
                "is_revoked": False
            },
            {"$set": {
                "is_revoked": True,
                "revoked_reason": reason,
                "updated_at": datetime.now(timezone.utc)
            }}
        )
        return result.modified_count > 0
