import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.analysis.readiness_gates import compute_readiness_metrics, evaluate_models, write_research_artifacts


def test_basic_readiness_metric_calculation_from_close_volume_data():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=30),
            "ticker": ["AAA"] * 30,
            "close": [10 + i * 0.1 for i in range(30)],
            "volume": [1000] * 28 + [700, 650],
            "signal_date": ["2025-01-05"] * 30,
        }
    )
    metrics = compute_readiness_metrics(df)
    row = metrics.iloc[0]
    assert row["trading_days_count"] == 30
    assert row["positive_volume_days"] == 30
    assert row["avg_volume_20d"] > 0
    assert pd.notna(row["close_to_close_volatility_20d"])


def test_missing_optional_rich_fields_do_not_crash():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=25),
            "ticker": ["BBB"] * 25,
            "close": [20.0] * 25,
            "volume": [0, 100] * 12 + [100],
            "signal_date": [None] * 25,
        }
    )
    metrics = compute_readiness_metrics(df)
    assert len(metrics) == 1
    assert not bool(metrics.iloc[0]["volatility_context_available"])


def test_model_b_classifies_trades_using_minimum_gate():
    df = pd.DataFrame(
        {
            "ticker": ["OK", "BAD"],
            "date": [pd.Timestamp("2025-02-01"), pd.Timestamp("2025-02-01")],
            "close": [10, 10],
            "volume": [1000, 0],
            "signal_date": ["2025-01-01", None],
        }
    )
    expanded = pd.concat([df[df["ticker"] == "OK"]] * 25 + [df[df["ticker"] == "BAD"]] * 25, ignore_index=True)
    metrics = compute_readiness_metrics(expanded)
    model_summary, detail = evaluate_models(metrics)
    b = detail[detail["model"] == "B_minimum"]
    assert b[b["ticker"] == "OK"]["funded"].iloc[0]
    assert not b[b["ticker"] == "BAD"]["funded"].iloc[0]
    assert "B_minimum" in set(model_summary["model"])


def test_model_c_reports_spread_limitation_when_high_low_unavailable():
    df = pd.DataFrame(
        {
            "date": pd.date_range("2025-01-01", periods=30),
            "ticker": ["AAA"] * 30,
            "close": [10 + i * 0.1 for i in range(30)],
            "volume": [1000] * 30,
            "signal_date": ["2025-01-05"] * 30,
        }
    )
    metrics = compute_readiness_metrics(df)
    _summary, detail = evaluate_models(metrics)
    strict_row = detail[detail["model"] == "C_strict"].iloc[0]
    assert strict_row["reason"] == "strict_spread_unavailable"


def test_output_files_created_in_expected_artifact_location(tmp_path):
    metrics = pd.DataFrame([{"ticker": "AAA"}])
    summary = pd.DataFrame([{"model": "A_current", "total_candidate_trades": 1}])
    by_model = pd.DataFrame([{"model": "A_current", "ticker": "AAA", "funded": True, "label": "Ready", "reason": "pass"}])

    write_research_artifacts(metrics, summary, by_model, tmp_path)

    assert (tmp_path / "readiness_gate_summary.csv").exists()
    assert (tmp_path / "readiness_gate_by_model.csv").exists()
    assert (tmp_path / "readiness_gate_by_ticker.csv").exists()
    assert (tmp_path / "readiness_gate_report.md").exists()
