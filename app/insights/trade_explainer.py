"""Trade-level explanation helpers for funded and unfunded portfolio rows."""

from __future__ import annotations

from typing import Any, Mapping

from app.planner.explanations import classify_decision_status


def explain_trade_reason(row: Mapping[str, Any], mode: str = "beginner") -> str:
    """Explain why a funded trade appears in the portfolio table."""
    analyst_mode = _is_analyst(mode)

    reasons: list[str] = []
    reasons.append(_funded_base_line(row, analyst_mode=analyst_mode))

    support = _support_context(row, analyst_mode=analyst_mode)
    if support:
        reasons.append(support)

    ranking = _ranking_context(row, funded=True, analyst_mode=analyst_mode)
    if ranking:
        reasons.append(ranking)

    return " ".join(reasons).strip()


def explain_unfunded_reason(row: Mapping[str, Any], mode: str = "beginner") -> str:
    """Explain why an unfunded trade was held out of the portfolio."""
    analyst_mode = _is_analyst(mode)
    decision_status = classify_decision_status(row)

    reasons: list[str] = []
    reasons.append(_unfunded_base_line(row, decision_status=decision_status, analyst_mode=analyst_mode))

    ranking = _ranking_context(row, funded=False, analyst_mode=analyst_mode)
    if ranking:
        reasons.append(ranking)

    support = _support_context(row, analyst_mode=analyst_mode)
    if support:
        reasons.append(support)

    return " ".join(reasons).strip()


def _funded_base_line(row: Mapping[str, Any], *, analyst_mode: bool) -> str:
    tier = _token(row.get("quality_tier")).upper()
    confidence = _token(row.get("confidence_label"))

    if tier == "A" and confidence == "strong":
        return "Selected because this setup ranked as a top-quality, high-confidence candidate."
    if tier == "A":
        return "Selected because this setup met strong quality conditions and stayed eligible for funding."
    if tier == "B":
        if analyst_mode:
            return "Selected because this setup remained competitive after risk controls were applied."
        return "Selected because this setup stayed competitive even though stronger options were limited."
    return "Selected because this setup remained eligible and ranked ahead of other available candidates."


def _unfunded_base_line(
    row: Mapping[str, Any],
    *,
    decision_status: str,
    analyst_mode: bool,
) -> str:
    if decision_status == "Not valid":
        return "Not funded because this setup did not pass required quality or liquidity rules."
    if decision_status == "Not funded (limit reached)":
        return "Not funded because available capital was reserved for stronger competing trades."
    if decision_status == "Not funded (cut to zero)":
        return "Not funded because risk controls reduced the final allocation to zero."

    tier = _token(row.get("quality_tier")).upper()
    if tier == "B":
        return "Not funded because this setup was weaker than funded alternatives in the same pass."
    if analyst_mode:
        return "Not funded because this candidate ranked below funded peers after constraints."
    return "Not funded because this setup ranked below stronger available trades."


def _support_context(row: Mapping[str, Any], *, analyst_mode: bool) -> str:
    fragments: list[str] = []

    if _is_true(row.get("volume_confirmed")) or _is_true(row.get("volume_confirmation")):
        fragments.append("volume confirmation supported this setup")

    spread_state = _token(row.get("spread_context") or row.get("spread_signal") or row.get("spread_state"))
    if spread_state in {"supportive", "tight", "favorable", "favourable"}:
        fragments.append("spread conditions were supportive")

    momentum_state = _token(row.get("momentum_context") or row.get("momentum_signal") or row.get("momentum_state"))
    if momentum_state in {"supportive", "positive", "strong", "aligned"}:
        fragments.append("momentum signals were supportive")

    if not fragments:
        return ""

    if analyst_mode:
        return "Context: " + "; ".join(fragments) + "."
    return "Also, " + " and ".join(fragments) + "."


def _ranking_context(row: Mapping[str, Any], *, funded: bool, analyst_mode: bool) -> str:
    rank = _int_or_none(row.get("selection_rank"))
    if rank is None:
        return ""

    if funded:
        if analyst_mode:
            return f"Ranking context: this trade was selected at rank #{rank}."
        return f"It ranked #{rank}, ahead of lower-priority candidates."

    if analyst_mode:
        return f"Ranking context: this candidate finished at rank #{rank}, outside funded capacity."
    return f"It ranked #{rank}, below trades that received funding first."


def _is_analyst(mode: str) -> bool:
    return _token(mode) == "analyst"


def _is_true(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return _token(value) in {"true", "yes", "1", "y"}


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
