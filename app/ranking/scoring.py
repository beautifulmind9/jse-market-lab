"""Scoring utilities for ranking."""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd

from .normalize import percentile_normalize
from .turnover import turnover_rate


def compute_components(
    df_summary: pd.DataFrame,
    years: float,
) -> Tuple[pd.DataFrame, pd.Series]:
    """Compute normalized components and turnover."""
    df = df_summary.copy()
    df["R"] = percentile_normalize(df["median_net_return"])
    df["W"] = df["win_rate_net"]
    df["H"] = df["hit_rate_above_cost"]
    turnover = turnover_rate(df["n_trades"], years)
    df["T"] = percentile_normalize(turnover)
    return df, turnover


def score_window(
    df: pd.DataFrame,
    weights: Dict[str, float],
    window_emphasis: Dict[int, float],
) -> pd.DataFrame:
    """Compute weighted scores per instrument-window."""
    df = df.copy()
    df["score_base"] = (
        weights["R"] * df["R"]
        + weights["W"] * df["W"]
        + weights["H"] * df["H"]
        + weights["T"] * (1 - df["T"])
    )
    df["window_multiplier"] = df["holding_window"].map(window_emphasis).fillna(1.0)
    df["score_window"] = df["score_base"] * df["window_multiplier"]
    return df
