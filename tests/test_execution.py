import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.execution import build_execution_summary
from app.language.formatter import contains_advisory_language


def test_execution_summary_contains_entry_exit_typical_and_risk_sections():
    payload = build_execution_summary(
        {
            "allocation_amount": 2500,
            "signal_day_close": 12.34,
            "holding_window": 10,
            "median_return": 0.015,
            "avg_return": 0.016,
            "spread_context": "wide",
        }
    )

    assert "signal-day close" in payload["entry_reference"]
    assert "10 trading days" in payload["planned_exit"]
    assert "median return" in payload["typical_outcome"]
    assert "spread" in payload["execution_risk"]


def test_median_is_primary_and_average_is_supporting_context():
    payload = build_execution_summary(
        {
            "holding_window": 5,
            "median_return": 0.01,
            "avg_return": 0.03,
        },
        mode="analyst",
    )

    text = payload["typical_outcome"]
    assert text.startswith("Typical result is centered on median return")
    assert "Supporting average return is" in text
    assert "few larger moves may be influencing the average" in text


def test_execution_copy_has_no_predictive_or_advisory_language():
    payload = build_execution_summary(
        {
            "allocation_amount": 0,
            "holding_window": 20,
            "median_return": 0.012,
            "avg_return": 0.011,
            "liquidity_pass": False,
        }
    )

    blob = " ".join(payload.values())
    assert contains_advisory_language(blob) is False
    assert "guaranteed fill" in payload["entry_reference"]
