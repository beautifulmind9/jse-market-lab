"""Shared backend context built from the existing JSE Market Lab engine."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import pandas as pd

from app.analysis.ticker_drilldown import build_ticker_drilldown
from app.analysis.ticker_intelligence import compute_ticker_metrics
from app.costs.profiles import DEFAULT_PROFILE_KEY
from app.data.ingest import ingest_dataset
from app.data.processor import canonicalize_symbol
from app.demo.run_demo import run_demo
from app.planner.allocation import generate_portfolio_allocation
from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked

from backend.app.core.config import DEFAULT_DATASET, normalize_mode


@lru_cache(maxsize=8)
def get_engine_context(cost_profile: str = DEFAULT_PROFILE_KEY) -> dict[str, Any]:
    """Load the canonical dataset and derived demo outputs by cost profile."""
    canonical_df, meta, issues = ingest_dataset(DEFAULT_DATASET)
    payload = run_demo(
        canonical_df=canonical_df,
        meta=meta,
        issues=issues,
        cost_profile=cost_profile,
    )
    ranked_df = payload.get("ranked", pd.DataFrame())
    analyst_df = build_analyst_dataset(canonical_df, ranked_df)
    trade_rows = coerce_trade_rows_from_ranked(ranked_df) if not ranked_df.empty else []
    return {
        "canonical_df": canonical_df,
        "meta": meta or {},
        "issues": issues or {},
        "cost_config": payload.get("cost_config", {}),
        "ranked_df": ranked_df,
        "analyst_df": analyst_df,
        "trade_rows": trade_rows,
    }


def build_allocation_payload(
    capital: float,
    mode: str | None,
    cost_profile: str = DEFAULT_PROFILE_KEY,
) -> dict[str, Any]:
    """Return allocations enriched with source trade rows."""
    context = get_engine_context(cost_profile)
    trade_rows = context["trade_rows"]
    allocation_payload = generate_portfolio_allocation(
        trade_rows,
        float(capital),
        mode=normalize_mode(mode),
    )
    allocations = allocation_payload.get("allocations", [])
    enriched = [{**row, **allocation} for row, allocation in zip(trade_rows, allocations)]
    return {
        "allocations": enriched,
        "allocation_summary": allocation_payload,
        "cost_config": context.get("cost_config", {}),
    }


def build_ticker_payload(ticker: str, mode: str | None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return existing ticker drilldown and intelligence payloads."""
    context = get_engine_context()
    normalized_ticker = canonicalize_symbol(str(ticker or "").strip())
    analyst_df = context["analyst_df"]
    return (
        build_ticker_drilldown(analyst_df, normalized_ticker),
        compute_ticker_metrics(analyst_df, normalized_ticker, mode=normalize_mode(mode)),
    )
