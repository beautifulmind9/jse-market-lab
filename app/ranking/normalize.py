"""Normalization helpers for ranking."""

from __future__ import annotations

import pandas as pd


def percentile_normalize(values: pd.Series) -> pd.Series:
    """Return percentile ranks scaled to 0-1."""
    if values.empty:
        return values
    return values.rank(pct=True).fillna(0.0)
