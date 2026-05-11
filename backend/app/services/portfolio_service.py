"""Portfolio planning service for API responses."""

from __future__ import annotations

from typing import Any

from app.costs.profiles import get_cost_disclaimer, get_profile_metadata
from backend.app.core.config import DISCLAIMER, public_mode
from backend.app.services.engine_context import build_allocation_payload


def _format_holding_window(value: Any) -> str:
    if value in (None, ""):
        return ""
    value_text = str(value).strip()
    if value_text.upper().endswith("D"):
        return value_text.upper()
    return f"{value_text}D"


def _risk_flags(row: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if row.get("liquidity_pass") is False:
        flags.append("Liquidity failed")
    severity = str(row.get("earnings_warning_severity") or "").strip().lower()
    if severity and severity not in {"info", "none", "nan"}:
        flags.append(f"Earnings/event risk: {severity}")
    volatility = str(row.get("volatility_bucket") or "").strip().lower()
    if volatility == "high":
        flags.append("High volatility")
    return flags


def _trade_response(row: dict[str, Any], *, mode: str | None) -> dict[str, Any]:
    public = public_mode(mode)
    reason_key = "allocation_reason_pro" if public == "advanced" else "allocation_reason_clear"
    ticker = str(row.get("instrument") or row.get("ticker") or "").strip()
    allocation_pct = float(row.get("allocation_pct") or 0.0)
    return {
        "ticker": ticker,
        "company_name": str(row.get("company_name") or ""),
        "tier": str(row.get("quality_tier") or row.get("tier") or ""),
        "holding_window": _format_holding_window(row.get("holding_window")),
        "allocation_amount": float(row.get("allocation_amount") or 0.0),
        "allocation_pct": allocation_pct,
        "liquidity_status": "Passed" if row.get("liquidity_pass") is not False else "Failed",
        "risk_flags": _risk_flags(row),
        "reason": str(row.get(reason_key) or row.get("allocation_reason_clear") or ""),
        "net_pl_context": str(row.get("net_pl_context") or ""),
        "selection_rank": row.get("selection_rank"),
        "funded_rank": row.get("funded_rank"),
    }


def _cost_profile_payload(cost_profile: str | None) -> dict[str, Any]:
    profile = get_profile_metadata(cost_profile)
    return {
        "key": profile["key"],
        "label": profile["label"],
        "broker_fee": profile["broker_fee"],
        "cess": profile["cess"],
        "verification_status": profile["verification_status"],
        "source": profile["source"],
        "note": profile["note"],
        "disclaimer": get_cost_disclaimer(),
    }


def get_portfolio_plan(
    capital: float,
    mode: str | None = None,
    cost_profile: str | None = None,
) -> dict[str, Any]:
    """Return funded and unfunded portfolio plan data for the API."""
    safe_capital = max(float(capital or 0.0), 0.0)
    cost_profile_payload = _cost_profile_payload(cost_profile)
    payload = build_allocation_payload(safe_capital, mode, cost_profile_payload["key"])
    allocations = payload["allocations"]
    summary_payload = payload["allocation_summary"]

    funded = [_trade_response(row, mode=mode) for row in allocations if float(row.get("allocation_pct") or 0.0) > 0]
    unfunded = [_trade_response(row, mode=mode) for row in allocations if float(row.get("allocation_pct") or 0.0) <= 0]

    total_allocated = float(summary_payload.get("total_allocated_amount") or 0.0)
    reserve_cash = float(summary_payload.get("cash_reserve_amount") or max(safe_capital - total_allocated, 0.0))

    return {
        "capital": safe_capital,
        "mode": public_mode(mode),
        "cost_profile": cost_profile_payload,
        "funded_trades": funded,
        "unfunded_trades": unfunded,
        "reserve_cash": reserve_cash,
        "summary": {
            "funded_count": len(funded),
            "unfunded_count": len(unfunded),
            "total_allocated": total_allocated,
            "cash_reserve": reserve_cash,
        },
        "disclaimer": DISCLAIMER,
    }
