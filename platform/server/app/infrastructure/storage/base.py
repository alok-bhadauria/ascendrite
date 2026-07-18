from abc import ABC, abstractmethod

class StorageProvider(ABC):
    """
    Stable platform abstraction for file storage integrations.
    Decoupled from S3-specific details to support switching backends:
    Local RustFS -> Local MinIO -> AWS S3 -> Azure Blob Storage.
    """
    @abstractmethod
    def get_object(self, bucket: str, key: str) -> bytes:
        pass
