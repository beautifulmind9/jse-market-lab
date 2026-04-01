"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import pandas as pd

from app.data.ingest import ingest_dataset
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
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

    insights_tab, plan_tab = st.tabs(["Analyst Insights", "Portfolio Plan"])

    with insights_tab:
        render_analyst_insights(analyst_df, st_module=st, analyst_mode=True)

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

        render_portfolio_plan(
            enriched_allocations,
            total_capital=total_capital,
            st_module=st,
        )


if __name__ == "__main__":
    main()
