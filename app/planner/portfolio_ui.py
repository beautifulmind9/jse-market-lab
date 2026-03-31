"""Streamlit helpers for rendering a user-facing portfolio plan."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd

_ALLOCATOR_REASON_KEYS = ("allocator_reason", "allocation_reason", "reason")


def build_portfolio_summary(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
) -> dict[str, Any]:
    """Build top-line portfolio summary values from allocation rows."""
    safe_capital = float(total_capital or 0.0)
    total_allocated_amount = round(
        sum(float(trade.get("allocation_amount", 0.0) or 0.0) for trade in allocations),
        2,
    )
    total_allocated_pct = (
        round(total_allocated_amount / safe_capital, 4) if safe_capital > 0 else 0.0
    )
    cash_reserve_amount = round(safe_capital - total_allocated_amount, 2)
    cash_reserve_pct = (
        round(cash_reserve_amount / safe_capital, 4) if safe_capital > 0 else 0.0
    )
    funded_trade_count = sum(
        1 for trade in allocations if float(trade.get("allocation_amount", 0.0) or 0.0) > 0
    )

    return {
        "total_allocated_amount": total_allocated_amount,
        "total_allocated_pct": total_allocated_pct,
        "cash_reserve_amount": cash_reserve_amount,
        "cash_reserve_pct": cash_reserve_pct,
        "funded_trade_count": funded_trade_count,
    }


def split_trades_by_funding(
    allocations: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split allocations into funded and unfunded trades."""
    funded_trades: list[dict[str, Any]] = []
    unfunded_trades: list[dict[str, Any]] = []

    for trade in allocations:
        row = dict(trade)
        amount = float(row.get("allocation_amount", 0.0) or 0.0)
        if amount > 0:
            funded_trades.append(row)
        else:
            unfunded_trades.append(row)

    return funded_trades, unfunded_trades


def generate_funding_reason(trade: Mapping[str, Any]) -> str:
    """Generate a compact, user-facing funding reason label."""
    quality_tier = str(trade.get("quality_tier", "")).strip().upper()
    if quality_tier == "C":
        return "Not funded — Tier C"

    liquidity_pass = trade.get("liquidity_pass")
    if liquidity_pass is False:
        return "Not funded — Liquidity"

    severity = str(trade.get("earnings_warning_severity", "")).strip().lower()
    if severity == "high":
        return "Reduced allocation — Earnings risk"

    volatility_bucket = str(trade.get("volatility_bucket", "")).strip().lower()
    if volatility_bucket == "high":
        return "Reduced allocation — High volatility"

    return "Eligible — meets criteria"


def resolve_unfunded_reason(trade: Mapping[str, Any]) -> str:
    """Resolve unfunded reason preferring allocator output before UI fallback labels."""
    for key in _ALLOCATOR_REASON_KEYS:
        value = trade.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return generate_funding_reason(trade)


def render_portfolio_plan(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
    st_module=None,
) -> None:
    """Render portfolio summary, funded/unfunded tables, and constraints."""
    if st_module is None:
        import streamlit as st_module

    st_module.subheader("Portfolio Plan")

    if not allocations:
        st_module.info("Portfolio Plan unavailable: no allocation outputs were provided.")
        return

    summary = build_portfolio_summary(allocations, total_capital)
    funded_trades, unfunded_trades = split_trades_by_funding(allocations)

    st_module.markdown("#### Portfolio Summary")
    summary_df = pd.DataFrame(
        [
            {
                "Total Capital": float(total_capital or 0.0),
                "Allocated Amount": summary["total_allocated_amount"],
                "Allocated %": summary["total_allocated_pct"],
                "Cash Reserve Amount": summary["cash_reserve_amount"],
                "Cash Reserve %": summary["cash_reserve_pct"],
                "Funded Trades": summary["funded_trade_count"],
            }
        ]
    )
    st_module.dataframe(summary_df, use_container_width=True)

    st_module.markdown("#### Funded Trades")
    if funded_trades:
        funded_df = pd.DataFrame(
            [
                {
                    "Instrument": trade.get("instrument", "Unknown"),
                    "Quality Tier": trade.get("quality_tier", "N/A"),
                    "Confidence": trade.get("confidence_label", "N/A"),
                    "Allocation %": trade.get("allocation_pct", 0.0),
                    "Allocation Amount": trade.get("allocation_amount", 0.0),
                    "Funding Note": generate_funding_reason(trade),
                }
                for trade in funded_trades
            ]
        )
        st_module.dataframe(funded_df, use_container_width=True)
    else:
        st_module.info("No funded trades for the selected inputs.")

    st_module.markdown("#### Unfunded Trades")
    if unfunded_trades:
        unfunded_df = pd.DataFrame(
            [
                {
                    "Instrument": trade.get("instrument", "Unknown"),
                    "Quality Tier": trade.get("quality_tier", "N/A"),
                    "Confidence": trade.get("confidence_label", "N/A"),
                    "Reason": resolve_unfunded_reason(trade),
                }
                for trade in unfunded_trades
            ]
        )
        st_module.dataframe(unfunded_df, use_container_width=True)
    else:
        st_module.info("No unfunded trades for the selected inputs.")

    st_module.markdown("#### Constraints")
    st_module.markdown(
        "- Max portfolio exposure: 70%\n"
        "- Min cash reserve: 30%\n"
        "- Max funded trades: 3\n"
        "- Tier C and liquidity failures are not funded"
    )
