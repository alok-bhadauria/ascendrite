import asyncio
from typing import Any, Callable
from fastapi import BackgroundTasks
from app.core.runtime.tasks.base import BackgroundTaskProvider

class AsyncioBackgroundTaskProvider(BackgroundTaskProvider):
    """Concurrently enqueues the coroutine task utilizing standard asyncio.create_task loop execution"""
    async def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        asyncio.create_task(func(*args, **kwargs))

class FastAPIBackgroundTaskProvider(BackgroundTaskProvider):
    """Concurrently enqueues execution leveraging FastAPI/Starlette BackgroundTasks stack"""
    def __init__(self, background_tasks: BackgroundTasks):
        self._background_tasks = background_tasks

    async def enqueue(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._background_tasks.add_task(func, *args, **kwargs)
