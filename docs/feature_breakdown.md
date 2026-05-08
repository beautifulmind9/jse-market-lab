# Feature Breakdown — JSE Market Lab

## Product Identity

JSE Market Lab is evolving from a JSE trading dashboard into a broader market intelligence, research, decision-support, education, brokerage-access, and monetization platform for Jamaican, Caribbean, and diaspora investors.

The dashboard remains the decision engine. The platform layers around it add research context, company pages, market intelligence, account-opening education, and future AI-assisted explanation workflows.

Core boundary:
- decision support only
- no financial advice
- no buy/sell instructions
- no prediction claims
- no guaranteed returns
- no trade execution
- no holding client funds
- missing or weak data must be disclosed

---

## Core Systems

### 1. Signal Engine
- Detects median crossover events
- Generates trade opportunities
- Supports event-based signal generation

### 2. Ranking Engine
- Scores opportunities based on:
  - trend strength
  - volume confirmation
  - volatility
  - spread behavior
  - quality tier
  - eligibility rules

### 3. Cost Engine
- Applies:
  - broker fee (0.50%)
  - CESS (0.35%)
- Produces net-of-cost returns
- Supports portfolio economics and future JMD outcome estimates

### 4. Weekly Trade Planner / Portfolio Engine
- Displays active opportunities
- Assigns holding windows (5D, 10D, 20D, 30D)
- Tracks entry/exit assumptions
- Preserves cash reserve
- Separates funded and unfunded trades
- Supports capital allocation logic

### 5. Earnings Intelligence Layer
- Tags earnings phases:
  - pre
  - reaction
  - post
  - non
- Detects overlap with holding windows

### 6. Earnings Warning System
- Generates:
  - warning title
  - warning body
  - severity level
- Signals risk during earnings overlap
- Preserves user agency rather than blocking automatically

### 7. Portfolio Decision Surface Layer

This layer translates allocation outputs into a user-facing decision interface.

#### Guided View
- Uses compact trade cards
- Prioritizes scanability and clarity
- Shows only core decision fields:
  - Ticker
  - Setup Strength
  - Confidence / Reliability
  - Holding Window
  - Why this trade / Why not funded
- Moves secondary fields into collapsed detail sections

#### Advanced View
- Uses a compact comparison table for first-pass scanning
- Avoids horizontal scrolling for critical fields
- Provides row-level drilldowns for deeper context

Primary comparison fields:
- Ticker
- Setup Strength / Tier
- Confidence / Reliability
- Holding Window
- Decision Status
- Allocation %
- Selection Rank

#### Drilldown Detail Layer
- Reveals deeper reasoning per trade:
  - Why this trade / Why not funded
  - Execution Summary
  - Rule Note
  - Allocation Amount
  - Allocation %
  - Selection Rank

#### Full Analyst Table
- Provides full raw data view
- May include horizontal scrolling
- Not used as the primary decision surface

Purpose:
- support fast comparison
- prevent hidden critical information
- preserve analytical depth without overwhelming users

### 8. Ticker Analysis

Ticker Analysis helps users understand one stock through:
- Quick Take
- Best Holding Strategy
- Risk Profile
- What Usually Happens
- What to Watch
- Execution Behavior
- Trade Readiness

Ticker Analysis is a strong user hook because users can start with a stock they already know, then connect back to portfolio logic.

### 9. Review / Decision Audit

Current direction:
- human-readable explanation of how ranking, quality, liquidity, and allocation rules were applied
- post-decision reflection and discipline guidance

Future direction:
- numeric/semi-numeric decision audit
- score breakdowns
- comparison of funded vs unfunded trades
- transparent explanation of why one setup outranked another

### 10. Trade Readiness Layer

Current direction:
- liquidity data availability
- volume support
- spread behavior
- volatility context
- evidence base
- signal timing

