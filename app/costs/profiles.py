"""Broker cost profiles."""

from __future__ import annotations

from typing import Dict


DEFAULT_PROFILE = {"broker_fee": 0.001, "cess": 0.0005}

PROFILES: Dict[str, Dict[str, float]] = {
    "Default": DEFAULT_PROFILE,
}


def get_profile(name: str) -> Dict[str, float]:
    """Return the cost profile for the given broker name."""
    if name not in PROFILES:
        raise ValueError(f"Unknown broker profile: {name}")
    return PROFILES[name].copy()
