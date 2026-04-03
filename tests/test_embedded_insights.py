import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.insights.embedded import generate_embedded_insights


APPROVED = {
    "Most of the stronger trades right now are coming from steadier stocks.",
    "Strong setups are leading this batch.",
    "Only a few trades made it into the final picks this time.",
    "Some trades look good on average, but the results are not consistent.",
    "Short trades are more hit or miss right now.",
    "A few setups have high returns but low win rates, which makes them less reliable.",
}


def test_embedded_insights_use_approved_fast_scan_lines():
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

    lines = payload["what_is_happening"] + payload["what_to_watch"]
    assert lines
    assert all(line in APPROVED for line in lines)
    assert all("\n" not in line for line in lines)