Future direction:
- readiness labels: Ready / Watch / Incomplete / Not fundable
- readiness gating after research and backtesting
- possible impact on funding eligibility, allocation sizing, or warning labels

---

## Data Foundation Features

### 1. Market Prices Dataset

Purpose:
Power signals, liquidity, volatility, spread, readiness, market pulse, and exit-risk research.

Recommended fields:
- date
- ticker
- market_code
- market_name
- security_type
- currency
- close
- high
- low
- volume
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
- estimated_value_traded
- source_url
- source_file
- ingested_at

Derived fields:
- open = previous trading day close, if true open is unavailable
- open_source = previous_close / reported / unavailable
- estimated_value_traded = close * volume when official value traded is unavailable

### 2. Ticker Master Reference

Purpose:
Maintain company-level metadata separately from daily price rows.

Recommended file:
- `data/reference/ticker_master.csv`

Recommended fields:
- ticker
- company_name
- market_code
- market_name
- sector
- security_type
- currency
- is_active
- effective_from
- effective_to
- source_url
- ingested_at

### 3. Events / News Dataset

Purpose:
Power earnings/news warnings, dividend announcements, corporate actions, Analyst Insights, and future AI context cards.

Recommended file:
- `data/events_news.csv`

Recommended fields:
- ticker
- event_date
- event_type
- source_title
- source_url
- source_date
- raw_text
- extracted_text
- summary
- event_period
- severity
- attention_flag
- ingested_at

This should be scraped separately from market prices.

---

## Platform Expansion Features

## Phase 3 — Brokerage Access Flow

Purpose:
Create a compliant pathway for users who have learned from the platform and want to open a brokerage account with a licensed institution.

Core user journey:
1. User reads insight / company page / research summary
2. User sees “Need a brokerage account?” CTA
3. User opens account-opening guide
4. User identifies country/residency
5. User answers readiness questions
6. User sees general document checklist
7. User consents to be contacted
8. Lead is routed to institution
9. Broker handles onboarding directly
10. JSE Market Lab tracks lead status

Key screens:
- Entry CTA
- User location
- Investor readiness
- General document checklist
- Consent and disclosure
- Confirmation

Allowed language:
- licensed institution
- account-opening support
- market access
- review all fees and requirements
- JSE Market Lab does not provide investment advice

Avoid:
- best broker
- recommended broker
- buy now
- invest in this stock
- this broker will give you the best return

## Phase 4 — Research Hub

Purpose:
Create one central place for JSE-related research, company filings, notices, dividend information, market commentary, and structured summaries.

MVP:
Start with a research index.

Research table fields:
- research_id
- date_published
- ticker
- company_name
- sector
- report_type
- source_name
- author
- source_url
- rights_status
- summary_short
- summary_beginner
- summary_analyst
- key_points
- risk_flags
- dividend_relevance
- earnings_relevance
- liquidity_relevance
- scored_call_yes_no
- created_at
- updated_at

Hosting policy:
Index and summarize responsibly. Host only where permission or licensing exists.

## Phase 5 — Company Pages

Purpose:
Create one structured page per listed company.

Sections:
1. Company overview
2. Market activity
3. Dividend profile
4. Earnings trend
5. Research library
6. Ownership / float
7. Dashboard signal context
8. Brokerage account CTA

Company Pages should combine company context with the existing decision-support engine.

## Phase 6 — Analyst Accountability Scoreboard

Purpose:
Track analyst calls against actual outcomes so research becomes more accountable and useful.

MVP name:
Research Call Tracker

Do not launch a public leaderboard immediately.

Initial public language:
> We are tracking research calls for transparency. Public rankings will appear once enough calls are available.

Minimum leaderboard rule:
Main leaderboard eligibility requires at least 10 scored calls.

Trust language:
Use:
- Call history
- Research performance
- Documented outcomes
- Scored calls
- Tracking in progress
- Methodology

Avoid:
- Worst analyst
- Bad analyst
- Exposed
- Failed prediction

