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
        return b""

rustfs_storage = RustFSStorageBoundary()

def get_rustfs() -> StorageProvider:
    return rustfs_storage
