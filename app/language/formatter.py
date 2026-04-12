"""Shared language helpers for beginner/analyst display copy."""

from __future__ import annotations

from typing import Any, Mapping


STRENGTH_LABELS = {
    "A": "Strong setup",
    "B": "Decent setup",
    "C": "Weak setup",
}

ADVISORY_TERMS = ("you should", "buy", "sell", "avoid this stock", "better to wait")


def get_strength_label(tier: Any) -> str:
    token = str(tier or "").strip().upper()
    return STRENGTH_LABELS.get(token, "Unrated setup")


def explain_strength(tier: Any, mode: str = "beginner") -> str:
    """Translate quality tier labels into plain-language setup meaning."""
    token = str(tier or "").strip().upper()
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"

    if token == "A":
        if analyst_mode:
            return "Strong setup (Tier A) — more key conditions are aligned and quality is higher."
        return "Strong setup — more key conditions are aligned."
    if token == "B":
        if analyst_mode:
            return "Mixed setup (Tier B) — supportive signals are present, but quality is not fully aligned."
        return "Mixed setup — some conditions are supportive, and some are weaker."
    if token == "C":
        if analyst_mode:
            return "Weak setup (Tier C) — fewer quality conditions are aligned, so risk is higher."
        return "Weak setup — quality is lower and risk is higher."

    if analyst_mode:
        return "Unrated setup — tier data is limited for this row."
    return "Unrated setup — this row has limited setup detail."


def explain_confidence(value_or_label: Any, mode: str = "beginner") -> str:
    """Translate confidence labels into non-predictive reliability language."""
    token = str(value_or_label or "").strip().lower()
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"

    if token in {"high", "strong"}:
        if analyst_mode:
            return "High confidence — similar setups have shown more reliable behavior in past observations."
        return "High confidence — similar setups have behaved more reliably in the past."
    if token in {"medium", "moderate", "mixed"}:
        if analyst_mode:
            return "Medium confidence — historical reliability is mixed across similar setups."
        return "Medium confidence — history is mixed for similar setups."
    if token in {"low", "weak", "high risk"}:
        if analyst_mode:
            return "Low confidence — similar setups have shown less reliable outcomes in historical samples."
        return "Low confidence — outcomes have been less reliable in similar setups."

    if analyst_mode:
        return "Confidence is unclear — the reliability signal is limited in this row."
    return "Confidence is unclear — this row has limited reliability detail."


def format_beginner_explanation(signal_or_row: Mapping[str, Any]) -> str:
    strength = get_strength_label(signal_or_row.get("quality_tier"))
    risk_line = _risk_sentence(signal_or_row)
    return f"{strength}. {risk_line}"


def format_analyst_explanation(signal_or_row: Mapping[str, Any]) -> str:
    strength = get_strength_label(signal_or_row.get("quality_tier"))
    win_rate = _pct_or_none(signal_or_row.get("win_rate"), 0)
    avg_return = _pct_or_none(signal_or_row.get("avg_return"), 2)

    metric_bits: list[str] = []
    if win_rate is not None:
        metric_bits.append(f"How often this works: {win_rate}")
    if avg_return is not None:
        metric_bits.append(f"Typical move: {avg_return}")
    metric_line = "; ".join(metric_bits) if metric_bits else "Key performance metrics are limited in this row."
    return f"{strength}. {_risk_sentence(signal_or_row)} {metric_line}"


def generate_explanation(signal_or_row: Mapping[str, Any], mode: str = "beginner") -> str:
    mode_token = str(mode or "beginner").strip().lower()
    if mode_token == "analyst":
        return format_analyst_explanation(signal_or_row)
    return format_beginner_explanation(signal_or_row)


def contains_advisory_language(text: str) -> bool:
    lowered = str(text or "").lower()
    return any(term in lowered for term in ADVISORY_TERMS)


def _risk_sentence(signal_or_row: Mapping[str, Any]) -> str:
    volatility = str(signal_or_row.get("volatility_bucket", "")).strip().lower()
    if volatility == "high":
        return "Prices are moving around more than usual, so this setup carries more risk."
    if volatility in {"low", "steady"}:
        return "Price movement is steadier than usual, which can help consistency."
    return "Price movement is mixed, so keep an eye on consistency."


def _pct_or_none(value: Any, decimals: int) -> str | None:
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return f"{numeric:.{decimals}%}"
