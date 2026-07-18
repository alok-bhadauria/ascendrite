import logging
from app.infrastructure.storage.base import StorageProvider

logger = logging.getLogger(__name__)

class StorageManager:
    """
    Intermediate management layer isolating business service layers 
    from raw backend physical storage operations.
    """
    def __init__(self, provider: StorageProvider):
        self._provider = provider

    def generate_storage_key(self, owner_id: str, asset_id: str, filename: str) -> str:
        return f"assets/{owner_id}/{asset_id}/{filename}"

    def retrieve_object(self, key: str) -> bytes:
        bucket = "ascendrite-assets"
        return self._provider.get_object(bucket, key)

    def store_object(self, key: str, data: bytes, content_type: str) -> None:
        bucket = "ascendrite-assets"
        self._provider.put_object(bucket, key, data, content_type)

    def remove_object(self, key: str) -> None:
        bucket = "ascendrite-assets"
        self._provider.delete_object(bucket, key)
