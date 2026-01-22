"""Objective weights and window emphasis rules."""

from __future__ import annotations

from typing import Dict


OBJECTIVE_WEIGHTS: Dict[str, Dict[str, float]] = {
    "income_stability": {"R": 0.35, "W": 0.35, "H": 0.2, "T": 0.1},
    "active_growth": {"R": 0.45, "W": 0.2, "H": 0.2, "T": 0.15},
    "risk_controlled_total_return": {"R": 0.4, "W": 0.3, "H": 0.2, "T": 0.1},
    "capital_preservation": {"R": 0.25, "W": 0.4, "H": 0.25, "T": 0.1},
}

WINDOW_EMPHASIS: Dict[str, Dict[int, float]] = {
    "income_stability": {5: 0.98, 10: 1.03, 20: 1.03, 30: 1.0},
    "active_growth": {5: 1.03, 10: 1.0, 20: 0.99, 30: 0.98},
    "risk_controlled_total_return": {5: 0.99, 10: 1.01, 20: 1.02, 30: 1.0},
    "capital_preservation": {5: 0.98, 10: 1.02, 20: 1.03, 30: 1.0},
}


def get_objective_weights(objective: str) -> Dict[str, float]:
    """Return the weight map for the selected objective."""
    if objective not in OBJECTIVE_WEIGHTS:
        raise ValueError(f"Unknown objective: {objective}")
    return OBJECTIVE_WEIGHTS[objective].copy()


def get_window_emphasis(objective: str) -> Dict[int, float]:
    """Return window emphasis multipliers for the objective."""
    if objective not in WINDOW_EMPHASIS:
        raise ValueError(f"Unknown objective: {objective}")
    return WINDOW_EMPHASIS[objective].copy()
