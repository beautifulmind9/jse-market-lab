import sys
import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.shell import build_analyst_dataset


def test_build_analyst_dataset_returns_return_bearing_trades_with_quality_tier(monkeypatch):
    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "close": [10.0, 20.0],
            "volume": [1000, 900],
        }
    )
    ranked_df = pd.DataFrame({"instrument": ["AAA", "BBB"], "tier": ["A", "B"]})

    trades_stub = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB"],
            "holding_window": [10, 10],
            "net_return_pct": [0.02, -0.01],
        }
    )

    def fake_run_cost_engine(df_prices, df_entries):
        assert not df_prices.empty
        assert not df_entries.empty
        return trades_stub, pd.DataFrame(), None, None

    monkeypatch.setattr("app.shell.run_cost_engine", fake_run_cost_engine)

    analyst_df = build_analyst_dataset(canonical_df, ranked_df)

    assert "net_return_pct" in analyst_df.columns
    assert "quality_tier" in analyst_df.columns
    assert list(analyst_df["quality_tier"]) == ["A", "B"]


def test_build_analyst_dataset_handles_empty_ranked_df(monkeypatch):
    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "date": pd.to_datetime(["2024-01-01"]),
            "close": [10.0],
            "volume": [1000],
        }
    )

    trades_stub = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "holding_window": [10],
            "net_return_pct": [0.03],
        }
    )

    monkeypatch.setattr(
        "app.shell.run_cost_engine",
        lambda df_prices, df_entries: (trades_stub, pd.DataFrame(), None, None),
    )

    analyst_df = build_analyst_dataset(canonical_df, pd.DataFrame())

    assert "net_return_pct" in analyst_df.columns
    assert "quality_tier" not in analyst_df.columns


def test_build_analyst_dataset_does_not_filter_to_ranked_subset(monkeypatch):
    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB", "CCC"],
            "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-01"]),
            "close": [10.0, 20.0, 30.0],
            "volume": [1000, 900, 850],
        }
    )
    ranked_df = pd.DataFrame({"instrument": ["AAA"], "tier": ["A"]})
    trades_stub = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB", "CCC"],
            "holding_window": [10, 10, 10],
            "net_return_pct": [0.02, -0.01, 0.01],
        }
    )

    monkeypatch.setattr(
        "app.shell.run_cost_engine",
        lambda df_prices, df_entries: (trades_stub, pd.DataFrame(), None, None),
    )

    analyst_df = build_analyst_dataset(canonical_df, ranked_df)

    assert set(analyst_df["instrument"]) == {"AAA", "BBB", "CCC"}
    assert "quality_tier" in analyst_df.columns
    assert analyst_df.loc[analyst_df["instrument"] == "AAA", "quality_tier"].iat[0] == "A"
    assert analyst_df.loc[analyst_df["instrument"] == "BBB", "quality_tier"].isna().all()
    assert analyst_df.loc[analyst_df["instrument"] == "CCC", "quality_tier"].isna().all()


def test_extract_ticker_options_uses_active_dataset_and_is_sorted():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    canonical_df = pd.DataFrame(
        {
            "instrument": ["CCC", "AAA", "BBB", "AAA", None, " "],
            "date": pd.to_datetime(
                ["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]
            ),
            "close": [10.0, 11.0, 12.0, 13.0, 14.0, 15.0],
        }
    )

    ticker_options = app_main._extract_ticker_options(canonical_df)

    assert ticker_options == ["AAA", "BBB", "CCC"]


def test_extract_ticker_options_does_not_split_marker_variants():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    canonical_df = pd.DataFrame(
        {
            "instrument": ["CAR", "CARXD", "CAR (XD)", "GK", "GKXD", "GK (XD)"],
            "ticker": ["CAR", "CAR", "CAR", "GK", "GK", "GK"],
            "raw_symbol": ["CAR", "CARXD", "CAR (XD)", "GK", "GKXD", "GK (XD)"],
            "display_symbol": ["CAR", "CARXD", "CAR (XD)", "GK", "GKXD", "GK (XD)"],
        }
    )

    ticker_options = app_main._extract_ticker_options(canonical_df)

    assert ticker_options == ["CAR", "GK"]
