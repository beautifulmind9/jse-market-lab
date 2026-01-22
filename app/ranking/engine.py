"""Ranking engine orchestrator."""

from __future__ import annotations

from typing import Dict, List

import pandas as pd

from .objectives import get_objective_weights, get_window_emphasis
from .scoring import compute_components, score_window
from .tiering import apply_liquidity_cap, assign_tier
from .turnover import dataset_years


def rank_instruments(
    df_summary: pd.DataFrame,
    meta: Dict[str, object],
    objective: str,
) -> pd.DataFrame:
    """Rank instruments based on objective and summary metrics."""
    start_date_raw = meta.get("start_date")
    end_date_raw = meta.get("end_date")
    if start_date_raw and end_date_raw:
        start_date = pd.to_datetime(start_date_raw)
        end_date = pd.to_datetime(end_date_raw)
        years = dataset_years(start_date, end_date)
    else:
        years = 1.0

    weights = get_objective_weights(objective)
    emphasis = get_window_emphasis(objective)

    scored, turnover = compute_components(df_summary, years)
    scored["turnover_rate"] = turnover
    scored = score_window(scored, weights, emphasis)

    best_rows: List[dict] = []
    for instrument, group in scored.groupby("instrument"):
        group = group.sort_values("score_window", ascending=False)
        best = group.iloc[0].copy()
        reasons = [f"Top score at {int(best['holding_window'])}D window."]

        if objective == "income_stability" and int(best["holding_window"]) == 5:
            high_turnover = float(best["T"]) > 0.75
            candidate = group[group["holding_window"] == 10]
            if high_turnover and not candidate.empty:
                candidate_row = candidate.iloc[0]
                if candidate_row["score_window"] >= best["score_window"] * 0.95:
                    best = candidate_row.copy()
                    reasons.append("Guardrail: shifted to 10D due to high turnover.")

        tier = assign_tier(float(best["score_window"]))
        volume_available = bool(
            meta.get("volume_confirmation_enabled", meta.get("volume_available", False))
            meta.get(
                "volume_confirmation_enabled",
                meta.get("volume_available", False),
            )
        )
        tier, warning = apply_liquidity_cap(
            tier,
            volume_available,
            str(meta.get("liquidity_ceiling", "B")),
        )
        warnings = [warning] if warning else []

        best_rows.append(
            {
                "instrument": instrument,
                "best_window": int(best["holding_window"]),
                "score_total": float(best["score_window"]),
                "tier": tier,
                "reasons": reasons,
                "warnings": warnings,
            }
        )

    return pd.DataFrame(best_rows).sort_values(
        ["score_total", "instrument"], ascending=[False, True]
    )
