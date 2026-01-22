import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.data.metadata import build_metadata
from app.data.normalize import detect_format, normalize_data
from app.data.validate import validate_canonical


def test_detect_format_long_vs_wide():
    long_df = pd.DataFrame(
        {"date": ["2024-01-01"], "instrument": ["ABC"], "close": [1.0]}
    )
    wide_df = pd.DataFrame({"date": ["2024-01-01"], "ABC": [1.0]})

    assert detect_format(long_df) == "long"
    assert detect_format(wide_df) == "wide"


def test_min_trading_days_hard_fail():
    dates = pd.date_range("2024-01-01", periods=10, freq="D")
    df = pd.DataFrame(
        {
            "date": dates,
            "instrument": ["AAA"] * len(dates),
            "close": [1.0] * len(dates),
            "volume": [np.nan] * len(dates),
            "market": [None] * len(dates),
            "currency": [None] * len(dates),
            "source": ["demo"] * len(dates),
            "dataset_id": ["test"] * len(dates),
        }
    )

    issues = validate_canonical(df)
    assert any("Fewer than 60" in err for err in issues["errors"])


def test_volume_missing_sets_liquidity_ceiling_b():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01"]),
            "instrument": ["AAA"],
            "close": [1.0],
            "volume": [np.nan],
            "market": [None],
            "currency": [None],
            "source": ["demo"],
            "dataset_id": ["test"],
        }
    )

    meta = build_metadata(df, source="demo", dataset_id="test")
    assert meta["liquidity_ceiling"] == "B"


def test_adj_close_accepted_when_close_missing():
    df = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "instrument": ["AAA", "AAA"],
            "adj_close": [1.0, 2.0],
        }
    )

    normalized, fmt = normalize_data(df, source="demo", dataset_id="test")
    assert fmt == "long"
    assert normalized["close"].tolist() == [1.0, 2.0]
