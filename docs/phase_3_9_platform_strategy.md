# Phase 3–9 Platform Strategy — JSE Market Lab

## Purpose

This document is the source-of-truth strategy for expanding JSE Market Lab beyond the current dashboard into a broader JSE market intelligence, research, education, brokerage-access, and monetization platform.

The dashboard remains the decision engine. The platform expansion adds the surrounding product layers that help users learn, research, compare, access licensed institutions, and eventually pay for higher-value tools.

---

## Strategic Product Shift

JSE Market Lab is evolving from:

> A JSE trading dashboard

into:

> A market intelligence, research, decision-support, education, and brokerage-access platform for Jamaican, Caribbean, and diaspora investors.

This expansion does not change the product boundary.

JSE Market Lab remains:
- decision-support only
- educational
- research-oriented
- transparent about data and risk
- careful about compliance and user agency

JSE Market Lab is not:
- a financial advisor
- a broker-dealer
- a signal-selling platform
- a prediction engine
- an auto-trading system
- a custodian of client funds

---

## Core Platform Principle

Every future layer must support one or more of the following:

1. Better market understanding
2. Better research discovery
3. Better decision structure
4. Better risk awareness
5. Better access to licensed institutions
6. Better user discipline
7. Better transparency
8. Better monetization without compromising trust

No layer should encourage blind following, guaranteed returns, hype, or unlicensed advice.

---

## Current Foundation

The current dashboard already supports:

- JSE market data ingestion
- median crossover signals
- cooldown logic
- liquidity checks
- volume confirmation
- spread context
- volatility buckets
- holding windows: 5D, 10D, 20D, 30D
- win rate
- median return as the main typical-outcome metric
- average return as supporting context
- quality tiers: A/B/C
- portfolio allocation
- funded vs unfunded trade separation
- capital input
- cash reserve
- Ticker Analysis
- Review / discipline layer
- Trade Readiness
- trading-cost assumptions: broker fee 0.50% and CESS 0.35%

This is the decision-support engine that future layers should connect to.

---

# Phase 3 — Brokerage Access Flow

## Purpose

Create a compliant pathway for users who have learned from the platform and want to open a brokerage account with a licensed institution.

## Product goal

Move the user from:

> I understand the JSE better now.

To:

> I know the next steps to open a brokerage account through a licensed institution.

## Core principle

The CTA must support market access, not investment advice.

## User journey

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

## Key screens

### Screen 1 — Entry CTA

Copy:

> Need a brokerage account to invest on the JSE?
>
> To buy or sell JSE-listed securities, you need an account with a licensed broker-dealer. JSE Market Lab can help you understand the account-opening process and connect you with a licensed institution.

Button:

> Start account-opening guide

### Screen 2 — User location

Fields:
- Jamaica
- Jamaican living overseas
- Caribbean resident
- United States
- Canada
- United Kingdom
- Other

### Screen 3 — Investor readiness

Questions:
- Do you already have a brokerage account?
- Are you looking to open one?
- Are you mainly interested in dividends, general investing, short/medium-term trading, or learning?

Approximate starting range:
- Under JMD $100,000
- JMD $100,000–$499,999
- JMD $500,000–$999,999
- JMD $1M–$4.9M
- JMD $5M+

### Screen 4 — General document checklist

Possible documents:
- government-issued ID
- proof of address
- TRN or tax ID where applicable
- source of funds
- employment/business information
- bank information
- tax residency declarations
- W-8BEN/FATCA-related documents for US persons if required by institution

### Screen 5 — Consent and disclosure

Required language:

> By submitting this form, you agree that JSE Market Lab may share your contact details and account-opening interest with a licensed financial institution for follow-up. JSE Market Lab does not provide investment advice, open accounts, hold funds, or execute trades.

### Screen 6 — Confirmation

Copy:

> Your request has been submitted. A licensed financial institution may contact you directly about account opening. Please review all documents, fees, risks, and requirements before proceeding.

## Data fields to store

