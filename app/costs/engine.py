"""Net-of-cost performance engine."""

from __future__ import annotations

from typing import Iterable, Optional, Tuple

import pandas as pd

from .config import resolve_cost_config
from .net_returns import compute_trade_results


def _summarize_by_instrument_window(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            columns=[
                "instrument",
                "holding_window",
                "n_trades",
                "win_rate_net",
                "median_net_return",
                "median_gross_return",
                "avg_net_return",
                "cost_drag_median",
                "hit_rate_above_cost",
            ]
        )

    grouped = trades.groupby(["instrument", "holding_window"])
    summary = grouped.agg(
        n_trades=("net_return_pct", "size"),
        win_rate_net=("net_return_pct", lambda x: (x > 0).mean()),
        median_net_return=("net_return_pct", "median"),
        median_gross_return=("gross_return_pct", "median"),
        avg_net_return=("net_return_pct", "mean"),
        cost_drag_median=("cost_drag_pct", "median"),
        hit_rate_above_cost=(
            "gross_return_pct",
            lambda x: (x > trades.loc[x.index, "cost_drag_pct"]).mean(),
        ),
    )
    return summary.reset_index()


def _summarize_overall(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame(
            columns=[
                "holding_window",
                "n_trades",
                "win_rate_net",
                "median_net_return",
                "median_gross_return",
                "avg_net_return",
            ]
        )

    grouped = trades.groupby("holding_window")
    summary = grouped.agg(
        n_trades=("net_return_pct", "size"),
        win_rate_net=("net_return_pct", lambda x: (x > 0).mean()),
        median_net_return=("net_return_pct", "median"),
        median_gross_return=("gross_return_pct", "median"),
        avg_net_return=("net_return_pct", "mean"),
    )
    return summary.reset_index()


def run_cost_engine(
    df_prices: pd.DataFrame,
    df_entries: pd.DataFrame,
    holding_windows: Optional[Iterable[int]] = None,
    broker_profile: str = "Default",
    override_enabled: bool = False,
    broker_fee: Optional[float] = None,
    cess: Optional[float] = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Run the cost engine and return trades, summaries, and config."""
    windows = list(holding_windows or [5, 10, 20, 30])
    config = resolve_cost_config(
        broker_profile=broker_profile,
        override_enabled=override_enabled,
        broker_fee=broker_fee,
        cess=cess,
    )
    trades = compute_trade_results(
        df_prices=df_prices,
        df_entries=df_entries,
        holding_windows=windows,
        round_trip_cost_rate=config["round_trip_cost_rate"],
    )
    summary_instrument = _summarize_by_instrument_window(trades)
    summary_overall = _summarize_overall(trades)
    return trades, summary_instrument, summary_overall, config
