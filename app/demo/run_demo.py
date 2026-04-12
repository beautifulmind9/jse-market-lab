"""Run the end-to-end demo pipeline."""

from __future__ import annotations

import json
import logging
import errno
from pathlib import Path

import pandas as pd

from app.costs.engine import run_cost_engine
from app.data.ingest import ingest_dataset
from app.demo.language import get_explanatory_copy
from app.events.earnings import tag_earnings_phase
from app.events.phase_metrics import compute_phase_metrics
from app.ranking.engine import rank_instruments


logger = logging.getLogger(__name__)


def _load_demo_events(events_path: Path) -> pd.DataFrame:
    """Load optional legacy demo earnings events, returning an empty-safe frame when absent."""
    if events_path.exists():
        return pd.read_csv(events_path)
    return pd.DataFrame(columns=["instrument", "earnings_date", "confidence"])


def run_demo(
    language_mode: str = "plain",
    *,
    canonical_df: pd.DataFrame | None = None,
    meta: dict | None = None,
    issues: dict | None = None,
) -> dict:
    """Run ingestion, cost, ranking, and phase metrics for demo data."""
    if canonical_df is None or meta is None or issues is None:
        canonical, meta, issues = ingest_dataset("demo")
    else:
        canonical = canonical_df

    entries = canonical[["instrument", "date"]].rename(columns={"date": "entry_date"})

    trades, summary_instrument, _, _ = run_cost_engine(
        df_prices=canonical,
        df_entries=entries,
    )
    ranked = rank_instruments(summary_instrument, meta, "income_stability")

    events_path = Path(__file__).resolve().parents[2] / "data" / "demo" / "earnings_events.csv"
    events_df = _load_demo_events(events_path)

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
    try:
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        ranked.to_csv(artifacts_dir / "ranked.csv", index=False)
        phase_metrics.to_csv(artifacts_dir / "phase_metrics.csv", index=False)
        meta_payload = {"meta": meta, "issues": issues}
        (artifacts_dir / "meta.json").write_text(json.dumps(meta_payload, indent=2))
    except PermissionError as exc:
        # Continue when running in restricted environments where local writes are unavailable.
        logger.warning("Demo artifacts not written due to restricted filesystem permissions: %s", exc)
    except OSError as exc:
        if exc.errno == errno.EROFS:
            logger.warning("Demo artifacts not written due to read-only filesystem: %s", exc)
        else:
            raise

    return {
        "ranked": ranked,
        "phase_metrics": phase_metrics,
        "meta": meta,
        "issues": issues,
        "language_mode": language_mode,
        "explanatory_copy": get_explanatory_copy(language_mode),
    }


def main() -> None:
    """CLI entrypoint for the demo pipeline."""
    run_demo()
    print("Demo pipeline complete. Outputs saved to artifacts/demo.")


if __name__ == "__main__":
    main()
