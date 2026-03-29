import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.allocation import generate_portfolio_allocation


def _base_rows():
    return [
        {
            "instrument": "AAA",
            "quality_tier": "A",
            "liquidity_pass": True,
            "volatility_bucket": "low",
            "earnings_warning_severity": "info",
            "confidence_label": "strong",
        },
        {
            "instrument": "BBB",
            "quality_tier": "B",
            "liquidity_pass": True,
            "volatility_bucket": "medium",
            "earnings_warning_severity": "info",
            "confidence_label": "moderate",
        },
    ]


def test_tier_c_gets_zero_allocation():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": "CCC",
                "quality_tier": "C",
                "liquidity_pass": True,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "confidence_label": "strong",
            }
        ],
        100_000,
    )

    assert payload["allocations"][0]["allocation_pct"] == 0.0


def test_liquidity_fail_gets_zero_allocation():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": "LLL",
                "quality_tier": "A",
                "liquidity_pass": False,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "confidence_label": "strong",
            }
        ],
        100_000,
    )

    assert payload["allocations"][0]["allocation_pct"] == 0.0


def test_strong_gets_more_than_moderate():
    payload = generate_portfolio_allocation(_base_rows(), 100_000)
    by_symbol = {row["instrument"]: row for row in payload["allocations"]}

    assert by_symbol["AAA"]["allocation_pct"] > by_symbol["BBB"]["allocation_pct"]


def test_risk_reductions_apply_correctly():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": "RISKY",
                "quality_tier": "A",
                "liquidity_pass": True,
                "volatility_bucket": "high",
                "earnings_warning_severity": "caution",
                "confidence_label": "strong",
            }
        ],
        100_000,
    )

    # strong 30% - caution 5% - high volatility 5% = 20%
    assert payload["allocations"][0]["allocation_pct"] == pytest.approx(0.20)


def test_total_exposure_never_exceeds_cap():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": f"S{i}",
                "quality_tier": "A",
                "liquidity_pass": True,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "confidence_label": "strong",
            }
            for i in range(5)
        ],
        100_000,
    )

    assert payload["total_allocated_pct"] <= 0.70


def test_funded_trade_count_never_exceeds_three():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": f"M{i}",
                "quality_tier": "B",
                "liquidity_pass": True,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "confidence_label": "moderate",
            }
            for i in range(6)
        ],
        100_000,
    )

    funded = [row for row in payload["allocations"] if row["allocation_pct"] > 0]
    assert len(funded) <= 3


def test_cash_reserve_is_at_least_minimum():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": f"X{i}",
                "quality_tier": "A",
                "liquidity_pass": True,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "confidence_label": "strong",
            }
            for i in range(4)
        ],
        100_000,
    )

    assert payload["cash_reserve_pct"] >= 0.30


def test_output_structure_is_stable():
    payload = generate_portfolio_allocation(_base_rows(), 50_000)

    assert set(payload.keys()) == {
        "allocations",
        "total_allocated_pct",
        "total_allocated_amount",
        "cash_reserve_pct",
        "cash_reserve_amount",
    }

    assert set(payload["allocations"][0].keys()) == {
        "instrument",
        "confidence_label",
        "allocation_pct",
        "allocation_amount",
        "allocation_reason_clear",
        "allocation_reason_pro",
    }


def test_confidence_derives_when_missing_label():
    payload = generate_portfolio_allocation(
        [
            {
                "instrument": "DERIVE",
                "quality_tier": "A",
                "liquidity_pass": True,
                "volatility_bucket": "low",
                "earnings_warning_severity": "info",
                "severity": "info",
            }
        ],
        100_000,
    )

    assert payload["allocations"][0]["confidence_label"] == "strong"
    assert payload["allocations"][0]["allocation_pct"] == 0.30
