from __future__ import annotations

from fastapi import APIRouter, Query

from backend.app.services.ticker_service import get_ticker_analysis

router = APIRouter(prefix="/api/ticker")


@router.get("/{ticker}/analysis")
def read_ticker_analysis(ticker: str, mode: str = Query(default="guided")) -> dict:
    return get_ticker_analysis(ticker=ticker, mode=mode)
