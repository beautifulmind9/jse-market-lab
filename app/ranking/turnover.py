"""Turnover proxies for ranking."""

from __future__ import annotations

from typing import Optional

import pandas as pd


def dataset_years(start_date: pd.Timestamp, end_date: pd.Timestamp) -> float:
    """Compute dataset length in years."""
    delta_days = (end_date - start_date).days
    return max(delta_days / 365.25, 0.01)


def turnover_rate(n_trades: pd.Series, years: float) -> pd.Series:
    """Compute turnover rate from trades per year."""
    return n_trades / years
