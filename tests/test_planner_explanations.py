import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.explanations import (
    classify_decision_status,
    explain_portfolio_decision,
    explain_primary_rule_or_constraint,
    resolve_explicit_reason,
)


def test_resolve_explicit_reason_uses_priority_order():
    trade = {
        "allocation_reason_pro": "pro reason",
        "allocation_reason_clear": "clear reason",
        "allocator_reason": "allocator reason",
    }
    assert resolve_explicit_reason(trade) == "clear reason"


def test_explain_portfolio_decision_prefers_explicit_reason_for_funded():
    text = explain_portfolio_decision(
        {
            "allocation_amount": 1000,
            "allocation_reason_clear": "Strong confidence starts at 30%. Final allocation is 25%.",
        }
    )
    assert text.startswith("Funded.")
    assert "Final allocation is 25%" in text


def test_explain_portfolio_decision_not_eligible_fallbacks():
    tier_c = explain_portfolio_decision({"allocation_amount": 0, "quality_tier": "C"})
    liquidity_fail = explain_portfolio_decision({"allocation_amount": 0, "liquidity_pass": False})

    assert "not eligible" in tier_c
    assert "liquidity screen failed" in liquidity_fail


def test_classify_decision_status_detects_eligible_but_constrained():
    status = classify_decision_status(
        {
            "allocation_amount": 0,
            "quality_tier": "A",
            "liquidity_pass": True,
            "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
        }
    )
    assert status == "eligible but constrained"


def test_primary_rule_or_constraint_uses_constraint_markers():
    text = explain_primary_rule_or_constraint(
        {
            "allocation_amount": 0,
            "allocation_reason_clear": "Final allocation is 0% because max portfolio exposure reached (70%).",
        }
    )
    assert "max portfolio exposure" in text
