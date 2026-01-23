"""Earnings phase metrics."""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from app.events.earnings import PHASE_EVENT, PHASE_NON, PHASE_POST, PHASE_PRE

PHASE_LABELS = {PHASE_PRE, PHASE_EVENT, PHASE_POST, PHASE_NON}
PHASE_ALIASES = {
    "pre": PHASE_PRE,
    "reaction": PHASE_EVENT,
    "event": PHASE_EVENT,
    "post": PHASE_POST,
    "non": PHASE_NON,
}


def normalize_phase_label(label: object | None) -> str:
    """Normalize phase labels to match earnings tagging constants."""
    if label is None or pd.isna(label):
        return PHASE_NON
    normalized = PHASE_ALIASES.get(str(label).strip().lower())
    if normalized is None:
        raise ValueError(f"Unknown phase label: {label}")
    return normalized


def compute_phase_metrics(
    df: pd.DataFrame,
    group_cols: list[str],
    return_col: str,
) -> pd.DataFrame:
    """Compute grouped phase metrics and flag insufficient history."""
    metrics_df = df.copy()
    if "earnings_phase" in metrics_df.columns:
        metrics_df["earnings_phase"] = metrics_df["earnings_phase"].map(
            normalize_phase_label
        )

    grouped = metrics_df.groupby(group_cols)[return_col]
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


def lookup_phase_metrics(
    metrics: pd.DataFrame,
    instrument: str,
    phase: str,
    inst_col: str = "instrument",
    phase_col: str = "earnings_phase",
) -> pd.Series | None:
    """Lookup metrics for a single instrument-phase combination."""
    normalized_phase = normalize_phase_label(phase)
    match = metrics[
        (metrics[inst_col] == instrument) & (metrics[phase_col] == normalized_phase)
    ]
    if match.empty:
        return None
    return match.iloc[0]


def normalize_phase_labels(phases: Iterable[str]) -> list[str]:
    """Normalize a list of phase labels to the supported set."""
    return [normalize_phase_label(label) for label in phases]
