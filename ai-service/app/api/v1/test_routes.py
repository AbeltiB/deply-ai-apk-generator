"""Development-only helper routes."""
from fastapi import APIRouter

router = APIRouter(prefix="/test")


@router.get("/ping")
async def ping():
    return {"message": "pong"}
