"""Run the end-to-end demo pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from app.costs.engine import run_cost_engine
from app.data.ingest import ingest_dataset
from app.events.earnings import tag_earnings_phase
from app.metrics.phase_metrics import compute_phase_metrics
from app.ranking.engine import rank_instruments


def run_demo() -> dict:
    """Run ingestion, cost, ranking, and phase metrics for demo data."""
    canonical, meta, issues = ingest_dataset("demo")

    entries = canonical[["instrument", "date"]].rename(columns={"date": "entry_date"})

    trades, summary_instrument, _, _ = run_cost_engine(
        df_prices=canonical,
        df_entries=entries,
    )
    ranked = rank_instruments(summary_instrument, meta, "income_stability")

    events_path = Path(__file__).resolve().parents[2] / "data" / "demo" / "earnings_events.csv"
    events_df = pd.read_csv(events_path)

    tagged_trades = tag_earnings_phase(
        trades,
        events_df,
        date_col="entry_date",
        inst_col="instrument",
    )
    phase_metrics = compute_phase_metrics(
        tagged_trades,
        ["instrument", "earnings_phase"],
        "net_return_pct",
    )

    artifacts_dir = Path(__file__).resolve().parents[2] / "artifacts" / "demo"
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    ranked.to_csv(artifacts_dir / "ranked.csv", index=False)
    phase_metrics.to_csv(artifacts_dir / "phase_metrics.csv", index=False)
    meta_payload = {"meta": meta, "issues": issues}
    (artifacts_dir / "meta.json").write_text(json.dumps(meta_payload, indent=2))

    return {
        "ranked": ranked,
        "phase_metrics": phase_metrics,
        "meta": meta,
        "issues": issues,
    }


def main() -> None:
    """CLI entrypoint for the demo pipeline."""
    run_demo()
    print("Demo pipeline complete. Outputs saved to artifacts/demo.")


if __name__ == "__main__":
    main()
