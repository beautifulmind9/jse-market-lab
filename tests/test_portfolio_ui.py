import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.portfolio_ui import (
    build_portfolio_summary,
    generate_funding_reason,
    render_portfolio_plan,
    resolve_unfunded_reason,
    split_trades_by_funding,
)


class DummyStreamlit:
    def __init__(self):
        self.dataframes = []
        self.info_messages = []
        self.captions = []

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


def test_build_portfolio_summary_calculates_totals():
    summary = build_portfolio_summary(
        [
            {"allocation_amount": 25_000},
            {"allocation_amount": 10_000},
            {"allocation_amount": 0},
        ],
        total_capital=100_000,
    )

    assert summary["total_allocated_amount"] == 35_000
    assert summary["total_allocated_pct"] == 0.35
    assert summary["cash_reserve_amount"] == 65_000
    assert summary["cash_reserve_pct"] == 0.65
    assert summary["funded_trade_count"] == 2


def test_split_trades_by_funding_separates_rows():
    funded, unfunded = split_trades_by_funding(
        [
            {"instrument": "AAA", "allocation_amount": 100},
            {"instrument": "BBB", "allocation_amount": 0},
            {"instrument": "CCC", "allocation_amount": 50},
        ]
    )

    assert [row["instrument"] for row in funded] == ["AAA", "CCC"]
    assert [row["instrument"] for row in unfunded] == ["BBB"]


def test_generate_funding_reason_uses_why_mapping():
    text = generate_funding_reason(
        {
            "allocation_amount": 1000,
            "selection_rank": 2,
        }
    )
    assert text == "Selected — one of the strongest setups right now. Ranked #2"


def test_unfunded_reason_uses_single_why_sentence():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
        "selection_rank": 5,
    }
    assert (
        resolve_unfunded_reason(trade)
        == "Not funded — better trades already used up the available slots. Ranked #5"
    )


def test_render_portfolio_plan_unfunded_table_shows_single_why_column():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "liquidity_pass": True,
                "selection_rank": 5,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    unfunded_df = st.dataframes[1][0]
    assert unfunded_df.iloc[0]["Decision Status"] == "eligible but constrained"
    assert unfunded_df.iloc[0]["Why"] == "Not funded — better trades already used up the available slots. Ranked #5"
    assert "Reason" not in unfunded_df.columns
    assert "Explanation" not in unfunded_df.columns
    assert "Primary Rule/Constraint" not in unfunded_df.columns


def test_render_portfolio_plan_adds_plain_language_context_note():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {"instrument": "AAA", "allocation_amount": 1000, "allocation_pct": 0.1, "quality_tier": "A"},
            {"instrument": "BBB", "allocation_amount": 0, "quality_tier": "C"},
        ],
        total_capital=10_000,
        st_module=st,
    )

    assert st.captions
    assert "quick plain-language reason" in st.captions[0]


def test_render_portfolio_plan_shows_why_column_for_funded_and_unfunded():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 1000,
                "allocation_pct": 0.1,
                "quality_tier": "A",
                "selection_rank": 1,
                "funded_rank": 1,
                "eligible_for_funding": True,
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "selection_rank": 4,
                "eligible_for_funding": True,
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
    assert funded_df.iloc[0]["Why"] == "Selected — one of the strongest setups right now. Ranked #1"
    assert unfunded_df.iloc[0]["Why"] == "Not funded — better trades already used up the available slots. Ranked #4"
