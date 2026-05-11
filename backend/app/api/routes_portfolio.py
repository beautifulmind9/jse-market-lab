from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.app.schemas.portfolio import PortfolioPlanRequest
from backend.app.services.portfolio_service import get_portfolio_plan

router = APIRouter(prefix="/api/portfolio")


@router.post("/plan")
def create_portfolio_plan(request: PortfolioPlanRequest) -> dict:
    try:
        return get_portfolio_plan(
            capital=request.capital,
            mode=request.mode,
            cost_profile=request.cost_profile,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
