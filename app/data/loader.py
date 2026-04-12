"""Load raw data for ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Optional

import pandas as pd

INTERNAL_DATASET_PATH = Path(__file__).resolve().parents[2] / "data" / "internal" / "jse_sample.csv"


def load_internal_dataset() -> pd.DataFrame:
    """Load the bundled JSE sample dataset from disk."""
    df = pd.read_csv(INTERNAL_DATASET_PATH, parse_dates=["date"])
    if "ticker" in df.columns and "instrument" not in df.columns:
        df = df.rename(columns={"ticker": "instrument"})
    return df


def load_demo() -> pd.DataFrame:
    """Backward-compatible alias for loading the internal sample dataset."""
    return load_internal_dataset()


def load_upload(uploaded_file: Optional[IO]) -> pd.DataFrame:
    """Load uploaded CSV data."""
    if uploaded_file is None:
        raise ValueError("uploaded_file is required for upload mode.")
    return pd.read_csv(uploaded_file)
