"""No-op database manager for local development bootstrap."""
from __future__ import annotations

from typing import Any


class DatabaseManager:
    def __init__(self) -> None:
        self._connected = False

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def health(self) -> dict[str, Any]:
        return {"connected": self._connected, "backend": "in-memory-fallback"}

    async def save_project(self, *args, **kwargs) -> str:
        return "local-project"

    async def save_conversation(self, *args, **kwargs) -> str:
        return "local-conversation"

    async def get_conversation_history(self, *args, **kwargs) -> list[dict[str, Any]]:
        return []

    async def get_project(self, *args, **kwargs) -> dict[str, Any] | None:
        return None

    async def get_user_projects(self, *args, **kwargs) -> list[dict[str, Any]]:
        return []

    async def get_user_preferences(self, *args, **kwargs) -> dict[str, Any]:
        return {}


db_manager = DatabaseManager()
