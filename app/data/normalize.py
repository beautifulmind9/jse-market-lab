"""Normalize raw input data into canonical format."""

from __future__ import annotations

from typing import Tuple

import numpy as np
import pandas as pd

from .schema import CANONICAL_COLUMNS, FORMAT_LONG, FORMAT_WIDE, LONG_REQUIRED_COLUMNS
from .processor import canonicalize_symbol_parts


def detect_format(df: pd.DataFrame) -> str:
    """Detect input format (long vs wide)."""
    lower_columns = {col.lower() for col in df.columns}
    if LONG_REQUIRED_COLUMNS.issubset(lower_columns) or {"date", "ticker"}.issubset(lower_columns):
        return FORMAT_LONG
    if "date" in lower_columns:
        return FORMAT_WIDE
    raise ValueError("Unable to detect input format.")




def _normalize_optional_symbol_metadata(
    series: pd.Series, fallback: pd.Series
) -> pd.Series:
    """Normalize optional symbol metadata with robust missing-value fallback."""
    normalized = series.astype("string").str.strip().str.upper()
    missing_mask = series.isna() | normalized.isin({"", "NAN", "NONE", "<NA>"})
    preserved = normalized.mask(missing_mask, fallback)
    return preserved.astype(object).where(pd.notna(preserved), None)


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
    instrument_col = "instrument" if "instrument" in cols else "ticker"
    if instrument_col not in cols:
        raise ValueError("Missing instrument or ticker column.")

    raw_symbols = df[cols[instrument_col]].astype(str).str.strip().str.upper()
    symbol_parts = raw_symbols.map(canonicalize_symbol_parts)
    data["ticker"] = symbol_parts.map(lambda parts: parts[0])
    data["instrument"] = data["ticker"]
    fallback_raw_symbol = symbol_parts.map(lambda parts: parts[2])

    if "raw_symbol" in cols:
        data["raw_symbol"] = _normalize_optional_symbol_metadata(
            df[cols["raw_symbol"]], fallback_raw_symbol
        )
    else:
        data["raw_symbol"] = fallback_raw_symbol

    fallback_marker = data["raw_symbol"].map(lambda symbol: canonicalize_symbol_parts(symbol)[1])
    if "symbol_marker" in cols:
        data["symbol_marker"] = _normalize_optional_symbol_metadata(
            df[cols["symbol_marker"]], fallback_marker
        )
    else:
        data["symbol_marker"] = fallback_marker

    if "display_symbol" in cols:
        data["display_symbol"] = _normalize_optional_symbol_metadata(
            df[cols["display_symbol"]], data["raw_symbol"]
        )
    else:
        data["display_symbol"] = data["raw_symbol"]
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
    date_col = df.columns[0]
    prices = df.melt(id_vars=[date_col], var_name="instrument", value_name="close")
    data = pd.DataFrame()
    data["date"] = pd.to_datetime(prices[date_col], errors="coerce")
    raw_symbols = prices["instrument"].astype(str).str.strip().str.upper()
    symbol_parts = raw_symbols.map(canonicalize_symbol_parts)
    data["ticker"] = symbol_parts.map(lambda parts: parts[0])
    data["instrument"] = data["ticker"]
    data["raw_symbol"] = symbol_parts.map(lambda parts: parts[2])
    data["symbol_marker"] = symbol_parts.map(lambda parts: parts[1])
    data["display_symbol"] = data["raw_symbol"]
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
