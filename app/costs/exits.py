"""Exit date computation utilities."""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd


def build_trading_calendar(df_prices: pd.DataFrame) -> Dict[str, List[pd.Timestamp]]:
    """Build per-instrument trading calendars from price data."""
    calendars: Dict[str, List[pd.Timestamp]] = {}
    grouped = df_prices.dropna(subset=["date"]).groupby("instrument")["date"]
    for instrument, dates in grouped:
        unique_dates = pd.to_datetime(dates).dropna().sort_values().unique()
        calendars[instrument] = list(unique_dates)
    return calendars


def compute_exit_date(
    calendar: Dict[str, List[pd.Timestamp]],
    instrument: str,
    entry_date: pd.Timestamp,
    holding_window: int,
) -> Optional[pd.Timestamp]:
    """Return the exit date N trading days after entry or None if unavailable."""
    dates = calendar.get(instrument, [])
    if not dates:
        return None
    try:
        entry_idx = dates.index(entry_date)
    except ValueError:
        return None
    exit_idx = entry_idx + holding_window
    if exit_idx >= len(dates):
        return None
    return dates[exit_idx]
