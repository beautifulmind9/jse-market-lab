"""Save synthetic demo prices to disk."""

from __future__ import annotations

from pathlib import Path

from .generate_prices import generate_demo_prices


def save_demo_prices() -> Path:
    """Generate and save demo prices CSV."""
    df = generate_demo_prices()
    output_path = Path(__file__).resolve().parents[2] / "data" / "demo" / "prices_demo.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    """CLI entrypoint for saving demo prices."""
    path = save_demo_prices()
    print(f"Saved demo prices to {path}")


if __name__ == "__main__":
    main()
