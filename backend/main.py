from __future__ import annotations

from fastapi import FastAPI

from backend.app.api.routes_data import router as data_router
from backend.app.api.routes_health import router as health_router
from backend.app.api.routes_portfolio import router as portfolio_router
from backend.app.api.routes_review import router as review_router
from backend.app.api.routes_ticker import router as ticker_router
from backend.app.core.config import SERVICE_NAME

app = FastAPI(title="JSE Market Lab API", version="0.1.0")

app.include_router(health_router)
app.include_router(data_router)
app.include_router(portfolio_router)
app.include_router(ticker_router)
app.include_router(review_router)


@app.get("/")
def root() -> dict[str, str]:
    return {"service": SERVICE_NAME, "status": "ok"}
