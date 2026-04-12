import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.analysis.ticker_intelligence import compute_ticker_metrics


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "instrument": ["NCB", "NCB", "NCB", "NCB", "NCB", "NCB", "NCB", "NCB", "JMMB"],
            "holding_window": [5, 5, 20, 20, 5, 20, 5, 20, 5],
            "net_return_pct": [0.02, -0.01, 0.03, 0.01, 0.00, -0.02, 0.01, 0.02, 0.04],
            "quality_tier": ["A", "A", "B", "B", "A", "B", "A", "B", "A"],
        }
    )


def test_compute_ticker_metrics_returns_required_structure():
    payload = compute_ticker_metrics(_sample_df(), "NCB")

    assert set(payload.keys()) == {"summary", "stats", "behavior", "execution"}
    assert set(payload["stats"].keys()) == {
        "win_rate",
        "median_return",
        "avg_return",
        "best_window",
        "signal_count",
    }
    assert set(payload["behavior"].keys()) == {
        "holding_window",
        "consistency",
        "reliability",
        "tier_profile",
    }
    assert set(payload["execution"].keys()) == {
        "entry_reference",
        "planned_exit",
        "typical_outcome",
        "execution_risk",
        "summary",
    }


def test_compute_ticker_metrics_generates_summary_with_best_window():
    payload = compute_ticker_metrics(_sample_df(), "NCB")

    assert "This setup has worked well in the past." in payload["summary"]
    assert "closed positive in 62% of signals" in payload["summary"]


def test_compute_ticker_metrics_uses_neutral_beginner_wording_for_weak_win_rate():
    df = pd.DataFrame(
        {
            "instrument": ["TEST"] * 6,
            "holding_window": [5, 5, 5, 20, 20, 20],
            "net_return_pct": [-0.02, -0.01, 0.01, -0.03, 0.01, -0.01],
        }
    )

    payload = compute_ticker_metrics(df, "TEST", mode="beginner")

    assert "This setup has been less consistent." in payload["summary"]
    assert "closed positive in 33% of signals" in payload["summary"]


def test_compute_ticker_metrics_flags_low_sample_size_in_summary():
    df = pd.DataFrame(
        {
            "instrument": ["TEST", "TEST", "TEST"],
            "holding_window": [5, 20, 5],
            "net_return_pct": [0.01, -0.01, 0.02],
        }
    )

    payload = compute_ticker_metrics(df, "TEST")

    assert payload["stats"]["signal_count"] == 3
    assert "only 3 signals" in payload["summary"]


def test_compute_ticker_metrics_handles_missing_data():
    df = pd.DataFrame({"instrument": ["AAA"], "holding_window": [5]})

    payload = compute_ticker_metrics(df, "AAA")

    assert payload["stats"]["signal_count"] == 0
    assert payload["stats"]["best_window"] == "N/A"
    assert "No clean return data" in payload["summary"]


def test_compute_ticker_metrics_scopes_to_canonical_ticker_with_marker_variants():
    df = pd.DataFrame(
        {
            "instrument": ["CAR", "CARXD", "CAR XD", "CAR (XD)", "GK"],
            "holding_window": [5, 20, 5, 20, 5],
            "net_return_pct": [0.01, 0.02, -0.01, 0.015, 0.04],
        }
    )

    payload = compute_ticker_metrics(df, "CAR")

    assert payload["stats"]["signal_count"] == 4
