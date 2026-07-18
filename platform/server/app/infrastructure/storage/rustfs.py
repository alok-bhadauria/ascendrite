import logging
from app.core.config import settings
from app.infrastructure.storage.base import StorageProvider

logger = logging.getLogger(__name__)

class RustFSStorageBoundary(StorageProvider):
    def __init__(self):
        self.endpoint = settings.S3_ENDPOINT
        self.region = settings.S3_REGION

    def get_object(self, bucket: str, key: str) -> bytes:
        logger.info(f"RustFS storage lookup: bucket={bucket} key={key}")
        # In a real environment we would fetch from storage endpoint; for now return mock bytes
        return b"mock-binary-data"

    def put_object(self, bucket: str, key: str, data: bytes, content_type: str) -> None:
        logger.info(f"RustFS storage put: bucket={bucket} key={key} size={len(data)} type={content_type}")

    def delete_object(self, bucket: str, key: str) -> None:
        logger.info(f"RustFS storage delete: bucket={bucket} key={key}")

rustfs_storage = RustFSStorageBoundary()

def get_rustfs() -> StorageProvider:
    return rustfs_storage
