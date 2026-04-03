"""Trade confidence classification layer for planner rows."""

from __future__ import annotations

from typing import Any, Mapping


HIGH_VOLATILITY_BUCKET = "high"


def generate_trade_confidence(trade_row: Mapping[str, Any]) -> dict:
    """Return confidence payload for a single trade row.

    Classification order is deterministic and intentionally simple.
    """
    liquidity_pass = bool(trade_row.get("liquidity_pass"))
    severity = _normalize_token(trade_row.get("severity"))
    quality_tier = _normalize_token(trade_row.get("quality_tier")).upper()
    volatility_bucket = _normalize_token(trade_row.get("volatility_bucket"))

    if not liquidity_pass:
        confidence_level = "avoid"
    elif severity == "high":
        confidence_level = "high risk"
    elif quality_tier == "A" and volatility_bucket != HIGH_VOLATILITY_BUCKET:
        confidence_level = "strong"
    elif quality_tier in {"A", "B"}:
        confidence_level = "moderate"
    elif quality_tier == "C":
        confidence_level = "watch"
    else:
        confidence_level = "moderate"

    return _confidence_copy(confidence_level)


def _normalize_token(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _confidence_copy(confidence_level: str) -> dict:
    if confidence_level in {"avoid", "high risk", "watch"}:
        return {
            "confidence_label": "weak",
            "confidence_title": "Weak",
            "confidence_body_clear": "Weak — signals are not lining up well.",
            "confidence_body_pro": "Weak — signals are not lining up well.",
            "confidence_level": "weak",
        }

    if confidence_level == "strong":
        return {
            "confidence_label": "strong",
            "confidence_title": "Strong",
            "confidence_body_clear": "Strong — signals are lining up clearly.",
            "confidence_body_pro": "Strong — signals are lining up clearly.",
            "confidence_level": "strong",
        }

    return {
        "confidence_label": "moderate",
        "confidence_title": "Moderate",
        "confidence_body_clear": "Moderate — some signals are there, but not all.",
        "confidence_body_pro": "Moderate — some signals are there, but not all.",
        "confidence_level": "moderate",
    }
