"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import pandas as pd

from app.analysis.ticker_drilldown import build_ticker_drilldown
from app.data.ingest import ingest_dataset
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
from app.insights.embedded import generate_embedded_insights, render_embedded_insights
from app.planner.allocation import generate_portfolio_allocation
from app.planner.portfolio_ui import render_portfolio_plan
from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked


def main() -> None:
    """Run the Streamlit shell with Analyst Insights and Portfolio Plan sections."""
    import streamlit as st

    st.set_page_config(
        page_title="JSE Decision Support Dashboard",
        page_icon="📈",
        layout="wide",
    )

    st.title("JSE Decision Support Dashboard")
    st.caption("Sprint 8 shell: dataset loading, Analyst Insights, Portfolio Plan, and Explanation Layer.")

    canonical_df, meta, issues = ingest_dataset("demo")
    st.markdown("### Data Status")
    st.write(
        {
            "dataset_id": meta.get("dataset_id"),
            "source": meta.get("source"),
            "row_count": int(len(canonical_df)),
            "validation_issues": issues,
        }
    )

    if canonical_df.empty:
        st.warning("No rows were loaded from the data layer. Please verify demo dataset files.")
        return

    st.markdown("### Main Dashboard")
    st.dataframe(canonical_df.head(50), use_container_width=True)

    demo_payload = run_demo()
    ranked_df = demo_payload.get("ranked", pd.DataFrame())
    analyst_df = build_analyst_dataset(canonical_df, ranked_df)

    insights_tab, ticker_tab, plan_tab = st.tabs(["Analyst Insights", "Ticker Analysis", "Portfolio Plan"])

    with insights_tab:
        render_analyst_insights(analyst_df, st_module=st, analyst_mode=True)

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

    with plan_tab:
        st.markdown("### Portfolio Plan")
        total_capital = st.number_input(
            "Total capital",
            min_value=0.0,
            value=100_000.0,
            step=5_000.0,
        )

        if ranked_df.empty:
            st.info("Portfolio Plan unavailable: ranked outputs were not generated.")
            return

        trade_rows = coerce_trade_rows_from_ranked(ranked_df)
        allocation_payload = generate_portfolio_allocation(trade_rows, total_capital)
        allocations = allocation_payload.get("allocations", [])

        # Attach lightweight context fields used by portfolio UI reason labels.
        enriched_allocations = []
        for row, allocation in zip(trade_rows, allocations):
            enriched_allocations.append({**allocation, **row})

        insights_payload = generate_embedded_insights(trade_rows, enriched_allocations)
        render_embedded_insights(insights_payload, st_module=st)

        render_portfolio_plan(
            enriched_allocations,
            total_capital=total_capital,
            st_module=st,
            signals_df=ranked_df,
        )


if __name__ == "__main__":
    main()
