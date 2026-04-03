"""Planner warning copy helpers."""

from __future__ import annotations

from typing import Dict, Optional


PHASES = {"pre", "reaction", "post", "non"}

TONE_COPY: Dict[str, Dict[str, Dict[str, str]]] = {
    "jm": {
        "pre": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
        "reaction": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
        "post": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
    },
    "cfa": {
        "pre": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
        "reaction": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
        "post": {
            "title": "⚠️ Earnings",
            "body": "This trade runs into earnings, so price movement may be unpredictable.",
        },
    },
}

SEVERITY_BY_PHASE = {"pre": "caution", "reaction": "caution", "post": "info"}
OVERLAP_LINE = {"jm": "", "cfa": ""}


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

    return {"severity": severity, "title": title, "body": body}
