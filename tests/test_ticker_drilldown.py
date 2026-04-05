import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.analysis.ticker_drilldown import (
    build_ticker_drilldown,
    compute_holding_window_stats,
    compute_return_distribution,
    compute_signal_breakdown,
    compute_tier_performance,
    compute_volatility_performance,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB", "NCB", "JMMB"],
            "date": pd.to_datetime(
                [
                    "2025-01-01",
                    "2025-01-10",
                    "2025-02-01",
                    "2025-02-12",
                    "2025-03-01",
                    "2025-01-08",
                ]
            ),
            "holding_window": [5, 5, 20, 20, 5, 5],
            "net_return_pct": [2.0, -1.0, 4.0, 1.0, 0.0, 3.0],
            "quality_tier": ["A", "B", "A", "C", "A", "B"],
            "volatility_bucket": ["low", "mid", "mid", "high", "low", "mid"],
        }
    )


def test_compute_signal_breakdown_extracts_selected_ticker_and_win_loss():
    signals = compute_signal_breakdown(_sample_df(), "NCB")

    assert len(signals) == 5
    assert signals[0]["date"] == "2025-03-01"
    assert all(row.get("quality_tier") in {"A", "B", "C"} for row in signals)
    assert {row["win_loss"] for row in signals if "win_loss" in row} == {"Win", "Loss"}


def test_compute_holding_window_stats_groups_rows_correctly():
    stats = compute_holding_window_stats(_sample_df(), "NCB")

    assert set(stats.keys()) == {"5D", "20D"}
    assert stats["5D"]["count"] == 3
    assert stats["20D"]["count"] == 2
    assert round(stats["20D"]["win_rate"], 2) == 1.0


def test_compute_return_distribution_buckets_values():
    distribution = compute_return_distribution(_sample_df(), "NCB")

    assert distribution == {"negative": 2, "small_positive": 2, "strong_positive": 1}


def test_compute_tier_performance_groups_by_quality_tier():
    tier_stats = compute_tier_performance(_sample_df(), "NCB")

    assert set(tier_stats.keys()) == {"A", "B", "C"}
    assert tier_stats["A"]["count"] == 3
    assert round(tier_stats["C"]["avg_return"], 2) == 1.0


def test_compute_volatility_performance_groups_by_bucket():
    vol_stats = compute_volatility_performance(_sample_df(), "NCB")

    assert set(vol_stats.keys()) == {"low", "mid", "high"}
    assert vol_stats["mid"]["count"] == 2


def test_build_ticker_drilldown_low_sample_summary():
    df = pd.DataFrame(
        {
            "instrument": ["AAA", "AAA"],
            "holding_window": [5, 20],
            "net_return_pct": [1.0, -2.0],
        }
    )

    payload = build_ticker_drilldown(df, "AAA")

    assert "not much data" in payload["pattern_summary"].lower()


def test_build_ticker_drilldown_handles_missing_columns_gracefully():
    df = pd.DataFrame({"instrument": ["AAA", "AAA"], "date": ["2025-01-01", "2025-01-02"]})

    payload = build_ticker_drilldown(df, "AAA")

    assert payload["holding_window_stats"] == {}
    assert payload["tier_performance"] == {}
    assert payload["volatility_performance"] == {}
    assert payload["return_distribution"] == {"negative": 0, "small_positive": 0, "strong_positive": 0}
    assert len(payload["signals"]) == 2


def test_build_ticker_drilldown_handles_empty_dataframe():
    payload = build_ticker_drilldown(pd.DataFrame(), "AAA")

    assert payload["signals"] == []
    assert payload["holding_window_stats"] == {}
    assert payload["return_distribution"] == {"negative": 0, "small_positive": 0, "strong_positive": 0}
    assert payload["tier_performance"] == {}
    assert payload["volatility_performance"] == {}
    assert "not enough data" in payload["pattern_summary"].lower()


def test_build_ticker_drilldown_output_structure():
    payload = build_ticker_drilldown(_sample_df(), "NCB")

    assert set(payload.keys()) == {
        "signals",
        "holding_window_stats",
        "return_distribution",
        "tier_performance",
        "volatility_performance",
        "pattern_summary",
    }


def _sample_df_with_alias(return_column: str) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB", "JMMB"],
            "holding_window": [5, 5, 20, 20, 5],
            return_column: [2.0, -1.0, 4.0, 1.0, 3.0],
            "quality_tier": ["A", "B", "A", "C", "B"],
            "volatility_bucket": ["low", "mid", "mid", "high", "mid"],
        }
    )


def test_return_column_alias_resolution_supports_net_return():
    df = _sample_df_with_alias("net_return")

    signals = compute_signal_breakdown(df, "NCB")
    holding = compute_holding_window_stats(df, "NCB")
    distribution = compute_return_distribution(df, "NCB")
    tier = compute_tier_performance(df, "NCB")
    volatility = compute_volatility_performance(df, "NCB")

    assert len(signals) == 4
    assert holding["5D"]["count"] == 2
    assert distribution == {"negative": 1, "small_positive": 2, "strong_positive": 1}
    assert tier["A"]["count"] == 2
    assert volatility["mid"]["count"] == 2


def test_return_column_alias_resolution_supports_return():
    df = _sample_df_with_alias("return")

    signals = compute_signal_breakdown(df, "NCB")
    holding = compute_holding_window_stats(df, "NCB")
    distribution = compute_return_distribution(df, "NCB")
    tier = compute_tier_performance(df, "NCB")
    volatility = compute_volatility_performance(df, "NCB")

    assert len(signals) == 4
    assert holding["20D"]["count"] == 2
    assert distribution == {"negative": 1, "small_positive": 2, "strong_positive": 1}
    assert tier["C"]["count"] == 1
    assert volatility["high"]["count"] == 1


def test_return_distribution_uses_percentage_point_cutoffs_for_all_aliases():
    expected = {"negative": 2, "small_positive": 2, "strong_positive": 2}
    base = {
        "instrument": ["NCB", "NCB", "NCB", "NCB", "NCB", "NCB"],
        "values": [-2.0, 0.0, 0.5, 2.99, 3.0, 7.5],
    }

    for column in ["net_return_pct", "return_pct", "net_return", "return"]:
        df = pd.DataFrame({"instrument": base["instrument"], column: base["values"]})
        distribution = compute_return_distribution(df, "NCB")
        assert distribution == expected


def test_metrics_stay_empty_safe_when_no_supported_return_alias_exists():
    df = pd.DataFrame(
        {
            "instrument": ["NCB", "NCB"],
            "holding_window": [5, 20],
            "quality_tier": ["A", "B"],
            "volatility_bucket": ["low", "high"],
            "gross_return": [1.2, -0.5],
        }
    )

    signals = compute_signal_breakdown(df, "NCB")
    holding = compute_holding_window_stats(df, "NCB")
    distribution = compute_return_distribution(df, "NCB")
    tier = compute_tier_performance(df, "NCB")
    volatility = compute_volatility_performance(df, "NCB")

    assert all("return_pct" not in row and "win_loss" not in row for row in signals)
    assert holding == {}
    assert distribution == {"negative": 0, "small_positive": 0, "strong_positive": 0}
    assert tier == {}
    assert volatility == {}
