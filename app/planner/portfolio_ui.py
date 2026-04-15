"""Streamlit helpers for rendering a user-facing portfolio plan."""

from __future__ import annotations

import re
from typing import Any, Mapping, Sequence

import pandas as pd

from app.language.formatter import explain_confidence, explain_strength
from app.insights.portfolio_snapshot import (
    build_portfolio_snapshot,
    build_reserved_cash_explanation,
)
from app.insights.execution import build_execution_summary
from app.insights.trade_explainer import explain_trade_reason, explain_unfunded_reason
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
)


_ALLOCATOR_REASON_KEYS = REASON_KEYS
_SENTENCE_BOUNDARY_PATTERN = re.compile(r"([.!?])\s+")
_KNOWN_ABBREVIATIONS = {
    "e.g.",
    "i.e.",
    "mr.",
    "mrs.",
    "ms.",
    "dr.",
    "prof.",
}
_INITIALISM_PATTERN = re.compile(r"(?:[A-Z]\.){2,}$")
_HOLDING_WINDOW_PATTERN = re.compile(
    r"^\s*([+-]?\d+)\s*(?:trading\s+days?|days?|d)?\s*$",
    re.IGNORECASE,
)
_BEGINNER_UNFUNDED_ROW_LIMIT = 12


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
    return explain_trade_reason(trade)


