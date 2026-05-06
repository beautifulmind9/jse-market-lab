from __future__ import annotations

from fastapi import APIRouter

from backend.app.schemas.portfolio import PortfolioPlanRequest
from backend.app.services.portfolio_service import get_portfolio_plan

router = APIRouter(prefix="/api/portfolio")


@router.post("/plan")
def create_portfolio_plan(request: PortfolioPlanRequest) -> dict:
    return get_portfolio_plan(capital=request.capital, mode=request.mode)
