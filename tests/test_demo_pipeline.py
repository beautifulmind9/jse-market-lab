import errno
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.costs.engine import run_cost_engine
from app.data.metadata import build_metadata
from app.data.normalize import normalize_data
from app.data.validate import validate_canonical
from app.demo.generate_prices import generate_demo_prices
from app.events.earnings import tag_earnings_phase
from app.events.phase_metrics import compute_phase_metrics
from app.ranking.engine import rank_instruments
from app.demo import run_demo as run_demo_module


def test_demo_pipeline_outputs():
    demo_prices = generate_demo_prices()
    canonical, _ = normalize_data(demo_prices, source="demo", dataset_id="test")
    issues = validate_canonical(canonical)
    assert issues["errors"] == []

    entries = canonical[["instrument", "date"]].rename(columns={"date": "entry_date"})
    trades, summary_instrument, _, _ = run_cost_engine(
        df_prices=canonical,
        df_entries=entries,
    )

    meta = build_metadata(canonical, source="demo", dataset_id="test")
    ranked = rank_instruments(summary_instrument, meta, "income_stability")
    assert not ranked.empty
    assert {"tier", "best_window", "score_total"}.issubset(ranked.columns)

    events_path = ROOT / "data" / "demo" / "earnings_events.csv"
    events_df = pd.read_csv(events_path)
    tagged = tag_earnings_phase(
        trades,
        events_df,
        date_col="entry_date",
        inst_col="instrument",
    )
    phases = set(tagged["earnings_phase"].unique())
    assert phases.issubset({"pre", "reaction", "post", "non"})

    phase_metrics = compute_phase_metrics(
        tagged,
        ["instrument", "earnings_phase"],
        "net_return_pct",
    )
    assert {"insufficient_history", "n"}.issubset(phase_metrics.columns)


def test_run_demo_logs_warning_when_artifact_writes_are_permission_restricted(caplog, monkeypatch):
    def raise_permission_error(*args, **kwargs):
        raise PermissionError("read-only filesystem")

    monkeypatch.setattr(Path, "mkdir", raise_permission_error)

    with caplog.at_level("WARNING"):
        result = run_demo_module.run_demo()

    assert not result["ranked"].empty
    assert "restricted filesystem permissions" in caplog.text


def test_run_demo_logs_warning_when_artifact_writes_are_read_only_filesystem(caplog, monkeypatch):
    def raise_read_only_os_error(*args, **kwargs):
        raise OSError(errno.EROFS, "read-only filesystem")

    monkeypatch.setattr(Path, "mkdir", raise_read_only_os_error)

    with caplog.at_level("WARNING"):
        result = run_demo_module.run_demo()

    assert not result["ranked"].empty
    assert "read-only filesystem" in caplog.text


def test_run_demo_does_not_swallow_unexpected_os_errors(monkeypatch):
    def raise_unexpected_os_error(*args, **kwargs):
        raise OSError(errno.ENOSPC, "disk full")

    monkeypatch.setattr(Path, "mkdir", raise_unexpected_os_error)

    with pytest.raises(OSError, match="disk full"):
        run_demo_module.run_demo()
