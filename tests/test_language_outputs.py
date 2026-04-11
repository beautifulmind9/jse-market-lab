import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.embedded import generate_embedded_insights
from app.language.formatter import contains_advisory_language, generate_explanation


def test_generate_explanation_differs_by_mode():
    row = {"quality_tier": "A", "volatility_bucket": "high", "win_rate": 0.61, "avg_return": 0.023}
    beginner = generate_explanation(row, mode="beginner")
    analyst = generate_explanation(row, mode="analyst")

    assert "How often this works" not in beginner
    assert "How often this works" in analyst
    assert "%" in analyst


def test_embedded_insight_has_required_sections():
    payload = generate_embedded_insights(
        [{"quality_tier": "A", "volatility_bucket": "high", "win_rate": 0.4, "avg_return": 0.03, "median_return": 0.01}],
        [{"allocation_amount": 1000, "eligible_for_funding": True}],
    )

    assert set(payload.keys()) == {"what_is_happening", "what_to_watch", "common_mistakes", "why_this_matters"}
    assert 1 <= len(payload["what_is_happening"]) <= 3
    assert 1 <= len(payload["what_to_watch"]) <= 3
    assert 1 <= len(payload["common_mistakes"]) <= 2
    assert isinstance(payload["why_this_matters"], str) and payload["why_this_matters"]


def test_new_copy_avoids_advisory_language():
    payload = generate_embedded_insights(
        [{"quality_tier": "A", "volatility_bucket": "medium", "win_rate": 0.5, "avg_return": 0.01, "median_return": 0.01}],
        [{"allocation_amount": 1000}],
    )
    text_blob = " ".join(payload["what_is_happening"] + payload["what_to_watch"] + payload["common_mistakes"])

    assert contains_advisory_language(text_blob) is False


def test_first_run_helper_renders_without_breaking():
    module_path = ROOT / "app.py"
    spec = importlib.util.spec_from_file_location("app_main", module_path)
    assert spec and spec.loader
    app_main = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_main)

    class DummyStreamlit:
        def __init__(self):
            self.lines = []

        def markdown(self, text):
            self.lines.append(text)

        def caption(self, text):
            self.lines.append(text)

    st = DummyStreamlit()
    app_main._render_first_run_header(st, mode="beginner")
    assert any("How to read this" in line for line in st.lines)
