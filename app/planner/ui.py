"""Streamlit UI helpers for Weekly Trade Planner rendering."""

from __future__ import annotations

from typing import Any, Callable, Mapping, Optional, Sequence

import numpy as np
import pandas as pd

from app.insights.analyst import render_analyst_insights
from app.planner.confidence import generate_trade_confidence
from app.planner.guidance import generate_trade_guidance

SEVERITY_LEVELS = {"info", "caution", "high"}


def _normalize_warning_severity(raw_severity: Optional[str]) -> str:
    """Normalize warning severity for planner UI rendering."""
    if raw_severity is None or pd.isna(raw_severity):
        return "info"

    severity = (
        raw_severity.strip().lower()
        if isinstance(raw_severity, str)
        else str(raw_severity).strip().lower()
    )
    if severity not in SEVERITY_LEVELS:
        return "info"
    return severity


def _overlap_is_explicit_true(overlap_value: Any) -> bool:
    """Return True only for explicit boolean true values."""
    return isinstance(overlap_value, (bool, np.bool_)) and bool(overlap_value)


def render_earnings_warning_block(
    trade_row: Mapping[str, Any],
    *,
    st_module=None,
    use_expander: bool = True,
) -> bool:
    """Render earnings warning directly under the trade header.

    Returns True when a warning was rendered.
    """
    if not _overlap_is_explicit_true(trade_row.get("earnings_overlaps_window")):
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
    guidance_mode: Optional[str] = None,
) -> None:
    """Render one planner trade card in scan-first order.

    Order: header -> earnings warning block -> confidence block -> guidance block -> trade math details.
    """
    if st_module is None:
        import streamlit as st_module

    instrument = trade_row.get("instrument", "Unknown")
    entry_date = trade_row.get("entry_date", "")
    holding_window = trade_row.get("holding_window", "")
    st_module.markdown(
        f"### {instrument} | Entry: {entry_date} | Window: {holding_window}D"
    )

    selected_guidance_mode = _resolve_guidance_mode(guidance_mode)

    render_earnings_warning_block(
        trade_row,
        st_module=st_module,
        use_expander=use_expander,
    )
    _render_confidence_block(
        trade_row,
        st_module=st_module,
        use_expander=use_expander,
        guidance_mode=selected_guidance_mode,
    )
    _render_guidance_block(
        trade_row,
        st_module=st_module,
        use_expander=use_expander,
        guidance_mode=selected_guidance_mode,
    )
    render_trade_math(trade_row)


def resolve_guidance_mode_for_planner(
    *,
    st_module=None,
    guidance_mode: Optional[str] = None,
    toggle_key: str = "guidance_mode_toggle",
) -> str:
    """Resolve guidance mode once for a planner/page-level view."""
    if guidance_mode in {"clear", "pro"}:
        return guidance_mode

    if st_module is None:
        import streamlit as st_module

    is_simple = st_module.toggle(
        "Simple explanation",
        value=True,
        key=toggle_key,
    )
    return "clear" if is_simple else "pro"


def render_trade_cards(
    trade_rows: Sequence[Mapping[str, Any]],
    render_trade_math: Callable[[Mapping[str, Any]], None],
    *,
    st_module=None,
    use_expander: bool = True,
    guidance_mode: Optional[str] = None,
    toggle_key: str = "guidance_mode_toggle",
) -> str:
    """Render planner trade cards using one shared guidance mode."""
    if st_module is None:
        import streamlit as st_module

    selected_guidance_mode = resolve_guidance_mode_for_planner(
        st_module=st_module,
        guidance_mode=guidance_mode,
        toggle_key=toggle_key,
    )

    for trade_row in trade_rows:
        render_trade_card(
            trade_row,
            render_trade_math,
            st_module=st_module,
            use_expander=use_expander,
            guidance_mode=selected_guidance_mode,
        )
    return selected_guidance_mode


def _resolve_guidance_mode(guidance_mode: Optional[str]) -> str:
    """Resolve whether guidance should render in clear or pro mode."""
    if guidance_mode in {"clear", "pro"}:
        return guidance_mode
    return "clear"


def _render_confidence_block(
    trade_row: Mapping[str, Any],
    *,
    st_module=None,
    use_expander: bool = True,
    guidance_mode: str = "clear",
) -> bool:
    """Render confidence classification block below warnings."""
    confidence = generate_trade_confidence(trade_row)
    confidence_title = confidence["confidence_title"]
    confidence_body = (
        confidence["confidence_body_pro"]
        if guidance_mode == "pro"
        else confidence["confidence_body_clear"]
    )
    confidence_level = confidence["confidence_level"]
    summary = f"**{confidence_title}** · `{confidence_level}`"

    if confidence_level in {"avoid", "high risk"}:
        st_module.error(summary)
    elif confidence_level == "watch":
        st_module.warning(summary)
    else:
        st_module.info(summary)

    if use_expander:
        with st_module.expander("Confidence", expanded=False):
            st_module.write(confidence_body)
    else:
        st_module.write(confidence_body)
    return True


def _render_guidance_block(
    trade_row: Mapping[str, Any],
    *,
    st_module=None,
    use_expander: bool = True,
    guidance_mode: str = "clear",
) -> bool:
    """Render guidance interpretation block below earnings warnings."""
    guidance = generate_trade_guidance(trade_row)
    if guidance is None:
        return False

    guidance_title = guidance["guidance_title"]
    guidance_body = (
        guidance["guidance_body_pro"]
        if guidance_mode == "pro"
        else guidance["guidance_body_clear"]
    )
    guidance_type = guidance["guidance_type"]
    summary = f"**{guidance_title}** · `{guidance_type}`"

    if guidance_type == "high":
        st_module.error(summary)
    elif guidance_type == "caution":
        st_module.warning(summary)
    else:
        st_module.info(summary)

    if use_expander:
        with st_module.expander("Guidance", expanded=False):
            st_module.write(guidance_body)
    else:
        st_module.write(guidance_body)
    return True


def render_analyst_insights_section(
    trades_df: pd.DataFrame,
    *,
    st_module=None,
    analyst_mode: bool = True,
) -> None:
    """Render analyst insights in analyst mode without mutating engine outputs."""
    render_analyst_insights(
        trades_df,
        st_module=st_module,
        analyst_mode=analyst_mode,
    )
