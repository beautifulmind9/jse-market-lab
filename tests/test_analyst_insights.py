import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.analyst import (
    build_exit_analysis,
    build_feature_insights,
    build_performance_matrix,
    grouped_trade_metrics,
    resolve_return_column,
)


def _sample_trades() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "quality_tier": ["A", "A", "B", "B"],
            "holding_window": [5, 10, 5, 10],
            "net_return_pct": [0.02, -0.01, 0.03, 0.01],
            "fast_slope_up": [True, True, False, False],
            "vol_bucket": ["low", "high", "high", "low"],
            "exit_reason": ["target_hit", "stop_hit", "target_hit", "time_exit"],
        }
    )


def test_grouped_trade_metrics_generates_expected_columns_and_values():
    summary = grouped_trade_metrics(
        _sample_trades(),
        ["quality_tier"],
        return_column="net_return_pct",
    )

    assert list(summary.columns) == [
        "quality_tier",
        "count",
        "win_rate",
        "avg_return",
        "median_return",
    ]

    row_a = summary[summary["quality_tier"] == "A"].iloc[0]
    assert row_a["count"] == 2
    assert row_a["win_rate"] == 0.5
    assert row_a["median_return"] == 0.005


def test_grouped_trade_metrics_raises_for_missing_columns():
    with pytest.raises(ValueError, match="Missing required columns"):
        grouped_trade_metrics(
            _sample_trades().drop(columns=["quality_tier"]),
            ["quality_tier"],
            return_column="net_return_pct",
        )


def test_feature_insights_only_returns_available_features():
    insights = build_feature_insights(
        _sample_trades().drop(columns=["fast_slope_up"]),
        return_column="net_return_pct",
    )

    assert "fast_slope_up" not in insights
    assert "vol_bucket" in insights


def test_performance_matrix_pivots_are_stable():
    payload = build_performance_matrix(_sample_trades(), return_column="net_return_pct")

    assert list(payload["summary"].columns) == [
        "quality_tier",
        "holding_window",
        "n_trades",
        "win_rate",
        "avg_return",
        "median_return",
    ]
    assert payload["win_rate_matrix"].shape == (2, 2)
    assert payload["median_return_matrix"].shape == (2, 2)


def test_exit_analysis_groups_by_quality_and_reason_and_window_when_available():
    summary = build_exit_analysis(_sample_trades(), return_column="net_return_pct")

    assert {"quality_tier", "exit_reason", "holding_window"}.issubset(summary.columns)


def test_resolve_return_column_finds_preferred_choice():
    df = pd.DataFrame({"return": [0.1]})
    assert resolve_return_column(df) == "return"
    assert resolve_return_column(pd.DataFrame({"x": [1]})) is None


class _DummyTab:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyStreamlitInsights:
    def __init__(self):
        self.calls = []

    def tabs(self, labels):
        self.calls.append(("tabs", tuple(labels)))
        return (_DummyTab(), _DummyTab(), _DummyTab())

    def subheader(self, text):
        self.calls.append(("subheader", text))

    def markdown(self, text):
        self.calls.append(("markdown", text))

    def dataframe(self, payload):
        self.calls.append(("dataframe", payload))

    def info(self, text):
        self.calls.append(("info", text))


def test_render_analyst_insights_handles_missing_quality_tier_for_exit_analysis():
    from app.insights.analyst import render_analyst_insights

    st = DummyStreamlitInsights()
    trades = _sample_trades().drop(columns=["quality_tier"])

    render_analyst_insights(trades, st_module=st, analyst_mode=True)

    assert (
        "info",
        "Exit Analysis unavailable — missing required columns: quality_tier",
    ) in st.calls


def test_render_analyst_insights_shows_exit_dataframe_when_required_columns_exist():
    from app.insights.analyst import render_analyst_insights

    st = DummyStreamlitInsights()

    render_analyst_insights(_sample_trades(), st_module=st, analyst_mode=True)

    exit_section_index = st.calls.index(("subheader", "Exit Analysis"))
    dataframes_after_exit_header = [
        call for call in st.calls[exit_section_index + 1 :] if call[0] == "dataframe"
    ]

    assert dataframes_after_exit_header
