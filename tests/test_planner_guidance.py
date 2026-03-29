import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.guidance import generate_trade_guidance


def test_generate_trade_guidance_high_case():
    guidance = generate_trade_guidance(
        {
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "HIGH",
            "holding_window": 7,
            "volatility_bucket": "high",
        }
    )

    assert guidance is not None
    assert guidance["guidance_type"] == "high"
    assert "put in a smaller amount" in guidance["guidance_body_clear"]
    assert "smaller position" in guidance["guidance_body_pro"]
    assert (
        "Your current plan is to hold for about 7 trading days."
        in guidance["guidance_body_clear"]
    )


def test_generate_trade_guidance_caution_case():
    guidance = generate_trade_guidance(
        {
            "earnings_overlaps_window": np.bool_(True),
            "earnings_warning_severity": "caution",
            "volatility_bucket": "medium",
        }
    )

    assert guidance is not None
    assert guidance["guidance_type"] == "caution"
    assert "go in with less" in guidance["guidance_body_clear"]
    assert "smaller position" in guidance["guidance_body_pro"]


def test_generate_trade_guidance_info_case():
    guidance = generate_trade_guidance(
        {
            "earnings_overlaps_window": True,
            "earnings_warning_severity": "info",
        }
    )

    assert guidance is not None
    assert guidance["guidance_type"] == "info"
    assert "just keep it in mind" in guidance["guidance_body_clear"]
    assert "No immediate action is needed." in guidance["guidance_body_pro"]


def test_generate_trade_guidance_returns_none_without_explicit_true_overlap():
    assert generate_trade_guidance({"earnings_overlaps_window": None}) is None
    assert generate_trade_guidance({"earnings_overlaps_window": np.nan}) is None
    assert generate_trade_guidance({"earnings_overlaps_window": 1}) is None


def test_generate_trade_guidance_falls_back_to_info_for_null_severity():
    guidance = generate_trade_guidance(
        {
            "earnings_overlaps_window": True,
            "earnings_warning_severity": None,
        }
    )

    assert guidance is not None
    assert guidance["guidance_type"] == "info"
    assert "guidance_body_clear" in guidance
    assert "guidance_body_pro" in guidance
