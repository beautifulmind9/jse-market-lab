import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.embedded import generate_embedded_insights


def test_embedded_insights_returns_both_sections_and_max_three_items():
    trade_rows = [
        {
            "quality_tier": "A",
            "volatility_bucket": "medium",
            "win_rate": 0.62,
            "avg_return": 0.03,
            "median_return": 0.02,
            "holding_window": 5,
        },
        {
            "quality_tier": "A",
            "volatility_bucket": "medium",
            "win_rate": 0.48,
            "avg_return": 0.04,
            "median_return": 0.01,
            "holding_window": 20,
        },
    ]
    allocations = [
        {"allocation_amount": 10_000, "eligible_for_funding": True},
        {"allocation_amount": 0, "eligible_for_funding": True},
    ]

    payload = generate_embedded_insights(trade_rows, allocations)

    assert set(payload.keys()) == {"what_is_happening", "what_to_watch"}
    assert 1 <= len(payload["what_is_happening"]) <= 3
    assert 1 <= len(payload["what_to_watch"]) <= 3


def test_embedded_insights_flags_inconsistency_when_avg_far_above_median():
    payload = generate_embedded_insights(
        [
            {
                "quality_tier": "B",
                "volatility_bucket": "high",
                "win_rate": 0.40,
                "avg_return": 0.05,
                "median_return": 0.01,
                "holding_window": 10,
            },
            {
                "quality_tier": "B",
                "volatility_bucket": "high",
                "win_rate": 0.42,
                "avg_return": 0.04,
                "median_return": 0.01,
                "holding_window": 20,
            },
        ],
        [{"allocation_amount": 0, "eligible_for_funding": True}],
    )

    joined = " ".join(payload["what_to_watch"]).lower()
    assert "average return sits well above median return" in joined
    assert "high-variance" in joined


def test_embedded_insights_fallback_when_data_is_limited():
    payload = generate_embedded_insights([], [])

    assert payload["what_is_happening"]
    assert payload["what_to_watch"]