- lead_id
- name
- email
- phone
- country
- resident_status
- has_brokerage_account
- interest_area
- estimated_funding_range
- preferred_contact_method
- consent_timestamp
- source_page
- broker_routed_to
- lead_status
- account_opened_status
- funded_status
- referral_fee_status
- created_at
- updated_at

## Lead statuses

- new
- qualified
- sent_to_broker
- broker_contacted
- account_opened
- account_funded
- closed_lost
- not_eligible
- user_withdrew

## Success metrics

- CTA click rate
- form completion rate
- qualified lead rate
- broker response time
- account-open conversion
- funded-account conversion
- revenue per lead
- user satisfaction
- complaint rate

## Guardrails

Do not say:
- Best broker
- Recommended broker
- Buy now
- Invest in this stock
- This broker will give you the best return

Do say:
- licensed institution
- account-opening support
- market access
- review all fees and requirements
- JSE Market Lab does not provide investment advice

---

# Phase 4 — Research Hub

## Purpose

Create one central place for JSE-related research, company filings, notices, dividend information, market commentary, and structured summaries.

## Product goal

Move the user from:

> Information is scattered everywhere.

To:

> I can find the research and company context I need in one place.

## MVP structure

Start with a research index.

## Research table schema

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

## Report types

- quarterly_financial_statement
- audited_financial_statement
- annual_report
- dividend_notice
- top_10_shareholder_notice
- company_announcement
- broker_research
- independent_analyst_note
- market_update
- earnings_summary
- sector_report
- ipo_apo_note
- education_note

## Rights status

- public_link_only
- permission_to_host
- partner_research
- original_jse_market_lab_summary
- licensed_content
- do_not_host

## Hosting policy

> Index and summarize responsibly. Host only where permission or licensing exists.

## User-facing filters

- ticker
- company
- sector
- report type
- source
- date
- dividend relevance
- earnings relevance
- risk flag
- analyst
- scored call status

## Beginner summary format

- What happened?
- Why it matters
- What to watch
- Data/source note

## Analyst summary format

- Source
- Main thesis
- Financial performance
- Dividend impact
- Liquidity/tradability context
- Risks
- Open questions

## Success metrics

- research page views
- search usage
- report clicks
- saved reports
- company page visits
- account-opening CTA clicks from research pages
- premium conversion from research pages

---

# Phase 5 — Company Pages

## Purpose

Create one structured page per listed company.

## Product goal

Move the user from:

> I need to search everywhere to understand this company.

To:

> This page gives me the company, research, dividend, earnings, ownership, and trading context.

## Company page sections

### 1. Company overview

- company name
- ticker
- sector
- business description
- listing market
- website
- latest available data date

### 2. Market activity

- latest price
- price change
- volume
- value traded or estimated value traded
- days traded
- liquidity status
- spread context

### 3. Dividend profile

- dividend-paying / non-dividend
- latest dividend
- dividend frequency
- dividend consistency
- dividend yield, if calculated
- dividend risk flag

### 4. Earnings trend

- latest quarter
- revenue trend
- profit trend
- EPS trend
- margin direction
- stronger/stable/weaker classification

### 5. Research library

- latest research notes
- filings
- broker commentary
- analyst notes
- JSE notices

### 6. Ownership / float

- top 10 shareholder concentration
- public float, if available
- float-adjusted liquidity interpretation

### 7. Dashboard signal context

- current signal status
- tier
- holding window
- median return context
- volume confirmation
- liquidity filter
- volatility bucket
- risk notes

### 8. CTA

Copy:

> Need a brokerage account to act on your research?

Button:

> Start account-opening guide

## Success metrics

- company page visits
- ticker searches
- time on page
- saved companies
- research clicks
- broker CTA clicks
- premium conversion

---

# Phase 6 — Analyst Accountability Scoreboard

## Purpose

Track analyst calls against actual outcomes so research becomes more accountable and useful.

## Product goal

Move the market from:

> Analysts and commentators give opinions.

To:

> Analyst views are documented, scored, and reviewed over time.

## MVP name

Research Call Tracker

