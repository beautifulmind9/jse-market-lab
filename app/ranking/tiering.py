"""Tiering and liquidity caps."""

from __future__ import annotations

from typing import Tuple


def assign_tier(score: float) -> str:
    """Assign a tier based on score thresholds."""
    if score >= 0.7:
        return "A"
    if score >= 0.55:
        return "B"
    return "C"


def apply_liquidity_cap(
    tier: str,
    volume_available: bool,
    liquidity_ceiling: str,
) -> Tuple[str, str | None]:
    """Cap tiers for illiquid datasets and return warning message if capped."""
    if volume_available and liquidity_ceiling == "A":
        return tier, None
    warning = "Tier capped at B due to limited liquidity data."
    if tier == "A":
        return "B", warning
    return tier, warning
