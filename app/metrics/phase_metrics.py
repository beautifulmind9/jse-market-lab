"""Earnings phase metrics."""

from __future__ import annotations

import pandas as pd


def compute_phase_metrics(
    df: pd.DataFrame,
    group_cols: list[str],
    return_col: str,
) -> pd.DataFrame:
    """Compute grouped phase metrics and flag insufficient history."""
    grouped = df.groupby(group_cols)[return_col]
    metrics = grouped.agg(
        n="size",
        win_rate=lambda x: (x > 0).mean(),
        median_return="median",
        p25=lambda x: x.quantile(0.25),
        p75=lambda x: x.quantile(0.75),
        vol="std",
    )
    metrics = metrics.reset_index()
    metrics["insufficient_history"] = metrics["n"] < 12
    return metrics
