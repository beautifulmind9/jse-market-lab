"""Planner earnings warning integration."""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from app.events.earnings import PHASE_NON, tag_earnings_phase
from app.planner.warnings import build_earnings_warning


def add_planner_earnings_warnings(
    planner_df: pd.DataFrame,
    prices_df: pd.DataFrame,
    events_df: pd.DataFrame,
    objective: str,
    inst_col: str = "instrument",
    entry_col: str = "entry_date",
    window_col: str = "holding_window",
) -> pd.DataFrame:
    """Attach earnings-aware warnings and phases to planner rows."""
    if planner_df.empty:
        result = planner_df.copy()
        for column in (
            "earnings_phase",
            "earnings_day_offset",
            "planned_exit_date",
            "exit_earnings_phase",
            "earnings_overlaps_window",
            "earnings_warning_title",
            "earnings_warning_body",
            "earnings_warning_severity",
        ):
            if column not in result.columns:
                result[column] = None
        return result

    calendar_df = _build_calendar_df(prices_df, inst_col)
    cal_tagged = tag_earnings_phase(
        calendar_df,
        events_df,
        date_col="date",
        inst_col=inst_col,
    )
    phase_map = {
        (row[inst_col], row["date"]): row["earnings_phase"]
        for _, row in cal_tagged.iterrows()
    }
    offset_map = {
        (row[inst_col], row["date"]): row["earnings_day_offset"]
        for _, row in cal_tagged.iterrows()
        if pd.notna(row["earnings_day_offset"])
    }

    planned_exit = _compute_planned_exit_dates(
        planner_df,
        prices_df,
        inst_col=inst_col,
        entry_col=entry_col,
        window_col=window_col,
    )

    combined = planned_exit.copy()
    combined[entry_col] = pd.to_datetime(combined[entry_col])
    combined["planned_exit_date"] = planned_exit["planned_exit_date"]
    combined["earnings_phase"] = combined.apply(
        lambda row: phase_map.get((row[inst_col], row[entry_col]), PHASE_NON),
        axis=1,
    )
    combined["earnings_day_offset"] = combined.apply(
        lambda row: offset_map.get((row[inst_col], row[entry_col])),
        axis=1,
    )
    combined["exit_earnings_phase"] = combined.apply(
        lambda row: phase_map.get(
            (row[inst_col], row["planned_exit_date"]), PHASE_NON
        ),
        axis=1,
    )

    combined["earnings_overlaps_window"] = (
        combined["earnings_phase"] != combined["exit_earnings_phase"]
    ) & (
        (combined["earnings_phase"] != PHASE_NON)
        | (combined["exit_earnings_phase"] != PHASE_NON)
    )

    warning_data = combined.apply(
        lambda row: build_earnings_warning(
            entry_phase=row["earnings_phase"],
            exit_phase=row["exit_earnings_phase"],
            entry_offset=row.get("earnings_day_offset"),
            overlaps=bool(row["earnings_overlaps_window"]),
            objective=objective,
        ),
        axis=1,
        result_type="expand",
    )
    warning_data = warning_data.rename(
        columns={
            "body": "earnings_warning_body",
            "severity": "earnings_warning_severity",
            "title": "earnings_warning_title",
        }
    )
    combined = pd.concat([combined, warning_data], axis=1)
    return combined


def _compute_planned_exit_dates(
    planner_df: pd.DataFrame,
    prices_df: pd.DataFrame,
    inst_col: str,
    entry_col: str,
    window_col: str,
) -> pd.DataFrame:
    result = planner_df.copy()
    result[entry_col] = pd.to_datetime(result[entry_col])
    prices = prices_df.copy()
    prices["date"] = pd.to_datetime(prices["date"])

    trading_days: Dict[str, pd.Index] = {}
    for instrument, group in prices.groupby(inst_col, sort=False):
        trading_days[instrument] = pd.Index(group["date"].sort_values().unique())

    planned_dates: list[Optional[pd.Timestamp]] = []
    for _, row in result.iterrows():
        instrument = row[inst_col]
        entry_date = row[entry_col]
        window = row[window_col]
        if pd.isna(entry_date) or pd.isna(window):
            planned_dates.append(pd.NaT)
            continue
        dates = trading_days.get(instrument)
        if dates is None or dates.empty:
            planned_dates.append(pd.NaT)
            continue
        try:
            entry_idx = int(dates.get_loc(entry_date))
        except KeyError:
            entry_idx = dates.get_indexer([entry_date], method="backfill")[0]
        if entry_idx < 0:
            planned_dates.append(pd.NaT)
            continue
        exit_idx = entry_idx + int(window)
        if exit_idx >= len(dates):
            planned_dates.append(pd.NaT)
            continue
        planned_dates.append(dates[exit_idx])

    result["planned_exit_date"] = planned_dates
    return result


def _build_calendar_df(
    prices_df: pd.DataFrame,
    inst_col: str,
) -> pd.DataFrame:
    if inst_col not in prices_df.columns:
        raise KeyError(f"prices_df must include {inst_col}")
    calendar_df = prices_df[[inst_col, "date"]].drop_duplicates().copy()
    calendar_df["date"] = pd.to_datetime(calendar_df["date"])
    calendar_df = calendar_df.sort_values([inst_col, "date"], kind="stable")
    return calendar_df

