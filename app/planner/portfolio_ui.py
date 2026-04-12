"""Streamlit helpers for rendering a user-facing portfolio plan."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

import pandas as pd

from app.language.formatter import generate_explanation
from app.planner.decision_review import (
    build_behavior_summary,
    compute_discipline_score,
    compute_trade_review,
    detect_decision_mistakes,
)
from app.planner.explanations import (
    REASON_KEYS,
    classify_decision_status,
    explain_funded_trade_why,
    explain_unfunded_trade_why,
)


_ALLOCATOR_REASON_KEYS = REASON_KEYS


def build_portfolio_summary(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
) -> dict[str, Any]:
    """Build top-line portfolio summary values from allocation rows."""
    safe_capital = float(total_capital or 0.0)
    total_allocated_amount = round(
        sum(float(trade.get("allocation_amount", 0.0) or 0.0) for trade in allocations),
        2,
    )
    total_allocated_pct = (
        round(total_allocated_amount / safe_capital, 4) if safe_capital > 0 else 0.0
    )
    cash_reserve_amount = round(safe_capital - total_allocated_amount, 2)
    cash_reserve_pct = (
        round(cash_reserve_amount / safe_capital, 4) if safe_capital > 0 else 0.0
    )
    funded_trade_count = sum(
        1 for trade in allocations if float(trade.get("allocation_amount", 0.0) or 0.0) > 0
    )

    return {
        "total_allocated_amount": total_allocated_amount,
        "total_allocated_pct": total_allocated_pct,
        "cash_reserve_amount": cash_reserve_amount,
        "cash_reserve_pct": cash_reserve_pct,
        "funded_trade_count": funded_trade_count,
    }


def split_trades_by_funding(
    allocations: Sequence[Mapping[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Split allocations into funded and unfunded trades."""
    funded_trades: list[dict[str, Any]] = []
    unfunded_trades: list[dict[str, Any]] = []

    for trade in allocations:
        row = dict(trade)
        amount = float(row.get("allocation_amount", 0.0) or 0.0)
        if amount > 0:
            funded_trades.append(row)
        else:
            unfunded_trades.append(row)

    return funded_trades, unfunded_trades


def generate_funding_reason(trade: Mapping[str, Any]) -> str:
    """Generate a compact funding explanation using explicit reasons first."""
    return explain_funded_trade_why(trade)


def resolve_unfunded_reason(trade: Mapping[str, Any]) -> str:
    """Resolve unfunded reason in the shared one-sentence voice."""
    return explain_unfunded_trade_why(trade)


