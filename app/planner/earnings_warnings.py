"""Planner earnings warning integration."""

from __future__ import annotations

from typing import Dict, Optional

import pandas as pd

from app.events.earnings import PHASE_NON, tag_earnings_phase


PHASES = {"pre", "reaction", "post", PHASE_NON}


INCOME_STABILITY_COPY = {
    "pre": {
        "title": "⚠️ Earnings upcoming",
        "body": (
            "Earnings in {days} trading days... Consider smaller size or "
            "allowing more time for the trade."
        ),
        "severity": "caution",
    },
    "reaction": {
        "title": "⚠️ Earnings reaction period",
        "body": "Earnings reactions can increase volatility.",
        "severity": "caution",
    },
    "post": {
        "title": "ℹ️ Post-earnings window",
        "body": "Post-earnings prices may still be stabilizing.",
        "severity": "info",
    },
}

ACTIVE_GROWTH_COPY = {
    "pre": {
        "title": "⚠️ Earnings upcoming",
        "body": "Earnings reactions can drive outsized volatility.",
        "severity": "caution",
    },
    "reaction": {
        "title": "⚠️ Earnings reaction period",
        "body": "Expect wider variance around earnings reactions.",
        "severity": "caution",
    },
    "post": {
        "title": "ℹ️ Post-earnings window",
        "body": "Watch for post-earnings follow-through.",
        "severity": "info",
    },
}

CAPITAL_PRESERVATION_COPY = {
    "pre": {
        "title": "⚠️ Earnings upcoming",
        "body": "Earnings windows can amplify downside gaps.",
        "severity": "caution",
    },
    "reaction": {
        "title": "⚠️ Earnings reaction period",
        "body": "Earnings reactions can elevate downside risk.",
        "severity": "caution",
    },
    "post": {
        "title": "ℹ️ Post-earnings window",
        "body": "Post-earnings pricing can still settle.",
        "severity": "info",
    },
}


OBJECTIVE_COPY: Dict[str, Dict[str, Dict[str, str]]] = {
    "income_stability": INCOME_STABILITY_COPY,
    "active_growth": ACTIVE_GROWTH_COPY,
    "capital_preservation": CAPITAL_PRESERVATION_COPY,
}


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

    if objective not in OBJECTIVE_COPY:
        raise ValueError(f"Unknown objective: {objective}")

    planned_exit = _compute_planned_exit_dates(
        planner_df,
        prices_df,
        inst_col=inst_col,
        entry_col=entry_col,
        window_col=window_col,
    )

    tagged = tag_earnings_phase(
        planned_exit,
        events_df,
        date_col=entry_col,
        inst_col=inst_col,
    )

    combined = tagged.copy()
    combined["planned_exit_date"] = planned_exit["planned_exit_date"]
    exit_phase = pd.Series(PHASE_NON, index=combined.index)
    valid_exit = combined["planned_exit_date"].notna()
    if valid_exit.any():
        exit_tagged = tag_earnings_phase(
            planned_exit.loc[valid_exit],
            events_df,
            date_col="planned_exit_date",
            inst_col=inst_col,
        )
        exit_phase.loc[valid_exit] = exit_tagged["earnings_phase"].fillna(PHASE_NON)
    combined["exit_earnings_phase"] = exit_phase.replace({None: PHASE_NON})
    combined["earnings_phase"] = combined["earnings_phase"].fillna(PHASE_NON)
    combined["earnings_phase"] = combined["earnings_phase"].replace({None: PHASE_NON})

    combined["earnings_overlaps_window"] = (
        combined["earnings_phase"] != combined["exit_earnings_phase"]
    ) & (
        (combined["earnings_phase"] != PHASE_NON)
        | (combined["exit_earnings_phase"] != PHASE_NON)
    )

    copy_map = OBJECTIVE_COPY[objective]
    warning_data = combined.apply(
        lambda row: _warning_for_row(row, copy_map),
        axis=1,
        result_type="expand",
    )
    warning_data.columns = [
        "earnings_warning_title",
        "earnings_warning_body",
        "earnings_warning_severity",
    ]
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


def _warning_for_row(row: pd.Series, copy_map: Dict[str, Dict[str, str]]):
    phase = row["earnings_phase"]
    if phase not in PHASES:
        phase = PHASE_NON
    if phase == PHASE_NON:
        return pd.Series([None, None, None])

    copy = copy_map.get(phase)
    if not copy:
        return pd.Series([None, None, None])

    title = copy.get("title")
    body = copy.get("body")
    severity = copy.get("severity")

    if phase == "pre" and body:
        offset = row.get("earnings_day_offset")
        if pd.notna(offset):
            body = body.format(days=abs(int(offset)))
        else:
            body = body.replace("{days} ", "").replace("{days}", "")

    if row.get("earnings_overlaps_window") and body:
        body = f"{body}\nThis trade overlaps an earnings window."

    return pd.Series([title, body, severity])
