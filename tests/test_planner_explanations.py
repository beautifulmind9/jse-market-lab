import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.explanations import (
    classify_decision_status,
    explain_funded_trade_why,
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


def test_funded_top_ranked_explanation_is_added_when_rank_fields_available():
    text = explain_portfolio_decision(
        {
            "allocation_amount": 10_000,
            "allocation_pct": 0.30,
            "selection_rank": 1,
            "funded_rank": 1,
            "eligible_for_funding": True,
        }
    )
    assert "top-ranked eligible trade" in text


def test_eligible_but_ranked_outside_funded_positions_explains_priority_limit():
    text = explain_portfolio_decision(
        {
            "allocation_amount": 0,
            "selection_rank": 4,
            "eligible_for_funding": True,
            "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
        }
    )
    assert classify_decision_status(
        {
            "allocation_amount": 0,
            "selection_rank": 4,
            "eligible_for_funding": True,
            "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
        }
    ) == "eligible but constrained"
    assert "funded slots were filled" in text


def test_hard_stop_stays_not_eligible_even_if_constraint_word_appears():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "C",
        "allocation_reason_clear": "Hard rule applied: quality tier C is not funded; portfolio constraint context present.",
    }

    assert classify_decision_status(trade) == "not eligible"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: quality tier C rule."




def test_eligible_for_funding_false_is_reduced_to_zero_when_not_hard_stop():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "eligible_for_funding": False,
    }

    assert classify_decision_status(trade) == "reduced to zero"
    assert "risk sizing reduced allocation to 0%" in explain_portfolio_decision(trade)

def test_preconstraints_text_is_classified_as_reduced_to_zero():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "allocation_reason_clear": "Final allocation is 0% because pre-constraints reduced allocation to zero.",
    }

    assert classify_decision_status(trade) == "reduced to zero"


def test_genuine_exposure_constraint_is_classified_as_constrained():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "allocation_reason_clear": "Final allocation is 0% because max portfolio exposure reached (70%).",
    }

    assert classify_decision_status(trade) == "eligible but constrained"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: max portfolio exposure limit."


def test_liquidity_failure_is_not_eligible():
    trade = {
        "allocation_amount": 0,
        "liquidity_pass": False,
        "allocation_reason_clear": "Liquidity screen failed before sizing constraints.",
    }

    assert classify_decision_status(trade) == "not eligible"
    assert explain_primary_rule_or_constraint(trade) == "Primary driver: liquidity eligibility rule."


def test_fallback_when_rank_fields_unavailable_remains_neutral():
    text = explain_portfolio_decision(
        {
            "allocation_amount": 0,
            "quality_tier": "A",
            "liquidity_pass": True,
        }
    )
    assert text == "Not funded. No explicit allocator reason was provided in this output."


def test_generic_fallback_stays_unfunded_when_no_markers_present():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "eligible_for_funding": None,
    }

    assert classify_decision_status(trade) == "unfunded"


def test_funded_why_mapping_for_tier_a_strong():
    text = explain_funded_trade_why({"quality_tier": "A", "confidence_label": "strong"})
    assert text == "Selected — strong setup with good confirmation."


def test_funded_why_mapping_for_tier_a_moderate():
    text = explain_funded_trade_why({"quality_tier": "A", "confidence_label": "moderate"})
    assert text == "Selected — solid setup with decent confirmation."


def test_funded_why_mapping_for_tier_b():
    text = explain_funded_trade_why({"quality_tier": "B", "confidence_label": "strong"})
    assert text == "Selected — decent setup but not the strongest."


def test_funded_why_uses_relative_strength_wording_for_smaller_position():
    text = explain_funded_trade_why(
        {
            "quality_tier": "A",
            "confidence_label": "strong",
            "allocation_reason_clear": "Reduced size due to relative strength against peers.",
        }
    )
    assert text == "Selected — smaller position due to relative strength."


def test_funded_why_rank_stays_single_sentence():
    text = explain_funded_trade_why(
        {"quality_tier": "A", "confidence_label": "strong", "selection_rank": 2}
    )
    assert text.count(".") == 1
    assert text.endswith("ranked #2.")
