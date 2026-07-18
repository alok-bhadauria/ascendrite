import logging
from typing import Dict, List, Callable, Awaitable
from app.core.runtime.events.base import Event, EventDispatcher

logger = logging.getLogger(__name__)

class LocalEventDispatcher(EventDispatcher):
    """
    Lightweight, synchronous in-memory application event dispatcher.
    Runs handlers sequentially inside the active coroutine thread.
    """
    def __init__(self):
        self._handlers: Dict[str, List[Callable[[Event], Awaitable[None]]]] = {}

    def register(self, event_name: str, handler: Callable[[Event], Awaitable[None]]) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    async def dispatch(self, event: Event) -> None:
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(
                    f"Error executing handler '{handler.__name__}' for event '{event.name}': {e}",
                    exc_info=True
                )
