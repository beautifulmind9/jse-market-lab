"""Streamlit application shell for the JSE Decision Support Dashboard."""

from __future__ import annotations

import inspect

import pandas as pd

from app.analysis.ticker_drilldown import build_ticker_drilldown
from app.analysis.ticker_intelligence import compute_ticker_metrics
from app.data.ingest import ingest_dataset
from app.data.processor import canonicalize_symbol
from app.demo.run_demo import run_demo
from app.insights.analyst import render_analyst_insights
from app.planner.allocation import generate_portfolio_allocation
from app.planner.portfolio_ui import render_portfolio_plan
from app.shell import build_analyst_dataset, coerce_trade_rows_from_ranked
from app.ui.display_labels import clean_dataframe_labels

_GUIDED_TABS = ["Portfolio", "Review", "Ticker Analysis", "Data"]
_ADVANCED_TABS = ["Portfolio", "Review", "Ticker Analysis", "Analyst Insights", "Data"]

_MODE_OPTIONS = {
    "Guided View": "beginner",
    "Advanced View": "analyst",
}

_START_HERE_EMBED_HTML = """<div style=\"position: relative; padding-bottom: 62.7177700348432%; height: 0;\"><iframe src=\"https://www.loom.com/embed/7429a995143a4bf498b640b5371309bc\" frameborder=\"0\" webkitallowfullscreen mozallowfullscreen allowfullscreen style=\"position: absolute; top: 0; left: 0; width: 100%; height: 100%;\"></iframe></div>"""
_HELP_VIDEO_URLS = {
    "portfolio": "https://www.loom.com/share/3b02f12dc1704595a2a717a0253b901b",
    "read_trade": "https://www.loom.com/share/58636a4aef5e4592a605efa8bb5c20d2",
    "ticker_analysis": "https://www.loom.com/share/c963e49ea0874277a5973ffec9d8a8f0",
    "review": "https://www.loom.com/share/6e2058d50c5d447b98d9031b4e1050cf",
    "analyst_mode": "https://www.loom.com/share/399c4760e90744c49fd4aadcf172f4a3",
}


def _has_analyst_insight_content(trades_df: pd.DataFrame, *, analyst_mode: bool) -> bool:
    if not analyst_mode or trades_df.empty:
        return False
    return any(column in trades_df.columns for column in ("net_return_pct", "net_return", "return_pct", "return"))


def _resolve_tabs_for_mode(mode: str) -> list[str]:
    return _ADVANCED_TABS if str(mode).lower() == "analyst" else _GUIDED_TABS


def _extract_ticker_options(df: pd.DataFrame) -> list[str]:
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
                float(item[1].get("median_return", 0.0)),
                float(item[1].get("win_rate", 0.0)),
                float(item[1].get("avg_return", 0.0)),
            ),
            reverse=True,
        )
        best_label = sorted_windows[0][0]
        hold_line = f"{best_label} has looked better than shorter alternatives in this sample."
    else:
        hold_line = "Holding-window comparison will sharpen as more 5D and 20D observations are added."

    return [
        f"This stock currently reads as {strength} from the signal sample.",
        f"It closed positive about {win_rate:.0%} of the time.",
        f"Typical outcome centers around median return near {median_return:.2%}; {consistency}.",
        hold_line,
    ]


def _build_holding_window_table(holding_window_stats: dict[str, dict], *, analyst_mode: bool) -> pd.DataFrame:
    if not holding_window_stats:
        return pd.DataFrame()
    rows: list[dict] = []
    for window, values in holding_window_stats.items():
        win_rate = float(values.get("win_rate", 0.0))
        median_return = float(values.get("median_return", 0.0))
        avg_return = float(values.get("avg_return", 0.0))
        count = int(values.get("count", 0))
        verdict = "More steady" if win_rate >= 0.6 and median_return > 0 else "Mixed" if win_rate >= 0.5 else "Less steady"
        row = {
            "holding_window": window,
            "win_rate": f"{win_rate:.0%}",
            "median_return": f"{median_return:.2f}%",
            "average_return": f"{avg_return:.2f}%",
            "verdict": verdict,
        }
        if analyst_mode:
            row["count"] = count
        else:
            row["sample_note"] = f"Built from about {count} completed trades"
        rows.append(row)
    return pd.DataFrame(rows)


def _build_execution_behavior_lines(*, execution_summary: dict, behavior: dict, stats: dict, analyst_mode: bool) -> list[str]:
    lines = [
        f"Entry framing: {execution_summary.get('entry_reference', '')}",
        f"Exit framing: {execution_summary.get('planned_exit', '')}",
        f"Typical outcome (median first): {execution_summary.get('typical_outcome', '')}",
        f"Execution caveats: {execution_summary.get('execution_risk', '')}",
    ]
    if analyst_mode:
        median_return = float(stats.get("median_return", 0.0))
        avg_return = float(stats.get("avg_return", 0.0))
        lines.append(
            "Outcome context: "
            + behavior.get("consistency", "")
            + f" (Median: {median_return:.2%}, Average: {avg_return:.2%})."
        )
    return lines