## Phase 7 — Market Intelligence Features

Features:
1. Dividend View
2. Earnings Scorecard
3. Performance vs Baseline
4. Float / Tradability View
5. Market Pulse

Purpose:
Help users answer:
- Which companies have an income profile?
- Is this company improving, stable, or weakening?
- Did the company perform better or worse than a realistic baseline?
- Can ordinary investors realistically trade this stock?
- How is the JSE doing right now?

Language constraints:
Use:
- Dividend-paying
- Non-dividend
- Irregular dividend
- Dividend watch
- Dividend risk
- Stronger
- Stable
- Weaker
- Earnings pressure
- Loss-making quarter
- Needs review
- Above baseline
- In line with baseline
- Below baseline
- Not enough data

Avoid:
- Best dividend stock
- Guaranteed income
- Safe dividend
- Bad stock
- Losing stock
- Failed company

## Phase 8 — Monetization Packaging

Investor-facing packages:
- Free
- Premium
- Pro
- Diaspora Investor Pack

Institution-facing packages:
- Lead Referral Package
- Account Opening Package
- Funded Account Package
- Research Distribution Package
- White-label Education Package

Required disclosures:
- whether content is sponsored
- whether broker placement is paid
- whether a referral fee may be earned
- JSE Market Lab does not provide personal investment advice
- users should review fees, risks, and requirements directly with the institution

## Phase 9 — Documentation and Operating System

Documents to maintain:
- Broker Referral Revenue Model
- Brokerage Access Flow Spec
- Research Hub Product Brief
- Company Pages Product Brief
- Analyst Scoreboard Methodology
- Market Intelligence Roadmap
- Compliance & Disclosure Playbook
- Partner Outreach Tracker
- AI Product Brief
- AI Workflow Architecture
- AI Guardrails
- AI Evaluation Plan
- AI Implementation Case Study

---

## AI-Assisted Features

AI should explain structured outputs. It should not invent market opinions or make trade recommendations.

Approved future AI use cases:
- Data Quality Assistant
- Signal Explanation Assistant
- Portfolio Rationale Assistant
- Trade Readiness Assistant
- Event/News Risk Assistant
- Weekly Market Insight Assistant

Guardrails:
- no buy/sell instructions
- no guaranteed returns
- no price predictions
- no unsupported claims
- disclose missing data
- preserve user agency
- explain uncertainty clearly
- use dashboard data only
- support Clear Mode and Pro Mode where relevant

Every AI feature needs evaluation tests.

---

## Architecture Migration Features

Target architecture:

```text
Next.js frontend on Vercel
        ↓
FastAPI backend
        ↓
Existing Python decision engine
        ↓
Data layer / generated datasets / future database
```

Initial backend endpoints:
- `GET /health`
- `GET /api/data/status`
- `POST /api/portfolio/plan`
- `GET /api/ticker/{ticker}/analysis`
- `GET /api/review/decision-audit`

Future backend endpoints:
- trade readiness
- company pages
- research index
- events/news context
- brokerage access leads
- market pulse
- dividend view
- earnings scorecard
- user profile / saved decisions
- AI explanation context

---

## Success Metrics by Layer

### Core Dashboard
- user understands where to start
- capital input usage
- ticker analysis clicks
- portfolio-to-ticker handoff usage
- review tab usage

### Brokerage Access
- CTA click rate
- form completion rate
- qualified lead rate
- broker response time
- account-open conversion
- funded-account conversion
- complaint rate

### Research Hub
- research page views
- search usage
- report clicks
- saved reports
- company page visits
- account-opening CTA clicks from research pages
- premium conversion from research pages

### Company Pages
- company page visits
- ticker searches
- time on page
- saved companies
- research clicks
- broker CTA clicks
- premium conversion

### Market Intelligence
- Market Pulse visits
- Dividend View usage
- Earnings View usage
- CTA clicks
- watchlist saves
- premium conversions
- returning users
