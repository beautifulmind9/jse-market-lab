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
    if confidence_level == "avoid":
        return {
            "confidence_label": "avoid",
            "confidence_title": "Avoid this setup",
            "confidence_body_clear": (
                "Liquidity did not pass, so entering this trade can be hard and riskier. "
                "Prioritize better-liquid setups first."
            ),
            "confidence_body_pro": (
                "Liquidity screen failed. Execution quality and slippage risk are elevated; "
                "deprioritize this setup."
            ),
            "confidence_level": "avoid",
        }

    if confidence_level == "high risk":
        return {
            "confidence_label": "high risk",
            "confidence_title": "High-risk setup",
            "confidence_body_clear": (
                "Warning severity is high, so this trade has elevated uncertainty. "
                "Use extra caution or reduce size."
            ),
            "confidence_body_pro": (
                "High severity context implies elevated event risk. Consider reduced exposure "
                "or waiting for cleaner conditions."
            ),
            "confidence_level": "high risk",
        }

    if confidence_level == "strong":
        return {
            "confidence_label": "strong",
            "confidence_title": "Strong confidence",
            "confidence_body_clear": (
                "Top quality tier with non-high volatility supports a stronger setup."
            ),
            "confidence_body_pro": (
                "Tier A quality with contained volatility supports higher relative confidence."
            ),
            "confidence_level": "strong",
        }

    if confidence_level == "watch":
        return {
            "confidence_label": "watch",
            "confidence_title": "Watch closely",
            "confidence_body_clear": (
                "Tier C quality suggests this trade needs monitoring before committing more capital."
            ),
            "confidence_body_pro": (
                "Tier C profile indicates lower conviction; keep on watchlist unless other factors improve."
            ),
            "confidence_level": "watch",
        }

    return {
        "confidence_label": "moderate",
        "confidence_title": "Moderate confidence",
        "confidence_body_clear": (
            "This setup is usable but not top-priority. Consider balanced sizing."
        ),
        "confidence_body_pro": (
            "Signal quality is acceptable but not elite; maintain standard risk controls."
        ),
        "confidence_level": "moderate",
    }
