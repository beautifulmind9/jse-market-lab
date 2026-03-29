import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.ui import (
    _normalize_warning_severity,
    render_trade_cards,
    render_earnings_warning_block,
    render_trade_card,
    resolve_guidance_mode_for_planner,
)


class _DummyExpander:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyStreamlit:
    def __init__(self, *, toggle_value=True):
        self.calls = []
        self.toggle_value = toggle_value

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

    def toggle(self, label, value=False, key=None):
        self.calls.append(("toggle", label, value, key))
        return self.toggle_value


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


def test_trade_card_order_is_header_then_warning_then_confidence_then_guidance_then_math():
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
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "B",
            "volatility_bucket": "high",
        },
        render_math,
        st_module=st,
    )

    warning_index = st.calls.index(("error", "**High risk earnings window** · `high`"))
    confidence_index = st.calls.index(("info", "**Moderate confidence** · `moderate`"))
    guidance_index = st.calls.index(("error", "**High earnings overlap guidance** · `high`"))
    math_index = st.calls.index(("math", "rendered"))

    assert st.calls.index(("markdown", "### AAA | Entry: 2024-01-02 | Window: 10D")) < warning_index
    assert warning_index < confidence_index < guidance_index < math_index


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


def test_trade_card_switches_guidance_between_clear_and_pro():
    st_clear = DummyStreamlit()
    st_pro = DummyStreamlit()

    def render_math(_row):
        return None

    trade_row = {
        "instrument": "AAA",
        "entry_date": "2024-01-02",
        "holding_window": 10,
        "earnings_overlaps_window": True,
        "earnings_warning_severity": "high",
        "quality_tier": "A",
        "volatility_bucket": "low",
        "liquidity_pass": True,
        "severity": "info",
    }

    render_trade_card(
        trade_row,
        render_math,
        st_module=st_clear,
        use_expander=False,
        guidance_mode="clear",
    )
    render_trade_card(
        trade_row,
        render_math,
        st_module=st_pro,
        use_expander=False,
        guidance_mode="pro",
    )

    clear_writes = [call[1] for call in st_clear.calls if call[0] == "write"]
    pro_writes = [call[1] for call in st_pro.calls if call[0] == "write"]

    assert any("put in a smaller amount" in text for text in clear_writes)
    assert any("smaller position" in text for text in pro_writes)
    assert any("stronger setup" in text for text in clear_writes)
    assert any("relative confidence" in text for text in pro_writes)




def test_trade_card_renders_confidence_block_between_warning_and_guidance():
    st = DummyStreamlit()

    def render_math(_row):
        st.calls.append(("math", "rendered"))

    render_trade_card(
        {
            "instrument": "AAA",
            "entry_date": "2024-01-02",
            "holding_window": 10,
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "caution",
            "quality_tier": "C",
            "volatility_bucket": "medium",
            "liquidity_pass": True,
            "severity": "caution",
        },
        render_math,
        st_module=st,
    )

    assert ("warning", "**Watch closely** · `watch`") in st.calls
    warning_index = st.calls.index(("warning", "**Earnings window warning** · `caution`"))
    confidence_index = st.calls.index(("warning", "**Watch closely** · `watch`"))
    guidance_index = st.calls.index(("warning", "**Caution earnings overlap guidance** · `caution`"))
    assert warning_index < confidence_index < guidance_index

def test_trade_card_does_not_create_toggle_widget_per_card():
    st = DummyStreamlit(toggle_value=False)

    def render_math(_row):
        return None

    render_trade_card(
        {
            "instrument": "AAA",
            "entry_date": "2024-01-02",
            "holding_window": 10,
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "high",
        },
        render_math,
        st_module=st,
        guidance_mode=None,
    )

    assert not any(call[0] == "toggle" for call in st.calls)


def test_planner_level_guidance_mode_applies_to_multiple_cards():
    st = DummyStreamlit(toggle_value=False)

    def render_math(_row):
        return None

    selected_mode = render_trade_cards(
        [
            {
                "instrument": "AAA",
                "entry_date": "2024-01-02",
                "holding_window": 10,
                "earnings_overlaps_window": True,
                "earnings_warning_severity": "high",
            },
            {
                "instrument": "BBB",
                "entry_date": "2024-01-03",
                "holding_window": 8,
                "earnings_overlaps_window": True,
                "earnings_warning_severity": "caution",
            },
        ],
        render_math,
        st_module=st,
        use_expander=False,
    )

    assert selected_mode == "pro"
    assert st.calls.count(
        ("toggle", "Simple explanation", True, "guidance_mode_toggle")
    ) == 1
    pro_writes = [call[1] for call in st.calls if call[0] == "write"]
    assert any("smaller position" in text for text in pro_writes)


def test_resolve_guidance_mode_for_planner_defaults_to_clear():
    st = DummyStreamlit(toggle_value=True)
    assert resolve_guidance_mode_for_planner(st_module=st) == "clear"


def test_resolve_guidance_mode_for_planner_accepts_custom_toggle_key():
    st = DummyStreamlit(toggle_value=True)
    resolve_guidance_mode_for_planner(
        st_module=st,
        toggle_key="my_custom_toggle_key",
    )

    assert ("toggle", "Simple explanation", True, "my_custom_toggle_key") in st.calls