def render_portfolio_plan(
    allocations: Sequence[Mapping[str, Any]],
    total_capital: float,
    st_module=None,
    *,
    signals_df: pd.DataFrame | None = None,
    show_review_table: bool = True,
    mode: str = "beginner",
    section: str = "both",
    show_header: bool = True,
) -> None:
    """Render portfolio summary/review details in one section or both."""
    if st_module is None:
        import streamlit as st_module

    normalized_section = str(section or "both").strip().lower()
    if normalized_section not in {"plan", "review", "both"}:
        normalized_section = "both"

    if show_header:
        st_module.subheader("Portfolio Plan")
    analyst_mode = str(mode or "beginner").lower() == "analyst"
    if show_header and normalized_section in {"plan", "both"}:
        st_module.caption(
            "The plan funds the strongest eligible setups first, while other trades stay out when rules or limits block them."
        )

    if not allocations:
        st_module.info("Portfolio Plan unavailable: no allocation outputs were provided.")
        return

    summary = build_portfolio_summary(allocations, total_capital)
    funded_trades, unfunded_trades = split_trades_by_funding(allocations)

    def _render_plan_section() -> None:
        st_module.markdown(
            '<div class="jse-card"><div class="jse-eyebrow">Portfolio Summary</div><p style="margin:0;" class="jse-muted">Funding view of current eligible setups and reserve coverage.</p></div>',
            unsafe_allow_html=True,
        )
        summary_df = pd.DataFrame(
            [
                {
                    "Total Capital": float(total_capital or 0.0),
                    "Allocated Amount": summary["total_allocated_amount"],
                    **({"Allocated %": summary["total_allocated_pct"]} if analyst_mode else {}),
                    "Cash Reserve Amount": summary["cash_reserve_amount"],
                    **({"Cash Reserve %": summary["cash_reserve_pct"]} if analyst_mode else {}),
                    "Funded Trades": summary["funded_trade_count"],
                }
            ]
        )
        st_module.dataframe(summary_df, use_container_width=True)

        st_module.markdown("#### Funded Trades")
        if funded_trades:
            funded_df = pd.DataFrame(
                [
                    {
                        "Instrument": trade.get("instrument", "Unknown"),
                        "Setup Strength": trade.get("quality_tier", "N/A"),
                        "Confidence": trade.get("confidence_label", "N/A"),
                        **({"Allocation %": trade.get("allocation_pct", 0.0)} if analyst_mode else {}),
                        "Allocation Amount": trade.get("allocation_amount", 0.0),
                        **({"Selection Rank": trade.get("selection_rank", "N/A")} if analyst_mode else {}),
                        "Decision Status": classify_decision_status(trade),
                        "Why": generate_explanation(trade, mode=mode),
                        **({"Rule Note": explain_funded_trade_why(trade)} if analyst_mode else {}),
                    }
                    for trade in funded_trades
                ]
            )
            st_module.dataframe(funded_df, use_container_width=True)
        else:
            st_module.info("No funded trades for the selected inputs.")

        st_module.markdown("#### Unfunded Trades")
        if unfunded_trades:
            unfunded_df = pd.DataFrame(
                [
                    {
                        "Instrument": trade.get("instrument", "Unknown"),
                        "Setup Strength": trade.get("quality_tier", "N/A"),
                        "Confidence": trade.get("confidence_label", "N/A"),
                        **({"Selection Rank": trade.get("selection_rank", "N/A")} if analyst_mode else {}),
                        "Decision Status": classify_decision_status(trade),
                        "Why": resolve_unfunded_reason(trade),
                    }
                    for trade in unfunded_trades
                ]
            )
            st_module.dataframe(unfunded_df, use_container_width=True)
        else:
            st_module.info("No unfunded trades for the selected inputs.")

        st_module.markdown("#### Portfolio Rules")
        st_module.markdown(
            "- Max portfolio exposure: 70%\n"
            "- Min cash reserve: 30%\n"
            "- Max funded trades: 3\n"
            "- Tier C and liquidity failures are not funded"
        )

    def _render_review_section() -> None:
        st_module.markdown(
            '<div class="jse-card"><div class="jse-eyebrow">Review Summary</div><p style="margin:0;">This section shows how closely selected trades followed system rules and where risk discipline changed.</p></div>',
            unsafe_allow_html=True,
        )
        trades_df = pd.DataFrame(list(allocations))
        safe_signals_df = signals_df if signals_df is not None else pd.DataFrame()
        review_df = compute_trade_review(trades_df, safe_signals_df)
        mistake_list = detect_decision_mistakes(
            trades_df,
            safe_signals_df,
            trades_df,
        )
        discipline_score = compute_discipline_score(review_df)

        st_module.write({"Discipline Score": discipline_score})

        behavior_summary = build_behavior_summary(trades_df, review_df)
        st_module.markdown("**Behavior Summary**")
        for item in behavior_summary:
            st_module.markdown(f"- {item}")

        st_module.markdown("**What this means**")
        for paragraph in _build_review_interpretation_paragraphs(review_df, mode=mode):
            st_module.markdown(paragraph)

        st_module.markdown("**What to improve**")
        for bullet in _build_behavior_improvement_points(review_df, mode=mode):
            st_module.markdown(f"- {bullet}")

        st_module.markdown("**Mistakes Detected**")
        grouped_mistakes = _group_mistakes_for_display(mistake_list, mode=mode)
        if grouped_mistakes:
            for line in grouped_mistakes:
                st_module.markdown(f"- {line}")
        else:
            st_module.markdown("- No clear decision mistakes were detected.")

        if show_review_table:
            st_module.markdown("**Trade Review Table**")
            if review_df.empty:
                st_module.info("No review rows available for this run.")
            else:
                st_module.dataframe(review_df, use_container_width=True)

    if normalized_section == "plan":
        _render_plan_section()
        return
    if normalized_section == "review":
        _render_review_section()
        return

    plan_tab, review_tab = st_module.tabs(["Plan", "Review"])
    with plan_tab:
        _render_plan_section()
    with review_tab:
        _render_review_section()


