"""Ticker analysis service for API responses."""

from __future__ import annotations

from typing import Any

from app.data.processor import canonicalize_symbol

from backend.app.core.config import DISCLAIMER, public_mode
from backend.app.services.engine_context import build_ticker_payload


def _safe_float(value: Any, fallback: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback


def _signal_count(stats: dict[str, Any], holding_window_stats: dict[str, dict]) -> int:
    direct_count = int(_safe_float(stats.get("signal_count"), 0.0))
    if direct_count > 0:
        return direct_count
    return sum(int(_safe_float(values.get("count"), 0.0)) for values in holding_window_stats.values())


def _quick_take(stats: dict[str, Any], holding_window_stats: dict[str, dict]) -> list[str]:
    signal_count = _signal_count(stats, holding_window_stats)
    if signal_count <= 0:
        return [
            "There is not enough completed signal history to give this ticker a clean quick take yet.",
            "The dashboard should treat this as insufficient data rather than a weak or strong setup.",
            "Review data coverage before using this ticker in a portfolio plan.",
        ]

    win_rate = _safe_float(stats.get("win_rate"), 0.0)
    median_return = _safe_float(stats.get("median_return"), 0.0)
    strength = "strong" if win_rate >= 0.60 else "mixed" if win_rate >= 0.45 else "weak"
    lines = [
        f"This ticker currently reads as {strength} from {signal_count} completed signal(s).",
        f"It closed positive about {win_rate:.0%} of the time in the sample.",
        f"The typical outcome centers around median return near {median_return:.2%}.",
    ]
    if holding_window_stats:
        lines.append("Holding-window behavior is available for comparison.")
    else:
        lines.append("Holding-window comparison is limited until more completed observations are available.")
    return lines


def _holding_windows(holding_window_stats: dict[str, dict]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for window, values in holding_window_stats.items():
        rows.append(
            {
                "holding_window": str(window),
                "count": int(_safe_float(values.get("count"), 0.0)),
                "win_rate": _safe_float(values.get("win_rate"), 0.0),
                "median_return": _safe_float(values.get("median_return"), 0.0),
                "average_return": _safe_float(values.get("avg_return"), 0.0),
            }
        )
    return rows


def _risk_profile(behavior: dict[str, Any], signal_count: int) -> list[str]:
    lines = [
        behavior.get("reliability"),
        behavior.get("tier_profile"),
    ]
    if signal_count <= 0:
        lines.insert(0, "Risk context is limited because this ticker does not have completed signal history in the current dataset.")
    return [str(line) for line in lines if line]


def get_ticker_analysis(ticker: str, mode: str | None = None) -> dict[str, Any]:
    """Return ticker analysis data in a frontend-friendly JSON shape."""
    normalized_ticker = canonicalize_symbol(str(ticker or "").strip())
    drilldown, metrics = build_ticker_payload(normalized_ticker, mode)
    stats = metrics.get("stats", {}) if isinstance(metrics, dict) else {}
    behavior = metrics.get("behavior", {}) if isinstance(metrics, dict) else {}
    holding_window_stats = drilldown.get("holding_window_stats", {}) if isinstance(drilldown, dict) else {}
    signal_count = _signal_count(stats, holding_window_stats)

    return {
        "ticker": normalized_ticker,
        "mode": public_mode(mode),
        "quick_take": _quick_take(stats, holding_window_stats),
        "best_holding_window": str(stats.get("best_window") or ""),
        "holding_windows": _holding_windows(holding_window_stats),
        "risk_profile": _risk_profile(behavior, signal_count),
        "what_to_watch": [
            "Review liquidity and volume support before acting.",
            "Compare the assigned holding window with the ticker's historical behavior.",
            "Treat small samples as supporting context, not certainty.",
        ],
        "execution_behavior": [line for line in [behavior.get("holding_window"), behavior.get("consistency")] if line],
        "disclaimer": DISCLAIMER,
    }
