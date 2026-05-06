"""Data status service for API responses."""

from __future__ import annotations

from typing import Any

import pandas as pd

from backend.app.services.engine_context import get_engine_context


def get_data_status() -> dict[str, Any]:
    """Return a safe data status summary for the active dataset."""
    context = get_engine_context()
    canonical_df = context["canonical_df"]
    meta = context["meta"]
    issues = context["issues"]

    latest_market_date = None
    if not canonical_df.empty and "date" in canonical_df.columns:
        date_values = pd.to_datetime(canonical_df["date"], errors="coerce").dropna()
        if not date_values.empty:
            latest_market_date = date_values.max().date().isoformat()

    warnings = [str(item) for item in issues.get("warnings", [])]
    errors = [str(item) for item in issues.get("errors", [])]
    row_count = int(len(canonical_df))

    return {
        "dataset_source": str(meta.get("dataset_source_label") or meta.get("source") or "demo"),
        "row_count": row_count,
        "latest_market_date": latest_market_date,
        "warnings": warnings,
        "errors": errors,
        "message": "Data loaded successfully." if row_count > 0 and not errors else "Data needs review.",
    }
