from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.modules.assets.models.asset import AssetModel
from app.modules.assets.repositories.base import AssetRepository

class MongoAssetRepository(AssetRepository):
    """MongoDB implementation of the AssetRepository contract"""
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["assets"]

    async def create(self, asset: AssetModel) -> AssetModel:
        doc = asset.model_dump(by_alias=True)
        await self.collection.insert_one(doc)
        return asset

    async def get_by_id(self, asset_id: str) -> Optional[AssetModel]:
        doc = await self.collection.find_one({"_id": asset_id})
        return AssetModel(**doc) if doc else None

    async def update(self, asset_id: str, asset: AssetModel) -> AssetModel:
        asset.updated_at = asset.updated_at.now()
        doc = asset.model_dump(by_alias=True)
        await self.collection.replace_one({"_id": asset_id}, doc)
        return asset

    async def get_by_owner(self, owner_id: str) -> List[AssetModel]:
        cursor = self.collection.find({"owner_id": owner_id})
        docs = await cursor.to_list(length=100)
        return [AssetModel(**doc) for doc in docs]
