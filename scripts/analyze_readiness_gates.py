from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from app.analysis.readiness_gates import compute_readiness_metrics, evaluate_models, write_research_artifacts
from app.data.loaders import load_internal_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze readiness-gate research models.")
    parser.add_argument("--output-dir", default="artifacts/research", help="Output directory for research artifacts")
    args = parser.parse_args()

    data = load_internal_dataset()
    metrics = compute_readiness_metrics(data)
    model_summary, model_ticker = evaluate_models(metrics)
    write_research_artifacts(metrics, model_summary, model_ticker, Path(args.output_dir))

    print(f"Wrote readiness research artifacts to {args.output_dir}")


if __name__ == "__main__":
    main()
