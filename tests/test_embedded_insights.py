import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.embedded import generate_embedded_insights
from app.insights.embedded import render_embedded_insights


def test_embedded_insights_keep_short_sections():
    payload = generate_embedded_insights(
        [
            {
                "quality_tier": "A",
                "volatility_bucket": "low",
                "win_rate": 0.40,
                "avg_return": 0.05,
                "median_return": 0.01,
                "holding_window": 5,
            },
            {
                "quality_tier": "B",
                "volatility_bucket": "medium",
                "win_rate": 0.42,
                "avg_return": 0.04,
                "median_return": 0.01,
                "holding_window": 20,
            },
        ],
        [{"allocation_amount": 0, "eligible_for_funding": True}],
    )

    assert len(payload["what_is_happening"]) <= 3
    assert len(payload["what_to_watch"]) <= 3
    assert 1 <= len(payload["common_mistakes"]) <= 2
    assert isinstance(payload["why_this_matters"], str)


def test_render_embedded_insights_renders_card_and_sections():
    class DummyStreamlit:
        def __init__(self):
            self.markdowns = []

        def markdown(self, text, **_kwargs):
            self.markdowns.append(text)

    dummy_st = DummyStreamlit()
    payload = {
        "what_is_happening": ["Signal quality improved."],
        "what_to_watch": ["Win rate dispersion widened."],
        "common_mistakes": ["Ignoring reserve limits."],
        "why_this_matters": "It frames risk before allocation.",
    }

    render_embedded_insights(payload, st_module=dummy_st)

    assert any("Final Insight" in block for block in dummy_st.markdowns)
    assert any("What’s happening now" in block for block in dummy_st.markdowns)
    assert any("Why this matters now" in block for block in dummy_st.markdowns)


def test_embedded_insights_dedupes_duplicate_lines_per_section():
    payload = generate_embedded_insights(
        [
            {
                "quality_tier": "B",
                "volatility_bucket": "medium",
                "win_rate": 0.40,
                "avg_return": 0.05,
                "median_return": 0.01,
                "holding_window": 5,
            },
            {
                "quality_tier": "B",
                "volatility_bucket": "medium",
                "win_rate": 0.42,
                "avg_return": 0.04,
                "median_return": 0.01,
                "holding_window": 20,
            },
        ],
        [{"allocation_amount": 0, "eligible_for_funding": True}],
    )

    assert payload["what_is_happening"].count(
        "Only a few trades made it into the final picks this time."
    ) == 1
