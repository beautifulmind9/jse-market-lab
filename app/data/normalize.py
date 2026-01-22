"""Normalize raw input data into canonical format."""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from .schema import CANONICAL_COLUMNS, FORMAT_LONG, FORMAT_WIDE, LONG_REQUIRED_COLUMNS


def detect_format(df: pd.DataFrame) -> str:
    """Detect input format (long vs wide)."""
    lower_columns = {col.lower() for col in df.columns}
    if LONG_REQUIRED_COLUMNS.issubset(lower_columns):
        return FORMAT_LONG
    if "date" in lower_columns:
        return FORMAT_WIDE
    raise ValueError("Unable to detect input format.")


def _normalize_long(df: pd.DataFrame, source: str, dataset_id: str) -> pd.DataFrame:
    """Normalize long-format input into canonical schema."""
    cols = {col.lower(): col for col in df.columns}
    price_col = None
    if "close" in cols:
        price_col = cols["close"]
    elif "adj_close" in cols:
        price_col = cols["adj_close"]
    else:
        raise ValueError("Missing close or adj_close column.")

    data = pd.DataFrame()
    data["date"] = pd.to_datetime(df[cols["date"]], errors="coerce")
    data["instrument"] = (
        df[cols["instrument"]].astype(str).str.strip().str.upper()
    )
    data["close"] = pd.to_numeric(df[price_col], errors="coerce")

    if "volume" in cols:
        data["volume"] = pd.to_numeric(df[cols["volume"]], errors="coerce")
    else:
        data["volume"] = np.nan

    for col_name in ("market", "currency"):
        if col_name in cols:
            data[col_name] = (
                df[cols[col_name]].astype(str).str.strip().replace({"nan": None})
            )
        else:
            data[col_name] = None

    data["source"] = source
    data["dataset_id"] = dataset_id
    return data[CANONICAL_COLUMNS]


def _normalize_wide(df: pd.DataFrame, source: str, dataset_id: str) -> pd.DataFrame:
    """Normalize wide-format input into canonical schema."""
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]
    date_candidates = [col for col in df.columns if col.lower() == "date"]
    if not date_candidates:
        raise ValueError("Wide format requires a 'date' column.")
    date_col = date_candidates[0]
    prices = df.melt(id_vars=[date_col], var_name="instrument", value_name="close")
    prices = prices.rename(columns={date_col: "date"}).dropna(subset=["close"])
    data = pd.DataFrame()
    data["date"] = pd.to_datetime(prices["date"], errors="coerce")
    data["instrument"] = prices["instrument"].astype(str).str.strip().str.upper()
    data["close"] = pd.to_numeric(prices["close"], errors="coerce")
    data["volume"] = np.nan
    data["market"] = None
    data["currency"] = None
    data["source"] = source
    data["dataset_id"] = dataset_id
    return data[CANONICAL_COLUMNS]


def normalize_data(
    df: pd.DataFrame, source: str, dataset_id: str
) -> Tuple[pd.DataFrame, str]:
    """Normalize data and return canonical dataframe with detected format."""
    fmt = detect_format(df)
    if fmt == FORMAT_LONG:
        return _normalize_long(df, source, dataset_id), fmt
    return _normalize_wide(df, source, dataset_id), fmt
