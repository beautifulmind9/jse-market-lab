import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.portfolio_ui import (
    build_portfolio_summary,
    generate_funding_reason,
    split_trades_by_funding,
)


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
