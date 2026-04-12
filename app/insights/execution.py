"""Execution framing helpers for portfolio and ticker-level explanations."""

from __future__ import annotations

from typing import Any, Mapping


def build_execution_summary(row: Mapping[str, Any], mode: str = "beginner") -> dict[str, str]:
    """Build non-predictive execution framing for a trade row."""
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"

    entry_reference = _build_entry_reference(row)
    planned_exit = _build_planned_exit(row)
    typical_outcome = _build_typical_outcome(row, analyst_mode=analyst_mode)
    execution_risk = _build_execution_risk(row, analyst_mode=analyst_mode)

    status_prefix = ""
    if float(row.get("allocation_amount", 0.0) or 0.0) <= 0:
        status_prefix = "Execution plan is inactive unless this trade is funded. "

    summary = (
        f"{status_prefix}Entry reference: {entry_reference} "
        f"Planned exit: {planned_exit} "
        f"Typical outcome: {typical_outcome} "
        f"Execution risk: {execution_risk}"
    ).strip()

    return {
        "entry_reference": entry_reference,
        "planned_exit": planned_exit,
        "typical_outcome": typical_outcome,
        "execution_risk": execution_risk,
        "summary": summary,
    }


def _build_entry_reference(row: Mapping[str, Any]) -> str:
    signal_close = _float_or_none(
        row.get("signal_day_close") or row.get("signal_close") or row.get("close")
    )
    if signal_close is None:
        return "Use the signal-day close area as a reference, not an exact guaranteed fill."
    return (
        f"Use the signal-day close area (around {signal_close:,.2f}) as a reference, "
        "not an exact guaranteed fill."
    )


def _build_planned_exit(row: Mapping[str, Any]) -> str:
    holding_window = _int_or_none(row.get("holding_window"))
    if holding_window is None:
        return "Use the default time-based exit window and review conditions before closing."
    return (
        f"Default exit is after about {holding_window} trading days, "
        "unless conditions are reviewed earlier."
    )


def _build_typical_outcome(row: Mapping[str, Any], *, analyst_mode: bool) -> str:
    median_return = _float_or_none(row.get("median_return"))
    avg_return = _float_or_none(row.get("avg_return"))

    if median_return is None:
        if avg_return is None:
            return "Median outcome data is limited for this setup."
        return f"Median outcome is unavailable; supporting average return is about {avg_return:.2%}."

    typical = f"Typical result is centered on median return near {median_return:.2%}."
    if avg_return is None:
        return typical

    gap = abs(avg_return - median_return)
    if gap <= 0.003:
        if analyst_mode:
            return typical + f" Supporting average return is {avg_return:.2%}, which is close."
        return typical

    direction = "higher" if avg_return > median_return else "lower"
    return (
        typical
        + f" Supporting average return is {avg_return:.2%}, {direction} than median, "
        "which suggests a few larger moves may be influencing the average."
    )


def _build_execution_risk(row: Mapping[str, Any], *, analyst_mode: bool) -> str:
    parts = ["Actual execution can differ from reference pricing"]

    liquidity_pass = row.get("liquidity_pass")
    if liquidity_pass is False:
        parts.append("lower liquidity can reduce fill quality")

    spread_state = _token(row.get("spread_context") or row.get("spread_signal") or row.get("spread_state"))
    if spread_state in {"wide", "elevated", "unstable"}:
        parts.append("wider spreads can increase entry and exit slippage")
    elif spread_state in {"supportive", "tight", "favorable", "favourable"} and analyst_mode:
        parts.append("current spread conditions look relatively stable")
    else:
        parts.append("spread conditions can affect realized fills")

    return "; ".join(parts) + "."


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


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
