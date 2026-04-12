"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import inspect

import pandas as pd

from app.analysis.ticker_drilldown import build_ticker_drilldown
from app.analysis.ticker_intelligence import compute_ticker_metrics
from app.data.processor import canonicalize_symbol
from app.data.ingest import ingest_dataset
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
from app.insights.embedded import generate_embedded_insights, render_embedded_insights
from app.planner.allocation import generate_portfolio_allocation
from app.planner.portfolio_ui import render_portfolio_plan
from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked

_BEGINNER_TABS = ["Portfolio", "Review", "Ticker Analysis"]
_ANALYST_TABS = [*_BEGINNER_TABS, "Analyst Insights", "Data"]


def _has_analyst_insight_content(trades_df: pd.DataFrame, *, analyst_mode: bool) -> bool:
    if not analyst_mode or trades_df.empty:
        return False
    return any(column in trades_df.columns for column in ("net_return_pct", "net_return", "return_pct", "return"))


def _resolve_tabs_for_mode(mode: str) -> list[str]:
    return _ANALYST_TABS if str(mode).lower() == "analyst" else _BEGINNER_TABS


def _extract_ticker_options(df: pd.DataFrame) -> list[str]:
    """Build sorted ticker options from the active canonical dataset."""
    if df.empty:
        return []

    ticker_column = None
    for candidate in ("instrument", "ticker"):
        if candidate in df.columns:
            ticker_column = candidate
            break
    if ticker_column is None:
        return []

    tickers = df[ticker_column].dropna().astype(str).str.strip().map(canonicalize_symbol)
    tickers = tickers[tickers != ""]
    return sorted(tickers.unique())


def _ticker_strength_label(win_rate: float) -> str:
    if win_rate >= 0.60:
        return "strong"
    if win_rate >= 0.45:
        return "mixed"
    return "weak"


def _build_quick_take(*, stats: dict, holding_window_stats: dict[str, dict]) -> list[str]:
    win_rate = float(stats.get("win_rate", 0.0))
    avg_return = float(stats.get("avg_return", 0.0))
    median_return = float(stats.get("median_return", 0.0))

    strength = _ticker_strength_label(win_rate)
    consistency = (
        "returns are fairly steady"
        if abs((avg_return - median_return) * 100) <= 0.3
        else "returns are a bit uneven"
    )
    if len(holding_window_stats) >= 2:
        sorted_windows = sorted(
            holding_window_stats.items(),
            key=lambda item: (
                float(item[1].get("win_rate", 0.0)),
                float(item[1].get("avg_return", 0.0)),
            ),
            reverse=True,
        )
        best_label = sorted_windows[0][0]
        hold_line = f"{best_label} has looked better than shorter alternatives in this sample."
    else:
        hold_line = "There is not enough history yet to compare short and long holding styles."

    return [
        f"This stock looks {strength} based on past signals.",
        f"It closed positive about {win_rate:.0%} of the time.",
        f"So far, {consistency}.",
        hold_line,
    ]


def _build_holding_window_table(holding_window_stats: dict[str, dict], *, analyst_mode: bool) -> pd.DataFrame:
    if not holding_window_stats:
        return pd.DataFrame()
    rows: list[dict] = []
    for window, values in holding_window_stats.items():
        win_rate = float(values.get("win_rate", 0.0))
        avg_return = float(values.get("avg_return", 0.0))
        count = int(values.get("count", 0))
        if win_rate >= 0.6 and avg_return > 0:
            verdict = "More steady"
        elif win_rate >= 0.5:
            verdict = "Mixed"
        else:
            verdict = "Less steady"
        row = {
            "holding_window": window,
            "win_rate": f"{win_rate:.0%}",
            "average_return": f"{avg_return:.2f}%",
            "verdict": verdict,
        }
        if analyst_mode:
            row["count"] = count
        else:
            row["sample_note"] = f"Based on ~{count} historical trades"
        rows.append(row)
    return pd.DataFrame(rows)


def _extract_unique_ticker_count(df: pd.DataFrame) -> int:
    """Count unique tickers/instruments from a dataframe."""
    if df.empty:
        return 0
    for candidate in ("instrument", "ticker"):
        if candidate in df.columns:
            tickers = df[candidate].dropna().astype(str).str.strip()
            tickers = tickers[tickers != ""]
            return int(tickers.nunique())
    return 0


def _extract_ticker_preview(df: pd.DataFrame, *, limit: int = 20) -> list[str]:
    """Return a small preview of distinct tickers/instruments."""
    if df.empty:
        return []
    for candidate in ("instrument", "ticker"):
        if candidate in df.columns:
            tickers = df[candidate].dropna().astype(str).str.strip()
            tickers = tickers[tickers != ""]
            return tickers.drop_duplicates().head(limit).tolist()
    return []


def _run_demo_with_active_dataset(
    *,
    canonical_df: pd.DataFrame,
    meta: dict,
    issues: dict,
) -> dict:
    """Run demo pipeline while preferring the active app dataset when supported."""
    run_demo_signature = inspect.signature(run_demo)
    supports_context_injection = all(
        param_name in run_demo_signature.parameters
        for param_name in ("canonical_df", "meta", "issues")
    )
    if supports_context_injection:
        return run_demo(canonical_df=canonical_df, meta=meta, issues=issues)
    return run_demo()


