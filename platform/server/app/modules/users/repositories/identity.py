from abc import abstractmethod
from typing import Any, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.users.models.identity import UserIdentityModel
from app.repositories.base import BaseRepository

class UserIdentityRepository(BaseRepository[UserIdentityModel]):
    @abstractmethod
    async def get_by_provider_id(self, provider: str, provider_user_id: str) -> Optional[UserIdentityModel]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> Optional[UserIdentityModel]:
        pass

class MongoUserIdentityRepository(UserIdentityRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["user_identities"]

    async def get_by_id(self, id: Any) -> Optional[UserIdentityModel]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            return UserIdentityModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_provider_id(self, provider: str, provider_user_id: str) -> Optional[UserIdentityModel]:
        doc = await self.collection.find_one({
            "provider": provider,
            "provider_user_id": provider_user_id.lower().strip()
        })
        return UserIdentityModel(**doc) if doc else None

    async def get_by_user_id(self, user_id: str) -> Optional[UserIdentityModel]:
        doc = await self.collection.find_one({"user_id": user_id})
        return UserIdentityModel(**doc) if doc else None

    async def get_all(self):
        return []

    async def create(self, entity: UserIdentityModel) -> UserIdentityModel:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: UserIdentityModel) -> Optional[UserIdentityModel]:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.replace_one({"_id": ObjectId(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
