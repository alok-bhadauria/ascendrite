from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.runtime.context import RuntimeContext
from app.modules.assets.models.asset import AssetModel, AssetStatus

class AssetService(ABC):
    """Interface boundary representing platform Asset service layer"""
    @abstractmethod
    async def upload_asset(
        self,
        filename: str,
        content_type: str,
        data: bytes,
        context: RuntimeContext
    ) -> AssetModel:
        pass

    @abstractmethod
    async def retrieve_asset_binary(self, asset_id: str, context: RuntimeContext) -> bytes:
        pass

    @abstractmethod
    async def get_asset_metadata(self, asset_id: str, context: RuntimeContext) -> AssetModel:
        pass

    @abstractmethod
    async def transition_asset_lifecycle(
        self,
        asset_id: str,
        new_status: AssetStatus,
        context: RuntimeContext
    ) -> AssetModel:
        pass

    @abstractmethod
    async def get_owner_assets(self, owner_id: str, context: RuntimeContext) -> List[AssetModel]:
        pass
