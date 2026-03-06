"""Simple in-memory queue manager fallback."""
from __future__ import annotations

from collections import deque
from typing import Any


class QueueManager:
    def __init__(self) -> None:
        self._queue: deque[dict[str, Any]] = deque()
        self._connected = False

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def publish_response(self, payload: dict[str, Any]) -> bool:
        self._queue.append(payload)
        return True

    async def get_stats(self) -> dict[str, int | bool]:
        return {
            "connected": self._connected,
            "queued_messages": len(self._queue),
        }


queue_manager = QueueManager()
