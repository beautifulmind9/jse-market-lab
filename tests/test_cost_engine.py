import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.costs.config import resolve_cost_config
from app.costs.engine import run_cost_engine


def test_default_profile_round_trip_cost_rate():
    config = resolve_cost_config("Default")
    expected = (config["broker_fee"] + config["cess"]) * 2
    assert config["round_trip_cost_rate"] == expected


def test_costs_reduce_net_return():
    dates = pd.date_range("2024-01-01", periods=6, freq="D")
    df_prices = pd.DataFrame(
        {
            "date": dates,
            "instrument": ["AAA"] * 6,
            "close": [100, 101, 102, 103, 104, 110],
        }
    )
    df_entries = pd.DataFrame({"instrument": ["AAA"], "entry_date": [dates[0]]})

    trades, _, _, _ = run_cost_engine(
        df_prices,
        df_entries,
        holding_windows=[5],
        broker_profile="Default",
        override_enabled=True,
        broker_fee=0.005,
        cess=0.0,
    )

    assert len(trades) == 1
    gross = trades.iloc[0]["gross_return_pct"]
    net = trades.iloc[0]["net_return_pct"]
    assert round(gross, 6) == 10.0
    assert round(net, 6) == 9.0


def test_missing_dates_use_trading_calendar():
    dates = pd.to_datetime(
        ["2024-01-01", "2024-01-03", "2024-01-10", "2024-01-20", "2024-01-30", "2024-02-10"]
    )
    df_prices = pd.DataFrame(
        {
            "date": dates,
            "instrument": ["AAA"] * 6,
            "close": [100, 101, 102, 103, 104, 105],
        }
    )
    df_entries = pd.DataFrame({"instrument": ["AAA"], "entry_date": [dates[0]]})

    trades, _, _, _ = run_cost_engine(
        df_prices,
        df_entries,
        holding_windows=[5],
        broker_profile="Default",
        override_enabled=True,
        broker_fee=0.0,
        cess=0.0,
    )

    assert trades.iloc[0]["exit_date"] == dates[5]


def test_insufficient_future_data_excluded_from_summary():
    dates = pd.date_range("2024-01-01", periods=3, freq="D")
    df_prices = pd.DataFrame(
        {
            "date": dates,
            "instrument": ["AAA"] * 3,
            "close": [100, 101, 102],
        }
    )
    df_entries = pd.DataFrame({"instrument": ["AAA"], "entry_date": [dates[0]]})

    trades, summary_instrument, summary_overall, _ = run_cost_engine(
        df_prices,
        df_entries,
        holding_windows=[5],
        broker_profile="Default",
        override_enabled=True,
        broker_fee=0.0,
        cess=0.0,
    )

    assert trades.empty
    assert summary_instrument.empty
    assert summary_overall.empty


def test_duplicate_price_rows_raise_error():
    df_prices = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
            "instrument": ["AAA", "AAA"],
            "close": [100, 101],
        }
    )
    df_entries = pd.DataFrame(
        {"instrument": ["AAA"], "entry_date": [pd.Timestamp("2024-01-01")]}
    )

    try:
        run_cost_engine(
            df_prices,
            df_entries,
            holding_windows=[5],
            broker_profile="Default",
        )
        assert False, "Expected ValueError for duplicate prices."
    except ValueError as exc:
        assert "Duplicate (instrument, date) rows found in prices" in str(exc)
