import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.ui import render_trade_card


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


def test_trade_card_shows_single_sentence_earnings_warning_and_new_confidence_voice():
    st = DummyStreamlit()

    def render_math(_row):
        return None

    render_trade_card(
        {
            "instrument": "AAA",
            "entry_date": "2024-01-02",
            "holding_window": 10,
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "high",
            "earnings_warning_title": "⚠️ Earnings",
            "earnings_warning_body": "This trade runs into earnings, so price movement may be unpredictable.",
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "A",
            "volatility_bucket": "medium",
        },
        render_math,
        st_module=st,
        use_expander=False,
    )

    writes = [text for kind, text in st.calls if kind == "write"]
    assert "This trade runs into earnings, so price movement may be unpredictable." in writes
    assert "Strong — signals are lining up clearly." in writes
