"""Helpers for converting backend-oriented labels into user-facing labels."""

from __future__ import annotations

import re
from typing import Any

import pandas as pd

_LABEL_OVERRIDES = {
    "avg_return": "Average Return",
    "median_return": "Median Return",
    "net_return_pct": "Net Return",
    "return_pct": "Return",
    "win_rate": "Win Rate",
    "n_trades": "Trades",
    "quality_tier": "Quality Tier",
    "holding_window": "Holding Window",
    "exit_reason": "Exit Reason",
    "vol_bucket": "Volatility Bucket",
    "stale_5d": "Stale 5D",
}


def display_label(raw_label: Any) -> str:
    """Convert common raw labels (snake_case) into cleaned UI labels."""
    if raw_label is None:
        return ""

    token = str(raw_label).strip()
    if token == "":
        return ""

    lowered = token.lower()
    if lowered in _LABEL_OVERRIDES:
        return _LABEL_OVERRIDES[lowered]

    spaced = re.sub(r"_+", " ", token)
    words = [word for word in spaced.split(" ") if word]
    return " ".join(_title_word(word) for word in words)


def display_value(raw_value: Any) -> Any:
    """Clean a scalar value when it is a snake_case status label."""
    if not isinstance(raw_value, str):
        return raw_value
    token = raw_value.strip()
    if token == "" or "_" not in token:
        return raw_value
    return display_label(token)


def clean_dataframe_labels(
    df: pd.DataFrame,
    *,
    value_columns: list[str] | None = None,
) -> pd.DataFrame:
    """Return a copy of ``df`` with cleaned column headers and optional value labels."""
    renamed = df.rename(columns={column: display_label(column) for column in df.columns})

    if not value_columns:
        return renamed

    output = renamed.copy()
    for column in value_columns:
        cleaned_column = display_label(column)
        if cleaned_column in output.columns:
            output[cleaned_column] = output[cleaned_column].map(display_value)
    return output


def _title_word(word: str) -> str:
    lower = word.lower()
    if lower.endswith("d") and lower[:-1].isdigit():
        return lower.upper()
    if lower in {"id", "pct"}:
        return lower.upper()
    return lower.capitalize()
