"""Cost configuration helpers."""

from __future__ import annotations

from typing import Dict, Optional

from .profiles import get_profile


def resolve_cost_config(
    broker_profile: str,
    override_enabled: bool = False,
    broker_fee: Optional[float] = None,
    cess: Optional[float] = None,
) -> Dict[str, float]:
    """Resolve broker costs and compute round-trip cost rate."""
    profile = get_profile(broker_profile)
    resolved_fee = profile["broker_fee"]
    resolved_cess = profile["cess"]

    if override_enabled:
        if broker_fee is not None:
            resolved_fee = broker_fee
        if cess is not None:
            resolved_cess = cess

    round_trip_cost_rate = (resolved_fee + resolved_cess) * 2
    return {
        "broker_profile": broker_profile,
        "broker_fee": resolved_fee,
        "cess": resolved_cess,
        "round_trip_cost_rate": round_trip_cost_rate,
    }
