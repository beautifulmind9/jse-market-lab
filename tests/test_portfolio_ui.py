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

    def subheader(self, _text):
        return None

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


def test_generate_funding_reason_labels():
    assert generate_funding_reason({"quality_tier": "C"}) == "Not funded — Tier C"
    assert generate_funding_reason({"liquidity_pass": False}) == "Not funded — Liquidity"
    assert (
        generate_funding_reason({"earnings_warning_severity": "high"})
        == "Reduced allocation — Earnings risk"
    )
    assert (
        generate_funding_reason({"volatility_bucket": "high"})
        == "Reduced allocation — High volatility"
    )
    assert generate_funding_reason({"quality_tier": "A"}) == "Eligible — meets criteria"


def test_helpers_handle_missing_optional_fields_gracefully():
    summary = build_portfolio_summary([{}], total_capital=0)
    funded, unfunded = split_trades_by_funding([{}])
    reason = generate_funding_reason({})

    assert summary["total_allocated_amount"] == 0
    assert summary["cash_reserve_amount"] == 0
    assert funded == []
    assert len(unfunded) == 1
    assert reason == "Eligible — meets criteria"


def test_unfunded_reason_prefers_allocator_reason_field():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "allocation_reason_clear": "Constraint limited — max funded trades reached",
    }
    assert (
        resolve_unfunded_reason(trade)
        == "Constraint limited — max funded trades reached"
    )


def test_unfunded_reason_falls_back_when_allocator_reason_missing():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "C",
    }
    assert resolve_unfunded_reason(trade) == "Not funded — Tier C"




def test_unfunded_reason_uses_new_priority_order():
    trade = {
        "allocation_amount": 0,
        "allocation_reason_clear": "Clear reason",
        "allocation_reason_pro": "Pro reason",
        "allocator_reason": "Allocator reason",
        "allocation_reason": "Allocation reason",
        "reason": "Generic reason",
    }
    assert resolve_unfunded_reason(trade) == "Clear reason"

def test_render_portfolio_plan_unfunded_table_shows_allocator_reason():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {"instrument": "AAA", "allocation_amount": 1000, "quality_tier": "A"},
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "A",
                "allocation_reason_clear": "Constraint limited — max funded trades reached",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    unfunded_df = st.dataframes[2][0]
    assert unfunded_df.iloc[0]["Reason"] == "Constraint limited — max funded trades reached"


def test_render_portfolio_plan_funded_rows_work_with_or_without_allocator_reason():
    st = DummyStreamlit()
    render_portfolio_plan(
        allocations=[
            {
                "instrument": "AAA",
                "allocation_amount": 1000,
                "allocation_pct": 0.1,
                "quality_tier": "A",
                "allocator_reason": "ignored for funded note",
            },
            {
                "instrument": "CCC",
                "allocation_amount": 500,
                "allocation_pct": 0.05,
                "quality_tier": "B",
            },
            {
                "instrument": "BBB",
                "allocation_amount": 0,
                "quality_tier": "C",
            },
        ],
        total_capital=10_000,
        st_module=st,
    )

    funded_df = st.dataframes[1][0]
    assert list(funded_df["Instrument"]) == ["AAA", "CCC"]
    assert list(funded_df["Funding Note"]) == [
        "Eligible — meets criteria",
        "Eligible — meets criteria",
    ]
