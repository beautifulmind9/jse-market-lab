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
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"
    candidate_count = len(allocations)
    funded_trades = [trade for trade in allocations if float(trade.get("allocation_amount", 0.0) or 0.0) > 0]
    funded_count = len(funded_trades)
    strong_candidates = sum(1 for trade in allocations if _is_stronger_setup(trade))
    funded_strong = sum(1 for trade in funded_trades if _is_stronger_setup(trade))

    safe_capital = float(total_capital or 0.0)
    allocated_amount = round(
        sum(float(trade.get("allocation_amount", 0.0) or 0.0) for trade in allocations),
        2,
    )
    reserve_ratio = round((safe_capital - allocated_amount) / safe_capital, 4) if safe_capital > 0 else 0.0

    lines = [
        f"The system found {candidate_count} possible trade{'s' if candidate_count != 1 else ''}.",
        f"{funded_count} trade{'s' if funded_count != 1 else ''} were funded from this set.",
        _build_strength_line(
            funded_count=funded_count,
            strong_candidates=strong_candidates,
            funded_strong=funded_strong,
            mode=mode,
        ),
    ]
    confidence_line = _build_confidence_line(funded_trades=funded_trades, mode=mode)
    if confidence_line:
        lines.append(confidence_line)
    lines.append(_build_glossary_support_line(mode=mode))

    if reserve_ratio > 0:
        lines.append("Some cash is being held back intentionally when strong opportunities are limited.")
    else:
        lines.append("Most available cash is currently deployed across funded trades.")

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


def _build_strength_line(
    *,
    funded_count: int,
    strong_candidates: int,
    funded_strong: int,
    mode: str,
) -> str:
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"

    if funded_count <= 0:
        if analyst_mode:
            return "No trades were funded in the current portfolio, so no strong setups cleared funding conditions this round."
        return "No trades were funded right now because no strong setups cleared the funding rules."

    strong_ratio = funded_strong / funded_count
    if strong_ratio >= 0.6:
        if analyst_mode:
            return f"Current funded setup mix is strong: {funded_strong}/{funded_count} funded trades are Tier A or strong-confidence setups."
        return "Current funded setup mix is strong, with most funded trades in higher-quality setups."

    if strong_ratio >= 0.25:
        if analyst_mode:
            return f"Current funded setup mix is constructive but mixed: {funded_strong}/{funded_count} funded trades are stronger-quality and the rest are moderate quality."
        return "Current funded setup mix is mixed but still constructive."

    if strong_candidates > funded_strong:
        if analyst_mode:
            return "Current funded setup mix is cautious: fewer stronger-quality setups were funded while stronger candidates remained limited."
        return "Current funded setup mix is weaker and more cautious."

    if analyst_mode:
        return "Current funded setup mix is weaker overall, with mostly lower-quality funded setups."
    return "Current funded setup mix is weaker overall, so caution is higher."


def _build_confidence_line(*, funded_trades: Sequence[Mapping[str, Any]], mode: str) -> str | None:
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"
    total_funded = len(funded_trades)
    if total_funded == 0:
        return None

    labels = [str(trade.get("confidence_label", "")).strip().lower() for trade in funded_trades]
    high_count = sum(1 for label in labels if label in {"high", "strong"})
    medium_count = sum(1 for label in labels if label in {"medium", "moderate", "mixed"})
    low_count = sum(1 for label in labels if label in {"low", "weak", "high risk"})
    labeled_count = high_count + medium_count + low_count
    unknown_count = total_funded - labeled_count

    coverage_ratio = labeled_count / total_funded
    if coverage_ratio < 0.5:
        if analyst_mode:
            coverage_pct = round(coverage_ratio * 100)
            return (
                "Confidence detail is limited for this plan "
                f"(high: {high_count}, medium: {medium_count}, low: {low_count}, unknown: {unknown_count}; "
                f"coverage ~{coverage_pct}%)."
            )
        return "Confidence detail is limited for this plan."

    high_ratio = high_count / total_funded
    low_ratio = low_count / total_funded
    coverage_pct = round(coverage_ratio * 100)

    if high_ratio >= 0.6:
        if analyst_mode:
            return (
                "Current funded confidence mix is high/reliable in most rows "
                f"(high: {high_count}, medium: {medium_count}, low: {low_count}, unknown: {unknown_count}; "
                f"coverage ~{coverage_pct}%)."
            )
        return "Current funded confidence is mostly high and historically more reliable."

    if low_ratio >= 0.6:
        if analyst_mode:
            return (
                "Current funded confidence mix is low in most rows "
                f"(high: {high_count}, medium: {medium_count}, low: {low_count}, unknown: {unknown_count}; "
                f"coverage ~{coverage_pct}%)."
            )
        return "Current funded confidence is mostly low, so reliability is weaker."

    if analyst_mode:
        return (
            "Current funded confidence mix is medium/mixed "
            f"(high: {high_count}, medium: {medium_count}, low: {low_count}, unknown: {unknown_count}; "
            f"coverage ~{coverage_pct}%)."
        )
    return "Current funded confidence is mixed across the funded portfolio."


def _build_glossary_support_line(*, mode: str) -> str:
    strength_line = explain_strength("A", mode=mode)
    confidence_line = explain_confidence("high", mode=mode)
    return f"How to read setup strength and confidence: Example glossary only — {strength_line} {confidence_line}"
