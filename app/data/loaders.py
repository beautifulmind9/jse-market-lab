"""Load raw data for ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Optional

import pandas as pd

from .processor import normalize_jse_dataset

INTERNAL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "internal" / "jse_dataset.csv"
LEGACY_INTERNAL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "internal" / "jse_sample.csv"


def load_internal_dataset() -> tuple[pd.DataFrame, str]:
    """Load and normalize the bundled internal JSE dataset from disk."""
    if INTERNAL_DATASET_PATH.exists():
        dataset_path = INTERNAL_DATASET_PATH
        source_label = "internal_jse_dataset"
    else:
        dataset_path = LEGACY_INTERNAL_DATASET_PATH
        source_label = "legacy_demo_dataset"

    raw = pd.read_csv(dataset_path)
    normalized = normalize_jse_dataset(raw)

    # Backward compatibility: downstream app paths still expect `instrument`.
    # Keep `ticker` from the normalized dataset while exposing a mirrored alias.
    normalized["instrument"] = normalized["ticker"]
    return normalized, source_label


def load_upload(uploaded_file: Optional[IO]) -> pd.DataFrame:
    """Load uploaded CSV data."""
    if uploaded_file is None:
        raise ValueError("uploaded_file is required for upload mode.")
    return pd.read_csv(uploaded_file)
