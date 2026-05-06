"""Portfolio API request schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PortfolioPlanRequest(BaseModel):
    """Request body for portfolio planning."""

    capital: float = Field(default=100_000.0, ge=0)
    mode: str = "guided"
