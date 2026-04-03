import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.planner.warnings import build_earnings_warning


def test_warning_builder_uses_standardized_sentence_for_supported_tones():
    for tone in ("cfa", "jm"):
        warning = build_earnings_warning(
            entry_phase="pre",
            exit_phase="reaction",
            entry_offset=-2,
            overlaps=True,
            objective="income_stability",
            tone=tone,
        )
        assert warning["title"] == "⚠️ Earnings"
        assert warning["body"] == "This trade runs into earnings, so price movement may be unpredictable."
        assert warning["severity"] == "caution"
