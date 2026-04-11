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
            return_column: [0.02, -0.01, 0.04, 0.01, 0.03],
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
    pct_expected = {"negative": 2, "small_positive": 2, "strong_positive": 2}
    pct_values = [-2.0, 0.0, 0.5, 2.99, 3.0, 7.5]

    for column in ["net_return_pct", "return_pct"]:
        df = pd.DataFrame({"instrument": ["NCB"] * 6, column: pct_values})
        distribution = compute_return_distribution(df, "NCB")
        assert distribution == pct_expected

    fractional_expected = {"negative": 2, "small_positive": 2, "strong_positive": 2}
    fractional_values = [-0.02, 0.0, 0.005, 0.0299, 0.03, 0.075]

    for column in ["net_return", "return"]:
        df = pd.DataFrame({"instrument": ["NCB"] * 6, column: fractional_values})
        distribution = compute_return_distribution(df, "NCB")
        assert distribution == fractional_expected


def test_return_column_priority_prefers_net_return_before_return_pct():
    df = pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB"],
            "net_return": [0.01, -0.01, 0.05, 0.02],
            "return_pct": [100.0, 100.0, 100.0, 100.0],
        }
    )

    distribution = compute_return_distribution(df, "NCB")

    assert distribution == {"negative": 1, "small_positive": 2, "strong_positive": 1}


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


def _equivalent_alias_df(return_column: str) -> pd.DataFrame:
    percent_point_returns = [2.5, -1.0, 3.5, 1.0]
    returns = (
        [value / 100.0 for value in percent_point_returns]
        if return_column in {"net_return", "return"}
        else percent_point_returns
    )
    return pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB"],
            "holding_window": [5, 5, 20, 20],
            "quality_tier": ["A", "B", "A", "C"],
            "volatility_bucket": ["low", "mid", "mid", "high"],
            return_column: returns,
        }
    )


def test_drilldown_outputs_are_schema_consistent_across_return_aliases():
    aliases = ["net_return_pct", "net_return", "return_pct", "return"]
    payloads = {alias: build_ticker_drilldown(_equivalent_alias_df(alias), "NCB") for alias in aliases}

    def _rounded_stats(stats: dict[str, dict[str, float | int]]) -> dict[str, dict[str, float | int]]:
        rounded: dict[str, dict[str, float | int]] = {}
        for bucket, values in stats.items():
            rounded[bucket] = {
                key: (round(float(value), 8) if isinstance(value, float) else value) for key, value in values.items()
            }
        return rounded

    baseline = payloads["net_return_pct"]
    for alias in aliases[1:]:
        assert len(payloads[alias]["signals"]) == len(baseline["signals"])
        for candidate_signal, baseline_signal in zip(payloads[alias]["signals"], baseline["signals"], strict=True):
            assert candidate_signal.keys() == baseline_signal.keys()
            for key in candidate_signal:
                if key == "return_pct":
                    assert round(float(candidate_signal[key]), 8) == round(float(baseline_signal[key]), 8)
                else:
                    assert candidate_signal[key] == baseline_signal[key]
        assert _rounded_stats(payloads[alias]["holding_window_stats"]) == _rounded_stats(baseline["holding_window_stats"])
        assert payloads[alias]["return_distribution"] == baseline["return_distribution"]
        assert _rounded_stats(payloads[alias]["tier_performance"]) == _rounded_stats(baseline["tier_performance"])
        assert _rounded_stats(payloads[alias]["volatility_performance"]) == _rounded_stats(
            baseline["volatility_performance"]
        )
        assert payloads[alias]["pattern_summary"] == baseline["pattern_summary"]


def _pattern_window_df(return_column: str, five_day_returns_pct: list[float], twenty_day_returns_pct: list[float]) -> pd.DataFrame:
    all_returns_pct = five_day_returns_pct + twenty_day_returns_pct
    returns = (
        [value / 100.0 for value in all_returns_pct]
        if return_column in {"net_return", "return"}
        else all_returns_pct
    )
    return pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB"],
            "holding_window": [5, 5, 20, 20],
            "quality_tier": ["A", "A", "A", "A"],
            "volatility_bucket": ["mid", "mid", "mid", "mid"],
            return_column: returns,
        }
    )


def test_pattern_summary_holding_window_threshold_does_not_trigger_below_point_three_pct():
    aliases = ["net_return_pct", "return_pct", "net_return", "return"]

    for alias in aliases:
        df = _pattern_window_df(
            return_column=alias,
            five_day_returns_pct=[1.0, 3.0],   # median 2.0
            twenty_day_returns_pct=[1.8, 1.8],  # median 1.8 (delta 0.2)
        )
        payload = build_ticker_drilldown(df, "NCB")
        assert "tends to hold up better on" not in payload["pattern_summary"]


def test_pattern_summary_holding_window_threshold_triggers_above_point_three_pct():
    aliases = ["net_return_pct", "return_pct", "net_return", "return"]

    for alias in aliases:
        df = _pattern_window_df(
            return_column=alias,
            five_day_returns_pct=[1.0, 3.0],   # median 2.0
            twenty_day_returns_pct=[1.5, 1.7],  # median 1.6 (delta 0.4)
        )
        payload = build_ticker_drilldown(df, "NCB")
        assert "looked stronger on 5D than 20D" in payload["pattern_summary"]
