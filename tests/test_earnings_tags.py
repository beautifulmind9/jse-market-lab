import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.events.earnings import (
    PHASE_EVENT,
    PHASE_POST,
    PHASE_PRE,
    tag_earnings_phase,
)


def test_earnings_phase_tags_use_trading_days():
    dates = pd.bdate_range("2024-01-02", periods=40)
    df = pd.DataFrame({"instrument": "AAA", "date": dates, "return": 0.0})
    event_date = dates[10]
    events_df = pd.DataFrame(
        {
            "instrument": ["AAA"],
            "earnings_date": [event_date],
            "confidence": ["confirmed"],
        }
    )

    tagged = tag_earnings_phase(df, events_df, "date", "instrument")

    friday_before = dates[9]
    friday_row = tagged[tagged["date"] == friday_before].iloc[0]
    assert friday_row["earnings_day_offset"] == -1

    event_row = tagged[tagged["date"] == event_date].iloc[0]
    assert event_row["earnings_phase"] == PHASE_EVENT


def test_earnings_phase_bounds():
    dates = pd.bdate_range("2024-03-01", periods=70)
    df = pd.DataFrame({"instrument": "BBB", "date": dates, "return": 0.0})
    event_date = dates[30]
    events_df = pd.DataFrame(
        {
            "instrument": ["BBB"],
            "earnings_date": [event_date],
            "confidence": ["estimated"],
        }
    )

    tagged = tag_earnings_phase(df, events_df, "date", "instrument")

    pre_day = dates[0]
    pre_row = tagged[tagged["date"] == pre_day].iloc[0]
    assert pre_row["earnings_phase"] == PHASE_PRE

    post_day = dates[34]
    post_row = tagged[tagged["date"] == post_day].iloc[0]
    assert post_row["earnings_phase"] == PHASE_POST

    outside_day = dates[65]
    outside_row = tagged[tagged["date"] == outside_day].iloc[0]
    assert pd.isna(outside_row["earnings_phase"])


def test_earnings_phase_snaps_weekend_to_next_trading_day():
    dates = pd.bdate_range("2024-01-02", periods=10)
    df = pd.DataFrame({"instrument": "DDD", "date": dates, "return": 0.0})
    weekend_event = pd.Timestamp("2024-01-06")
    events_df = pd.DataFrame(
        {
            "instrument": ["DDD"],
            "earnings_date": [weekend_event],
            "confidence": ["confirmed"],
        }
    )

    tagged = tag_earnings_phase(df, events_df, "date", "instrument")

    event_day = pd.Timestamp("2024-01-08")
    event_row = tagged[tagged["date"] == event_day].iloc[0]
    assert event_row["earnings_phase"] == PHASE_EVENT
    assert event_row["earnings_day_offset"] == 0

    pre_day = pd.Timestamp("2024-01-05")
    pre_row = tagged[tagged["date"] == pre_day].iloc[0]
    assert pre_row["earnings_phase"] == PHASE_PRE
    assert pre_row["earnings_day_offset"] == -1


def test_earnings_phase_tie_breaks_on_confidence():
    dates = pd.bdate_range("2024-04-01", periods=25)
    df = pd.DataFrame({"instrument": "CCC", "date": dates, "return": 0.0})
    event_estimated = dates[5]
    event_confirmed = dates[9]
    anchor_date = dates[7]
    events_df = pd.DataFrame(
        {
            "instrument": ["CCC", "CCC"],
            "earnings_date": [event_estimated, event_confirmed],
            "confidence": ["estimated", "confirmed"],
        }
    )

    tagged = tag_earnings_phase(df, events_df, "date", "instrument")
    anchor_row = tagged[tagged["date"] == anchor_date].iloc[0]
    assert anchor_row["earnings_day_offset"] == -2
