import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.explanations import classify_decision_status, explain_portfolio_decision


def _is_single_sentence(text: str) -> bool:
    return text.count(".") <= 1 and "\n" not in text


def test_status_labels_match_new_mapping():
    assert classify_decision_status({"allocation_amount": 100}) == "Selected"
    assert classify_decision_status({"allocation_amount": 0, "quality_tier": "C"}) == "Not valid"
    assert (
        classify_decision_status(
            {
                "allocation_amount": 0,
                "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
            }
        )
        == "Not funded (limit reached)"
    )
    assert (
        classify_decision_status(
            {
                "allocation_amount": 0,
                "eligible_for_funding": False,
            }
        )
        == "Not funded (cut to zero)"
    )
    assert classify_decision_status({"allocation_amount": 0, "quality_tier": "A"}) == "Not funded"

    assert text == "Selected — one of the strongest setups right now. Ranked #1"

def test_explanations_use_new_voice_and_are_single_sentence():
    funded = explain_portfolio_decision(
        {
            "allocation_amount": 100,
            "quality_tier": "A",
            "confidence_label": "strong",
            "selection_rank": 1,
        }
    )
    assert funded == "Selected — strong setup with good confirmation, ranked #1."
    assert _is_single_sentence(funded)

    limit = explain_portfolio_decision(
        {
            "allocation_amount": 0,
            "allocation_reason_clear": "max funded trades reached",
        }
    )
    assert limit == "Not funded — better trades already filled the slots."
    assert _is_single_sentence(limit)

    hard_rule = explain_portfolio_decision({"allocation_amount": 0, "quality_tier": "C"})
    assert hard_rule == "Not funded — this setup didn’t meet the rules."

    zeroed = explain_portfolio_decision(
        {"allocation_amount": 0, "quality_tier": "A", "eligible_for_funding": False}
    )
    assert zeroed == "Not funded — risk rules cut this position to zero."

    fallback = explain_portfolio_decision({"allocation_amount": 0, "quality_tier": "A"})
    assert fallback == "Not funded — this setup wasn’t strong enough."
