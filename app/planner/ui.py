"""Streamlit UI helpers for Weekly Trade Planner rendering."""

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional

SEVERITY_LEVELS = {"info", "caution", "high"}


def _normalize_warning_severity(raw_severity: Optional[str]) -> str:
    """Normalize warning severity for planner UI rendering."""
    severity = (raw_severity or "").strip().lower()
    if severity not in SEVERITY_LEVELS:
        return "info"
    return severity


def render_earnings_warning_block(
    trade_row: Mapping[str, Any],
    *,
    st_module=None,
    use_expander: bool = True,
) -> bool:
    """Render earnings warning directly under the trade header.

    Returns True when a warning was rendered.
    """
    if not bool(trade_row.get("earnings_overlaps_window")):
        return False

    if st_module is None:
        import streamlit as st_module

    severity = _normalize_warning_severity(trade_row.get("earnings_warning_severity"))
    title = trade_row.get("earnings_warning_title") or "Earnings window warning"
    body = trade_row.get("earnings_warning_body") or ""
    summary = f"**{title}** · `{severity}`"

    if severity == "high":
        st_module.error(summary)
    elif severity == "caution":
        st_module.warning(summary)
    else:
        st_module.info(summary)

    if body:
        if use_expander:
            with st_module.expander("Details", expanded=False):
                st_module.write(body)
        else:
            st_module.write(body)
    return True


def render_trade_card(
    trade_row: Mapping[str, Any],
    render_trade_math: Callable[[Mapping[str, Any]], None],
    *,
    st_module=None,
    use_expander: bool = True,
) -> None:
    """Render one planner trade card in scan-first order.

    Order: header -> earnings warning block -> trade math details.
    """
    if st_module is None:
        import streamlit as st_module

    instrument = trade_row.get("instrument", "Unknown")
    entry_date = trade_row.get("entry_date", "")
    holding_window = trade_row.get("holding_window", "")
    st_module.markdown(
        f"### {instrument} | Entry: {entry_date} | Window: {holding_window}D"
    )

    render_earnings_warning_block(
        trade_row,
        st_module=st_module,
        use_expander=use_expander,
    )
    render_trade_math(trade_row)
