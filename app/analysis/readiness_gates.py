from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ReadinessThresholds:
    min_positive_volume_ratio: float = 0.6
    min_trading_days: int = 20
    min_avg_volume_20d: float = 1.0
    min_latest_volume_vs_avg20: float = 0.5
    small_sample_days: int = 60


def _first_existing(df: pd.DataFrame, candidates: list[str]) -> str | None:
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _to_datetime(df: pd.DataFrame, column: str = "date") -> pd.DataFrame:
    out = df.copy()
    if column in out.columns:
        out[column] = pd.to_datetime(out[column], errors="coerce")
    return out


def compute_readiness_metrics(data: pd.DataFrame, thresholds: ReadinessThresholds | None = None) -> pd.DataFrame:
    thresholds = thresholds or ReadinessThresholds()
    df = _to_datetime(data)
    ticker_col = _first_existing(df, ["ticker", "instrument", "symbol"])
    if ticker_col is None or "date" not in df.columns:
        raise ValueError("Input data must contain date and ticker/instrument/symbol fields.")

    close_col = _first_existing(df, ["close", "close_price", "adjusted_close", "adj_close"])
    high_col = _first_existing(df, ["high"])
    low_col = _first_existing(df, ["low"])
    volume_col = _first_existing(df, ["volume"])
    traded_value_col = _first_existing(df, ["value_traded"])
    trades_count_col = _first_existing(df, ["trades_count"])
    signal_date_col = _first_existing(df, ["signal_date", "candidate_date", "entry_date"])

    base_cols = [ticker_col, "date"] + [c for c in [close_col, high_col, low_col, volume_col, traded_value_col, trades_count_col, signal_date_col] if c]
    work = df[base_cols].copy().sort_values([ticker_col, "date"])

    rows: list[dict[str, Any]] = []
    for ticker, grp in work.groupby(ticker_col):
        grp = grp.dropna(subset=["date"]).sort_values("date")
        trading_days_count = int(len(grp))
        vol = grp[volume_col] if volume_col else pd.Series(dtype=float)
        vol_num = pd.to_numeric(vol, errors="coerce") if volume_col else pd.Series([np.nan] * len(grp))
        positive_volume_days = int((vol_num > 0).sum())
        zero_volume_days = int((vol_num.fillna(0) <= 0).sum()) if len(grp) else 0
        positive_volume_ratio = float(positive_volume_days / trading_days_count) if trading_days_count else np.nan

        avg_volume_20d = float(vol_num.tail(20).mean()) if trading_days_count else np.nan
        median_volume_20d = float(vol_num.tail(20).median()) if trading_days_count else np.nan
        avg_volume_60d = float(vol_num.tail(60).mean()) if trading_days_count >= 60 else np.nan
        median_volume_60d = float(vol_num.tail(60).median()) if trading_days_count >= 60 else np.nan

        close = pd.to_numeric(grp[close_col], errors="coerce") if close_col else pd.Series([np.nan] * len(grp))
        estimated_turnover = close * vol_num
        turnover = pd.to_numeric(grp[traded_value_col], errors="coerce") if traded_value_col else estimated_turnover
        turnover = turnover.fillna(estimated_turnover)

        daily_return = close.pct_change()
        vol20 = float(daily_return.tail(20).std()) if trading_days_count >= 2 else np.nan
        vol60 = float(daily_return.tail(60).std()) if trading_days_count >= 60 else np.nan

        rolling_peak = close.cummax()
        drawdown = (close / rolling_peak) - 1.0
        max_drawdown = float(drawdown.min()) if len(drawdown) else np.nan

        if high_col and low_col:
            high = pd.to_numeric(grp[high_col], errors="coerce")
            low = pd.to_numeric(grp[low_col], errors="coerce")
            daily_range_pct = (high - low) / close.replace(0, np.nan)
            avg_range_pct_20d = float(daily_range_pct.tail(20).mean())
            high_low_volatility = bool(avg_range_pct_20d > 0.05) if not np.isnan(avg_range_pct_20d) else False
            volatility_context_available = True
            spread_context_available = True
        else:
            avg_range_pct_20d = np.nan
            high_low_volatility = False
            volatility_context_available = False
            spread_context_available = False

        latest_volume = float(vol_num.iloc[-1]) if len(vol_num) else np.nan
        volume_deterioration = bool(
            not np.isnan(latest_volume)
            and not np.isnan(avg_volume_20d)
            and avg_volume_20d > 0
            and latest_volume < (avg_volume_20d * thresholds.min_latest_volume_vs_avg20)
        )

        liquidity_data_available = bool(volume_col is not None and close_col is not None)
        volume_support_present = bool(
            trading_days_count >= thresholds.min_trading_days
            and positive_volume_ratio >= thresholds.min_positive_volume_ratio
            and (np.isnan(avg_volume_20d) or avg_volume_20d >= thresholds.min_avg_volume_20d)
        )

        timing_assessable = bool(signal_date_col is not None and grp[signal_date_col].notna().any())

        rows.append(
            {
                "ticker": ticker,
                "latest_market_date": grp["date"].max(),
                "candidate_date_field": signal_date_col,
                "trading_days_count": trading_days_count,
                "positive_volume_days": positive_volume_days,
                "zero_volume_days": zero_volume_days,
                "positive_volume_ratio": positive_volume_ratio,
                "avg_volume_20d": avg_volume_20d,
                "median_volume_20d": median_volume_20d,
                "avg_volume_60d": avg_volume_60d,
                "median_volume_60d": median_volume_60d,
                "avg_turnover_20d": float(turnover.tail(20).mean()) if trading_days_count else np.nan,
                "median_turnover_20d": float(turnover.tail(20).median()) if trading_days_count else np.nan,
                "volume_deterioration": volume_deterioration,
                "avg_trades_count_20d": float(pd.to_numeric(grp[trades_count_col], errors="coerce").tail(20).mean()) if trades_count_col else np.nan,
                "close_to_close_volatility_20d": vol20,
                "close_to_close_volatility_60d": vol60,
                "max_close_to_close_drawdown": max_drawdown,
                "avg_range_pct_20d": avg_range_pct_20d,
                "high_low_volatility": high_low_volatility,
                "signal_date_available": timing_assessable,
                "timing_assessable": timing_assessable,
                "liquidity_data_available": liquidity_data_available,
                "volume_support_present": volume_support_present,
                "volatility_context_available": volatility_context_available,
                "spread_context_available": spread_context_available,
                "small_sample": trading_days_count < thresholds.small_sample_days,
                "risk_hook_downside_threshold_candidate": np.nan,
                "risk_hook_price_decline_from_entry": np.nan,
                "risk_hook_volume_deterioration_after_entry": np.nan,
                "risk_hook_signal_invalidation": np.nan,
            }
        )

    return pd.DataFrame(rows)


