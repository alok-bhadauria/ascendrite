import logging
from typing import Any, Callable
from app.core.runtime.tasks.base import BackgroundTaskService, BackgroundTaskProvider

logger = logging.getLogger(__name__)

class BackgroundTaskScheduler(BackgroundTaskService):
    """
    Platform task coordinator delegating execution to the active provider.
    Keeps codebase independent from the runner runtime (Asyncio vs Celery).
    """
    def __init__(self, provider: BackgroundTaskProvider):
        self._provider = provider

    async def run_in_background(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        try:
            await self._provider.enqueue(func, *args, **kwargs)
        except Exception as e:
            logger.error(f"Failed to enqueue background task: {e}", exc_info=True)
