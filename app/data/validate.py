"""Validation for canonical datasets."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd


def validate_canonical(df: pd.DataFrame) -> Dict[str, List[str]]:
    """Validate canonical dataset and return issues dict."""
    issues: Dict[str, List[str]] = {"errors": [], "warnings": []}

    if df["date"].isna().any():
        issues["errors"].append("Unparseable dates detected.")
    if df["close"].isna().any():
        issues["errors"].append("Non-numeric close values detected.")

    duplicates = df.duplicated(subset=["date", "instrument"]).any()
    if duplicates:
        issues["errors"].append("Duplicate (date, instrument) rows detected.")

    trading_days = df["date"].dropna().dt.normalize().nunique()
    if trading_days < 60:
        issues["errors"].append("Fewer than 60 unique trading days.")

    obs_counts = df.dropna(subset=["date"]).groupby("instrument")["date"].nunique()
    sparse = obs_counts[obs_counts < 40].index.tolist()
    if sparse:
        issues["warnings"].append(
            "Some instruments have fewer than 40 observations: "
            + ", ".join(sorted(sparse))
            + "."
        )

    return issues
