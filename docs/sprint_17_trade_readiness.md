# Sprint 17 — Trade Readiness, Liquidity & Data Foundations

## Objective

Help users understand whether a funded trade has enough practical context to consider, without changing the funding logic.

Sprint 17 focuses on:
- liquidity visibility
- volume support clarity
- spread and volatility context
- sample-size interpretation
- signal-date readiness for future freshness logic

---

## Why This Sprint Exists

Sprint 16 clarified:
- when the dashboard was viewed
- the latest market data date
- how users should count review windows from their entry date

The next question users naturally ask is:

> Is this trade ready enough for me to consider?

That question requires more than a funded label. Users need to understand tradeability, supporting evidence, and whether the current system has enough data to make a strong statement.

---

## Product Principle

Funding status is determined by portfolio and ranking rules.

Liquidity, volume, spread, volatility, sample size, and signal timing are trade-readiness context.

These fields help users interpret the decision, but they should not contradict funded status unless a rule explicitly blocks the trade.

---

## Liquidity Decision

Sprint 17 should **not** enforce a new strong numeric liquidity threshold yet.

### Reason
The current system treats liquidity/volume mainly as:
- availability context
- tier-capping context
- signal-support context

A hard liquidity threshold should be:
- researched
- backtested
- calibrated for JSE market behavior
- documented before becoming a blocking rule

Sprint 17 should expose what currently exists and identify what is missing.

---

## Required Deliverables

### 1. Trade Readiness Section

Add a compact Trade Readiness section where data exists.

Suggested fields:
- Liquidity data: Available / Limited / Not available
- Volume support: Present / Limited / Not available
- Spread behavior: Supportive / Watch / Not available
- Volatility context: Low / Moderate / High / Not available
- Evidence base: Small sample / Moderate sample / Broader sample
- Signal timing: Not yet assessed / Signal date unavailable

If a field is missing or unreliable, say so plainly.

Do not invent values.

---

### 2. Funding vs Supporting Analysis Copy

Add copy near Ticker Analysis when opened from Portfolio:

> This trade was selected by the portfolio rules. The analysis below gives supporting historical context.

This prevents the analysis layer from sounding like it contradicts the funding decision.

---

### 3. Sample-Size Interpretation

Improve sample-size notes.

For small samples:

> Built from about {n} completed trades. This gives supporting context, but the pattern is still developing.

For broader samples:

> Built from a broader set of completed trades, so the holding-window read is more mature.

Sample size should not block funding in Sprint 17.

---

### 4. Liquidity Wording Guardrails

Avoid:
- Liquidity confirmed
- Trade is liquid
- Safe to enter

Use:
- Liquidity data available
- Liquidity data limited
- Tradeability should be reviewed carefully

---

### 5. Signal-Date Readiness Audit

Inspect whether current Portfolio or Ticker Analysis rows include a clean signal date.

Document:
- available signal-date fields
- reliability of those fields
- missing fields needed for future Fresh / Active / Late / Stale labels

Do not implement signal freshness labels unless the data is clean and stable.

---

## Out of Scope

Do not implement:
- new numeric liquidity thresholds
- new ranking logic
- new allocation logic
- stop-loss / price-exit logic
- fee or return projections
- AI news, earnings, or economic summaries
- live market streaming

---

## Success Criteria

A user should be able to answer:
- Is there liquidity or volume context for this trade?
- Is the sample size small or more mature?
- Is Ticker Analysis supporting the Portfolio decision rather than contradicting it?
- Is signal timing currently assessed or still missing?

---

## Future Dependencies

Sprint 17 should prepare the ground for:
- Signal Freshness Layer
- Exit Logic & Risk Controls
- Portfolio Economics Layer
- AI Event / News / Earnings Context Layer
