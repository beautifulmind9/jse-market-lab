import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.trade_explainer import explain_trade_reason, explain_unfunded_reason
from app.language.formatter import contains_advisory_language


def test_funded_trade_explanation_includes_strength_and_rank_context():
    text = explain_trade_reason(
        {
            "allocation_amount": 3000,
            "quality_tier": "A",
            "confidence_label": "strong",
            "selection_rank": 1,
            "volume_confirmed": True,
            "momentum_context": "supportive",
        },
        mode="beginner",
    )

    assert "Selected because this setup ranked as a top-quality" in text
    assert "volume confirmation supported this setup" in text
    assert "ranked #1" in text


def test_unfunded_trade_explanation_covers_constraint_and_competing_trades():
    text = explain_unfunded_reason(
        {
            "allocation_amount": 0,
            "quality_tier": "A",
            "selection_rank": 5,
            "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
        },
        mode="beginner",
    )

    assert "Not funded because higher-ranked eligible trades were funded first" in text
    assert "ranked #5" in text


def test_beginner_and_analyst_wording_differs():
    row = {
        "allocation_amount": 0,
        "quality_tier": "B",
        "selection_rank": 4,
        "allocation_reason_clear": "Final allocation is 0% because max funded trades reached (3).",
    }

    beginner = explain_unfunded_reason(row, mode="beginner")
    analyst = explain_unfunded_reason(row, mode="analyst")

    assert beginner != analyst
    assert "outside funded capacity" in analyst
    assert "below trades that received funding first" in beginner


def test_trade_explanations_avoid_advisory_language():
    funded = explain_trade_reason(
        {
            "allocation_amount": 2000,
            "quality_tier": "A",
            "confidence_label": "strong",
        }
    )
    unfunded = explain_unfunded_reason(
        {
            "allocation_amount": 0,
            "quality_tier": "C",
        }
    )

    blob = f"{funded} {unfunded}"
    assert contains_advisory_language(blob) is False
