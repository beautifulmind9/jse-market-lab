"""Dataset-specific preprocessing helpers."""

from __future__ import annotations

import re

import pandas as pd

_TEMPORARY_MARKERS = ("XD",)
_MARKER_PATTERN = re.compile(
    r"^(?P<ticker>[A-Z0-9]+?)(?:(?:[.\-_ ]?(?P<marker>XD))|(?:\s*\((?P<paren_marker>XD)\)))?$"
)


def _parse_symbol_parts(symbol: object) -> tuple[str, str | None]:
    """Split raw JSE symbol into canonical ticker and optional marker suffix."""
    raw_symbol = str(symbol or "").strip().upper()
    if not raw_symbol:
        return "", None

    match = _MARKER_PATTERN.match(raw_symbol)
    if not match:
        return raw_symbol, None

    marker = match.group("marker") or match.group("paren_marker")
    ticker = match.group("ticker") or raw_symbol
    if marker in _TEMPORARY_MARKERS:
        return ticker, marker
    return raw_symbol, None


def canonicalize_symbol_parts(symbol: object) -> tuple[str, str | None, str]:
    """Return canonical ticker, optional marker, and normalized raw symbol."""
    raw_symbol = str(symbol or "").strip().upper()
    ticker, marker = _parse_symbol_parts(raw_symbol)
    return ticker, marker, raw_symbol


def canonicalize_symbol(symbol: object) -> str:
    """Return canonical ticker token from a raw market symbol."""
    ticker, _marker, _raw = canonicalize_symbol_parts(symbol)
    return ticker


def normalize_jse_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the internal JSE dataset into ingestion-ready long format."""
    normalized = df.rename(
        columns={
            "symbol": "raw_symbol",
            "close_price": "close",
        }
    )

    normalized = normalized[["date", "raw_symbol", "close", "volume"]].copy()
    symbol_parts = normalized["raw_symbol"].map(canonicalize_symbol_parts)
    normalized["ticker"] = symbol_parts.map(lambda parts: parts[0])
    normalized["symbol_marker"] = symbol_parts.map(lambda parts: parts[1])
    normalized["display_symbol"] = normalized["raw_symbol"].astype(str).str.strip().str.upper()
    normalized["instrument"] = normalized["ticker"]
    normalized["date"] = pd.to_datetime(normalized["date"], errors="coerce")
    normalized = normalized.sort_values(["ticker", "date"]).reset_index(drop=True)
    return normalized
