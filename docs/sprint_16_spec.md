# Sprint 16 — Live Context & Trade Timing Layer

## Objective

Make the dashboard time-aware so users understand:
- when they are viewing the plan
- what data the plan is based on
- how to interpret holding windows correctly

---

## Problem

After Sprint 15:
- users can navigate Portfolio → Ticker Analysis
- the system feels more actionable

But currently:
- there is no clear `Viewed as at` time
- there is no clear visible distinction between user view time and latest market data date
- holding windows can be misinterpreted as calendar-month timing

This creates a false sense of immediacy or timelessness.

---

## Product Principle

The dashboard should never make a trade idea feel timeless.

Every plan should distinguish:

1. **Viewed as at** — when the user loaded or refreshed the page
2. **Latest market data date** — the latest date included in the loaded dataset
3. **Holding window** — the trading-day review period tied to the signal or entry reference
4. **Signal timing** — when the signal occurred and whether it still appears fresh, active, late, or stale, if clean signal-date fields are available

---

## Scope

### Sprint 16A — Implement Now

Add live context copy and timestamps.

#### Required UI additions

Add near the top of Portfolio and Ticker Analysis:

- `Viewed as at: {timestamp}`
- `Latest market data in dashboard: {date}`

Add holding-window interpretation copy.

Current copy is directionally correct but may feel too vague for first-time users:

> Holding windows are measured in trading days from the signal or entry reference, not from the calendar month.

Preferred clearer copy:

> Holding windows are review periods. A 5D, 10D, 20D, or 30D window means the trade should be reviewed after that many trading days from the signal or your entry reference — not held until month-end.

If space is limited, use:

> 5D, 10D, 20D, and 30D are trading-day review windows from the signal or entry reference, not calendar-month deadlines.

Wording must stay clear that the app is not a live-streaming market feed.

---

### Sprint 16B — Conditional Follow-up

Only implement if the required signal-date fields are already available cleanly in Portfolio or Ticker Analysis rows.

Potential additions:
- signal date
- signal age in trading days
- timing classification: Fresh, Active, Late, Stale
- approximate remaining holding-window context

If the data is not cleanly available, document this as follow-up rather than forcing a fragile implementation.

---

## Out of Scope

Do not implement in Sprint 16:
- fee and expected-return-by-capital layer
- new liquidity numeric thresholds
- Decision Audit Table expansion
- user-controlled date-range regeneration
- live market streaming
- trade tracking
- brokerage execution workflow

---

## Success Criteria

A user should be able to answer:
- When am I viewing this plan?
- How recent is the market data in the dashboard?
- How should I interpret 5D, 10D, 20D, or 30D holding windows?
- Does the holding-window label mean a review period rather than a calendar deadline?

---

## Constraints

Presentation/context layer first.

Do not change:
- ranking logic
- allocation logic
- signal generation
- ticker-analysis calculations
- backtest logic