Do not launch a “Top Analyst” leaderboard immediately.

Start with:

> We are tracking research calls for transparency. Public rankings will appear once enough calls are available.

## Analyst call schema

- call_id
- analyst_name
- firm_name
- source_type
- ticker
- company_name
- date_published
- call_type
- time_horizon
- publication_price
- target_price
- main_thesis
- risk_disclosures
- source_url
- report_id
- is_scored_call
- score_status
- outcome_30d
- outcome_90d
- outcome_180d
- outcome_1y
- benchmark_return
- dividend_adjustment
- corporate_action_adjustment
- liquidity_adjustment
- overall_score
- created_at
- updated_at

## Call types

- buy
- hold
- sell
- accumulate
- reduce
- watch
- under_review
- outperform
- underperform
- dividend_income_view
- earnings_positive
- earnings_negative

## Content classification

| Content type | Scored? |
|---|---|
| Clear directional call | Yes |
| Target price call | Yes |
| Outperform/underperform view | Yes |
| General earnings summary | No |
| Education article | No |
| Vague commentary | No |
| Market recap | No, unless testable call exists |

## Scoring components

| Component | Weight |
|---|---:|
| Direction accuracy | 25% |
| Benchmark-adjusted performance | 20% |
| Risk/liquidity realism | 15% |
| Thesis quality | 15% |
| Update discipline | 10% |
| Specificity/testability | 10% |
| Risk disclosure | 5% |

## Minimum ranking rule

Main leaderboard eligibility = at least 10 scored calls.

Before 10 calls:

> Tracking in progress — not enough scored calls yet.

## Correction/dispute process

Analysts must be able to request corrections for:
- wrong publication price
- wrong date
- wrong ticker
- incorrect call classification
- missing update
- corporate action adjustment
- dividend adjustment
- source context

## Trust language

Avoid:
- Worst analyst
- Bad analyst
- Exposed
- Failed prediction

Use:
- Call history
- Research performance
- Documented outcomes
- Scored calls
- Tracking in progress
- Methodology

---

# Phase 7 — Market Intelligence Features

## Purpose

Add investor-facing data views suggested by product and partner discussions.

## Feature 1 — Dividend View

User question:

> Which companies have an income profile?

Fields:
- ticker
- company_name
- dividend_paying_status
- latest_dividend
- ex_dividend_date
- payment_date
- dividend_yield
- dividend_frequency
- dividend_consistency
- dividend_growth_trend
- earnings_support_flag
- dividend_risk_flag

Labels:
Use:
- Dividend-paying
- Non-dividend
- Irregular dividend
- Dividend watch
- Dividend risk

Avoid:
- Best dividend stock
- Guaranteed income
- Safe dividend

## Feature 2 — Earnings Scorecard

User question:

> Is this company improving, stable, or weakening?

Fields:
- ticker
- quarter
- revenue_current
- revenue_prior_year
- profit_current
- profit_prior_year
- eps_current
- eps_prior_year
- margin_current
- margin_prior_year
- earnings_direction
- earnings_pressure_flag
- loss_making_flag

Labels:
Use:
- Stronger
- Stable
- Weaker
- Earnings pressure
- Loss-making quarter
- Needs review

Avoid:
- Bad stock
- Losing stock
- Failed company

## Feature 3 — Performance vs Baseline

User question:

> Did the company perform better or worse than a realistic comparison point?

Baselines:
- same quarter last year
- previous quarter
- trailing average
- dividend history
- management guidance if available

Labels:
- Above baseline
- In line with baseline
- Below baseline
- Not enough data

## Feature 4 — Float / Tradability View

User question:

> Can ordinary investors realistically trade this stock?

Fields:
- ticker
- public_float
- top_10_shareholder_concentration
- average_daily_volume
- days_traded_last_20
- bid_ask_spread
- liquidity_status
- float_adjusted_liquidity_score
- tradability_warning

## Feature 5 — Market Pulse

User question:

> How is the JSE doing right now?

