"""Metadata helpers for ingestion."""

from __future__ import annotations

import uuid
from typing import Dict

import pandas as pd


def generate_dataset_id() -> str:
    """Generate a unique dataset identifier."""
    return uuid.uuid4().hex


def build_metadata(df: pd.DataFrame, source: str, dataset_id: str) -> Dict[str, object]:
    """Build metadata for a canonical dataset."""
    volume_present = df["volume"].notna().any()
    if volume_present:
        liquidity_ceiling = "A"
        volume_confirmation_enabled = True
        extended_windows_allowed = True
    else:
        liquidity_ceiling = "B"
        volume_confirmation_enabled = False
        extended_windows_allowed = False

    return {
        "source": source,
        "dataset_id": dataset_id,
        "liquidity_ceiling": liquidity_ceiling,
        "volume_confirmation_enabled": volume_confirmation_enabled,
        "extended_windows_allowed": extended_windows_allowed,
    }
