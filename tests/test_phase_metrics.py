import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.metrics.phase_metrics import compute_phase_metrics


def test_phase_metrics_threshold_and_stats():
    df = pd.DataFrame(
        {
            "instrument": ["AAA"] * 12 + ["BBB"] * 5,
            "earnings_phase": ["reaction"] * 12 + ["post"] * 5,
            "net_return": [0.02] * 6 + [-0.01] * 6 + [0.03] * 5,
        }
    )

    metrics = compute_phase_metrics(
        df, ["instrument", "earnings_phase"], "net_return"
    )

    aaa = metrics[metrics["instrument"] == "AAA"].iloc[0]
    assert aaa["n"] == 12
    assert bool(aaa["insufficient_history"]) is False
    assert aaa["win_rate"] == 0.5
    assert aaa["median_return"] == 0.005

    bbb = metrics[metrics["instrument"] == "BBB"].iloc[0]
    assert bbb["n"] == 5
    assert bool(bbb["insufficient_history"]) is True
