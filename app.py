"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import pandas as pd

from app.analysis.ticker_drilldown import build_ticker_drilldown
from app.analysis.ticker_intelligence import compute_ticker_metrics
from app.data.ingest import ingest_dataset
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
from app.insights.embedded import generate_embedded_insights, render_embedded_insights
from app.planner.allocation import generate_portfolio_allocation
from app.planner.portfolio_ui import render_portfolio_plan
from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked


def _has_analyst_insight_content(trades_df: pd.DataFrame, *, analyst_mode: bool) -> bool:
    if not analyst_mode or trades_df.empty:
        return False
    return any(column in trades_df.columns for column in ("net_return_pct", "net_return", "return_pct", "return"))


def _render_data_status_summary(
    st_module,
    *,
    source: str | None,
    row_count: int,
    issues: dict[str, list[str]] | None,
    dataset_id: str | None,
    analyst_mode: bool,
) -> None:
    issues = issues or {}
    errors = issues.get("errors", [])
    warnings = issues.get("warnings", [])

    st_module.markdown("#### Data Status")
    status_col, quality_col = st_module.columns(2)
    with status_col:
        st_module.markdown(f"**Source:** {source or 'Unknown'}")
        st_module.markdown(f"**Rows loaded:** {row_count}")
        st_module.markdown(f"**Errors:** {len(errors)}")
    with quality_col:
        st_module.markdown(f"**Warnings:** {len(warnings)}")
        if analyst_mode:
            st_module.markdown(f"**Dataset ID:** {dataset_id or 'N/A'}")

    if warnings:
        st_module.markdown("**Warning details**")
        for warning in warnings:
            st_module.markdown(f"- {warning}")
    else:
        st_module.caption("No ingestion warnings were reported for this dataset.")

    if errors:
        st_module.markdown("**Error details**")
        for error in errors:
            st_module.markdown(f"- {error}")
    else:
        st_module.caption("No ingestion errors were reported for this dataset.")


