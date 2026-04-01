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


def test_hard_stop_tier_c_not_mislabeled_as_constraint_when_reason_mentions_constraint():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "C",
        "allocation_reason_clear": "Hard rule applied: quality tier C is not funded; portfolio constraint context present.",
    }

    assert classify_decision_status(trade) == "not eligible"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: quality tier C rule."


def test_liquidity_failure_is_labeled_not_eligible():
    trade = {
        "allocation_amount": 0,
        "liquidity_pass": False,
        "allocation_reason_clear": "Liquidity screen failed before sizing constraints.",
    }

    assert classify_decision_status(trade) == "not eligible"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: liquidity eligibility rule."
    decision_text = explain_portfolio_decision(trade)
    assert decision_text.startswith("Not funded.")
    assert "liquidity" in decision_text.lower()


def test_genuine_constraint_case_is_labeled_constrained():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
    }

    assert classify_decision_status(trade) == "eligible but constrained"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: max funded trades limit."


def test_sparse_reason_fields_fallback_behavior():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
    }

    assert classify_decision_status(trade) == "unfunded"
    assert explain_primary_rule_or_constraint(trade) == (
        "Primary driver: no explicit rule or constraint label available."
    )
    assert explain_portfolio_decision(trade) == (
        "Not funded. No explicit allocator reason was provided in this output."
    )
