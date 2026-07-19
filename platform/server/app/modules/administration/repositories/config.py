from abc import ABC, abstractmethod
from typing import Any, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.administration.models.config import PlatformConfigModel
from app.repositories.base import BaseRepository

class PlatformConfigRepository(BaseRepository[PlatformConfigModel], ABC):
    pass

class MongoPlatformConfigRepository(PlatformConfigRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["platform_configs"]

    def _to_db_doc(self, model: PlatformConfigModel) -> dict:
        return model.model_dump(by_alias=True)

    async def get_by_id(self, id: Any) -> Optional[PlatformConfigModel]:
        try:
            doc = await self.collection.find_one({"_id": str(id)})
            return PlatformConfigModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[PlatformConfigModel]:
        cursor = self.collection.find()
        return [PlatformConfigModel(**doc) for doc in await cursor.to_list(length=10)]

    async def create(self, entity: PlatformConfigModel) -> PlatformConfigModel:
        doc = self._to_db_doc(entity)
        await self.collection.insert_one(doc)
        return entity

    async def update(self, id: Any, entity: PlatformConfigModel) -> Optional[PlatformConfigModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": str(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": str(id)})
        return result.deleted_count > 0
