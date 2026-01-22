"""Trade-level net return computations."""

from __future__ import annotations

from typing import Iterable, List

import pandas as pd

from .exits import build_trading_calendar, compute_exit_date


def compute_trade_results(
    df_prices: pd.DataFrame,
    df_entries: pd.DataFrame,
    holding_windows: Iterable[int],
    round_trip_cost_rate: float,
) -> pd.DataFrame:
    """Compute trade-level returns for each entry across holding windows."""
    prices = df_prices.copy()
    prices["date"] = pd.to_datetime(prices["date"], errors="coerce")
    price_index = prices.set_index(["instrument", "date"])["close"]

    entries = df_entries.copy()
    entries["entry_date"] = pd.to_datetime(entries["entry_date"], errors="coerce")

    calendar = build_trading_calendar(prices)
    results: List[dict] = []

    for _, entry in entries.iterrows():
        instrument = entry["instrument"]
        entry_date = entry["entry_date"]
        if pd.isna(entry_date):
            continue
        entry_price = price_index.get((instrument, entry_date))
        if entry_price is None or pd.isna(entry_price):
            continue
        for window in holding_windows:
            exit_date = compute_exit_date(calendar, instrument, entry_date, window)
            if exit_date is None:
                continue
            exit_price = price_index.get((instrument, exit_date))
            if exit_price is None or pd.isna(exit_price):
                continue
            gross_return_pct = (exit_price / entry_price - 1) * 100
            cost_drag_pct = round_trip_cost_rate * 100
            net_return_pct = gross_return_pct - cost_drag_pct
            results.append(
                {
                    "instrument": instrument,
                    "entry_date": entry_date,
                    "exit_date": exit_date,
                    "entry_price": float(entry_price),
                    "exit_price": float(exit_price),
                    "holding_window": int(window),
                    "gross_return_pct": gross_return_pct,
                    "net_return_pct": net_return_pct,
                    "cost_drag_pct": cost_drag_pct,
                    "exit_reason": "Time Exit",
                }
            )

    return pd.DataFrame(results)
