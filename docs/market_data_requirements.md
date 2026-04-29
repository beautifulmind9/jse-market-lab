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

## Rich Market Prices Dataset

A richer market-prices scrape can improve Sprint 18 readiness research and future Analyst Insights.

Example fields from the market-prices dataset:

- date
- ticker
- company_name
- market_code
- market_name
- security_type
- currency
- open
- high
- low
- close
- adjusted_close
- volume
- value_traded
- trades_count
- source
- source_url
- source_file
- ingested_at

### High-value fields

The most valuable additions beyond the current canonical dataset are:

- **open / high / low / close** — supports volatility, range, drawdown, and better risk-control testing
- **value_traded** — supports stronger liquidity and turnover rules
- **trades_count** — supports participation quality, not just raw volume
- **security_type** — allows filtering ordinary shares vs preference shares
- **currency** — prevents JMD and USD instruments from being mixed incorrectly
- **source_url / source_file / ingested_at** — supports auditability and data lineage

---

## Mini Scraper Run Audit — 2026-04-20 to 2026-04-24

A mini scraper run across all markets produced normalized and raw outputs for:

- all markets
- main market
- junior market
- USD market

### Normalized all-markets output

Observed shape:

- 625 rows
- 125 tickers
- date range: 2026-04-20 to 2026-04-24

Market/security coverage:

- junior_market ordinary_share JMD: 240 rows
- main_market ordinary_share JMD: 265 rows
- main_market preference_share JMD: 80 rows
- usd_market preference_share USD: 40 rows

### Field completeness observed

Fully populated:

- high
- low
- close
- volume
- date
- ticker
- market_code
- market_name
- security_type
- currency
- source
- source_url
- source_file
- ingested_at

Currently empty in normalized output:

- open
- adjusted_close
- value_traded
- trades_count
- company_name

### Important raw payload fields available

The raw payload includes fields that should be promoted into normalized columns where possible:

- last_traded_price
- closing_price
- price_change
- closing_bid
- closing_ask
- today_s_range
- 52_week_range
- total_prev_yr_div
- total_current_yr_div

### Product implication

This scraper run materially improves Sprint 18 possibilities because `high` and `low` are now populated.

It supports:

- high-low daily range
- better volatility research
- intraday range context
- price-risk research using daily range and close
- bid/ask spread research if closing_bid and closing_ask are normalized from raw payload
- dividend context if dividend fields are normalized

It still does not yet support:

- true value traded unless source data can populate it
- trades count unless source data can populate it
- company name unless another reference source is joined
- full news/earnings analysis without a separate events/news dataset

---

## Recommended Scraper Formatting

To support upcoming development, the scraper should output a consistent daily row per ticker with these columns where possible:

### Required baseline

- date
- ticker
- market_code
- market_name
- security_type
- currency
- close
- volume
- source_url
- ingested_at

### Strongly recommended

- open
- high
- low
- value_traded
- trades_count
- adjusted_close
- company_name

### Newly recommended from raw payload

Because the raw JSE trade quote payload includes these fields, the scraper should attempt to normalize them:

- last_traded_price
- price_change
- closing_bid
- closing_ask
- bid_ask_spread
- bid_ask_spread_pct
- today_range_low
- today_range_high
- week_52_low
- week_52_high
- total_prev_yr_div
- total_current_yr_div

### Future event/news fields

Event/news data can be stored separately, but should join cleanly to ticker/date:

- ticker
- event_date
- event_type
- source_title
- source_url
- source_date
- raw_text or extracted_text
- summary
- event_period
- severity / attention_flag

---

## What Each Field Unlocks

### Volatility and risk controls

Requires:
- open
- high
- low
- close

Unlocks:
- daily range
- close-to-close volatility
- high-low volatility
- maximum adverse movement if entry/exit dates are known
- better price-exit research

### Liquidity and tradeability

Requires:
- volume
- value_traded
- trades_count
- closing_bid
- closing_ask

Unlocks:
- turnover rules
- participation quality
- volume reliability
- zero-volume / thin-trading detection
- bid-ask spread checks
- liquidity deterioration checks

### Analyst Insights

Requires:
- security_type
- currency
- market_name
- richer price/volume fields
- event/news data

Unlocks:
- ordinary-share vs preference-share separation
- JMD vs USD separation
- market/board comparisons
- event-aware performance summaries
- richer insight cards

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
- Sprint 18: Readiness Gating Research & Risk Control Design
- Signal Freshness Layer
- Exit Logic & Risk Controls
- Portfolio Economics Layer
- AI Event / News / Earnings Context Layer