def _render_visual_polish(st_module) -> None:
    st_module.markdown(
        """
        <style>
        :root { --jse-accent: #7ea6ff; --jse-panel: #141b2a; --jse-border: #263248; --jse-muted: #aeb8cd; }
        .jse-card {
            background: linear-gradient(180deg, rgba(20, 27, 42, 0.92), rgba(17, 23, 36, 0.92));
            border: 1px solid var(--jse-border);
            border-radius: 14px;
            padding: 1rem 1.1rem;
            margin: 0.35rem 0 0.8rem 0;
        }
        .jse-eyebrow { color: var(--jse-accent); font-size: 0.82rem; letter-spacing: 0.03em; text-transform: uppercase; margin-bottom: 0.35rem; }
        .jse-muted { color: var(--jse-muted); }
        .jse-metric-grid { display: grid; grid-template-columns: repeat(4, minmax(90px, 1fr)); gap: 0.6rem; margin-top: 0.5rem; }
        .jse-metric { border: 1px solid var(--jse-border); border-radius: 10px; padding: 0.55rem 0.65rem; background: rgba(24, 32, 49, 0.75); }
        .jse-metric-label { color: var(--jse-muted); font-size: 0.74rem; }
        .jse-metric-value { color: #eaf0ff; font-size: 1rem; font-weight: 600; }
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-weight: 600; }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { border-bottom-color: var(--jse-accent) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


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
    _render_visual_polish(st)

    st.title("JSE Market Lab")
    mode = st.radio("Mode", options=["Beginner", "Analyst"], horizontal=True, index=0)
    mode_token = mode.lower()

    canonical_df, meta, issues = ingest_dataset("demo")
    dataset_source_label = str(meta.get("dataset_source_label") or "unknown_dataset")
    st.caption(f"Data source: {dataset_source_label}")
    st.caption("Using historical data from the Jamaican stock market.")

    if dataset_source_label == "legacy_demo_dataset":
        st.warning("Internal JSE dataset not found. Using fallback dataset.")

    if canonical_df.empty:
        st.warning("No rows were loaded from the data layer. Please verify the internal sample data file.")
        return

    demo_payload = _run_demo_with_active_dataset(
        canonical_df=canonical_df,
        meta=meta,
        issues=issues,
    )
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

    tabs = st.tabs(_resolve_tabs_for_mode(mode_token))
    tab_map = {name: tab for name, tab in zip(_resolve_tabs_for_mode(mode_token), tabs)}

    with tab_map["Portfolio"]:
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

    with tab_map["Review"]:
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

    with tab_map["Ticker Analysis"]:
        st.markdown("### Ticker Analysis")
        ticker_options = _extract_ticker_options(canonical_df)
        if not ticker_options:
            st.info("Ticker Analysis is unavailable because no ticker rows are loaded.")
        else:
            selected_ticker = st.selectbox("Select ticker", ticker_options)
            ticker_payload = build_ticker_drilldown(analyst_df, selected_ticker)
            ticker_metrics = compute_ticker_metrics(analyst_df, selected_ticker, mode=mode_token)
            analyst_mode = mode_token == "analyst"
            metrics_stats = ticker_metrics.get("stats", {})
            metrics_behavior = ticker_metrics.get("behavior", {})

            st.markdown("#### A) Quick Take")
            st.caption("A fast read of what this stock has looked like so far.")
            for line in _build_quick_take(
                stats=metrics_stats, holding_window_stats=ticker_payload["holding_window_stats"]
            ):
                st.markdown(f"- {line}")

            st.markdown("#### B) Best Holding Strategy")
            st.caption("This compares how the stock has behaved across holding periods and highlights the strongest window.")
            holding_window_df = _build_holding_window_table(
                ticker_payload["holding_window_stats"], analyst_mode=analyst_mode
            )
            if holding_window_df.empty:
                st.info("No holding window data is ready for this ticker yet.")
            else:
                best_window = str(metrics_stats.get("best_window") or "N/A")
                st.markdown(f"**Best holding period:** {best_window}")
                st.markdown(f"{metrics_behavior.get('holding_window', 'Holding-window comparison is limited right now.')}")
                st.dataframe(holding_window_df, use_container_width=True, hide_index=True)

            st.markdown("#### C) Risk Profile")
            st.caption("This explains how steady or uneven the returns have been.")
            for key in ("reliability", "consistency"):
                st.markdown(f"- {metrics_behavior.get(key, '')}")
            distribution = ticker_payload["return_distribution"]
            st.markdown(
                f"- Losses: {distribution.get('negative', 0)} | Smaller wins: {distribution.get('small_positive', 0)} | Strong wins: {distribution.get('strong_positive', 0)}."
            )
            if distribution.get("strong_positive", 0) > 0 and distribution.get("strong_positive", 0) <= distribution.get(
                "small_positive", 0
            ):
                st.markdown("- The average can be lifted by a smaller number of bigger wins.")

            st.markdown("#### D) What Usually Happens")
            st.caption("This section translates recurring behavior seen in the historical sample.")
            st.markdown(f"- {ticker_payload['pattern_summary']}")
            st.markdown(f"- {metrics_behavior.get('holding_window', '')}")
            st.markdown(f"- {metrics_behavior.get('tier_profile', '')}")

            st.markdown("#### E) What to Watch")
            st.caption("These points flag caution areas that can make results look better or worse than expected.")
            if "20D looks stronger" in metrics_behavior.get("holding_window", ""):
                st.markdown("- Short-term setups have looked weaker than longer holds in this sample.")
            st.markdown("- Results can look mixed when win rate and average return move in different directions.")
            st.markdown("- A smaller number of bigger moves can shape the average return.")

            if analyst_mode:
                st.markdown("#### F) Analyst Deep Dive")
                st.caption("These tables provide the full raw breakdown for deeper inspection.")

                st.markdown("This table shows full holding-window stats including raw sample count.")
                raw_holding_df = pd.DataFrame.from_dict(ticker_payload["holding_window_stats"], orient="index")
                st.dataframe(raw_holding_df.reset_index().rename(columns={"index": "holding_window"}), use_container_width=True)

                st.markdown("This table shows how each quality tier has performed for this ticker.")
                tier_df = pd.DataFrame.from_dict(ticker_payload["tier_performance"], orient="index")
                if tier_df.empty:
                    st.info("No tier breakdown is ready for this ticker yet.")
                else:
                    st.dataframe(tier_df.reset_index().rename(columns={"index": "quality_tier"}), use_container_width=True)

                st.markdown("This table shows whether results changed across volatility buckets.")
                volatility_df = pd.DataFrame.from_dict(ticker_payload["volatility_performance"], orient="index")
                if volatility_df.empty:
                    st.info("No volatility breakdown is ready for this ticker yet.")
                else:
                    st.dataframe(
                        volatility_df.reset_index().rename(columns={"index": "volatility_bucket"}),
                        use_container_width=True,
                    )

                st.markdown("This table shows the return distribution split between losses and stronger wins.")
                distribution_df = pd.DataFrame([ticker_payload["return_distribution"]])
                st.dataframe(distribution_df, use_container_width=True)

                st.markdown("This table lists the raw signal history for analyst review.")
                signal_df = pd.DataFrame(ticker_payload["signals"])
                if signal_df.empty:
                    st.info("No signal history is available for this ticker yet.")
                else:
                    st.dataframe(signal_df, use_container_width=True)
            else:
                st.markdown("**Analyst Deep Dive** is available in Analyst mode for full raw tables.")

    if "Analyst Insights" in tab_map:
        with tab_map["Analyst Insights"]:
            st.markdown("### Analyst Insights")
            if _has_analyst_insight_content(analyst_df, analyst_mode=mode_token == "analyst"):
                render_analyst_insights(analyst_df, st_module=st, analyst_mode=True)
            else:
                st.info("Analyst insights are not available for this dataset yet.")

    if "Data" in tab_map:
        with tab_map["Data"]:
            st.markdown("### Data")
            _render_data_status_summary(
                st,
                source=meta.get("source"),
                row_count=int(len(canonical_df)),
                issues=issues,
                dataset_id=meta.get("dataset_id"),
                analyst_mode=mode_token == "analyst",
            )
            st.caption("Dataset diagnostics (temporary)")
            diagnostics_df = pd.DataFrame(
                [
                    {"stage": "canonical", "rows": int(len(canonical_df)), "unique_tickers": _extract_unique_ticker_count(canonical_df)},
                    {"stage": "ranked", "rows": int(len(ranked_df)), "unique_tickers": _extract_unique_ticker_count(ranked_df)},
                ]
            )
            st.dataframe(diagnostics_df, use_container_width=True, hide_index=True)
            st.code(
                (
                    f"canonical first 20 tickers: {_extract_ticker_preview(canonical_df)}\n"
                    f"ranked first 20 tickers: {_extract_ticker_preview(ranked_df)}"
                ),
                language="text",
            )
            st.markdown("#### Main Dashboard")
            st.dataframe(canonical_df.head(50), use_container_width=True)


def _render_first_run_header(st_module, *, mode: str) -> None:
    mode_label = "Analyst" if str(mode).lower() == "analyst" else "Beginner"
    st_module.markdown(
        (
            '<div class="jse-card">'
            '<div class="jse-eyebrow">First-Run Orientation</div>'
            "<h3 style='margin:0 0 0.45rem 0;'>JSE Market Lab</h3>"
            "<p style='margin:0 0 0.35rem 0;'>This dashboard helps you review stock opportunities on the Jamaican market using structured rules and risk checks.</p>"
            "<p class='jse-muted' style='margin:0;'>It highlights stronger setups, explains key risks, and keeps your review flow focused for "
            f"{mode_label} mode.</p>"
            "</div>"
        ),
        unsafe_allow_html=True,
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
