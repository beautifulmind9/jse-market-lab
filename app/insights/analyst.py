"""Analyst-focused insight helpers for validating system behavior."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd

from app.ui.display_labels import clean_dataframe_labels, display_label

FEATURE_COLUMNS = [
    "fast_slope_up",
    "slow_slope_up",
    "spread_widening",
    "volume_confirmed",
    "stale_5d",
    "vol_bucket",
]

PREFERRED_RETURN_COLUMNS = ["net_return_pct", "net_return", "return_pct", "return"]


def resolve_return_column(df: pd.DataFrame, preferred: Sequence[str] | None = None) -> str | None:
    """Return the first available return column from preferred names."""
    columns_to_check = preferred if preferred is not None else PREFERRED_RETURN_COLUMNS
    for column in columns_to_check:
        if column in df.columns:
            return column
    return None


def _missing_columns(df: pd.DataFrame, required_columns: Sequence[str]) -> list[str]:
    return [column for column in required_columns if column not in df.columns]


def grouped_trade_metrics(
    df: pd.DataFrame,
    group_columns: Sequence[str],
    *,
    return_column: str,
) -> pd.DataFrame:
    """Compute grouped analyst metrics for any dimensional slice."""
    required_columns = [*group_columns, return_column]
    missing = _missing_columns(df, required_columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    grouped = (
        df.groupby(list(group_columns), dropna=False)
        .agg(
            count=(return_column, "size"),
            win_rate=(return_column, lambda values: (values > 0).mean()),
            avg_return=(return_column, "mean"),
            median_return=(return_column, "median"),
        )
        .reset_index()
        .sort_values("count", ascending=False)
        .reset_index(drop=True)
    )
    return grouped


def build_feature_insights(
    df: pd.DataFrame,
    *,
    return_column: str,
    feature_columns: Sequence[str] | None = None,
) -> dict[str, pd.DataFrame]:
    """Build grouped summaries for each available feature column."""
    insights: dict[str, pd.DataFrame] = {}
    features_to_use = feature_columns if feature_columns is not None else FEATURE_COLUMNS
    for feature in features_to_use:
        if feature not in df.columns:
            continue
        insights[feature] = grouped_trade_metrics(
            df,
            [feature],
            return_column=return_column,
        )
    return insights


def build_performance_matrix(
    df: pd.DataFrame,
    *,
    return_column: str,
) -> Mapping[str, Any]:
    """Build tier/window summary and matrix pivots."""
    required = ["quality_tier", "holding_window", return_column]
    missing = _missing_columns(df, required)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    summary = grouped_trade_metrics(
        df,
        ["quality_tier", "holding_window"],
        return_column=return_column,
    ).rename(columns={"count": "n_trades"})

    win_rate_matrix = summary.pivot(
        index="quality_tier",
        columns="holding_window",
        values="win_rate",
    )
    median_return_matrix = summary.pivot(
        index="quality_tier",
        columns="holding_window",
        values="median_return",
    )

    best_setups = summary.sort_values(
        ["win_rate", "median_return", "n_trades"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    return {
        "summary": summary,
        "win_rate_matrix": win_rate_matrix,
        "median_return_matrix": median_return_matrix,
        "best_setups": best_setups,
    }


def build_exit_analysis(
    df: pd.DataFrame,
    *,
    return_column: str,
    include_holding_window: bool = True,
) -> pd.DataFrame:
    """Build grouped exit summaries for analyst review."""
    group_columns = ["quality_tier", "exit_reason"]
    if include_holding_window and "holding_window" in df.columns:
        group_columns.append("holding_window")

    return grouped_trade_metrics(
        df,
        group_columns,
        return_column=return_column,
    )


def render_analyst_insights(
    trades_df: pd.DataFrame,
    *,
    st_module=None,
    analyst_mode: bool = True,
) -> None:
    """Render Analyst Insights tab in analyst mode, handling sparse schemas."""
    if not analyst_mode:
        return

    if st_module is None:
        import streamlit as st_module

    return_column = resolve_return_column(trades_df)
    if return_column is None:
        st_module.info(
            "Analyst Insights unavailable: no return column found. "
            f"Expected one of {PREFERRED_RETURN_COLUMNS}."
        )
        return

    insights_tab, matrix_tab, exit_tab = st_module.tabs(
        ["Feature Insights", "Performance Matrix", "Exit Analysis"]
    )

    with insights_tab:
        st_module.subheader("Feature Insights")
        st_module.caption(
            "Question answered: Which setup tags are associated with stronger or weaker outcomes? "
            "This view is only shown when feature-tag columns are present in the dataset."
        )
        insights = build_feature_insights(trades_df, return_column=return_column)
        if not insights:
            st_module.info(
                "Feature Insights is not available yet for this dataset because feature-tag columns are missing."
            )
        for feature, summary in insights.items():
            st_module.markdown(f"#### {display_label(feature)}")
            st_module.dataframe(clean_dataframe_labels(summary, value_columns=[feature]))

    with matrix_tab:
        st_module.subheader("Performance Matrix")
        st_module.caption(
            "Question answered: Which setup tier and holding period combinations have historically behaved best? "
            "Grouping by both matters because setup quality can perform differently at short vs. longer holds."
        )
        try:
            matrix_payload = build_performance_matrix(
                trades_df,
                return_column=return_column,
            )
        except ValueError as error:
            st_module.info(f"Performance Matrix unavailable: {error}")
        else:
            st_module.markdown("#### Grouped Summary")
            st_module.dataframe(clean_dataframe_labels(matrix_payload["summary"]))
            st_module.markdown("#### Win-Rate Matrix")
            st_module.dataframe(clean_dataframe_labels(matrix_payload["win_rate_matrix"].reset_index()))
            st_module.markdown("#### Median-Return Matrix")
            st_module.dataframe(clean_dataframe_labels(matrix_payload["median_return_matrix"].reset_index()))
            st_module.markdown("#### Best Setups")
            st_module.dataframe(clean_dataframe_labels(matrix_payload["best_setups"].head(10)))

    with exit_tab:
        st_module.subheader("Exit Analysis")
        st_module.caption(
            "Question answered: How do trades usually end, and does that exit pattern reveal useful behavior? "
            "If one exit reason dominates, that can indicate whether winners or risk controls are driving outcomes."
        )
        required_cols = {"exit_reason", "quality_tier"}
        if required_cols.issubset(trades_df.columns):
            st_module.dataframe(
                clean_dataframe_labels(
                    build_exit_analysis(trades_df, return_column=return_column),
                    value_columns=["exit_reason"],
                )
            )
        else:
            missing = required_cols - set(trades_df.columns)
            st_module.info(
                "Exit Analysis unavailable — missing required columns: "
                + ", ".join(sorted(missing))
            )