def _extract_unique_ticker_count(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    for candidate in ("instrument", "ticker"):
        if candidate in df.columns:
            tickers = df[candidate].dropna().astype(str).str.strip()
            tickers = tickers[tickers != ""]
            return int(tickers.nunique())
    return 0


def _extract_ticker_preview(df: pd.DataFrame, *, limit: int = 20) -> list[str]:
    if df.empty:
        return []
    for candidate in ("instrument", "ticker"):
        if candidate in df.columns:
            tickers = df[candidate].dropna().astype(str).str.strip()
            tickers = tickers[tickers != ""]
            return tickers.drop_duplicates().head(limit).tolist()
    return []


def _run_demo_with_active_dataset(*, canonical_df: pd.DataFrame, meta: dict, issues: dict) -> dict:
    run_demo_signature = inspect.signature(run_demo)
    supports_context_injection = all(
        param_name in run_demo_signature.parameters
        for param_name in ("canonical_df", "meta", "issues")
    )
    if supports_context_injection:
        return run_demo(canonical_df=canonical_df, meta=meta, issues=issues)
    return run_demo()


def _freeze_issues(issues: dict | None) -> tuple[tuple[str, tuple[str, ...]], ...]:
    safe_issues = issues or {}
    return tuple(sorted((str(key), tuple(str(item) for item in value)) for key, value in safe_issues.items()))


def _unfreeze_issues(frozen_issues: tuple[tuple[str, tuple[str, ...]], ...]) -> dict[str, list[str]]:
    return {key: list(values) for key, values in frozen_issues}


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
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p { font-weight: 600; }
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] { border-bottom-color: var(--jse-accent) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_video_link(st_module, *, label: str, url: str) -> None:
    st_module.markdown(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{label}</a>', unsafe_allow_html=True)


def _render_start_here_video(st_module) -> None:
    st_module.markdown("### New here? Start with this video")
    st_module.caption("This quick walkthrough shows how to use the dashboard and where to start.")
    st_module.components.v1.html(_START_HERE_EMBED_HTML, height=460)


def _render_onboarding(st_module) -> None:
    st_module.caption(
        "Decision-support for JSE trades, using price action, volume participation, volatility, liquidity, and realized outcomes from the JSE sample (since 2018 where available)."
    )
    _render_start_here_video(st_module)

    st_module.markdown("### Where to start")
    portfolio_col, ticker_col, review_col = st_module.columns(3)
    with portfolio_col:
        st_module.info("**Portfolio**\n\nSee strongest setups and how capital is being handled.")
    with ticker_col:
        st_module.info("**Ticker Analysis**\n\nUnderstand one stock through price, volume, volatility, liquidity, and outcome patterns.")
    with review_col:
        st_module.info("**Review**\n\nCheck whether the plan followed its rules.")

    with st_module.expander("What this dashboard does"):
        st_module.markdown("- Highlights stronger and weaker setups.")
        st_module.markdown("- Helps compare trades more clearly.")
        st_module.markdown("- Shows how long setups typically take to play out.")
        st_module.markdown("- Helps frame risk, not just returns.")

    with st_module.expander("How this dashboard supports decisions"):
        st_module.markdown("- Structures trade review with consistent rules.")
        st_module.markdown("- Keeps portfolio discipline visible before and after selection.")
        st_module.markdown("- Helps compare opportunities with a shared, repeatable framework.")

    with st_module.expander("What the system looks at"):
        st_module.markdown("- Price behavior.")
        st_module.markdown("- Volume / participation.")
        st_module.markdown("- Volatility / risk.")
        st_module.markdown("- Liquidity.")
        st_module.markdown("- Historical outcomes like win rate and median return.")


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
    c1, c2, c3 = st_module.columns(3)
    c1.metric("Rows loaded", row_count)
    c2.metric("Warnings", len(warnings))
    c3.metric("Errors", len(errors))
    st_module.caption(f"Source: {source or 'Unknown'}")

    if analyst_mode:
        st_module.caption(f"Dataset ID: {dataset_id or 'N/A'}")

    if warnings:
        st_module.warning("Warnings were reported during ingestion.")
        with st_module.expander("Warning details"):
            for warning in warnings:
                st_module.markdown(f"- {warning}")
    if errors:
        st_module.warning("Errors were reported during ingestion.")
        with st_module.expander("Error details"):
            for error in errors:
                st_module.markdown(f"- {error}")


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="JSE Decision Support Dashboard", page_icon="📈", layout="wide")
    _render_visual_polish(st)

    st.title("JSE Market Lab")
    mode_label = st.radio("View", options=list(_MODE_OPTIONS.keys()), horizontal=True, index=0)
    mode_token = _MODE_OPTIONS[mode_label]
    st.caption("Guided View: simpler explanations and lighter detail")
    st.caption("Advanced View: deeper breakdowns and fuller analysis")

    @st.cache_data(show_spinner=False)
    def _cached_ingest_dataset() -> tuple[pd.DataFrame, dict, tuple[tuple[str, tuple[str, ...]], ...]]:
        canonical_df_value, meta_value, issues_value = ingest_dataset("demo")
        return canonical_df_value, meta_value, _freeze_issues(issues_value)

    @st.cache_data(show_spinner=False)
    def _cached_run_demo_payload(
        canonical_df_value: pd.DataFrame,
        meta_value: dict,
        frozen_issues: tuple[tuple[str, tuple[str, ...]], ...],
    ) -> pd.DataFrame:
        payload = _run_demo_with_active_dataset(
            canonical_df=canonical_df_value,
            meta=meta_value,
            issues=_unfreeze_issues(frozen_issues),
        )
        return payload.get("ranked", pd.DataFrame())

    @st.cache_data(show_spinner=False)
    def _cached_build_analyst_dataset(canonical_df_value: pd.DataFrame, ranked_df_value: pd.DataFrame) -> pd.DataFrame:
        return build_analyst_dataset(canonical_df_value, ranked_df_value)

    @st.cache_data(show_spinner=False)
    def _cached_extract_ticker_options(canonical_df_value: pd.DataFrame) -> list[str]:
        return _extract_ticker_options(canonical_df_value)

    @st.cache_data(show_spinner=False)
    def _cached_ticker_payloads(analyst_df_value: pd.DataFrame, ticker: str, mode_value: str) -> tuple[dict, dict]:
        payload = build_ticker_drilldown(analyst_df_value, ticker)
        metrics = compute_ticker_metrics(analyst_df_value, ticker, mode=mode_value)
        return payload, metrics

    canonical_df, meta, frozen_issues = _cached_ingest_dataset()
    issues = _unfreeze_issues(frozen_issues)
    dataset_source_label = str(meta.get("dataset_source_label") or "unknown_dataset")

    if dataset_source_label == "legacy_demo_dataset":
        st.warning("Internal JSE dataset not found. Using fallback dataset.")

    if canonical_df.empty:
        st.warning("No rows were loaded from the data layer. Please verify the internal sample data file.")
        return

    ranked_df = _cached_run_demo_payload(canonical_df, meta, frozen_issues)
    analyst_df = _cached_build_analyst_dataset(canonical_df, ranked_df)
    trade_rows = coerce_trade_rows_from_ranked(ranked_df) if not ranked_df.empty else []

    default_capital = 100_000.0
    selected_capital = float(st.session_state.get("total_capital", default_capital))

    if ranked_df.empty:
        enriched_allocations: list[dict] = []
    else:
        allocation_payload = generate_portfolio_allocation(trade_rows, selected_capital)
        base_allocations = allocation_payload.get("allocations", [])
        enriched_allocations = [{**allocation, **row} for row, allocation in zip(trade_rows, base_allocations)]

    _render_onboarding(st)

    tabs = st.tabs(_resolve_tabs_for_mode(mode_token))
    tab_map = {name: tab for name, tab in zip(_resolve_tabs_for_mode(mode_token), tabs)}

    with tab_map["Portfolio"]:
        st.markdown("### Portfolio")
        _render_video_link(st, label="▶ Watch: Understanding the Portfolio", url=_HELP_VIDEO_URLS["portfolio"])
        _render_video_link(st, label="▶ Watch: How to Read a Trade", url=_HELP_VIDEO_URLS["read_trade"])
        selected_capital = st.number_input("Total capital", min_value=0.0, value=selected_capital, step=5_000.0, key="total_capital")
        if ranked_df.empty:
            st.info("Portfolio Plan will appear after ranked outputs are generated for the current run.")
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
        _render_video_link(st, label="▶ Watch: Understanding Review", url=_HELP_VIDEO_URLS["review"])
        if ranked_df.empty:
            st.info("Review will populate once ranked outputs are generated for this run.")
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
        _render_video_link(st, label="▶ Watch: Understanding Ticker Analysis", url=_HELP_VIDEO_URLS["ticker_analysis"])
        ticker_options = _cached_extract_ticker_options(canonical_df)
        if not ticker_options:
            st.info("Ticker Analysis will populate once ticker rows are loaded into the dataset.")
        else:
            selected_ticker = st.selectbox("Select ticker", ticker_options)
            ticker_payload, ticker_metrics = _cached_ticker_payloads(analyst_df, selected_ticker, mode_token)
            analyst_mode = mode_token == "analyst"
            metrics_stats = ticker_metrics.get("stats", {})
            metrics_behavior = ticker_metrics.get("behavior", {})

            st.markdown("#### Quick Take")
            for line in _build_quick_take(stats=metrics_stats, holding_window_stats=ticker_payload["holding_window_stats"]):
                st.markdown(f"- {line}")

            st.markdown("#### Best Holding Strategy")
            holding_window_df = _build_holding_window_table(ticker_payload["holding_window_stats"], analyst_mode=analyst_mode)
            if holding_window_df.empty:
                st.info("No holding window data is ready for this ticker yet.")
            else:
                st.metric("Best holding period", str(metrics_stats.get("best_window") or "N/A"))
                st.info(metrics_behavior.get("holding_window", "Holding-window comparison is limited right now."))
                st.dataframe(clean_dataframe_labels(holding_window_df), use_container_width=True, hide_index=True)

            st.markdown("#### Risk Profile")
            st.warning(metrics_behavior.get("reliability", ""))
            st.info(metrics_behavior.get("consistency", ""))

            st.markdown("#### What Usually Happens")
            st.markdown(f"- {ticker_payload['pattern_summary']}")
            st.markdown(f"- {metrics_behavior.get('tier_profile', '')}")

            st.markdown("#### What to Watch")
            st.markdown("- Results can look mixed when win rate and average return move in different directions.")
            st.markdown("- Median return stays primary; average return adds context.")

            st.markdown("#### Execution Behavior")
            for line in _build_execution_behavior_lines(
                execution_summary=ticker_metrics.get("execution", {}),
                behavior=metrics_behavior,
                stats=metrics_stats,
                analyst_mode=analyst_mode,
            ):
                st.markdown(f"- {line}")

            if analyst_mode:
                with st.expander("Advanced breakdown", expanded=False):
                    st.markdown("##### Holding window details")
                    raw_holding_df = pd.DataFrame.from_dict(ticker_payload["holding_window_stats"], orient="index")
                    st.dataframe(
                        clean_dataframe_labels(raw_holding_df.reset_index().rename(columns={"index": "holding_window"})),
                        use_container_width=True,
                    )

                    st.markdown("##### Tier breakdown")
                    tier_df = pd.DataFrame.from_dict(ticker_payload["tier_performance"], orient="index")
                    st.dataframe(
                        clean_dataframe_labels(tier_df.reset_index().rename(columns={"index": "quality_tier"})),
                        use_container_width=True,
                    )

                    st.markdown("##### Volatility breakdown")
                    volatility_df = pd.DataFrame.from_dict(ticker_payload["volatility_performance"], orient="index")
                    st.dataframe(
                        clean_dataframe_labels(volatility_df.reset_index().rename(columns={"index": "volatility_bucket"})),
                        use_container_width=True,
                    )

                    st.markdown("##### Return distribution")
                    st.dataframe(clean_dataframe_labels(pd.DataFrame([ticker_payload["return_distribution"]])), use_container_width=True)

                    st.markdown("##### Signal history")
                    signal_df = pd.DataFrame(ticker_payload["signals"])
                    if signal_df.empty:
                        st.info("No signal history is available for this ticker yet.")
                    else:
                        st.dataframe(clean_dataframe_labels(signal_df), use_container_width=True)
            else:
                st.caption("Switch to Advanced View to open the full table breakdown.")

    if "Analyst Insights" in tab_map:
        with tab_map["Analyst Insights"]:
            st.markdown("### Analyst Insights")
            _render_video_link(st, label="▶ Watch: How to Use Analyst Mode", url=_HELP_VIDEO_URLS["analyst_mode"])
            if _has_analyst_insight_content(analyst_df, analyst_mode=True):
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
            if mode_token == "analyst":
                diagnostics_df = pd.DataFrame(
                    [
                        {"stage": "canonical", "rows": int(len(canonical_df)), "unique_tickers": _extract_unique_ticker_count(canonical_df)},
                        {"stage": "ranked", "rows": int(len(ranked_df)), "unique_tickers": _extract_unique_ticker_count(ranked_df)},
                    ]
                )
                st.dataframe(clean_dataframe_labels(diagnostics_df), use_container_width=True, hide_index=True)
                st.code(
                    (
                        f"canonical first 20 tickers: {_extract_ticker_preview(canonical_df)}\n"
                        f"ranked first 20 tickers: {_extract_ticker_preview(ranked_df)}"
                    ),
                    language="text",
                )
                with st.expander("Data preview"):
                    st.dataframe(clean_dataframe_labels(canonical_df.head(100)), use_container_width=True)
            else:
                with st.expander("Preview loaded rows"):
                    st.dataframe(clean_dataframe_labels(canonical_df.head(25)), use_container_width=True)


if __name__ == "__main__":
    main()
