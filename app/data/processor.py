"""Dataset-specific preprocessing helpers."""

from __future__ import annotations

import pandas as pd


def normalize_jse_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the internal JSE dataset into ingestion-ready long format."""
    normalized = df.rename(
        columns={
            "symbol": "ticker",
            "close_price": "close",
        }
    )

    normalized = normalized[["date", "ticker", "close", "volume"]].copy()
    normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    normalized = normalized.sort_values(["ticker", "date"]).reset_index(drop=True)
    return normalized