def _build_review_interpretation_paragraphs(review_df: pd.DataFrame, *, mode: str = "beginner") -> list[str]:
    if review_df is None or review_df.empty:
        return ["There is not enough decision activity yet to read a clear behavior pattern."]

    total = max(int(len(review_df)), 1)
    followed = int(review_df["followed_rules"].fillna(False).astype(bool).sum())
    rank_misses = int((review_df["deviation_type"] == "rank_deviation").sum())
    quality_fails = int((review_df["quality_flag"] == "fail").sum())
    liquidity_fails = int((review_df["liquidity_flag"] == "fail").sum())

    if str(mode).lower() == "analyst":
        return [
            f"Rule alignment came in at {followed}/{total} ({followed / total:.0%}), based on the current review set.",
            f"Deviation mix: rank {rank_misses}, quality {quality_fails}, liquidity {liquidity_fails}.",
        ]
    return [
        f"{followed} of {total} reviewed trades followed the full process rules.",
        "Where rules were missed, the gaps came from rank order, quality checks, or liquidity checks.",
    ]


def _build_behavior_improvement_points(review_df: pd.DataFrame, *, mode: str = "beginner") -> list[str]:
    if review_df is None or review_df.empty:
        return ["Keep logging decisions so this section can track repeat behavior over time."]

    rank_misses = int((review_df["deviation_type"] == "rank_deviation").sum())
    quality_fails = int((review_df["quality_flag"] == "fail").sum())
    liquidity_fails = int((review_df["liquidity_flag"] == "fail").sum())

    if str(mode).lower() == "analyst":
        bullets = [
            "Keep selection order aligned with the highest-ranked eligible setups.",
            "Keep quality filtering steady so weaker setups appear less often.",
            "Apply liquidity checks before entries are finalized.",
        ]
    else:
        bullets = [
            "Keep the strongest eligible setups at the top of selection order.",
            "Keep quality checks steady so weaker setups stay out.",
            "Run liquidity checks before final funding.",
        ]

    if rank_misses == 0:
        bullets[0] = "Ranking discipline was stable; maintain this ordering consistency."
    if quality_fails == 0:
        bullets[1] = "Quality discipline was stable; maintain current quality filtering consistency."
    if liquidity_fails == 0:
        bullets[2] = "Liquidity screening was stable; maintain current execution-quality checks."

    return bullets


def _group_mistakes_for_display(mistakes: Sequence[Mapping[str, Any]], *, mode: str = "beginner") -> list[str]:
    grouped: dict[str, dict[str, Any]] = {}
    for item in mistakes:
        mistake_type = str(item.get("type", "rule_violation"))
        if mistake_type not in grouped:
            grouped[mistake_type] = {"count": 0}
        grouped[mistake_type]["count"] += 1

    lines: list[str] = []
    for mistake_type, payload in grouped.items():
        count = int(payload["count"])
        lines.append(_render_grouped_mistake_line(mistake_type, count, mode=mode))
    return lines


def _render_grouped_mistake_line(mistake_type: str, count: int, *, mode: str = "beginner") -> str:
    templates = {
        "low_quality_trade": "{count} trade(s) missed the setup-quality rule.",
        "ignored_higher_rank": "{count} trade(s) were picked while a stronger-ranked setup was available.",
        "liquidity_violation": "{count} trade(s) failed the liquidity check.",
        "over_allocation": "{count} trade(s) went above the allocation cap.",
        "cooldown_violation": "{count} trade(s) were funded while cooldown was active.",
    }
    if str(mode).lower() == "analyst":
        templates["low_quality_trade"] = "{count} trade(s) did not meet the quality tier rule."
    template = templates.get(mistake_type, "{count} trade(s) showed a decision rule deviation.")
    return template.format(count=count)


def _first_sentence(text: str) -> str:
    cleaned = str(text or "").strip()
    if not cleaned:
        return ""

    sentence = cleaned.split(".")[0].strip()
    if not sentence:
        return ""
    return f"{sentence}."
