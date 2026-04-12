import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.language.formatter import contains_advisory_language, explain_confidence, explain_strength


def test_beginner_translation_is_simple_and_jargon_light():
    strength = explain_strength("A", mode="beginner")
    confidence = explain_confidence("strong", mode="beginner")

    assert "Tier" not in strength
    assert "Strong setup" in strength
    assert "High confidence" in confidence


def test_analyst_translation_is_more_precise_than_beginner():
    beginner_strength = explain_strength("B", mode="beginner")
    analyst_strength = explain_strength("B", mode="analyst")
    beginner_confidence = explain_confidence("medium", mode="beginner")
    analyst_confidence = explain_confidence("medium", mode="analyst")

    assert "Tier B" in analyst_strength
    assert "Tier B" not in beginner_strength
    assert "historical reliability" in analyst_confidence
    assert "historical reliability" not in beginner_confidence


def test_confidence_wording_remains_non_predictive():
    low = explain_confidence("low", mode="beginner").lower()
    high = explain_confidence("high", mode="analyst").lower()

    assert "will" not in low
    assert "will" not in high
    assert "guarantee" not in low
    assert "guarantee" not in high


def test_translation_helpers_avoid_advisory_language():
    blob = " ".join(
        [
            explain_strength("A", mode="beginner"),
            explain_strength("C", mode="analyst"),
            explain_confidence("strong", mode="beginner"),
            explain_confidence("weak", mode="analyst"),
        ]
    )
    assert contains_advisory_language(blob) is False
