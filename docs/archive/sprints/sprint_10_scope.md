# Sprint 10 — Ticker Drilldown (Deep Understanding Layer)

## Goal
Give users deeper understanding of each stock beyond summary behavior.

This layer answers:
- Why does this stock behave this way?
- What patterns show up over time?
- When does it actually perform best?

---

## Problem

Sprint 9 tells the user:
- how a stock behaves (summary + insights)

But it does NOT show:
- detailed performance breakdown
- distribution of outcomes
- consistency across holding windows
- how tiers perform for that stock

---

## Scope

### 1. Ticker Drilldown View (Extended Analysis)

This builds on Sprint 9.

User selects ticker → sees:

- deeper breakdown
- structured performance view

---

### 2. Signal Breakdown

Show all signals for the ticker:

- date
- holding window (5D / 20D)
- return %
- win/loss
- quality tier
- volatility bucket

---

### 3. Holding Window Performance

Compare:

- 5D vs 20D:
  - win rate
  - median return
  - average return

Output example:

> Short trades give quicker results but are less stable. Longer holds are more consistent.

---

### 4. Return Distribution

Show:

- how often returns are:
  - negative
  - small positive
  - strong positive

Purpose:
- show variability
- reduce “average illusion”

---

### 5. Tier Performance

Breakdown:

- Tier A:
  - win rate
  - returns

- Tier B:
  - win rate
  - returns

- Tier C:
  - (optional, informational only)

Output example:

> Tier A setups drive most of the positive results for this stock.

---

### 6. Volatility Behavior

Breakdown by:
- low / mid / high volatility

Output example:

> Mid-volatility setups tend to perform more reliably for this stock.

---

### 7. Pattern Summary (Top Insight)

One short section:

- what consistently works
- what doesn’t

Example:

> This stock works best with mid-volatility Tier A setups over longer holding periods.

---

## Output Structure

```python
{
  "signals": [...],
  "holding_window_stats": {...},
  "return_distribution": {...},
  "tier_performance": {...},
  "volatility_performance": {...},
  "pattern_summary": "..."
}
