"""Backward-compatible loader exports."""

from .loaders import load_internal_dataset, load_upload


def load_demo():
    """Backward-compatible alias for loading the internal dataset."""
    dataset, _source_label = load_internal_dataset()
    return dataset
