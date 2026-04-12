"""Interpretation-first helpers for portfolio snapshot and reserved cash language."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.language.formatter import explain_confidence, explain_strength


def build_portfolio_snapshot(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
    *,
    mode: str = "beginner",
) -> dict[str, Any]:
    """Build concise snapshot copy shown before detailed portfolio tables."""
    candidate_count = len(allocations)
    funded_count = sum(
        1 for trade in allocations if float(trade.get("allocation_amount", 0.0) or 0.0) > 0
    )
    strong_candidates = sum(1 for trade in allocations if _is_stronger_setup(trade))
    funded_strong = sum(
        1
        for trade in allocations
        if float(trade.get("allocation_amount", 0.0) or 0.0) > 0 and _is_stronger_setup(trade)
    )

    safe_capital = float(total_capital or 0.0)
    allocated_amount = round(
        sum(float(trade.get("allocation_amount", 0.0) or 0.0) for trade in allocations),
        2,
    )
    reserve_ratio = round((safe_capital - allocated_amount) / safe_capital, 4) if safe_capital > 0 else 0.0

    lines = [
        f"The system found {candidate_count} possible trade{'s' if candidate_count != 1 else ''}.",
        f"{funded_count} trade{'s' if funded_count != 1 else ''} were funded from this set.",
        _build_strength_line(funded_count=funded_count, strong_candidates=strong_candidates, funded_strong=funded_strong),
    ]
    lines.append(_build_translation_support_line(mode=mode))

    if reserve_ratio > 0:
        lines.append("Some cash is being held back intentionally when strong opportunities are limited.")
    else:
        lines.append("Most available cash is currently deployed across funded trades.")

    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"
    if analyst_mode:
        lines.append(
            f"Context: funded {funded_count}/{candidate_count}; reserve ratio {reserve_ratio:.0%}."
        )

    return {
        "title": "Portfolio Snapshot",
        "lines": lines,
        "candidate_count": candidate_count,
        "funded_count": funded_count,
        "reserve_ratio": reserve_ratio,
        "strong_candidates": strong_candidates,
        "funded_strong": funded_strong,
    }


def build_reserved_cash_explanation(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
    *,
    mode: str = "beginner",
) -> dict[str, Any]:
    """Explain why portfolio cash may remain unallocated."""
    safe_capital = float(total_capital or 0.0)
    funded_count = sum(
        1 for trade in allocations if float(trade.get("allocation_amount", 0.0) or 0.0) > 0
    )
    unfunded_count = max(len(allocations) - funded_count, 0)
    allocated_amount = round(
        sum(float(trade.get("allocation_amount", 0.0) or 0.0) for trade in allocations),
        2,
    )
    reserve_amount = round(safe_capital - allocated_amount, 2)
    reserve_ratio = round(reserve_amount / safe_capital, 4) if safe_capital > 0 else 0.0

    if reserve_ratio <= 0:
        reason = "Little or no cash is reserved because available capital is already allocated."
    elif funded_count == 0 and len(allocations) > 0:
        reason = "Cash is being held back because current setups did not clear funding conditions."
    elif reserve_ratio >= 0.4 and unfunded_count > 0:
        reason = "Cash is reserved because stronger risk controls are active while market conditions are mixed."
    elif unfunded_count > 0:
        reason = "Cash is being held back because only part of the candidate list met stronger setup conditions."
    else:
        reason = "Cash remains reserved to avoid forcing trades when high-quality opportunities are limited."

    lines = [reason]
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"
    if analyst_mode and reserve_ratio > 0:
        lines.append(
            f"Reserve context: {reserve_ratio:.0%} unallocated ({reserve_amount:,.2f}) with {funded_count} funded and {unfunded_count} unfunded."
        )

    return {
        "title": "Why cash is reserved",
        "lines": lines,
        "reserve_ratio": reserve_ratio,
        "reserve_amount": reserve_amount,
        "funded_count": funded_count,
        "unfunded_count": unfunded_count,
    }


def _is_stronger_setup(trade: Mapping[str, Any]) -> bool:
    tier = str(trade.get("quality_tier", "")).strip().upper()
    confidence = str(trade.get("confidence_label", "")).strip().lower()
    return tier == "A" or confidence == "strong"


def _build_strength_line(*, funded_count: int, strong_candidates: int, funded_strong: int) -> str:
    if funded_count <= 0:
        return "No setups were funded, so stronger-priority filters are blocking this round."
    if funded_strong == funded_count and funded_count > 0:
        return "Funded trades are dominated by stronger setups."
    if strong_candidates > funded_strong:
        return "Stronger setups are being prioritized, with some lower-strength trades left unfunded."
    return "Setup strength is mixed across funded trades in this run."


def _build_translation_support_line(*, mode: str) -> str:
    strength_line = explain_strength("A", mode=mode)
    confidence_line = explain_confidence("high", mode=mode)
    return f"{strength_line} {confidence_line}"
