import re
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


def _single_sentence(text: str) -> bool:
    cleaned = re.sub(r"\.\s*Ranked\s+#\d+$", "", text.replace("—", " "))
    parts = [part.strip() for part in re.split(r"[.!?]", cleaned) if part.strip()]
    return len(parts) == 1


def test_resolve_explicit_reason_uses_priority_order():
    trade = {
        "allocation_reason_pro": "pro reason",
        "allocation_reason_clear": "clear reason",
        "allocator_reason": "allocator reason",
    }
    assert resolve_explicit_reason(trade) == "clear reason"


def test_funded_status_maps_to_simple_why_with_optional_rank():
    text = explain_portfolio_decision(
        {
            "allocation_amount": 10_000,
            "selection_rank": 1,
        }
    )

    assert text == "Selected — one of the strongest setups right now. Ranked #1"


def test_eligible_but_constrained_maps_to_simple_why():
    trade = {
        "allocation_amount": 0,
        "selection_rank": 4,
        "eligible_for_funding": True,
        "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
    }
    assert classify_decision_status(trade) == "eligible but constrained"
    assert (
        explain_portfolio_decision(trade)
        == "Not funded — better trades already used up the available slots. Ranked #4"
    )


def test_hard_stop_maps_to_not_eligible_why():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "C",
        "allocation_reason_clear": "Hard rule applied: quality tier C is not funded.",
    }

    assert classify_decision_status(trade) == "not eligible"
    assert explain_portfolio_decision(trade) == "Not funded — this setup didn’t meet the rules."


def test_eligible_for_funding_false_maps_to_reduced_to_zero_why():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "eligible_for_funding": False,
    }

    assert classify_decision_status(trade) == "reduced to zero"
    assert explain_portfolio_decision(trade) == "Not funded — risk rules cut this position to zero."


def test_fallback_maps_to_not_strong_enough_why():
    trade = {
        "allocation_amount": 0,
        "quality_tier": "A",
        "liquidity_pass": True,
        "eligible_for_funding": None,
    }

    assert classify_decision_status(trade) == "unfunded"
    assert explain_portfolio_decision(trade) == "Not funded — this setup wasn’t strong enough."


def test_why_is_one_sentence_short_and_non_technical():
    text = explain_portfolio_decision({"allocation_amount": 0, "quality_tier": "C", "selection_rank": 8})

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