def resolve_unfunded_reason(trade: Mapping[str, Any]) -> str:
    """Resolve unfunded reason in the shared one-sentence voice."""
    return explain_unfunded_reason(trade)


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
    analyst_max_funded_trades_override: int | None = None,
) -> None:
    """Render portfolio summary/review details in one section or both."""
    if st_module is None:
        import streamlit as st_module

    normalized_section = str(section or "both").strip().lower()
    if normalized_section not in {"plan", "review", "both"}:
        normalized_section = "both"

    if show_header:
        st_module.subheader("Portfolio")
    analyst_mode = str(mode or "beginner").lower() == "analyst"
    if show_header and normalized_section in {"plan", "both"}:
        st_module.caption("The plan funds stronger eligible setups first and keeps reserve discipline in view.")

    if not allocations:
        st_module.info("Portfolio Plan will populate once allocation outputs are available.")
        return

    summary = build_portfolio_summary(allocations, total_capital)
    funded_trades, unfunded_trades = split_trades_by_funding(allocations)

    def _portfolio_plan_row(trade: Mapping[str, Any], *, funded: bool) -> dict[str, Any]:
        holding_days = _extract_holding_days(trade.get("holding_window"))
        execution_row = dict(trade)
        execution_row["holding_window"] = holding_days
        execution = build_execution_summary(execution_row, mode=mode)
        row: dict[str, Any] = {
            "Ticker": trade.get("instrument", "Unknown"),
            "Setup Strength": explain_strength(trade.get("quality_tier"), mode=mode),
            "Confidence / Reliability": explain_confidence(trade.get("confidence_label"), mode=mode),
            "Holding Window": _format_holding_window_label(holding_days),
            "Why this trade": (
                explain_trade_reason(trade, mode=mode) if funded else resolve_unfunded_reason(trade)
            ),
            "Execution Summary": _compact_execution_summary(execution, mode=mode),
        }

        if analyst_mode:
            row.update(
                {
                    "Decision Status": classify_decision_status(trade),
                    "Allocation %": trade.get("allocation_pct", 0.0),
                    "Allocation Amount": trade.get("allocation_amount", 0.0),
                    "Selection Rank": trade.get("selection_rank", "N/A"),
                    "Rule Note": explain_funded_trade_why(trade) if funded else "Not funded this cycle.",
                }
            )
        return row

    def _render_snapshot_blocks() -> None:
        snapshot = build_portfolio_snapshot(allocations, total_capital, mode=mode)
        st_module.markdown("#### Portfolio Snapshot")
        metric_cols = st_module.columns(4)
        metric_cols[0].metric("Trades Found", len(allocations))
        metric_cols[1].metric("Funded Trades", summary["funded_trade_count"])
        metric_cols[2].metric("Allocated %", f"{summary['total_allocated_pct']:.0%}")
        metric_cols[3].metric("Cash Reserved %", f"{summary['cash_reserve_pct']:.0%}")
        interpretation = (
            "Funding remained concentrated in stronger ranked setups while preserving cash for selectivity."
            if analyst_mode
            else "This plan funds the stronger setups first while preserving a cash buffer for discipline."
        )
        st_module.caption(interpretation)

        with st_module.expander("How to read setup strength and confidence"):
            for line in snapshot["lines"]:
                st_module.markdown(f"- {line}")

        reserved_cash = build_reserved_cash_explanation(allocations, total_capital, mode=mode)
        if reserved_cash["reserve_ratio"] > 0:
            with st_module.expander("Why cash is reserved", expanded=False):
                st_module.caption(
                    reserved_cash["lines"][0] if reserved_cash["lines"] else "Cash reserve supports discipline."
                )
                if analyst_mode and len(reserved_cash["lines"]) > 1:
                    for line in reserved_cash["lines"][1:]:
                        st_module.markdown(f"- {line}")

    def _render_trade_cards(trades: Sequence[Mapping[str, Any]], *, funded: bool) -> None:
        for trade in trades:
            plan_row = _portfolio_plan_row(trade, funded=funded)
            st_module.markdown(f"#### {plan_row['Ticker']}")
            st_module.markdown(f"**Setup Strength:** {plan_row['Setup Strength']}")
            st_module.markdown(f"**Confidence / Reliability:** {plan_row['Confidence / Reliability']}")
            st_module.markdown(f"**Holding Window:** {plan_row['Holding Window']}")
            st_module.markdown(f"**Why this trade:** {plan_row['Why this trade']}")
            st_module.markdown(
                f"**Execution Summary:** {plan_row['Execution Summary'] if funded else 'Not funded in this cycle.'}"
            )
            st_module.markdown("---")


    def _render_plan_section() -> None:
        _render_snapshot_blocks()

        st_module.markdown("#### Funded Trades")
        if funded_trades:
            if analyst_mode:
                funded_df = pd.DataFrame([_portfolio_plan_row(trade, funded=True) for trade in funded_trades])
                st_module.dataframe(funded_df, use_container_width=True)
            else:
                _render_trade_cards(funded_trades, funded=True)
        else:
            st_module.info("No funded trades for the selected inputs.")

        st_module.markdown("#### Unfunded Trades")
        if unfunded_trades:
            visible_unfunded = unfunded_trades
            hidden_unfunded_count = 0
            if not analyst_mode and len(unfunded_trades) > _BEGINNER_UNFUNDED_ROW_LIMIT:
                visible_unfunded = sorted(
                    unfunded_trades,
                    key=lambda trade: float(trade.get("selection_rank", 10_000) or 10_000),
                )[:_BEGINNER_UNFUNDED_ROW_LIMIT]
                hidden_unfunded_count = len(unfunded_trades) - len(visible_unfunded)

            if analyst_mode:
                unfunded_df = pd.DataFrame([_portfolio_plan_row(trade, funded=False) for trade in visible_unfunded])
                st_module.dataframe(unfunded_df, use_container_width=True)
            else:
                _render_trade_cards(visible_unfunded, funded=False)
            if hidden_unfunded_count > 0:
                st_module.caption(
                    f"Showing top {_BEGINNER_UNFUNDED_ROW_LIMIT} unfunded trades for speed. "
                    f"Switch to Advanced View to view all {len(unfunded_trades)} rows."
                )
                with st_module.expander("See why more trades were not funded"):
                    st_module.markdown(
                        "Lower-ranked setups remain unfunded first when limits and reserve rules are active."
                    )
        else:
            st_module.info("No unfunded trades for the selected inputs.")

        st_module.markdown("#### Portfolio Rules")
        rules = [
            "- Max portfolio exposure: 70%",
            "- Min cash reserve: 30%",
            "- Funding approach: prioritize top-ranked, stronger setups and expand only when multiple strong opportunities are available.",
            "- Tier C and liquidity failures are not funded.",
        ]
        if analyst_mode and analyst_max_funded_trades_override is not None:
            rules.append(
                f"- Analyst cap override: up to {int(analyst_max_funded_trades_override)} funded trades (secondary control)."
            )
            rules.append(
                "- Caution: increasing this cap may include lower-ranked setups and reduce reserve discipline."
            )
        if analyst_mode:
            st_module.markdown("\n".join(rules))
        else:
            with st_module.expander("Portfolio rules and funding approach"):
                st_module.markdown("\n".join(rules))

    def _render_review_section() -> None:
        st_module.markdown("#### Review")
        st_module.info(
            "Review checks whether the plan followed its intended rules and where discipline mattered."
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

        st_module.metric("Discipline Score", discipline_score)

        behavior_summary = build_behavior_summary(trades_df, review_df)
        st_module.markdown("**Summary**")
        for item in behavior_summary[: (3 if not analyst_mode else len(behavior_summary))]:
            st_module.markdown(f"- {item}")
        if not analyst_mode and len(behavior_summary) > 3:
            with st_module.expander("More summary detail"):
                for item in behavior_summary[3:]:
                    st_module.markdown(f"- {item}")

        st_module.markdown("**Interpretation**")
        for paragraph in _build_review_interpretation_paragraphs(review_df, mode=mode):
            st_module.markdown(paragraph)

        st_module.markdown("**What to improve**")
        improvements = _build_behavior_improvement_points(review_df, mode=mode)
        for bullet in improvements[: (2 if not analyst_mode else len(improvements))]:
            st_module.markdown(f"- {bullet}")
        if not analyst_mode and len(improvements) > 2:
            with st_module.expander("More improvement points"):
                for bullet in improvements[2:]:
                    st_module.markdown(f"- {bullet}")

        st_module.markdown("**Mistakes Detected**")
        grouped_mistakes = _group_mistakes_for_display(mistake_list, mode=mode)
        if grouped_mistakes:
            for line in grouped_mistakes[: (2 if not analyst_mode else len(grouped_mistakes))]:
                st_module.markdown(f"- {line}")
            if not analyst_mode and len(grouped_mistakes) > 2:
                with st_module.expander("More detected mistakes"):
                    for line in grouped_mistakes[2:]:
                        st_module.markdown(f"- {line}")
        else:
            st_module.markdown("- No clear decision mistakes were detected.")

        if show_review_table:
            st_module.markdown("**Decision Audit**")
            if review_df.empty:
                st_module.info("No review rows available for this run.")
            else:
                st_module.dataframe(
                    _build_decision_audit_table(review_df),
                    use_container_width=True,
                )

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
        return ["Behavior read becomes sharper as more reviewed decisions accumulate."]

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

    for match in _SENTENCE_BOUNDARY_PATTERN.finditer(cleaned):
        punctuation = match.group(1)
        punctuation_idx = match.start(1)
        next_char_idx = match.end()
        prev_char = cleaned[punctuation_idx - 1] if punctuation_idx > 0 else ""
        next_char = cleaned[next_char_idx] if next_char_idx < len(cleaned) else ""

        if punctuation == "." and prev_char.isdigit() and next_char.isdigit():
            continue

        if punctuation == "." and _is_abbreviation_boundary(cleaned, punctuation_idx):
            continue

        return cleaned[: punctuation_idx + 1].strip()

    return cleaned


def _is_abbreviation_boundary(text: str, punctuation_idx: int) -> bool:
    fragment = text[: punctuation_idx + 1]
    token_match = re.search(r"(\S+)$", fragment)
    if token_match is None:
        return False

    token = token_match.group(1).strip()
    normalized_token = token.strip("\"'”’)]}").lstrip("\"'“‘([{")
    lowered = normalized_token.lower()
    if lowered in _KNOWN_ABBREVIATIONS:
        return True

    return bool(_INITIALISM_PATTERN.fullmatch(normalized_token))


def _format_holding_window_label(value: Any) -> str:
    window = _extract_holding_days(value)
    if window is None:
        return "Not specified"
    return f"{window} trading days"


def _extract_holding_days(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, float):
        if pd.isna(value) or not value.is_integer():
            return None
        integer_value = int(value)
        return integer_value if integer_value > 0 else None

    match = _HOLDING_WINDOW_PATTERN.fullmatch(str(value))
    if match is None:
        return None

    days = _int_or_none(match.group(1))
    if days is None or days <= 0:
        return None
    return days


def _build_decision_audit_table(review_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, str]] = []
    for _, row in review_df.iterrows():
        status, happened, matters = _translate_review_row(row)
        rows.append(
            {
                "Ticker": str(row.get("instrument", "Unknown")),
                "Status": status,
                "What happened": happened,
                "Why it matters": matters,
            }
        )
    return pd.DataFrame(rows)


