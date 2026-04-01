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

    return "unfunded"


def explain_portfolio_decision(trade: Mapping[str, Any]) -> str:
    """Explain why a trade was funded or not funded using available planner fields."""
    status = classify_decision_status(trade)
    explicit_reason = resolve_explicit_reason(trade)

    if status == "funded":
        if explicit_reason:
            base_text = f"Funded. {explicit_reason}"
        else:
            allocation_pct = float(trade.get("allocation_pct", 0.0) or 0.0)
            base_text = f"Funded. Final allocation is {allocation_pct:.0%}."
        return _append_ranking_context(base_text, trade, status)

    if explicit_reason:
        base_text = f"Not funded. {explicit_reason}"
        return _append_ranking_context(base_text, trade, status)

    quality_tier = _token(trade.get("quality_tier")).upper()
    if quality_tier == "C":
        return "Not funded. Trade is not eligible because quality tier C is excluded by rule."

    if trade.get("liquidity_pass") is False:
        return "Not funded. Trade is not eligible because the liquidity screen failed."

    if status == "eligible but constrained":
        base_text = "Not funded. Trade was eligible, but portfolio constraints prevented funding."
        return _append_ranking_context(base_text, trade, status)

    severity = _token(trade.get("earnings_warning_severity"))
    volatility = _token(trade.get("volatility_bucket"))
    if severity == "high" or volatility == "high":
        return "Not funded. Trade remained eligible, but risk adjustments reduced allocation to zero."

    return _append_ranking_context(
        "Not funded. No explicit allocator reason was provided in this output.",
        trade,
        status,
    )


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
    funded_rank = _int_or_none(trade.get("funded_rank"))
    eligible = bool(trade.get("eligible_for_funding"))
    explicit_reason = _token(resolve_explicit_reason(trade))

    if status == "funded" and funded_rank is not None:
        if funded_rank == 1:
            return base_text + " Ranked #1 among eligible trades and selected as a top-ranked eligible trade."
        return (
            base_text
            + f" Ranked #{funded_rank} among funded positions and selected ahead of lower-priority eligible trades."
        )

    if status == "eligible but constrained" and rank is not None:
        if "max funded trades" in explicit_reason:
            return (
                base_text
                + f" Trade remained eligible at rank #{rank}, but funded slots were filled before this position."
            )
        if "max portfolio exposure" in explicit_reason:
            return (
                base_text
                + f" Trade remained eligible at rank #{rank}, but portfolio exposure was fully used before this position."
            )

    if status == "unfunded" and eligible and rank is not None:
        return base_text + f" Trade remained eligible but finished outside funded positions at rank #{rank}."

    return base_text


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
