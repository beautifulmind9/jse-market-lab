# Sprint 9 — Ticker Intelligence Layer

## Goal
Help users understand how individual stocks behave so they can make better decisions beyond just selecting trades.

---

## Problem

The dashboard currently shows:
- which trades are selected
- why they were selected

But it does not answer:

- Does this stock usually work?
- Is it consistent or unpredictable?
- Is it better short-term or long-term?

---

## Scope

### 1. Ticker Analysis Tab

Add a new section to the app:

**Ticker Analysis**

User flow:
- Select ticker from dropdown
- View:
  - Summary
  - Key stats
  - Behavior insights

---

### 2. Summary (Top Output)

Single sentence that explains:

- how the stock behaves
- what kind of results it produces

Example:

> This stock works better over longer holds and gives more consistent results.

---

### 3. Key Stats

Display minimal stats:

- Win rate
- Median return
- Average return
- Best holding window
- Signal count

---

### 4. Behavior Insights

Four core insights:

#### Holding Window
- Compare 5D vs 20D

#### Consistency
- Compare median vs average return

#### Reliability
- Based on win rate

#### Tier Profile
- Based on quality tier distribution

---

### 5. Sample Size Warning

If signals are low:
> There is limited data for this stock, so results may not be reliable.

---

## Output Structure

```python
{
  "summary": "...",
  "stats": {...},
  "behavior": {
    "holding_window": "...",
    "consistency": "...",
    "reliability": "...",
    "tier_profile": "..."
  }
}
