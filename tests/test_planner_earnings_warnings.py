import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.earnings_warnings import add_planner_earnings_warnings


def _base_inputs(entry_date="2024-01-02", window=3):
    planner_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "entry_date": [pd.Timestamp(entry_date)],
            "holding_window": [window],
        }
    )
    prices_df = pd.DataFrame(
        {
            "instrument": ["AAA"] * 6,
            "date": pd.bdate_range("2024-01-02", periods=6),
            "close": [10, 11, 12, 13, 14, 15],
        }
    )
    events_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "earnings_date": [pd.Timestamp("2024-01-03")],
            "confidence": ["confirmed"],
        }
    )
    return planner_df, prices_df, events_df


def test_earnings_phase_defaults_to_non():
    planner_df, prices_df, events_df = _base_inputs()
    events_df = events_df.iloc[0:0]

    tagged = add_planner_earnings_warnings(
        planner_df,
        prices_df,
        events_df,
        objective="income_stability",
    )

    assert tagged.loc[0, "earnings_phase"] == "non"
    assert tagged.loc[0, "exit_earnings_phase"] == "non"


def test_overlap_flag_triggers_on_phase_change():
    planner_df, prices_df, events_df = _base_inputs(entry_date="2024-01-02", window=2)

    tagged = add_planner_earnings_warnings(
        planner_df,
        prices_df,
        events_df,
        objective="income_stability",
    )

    assert tagged.loc[0, "earnings_phase"] != tagged.loc[0, "exit_earnings_phase"]
    assert bool(tagged.loc[0, "earnings_overlaps_window"]) is True


def test_non_phase_yields_no_warning_fields():
    planner_df, prices_df, events_df = _base_inputs()
    events_df = events_df.iloc[0:0]

    tagged = add_planner_earnings_warnings(
        planner_df,
        prices_df,
        events_df,
        objective="active_growth",
    )

    assert tagged.loc[0, "earnings_warning_title"] is None
    assert tagged.loc[0, "earnings_warning_body"] is None
    assert tagged.loc[0, "earnings_warning_severity"] is None


def test_missing_planned_exit_date_sets_exit_phase_non():
    planner_df, prices_df, events_df = _base_inputs(window=30)

    tagged = add_planner_earnings_warnings(
        planner_df,
        prices_df,
        events_df,
        objective="capital_preservation",
    )

    assert tagged.loc[0, "exit_earnings_phase"] == "non"
