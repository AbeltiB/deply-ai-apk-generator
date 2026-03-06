"""Minimal stats endpoints."""
from __future__ import annotations

import time
from fastapi import APIRouter

from app.core.cache import cache_manager
from app.core.messaging import queue_manager

router = APIRouter(prefix="/stats")
START_TIME = time.time()


@router.get("")
async def get_stats():
    return {
        "uptime_seconds": int(time.time() - START_TIME),
        "queue": await queue_manager.get_stats(),
        "cache_keys": len(cache_manager._store),
    }
