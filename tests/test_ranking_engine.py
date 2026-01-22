import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.data.metadata import build_metadata
from app.ranking.engine import rank_instruments
from app.ranking.objectives import get_objective_weights


def _base_summary():
    return pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "holding_window": 5,
                "n_trades": 200,
                "win_rate_net": 0.55,
                "median_net_return": 0.04,
                "hit_rate_above_cost": 0.52,
            },
            {
                "instrument": "AAA",
                "holding_window": 10,
                "n_trades": 120,
                "win_rate_net": 0.56,
                "median_net_return": 0.039,
                "hit_rate_above_cost": 0.53,
            },
            {
                "instrument": "BBB",
                "holding_window": 5,
                "n_trades": 80,
                "win_rate_net": 0.52,
                "median_net_return": 0.03,
                "hit_rate_above_cost": 0.5,
            },
            {
                "instrument": "BBB",
                "holding_window": 10,
                "n_trades": 70,
                "win_rate_net": 0.5,
                "median_net_return": 0.029,
                "hit_rate_above_cost": 0.49,
            },
        ]
    )


def test_tier_cap_when_volume_missing():
    df_summary = _base_summary()
    meta = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "volume_available": False,
        "liquidity_ceiling": "B",
    }

    ranked = rank_instruments(df_summary, meta, "active_growth")
    assert (ranked["tier"] == "A").sum() == 0
    assert ranked["warnings"].apply(len).sum() > 0


def test_objective_changes_weights_not_summary():
    df_summary = _base_summary()
    meta = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "volume_available": True,
        "liquidity_ceiling": "A",
    }

    original = df_summary.copy(deep=True)
    ranked_income = rank_instruments(df_summary, meta, "income_stability")
    ranked_growth = rank_instruments(df_summary, meta, "active_growth")

    assert df_summary.equals(original)
    assert get_objective_weights("income_stability") != get_objective_weights(
        "active_growth"
    )
    assert not ranked_income["score_total"].equals(ranked_growth["score_total"])


def test_metadata_without_dates_uses_volume_confirmation():
    df_summary = _base_summary()
    meta = {
        "volume_confirmation_enabled": True,
        "liquidity_ceiling": "A",
    }

    ranked = rank_instruments(df_summary, meta, "active_growth")
    assert ranked["warnings"].apply(len).sum() == 0


def test_guardrail_shifts_to_10d_on_high_turnover():
    df_summary = pd.DataFrame(
        [
            {
                "instrument": "AAA",
                "holding_window": 5,
                "n_trades": 300,
                "win_rate_net": 0.55,
                "median_net_return": 0.04,
                "hit_rate_above_cost": 0.53,
            },
            {
                "instrument": "AAA",
                "holding_window": 10,
                "n_trades": 120,
                "win_rate_net": 0.56,
                "median_net_return": 0.039,
                "hit_rate_above_cost": 0.54,
            },
            {
                "instrument": "BBB",
                "holding_window": 10,
                "n_trades": 90,
                "win_rate_net": 0.52,
                "median_net_return": 0.03,
                "hit_rate_above_cost": 0.5,
            },
            {
                "instrument": "CCC",
                "holding_window": 10,
                "n_trades": 80,
                "win_rate_net": 0.51,
                "median_net_return": 0.029,
                "hit_rate_above_cost": 0.49,
            },
        ]
    )
    meta = {
        "start_date": "2023-01-01",
        "end_date": "2024-01-01",
        "volume_available": True,
        "liquidity_ceiling": "A",
    }

    ranked = rank_instruments(df_summary, meta, "income_stability")
    assert ranked.iloc[0]["best_window"] == 10


def test_rank_handles_missing_dates_and_volume_flag():
    df_summary = _base_summary()
    meta = {
        "volume_confirmation_enabled": True,
        "liquidity_ceiling": "A",
    }

    ranked = rank_instruments(df_summary, meta, "active_growth")
    assert ranked["warnings"].apply(len).sum() == 0
