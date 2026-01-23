"""Language-mode copy for demo outputs."""

from __future__ import annotations

from typing import Dict

LANGUAGE_MODES = {"plain", "analyst"}

EXPLANATORY_COPY: Dict[str, Dict[str, str]] = {
    "plain": {
        "overview": "This demo summarizes how strategies behave after costs.",
        "ranking": "Rankings highlight the strongest performers for the chosen objective.",
        "phase_metrics": "Phase metrics show returns around earnings windows.",
        "caveats": "Use these results as decision support, not investment advice.",
    },
    "analyst": {
        "overview": "This demo summarizes net-of-cost strategy behavior.",
        "ranking": "Rankings surface instruments with the strongest objective-weighted scores.",
        "phase_metrics": "Phase metrics quantify return distributions across earnings phases.",
        "caveats": "Outputs are descriptive analytics, not predictive recommendations.",
    },
}


def get_explanatory_copy(mode: str) -> Dict[str, str]:
    """Return explanatory copy for the requested language mode."""
    normalized = mode.strip().lower()
    if normalized not in LANGUAGE_MODES:
        raise ValueError("language mode must be 'plain' or 'analyst'")
    return EXPLANATORY_COPY[normalized].copy()
