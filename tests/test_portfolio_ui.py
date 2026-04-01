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


def test_generate_funding_reason_prefers_allocator_reason_when_available():
    text = generate_funding_reason(
        {
            "allocation_amount": 1000,
            "allocation_reason_clear": "Strong confidence starts at 30%. Final allocation is 20%.",
        }
    )
    assert text.startswith("Funded.")
    assert "Final allocation is 20%" in text


def test_unfunded_reason_prefers_allocator_reason_field():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
    }
    assert (
        resolve_unfunded_reason(trade)
        == "Final allocation is 0% because max funded trades reached (3)."
    )


def test_unfunded_reason_falls_back_to_rule_explanation_when_reason_missing():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "C",
    }
    assert "not eligible" in resolve_unfunded_reason(trade)


def test_render_portfolio_plan_unfunded_table_shows_status_and_explanations():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "liquidity_pass": True,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    unfunded_df = st.dataframes[1][0]
    assert unfunded_df.iloc[0]["Decision Status"] == "eligible but constrained"
    assert "max funded trades reached" in unfunded_df.iloc[0]["Reason"]
    assert "Primary driver" in unfunded_df.iloc[0]["Primary Rule/Constraint"]


def test_render_portfolio_plan_adds_context_note_for_funded_vs_unfunded():
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
    assert "Funded trades received non-zero allocation" in st.captions[0]
