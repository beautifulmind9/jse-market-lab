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

    quality_tier = _token(trade.get("quality_tier")).upper()
    if quality_tier == "C":
        return "not eligible"

    if trade.get("liquidity_pass") is False:
        return "not eligible"

    explicit_reason = _token(resolve_explicit_reason(trade))
    if any(
        marker in explicit_reason
        for marker in ("max funded trades", "max portfolio exposure", "constraint")
    ):
        return "eligible but constrained"

    return "unfunded"


def explain_portfolio_decision(trade: Mapping[str, Any]) -> str:
    """Explain why a trade was funded or not funded using available planner fields."""
    status = classify_decision_status(trade)
    explicit_reason = resolve_explicit_reason(trade)

    if status == "funded":
        if explicit_reason:
            return f"Funded. {explicit_reason}"
        allocation_pct = float(trade.get("allocation_pct", 0.0) or 0.0)
        return f"Funded. Final allocation is {allocation_pct:.0%}."

    if explicit_reason:
        return f"Not funded. {explicit_reason}"

    quality_tier = _token(trade.get("quality_tier")).upper()
    if quality_tier == "C":
        return "Not funded. Trade is not eligible because quality tier C is excluded by rule."

    if trade.get("liquidity_pass") is False:
        return "Not funded. Trade is not eligible because the liquidity screen failed."

    if status == "eligible but constrained":
        return "Not funded. Trade was eligible, but portfolio constraints prevented funding."

    severity = _token(trade.get("earnings_warning_severity"))
    volatility = _token(trade.get("volatility_bucket"))
    if severity == "high" or volatility == "high":
        return "Not funded. Trade remained eligible, but risk adjustments reduced allocation to zero."

    return "Not funded. No explicit allocator reason was provided in this output."


def explain_primary_rule_or_constraint(trade: Mapping[str, Any]) -> str:
    """Describe the main rule/constraint affecting the outcome."""
    explicit_reason = _token(resolve_explicit_reason(trade))

    if "max funded trades" in explicit_reason:
        return "Primary driver: max funded trades limit."
    if "max portfolio exposure" in explicit_reason:
        return "Primary driver: max portfolio exposure limit."
    if "constraint" in explicit_reason:
        return "Primary driver: portfolio constraint."

    quality_tier = _token(trade.get("quality_tier")).upper()
    if quality_tier == "C":
        return "Primary driver: quality tier C rule."
    if trade.get("liquidity_pass") is False:
        return "Primary driver: liquidity eligibility rule."

    severity = _token(trade.get("earnings_warning_severity"))
    volatility = _token(trade.get("volatility_bucket"))
    if severity == "high" or volatility == "high":
        return "Primary driver: risk adjustment factors."

    return "Primary driver: no explicit rule or constraint label available."


def _token(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()
