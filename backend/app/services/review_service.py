"""Decision-audit service for API responses."""

from __future__ import annotations

from typing import Any

from backend.app.core.config import DISCLAIMER, public_mode
from backend.app.services.portfolio_service import get_portfolio_plan


def _rule_lines(plan: dict[str, Any]) -> list[str]:
    return [
        "Quality tiers were reviewed before funding. Tier A and B setups are prioritised over Tier C.",
        "Liquidity status was checked so weaker execution conditions are not treated the same as cleaner setups.",
        "Capital was allocated using portfolio rules instead of forcing every available setup into the plan.",
        "Reserve cash remains when the system does not find enough fundable opportunities under the current rules.",
    ]


def get_decision_audit(capital: float, mode: str | None = None) -> dict[str, Any]:
    """Return a human-readable review of how the current plan was formed."""
    plan = get_portfolio_plan(capital, mode)
    funded = plan.get("funded_trades", [])
    unfunded = plan.get("unfunded_trades", [])
    reserve_cash = float(plan.get("reserve_cash") or 0.0)

    funded_rationale = [
        f"{trade.get('ticker', 'Unknown')} was funded because it received a positive allocation under the current quality, confidence, and portfolio rules."
        for trade in funded
    ]
    unfunded_rationale = [
        f"{trade.get('ticker', 'Unknown')} was not funded. Reason: {trade.get('reason', 'The setup did not receive allocation under the current rules.')}"
        for trade in unfunded
    ]

    return {
        "mode": public_mode(mode),
        "summary": [
            f"The plan funded {len(funded)} setup(s) and left {len(unfunded)} setup(s) unfunded.",
            f"Cash reserve is JMD {reserve_cash:,.2f} based on the current capital input and portfolio rules.",
            "This audit explains how the rules shaped the plan. It does not tell the user what to buy or sell.",
        ],
        "funded_rationale": funded_rationale,
        "unfunded_rationale": unfunded_rationale,
        "rules_applied": _rule_lines(plan),
        "cash_reserve_explanation": (
            "Cash was left unallocated because the system does not force lower-quality or constrained setups into the plan. "
            "This supports discipline and keeps user choice visible."
        ),
        "disclaimer": DISCLAIMER,
    }
