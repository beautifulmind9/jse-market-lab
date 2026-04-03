"""Trade guidance interpretation layer for planner warnings."""

from __future__ import annotations

from typing import Any, Mapping, Optional

import numpy as np
import pandas as pd


SEVERITY_TYPES = {"info", "caution", "high"}


def _overlap_is_explicit_true(overlap_value: Any) -> bool:
    """Return True only for explicit boolean true values."""
    return isinstance(overlap_value, (bool, np.bool_)) and bool(overlap_value)


def _normalize_guidance_severity(raw_severity: Any) -> str:
    """Normalize incoming severity with safe fallback."""
    if raw_severity is None or pd.isna(raw_severity):
        return "info"
    severity = (
        raw_severity.strip().lower()
        if isinstance(raw_severity, str)
        else str(raw_severity).strip().lower()
    )
    if severity not in SEVERITY_TYPES:
        return "info"
    return severity


def generate_trade_guidance(trade_row: Mapping[str, Any]) -> Optional[dict]:
    """Return actionable guidance payload for a single trade row."""
    if not _overlap_is_explicit_true(trade_row.get("earnings_overlaps_window")):
        return None

    severity = _normalize_guidance_severity(trade_row.get("earnings_warning_severity"))
    holding_window = trade_row.get("holding_window")
    volatility_bucket = trade_row.get("volatility_bucket")

    volatility_hint_clear = (
        f" Current price movement level: {volatility_bucket}."
        if volatility_bucket is not None and not pd.isna(volatility_bucket)
        else ""
    )
    volatility_hint_pro = (
        f" Current volatility level: {volatility_bucket}."
        if volatility_bucket is not None and not pd.isna(volatility_bucket)
        else ""
    )
    window_hint_clear = (
        f" Your current plan is to hold for about {holding_window} trading days."
        if holding_window is not None and not pd.isna(holding_window)
        else ""
    )
    window_hint_pro = (
        f" Current holding period: {holding_window} trading days."
        if holding_window is not None and not pd.isna(holding_window)
        else ""
    )

    if severity == "high":
        return {
            "guidance_title": "High earnings overlap guidance",
            "guidance_body_clear": (
                "This trade runs into earnings, so price movement may be unpredictable."
            ),
            "guidance_body_pro": (
                "This trade runs into earnings, so price movement may be unpredictable."
            ),
            "guidance_type": "high",
        }
    if severity == "caution":
        return {
            "guidance_title": "Caution earnings overlap guidance",
            "guidance_body_clear": (
                "This trade runs into earnings, so price movement may be unpredictable."
            ),
            "guidance_body_pro": (
                "This trade runs into earnings, so price movement may be unpredictable."
            ),
            "guidance_type": "caution",
        }

    return {
        "guidance_title": "Earnings overlap awareness",
        "guidance_body_clear": (
            "This trade runs into earnings, so price movement may be unpredictable."
        ),
        "guidance_body_pro": (
            "This trade runs into earnings, so price movement may be unpredictable."
        ),
        "guidance_type": "info",
    }
