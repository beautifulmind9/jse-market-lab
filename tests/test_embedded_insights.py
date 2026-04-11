import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.embedded import generate_embedded_insights


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
