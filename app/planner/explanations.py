"""Plain-language explanation helpers for portfolio funding decisions."""

from __future__ import annotations

from typing import Any, Mapping

REASON_KEYS = (
    "allocation_reason_clear",
    "allocation_reason_pro",
    "allocator_reason",
    "allocation_reason",
    "reason",
)

_HARD_STOP_MARKERS = (
    "tier c",
    "quality tier c",
    "low tier",
    "liquidity",
    "not eligible",
    "ineligible",
    "hard rule",
    "hard-stop",
)

_CONSTRAINT_MARKERS = (
    "max funded trades",
    "max portfolio exposure",
    "capacity",
)

_REDUCED_TO_ZERO_MARKERS = (
    "pre-constraints reduced allocation to zero",
    "reduced allocation to zero",
)

_STATUS_WHY_TEXT = {
    "funded": "Selected — one of the strongest setups right now.",
    "eligible but constrained": "Not funded — better trades already used up the available slots.",
    "not eligible": "Not funded — this setup didn’t meet the rules.",
    "reduced to zero": "Not funded — risk rules cut this position to zero.",
    "unfunded": "Not funded — this setup wasn’t strong enough.",
}


def resolve_explicit_reason(trade: Mapping[str, Any]) -> str:
    """Return allocator-provided reason text using priority order."""
    for key in REASON_KEYS:
        value = trade.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def classify_decision_status(trade: Mapping[str, Any]) -> str:
    """Classify funded/unfunded outcomes for explanation display."""
    allocation_amount = float(trade.get("allocation_amount", 0.0) or 0.0)
    if allocation_amount > 0:
        return "funded"

    explicit_reason = _token(resolve_explicit_reason(trade))
    if _is_hard_stop(trade, explicit_reason):
        return "not eligible"

    if any(marker in explicit_reason for marker in _CONSTRAINT_MARKERS):
        return "eligible but constrained"

    eligible_for_funding = trade.get("eligible_for_funding")
    if eligible_for_funding is False or any(
        marker in explicit_reason for marker in _REDUCED_TO_ZERO_MARKERS
    ):
        return "reduced to zero"

    return "unfunded"


def explain_portfolio_decision(trade: Mapping[str, Any]) -> str:
    """Return one short plain-language sentence for portfolio plan rows."""
    status = classify_decision_status(trade)
    base_text = _STATUS_WHY_TEXT.get(status, _STATUS_WHY_TEXT["unfunded"])
    return _append_rank(base_text, trade)


def _append_rank(base_text: str, trade: Mapping[str, Any]) -> str:
    rank = _int_or_none(trade.get("selection_rank"))
    if rank is None:
        rank = _int_or_none(trade.get("funded_rank"))
    if rank is None:
        return base_text

    sentence = base_text if base_text.endswith(".") else f"{base_text}."
    return f"{sentence} Ranked #{rank}"


def _is_hard_stop(trade: Mapping[str, Any], explicit_reason: str) -> bool:
    quality_tier = _token(trade.get("quality_tier")).upper()
    if quality_tier == "C":
        return True
    if trade.get("liquidity_pass") is False:
        return True
    return any(marker in explicit_reason for marker in _HARD_STOP_MARKERS)


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _token(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()