def main() -> None:
    """Run the Streamlit shell with Analyst Insights and Portfolio Plan sections."""
    import streamlit as st

    st.set_page_config(
        page_title="JSE Decision Support Dashboard",
        page_icon="📈",
        layout="wide",
    )

    st.title("JSE Market Lab")
    mode = st.radio("Mode", options=["Beginner", "Analyst"], horizontal=True, index=0)
    mode_token = mode.lower()

    canonical_df, meta, issues = ingest_dataset("demo")

    if canonical_df.empty:
        st.warning("No rows were loaded from the data layer. Please verify demo dataset files.")
        return

    demo_payload = run_demo()
    ranked_df = demo_payload.get("ranked", pd.DataFrame())
    analyst_df = build_analyst_dataset(canonical_df, ranked_df)
    trade_rows = coerce_trade_rows_from_ranked(ranked_df) if not ranked_df.empty else []

    default_capital = 100_000.0
    selected_capital = float(st.session_state.get("total_capital", default_capital))

    if ranked_df.empty:
        enriched_allocations: list[dict] = []
    else:
        allocation_payload = generate_portfolio_allocation(trade_rows, selected_capital)
        base_allocations = allocation_payload.get("allocations", [])
        enriched_allocations = [{**allocation, **row} for row, allocation in zip(trade_rows, base_allocations)]

    if trade_rows:
        insights_payload = generate_embedded_insights(trade_rows, enriched_allocations, mode=mode_token)
    else:
        insights_payload = generate_embedded_insights([], [], mode=mode_token)

    _render_first_run_header(st, mode=mode_token)
    render_embedded_insights(insights_payload, st_module=st)

    portfolio_tab, review_tab, ticker_tab, insights_tab, data_tab = st.tabs(
        ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]
    )

    with portfolio_tab:
        st.markdown("### Portfolio Plan")
        selected_capital = st.number_input(
            "Total capital",
            min_value=0.0,
            value=selected_capital,
            step=5_000.0,
            key="total_capital",
        )
        if ranked_df.empty:
            st.info("Portfolio Plan unavailable: ranked outputs were not generated.")
        else:
            render_portfolio_plan(
                enriched_allocations,
                total_capital=selected_capital,
                st_module=st,
                signals_df=ranked_df,
                mode=mode_token,
                section="plan",
                show_header=False,
            )

    with review_tab:
        st.markdown("### Review")
        if ranked_df.empty:
            st.info("Review unavailable: ranked outputs were not generated.")
        else:
            render_portfolio_plan(
                enriched_allocations,
                total_capital=selected_capital,
                st_module=st,
                signals_df=ranked_df,
                mode=mode_token,
                section="review",
                show_header=False,
            )

    with ticker_tab:
        st.markdown("### Ticker Analysis")
        if analyst_df.empty or "instrument" not in analyst_df.columns:
            st.info("Ticker Analysis is unavailable because no ticker rows are loaded.")
        else:
            ticker_options = sorted(analyst_df["instrument"].dropna().astype(str).unique())
            if not ticker_options:
                st.info("Ticker Analysis is unavailable because no tickers are available.")
            else:
                selected_ticker = st.selectbox("Select ticker", ticker_options)
                ticker_payload = build_ticker_drilldown(analyst_df, selected_ticker)
                ticker_metrics = compute_ticker_metrics(analyst_df, selected_ticker, mode=mode_token)

                st.markdown("#### Ticker Summary")
                st.write(ticker_metrics["summary"])

                st.markdown("#### Behavior Insights")
                for line in ticker_metrics["behavior"].values():
                    st.markdown(f"- {line}")

                st.markdown("#### Pattern Summary")
                st.write(ticker_payload["pattern_summary"])

                signal_df = pd.DataFrame(ticker_payload["signals"])
                signal_count = int(len(signal_df))
                if signal_df.empty or "return_pct" not in signal_df.columns:
                    key_stats = {
                        "Signal Count": signal_count,
                        "Win Rate": 0.0,
                        "Median Return": 0.0,
                        "Average Return": 0.0,
                    }
                else:
                    returns = pd.to_numeric(signal_df["return_pct"], errors="coerce").dropna()
                    if returns.empty:
                        key_stats = {
                            "Signal Count": signal_count,
                            "Win Rate": 0.0,
                            "Median Return": 0.0,
                            "Average Return": 0.0,
                        }
                    else:
                        key_stats = {
                            "Signal Count": signal_count,
                            "Win Rate": float((returns > 0).mean()),
                            "Median Return": float(returns.median()),
                            "Average Return": float(returns.mean()),
                        }

                if mode_token == "analyst":
                    st.markdown("#### Key Stats")
                    st.dataframe(pd.DataFrame([key_stats]), use_container_width=True)

                st.markdown("#### Holding Window Comparison")
                holding_window_df = pd.DataFrame.from_dict(
                    ticker_payload["holding_window_stats"], orient="index"
                )
                if holding_window_df.empty:
                    st.info("No holding window data is ready for this ticker yet.")
                else:
                    st.dataframe(holding_window_df.reset_index().rename(columns={"index": "holding_window"}), use_container_width=True)

                st.markdown("#### Tier Performance")
                tier_df = pd.DataFrame.from_dict(ticker_payload["tier_performance"], orient="index")
                if tier_df.empty:
                    st.info("No tier breakdown is ready for this ticker yet.")
                else:
                    st.dataframe(tier_df.reset_index().rename(columns={"index": "quality_tier"}), use_container_width=True)

                st.markdown("#### Volatility Performance")
                volatility_df = pd.DataFrame.from_dict(ticker_payload["volatility_performance"], orient="index")
                if volatility_df.empty:
                    st.info("No volatility breakdown is ready for this ticker yet.")
                else:
                    st.dataframe(volatility_df.reset_index().rename(columns={"index": "volatility_bucket"}), use_container_width=True)

                st.markdown("#### Return Distribution")
                distribution_df = pd.DataFrame([ticker_payload["return_distribution"]])
                st.dataframe(distribution_df, use_container_width=True)

                st.markdown("#### Signal Breakdown")
                if signal_df.empty:
                    st.info("No signal history is available for this ticker yet.")
                else:
                    st.dataframe(signal_df, use_container_width=True)

    with insights_tab:
        st.markdown("### Analyst Insights")
        if _has_analyst_insight_content(analyst_df, analyst_mode=mode_token == "analyst"):
            render_analyst_insights(analyst_df, st_module=st, analyst_mode=True)
        else:
            st.info("Analyst insights are not available for this dataset yet.")

    with data_tab:
        st.markdown("### Data")
        _render_data_status_summary(
            st,
            source=meta.get("source"),
            row_count=int(len(canonical_df)),
            issues=issues,
            dataset_id=meta.get("dataset_id"),
            analyst_mode=mode_token == "analyst",
        )
        st.markdown("#### Main Dashboard")
        st.dataframe(canonical_df.head(50), use_container_width=True)


def _render_first_run_header(st_module, *, mode: str) -> None:
    st_module.markdown("### JSE Market Lab")
    st_module.markdown(
        "This dashboard helps you review stock opportunities on the Jamaican market using structured rules and risk checks."
    )
    st_module.markdown(
        "It highlights stronger setups, explains the risks, and shows what to watch before making decisions."
    )
    st_module.markdown("**How to read this**")
    st_module.markdown("- The system scans the market and ranks possible trades.")
    st_module.markdown("- Only the stronger setups are selected in the plan below.")
    st_module.markdown("- Each trade explains why it was chosen and what risk is involved.")
    st_module.caption("Based on historical data. Results can vary, so risk still matters.")
    if mode == "beginner":
        st_module.caption("Beginner mode keeps the view simple: explanation first, fewer metrics.")
    else:
        st_module.caption("Analyst mode adds more metrics while keeping explanations first.")


if __name__ == "__main__":
    main()
