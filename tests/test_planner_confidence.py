import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.confidence import generate_trade_confidence


def test_generate_trade_confidence_avoid_on_failed_liquidity():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": False,
            "severity": "info",
            "quality_tier": "A",
            "volatility_bucket": "low",
        }
    )

    assert payload["confidence_level"] == "avoid"
    assert payload["confidence_label"] == "avoid"


def test_generate_trade_confidence_high_risk_on_high_severity():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "high",
            "quality_tier": "A",
            "volatility_bucket": "low",
        }
    )

    assert payload["confidence_level"] == "high risk"


def test_generate_trade_confidence_strong_for_a_non_high_volatility():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "caution",
            "quality_tier": "A",
            "volatility_bucket": "medium",
        }
    )

    assert payload["confidence_level"] == "strong"


def test_generate_trade_confidence_moderate_for_a_with_high_volatility():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "A",
            "volatility_bucket": "high",
        }
    )

    assert payload["confidence_level"] == "moderate"


def test_generate_trade_confidence_moderate_for_b_tier():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "B",
            "volatility_bucket": "high",
        }
    )

    assert payload["confidence_level"] == "moderate"


def test_generate_trade_confidence_watch_for_c_tier():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "C",
            "volatility_bucket": "low",
        }
    )

    assert payload["confidence_level"] == "watch"


def test_generate_trade_confidence_fallback_to_moderate():
    payload = generate_trade_confidence(
        {
            "liquidity_pass": True,
            "severity": "info",
            "quality_tier": "D",
            "volatility_bucket": "low",
        }
    )

    assert payload["confidence_level"] == "moderate"
    assert set(payload.keys()) == {
        "confidence_label",
        "confidence_title",
        "confidence_body_clear",
        "confidence_body_pro",
        "confidence_level",
    }
