from abc import ABC, abstractmethod
from typing import Any, Callable

class BackgroundTaskProvider(ABC):
    """Abstract provider layer to delegate async job executions"""
    @abstractmethod
    async def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        pass

class BackgroundTaskService(ABC):
    """Shared platform contract to queue background actions"""
    @abstractmethod
    async def run_in_background(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        pass
