# Market Data Requirements

## Purpose

This document tracks market, event, and contextual data needed for upcoming development and analyst insight layers.

The goal is to prevent future features from overclaiming when the underlying data is missing or incomplete.

---

## Current Priority Areas

### 1. Liquidity & Tradeability

Needed for stronger liquidity rules and trade-readiness context:

- ticker / instrument
- trade date
- close price
- volume traded
- value traded, if available
- bid price, if available
- ask price, if available
- spread or bid-ask spread, if available
- number of trading days in lookback window
- average volume over lookback windows, e.g. 5D / 20D / 60D
- number of zero-volume days
- liquidity pass / fail / watch flag

Future use:
- numeric liquidity threshold calibration
- liquidity deterioration exits
- realistic execution warnings

---

### 2. Signal Timing

Needed for signal freshness and remaining-window logic:

- signal date
- entry reference date
- signal-day close price
- holding window assigned
- current/latest market data date
- trading days since signal
- trading days since user entry, if user-entered trade tracking is added

Future use:
- Fresh / Active / Late / Stale labels
- remaining review-window context
- late-entry warnings

---

### 3. Portfolio Economics

Needed for capital-based outcomes:

- user capital input
- allocation percentage
- allocation amount
- entry reference price
- exit/reference price
- broker fee
- CESS
- total estimated trading cost
- median return by holding window
- average return by holding window
- net JMD outcome estimate

Future use:
- expected net outcome by capital
- fee drag education
- portfolio-level cost summary

---

### 4. Exit Logic & Risk Controls

Needed before adding price/risk exits:

- entry price
- signal-day close
- daily low/high if available
- close-to-close drawdown
- maximum adverse excursion, if calculable
- volatility bucket
- spread behavior after entry
- volume deterioration after entry
- earnings/event overlap

Future use:
- price-based exits
- downside threshold testing
- signal invalidation exits
- liquidity deterioration exits

---

### 5. Earnings Season & Corporate Events

Needed for earnings and event context:

- ticker
- event date
- event type: earnings, dividend, annual report, notice, circular, corporate action
- source URL or uploaded source reference
- source publication date
- summary text
- event period: pre, reaction, post, non
- overlap with holding window
- severity / attention flag

Future use:
- earnings-season warnings
- dividend context
- event-aware holding-window interpretation

---

### 6. News & Economic Context

Needed for AI-assisted context reviews:

- ticker, if company-specific
- source title
- source date
- source publisher
- source URL or document reference
- article text or extracted summary
- macro category, if relevant: inflation, FX, interest rates, GDP, sector conditions
- relevance to ticker / sector / market

Future use:
- AI event summary cards
- macro context cards
- analyst insight notes

---

## AI API Guardrails

The AI layer should be a context review layer, not a trade recommender.

It should answer:
- What happened?
- Why might it matter?
- What should the user watch?
- What source/date is this based on?

It should not answer:
- Should I buy?
- Will this stock go up?
- Is this guaranteed?

Required guardrails:
- always show source and date
- separate facts from interpretation
- avoid buy/sell language
- flag missing or weak source context
- do not automatically change rankings in early versions

---

## Roadmap Link

These requirements support:
- Sprint 17: Trade Readiness, Liquidity & Data Foundations
- Signal Freshness Layer
- Exit Logic & Risk Controls
- Portfolio Economics Layer
- AI Event / News / Earnings Context Layer
