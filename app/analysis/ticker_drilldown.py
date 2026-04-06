"""Ticker drilldown layer for deeper, structured stock behavior analysis."""

from __future__ import annotations

from typing import Any

import pandas as pd


TICKER_COLUMNS = ["ticker", "instrument"]
RETURN_COLUMNS = ["net_return_pct", "net_return", "return_pct", "return"]
TIER_COLUMNS = ["quality_tier", "tier"]
NORMALIZED_RETURN_COLUMN = "_normalized_return_pct"
PATTERN_SUMMARY_THRESHOLD_PCT = 0.3


def _resolve_first_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for column in candidates:
        if column in df.columns:
            return column
    return None


def _resolve_ticker_column(df: pd.DataFrame) -> str | None:
    return _resolve_first_column(df, TICKER_COLUMNS)


def _resolve_return_column(df: pd.DataFrame) -> str | None:
    return _resolve_first_column(df, RETURN_COLUMNS)


def _normalize_returns_to_percentage_points(returns: pd.Series, return_column: str) -> pd.Series:
    if return_column in {"net_return", "return"}:
        return returns * 100.0
    return returns


def _attach_normalized_returns(df: pd.DataFrame, return_column: str) -> pd.DataFrame:
    scoped = df.copy()
    returns = pd.to_numeric(scoped[return_column], errors="coerce")
    scoped[NORMALIZED_RETURN_COLUMN] = _normalize_returns_to_percentage_points(returns, return_column)
    return scoped


def _resolve_tier_column(df: pd.DataFrame) -> str | None:
    return _resolve_first_column(df, TIER_COLUMNS)


