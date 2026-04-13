"""Shared shell helpers for the Streamlit app entrypoint."""

from __future__ import annotations

import re

import pandas as pd

from app.costs.engine import run_cost_engine

_HOLDING_WINDOW_PATTERN = re.compile(r"([+-]?\d+)")


def coerce_trade_rows_from_ranked(ranked_df: pd.DataFrame) -> list[dict]:
    """Build minimal planner trade rows from ranked outputs for UI wiring."""
    trade_rows: list[dict] = []
    for row in ranked_df.to_dict("records"):
        quality_tier = str(row.get("tier", "B") or "B")
        holding_window = _coerce_holding_window(
            row.get("holding_window"),
            row.get("best_window"),
            row.get("window"),
            row.get("holding_period"),
        )
        trade_rows.append(
            {
                "instrument": row.get("instrument", "Unknown"),
                "quality_tier": quality_tier,
                "liquidity_pass": True,
                "volatility_bucket": "medium",
                "earnings_warning_severity": "info",
                "confidence_label": "strong" if quality_tier.upper() == "A" else "moderate",
                "holding_window": holding_window,
            }
        )
    return trade_rows


def _coerce_holding_window(*values: object) -> int | None:
    for value in values:
        if value is None or isinstance(value, bool):
            continue
        if isinstance(value, int):
            if value > 0:
                return value
            continue
        if isinstance(value, float):
            if pd.isna(value) or not value.is_integer():
                continue
            integer_value = int(value)
            if integer_value > 0:
                return integer_value
            continue

        match = _HOLDING_WINDOW_PATTERN.search(str(value).strip())
        if match is None:
            continue
        try:
            parsed = int(match.group(1))
        except (TypeError, ValueError):
            continue
        if parsed > 0:
            return parsed
    return None


def build_analyst_dataset(canonical_df: pd.DataFrame, ranked_df: pd.DataFrame) -> pd.DataFrame:
    """Build a return-bearing dataset for Analyst Insights from existing demo outputs."""
    entries = canonical_df[["instrument", "date"]].rename(columns={"date": "entry_date"})
    trades_df, _, _, _ = run_cost_engine(
        df_prices=canonical_df,
        df_entries=entries,
    )

    if ranked_df.empty:
        return trades_df

    tier_lookup = ranked_df[["instrument", "tier"]].rename(columns={"tier": "quality_tier"})
    enriched = trades_df.merge(tier_lookup, on="instrument", how="left")
    return enriched