def evaluate_models(metrics: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    model_rows = []
    ticker_rows = []
    for _, row in metrics.iterrows():
        base = {
            "A_current": (True, "none"),
            "B_minimum": (
                bool(row["liquidity_data_available"] and row["volume_support_present"] and row["timing_assessable"]),
                "failed_minimum_gate",
            ),
            "C_strict": (
                bool(
                    row["liquidity_data_available"]
                    and row["volume_support_present"]
                    and row["timing_assessable"]
                    and row["volatility_context_available"]
                    and row["spread_context_available"]
                ),
                "failed_strict_gate",
            ),
        }
        for model, (funded, fail_reason) in base.items():
            if funded:
                label = "Watch" if row["small_sample"] else "Ready"
                reason = "small_sample_watch" if row["small_sample"] else "pass"
            else:
                label = "Not fundable"
                reason = fail_reason
            if model == "C_strict" and not row["spread_context_available"]:
                reason = "strict_spread_unavailable"
                label = "Incomplete"

            ticker_rows.append({"model": model, "ticker": row["ticker"], "funded": funded, "label": label, "reason": reason})

    detail = pd.DataFrame(ticker_rows)
    for model, grp in detail.groupby("model"):
        model_rows.append(
            {
                "model": model,
                "total_candidate_trades": int(len(grp)),
                "funded_trades_under_model": int(grp["funded"].sum()),
                "excluded_trades": int((~grp["funded"]).sum()),
                "top_exclusion_reason": grp.loc[~grp["funded"], "reason"].mode().iloc[0] if (~grp["funded"]).any() else "none",
                "return_impact_note": "Return/outcome fields unavailable in current readiness input.",
            }
        )
    return pd.DataFrame(model_rows), detail


def write_research_artifacts(metrics: pd.DataFrame, model_summary: pd.DataFrame, model_ticker: pd.DataFrame, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(output_dir / "readiness_gate_by_ticker.csv", index=False)
    model_ticker.to_csv(output_dir / "readiness_gate_by_model.csv", index=False)
    model_summary.to_csv(output_dir / "readiness_gate_summary.csv", index=False)

    report = [
        "# Readiness Gate Research Report",
        "",
        "## Data support and limitations",
        "- This research uses available close/volume fields and optional rich fields when present.",
        "- If return/outcome columns are absent, return impact cannot be evaluated.",
        "- Strict spread gating is marked incomplete when spread/high-low context is unavailable.",
        "",
        "## Model comparison",
        model_summary.to_csv(index=False),
    ]
    (output_dir / "readiness_gate_report.md").write_text("\n".join(report), encoding="utf-8")
