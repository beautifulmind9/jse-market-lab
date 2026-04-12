import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.data.metadata import build_metadata
from app.data.loaders import (
    INTERNAL_DATASET_PATH,
    get_internal_dataset_source_label,
    load_internal_dataset,
    load_internal_dataset_with_source,
)
from app.data.normalize import detect_format, normalize_data
from app.data.ingest import ingest_dataset
from app.data.validate import validate_canonical
from app.data.processor import normalize_jse_dataset


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

    loaded = load_internal_dataset()
    source_label = get_internal_dataset_source_label()

    assert "ticker" in loaded.columns
    assert "instrument" in loaded.columns
    pd.testing.assert_series_equal(
        loaded["instrument"],
        loaded["ticker"],
        check_names=False,
    )
    assert source_label in {"internal_jse_dataset", "legacy_demo_dataset"}
    assert isinstance(loaded, pd.DataFrame)
    assert not isinstance(loaded, tuple)


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

    _, source_label = load_internal_dataset_with_source()

    assert calls == [bundled_path]
    assert source_label == "internal_jse_dataset"


def test_internal_loader_uses_real_bundled_dataset_when_available():
    assert INTERNAL_DATASET_PATH.as_posix().endswith("data/internal/jse_dataset.csv")
    assert INTERNAL_DATASET_PATH.exists()

    loaded = load_internal_dataset()
    source_label = get_internal_dataset_source_label()

    assert source_label == "internal_jse_dataset"
    assert len(loaded) > 1000


def test_internal_loader_real_bundled_dataset_has_more_than_legacy_ticker_universe():
    loaded = load_internal_dataset()
    ticker_count = int(loaded["instrument"].dropna().astype(str).nunique())

    assert ticker_count > 9


def test_demo_ingestion_preserves_large_ticker_universe_from_internal_dataset():
    loaded = load_internal_dataset()
    canonical, _meta, _issues = ingest_dataset("demo")

    loaded_tickers = int(loaded["instrument"].dropna().astype(str).nunique())
    canonical_tickers = int(canonical["instrument"].dropna().astype(str).nunique())

    assert loaded_tickers > 9
    assert canonical_tickers > 9
    assert canonical_tickers >= int(loaded_tickers * 0.8)


def test_jse_symbol_markers_normalize_to_canonical_ticker():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"],
            "symbol": ["CAR", "CARXD", "GK", "GKXD", "CAR (XD)", "GK (XD)"],
            "close_price": [10.0, 10.1, 8.0, 8.2, 10.3, 8.3],
            "volume": [1000, 900, 1100, 950, 980, 920],
        }
    )

    normalized = normalize_jse_dataset(raw)

    car_rows = normalized[normalized["raw_symbol"].str.startswith("CAR")]
    gk_rows = normalized[normalized["raw_symbol"].str.startswith("GK")]
    assert set(car_rows["ticker"]) == {"CAR"}
    assert set(gk_rows["ticker"]) == {"GK"}
    assert set(normalized["instrument"]) == {"CAR", "GK"}


def test_demo_ingestion_collapses_marker_variants_to_single_instrument(monkeypatch):
    sample_raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-03"],
            "symbol": ["CAR", "CARXD", "GK", "GKXD", "CAR (XD)", "GK (XD)"],
            "close_price": [10.0, 10.2, 8.0, 8.1, 10.3, 8.2],
            "volume": [1000, 1200, 900, 950, 980, 930],
        }
    )
    monkeypatch.setattr("app.data.loaders.pd.read_csv", lambda *_args, **_kwargs: sample_raw)

    canonical, _meta, _issues = ingest_dataset("demo")
    assert set(canonical["instrument"]) == {"CAR", "GK"}
    assert "display_symbol" in canonical.columns
    assert set(canonical["raw_symbol"]) == {"CAR", "CARXD", "CAR (XD)", "GK", "GKXD", "GK (XD)"}


def test_normalize_data_collapses_marker_variants_to_single_canonical_ticker():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-01", "2024-01-03"],
            "instrument": ["CAR", "CARXD", "CAR XD", "CAR (XD)"],
            "close": [10.0, 10.1, 10.2, 10.4],
        }
    )

    canonical, fmt = normalize_data(raw, source="upload", dataset_id="dataset-1")

    assert fmt == "long"
    assert set(canonical["ticker"]) == {"CAR"}
    assert set(canonical["instrument"]) == {"CAR"}


def test_normalize_data_parenthesized_gk_xd_maps_to_gk():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "instrument": ["GK", "GK (XD)"],
            "close": [8.0, 8.1],
        }
    )

    canonical, fmt = normalize_data(raw, source="upload", dataset_id="dataset-2")

    assert fmt == "long"
    assert set(canonical["ticker"]) == {"GK"}
    assert set(canonical["instrument"]) == {"GK"}


