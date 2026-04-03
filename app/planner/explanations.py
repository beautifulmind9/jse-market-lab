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



def explain_funded_trade_why(
    trade: Mapping[str, Any],
    *,
    include_rank: bool = True,
) -> str:
    """Return a short, user-first reason for funded rows."""
    base = _funded_base_message(trade)

    if not include_rank:
        return base

    rank = _int_or_none(trade.get("selection_rank"))
    if rank is None:
        return base
    trimmed = base[:-1] if base.endswith(".") else base
    return f"{trimmed}, ranked #{rank}."


def explain_primary_rule_or_constraint(trade: Mapping[str, Any]) -> str:
    """Describe the main rule/constraint affecting the outcome."""
    explicit_reason = _token(resolve_explicit_reason(trade))

    if _is_hard_stop(trade, explicit_reason):
        quality_tier = _token(trade.get("quality_tier")).upper()
        if quality_tier == "C" or "tier c" in explicit_reason:
            return "Primary driver: quality tier C rule."
        if trade.get("liquidity_pass") is False or "liquidity" in explicit_reason:
            return "Primary driver: liquidity eligibility rule."
        return "Primary driver: eligibility hard-stop rule."

    if "max funded trades" in explicit_reason:
        return "Primary driver: max funded trades limit."
    if "max portfolio exposure" in explicit_reason:
        return "Primary driver: max portfolio exposure limit."
    if "capacity" in explicit_reason:
        return "Primary driver: portfolio constraint."

    severity = _token(trade.get("earnings_warning_severity"))
    volatility = _token(trade.get("volatility_bucket"))
    if severity == "high" or volatility == "high":
        return "Primary driver: risk adjustment factors."

    return "Primary driver: no explicit rule or constraint label available."


def _append_ranking_context(base_text: str, trade: Mapping[str, Any], status: str) -> str:
    rank = _int_or_none(trade.get("selection_rank"))
    if rank is None:
        rank = _int_or_none(trade.get("funded_rank"))
    if rank is None:
        return base_text

    sentence = base_text if base_text.endswith(".") else f"{base_text}."
    return f"{sentence} Ranked #{rank}"


def _funded_base_message(trade: Mapping[str, Any]) -> str:
    if _is_lower_allocation_vs_peers(trade):
        return "Selected — smaller position due to relative strength."

    quality_tier = _token(trade.get("quality_tier")).upper()
    confidence = _token(trade.get("confidence_label"))

    if quality_tier == "A" and confidence == "strong":
        return "Selected — strong setup with good confirmation."
    if quality_tier == "A" and confidence == "moderate":
        return "Selected — solid setup with decent confirmation."
    if quality_tier == "B":
        return "Selected — decent setup but not the strongest."
    return "Selected — setup met the bar for funding."


def _is_lower_allocation_vs_peers(trade: Mapping[str, Any]) -> bool:
    if bool(trade.get("lower_allocation_vs_peers")):
        return True

    explicit_reason = _token(resolve_explicit_reason(trade))
    markers = (
        "relative strength",
        "smaller position",
        "smaller size",
        "reduced size",
        "below base",
    )
    return any(marker in explicit_reason for marker in markers)


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
