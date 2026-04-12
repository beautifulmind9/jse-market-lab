import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.data.metadata import build_metadata
from app.data.loaders import INTERNAL_DATASET_PATH, load_internal_dataset
from app.data.normalize import detect_format, normalize_data
from app.data.ingest import ingest_dataset
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


def test_internal_loader_returns_ticker_and_instrument_columns(monkeypatch):
    sample_raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "symbol": ["AAA", "AAA"],
            "close_price": [10.0, 10.5],
            "volume": [1000, 1200],
        }
    )
    monkeypatch.setattr("app.data.loaders.pd.read_csv", lambda *_args, **_kwargs: sample_raw)

    loaded, source_label = load_internal_dataset()

    assert "ticker" in loaded.columns
    assert "instrument" in loaded.columns
    pd.testing.assert_series_equal(
        loaded["instrument"],
        loaded["ticker"],
        check_names=False,
    )
    assert source_label in {"internal_jse_dataset", "legacy_demo_dataset"}


def test_demo_ingestion_path_accepts_internal_loader_compatibility_contract(monkeypatch):
    sample_raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "symbol": ["AAA", "AAA"],
            "close_price": [10.0, 10.5],
            "volume": [1000, 1200],
        }
    )
    monkeypatch.setattr("app.data.loaders.pd.read_csv", lambda *_args, **_kwargs: sample_raw)

    canonical, meta, issues = ingest_dataset("demo")

    assert not canonical.empty
    assert "instrument" in canonical.columns
    assert meta["source"] == "demo"
    assert "errors" in issues and "warnings" in issues


def test_internal_loader_prefers_bundled_jse_dataset(monkeypatch, tmp_path):
    calls = []
    sample_raw = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "symbol": ["AAA"],
            "close_price": [10.0],
            "volume": [1000],
        }
    )

    bundled_path = tmp_path / "jse_dataset.csv"
    legacy_path = tmp_path / "jse_sample.csv"
    bundled_path.write_text("date,symbol,close_price,volume\n")
    legacy_path.write_text("date,symbol,close_price,volume\n")

    monkeypatch.setattr("app.data.loaders.pd.read_csv", lambda path: calls.append(path) or sample_raw)
    monkeypatch.setattr("app.data.loaders.INTERNAL_DATASET_PATH", bundled_path)
    monkeypatch.setattr("app.data.loaders.LEGACY_INTERNAL_DATASET_PATH", legacy_path)

    _, source_label = load_internal_dataset()

    assert calls == [bundled_path]
    assert source_label == "internal_jse_dataset"
