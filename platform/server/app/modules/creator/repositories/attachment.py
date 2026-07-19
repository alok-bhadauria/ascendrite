from abc import ABC, abstractmethod
from typing import Any, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.creator.models.attachment import AssetAttachmentModel
from app.repositories.base import BaseRepository

class AssetAttachmentRepository(BaseRepository[AssetAttachmentModel], ABC):
    @abstractmethod
    async def get_by_draft(self, draft_id: Any) -> List[AssetAttachmentModel]:
        pass

    @abstractmethod
    async def get_link(self, draft_id: Any, asset_id: str) -> Optional[AssetAttachmentModel]:
        pass

class MongoAssetAttachmentRepository(AssetAttachmentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["creator_asset_attachments"]

    def _to_db_doc(self, model: AssetAttachmentModel) -> dict:
        doc = model.model_dump(by_alias=True, exclude={"id"})
        for key in ["draft_id"]:
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

    async def get_by_id(self, id: Any) -> Optional[AssetAttachmentModel]:
        try:
            doc = await self.collection.find_one({"_id": self._to_query_id(id)})
            return AssetAttachmentModel(**doc) if doc else None
        except Exception:
            return None

    async def get_by_draft(self, draft_id: Any) -> List[AssetAttachmentModel]:
        try:
            cursor = self.collection.find({"draft_id": self._to_query_id(draft_id)})
            return [AssetAttachmentModel(**doc) for doc in await cursor.to_list(length=100)]
        except Exception:
            return []

    async def get_link(self, draft_id: Any, asset_id: str) -> Optional[AssetAttachmentModel]:
        try:
            doc = await self.collection.find_one({
                "draft_id": self._to_query_id(draft_id),
                "asset_id": asset_id
            })
            return AssetAttachmentModel(**doc) if doc else None
        except Exception:
            return None

    async def get_all(self) -> List[AssetAttachmentModel]:
        cursor = self.collection.find()
        return [AssetAttachmentModel(**doc) for doc in await cursor.to_list(length=100)]

    async def create(self, entity: AssetAttachmentModel) -> AssetAttachmentModel:
        doc = self._to_db_doc(entity)
        result = await self.collection.insert_one(doc)
        entity.id = str(result.inserted_id)
        return entity

    async def update(self, id: Any, entity: AssetAttachmentModel) -> Optional[AssetAttachmentModel]:
        doc = self._to_db_doc(entity)
        result = await self.collection.replace_one({"_id": self._to_query_id(id)}, doc)
        if result.matched_count:
            return entity
        return None

    async def delete(self, id: Any) -> bool:
        result = await self.collection.delete_one({"_id": self._to_query_id(id)})
        return result.deleted_count > 0
