"""Synthetic demo price generation."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_demo_prices(
    universe_size: int = 10,
    total_trading_days: int = 60,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic daily prices for a demo universe."""
    size = int(universe_size)
    size = max(8, min(size, 12))
    total_days = max(int(total_trading_days), 1)

    rng = np.random.default_rng(seed)
    tickers = [f"DEMO{i + 1}" for i in range(size)]
    dates = pd.bdate_range("2024-01-02", periods=total_days)

    low_vol_count = max(1, size // 3)
    high_vol_count = max(1, size // 3)
    low_vol_tickers = set(tickers[:low_vol_count])
    high_vol_tickers = set(tickers[-high_vol_count:])
    low_volume_tickers = set(tickers[::4])

    records: list[dict] = []
    for ticker in tickers:
        base_price = rng.uniform(20, 150)
        if ticker in high_vol_tickers:
            daily_vol = 0.03
        elif ticker in low_vol_tickers:
            daily_vol = 0.008
        else:
            daily_vol = 0.015

        returns = rng.normal(0.0005, daily_vol, size=total_days)
        prices = base_price * np.exp(np.cumsum(returns))

        if ticker in low_volume_tickers:
            base_volume = rng.integers(2_000, 8_000)
            volume_noise = rng.normal(0, 500, size=total_days)
        else:
            base_volume = rng.integers(20_000, 80_000)
            volume_noise = rng.normal(0, 5_000, size=total_days)

        volumes = np.maximum(base_volume + volume_noise, 100).astype(int)

        for date, price, volume in zip(dates, prices, volumes):
            records.append(
                {
                    "date": date,
                    "instrument": ticker,
                    "close": float(price),
                    "volume": int(volume),
                }
            )

    return pd.DataFrame.from_records(records)
