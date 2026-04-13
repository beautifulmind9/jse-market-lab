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
    assert "capital" in blob.lower()
    assert "current funded setup mix" in blob.lower()
    assert "current funded confidence" in blob.lower()
    assert "example glossary only" in blob.lower()
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


def test_snapshot_strong_funded_portfolio_is_data_driven_not_hardcoded():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_000, "quality_tier": "A", "confidence_label": "strong"},
            {"allocation_amount": 1_500, "quality_tier": "B", "confidence_label": "high"},
        ],
        10_000,
        mode="analyst",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "current funded setup mix is strong" in blob
    assert "current funded confidence mix is high/reliable" in blob


def test_snapshot_missing_labels_do_not_inflate_to_mostly_high():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_000, "quality_tier": "B", "confidence_label": "strong"},
            {"allocation_amount": 1_500, "quality_tier": "C", "confidence_label": ""},
            {"allocation_amount": 1_000, "quality_tier": "C"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "current funded confidence is mostly high" not in blob
    assert "current funded confidence is mixed across the funded portfolio" in blob


def test_snapshot_low_coverage_triggers_limited_confidence_detail():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_500, "quality_tier": "B", "confidence_label": ""},
            {"allocation_amount": 1_500, "quality_tier": "C"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"])
    assert "Confidence detail is limited for this plan." in blob


def test_snapshot_mixed_funded_portfolio_uses_mixed_language():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_500, "quality_tier": "B", "confidence_label": "medium"},
            {"allocation_amount": 1_500, "quality_tier": "C", "confidence_label": "low"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "mixed but still constructive" in blob
    assert "current funded confidence is mixed" in blob
    assert "high confidence" not in blob or "example glossary only" in blob


def test_snapshot_mixed_labeled_and_unlabeled_uses_total_funded_denominator():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_500, "quality_tier": "B", "confidence_label": "medium"},
            {"allocation_amount": 1_500, "quality_tier": "C", "confidence_label": "low"},
            {"allocation_amount": 1_000, "quality_tier": "C"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "current funded confidence is mixed across the funded portfolio" in blob


def test_snapshot_analyst_mode_includes_coverage_and_unknown_details():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_500, "quality_tier": "B", "confidence_label": "medium"},
            {"allocation_amount": 1_500, "quality_tier": "C", "confidence_label": "low"},
            {"allocation_amount": 1_000, "quality_tier": "C"},
        ],
        10_000,
        mode="analyst",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "current funded confidence mix is medium/mixed" in blob
    assert "high: 1, medium: 1, low: 1, unknown: 1" in blob
    assert "coverage ~75%" in blob


def test_snapshot_unfunded_portfolio_does_not_claim_strong_or_high_confidence():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 0, "quality_tier": "B", "confidence_label": "medium"},
            {"allocation_amount": 0, "quality_tier": "C", "confidence_label": "low"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"]).lower()
    assert "no trades were funded" in blob
    assert "current funded confidence is mostly high" not in blob
    assert "current funded confidence mix is high/reliable" not in blob


def test_snapshot_confidence_copy_remains_non_advisory_with_coverage_logic():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 3_000, "quality_tier": "A", "confidence_label": "high"},
            {"allocation_amount": 2_500, "quality_tier": "B", "confidence_label": ""},
            {"allocation_amount": 1_500, "quality_tier": "C"},
        ],
        10_000,
        mode="analyst",
    )

    combined = " ".join(snapshot["lines"])
    assert contains_advisory_language(combined) is False


def test_snapshot_glossary_text_is_clearly_separated_from_live_interpretation():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 2_000, "quality_tier": "C", "confidence_label": "low"},
        ],
        10_000,
        mode="analyst",
    )

    assert any(line.startswith("How to read setup strength and confidence:") for line in snapshot["lines"])


def test_snapshot_includes_adaptive_funding_language_for_broad_strong_market():
    snapshot = build_portfolio_snapshot(
        [
            {"allocation_amount": 1_000, "quality_tier": "A", "confidence_label": "strong"},
            {"allocation_amount": 1_000, "quality_tier": "A", "confidence_label": "strong"},
            {"allocation_amount": 1_000, "quality_tier": "A", "confidence_label": "strong"},
            {"allocation_amount": 1_000, "quality_tier": "B", "confidence_label": "moderate"},
        ],
        10_000,
        mode="beginner",
    )

    blob = " ".join(snapshot["lines"])
    assert "Multiple strong setups were available, so capital was spread across them." in blob
    assert "Max funded trades: 3" not in blob
