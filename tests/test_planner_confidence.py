import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.confidence import generate_trade_confidence


def test_confidence_rewrite_matches_requested_copy():
    strong = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "A",
            "volatility_bucket": "medium",
        }
    )
    assert strong["confidence_label"] == "strong"
    assert strong["confidence_body_clear"] == "Strong — signals are lining up clearly."

    moderate = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "B",
            "volatility_bucket": "high",
        }
    )
    assert moderate["confidence_label"] == "moderate"
    assert moderate["confidence_body_clear"] == "Moderate — some signals are there, but not all."

    weak = generate_trade_confidence(
        {
            "liquidity_pass": False,
            "severity": "high",
            "quality_tier": "C",
            "volatility_bucket": "low",
        }
    )
    assert weak["confidence_label"] == "weak"
    assert weak["confidence_body_clear"] == "Weak — signals are not lining up well."
