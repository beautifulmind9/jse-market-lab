import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.earnings_warnings import add_planner_earnings_warnings


def test_earnings_warning_copy_is_standardized_single_sentence():
    planner_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "entry_date": [pd.Timestamp("2024-01-02")],
            "holding_window": [1],
        }
    )
    prices_df = pd.DataFrame(
        {
            "instrument": ["AAA", "AAA", "AAA"],
            "date": pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
            "close": [10, 11, 12],
        }
    )
    events_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "earnings_date": [pd.Timestamp("2024-01-03")],
            "confidence": ["confirmed"],
        }
    )

    tagged = add_planner_earnings_warnings(
        planner_df,
        prices_df,
        events_df,
        objective="income_stability",
    )

    assert tagged.loc[0, "earnings_warning_title"] == "⚠️ Earnings"
    assert (
        tagged.loc[0, "earnings_warning_body"]
        == "This trade runs into earnings, so price movement may be unpredictable."
    )
