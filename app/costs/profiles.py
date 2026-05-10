"""Broker and planning cost profiles.

The profiles in this module are planning estimates, not fee guarantees.
Actual fees may vary by broker, channel, transaction size, taxes, and account terms.
"""

from __future__ import annotations

from typing import Dict, TypedDict


class CostProfile(TypedDict):
    """Cost profile values expressed as decimal rates."""

    broker_fee: float
    cess: float


class CostProfileMetadata(TypedDict):
    """User-facing profile metadata."""

    key: str
    label: str
    broker_fee: float
    cess: float
    verification_status: str
    source: str
    note: str


DEFAULT_PROFILE_KEY = "conservative_estimate"

# Preserve the legacy profile for backwards compatibility and historical comparisons.
LEGACY_DEFAULT_PROFILE: CostProfile = {"broker_fee": 0.001, "cess": 0.0005}

# Older engine code may still request this exact profile name.
LEGACY_PROFILE_ALIASES = {
    "default": "legacy_default",
    "Default": "legacy_default",
}

# Neutral planning profiles. These should not imply that any broker is preferred.
PROFILES: Dict[str, CostProfileMetadata] = {
    "legacy_default": {
        "key": "legacy_default",
        "label": "Legacy default estimate",
        "broker_fee": 0.001,
        "cess": 0.0005,
        "verification_status": "legacy_internal",
        "source": "Existing engine default retained for compatibility",
        "note": "Historical internal default. Do not treat as a universal broker fee.",
    },
    "low_cost_estimate": {
        "key": "low_cost_estimate",
        "label": "Low-cost estimate",
        "broker_fee": 0.005,
        "cess": 0.0035,
        "verification_status": "planning_estimate",
        "source": "Internal planning assumption pending broker verification",
        "note": "Illustrative estimate only. Confirm actual fees with the selected licensed broker.",
    },
    "conservative_estimate": {
        "key": "conservative_estimate",
        "label": "Conservative estimate",
        "broker_fee": 0.02,
        "cess": 0.0035,
        "verification_status": "planning_estimate",
        "source": "Internal planning assumption pending broker verification",
        "note": "Higher-fee planning estimate for stress-testing costs. Confirm actual fees with the selected licensed broker.",
    },
    "high_cost_estimate": {
        "key": "high_cost_estimate",
        "label": "High-cost estimate",
        "broker_fee": 0.025,
        "cess": 0.0035,
        "verification_status": "planning_estimate",
        "source": "Internal planning assumption pending broker verification",
        "note": "Upper-range planning estimate for cost sensitivity review. Confirm actual fees with the selected licensed broker.",
    },
}

# Backwards-compatible constant used by older engine helpers.
DEFAULT_PROFILE: CostProfile = {
    "broker_fee": PROFILES[DEFAULT_PROFILE_KEY]["broker_fee"],
    "cess": PROFILES[DEFAULT_PROFILE_KEY]["cess"],
}


def get_profile(name: str | None = None) -> CostProfile:
    """Return the cost profile rates for the given profile key or label."""
    metadata = get_profile_metadata(name)
    return {"broker_fee": metadata["broker_fee"], "cess": metadata["cess"]}


def get_profile_metadata(name: str | None = None) -> CostProfileMetadata:
    """Return profile metadata for the given profile key or label."""
    profile_name = (name or DEFAULT_PROFILE_KEY).strip()
    alias_key = LEGACY_PROFILE_ALIASES.get(profile_name) or LEGACY_PROFILE_ALIASES.get(profile_name.lower())
    if alias_key:
        return PROFILES[alias_key].copy()

    if profile_name in PROFILES:
        return PROFILES[profile_name].copy()

    normalized = profile_name.lower()
    for profile in PROFILES.values():
        if profile["label"].lower() == normalized:
            return profile.copy()

    raise ValueError(f"Unknown broker or cost profile: {name}")


def list_profiles() -> list[CostProfileMetadata]:
    """Return all available neutral cost profiles."""
    return [profile.copy() for profile in PROFILES.values()]


def get_cost_disclaimer() -> str:
    """Return the standard cost-profile disclaimer."""
    return (
        "Estimated costs are based on the selected cost profile. Actual fees may vary by broker, "
        "channel, transaction size, taxes, and account terms. Confirm fees with your licensed broker before acting."
    )
