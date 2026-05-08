"""Configuration helpers for the JSE Market Lab API."""

from __future__ import annotations

import os

SERVICE_NAME = "jse-market-lab-api"
DEFAULT_DATASET = "demo"
DEFAULT_MODE = "guided"
DISCLAIMER = "This is decision support, not financial advice."

MODE_MAP = {
    "guided": "beginner",
    "beginner": "beginner",
    "advanced": "analyst",
    "analyst": "analyst",
}


def normalize_mode(mode: str | None) -> str:
    """Return the internal mode token used by existing engine helpers."""
    if mode is None:
        return MODE_MAP[DEFAULT_MODE]
    return MODE_MAP.get(str(mode).strip().lower(), MODE_MAP[DEFAULT_MODE])


def public_mode(mode: str | None) -> str:
    """Return the API-facing mode label."""
    internal = normalize_mode(mode)
    return "advanced" if internal == "analyst" else "guided"


def get_cors_origins() -> list[str]:
    """Return allowed frontend origins from the API environment."""
    raw_origins = os.getenv("BACKEND_CORS_ORIGINS", "")
    origins = [origin.strip().rstrip("/") for origin in raw_origins.split(",") if origin.strip()]

    if origins:
        return origins

    return [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
