from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar

T = TypeVar("T")

class BaseRepository(Generic[T], ABC):
    @abstractmethod
    async def get_by_id(self, id: Any) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self) -> List[T]:
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        pass

    @abstractmethod
    async def update(self, id: Any, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, id: Any) -> bool:
        pass
