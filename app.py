"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.data.ingest import ingest_dataset
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
from app.planner.allocation import generate_portfolio_allocation
from app.planner.portfolio_ui import render_portfolio_plan


def _coerce_trade_rows_from_ranked(ranked_df: pd.DataFrame) -> list[dict]:
    """Build minimal planner trade rows from ranked outputs.

    Assumption: ranked outputs do not yet carry full planner fields, so this adapter
    uses safe defaults and preserves available ranking fields for UI visibility.
    """
    trade_rows: list[dict] = []
    for row in ranked_df.to_dict("records"):
        quality_tier = str(row.get("tier", "B") or "B")
        trade_rows.append(
            {
                "instrument": row.get("instrument", "Unknown"),
                "quality_tier": quality_tier,
                "liquidity_pass": True,
                "volatility_bucket": "medium",
                "earnings_warning_severity": "info",
                "confidence_label": "strong" if quality_tier.upper() == "A" else "moderate",
            }
        )
    return trade_rows


def main() -> None:
    """Run the Streamlit shell with Analyst Insights and Portfolio Plan sections."""
    st.set_page_config(
        page_title="JSE Decision Support Dashboard",
        page_icon="📈",
        layout="wide",
    )

    st.title("JSE Decision Support Dashboard")
    st.caption("Sprint 7 shell: dataset loading, Analyst Insights, and Portfolio Plan UI.")

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

    insights_tab, plan_tab = st.tabs(["Analyst Insights", "Portfolio Plan"])

    with insights_tab:
        render_analyst_insights(canonical_df, st_module=st, analyst_mode=True)

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

        trade_rows = _coerce_trade_rows_from_ranked(ranked_df)
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
