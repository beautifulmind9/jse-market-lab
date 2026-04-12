"""Load raw data for ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Optional

import pandas as pd

from .processor import normalize_jse_dataset

INTERNAL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "internal" / "jse_dataset.csv"
LEGACY_INTERNAL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "internal" / "jse_sample.csv"


def load_internal_dataset() -> pd.DataFrame:
    """Load and normalize the bundled internal JSE dataset from disk."""
    dataset_path = INTERNAL_DATASET_PATH if INTERNAL_DATASET_PATH.exists() else LEGACY_INTERNAL_DATASET_PATH
    raw = pd.read_csv(dataset_path)
    normalized = normalize_jse_dataset(raw)

    # Backward compatibility: downstream app paths still expect `instrument`.
    # Keep `ticker` from the normalized dataset while exposing a mirrored alias.
    normalized["instrument"] = normalized["ticker"]
    return normalized


def load_upload(uploaded_file: Optional[IO]) -> pd.DataFrame:
    """Load uploaded CSV data."""
    if uploaded_file is None:
        raise ValueError("uploaded_file is required for upload mode.")
    return pd.read_csv(uploaded_file)
