from __future__ import annotations

from fastapi import APIRouter

from backend.app.services.data_service import get_data_status

router = APIRouter(prefix="/api/data")


@router.get("/status")
def read_data_status() -> dict:
    return get_data_status()
