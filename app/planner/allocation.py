"""Deterministic portfolio allocation layer for planner trade rows."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from app.planner.confidence import generate_trade_confidence

_BASE_ALLOCATION_BY_CONFIDENCE = {
    "strong": 0.30,
    "moderate": 0.20,
    "high risk": 0.10,
    "watch": 0.00,
    "avoid": 0.00,
}

_CONFIDENCE_PRIORITY = {
    "strong": 0,
    "moderate": 1,
    "high risk": 2,
    "watch": 3,
    "avoid": 4,
}

_QUALITY_PRIORITY = {"A": 0, "B": 1, "C": 2}
_VOLATILITY_PRIORITY = {"low": 0, "medium": 1, "high": 2}
_SEVERITY_PRIORITY = {"info": 0, "caution": 1, "high": 2}


MAX_FUNDED_TRADES = 3
MAX_TOTAL_EXPOSURE = 0.70
MIN_CASH_RESERVE = 0.30


def generate_portfolio_allocation(
    trade_rows: Sequence[Mapping[str, Any]],
    total_capital: float,
) -> dict:
    """Generate an explainable allocation plan for planner trade rows."""
    rows_with_scoring: list[dict[str, Any]] = []
    for idx, row in enumerate(trade_rows):
        confidence_label = _resolve_confidence_label(row)
        base_pct = _BASE_ALLOCATION_BY_CONFIDENCE.get(confidence_label, 0.0)

        hard_stop_reason = _hard_stop_reason(row)
        reduction, reduction_reasons = _risk_reduction(row)
        preconstraint_pct = max(0.0, base_pct - reduction)
        if hard_stop_reason is not None:
            preconstraint_pct = 0.0

        rows_with_scoring.append(
            {
                "idx": idx,
                "row": row,
                "confidence_label": confidence_label,
                "base_pct": base_pct,
                "preconstraint_pct": preconstraint_pct,
                "hard_stop_reason": hard_stop_reason,
                "reduction_reasons": reduction_reasons,
                "sort_key": _sort_key(row, confidence_label, idx),
            }
        )

    ordered_rows = sorted(rows_with_scoring, key=lambda item: item["sort_key"])

    remaining_exposure = MAX_TOTAL_EXPOSURE
    funded_count = 0
    allocations_by_idx: dict[int, dict[str, Any]] = {}

    for item in ordered_rows:
        row = item["row"]
        instrument = _display_text(row.get("instrument"), fallback="Unknown")
        preconstraint_pct = item["preconstraint_pct"]

        allocation_pct = 0.0
        constraint_reason = None

        if preconstraint_pct <= 0.0:
            constraint_reason = "pre-constraints reduced allocation to zero"
        elif funded_count >= MAX_FUNDED_TRADES:
            constraint_reason = f"max funded trades reached ({MAX_FUNDED_TRADES})"
        elif remaining_exposure <= 0.0:
            constraint_reason = (
                f"max portfolio exposure reached ({MAX_TOTAL_EXPOSURE:.0%})"
            )
        else:
            allocation_pct = min(preconstraint_pct, remaining_exposure)
            if allocation_pct > 0:
                funded_count += 1
                remaining_exposure -= allocation_pct

        allocations_by_idx[item["idx"]] = {
            "instrument": instrument,
            "confidence_label": item["confidence_label"],
            "allocation_pct": round(allocation_pct, 4),
            "allocation_amount": round(allocation_pct * float(total_capital), 2),
            "allocation_reason_clear": _build_reason_clear(
                item,
                allocation_pct,
                constraint_reason,
            ),
            "allocation_reason_pro": _build_reason_pro(
                item,
                allocation_pct,
                constraint_reason,
            ),
        }

    allocations = [allocations_by_idx[i] for i in range(len(rows_with_scoring))]
    total_allocated_pct = round(sum(a["allocation_pct"] for a in allocations), 4)
    total_allocated_amount = round(total_allocated_pct * float(total_capital), 2)
    cash_reserve_pct = round(max(0.0, 1.0 - total_allocated_pct), 4)
    cash_reserve_amount = round(cash_reserve_pct * float(total_capital), 2)

    return {
        "allocations": allocations,
        "total_allocated_pct": total_allocated_pct,
        "total_allocated_amount": total_allocated_amount,
        "cash_reserve_pct": cash_reserve_pct,
        "cash_reserve_amount": cash_reserve_amount,
    }


def _resolve_confidence_label(trade_row: Mapping[str, Any]) -> str:
    for key in ("confidence_label", "confidence_level"):
        value = _normalize_text(trade_row.get(key))
        if value:
            return value

    confidence_payload = generate_trade_confidence(_confidence_input(trade_row))
    return _normalize_text(confidence_payload.get("confidence_label"), fallback="watch")


def _confidence_input(trade_row: Mapping[str, Any]) -> dict[str, Any]:
    payload = dict(trade_row)
    if payload.get("severity") is None and payload.get("earnings_warning_severity") is not None:
        payload["severity"] = payload.get("earnings_warning_severity")
    return payload


def _hard_stop_reason(trade_row: Mapping[str, Any]) -> str | None:
    quality_tier = _normalize_text(trade_row.get("quality_tier")).upper()
    if quality_tier == "C":
        return "quality tier C is not funded"
    if trade_row.get("liquidity_pass") is False:
        return "liquidity screen failed"
    return None


def _risk_reduction(trade_row: Mapping[str, Any]) -> tuple[float, list[str]]:
    reduction = 0.0
    reasons: list[str] = []

    severity = _normalize_text(trade_row.get("earnings_warning_severity"))
    if severity == "high":
        reduction += 0.10
        reasons.append("high earnings warning severity (-10%)")
    elif severity == "caution":
        reduction += 0.05
        reasons.append("caution earnings warning severity (-5%)")

    volatility_bucket = _normalize_text(trade_row.get("volatility_bucket"))
    if volatility_bucket == "high":
        reduction += 0.05
        reasons.append("high volatility bucket (-5%)")

    return reduction, reasons


def _sort_key(trade_row: Mapping[str, Any], confidence_label: str, idx: int) -> tuple:
    quality_tier = _normalize_text(trade_row.get("quality_tier")).upper()
    volatility_bucket = _normalize_text(trade_row.get("volatility_bucket"))
    severity = _normalize_text(trade_row.get("earnings_warning_severity"))

    return (
        _CONFIDENCE_PRIORITY.get(confidence_label, 99),
        _QUALITY_PRIORITY.get(quality_tier, 99),
        _VOLATILITY_PRIORITY.get(volatility_bucket, 99),
        _SEVERITY_PRIORITY.get(severity, 99),
        idx,
    )


def _build_reason_clear(
    item: Mapping[str, Any],
    allocation_pct: float,
    constraint_reason: str | None,
) -> str:
    base_text = f"{item['confidence_label'].title()} confidence starts at {item['base_pct']:.0%}."
    parts = [base_text]

    if item["hard_stop_reason"]:
        parts.append(f"Hard rule applied: {item['hard_stop_reason']}.")
    elif item["reduction_reasons"]:
        parts.append("Risk reductions: " + "; ".join(item["reduction_reasons"]) + ".")

    if constraint_reason and allocation_pct <= 0:
        parts.append(f"Final allocation is 0% because {constraint_reason}.")
    elif constraint_reason:
        parts.append(
            f"Portfolio constraint applied, capping final allocation at {allocation_pct:.0%}."
        )
    else:
        parts.append(f"Final allocation is {allocation_pct:.0%}.")

    return " ".join(parts)


def _build_reason_pro(
    item: Mapping[str, Any],
    allocation_pct: float,
    constraint_reason: str | None,
) -> str:
    reasons = []
    if item["hard_stop_reason"]:
        reasons.append(f"hard_stop={item['hard_stop_reason']}")
    if item["reduction_reasons"]:
        reasons.append("risk_adjustments=" + ", ".join(item["reduction_reasons"]))
    if constraint_reason:
        reasons.append(f"constraint={constraint_reason}")

    reason_suffix = "; ".join(reasons) if reasons else "no adjustments"
    return (
        f"base={item['base_pct']:.2f}; final={allocation_pct:.2f}; "
        f"{reason_suffix}."
    )


def _normalize_text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value).strip().lower()


def _display_text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    return str(value).strip()
