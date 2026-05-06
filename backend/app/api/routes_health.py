"""Health route."""

from __future__ import annotations

from fastapi import APIRouter

from backend.app.core.config import SERVICE_NAME

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    """Return API health status."""
    return {"status": "ok", "service": SERVICE_NAME}
