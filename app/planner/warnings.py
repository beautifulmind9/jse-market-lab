"""Planner warning copy helpers."""

from __future__ import annotations

from typing import Dict, Optional


PHASES = {"pre", "reaction", "post", "non"}

TONE_COPY: Dict[str, Dict[str, Dict[str, str]]] = {
    "jm": {
        "pre": {
            "title": "⚠️ Earnings soon",
            "body": (
                "Earnings in {days} trading days. Price can move wild round "
                "results time. If yuh a aim fi steady income, consider "
                "smaller size or give the trade more time."
            ),
        },
        "reaction": {
            "title": "⚠️ Results reaction window",
            "body": (
                "We deh in the earnings reaction period. Expect sharper moves "
                "and execution risk. Avoid forcing exits if the spread widen."
            ),
        },
        "post": {
            "title": "ℹ️ Post-earnings window",
            "body": (
                "Post-results period. Moves usually calm down compared to "
                "reaction days, but still watch liquidity."
            ),
        },
    },
    "cfa": {
        "pre": {
            "title": "⚠️ Earnings upcoming",
            "body": (
                "Earnings in {days} trading days. Volatility and spreads can "
                "increase around announcements. For income-oriented trades, "
                "consider smaller size or a longer holding window."
            ),
        },
        "reaction": {
            "title": "⚠️ Earnings reaction window",
            "body": (
                "This trade sits in the earnings reaction window. Short-term "
                "variance and execution risk may be elevated; spreads can "
                "widen."
            ),
        },
        "post": {
            "title": "ℹ️ Post-earnings window",
            "body": (
                "Post-earnings period. Volatility often stabilizes relative to "
                "the reaction window, though liquidity conditions still "
                "matter."
            ),
        },
    },
}

SEVERITY_BY_PHASE = {"pre": "caution", "reaction": "caution", "post": "info"}
OVERLAP_LINE = {
    "jm": "This trade crosses an earnings phase.",
    "cfa": "This trade overlaps an earnings-phase boundary.",
}


def build_earnings_warning(
    entry_phase: str,
    exit_phase: str,
    entry_offset: Optional[int],
    overlaps: bool,
    objective: str,
    tone: str = "cfa",
) -> Dict[str, Optional[str]]:
    """Build earnings warning copy for a planner row."""
    _ = objective
    if entry_phase not in PHASES or entry_phase == "non":
        return {"severity": None, "title": None, "body": None}

    tone_copy = TONE_COPY.get(tone, TONE_COPY["cfa"])
    copy = tone_copy.get(entry_phase, {})
    title = copy.get("title")
    body = copy.get("body")
    severity = SEVERITY_BY_PHASE.get(entry_phase)

    if entry_phase == "pre" and body:
        if entry_offset is not None:
            body = body.format(days=abs(int(entry_offset)))
        else:
            body = body.replace("{days} ", "").replace("{days}", "")

    if overlaps and body:
        body = f"{body}\n{OVERLAP_LINE.get(tone, OVERLAP_LINE['cfa'])}"

    return {"severity": severity, "title": title, "body": body}
