"""Load raw data for ingestion."""

from __future__ import annotations

from pathlib import Path
from typing import IO, Optional

import pandas as pd

DEMO_PATH = Path(__file__).resolve().parents[2] / "data" / "demo" / "demo_prices.csv"


def load_demo() -> pd.DataFrame:
    """Load demo data from the packaged CSV."""
    return pd.read_csv(DEMO_PATH)


def load_upload(uploaded_file: Optional[IO]) -> pd.DataFrame:
    """Load uploaded CSV data."""
    if uploaded_file is None:
        raise ValueError("uploaded_file is required for upload mode.")
    return pd.read_csv(uploaded_file)
