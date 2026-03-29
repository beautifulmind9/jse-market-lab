import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.ui import (
    _normalize_warning_severity,
    render_earnings_warning_block,
    render_trade_card,
)


class _DummyExpander:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyStreamlit:
    def __init__(self):
        self.calls = []

    def markdown(self, text):
        self.calls.append(("markdown", text))

    def info(self, text):
        self.calls.append(("info", text))

    def warning(self, text):
        self.calls.append(("warning", text))

    def error(self, text):
        self.calls.append(("error", text))

    def write(self, text):
        self.calls.append(("write", text))

    def expander(self, label, expanded=False):
        self.calls.append(("expander", label, expanded))
        return _DummyExpander()


def test_normalize_warning_severity_defaults_to_info():
    assert _normalize_warning_severity(None) == "info"
    assert _normalize_warning_severity(np.nan) == "info"
    assert _normalize_warning_severity("unknown") == "info"


def test_warning_block_renders_caution_with_details():
    st = DummyStreamlit()
    rendered = render_earnings_warning_block(
        {
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "caution",
            "earnings_warning_title": "⚠️ Earnings upcoming",
            "earnings_warning_body": "Trade overlaps earnings.",
        },
        st_module=st,
    )

    assert rendered is True
    assert ("warning", "**⚠️ Earnings upcoming** · `caution`") in st.calls
    assert ("write", "Trade overlaps earnings.") in st.calls


def test_warning_block_skips_non_overlapping_rows():
    st = DummyStreamlit()
    rendered = render_earnings_warning_block(
        {
            "earnings_overlaps_window": False,
            "earnings_warning_severity": "high",
        },
        st_module=st,
    )

    assert rendered is False
    assert st.calls == []

def test_warning_block_skips_null_overlap_values():
    st = DummyStreamlit()
    rendered = render_earnings_warning_block(
        {
            "earnings_overlaps_window": np.nan,
            "earnings_warning_severity": "high",
            "earnings_warning_title": "High risk earnings window",
        },
        st_module=st,
    )

    assert rendered is False
    assert st.calls == []


def test_warning_block_renders_for_numpy_true_overlap():
    st = DummyStreamlit()
    rendered = render_earnings_warning_block(
        {
            "earnings_overlaps_window": np.bool_(True),
            "earnings_warning_severity": "high",
            "earnings_warning_title": "High risk earnings window",
        },
        st_module=st,
    )

    assert rendered is True
    assert ("error", "**High risk earnings window** · `high`") in st.calls


def test_trade_card_order_is_header_then_warning_then_math():
    st = DummyStreamlit()

    def render_math(_row):
        st.calls.append(("math", "rendered"))

    render_trade_card(
        {
            "instrument": "AAA",
            "entry_date": "2024-01-02",
            "holding_window": 10,
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "high",
            "earnings_warning_title": "High risk earnings window",
            "earnings_warning_body": "Body",
        },
        render_math,
        st_module=st,
    )

    event_order = [event[0] for event in st.calls]
    first_error = event_order.index("error")
    second_error = event_order.index("error", first_error + 1)
    assert event_order.index("markdown") < first_error
    assert first_error < second_error
    assert second_error < event_order.index("math")


def test_trade_card_renders_info_guidance_below_warning():
    st = DummyStreamlit()

    def render_math(_row):
        st.calls.append(("math", "rendered"))

    render_trade_card(
        {
            "instrument": "AAA",
            "entry_date": "2024-01-02",
            "holding_window": 10,
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "info",
            "earnings_warning_title": "ℹ️ Post-earnings window",
            "earnings_warning_body": "Body",
        },
        render_math,
        st_module=st,
    )

    assert ("info", "**Earnings overlap awareness** · `info`") in st.calls
    assert ("expander", "Guidance", False) in st.calls