def _scope_to_ticker(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    ticker_column = _resolve_ticker_column(df)
    if df.empty or ticker_column is None:
        return pd.DataFrame(columns=df.columns)
    scoped = df[df[ticker_column].astype(str) == str(ticker)].copy()
    return scoped


def _format_holding_window(value: Any) -> str:
    if pd.isna(value):
        return "unknown"
    try:
        numeric_value = float(value)
        if numeric_value.is_integer():
            return f"{int(numeric_value)}D"
    except (TypeError, ValueError):
        pass

    value_str = str(value).strip()
    if not value_str:
        return "unknown"
    if value_str.upper().endswith("D"):
        return value_str.upper()
    return f"{value_str}D"


def _build_group_stats(group_df: pd.DataFrame, return_column: str) -> dict[str, float | int]:
    returns = pd.to_numeric(group_df[return_column], errors="coerce").dropna()
    count = int(returns.size)
    if count == 0:
        return {"count": 0, "win_rate": 0.0, "median_return": 0.0, "avg_return": 0.0}

    wins = int((returns > 0).sum())
    return {
        "count": count,
        "win_rate": float(wins / count),
        "median_return": float(returns.median()),
        "avg_return": float(returns.mean()),
    }


def compute_signal_breakdown(df: pd.DataFrame, ticker: str) -> list[dict[str, Any]]:
    scoped = _scope_to_ticker(df, ticker)
    if scoped.empty:
        return []

    return_column = _resolve_return_column(scoped)
    if return_column is not None:
        scoped = _attach_normalized_returns(scoped, return_column)
    tier_column = _resolve_tier_column(scoped)

    if "date" in scoped.columns:
        scoped["_sort_date"] = pd.to_datetime(scoped["date"], errors="coerce")
        scoped = scoped.sort_values("_sort_date", ascending=False, na_position="last")

    signals: list[dict[str, Any]] = []
    for _, row in scoped.iterrows():
        signal: dict[str, Any] = {}

        if "date" in scoped.columns and not pd.isna(row.get("date")):
            parsed_date = pd.to_datetime(row.get("date"), errors="coerce")
            signal["date"] = parsed_date.strftime("%Y-%m-%d") if not pd.isna(parsed_date) else str(row.get("date"))

        if "holding_window" in scoped.columns:
            signal["holding_window"] = _format_holding_window(row.get("holding_window"))

        if return_column is not None:
            return_value = pd.to_numeric(row.get(NORMALIZED_RETURN_COLUMN), errors="coerce")
            if not pd.isna(return_value):
                return_float = float(return_value)
                signal["return_pct"] = return_float
                signal["win_loss"] = "Win" if return_float > 0 else "Loss"

        if tier_column is not None and not pd.isna(row.get(tier_column)):
            signal["quality_tier"] = str(row.get(tier_column))

        if "volatility_bucket" in scoped.columns and not pd.isna(row.get("volatility_bucket")):
            signal["volatility_bucket"] = str(row.get("volatility_bucket"))

        signals.append(signal)

    return signals


def compute_holding_window_stats(df: pd.DataFrame, ticker: str) -> dict[str, dict[str, float | int]]:
    scoped = _scope_to_ticker(df, ticker)
    return_column = _resolve_return_column(scoped)
    if scoped.empty or return_column is None or "holding_window" not in scoped.columns:
        return {}
    scoped = _attach_normalized_returns(scoped, return_column)

    stats: dict[str, dict[str, float | int]] = {}
    for window, group in scoped.groupby("holding_window", dropna=True):
        stats[_format_holding_window(window)] = _build_group_stats(group, NORMALIZED_RETURN_COLUMN)

    return stats


def compute_return_distribution(df: pd.DataFrame, ticker: str) -> dict[str, int]:
    distribution = {"negative": 0, "small_positive": 0, "strong_positive": 0}
    scoped = _scope_to_ticker(df, ticker)
    return_column = _resolve_return_column(scoped)
    if scoped.empty or return_column is None:
        return distribution

    scoped = _attach_normalized_returns(scoped, return_column)
    returns = pd.to_numeric(scoped[NORMALIZED_RETURN_COLUMN], errors="coerce").dropna()
    if returns.empty:
        return distribution

    distribution["negative"] = int((returns <= 0).sum())
    distribution["small_positive"] = int(((returns > 0) & (returns < 3.0)).sum())
    distribution["strong_positive"] = int((returns >= 3.0).sum())
    return distribution


def compute_tier_performance(df: pd.DataFrame, ticker: str) -> dict[str, dict[str, float | int]]:
    scoped = _scope_to_ticker(df, ticker)
    return_column = _resolve_return_column(scoped)
    tier_column = _resolve_tier_column(scoped)
    if scoped.empty or return_column is None or tier_column is None:
        return {}
    scoped = _attach_normalized_returns(scoped, return_column)

    stats: dict[str, dict[str, float | int]] = {}
    for tier, group in scoped.groupby(tier_column, dropna=True):
        stats[str(tier)] = _build_group_stats(group, NORMALIZED_RETURN_COLUMN)

    return stats


def compute_volatility_performance(df: pd.DataFrame, ticker: str) -> dict[str, dict[str, float | int]]:
    scoped = _scope_to_ticker(df, ticker)
    return_column = _resolve_return_column(scoped)
    if scoped.empty or return_column is None or "volatility_bucket" not in scoped.columns:
        return {}
    scoped = _attach_normalized_returns(scoped, return_column)

    stats: dict[str, dict[str, float | int]] = {}
    for bucket, group in scoped.groupby("volatility_bucket", dropna=True):
        stats[str(bucket)] = _build_group_stats(group, NORMALIZED_RETURN_COLUMN)

    return stats


def _pick_best_bucket(stats: dict[str, dict[str, float | int]]) -> tuple[str, dict[str, float | int]] | None:
    if not stats:
        return None

    ranked = sorted(
        stats.items(),
        key=lambda item: (
            float(item[1].get("win_rate", 0.0)),
            float(item[1].get("median_return", 0.0)),
            float(item[1].get("avg_return", 0.0)),
            int(item[1].get("count", 0)),
        ),
        reverse=True,
    )
    return ranked[0]


def build_pattern_summary(
    holding_window_stats: dict[str, dict[str, float | int]],
    tier_performance: dict[str, dict[str, float | int]],
    volatility_performance: dict[str, dict[str, float | int]],
    return_distribution: dict[str, int],
    signal_count: int,
) -> str:
    if signal_count < 3:
        return "There is not much data for this stock yet, so the pattern is still limited."

    if len(holding_window_stats) >= 2:
        ranked_windows = sorted(
            holding_window_stats.items(),
            key=lambda item: (
                float(item[1].get("win_rate", 0.0)),
                float(item[1].get("median_return", 0.0)),
                float(item[1].get("avg_return", 0.0)),
            ),
            reverse=True,
        )
        top_window, top_stats = ranked_windows[0]
        second_window, second_stats = ranked_windows[1]
        if (
            float(top_stats.get("win_rate", 0.0)) >= float(second_stats.get("win_rate", 0.0)) + 0.1
            or float(top_stats.get("median_return", 0.0))
            >= float(second_stats.get("median_return", 0.0)) + PATTERN_SUMMARY_THRESHOLD_PCT
        ):
            return f"This stock tends to hold up better on {top_window} than {second_window} in this dataset."

    best_tier = _pick_best_bucket(tier_performance)
    if best_tier is not None and len(tier_performance) >= 2:
        tier_name, tier_stats = best_tier
        if int(tier_stats.get("count", 0)) >= 2 and float(tier_stats.get("win_rate", 0.0)) >= 0.6:
            return f"This stock looks strongest when the {tier_name} quality setups show up."

    best_volatility = _pick_best_bucket(volatility_performance)
    if best_volatility is not None and len(volatility_performance) >= 2:
        bucket, bucket_stats = best_volatility
        if int(bucket_stats.get("count", 0)) >= 2:
            return f"For this stock, {bucket} volatility setups have looked more stable so far."

    negative = int(return_distribution.get("negative", 0))
    strong_positive = int(return_distribution.get("strong_positive", 0))
    if negative > strong_positive:
        return "This stock has shown more weak closes than strong wins in this sample."

    return "This stock has mixed results so far, with no single pattern standing out clearly."


def build_ticker_drilldown(df: pd.DataFrame, ticker: str) -> dict[str, Any]:
    scoped = _scope_to_ticker(df, ticker)
    signal_count = int(len(scoped))

    signals = compute_signal_breakdown(df, ticker)
    holding_window_stats = compute_holding_window_stats(df, ticker)
    return_distribution = compute_return_distribution(df, ticker)
    tier_performance = compute_tier_performance(df, ticker)
    volatility_performance = compute_volatility_performance(df, ticker)

    if signal_count == 0:
        pattern_summary = "There is not enough data to say much about this stock yet."
    else:
        pattern_summary = build_pattern_summary(
            holding_window_stats=holding_window_stats,
            tier_performance=tier_performance,
            volatility_performance=volatility_performance,
            return_distribution=return_distribution,
            signal_count=signal_count,
        )

    return {
        "signals": signals,
        "holding_window_stats": holding_window_stats,
        "return_distribution": return_distribution,
        "tier_performance": tier_performance,
        "volatility_performance": volatility_performance,
        "pattern_summary": pattern_summary,
    }
