import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.warnings import build_earnings_warning


def test_pre_offset_uses_positive_days_for_both_tones():
    for tone in ("cfa", "jm"):
        warning = build_earnings_warning(
            entry_phase="pre",
            exit_phase="pre",
            entry_offset=-5,
            overlaps=False,
            objective="income_stability",
            tone=tone,
        )
        assert warning["body"] is not None
        assert "Earnings in 5 trading days" in warning["body"]


def test_non_phase_returns_none_fields():
    warning = build_earnings_warning(
        entry_phase="non",
        exit_phase="non",
        entry_offset=None,
        overlaps=False,
        objective="income_stability",
        tone="cfa",
    )
    assert warning == {"severity": None, "title": None, "body": None}


def test_overlap_appends_line_per_tone():
    jm_warning = build_earnings_warning(
        entry_phase="pre",
        exit_phase="reaction",
        entry_offset=-1,
        overlaps=True,
        objective="income_stability",
        tone="jm",
    )
    cfa_warning = build_earnings_warning(
        entry_phase="pre",
        exit_phase="reaction",
        entry_offset=-1,
        overlaps=True,
        objective="income_stability",
        tone="cfa",
    )
    assert jm_warning["body"].endswith("This trade crosses an earnings phase.")
    assert cfa_warning["body"].endswith("This trade overlaps an earnings-phase boundary.")


def test_reaction_post_severity_and_titles():
    reaction = build_earnings_warning(
        entry_phase="reaction",
        exit_phase="reaction",
        entry_offset=0,
        overlaps=False,
        objective="income_stability",
        tone="cfa",
    )
    post = build_earnings_warning(
        entry_phase="post",
        exit_phase="post",
        entry_offset=4,
        overlaps=False,
        objective="income_stability",
        tone="cfa",
    )
    assert reaction["severity"] == "caution"
    assert reaction["title"] == "⚠️ Earnings reaction window"
    assert post["severity"] == "info"
    assert post["title"] == "ℹ️ Post-earnings window"
