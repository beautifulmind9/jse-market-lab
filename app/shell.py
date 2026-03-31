"""Shared shell helpers for the Streamlit app entrypoint."""

from __future__ import annotations

import pandas as pd

from app.costs.engine import run_cost_engine


def coerce_trade_rows_from_ranked(ranked_df: pd.DataFrame) -> list[dict]:
    """Build minimal planner trade rows from ranked outputs for UI wiring."""
    trade_rows: list[dict] = []
    for row in ranked_df.to_dict("records"):
        quality_tier = str(row.get("tier", "B") or "B")
        trade_rows.append(
            {
                "instrument": row.get("instrument", "Unknown"),
                "quality_tier": quality_tier,
                "liquidity_pass": True,
                "volatility_bucket": "medium",
                "earnings_warning_severity": "info",
                "confidence_label": "strong" if quality_tier.upper() == "A" else "moderate",
            }
        )
    return trade_rows


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
