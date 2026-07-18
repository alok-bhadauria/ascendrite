from abc import abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.users.models.user import UserModel
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserModel]:
        pass

class MongoUserRepository(UserRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["users"]

    async def get_by_id(self, id: Any) -> Optional[UserModel]:
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id), "is_deleted": False})
            return UserModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        doc = await self.collection.find_one({"email": email.lower().strip(), "is_deleted": False})
        return UserModel(**doc) if doc else None

    async def get_all(self) -> List[UserModel]:
        cursor = self.collection.find({"is_deleted": False})
        return [UserModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: UserModel) -> UserModel:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: UserModel) -> Optional[UserModel]:
        doc = entity.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.replace_one({"_id": ObjectId(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.update_one({"_id": ObjectId(id)}, {"$set": {"is_deleted": True}})
        return result.modified_count > 0
