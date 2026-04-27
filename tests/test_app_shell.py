import sys
import importlib.util
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked


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


def test_coerce_trade_rows_from_ranked_preserves_holding_window_values():
    ranked_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB", "CCC", "DDD"],
            "tier": ["A", "B", "A", "B"],
            "holding_window": [10, None, None, -5],
            "best_window": [None, "20D", "30 trading days", None],
        }
    )

    rows = coerce_trade_rows_from_ranked(ranked_df)

    assert rows[0]["holding_window"] == 10
    assert rows[1]["holding_window"] == 20
    assert rows[2]["holding_window"] == 30
    assert rows[3]["holding_window"] is None


def test_coerce_trade_rows_from_ranked_skips_non_positive_holding_window_for_fallback_fields():
    ranked_df = pd.DataFrame(
        {
            "instrument": ["AAA", "BBB", "CCC", "DDD"],
            "tier": ["A", "B", "A", "B"],
            "holding_window": [0, -1, None, 0],
            "best_window": ["20D", None, None, "0D"],
            "window": [None, 30, None, None],
            "holding_period": [None, None, "10 trading days", "0 trading days"],
        }
    )

    rows = coerce_trade_rows_from_ranked(ranked_df)

    assert rows[0]["holding_window"] == 20
    assert rows[1]["holding_window"] == 30
    assert rows[2]["holding_window"] == 10
    assert rows[3]["holding_window"] is None


def test_freeze_and_unfreeze_issues_round_trip():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    issues = {"warnings": ["w1", "w2"], "errors": ["e1"]}

    frozen = app_main._freeze_issues(issues)
    restored = app_main._unfreeze_issues(frozen)

    assert restored == issues


def test_dataset_period_description_uses_date_range_when_available():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    df = pd.DataFrame({"date": pd.to_datetime(["2020-01-01", "2024-12-31", None])})
    assert app_main._resolve_dataset_period_description(df) == (
        "Using historical JSE data from 2020-01-01 to 2024-12-31 in the current dataset."
    )


def test_app_no_long_hard_coded_data_period_copy():
    source = (ROOT / "app.py").read_text()
    assert "since 2018 where available" not in source


def test_trade_readiness_signal_timing_falls_back_to_canonical_market_date():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA", "AAA"],
            "date": ["2024-01-10", "2024-01-11"],
            "volume": [1000, 1200],
        }
    )
    analyst_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "liquidity_pass": [True],
        }
    )

    lines = app_main._build_trade_readiness_lines(
        canonical_df=canonical_df,
        analyst_df=analyst_df,
        selected_ticker="AAA",
        ticker_payload={},
        metrics_stats={},
    )

    assert "Signal timing: Not yet assessed" in lines


def test_trade_readiness_signal_timing_unavailable_when_no_parseable_dates():
    spec = importlib.util.spec_from_file_location("app_main", ROOT / "app.py")
    app_main = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(app_main)

    canonical_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "date": ["not-a-date"],
            "volume": [1000],
        }
    )
    analyst_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "signal_date": ["still-not-a-date"],
        }
    )

    lines = app_main._build_trade_readiness_lines(
        canonical_df=canonical_df,
        analyst_df=analyst_df,
        selected_ticker="AAA",
        ticker_payload={},
        metrics_stats={},
    )

    assert "Signal timing: Signal date unavailable" in lines
