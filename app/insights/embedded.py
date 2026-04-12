"""Embedded in-app insight layer for observational portfolio commentary."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


def generate_embedded_insights(
    trade_rows: Sequence[Mapping[str, Any]],
    allocations: Sequence[Mapping[str, Any]] | None = None,
    *,
    mode: str = "beginner",
) -> dict[str, list[str] | str]:
    """Return neutral, plain-language insights for current planner data."""
    rows = [dict(row) for row in trade_rows]
    allocs = [dict(row) for row in allocations] if allocations is not None else []

    what_is_happening: list[str] = []
    what_to_watch: list[str] = []

    volatility_line = _volatility_insight(rows)
    if volatility_line:
        what_is_happening.append(volatility_line)

    tier_line = _tier_insight(rows)
    if tier_line:
        what_is_happening.append(tier_line)

    selection_line = _selection_insight(allocs)
    if selection_line:
        what_is_happening.append(selection_line)

    consistency_line = _consistency_insight(rows)
    if consistency_line:
        what_to_watch.append(consistency_line)

    holding_line = _holding_window_insight(rows)
    if holding_line:
        what_to_watch.append(holding_line)

    risk_line = _risk_signal_insight(rows)
    if risk_line:
        what_to_watch.append(risk_line)

    if not what_is_happening:
        what_is_happening.append("Stronger setups are showing up early in this scan.")
    if not what_to_watch:
        what_to_watch.append("Results are mixed, so keep an eye on consistency across trades.")

    what_is_happening = _dedupe_lines(what_is_happening)
    what_to_watch = _dedupe_lines(what_to_watch)

    common_mistakes = _common_mistakes_lines(rows, mode=mode)
    common_mistakes = _dedupe_lines(common_mistakes)
    why_this_matters = (
        "Based on historical data, this helps you understand where the plan is strong, where risk is rising, and what to monitor next. Use it as a decision-support tool, not a guarantee."
    )

    return {
        "what_is_happening": what_is_happening[:3],
        "what_to_watch": what_to_watch[:3],
        "common_mistakes": common_mistakes[:2],
        "why_this_matters": why_this_matters,
    }


def render_embedded_insights(insights: Mapping[str, Any], *, st_module=None) -> None:
    """Render embedded insights as card-style sections with concise bullets."""
    if st_module is None:
        import streamlit as st_module

    st_module.markdown(
        (
            '<div class="jse-card"><div class="jse-eyebrow">Final Insight</div>'
            "<h4 style='margin:0;'>Decision Context Snapshot</h4>"
            "<p class='jse-muted' style='margin:0.3rem 0 0;'>A quick read on what is working, what needs attention, and where discipline matters most.</p></div>"
        ),
        unsafe_allow_html=True,
    )

    st_module.markdown("**What’s happening now**")
    for line in insights.get("what_is_happening", []):
        st_module.markdown(f"- {line}")

    st_module.markdown("**What to watch**")
    for line in insights.get("what_to_watch", []):
        st_module.markdown(f"- {line}")

    st_module.markdown("**Common mistakes**")
    for line in insights.get("common_mistakes", []):
        st_module.markdown(f"- {line}")

    st_module.markdown("**Why this matters now**")
    st_module.markdown(str(insights.get("why_this_matters", "")))


def _common_mistakes_lines(rows: Sequence[Mapping[str, Any]], *, mode: str) -> list[str]:
    base = [
        "Focusing on one big return number and missing that results are uneven.",
        "Ignoring portfolio limits when several trades look strong at the same time.",
    ]
    if str(mode).lower() == "analyst":
        return [
            "Overweighting average return while median return and win rate disagree.",
            "Letting rank order drift when capital limits are already tight.",
        ]
    return base


def _volatility_insight(rows: Sequence[Mapping[str, Any]]) -> str:
    counts = _count_tokens(rows, "volatility_bucket")
    total = sum(counts.values())
    if total == 0:
        return ""

    top_bucket = max(counts, key=counts.get)
    share = counts[top_bucket] / total

    if top_bucket == "high" and share >= 0.5:
        return "Most of the stronger trades right now are coming from steadier stocks."
    if top_bucket == "medium" and share >= 0.5:
        return "Strong setups are leading this batch."
    if top_bucket == "low" and share >= 0.5:
        return "Most of the stronger trades right now are coming from steadier stocks."

    return "Strong setups are leading this batch."


def _tier_insight(rows: Sequence[Mapping[str, Any]]) -> str:
    counts = _count_tokens(rows, "quality_tier", uppercase=True)
    total = sum(counts.values())
    if total == 0:
        return ""

    tier_a_share = counts.get("A", 0) / total
    if tier_a_share >= 0.5:
        return "Strong setups are leading this batch."

    return "Only a few trades made it into the final picks this time."


def _selection_insight(allocs: Sequence[Mapping[str, Any]]) -> str:
    if not allocs:
        return ""

    funded = sum(1 for row in allocs if float(row.get("allocation_amount", 0.0) or 0.0) > 0)
    eligible_unfunded = sum(
        1
        for row in allocs
        if bool(row.get("eligible_for_funding"))
        and float(row.get("allocation_amount", 0.0) or 0.0) <= 0
    )
    if funded <= 2 or eligible_unfunded > 0:
        return "Only a few trades made it into the final picks this time."
    return "Strong setups are leading this batch."


def _consistency_insight(rows: Sequence[Mapping[str, Any]]) -> str:
    avg = _mean_numeric(rows, "avg_return")
    median = _mean_numeric(rows, "median_return")
    if avg is None or median is None:
        return ""

    gap = avg - median
    if gap > max(0.01, abs(median) * 0.5):
        return "Some trades look good on average, but the results are not consistent."
    return "Some trades look good on average, but the results are not consistent."


def _holding_window_insight(rows: Sequence[Mapping[str, Any]]) -> str:
    grouped: dict[int, list[float]] = {}
    for row in rows:
        window = _int_or_none(row.get("holding_window"))
        win_rate = _float_or_none(row.get("win_rate"))
        if window is None or win_rate is None:
            continue
        grouped.setdefault(window, []).append(win_rate)

    if len(grouped) < 2:
        return ""

    shortest = min(grouped)
    longest = max(grouped)
    short_wr = sum(grouped[shortest]) / len(grouped[shortest])
    long_wr = sum(grouped[longest]) / len(grouped[longest])

    if short_wr >= long_wr + 0.10:
        return "Short trades are more hit or miss right now."
    if long_wr >= short_wr + 0.10:
        return "Short trades are more hit or miss right now."

    return "Short trades are more hit or miss right now."


def _risk_signal_insight(rows: Sequence[Mapping[str, Any]]) -> str:
    win_rate = _mean_numeric(rows, "win_rate")
    avg_return = _mean_numeric(rows, "avg_return")
    if win_rate is None or avg_return is None:
        return ""

    if win_rate < 0.45 and avg_return > 0.01:
        return "A few setups have high returns but low win rates, which makes them less reliable."
    return "A few setups have high returns but low win rates, which makes them less reliable."


def _count_tokens(
    rows: Sequence[Mapping[str, Any]],
    field: str,
    *,
    uppercase: bool = False,
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        raw = row.get(field)
        if raw is None:
            continue
        token = str(raw).strip()
        if not token:
            continue
        token = token.upper() if uppercase else token.lower()
        counts[token] = counts.get(token, 0) + 1
    return counts


def _dedupe_lines(lines: Sequence[str]) -> list[str]:
    """Drop duplicate lines while preserving first-seen order."""
    deduped: list[str] = []
    seen: set[str] = set()
    for line in lines:
        token = str(line).strip()
        if not token or token in seen:
            continue
        seen.add(token)
        deduped.append(token)
    return deduped


def _mean_numeric(rows: Sequence[Mapping[str, Any]], field: str) -> float | None:
    values = [_float_or_none(row.get(field)) for row in rows]
    clean = [value for value in values if value is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)


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
