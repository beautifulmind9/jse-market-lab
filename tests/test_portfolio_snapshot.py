import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.portfolio_snapshot import build_portfolio_snapshot, build_reserved_cash_explanation
from app.language.formatter import contains_advisory_language


def test_snapshot_contains_required_interpretation_sections():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "strong"},
            {"allocation_amount": 0, "quality_tier": "B", "confidence_label": "medium"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"])
    assert snapshot["title"] == "Portfolio Snapshot"
    assert "found 2 possible trades" in blob.lower()
    assert "were funded" in blob.lower()
    assert "stronger" in blob.lower()
    assert "cash" in blob.lower()


def test_reserved_cash_explanation_appears_when_capital_is_held_back():
    explanation = build_reserved_cash_explanation(
        [
            {"allocation_amount": 3_000, "quality_tier": "A"},
            {"allocation_amount": 0, "quality_tier": "B"},
        ],
        10_000,
        mode="beginner",
    )

    assert explanation["reserve_ratio"] > 0
    assert explanation["title"] == "Why cash is reserved"
    assert any("cash" in line.lower() for line in explanation["lines"])


def test_beginner_vs_analyst_snapshot_behavior_differs_with_context_line():
    beginner_snapshot = build_portfolio_snapshot(
        [{"allocation_amount": 2_000, "quality_tier": "A"}], 10_000, mode="beginner"
    )
    analyst_snapshot = build_portfolio_snapshot(
        [{"allocation_amount": 2_000, "quality_tier": "A"}], 10_000, mode="analyst"
    )

    assert len(analyst_snapshot["lines"]) > len(beginner_snapshot["lines"])
    assert any("reserve ratio" in line.lower() for line in analyst_snapshot["lines"])
    assert all("reserve ratio" not in line.lower() for line in beginner_snapshot["lines"])


def test_snapshot_and_reserved_cash_copy_has_no_advisory_language():
    snapshot = build_portfolio_snapshot(
        [{"allocation_amount": 2_000, "quality_tier": "A"}, {"allocation_amount": 0, "quality_tier": "C"}],
        10_000,
        mode="analyst",
    )
    reserved_cash = build_reserved_cash_explanation(
        [{"allocation_amount": 2_000, "quality_tier": "A"}, {"allocation_amount": 0, "quality_tier": "C"}],
        10_000,
        mode="analyst",
    )

    combined = " ".join(snapshot["lines"] + reserved_cash["lines"])
    assert contains_advisory_language(combined) is False
