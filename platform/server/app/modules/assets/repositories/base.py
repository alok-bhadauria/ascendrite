from abc import ABC, abstractmethod
from typing import Optional, List
from app.modules.assets.models.asset import AssetModel

class AssetRepository(ABC):
    """Interface boundary for assets repository operations"""
    @abstractmethod
    async def create(self, asset: AssetModel) -> AssetModel:
        pass

    @abstractmethod
    async def get_by_id(self, asset_id: str) -> Optional[AssetModel]:
        pass

    @abstractmethod
    async def update(self, asset_id: str, asset: AssetModel) -> AssetModel:
        pass

    @abstractmethod
    async def get_by_owner(self, owner_id: str) -> List[AssetModel]:
        pass
