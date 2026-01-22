"""Upload helpers for ingestion."""

from __future__ import annotations

from typing import IO

import pandas as pd


def read_upload(file_obj: IO) -> pd.DataFrame:
    """Read a CSV file-like object into a DataFrame."""
    return pd.read_csv(file_obj)
