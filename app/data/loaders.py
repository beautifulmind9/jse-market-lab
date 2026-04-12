"""Load raw data for ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Optional

import pandas as pd

from .processor import normalize_jse_dataset

REPO_ROOT = Path(__file__).resolve().parents[2]
INTERNAL_DATASET_PATH = REPO_ROOT / "data" / "internal" / "jse_dataset.csv"
LEGACY_INTERNAL_DATASET_PATH = REPO_ROOT / "data" / "internal" / "jse_sample.csv"


def _build_legacy_fallback_dataset() -> pd.DataFrame:
    """Build a tiny emergency fallback dataset when no file-based fallback exists."""
    return pd.DataFrame(
        {
            "date": ["2024-01-02", "2024-01-03", "2024-01-04"],
            "symbol": ["DEMO", "DEMO", "DEMO"],
            "close_price": [10.0, 10.2, 10.1],
            "volume": [1000, 1200, 900],
        }
    )


def load_internal_dataset_with_source() -> tuple[pd.DataFrame, str]:
    """Load and normalize the bundled internal JSE dataset from disk with source label."""
    if INTERNAL_DATASET_PATH.exists():
        dataset_path = INTERNAL_DATASET_PATH
        source_label = "internal_jse_dataset"
        raw = pd.read_csv(dataset_path)
    else:
        dataset_path = LEGACY_INTERNAL_DATASET_PATH
        source_label = "legacy_demo_dataset"
        if dataset_path.exists():
            raw = pd.read_csv(dataset_path)
        else:
            raw = _build_legacy_fallback_dataset()

    normalized = normalize_jse_dataset(raw)

    # Backward compatibility: downstream app paths still expect `instrument`.
    # Keep `instrument` mirrored to the canonical ticker.
    normalized["instrument"] = normalized["ticker"]
    return normalized, source_label


def load_internal_dataset() -> pd.DataFrame:
    """Load and normalize the bundled internal JSE dataset from disk."""
    dataset, _source_label = load_internal_dataset_with_source()
    return dataset


def get_internal_dataset_source_label() -> str:
    """Return the current source label for the bundled internal dataset."""
    _dataset, source_label = load_internal_dataset_with_source()
    return source_label


def load_upload(uploaded_file: Optional[IO]) -> pd.DataFrame:
    """Load uploaded CSV data."""
    if uploaded_file is None:
        raise ValueError("uploaded_file is required for upload mode.")
    return pd.read_csv(uploaded_file)
