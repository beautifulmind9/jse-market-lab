"""Earnings event tagging."""

from __future__ import annotations

from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd


PHASE_PRE = "pre_earnings"
PHASE_EVENT = "earnings"
PHASE_POST = "post_earnings"

PRE_WINDOW = (-30, -1)
EVENT_WINDOW = (0, 3)
POST_WINDOW = (4, 30)


def tag_earnings_phase(
    df: pd.DataFrame,
    events_df: pd.DataFrame,
    date_col: str,
    inst_col: str,
) -> pd.DataFrame:
    """Tag rows with earnings phases using trading-day offsets."""
    tagged = df.copy()
    tagged[date_col] = pd.to_datetime(tagged[date_col])

    events = events_df.copy()
    if "earnings_date" not in events.columns:
        raise KeyError("events_df must include an earnings_date column")
    events["earnings_date"] = pd.to_datetime(events["earnings_date"])
    if "confidence" not in events.columns:
        events["confidence"] = "estimated"

    phase_values: Dict[Tuple[str, pd.Timestamp], str] = {}
    offset_values: Dict[Tuple[str, pd.Timestamp], int] = {}

    for instrument, group in tagged.groupby(inst_col, sort=False):
        dates = pd.Index(group[date_col].sort_values().unique())
        if dates.empty:
            continue

        event_rows = events[events[inst_col] == instrument]
        if event_rows.empty:
            continue

        event_indices = _event_indices(
            dates,
            event_rows["earnings_date"],
            event_rows["confidence"],
        )
        if not event_indices:
            continue

        offsets = _closest_offsets(len(dates), event_indices)
        phase_map = _phase_from_offsets(offsets)
        for idx, date in enumerate(dates):
            offset = offsets[idx]
            phase = phase_map[idx]
            if phase is None or offset is None:
                continue
            phase_values[(instrument, date)] = phase
            offset_values[(instrument, date)] = int(offset)

    tagged["earnings_phase"] = tagged.apply(
        lambda row: phase_values.get((row[inst_col], row[date_col])), axis=1
    )
    tagged["earnings_day_offset"] = tagged.apply(
        lambda row: offset_values.get((row[inst_col], row[date_col])), axis=1
    )

    return tagged


def _event_indices(
    dates: pd.Index,
    event_dates: Iterable[pd.Timestamp],
    confidences: Iterable[str],
) -> list[tuple[int, int]]:
    indices: list[tuple[int, int]] = []
    for event_date, confidence in zip(
        pd.to_datetime(list(event_dates)),
        list(confidences),
    ):
        position = dates.get_indexer([event_date])[0]
        if position >= 0:
            indices.append((int(position), _confidence_score(str(confidence))))
    return indices


def _closest_offsets(length: int, event_indices: Iterable[tuple[int, int]]) -> np.ndarray:
    index_values = np.arange(length)
    best_offsets = np.full(length, np.nan)
    best_abs = np.full(length, np.inf)
    best_confidence = np.full(length, -1)

    for event_index, confidence_score in event_indices:
        offsets = index_values - event_index
        within = (offsets >= PRE_WINDOW[0]) & (offsets <= POST_WINDOW[1])
        abs_offsets = np.abs(offsets)
        update = within & (
            (abs_offsets < best_abs)
            | ((abs_offsets == best_abs) & (confidence_score > best_confidence))
            | (
                (abs_offsets == best_abs)
                & (confidence_score == best_confidence)
                & (offsets < best_offsets)
            )
        )
        best_abs[update] = abs_offsets[update]
        best_confidence[update] = confidence_score
        best_offsets[update] = offsets[update]

    return best_offsets


def _phase_from_offsets(offsets: np.ndarray) -> list[str | None]:
    phases: list[str | None] = []
    for offset in offsets:
        if np.isnan(offset):
            phases.append(None)
            continue
        offset_int = int(offset)
        if PRE_WINDOW[0] <= offset_int <= PRE_WINDOW[1]:
            phases.append(PHASE_PRE)
        elif EVENT_WINDOW[0] <= offset_int <= EVENT_WINDOW[1]:
            phases.append(PHASE_EVENT)
        elif POST_WINDOW[0] <= offset_int <= POST_WINDOW[1]:
            phases.append(PHASE_POST)
        else:
            phases.append(None)
    return phases


def _confidence_score(confidence: str) -> int:
    if confidence.lower() == "confirmed":
        return 2
    if confidence.lower() == "estimated":
        return 1
    return 0
