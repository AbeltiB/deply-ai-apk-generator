"""In-memory cache manager used when Redis is unavailable."""
from __future__ import annotations

import fnmatch
import time
from typing import Any


class _InMemoryRedisClient:
    def __init__(self, store: dict[str, Any], expires: dict[str, float]) -> None:
        self._store = store
        self._expires = expires

    def _purge_if_expired(self, key: str) -> None:
        expiry = self._expires.get(key)
        if expiry is not None and expiry <= time.time():
            self._store.pop(key, None)
            self._expires.pop(key, None)

    async def scan(self, cursor: int = 0, match: str = "*", count: int = 100):
        keys = [k for k in list(self._store.keys()) if fnmatch.fnmatch(k, match)]
        for key in keys:
            self._purge_if_expired(key)
        keys = [k for k in keys if k in self._store]
        return 0, keys[:count]

    async def incr(self, key: str) -> int:
        self._purge_if_expired(key)
        value = int(self._store.get(key, 0)) + 1
        self._store[key] = value
        return value

    async def ttl(self, key: str) -> int:
        self._purge_if_expired(key)
        if key not in self._store:
            return -2
        expiry = self._expires.get(key)
        if expiry is None:
            return -1
        return max(int(expiry - time.time()), 0)

    async def expire(self, key: str, seconds: int) -> bool:
        if key not in self._store:
            return False
        self._expires[key] = time.time() + seconds
        return True


class CacheManager:
    def __init__(self) -> None:
        self._store: dict[str, Any] = {}
        self._expires: dict[str, float] = {}
        self.client = _InMemoryRedisClient(self._store, self._expires)
        self._connected = False

    def _purge_if_expired(self, key: str) -> None:
        expiry = self._expires.get(key)
        if expiry is not None and expiry <= time.time():
            self._store.pop(key, None)
            self._expires.pop(key, None)

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def get(self, key: str):
        self._purge_if_expired(key)
        return self._store.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None, expire: int | None = None) -> bool:
        self._store[key] = value
        ttl_seconds = ttl if ttl is not None else expire
        if ttl_seconds is not None:
            self._expires[key] = time.time() + ttl_seconds
        else:
            self._expires.pop(key, None)
        return True

    async def delete(self, key: str) -> bool:
        existed = key in self._store
        self._store.pop(key, None)
        self._expires.pop(key, None)
        return existed

    async def clear_pattern(self, pattern: str) -> int:
        keys = [k for k in list(self._store.keys()) if fnmatch.fnmatch(k, pattern)]
        for key in keys:
            await self.delete(key)
        return len(keys)


cache_manager = CacheManager()
