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
    """Classify funded/unfunded outcomes for explanation display labels."""
    allocation_amount = float(trade.get("allocation_amount", 0.0) or 0.0)
    if allocation_amount > 0:
        return "Selected"

    explicit_reason = _token(resolve_explicit_reason(trade))
    if _is_hard_stop(trade, explicit_reason):
        return "Not valid"

    if any(marker in explicit_reason for marker in _CONSTRAINT_MARKERS):
        return "Not funded (limit reached)"

    eligible_for_funding = trade.get("eligible_for_funding")
    if eligible_for_funding is False or any(
        marker in explicit_reason for marker in _REDUCED_TO_ZERO_MARKERS
    ):
        return "Not funded (cut to zero)"

    return "Not funded"


def explain_portfolio_decision(trade: Mapping[str, Any]) -> str:
    """Explain why a trade was funded or not funded using a single sentence."""
    status = classify_decision_status(trade)
    quality_tier = _token(trade.get("quality_tier")).upper()
    confidence = _token(trade.get("confidence_label"))
    base_text = "Not funded — this setup wasn’t strong enough."

    if status == "Selected":
        if quality_tier == "A" and confidence == "strong":
            base_text = "Selected — strong setup with good confirmation."
        elif quality_tier == "A" and confidence == "moderate":
            base_text = "Selected — solid setup with decent confirmation."
        elif quality_tier == "B":
            base_text = "Selected — decent setup but not the strongest."
        else:
            base_text = "Selected — smaller position due to relative strength."
    elif status == "Not funded (limit reached)":
        base_text = "Not funded — better trades already filled the slots."
    elif status == "Not valid":
        base_text = "Not funded — this setup didn’t meet the rules."
    elif status == "Not funded (cut to zero)":
        base_text = "Not funded — risk rules cut this position to zero."

    return _append_ranking_context(base_text, trade)


def explain_funded_trade_why(trade: Mapping[str, Any]) -> str:
    """Backward-compatible funded Why helper."""
    return explain_portfolio_decision(trade)


def explain_unfunded_trade_why(trade: Mapping[str, Any]) -> str:
    """Backward-compatible unfunded Why helper."""
    return explain_portfolio_decision(trade)


def explain_primary_rule_or_constraint(trade: Mapping[str, Any]) -> str:
    """Describe the main rule/constraint affecting the outcome."""
    explicit_reason = _token(resolve_explicit_reason(trade))

    if _is_hard_stop(trade, explicit_reason):
        return "Not funded — this setup didn’t meet the rules."
    if "max funded trades" in explicit_reason or "max portfolio exposure" in explicit_reason:
        return "Not funded — better trades already filled the slots."
    return "Not funded — this setup wasn’t strong enough."


def _append_ranking_context(base_text: str, trade: Mapping[str, Any]) -> str:
    rank = _int_or_none(trade.get("selection_rank"))
    if rank is None:
        return base_text
    return f"{base_text[:-1]}, ranked #{rank}." if base_text.endswith(".") else f"{base_text}, ranked #{rank}."


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
