"""Main ingestion entrypoint."""

from __future__ import annotations

from typing import IO, Optional, Tuple

import pandas as pd

from .loader import load_demo, load_upload
from .metadata import build_metadata, generate_dataset_id
from .normalize import normalize_data
from .validate import validate_canonical


def ingest_dataset(
    mode: str, uploaded_file: Optional[IO] = None
) -> Tuple[pd.DataFrame, dict, dict]:
    """Ingest a dataset and return canonical data, metadata, and issues."""
    if mode not in {"demo", "upload"}:
        raise ValueError("mode must be 'demo' or 'upload'.")

    if mode == "demo":
        raw = load_demo()
        source = "demo"
    else:
        raw = load_upload(uploaded_file)
        source = "upload"

    dataset_id = generate_dataset_id()
    canonical, _ = normalize_data(raw, source=source, dataset_id=dataset_id)
    issues = validate_canonical(canonical)
    meta = build_metadata(canonical, source=source, dataset_id=dataset_id)
    return canonical, meta, issues
