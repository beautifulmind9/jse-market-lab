import sys
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