def test_normalize_data_preserves_existing_raw_symbol_metadata_in_long_format():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
            "instrument": ["CAR", "CAR", "CAR"],
            "ticker": ["CAR", "CAR", "CAR"],
            "raw_symbol": ["CAR", "CARXD", "CAR (XD)"],
            "symbol_marker": [None, "XD", "XD"],
            "display_symbol": ["CAR", "CARXD", "CAR (XD)"],
            "close": [10.0, 10.1, 10.2],
        }
    )

    canonical, fmt = normalize_data(raw, source="demo", dataset_id="dataset-preserve-1")

    assert fmt == "long"
    assert canonical["ticker"].tolist() == ["CAR", "CAR", "CAR"]
    assert canonical["instrument"].tolist() == ["CAR", "CAR", "CAR"]
    assert canonical["raw_symbol"].tolist() == ["CAR", "CARXD", "CAR (XD)"]
    assert canonical["symbol_marker"].tolist() == [None, "XD", "XD"]
    assert canonical["display_symbol"].tolist() == ["CAR", "CARXD", "CAR (XD)"]


def test_normalize_data_preserves_parenthesized_xd_metadata_with_canonical_ticker():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "instrument": ["CAR"],
            "raw_symbol": ["CAR (XD)"],
            "symbol_marker": ["XD"],
            "display_symbol": ["CAR (XD)"],
            "close": [10.3],
        }
    )

    canonical, _fmt = normalize_data(raw, source="demo", dataset_id="dataset-preserve-2")
    row = canonical.iloc[0]

    assert row["ticker"] == "CAR"
    assert row["instrument"] == "CAR"
    assert row["raw_symbol"] == "CAR (XD)"
    assert row["symbol_marker"] == "XD"
    assert row["display_symbol"] == "CAR (XD)"




def test_normalize_data_nullable_string_raw_symbol_na_falls_back_to_canonical_metadata():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "instrument": ["CAR (XD)"],
            "raw_symbol": pd.Series([pd.NA], dtype="string"),
            "symbol_marker": pd.Series([pd.NA], dtype="string"),
            "display_symbol": pd.Series([pd.NA], dtype="string"),
            "close": [10.3],
        }
    )

    canonical, fmt = normalize_data(raw, source="demo", dataset_id="dataset-preserve-nullable")
    row = canonical.iloc[0]

    assert fmt == "long"
    assert row["ticker"] == "CAR"
    assert row["instrument"] == "CAR"
    assert row["raw_symbol"] == "CAR (XD)"
    assert row["symbol_marker"] == "XD"
    assert row["display_symbol"] == "CAR (XD)"


def test_normalize_data_string_missing_tokens_fall_back_for_optional_symbol_metadata():
    raw = pd.DataFrame(
        {
            "date": [
                "2024-01-01",
                "2024-01-02",
                "2024-01-03",
                "2024-01-04",
            ],
            "instrument": ["CAR (XD)", "CAR (XD)", "CAR (XD)", "CAR (XD)"],
            "raw_symbol": ["", "nan", "none", "<NA>"],
            "symbol_marker": ["", "nan", "none", "<NA>"],
            "display_symbol": ["", "nan", "none", "<NA>"],
            "close": [10.3, 10.4, 10.5, 10.6],
        }
    )

    canonical, _fmt = normalize_data(raw, source="demo", dataset_id="dataset-preserve-missing-tokens")

    assert set(canonical["ticker"]) == {"CAR"}
    assert set(canonical["instrument"]) == {"CAR"}
    assert canonical["raw_symbol"].tolist() == ["CAR (XD)", "CAR (XD)", "CAR (XD)", "CAR (XD)"]
    assert canonical["symbol_marker"].tolist() == ["XD", "XD", "XD", "XD"]
    assert canonical["display_symbol"].tolist() == ["CAR (XD)", "CAR (XD)", "CAR (XD)", "CAR (XD)"]

def test_normalize_data_keeps_canonical_universe_collapsed_when_raw_metadata_varies():
    raw = pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
            "instrument": ["CAR", "CAR", "CAR", "CAR"],
            "raw_symbol": ["CAR", "CARXD", "CAR (XD)", "CAR XD"],
            "symbol_marker": [None, "XD", "XD", "XD"],
            "display_symbol": ["CAR", "CARXD", "CAR (XD)", "CAR XD"],
            "close": [10.0, 10.1, 10.2, 10.3],
        }
    )

    canonical, _fmt = normalize_data(raw, source="demo", dataset_id="dataset-preserve-3")

    assert set(canonical["ticker"]) == {"CAR"}
    assert set(canonical["instrument"]) == {"CAR"}
    assert canonical["raw_symbol"].nunique() == 4
    assert canonical["display_symbol"].tolist() == ["CAR", "CARXD", "CAR (XD)", "CAR XD"]