Sections:
- market direction
- index movement
- top gainers
- top decliners
- most active by volume
- most active by value
- dividend notices
- earnings alerts
- liquidity warnings
- unusual movement
- weekly summary

## Success metrics

- Market Pulse visits
- Dividend View usage
- Earnings View usage
- CTA clicks
- watchlist saves
- premium conversions
- returning users

---

# Phase 8 — Monetization Packaging

## Purpose

Turn features into sellable products.

## Investor-facing packages

### Free

Includes:
- basic Market Pulse
- limited company pages
- basic education
- account-opening guide
- limited research index

### Premium

Includes:
- full company research summaries
- dividend view
- earnings scorecard
- watchlists
- weekly market insights
- saved companies
- limited analyst call history

### Pro

Includes:
- advanced filters
- portfolio planning
- analyst scoreboard
- exports
- deeper research archive
- advanced company comparisons

### Diaspora Investor Pack

Includes:
- JSE investing guide
- broker access flow
- account-opening checklist
- dividend/income education
- company research pack
- market orientation guide

## Institution-facing packages

- Lead Referral Package
- Account Opening Package
- Funded Account Package
- Research Distribution Package
- White-label Education Package

## Required disclosures

Every paid/sponsored/broker-related area must clearly show:
- whether content is sponsored
- whether the broker paid for placement
- whether a referral fee may be earned
- that JSE Market Lab does not provide personal investment advice
- that users should review fees, risks, and requirements directly with the institution

---

# Phase 9 — Documentation and Operating System

## Purpose

Create the internal documents needed to guide the next build chats, protect the product direction, and support the portfolio story.

## Documents to create / maintain

1. Broker Referral Revenue Model
2. Brokerage Access Flow Spec
3. Research Hub Product Brief
4. Company Pages Product Brief
5. Analyst Scoreboard Methodology
6. Market Intelligence Roadmap
7. Compliance & Disclosure Playbook
8. Partner Outreach Tracker
9. AI Product Brief
10. AI Workflow Architecture
11. AI Guardrails
12. AI Evaluation Plan
13. AI Implementation Case Study

---

# Build Priority

## First

- Continue Sprint 18A readiness-gate research layer
- Continue richer market scraper work
- Send JSE data/licensing email
- Send FSC/legal compliance query
- Create Broker Referral Revenue Model doc
- Create Research Hub MVP structure
- Create Brokerage Access Flow spec

## Second

- Build FastAPI backend foundation
- Keep Streamlit running during migration
- Add soft CTA prototype only after compliance language is validated
- Start manual broker/advisor research
- Start research index manually
- Define analyst scoring methodology before public leaderboard

## Third

- Build Company Pages
- Build Market Pulse
- Add Dividend View
- Add Earnings Scorecard
- Add Float / Tradability View

## Later

- Launch broker referral pilot
- Launch paid subscription
- Launch analyst profiles
- Launch public analyst leaderboard only after enough data
- Add AI-assisted explanation workflows after structured outputs and guardrails are stable

---

# Strategic Summary for Future Chats

JSE Market Lab is evolving from a JSE trading dashboard into a market intelligence, research, decision-support, and brokerage-access platform for Jamaican, Caribbean, and diaspora investors.

The product must remain decision-support only. It must not provide personal investment advice, guarantee outcomes, recommend buy/sell actions, execute trades, or hold client funds.

The new pathway includes:
1. Research Hub
2. Company Pages
3. Analyst Accountability Scoreboard
4. Market Pulse
5. Dividend View
6. Earnings Scorecard
7. Float / Tradability View
8. Brokerage Access Flow
9. Broker referral / account-opening revenue model
10. Premium research and subscription products

The revenue model includes:
- broker referral fees for qualified leads, opened accounts, or funded accounts
- investor subscriptions
- research distribution partnerships
- analyst profiles
- white-label investor education/onboarding products

Compliance must be validated with JSE for data licensing and FSC/legal counsel for securities, investment advice, referral fees, research hosting, analyst scoring, and disclosure requirements.

All language must emphasize education, research, transparency, data quality, user agency, and licensed financial institution account-opening support.
