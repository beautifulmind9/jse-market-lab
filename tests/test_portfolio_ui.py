import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.portfolio_ui import _group_mistakes_for_display, render_portfolio_plan


class DummyStreamlit:
    def __init__(self):
        self.dataframes = []
        self.info_messages = []
        self.captions = []
        self.writes = []
        self.markdowns = []
        self.tabs_requested = []

    class _DummyTab:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def subheader(self, _text):
        return None

    def caption(self, text):
        self.captions.append(text)

    def markdown(self, _text, **_kwargs):
        self.markdowns.append(_text)
        return None

    def info(self, text):
        self.info_messages.append(text)

    def dataframe(self, df, use_container_width=False):
        self.dataframes.append((df.copy(), use_container_width))

    def write(self, payload):
        self.writes.append(payload)

    def tabs(self, names):
        self.tabs_requested.append(list(names))
        return [self._DummyTab(), self._DummyTab()]


def test_render_portfolio_plan_uses_why_column_and_no_primary_rule_column():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 1000,
                "allocation_pct": 0.1,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "selection_rank": 4,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    funded_df = st.dataframes[1][0]
    unfunded_df = st.dataframes[2][0]

    assert "Why" in funded_df.columns
    assert "Why" in unfunded_df.columns
    assert "Setup Strength" in funded_df.columns
    assert "Strong setup" in funded_df.iloc[0]["Setup Strength"]
    assert "High confidence" in funded_df.iloc[0]["Confidence"]
    assert "Primary Rule/Constraint" not in funded_df.columns
    assert "Primary Rule/Constraint" not in unfunded_df.columns
    assert funded_df.iloc[0]["Decision Status"] == "Selected"
    assert unfunded_df.iloc[0]["Decision Status"] == "Not funded (limit reached)"
    assert "funds the strongest eligible setups first" in st.captions[0]
    assert st.tabs_requested == [["Plan", "Review"]]
    assert any("followed system rules" in line for line in st.markdowns)


def test_group_mistakes_for_display_combines_repeated_types():
    grouped = _group_mistakes_for_display(
        [
            {"type": "low_quality_trade", "message": "a"},
            {"type": "low_quality_trade", "message": "b"},
            {"type": "low_quality_trade", "message": "c"},
            {"type": "liquidity_violation", "message": "d"},
        ]
    )

    assert "3 trade(s) missed the setup-quality rule." in grouped
    assert "1 trade(s) failed the liquidity check." in grouped


def test_render_portfolio_plan_places_snapshot_and_reserved_cash_before_tables():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 2000,
                "allocation_pct": 0.2,
                "quality_tier": "A",
                "confidence_label": "strong",
                "selection_rank": 1,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "allocation_pct": 0.0,
                "quality_tier": "B",
                "confidence_label": "medium",
                "selection_rank": 4,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
        section="plan",
    )

    assert "#### Portfolio Snapshot" in st.markdowns
    assert "#### Why cash is reserved" in st.markdowns
    snapshot_idx = st.markdowns.index("#### Portfolio Snapshot")
    summary_idx = next(
        idx
        for idx, text in enumerate(st.markdowns)
        if "Portfolio Summary" in text
    )
    assert snapshot_idx < summary_idx
