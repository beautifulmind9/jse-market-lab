"""Decision review utilities for post-allocation discipline checks."""

from __future__ import annotations

from typing import Any, Mapping

import pandas as pd


def compute_trade_review(trades_df: pd.DataFrame, signals_df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-trade decision review fields in an empty-safe way."""
    if trades_df is None or trades_df.empty:
        return pd.DataFrame(
            columns=[
                "instrument",
                "followed_rules",
                "deviation_type",
                "selected_rank",
                "best_available_rank",
                "quality_flag",
                "liquidity_flag",
            ]
        )

    signal_rank_lookup = _build_signal_rank_lookup(signals_df)

    reviewed_rows: list[dict[str, Any]] = []
    for idx, trade in trades_df.reset_index(drop=True).iterrows():
        trade_map = trade.to_dict()
        instrument = _as_text(trade_map.get("instrument"), fallback=f"row_{idx + 1}")

        selected_rank = _int_or_none(trade_map.get("selection_rank"))
        best_available_rank = signal_rank_lookup.get(instrument)

        quality_ok = _quality_passes(trade_map)
        liquidity_ok = _liquidity_passes(trade_map)
        rank_ok = True
        if selected_rank is not None and best_available_rank is not None:
            rank_ok = selected_rank <= best_available_rank

        followed_rules = bool(quality_ok and liquidity_ok and rank_ok)
        deviation_type = _resolve_deviation_type(
            followed_rules=followed_rules,
            quality_ok=quality_ok,
            liquidity_ok=liquidity_ok,
            rank_ok=rank_ok,
        )

        reviewed_rows.append(
            {
                "instrument": instrument,
                "followed_rules": followed_rules,
                "deviation_type": deviation_type,
                "selected_rank": selected_rank,
                "best_available_rank": best_available_rank,
                "quality_flag": "pass" if quality_ok else "fail",
                "liquidity_flag": "pass" if liquidity_ok else "fail",
            }
        )

    return pd.DataFrame(reviewed_rows)


def detect_decision_mistakes(
    trades_df: pd.DataFrame,
    signals_df: pd.DataFrame,
    allocation_df: pd.DataFrame,
) -> list[dict[str, Any]]:
    """Detect selection mistakes from trade, signal, and allocation context."""
    if trades_df is None or trades_df.empty:
        return []

    review_df = compute_trade_review(trades_df, signals_df)
    mistakes: list[dict[str, Any]] = []

    for row in review_df.to_dict("records"):
        instrument = row.get("instrument", "Trade")
        selected_rank = row.get("selected_rank")
        best_rank = row.get("best_available_rank")

        if selected_rank is not None and best_rank is not None and selected_rank > best_rank:
            mistakes.append(
                {
                    "type": "ignored_higher_rank",
                    "message": (
                        f"{instrument} was selected at rank #{selected_rank} while rank #{best_rank} "
                        "was available."
                    ),
                    "impact": "Selection order drifted from top-ranked signals.",
                }
            )

        if row.get("quality_flag") == "fail":
            mistakes.append(
                {
                    "type": "low_quality_trade",
                    "message": f"{instrument} did not meet the quality tier rule.",
                    "impact": "Trade quality consistency dropped.",
                }
            )

        if row.get("liquidity_flag") == "fail":
            mistakes.append(
                {
                    "type": "liquidity_violation",
                    "message": f"{instrument} failed the liquidity screen.",
                    "impact": "Execution reliability may be weaker.",
                }
            )

    allocation_safe = allocation_df if allocation_df is not None else pd.DataFrame()
    allocation_pct_series = _coerce_allocation_pct_series(allocation_safe)
    if not allocation_safe.empty and allocation_pct_series is not None:
        over_allocated = allocation_safe[allocation_pct_series > 0.70]
        for _, row in over_allocated.iterrows():
            instrument = _as_text(row.get("instrument"), fallback="Trade")
            allocation_pct = float(pd.to_numeric(row.get("allocation_pct"), errors="coerce") or 0.0)
            mistakes.append(
                {
                    "type": "over_allocation",
                    "message": f"{instrument} received {allocation_pct:.0%}, above the 70% cap.",
                    "impact": "Portfolio concentration became too high.",
                }
            )

    merged_df = trades_df.copy()
    if not allocation_safe.empty and "instrument" in merged_df.columns and "instrument" in allocation_safe.columns:
        if "allocation_pct" not in merged_df.columns and "allocation_pct" in allocation_safe.columns:
            merged_df = merged_df.merge(
                allocation_safe[["instrument", "allocation_pct"]],
                on="instrument",
                how="left",
            )
    merged_df = _normalize_allocation_pct_column(merged_df)

    cooldown_mask = _build_cooldown_mask(merged_df)
    if cooldown_mask.any():
        flagged = merged_df[cooldown_mask]
        for _, row in flagged.iterrows():
            instrument = _as_text(row.get("instrument"), fallback="Trade")
            allocation_pct = float(pd.to_numeric(row.get("allocation_pct"), errors="coerce") or 0.0)
            if allocation_pct > 0:
                mistakes.append(
                    {
                        "type": "cooldown_violation",
                        "message": f"{instrument} was funded while cooldown was active.",
                        "impact": "Cooldown discipline was broken.",
                    }
                )

    return mistakes


def _coerce_allocation_pct_series(df: pd.DataFrame) -> pd.Series | None:
    if df is None or df.empty:
        return None
    if "allocation_pct" not in df.columns:
        return None
    return pd.to_numeric(df["allocation_pct"], errors="coerce").fillna(0.0)


def _normalize_allocation_pct_column(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return df

    if "allocation_pct" in df.columns:
        return df

    candidates = [col for col in ("allocation_pct_x", "allocation_pct_y") if col in df.columns]
    if not candidates:
        return df

    normalized = pd.to_numeric(df[candidates[0]], errors="coerce")
    for col in candidates[1:]:
        normalized = normalized.combine_first(pd.to_numeric(df[col], errors="coerce"))
    df = df.copy()
    df["allocation_pct"] = normalized
    return df


def build_behavior_summary(trades_df: pd.DataFrame, review_df: pd.DataFrame) -> list[str]:
    """Build 2-4 plain-language observations about trade selection behavior."""
    trade_count = int(len(trades_df)) if trades_df is not None else 0
    if review_df is None or review_df.empty or trade_count == 0:
        return [
            "No trade behavior to review yet.",
            "Add a few completed selections to see a pattern summary.",
        ]

    total = max(int(len(review_df)), 1)
    followed = int(pd.to_numeric(review_df["followed_rules"], errors="coerce").fillna(0).astype(int).sum())
    rule_rate = followed / total

    rank_misses = int((review_df["deviation_type"] == "rank_deviation").sum())
    quality_fails = int((review_df["quality_flag"] == "fail").sum())
    liquidity_fails = int((review_df["liquidity_flag"] == "fail").sum())

    insights: list[str] = [
        f"{followed} of {total} trades followed the selection rules ({rule_rate:.0%}).",
        f"Selection order drift showed on {rank_misses} trade(s).",
    ]

    if quality_fails > 0:
        insights.append(f"{quality_fails} trade(s) came in below the quality rule.")
    else:
        insights.append("All reviewed trades stayed within the quality rule.")

    if liquidity_fails > 0:
        insights.append(f"Liquidity checks failed on {liquidity_fails} trade(s).")
    else:
        insights.append("There was enough trading activity across the selected trades.")

    return insights[:4]


def compute_discipline_score(review_df: pd.DataFrame) -> float:
    """Compute discipline score on a 0-100 scale from review adherence."""
    if review_df is None or review_df.empty:
        return 0.0

    total = max(int(len(review_df)), 1)
    followed_rate = float(review_df["followed_rules"].fillna(False).astype(bool).mean())

    rank_series = pd.Series([True] * total)
    if "selected_rank" in review_df.columns and "best_available_rank" in review_df.columns:
        rank_series = review_df.apply(
            lambda row: _rank_passes(row.get("selected_rank"), row.get("best_available_rank")),
            axis=1,
        )
    rank_rate = float(rank_series.astype(bool).mean())

    quality_rate = float((review_df.get("quality_flag", pd.Series(["fail"] * total)) == "pass").mean())

    score = (followed_rate * 0.5 + rank_rate * 0.25 + quality_rate * 0.25) * 100
    return round(float(score), 1)


def _build_signal_rank_lookup(signals_df: pd.DataFrame) -> dict[str, int]:
    if signals_df is None or signals_df.empty or "instrument" not in signals_df.columns:
        return {}

    working = signals_df.copy()
    if "rank" not in working.columns:
        if "score_total" in working.columns:
            working = working.sort_values("score_total", ascending=False).reset_index(drop=True)
            working["rank"] = working.index + 1
        else:
            working = working.reset_index(drop=True)
            working["rank"] = working.index + 1

    lookup: dict[str, int] = {}
    for _, row in working.iterrows():
        instrument = _as_text(row.get("instrument"))
        rank = _int_or_none(row.get("rank"))
        if instrument and rank is not None and instrument not in lookup:
            lookup[instrument] = rank
    return lookup


def _quality_passes(trade: Mapping[str, Any]) -> bool:
    quality_tier = _as_text(trade.get("quality_tier")).upper()
    return quality_tier != "C"


def _liquidity_passes(trade: Mapping[str, Any]) -> bool:
    value = trade.get("liquidity_pass")
    if value is None:
        return True
    return bool(value)


def _resolve_deviation_type(
    *,
    followed_rules: bool,
    quality_ok: bool,
    liquidity_ok: bool,
    rank_ok: bool,
) -> str | None:
    if followed_rules:
        return None
    if not rank_ok:
        return "rank_deviation"
    if not quality_ok:
        return "quality_deviation"
    if not liquidity_ok:
        return "liquidity_deviation"
    return "rule_deviation"


def _build_cooldown_mask(df: pd.DataFrame) -> pd.Series:
    if df is None or df.empty:
        return pd.Series(dtype=bool)

    cooldown_active = pd.Series(False, index=df.index)
    for column in ("cooldown_active", "cooldown_violation", "in_cooldown"):
        if column in df.columns:
            cooldown_active = cooldown_active | df[column].fillna(False).astype(bool)

    if "days_since_exit" in df.columns:
        days = pd.to_numeric(df["days_since_exit"], errors="coerce")
        cooldown_active = cooldown_active | (days < 5)

    return cooldown_active


def _rank_passes(selected_rank: Any, best_available_rank: Any) -> bool:
    selected = _int_or_none(selected_rank)
    best = _int_or_none(best_available_rank)
    if selected is None or best is None:
        return True
    return selected <= best


def _int_or_none(value: Any) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_text(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    token = str(value).strip()
    return token or fallback
