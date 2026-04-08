import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.portfolio_ui import render_portfolio_plan


class DummyStreamlit:
    def __init__(self):
        self.dataframes = []
        self.info_messages = []
        self.captions = []
        self.writes = []

    def subheader(self, _text):
        return None

    def caption(self, text):
        self.captions.append(text)

    def markdown(self, _text):
        return None

    def info(self, text):
        self.info_messages.append(text)

    def dataframe(self, df, use_container_width=False):
        self.dataframes.append((df.copy(), use_container_width))

    def write(self, payload):
        self.writes.append(payload)


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
    assert "Primary Rule/Constraint" not in funded_df.columns
    assert "Primary Rule/Constraint" not in unfunded_df.columns
    assert funded_df.iloc[0]["Decision Status"] == "Selected"
    assert unfunded_df.iloc[0]["Decision Status"] == "Not funded (limit reached)"
    assert "Selected trades received funding" in st.captions[0]
