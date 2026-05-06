from __future__ import annotations

from fastapi import APIRouter, Query

from backend.app.services.review_service import get_decision_audit

router = APIRouter(prefix="/api/review")


@router.get("/decision-audit")
def read_decision_audit(
    capital: float = Query(default=100_000.0, ge=0),
    mode: str = Query(default="guided"),
) -> dict:
    return get_decision_audit(capital=capital, mode=mode)
