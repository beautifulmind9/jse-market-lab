"""Ticker intelligence layer with plain-language behavior summaries."""

from __future__ import annotations

from typing import Any

import pandas as pd

RETURN_COLUMNS = ["net_return_pct", "net_return", "return_pct", "return"]


def _resolve_return_column(df: pd.DataFrame) -> str | None:
    for column in RETURN_COLUMNS:
        if column in df.columns:
            return column
    return None


def _empty_payload() -> dict[str, Any]:
    return {
        "summary": "No clean return data showed up for this ticker yet.",
        "stats": {
            "win_rate": 0.0,
            "median_return": 0.0,
            "avg_return": 0.0,
            "best_window": "N/A",
            "signal_count": 0,
        },
        "behavior": {
            "holding_window": "There is not enough 5D or 20D data to compare holding windows right now.",
            "consistency": "No consistency read is available because return data is missing.",
            "reliability": "Reliability cannot be read because there are no completed signals.",
            "tier_profile": "Tier profile cannot be read because tier data is missing.",
        },
    }


def build_ticker_summary(metrics: dict[str, Any], *, mode: str = "beginner") -> str:
    stats = metrics["stats"]
    signal_count = int(stats["signal_count"])
    win_rate = float(stats["win_rate"]) * 100
    median_return = float(stats["median_return"]) * 100
    best_window = stats["best_window"]

    if str(mode).lower() == "analyst":
        base = (
            f"{metrics['ticker']} closed positive {win_rate:.0f}% of the time, with median return {median_return:.2f}%, "
            f"and the strongest read at {best_window}."
        )
    else:
        base = (
            f"{metrics['ticker']} had more positive closes than negative ones in {win_rate:.0f}% of signals, "
            f"with a typical return near {median_return:.2f}%."
        )

    if signal_count < 8:
        return base[:-1] + f" This read comes from only {signal_count} signals, so confidence is limited."
    return base


def build_ticker_behavior(metrics: dict[str, Any], *, mode: str = "beginner") -> dict[str, str]:
    by_window = metrics.get("by_window", {})

    five_day = by_window.get(5)
    twenty_day = by_window.get(20)
    if five_day and twenty_day:
        if five_day["avg_return"] > twenty_day["avg_return"]:
            holding_window = "5D looks stronger than 20D in this dataset."
        elif five_day["avg_return"] < twenty_day["avg_return"]:
            holding_window = "20D looks stronger than 5D in this dataset."
        else:
            holding_window = "The 5D and 20D windows came out nearly the same for this ticker."
    else:
        holding_window = "There is not enough 5D or 20D data to compare holding windows right now."

    avg_return = float(metrics["stats"]["avg_return"])
    median_return = float(metrics["stats"]["median_return"])
    if abs(avg_return - median_return) <= 0.002:
        consistency = "Average and median returns are close, so results look fairly steady."
    elif avg_return > median_return:
        consistency = "Average return is above typical return, so a few bigger wins are lifting the average."
    else:
        consistency = "Median return sits above average return, so weaker outliers are pulling the average down."

    win_rate = float(metrics["stats"]["win_rate"])
    if win_rate >= 0.6:
        reliability = "How often this works looks steady because most signals closed positive."
    elif win_rate >= 0.5:
        reliability = "Win rate reads as moderate because positive and negative closes are fairly mixed."
    else:
        reliability = "Win rate reads as uneven because negative closes showed up more often."

    tier_counts = metrics.get("tier_counts", {})
    if tier_counts:
        top_tier = max(tier_counts, key=tier_counts.get)
        top_share = (tier_counts[top_tier] / sum(tier_counts.values())) * 100
        tier_profile = f"Setup mix leans to {top_tier}, with about {top_share:.0f}% of rows in that tier."
    else:
        tier_profile = "Tier profile cannot be read because tier data is missing."

    if str(mode).lower() == "analyst":
        reliability = reliability + f" (Win rate: {win_rate:.0%})"

    return {
        "holding_window": holding_window,
        "consistency": consistency,
        "reliability": reliability,
        "tier_profile": tier_profile,
    }


def compute_ticker_metrics(df: pd.DataFrame, ticker: str, *, mode: str = "beginner") -> dict[str, Any]:
    if df.empty or "instrument" not in df.columns:
        return _empty_payload()

    return_column = _resolve_return_column(df)
    if return_column is None:
        return _empty_payload()

    scoped = df[df["instrument"].astype(str) == str(ticker)].copy()
    scoped = scoped.dropna(subset=[return_column])
    if scoped.empty:
        return _empty_payload()

    scoped["return_value"] = pd.to_numeric(scoped[return_column], errors="coerce")
    scoped = scoped.dropna(subset=["return_value"])
    if scoped.empty:
        return _empty_payload()

    grouped = scoped.groupby("holding_window") if "holding_window" in scoped.columns else None
    by_window: dict[int, dict[str, float]] = {}
    if grouped is not None:
        for window, values in grouped:
            by_window[int(window)] = {
                "avg_return": float(values["return_value"].mean()),
                "median_return": float(values["return_value"].median()),
                "win_rate": float((values["return_value"] > 0).mean()),
                "count": int(values["return_value"].size),
            }

    if by_window:
        best_window = max(
            by_window,
            key=lambda w: (
                by_window[w]["avg_return"],
                by_window[w]["median_return"],
                by_window[w]["win_rate"],
            ),
        )
        best_window_label = f"{best_window}D"
    else:
        best_window_label = "N/A"

    tier_column = "quality_tier" if "quality_tier" in scoped.columns else "tier" if "tier" in scoped.columns else None
    tier_counts = (
        scoped[tier_column].astype(str).value_counts().to_dict() if tier_column is not None else {}
    )

    metrics: dict[str, Any] = {
        "ticker": str(ticker),
        "stats": {
            "win_rate": float((scoped["return_value"] > 0).mean()),
            "median_return": float(scoped["return_value"].median()),
            "avg_return": float(scoped["return_value"].mean()),
            "best_window": best_window_label,
            "signal_count": int(scoped["return_value"].size),
        },
        "by_window": by_window,
        "tier_counts": tier_counts,
    }
    metrics["summary"] = build_ticker_summary(metrics, mode=mode)
    metrics["behavior"] = build_ticker_behavior(metrics, mode=mode)
    return {
        "summary": metrics["summary"],
        "stats": metrics["stats"],
        "behavior": metrics["behavior"],
    }
