"""Health endpoints."""
from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter

from app.core.cache import cache_manager
from app.core.database import db_manager
from app.core.messaging import queue_manager

router = APIRouter(prefix="/health")


@router.get("/live")
async def liveness():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/ready")
async def readiness():
    return {
        "status": "ready",
        "cache": "ok" if cache_manager is not None else "missing",
        "queue": await queue_manager.get_stats(),
        "database": await db_manager.health(),
    }


@router.get("/full")
async def full_health():
    return {
        "service": "ai-service",
        "liveness": await liveness(),
        "readiness": await readiness(),
    }