def _translate_review_row(row: Mapping[str, Any]) -> tuple[str, str, str]:
    deviation_type = str(row.get("deviation_type", "")).strip().lower()
    quality_flag = str(row.get("quality_flag", "")).strip().lower()
    liquidity_flag = str(row.get("liquidity_flag", "")).strip().lower()
    followed_rules = bool(row.get("followed_rules", False))

    if deviation_type == "rank_deviation":
        selected_rank = _int_or_none(row.get("selected_rank"))
        best_available_rank = _int_or_none(row.get("best_available_rank"))
        if selected_rank is not None and best_available_rank is not None:
            happened = (
                f"A lower-ranked trade was selected (rank {selected_rank}) while rank "
                f"{best_available_rank} was available."
            )
        else:
            happened = "A lower-ranked trade was selected while a stronger rank was available."
        return (
            "Rank order deviation",
            happened,
            "This breaks rank discipline and can weaken expected portfolio quality.",
        )

    if quality_flag == "fail":
        return (
            "Blocked by quality rule",
            "The setup failed the minimum quality tier required for funding.",
            "Funding lower-quality setups can reduce signal reliability.",
        )

    if liquidity_flag == "fail":
        return (
            "Blocked by liquidity check",
            "The trade failed liquidity checks used to control slippage and execution risk.",
            "Poor liquidity can increase trading friction and downside risk.",
        )

    if followed_rules:
        return (
            "Rule-aligned",
            "The trade followed portfolio selection and risk rules.",
            "Consistent rule-following helps keep risk and selection quality stable.",
        )

    return (
        "Rule deviation",
        "The trade showed a portfolio rule deviation.",
        "Rule deviations can weaken consistency in portfolio outcomes.",
    )


def _compact_execution_summary(execution: Mapping[str, Any], *, mode: str = "beginner") -> str:
    entry_reference = _first_sentence(str(execution.get("entry_reference", "")).strip())
    entry_phrase = "Entry reference uses the signal-day close area"
    if entry_reference:
        entry_phrase = entry_reference.rstrip(".")

    planned_exit = str(execution.get("planned_exit", "")).strip()
    holding_days = _extract_planned_exit_days(planned_exit)
    if holding_days is None:
        holding_days = _extract_holding_days(execution.get("holding_window"))
    analyst_mode = str(mode or "beginner").strip().lower() == "analyst"

    if holding_days is None:
        exit_phrase = "planned exit timing is not specified"
    elif analyst_mode:
        exit_phrase = f"planned exit after {holding_days} trading days"
    else:
        exit_phrase = f"planned exit after {holding_days} trading days"

    return f"{entry_phrase}; {exit_phrase}."


def _extract_planned_exit_days(planned_exit: str) -> int | None:
    match = re.search(r"(\d+)\s+trading\s+days", str(planned_exit or ""), flags=re.IGNORECASE)
    if match is None:
        return None
    return _int_or_none(match.group(1))


def _int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
