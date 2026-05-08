# Product Backlog

## Current Product Stage

JSE Market Lab is moving from a Streamlit-first decision-support dashboard into a broader JSE market intelligence, research, education, brokerage-access, and monetization platform.

The core dashboard remains the decision engine. The expanded platform will add research, company context, market intelligence views, account-opening guidance, monetization, and operating documentation around that engine.

Core boundary:

- Decision support only
- No personal investment advice
- No buy/sell instructions
- No guaranteed outcomes
- No trade execution
- No holding client funds
- Missing or weak data must be disclosed
- Brokerage/account-opening flows must route users to licensed institutions, not position JSE Market Lab as an account opener or broker

---

## Phase 2 — Post-Beta Refinement / Decision Engine Trust Layer

### Sprint 16 — Live Context & Trade Timing
Status: Complete

Completed:
- Viewed timestamp
- Dataset recency visibility
- Entry-based holding-window interpretation clarity

Follow-up backlog:
- Signal timing awareness
- Signal age in trading days
- Fresh / Active / Late / Stale timing status
- Remaining holding-window context

---

### Sprint 17 — Trade Readiness, Liquidity & Data Foundations
Status: Complete

Completed:
- Trade Readiness UI layer
- Liquidity / volume / spread / volatility context without overclaiming
- Sample-size context without undermining funded trades
- Funding decision vs supporting analysis copy
- Signal-date readiness audit
- Canonical market date fallback for signal timing readiness

Follow-up backlog:
- Stronger numeric liquidity model research
- Calibrated liquidity thresholds by market/board/ticker behavior
- Signal freshness implementation after signal-date fields are stable

---

### Sprint 18 — Readiness Gating Research & Risk Control Design
Status: Active / research tooling in progress

Purpose:
Research whether Trade Readiness should affect funding eligibility, allocation sizing, warning labels, and early-exit/risk-control logic before changing the strategy engine.

Scope:
- Research whether Trade Readiness should affect funding eligibility
- Backtest minimum readiness gates before changing allocation logic
- Define Ready / Watch / Incomplete / Not fundable labels
- Design price-based and downside exit rules
- Design signal invalidation exits
- Design liquidity deterioration exits
- Design event-risk exits

Important constraint:
Do not change production funding, allocation, signal, or exit logic until readiness gates and risk controls are researched and backtested.

---

### Sprint 19 — Exit Logic Implementation & Review Guidance
Planned after Sprint 18 evidence.

Scope:
- Implement validated exit logic from Sprint 18 research
- Show risk-exit context in Execution Behavior
- Clarify that holding windows are review checkpoints, not unconditional holds
- Add reviewed-earlier-if-risk-changes guidance

---

### Sprint 20 — Portfolio Economics Layer
Scope:
- Allocation-based fee calculation
- Estimated net returns based on capital
- Portfolio-level cost summary
- Net outcome scenarios
- Broker fee: 0.50%
- CESS: 0.35%

---

### Sprint 21 — AI Event, Earnings, News & Economic Context Layer
Scope:
- Earnings season review cards
- Dividend and corporate action context
- Company news summaries
- Economic context summaries
- Source/date-grounded AI outputs
- AI guardrails to prevent buy/sell recommendations

---

### Sprint 22 — User Profile, Decision History & Adaptive Guidance
Scope:
- User profile storage
- Saved decisions and planned trades
- Review outcomes over time
- Track whether user followed plan rules
- Update guidance when market data changes
- Compare old saved decisions against new loaded market data
- Personal decision discipline feedback

---

### Sprint 23 — Decision Audit & Transparency
Scope:
- Ranking transparency
- Score breakdown visibility
- Structured comparison across trades
- Numeric/semi-numeric decision audit table
- Clear explanation of why one trade outranked another

---

## Architecture Migration Track

### Architecture Decision — Next.js + FastAPI
Status: Open issue #130

Direction:

```text
Next.js frontend on Vercel
        ↓
FastAPI backend
        ↓
Existing Python decision engine
        ↓
Data layer / generated datasets / future database
```

Purpose:
- Better mobile experience
- Better custom UI
- Future user accounts
- Saved portfolios
- Research Hub
- Company Pages
- Brokerage Access Flow
- AI explanation layers
- Subscriptions and premium features

### Backend API Foundation
Status: Open issue #131

Initial endpoints:
- `GET /health`
- `GET /api/data/status`
- `POST /api/portfolio/plan`
- `GET /api/ticker/{ticker}/analysis`
- `GET /api/review/decision-audit`

Future endpoints:
- trade readiness
- company pages
- research index
- events/news context
- brokerage access lead submission
- market pulse
- dividend view
- earnings scorecard
- user profile / saved decisions
- AI explanation context

---

## Phase 3 — Brokerage Access Flow

Purpose:
Create a compliant pathway for users who have learned from the platform and want to open a brokerage account with a licensed institution.

Product goal:
Move the user from:

> I understand the JSE better now.

To:

> I know the next steps to open a brokerage account through a licensed institution.

Core principle:
The CTA must support market access, not investment advice.

High-level user journey:
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

Data fields:
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

Lead statuses:
- new
- qualified
- sent_to_broker
- broker_contacted
- account_opened
- account_funded
- closed_lost
- not_eligible
- user_withdrew

Guardrails:
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

Compliance gate:
Do not launch this flow publicly until JSE/FSC/legal/broker referral questions are validated.

---

## Phase 4 — Research Hub

Purpose:
Create one central place for JSE-related research, company filings, notices, dividend information, market commentary, and structured summaries.

Product goal:
Move the user from:

> Information is scattered everywhere.

To:

> I can find the research and company context I need in one place.

MVP:
Start with a research index.

Research table schema:
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

Report types:
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

Rights policy:
Index and summarize responsibly. Host only where permission or licensing exists.

Rights statuses:
- public_link_only
- permission_to_host
- partner_research
- original_jse_market_lab_summary
- licensed_content
- do_not_host

---

## Phase 5 — Company Pages

Purpose:
Create one structured page per listed company.

Company page sections:
1. Company overview
2. Market activity
3. Dividend profile
4. Earnings trend
5. Research library
6. Ownership / float
7. Dashboard signal context
8. Brokerage account CTA

Company Pages should connect research context with the existing decision-support engine: signal logic, liquidity checks, holding windows, quality tiers, readiness, and trading-cost assumptions.

---

## Phase 6 — Analyst Accountability Scoreboard

Purpose:
Track analyst calls against actual outcomes so research becomes more accountable and useful.

MVP name:
Research Call Tracker

Do not launch a public “Top Analyst” leaderboard immediately.

Initial language:

> We are tracking research calls for transparency. Public rankings will appear once enough calls are available.

Analyst call schema:
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

---

## Phase 7 — Market Intelligence Features

Purpose:
Add investor-facing data views suggested by product and partner discussions.

Features:
1. Dividend View
2. Earnings Scorecard
3. Performance vs Baseline
4. Float / Tradability View
5. Market Pulse

Important language constraints:
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

---

## Phase 8 — Monetization Packaging

Investor-facing packages:

### Free
- Basic Market Pulse
- Limited company pages
- Basic education
- Account-opening guide
- Limited research index

### Premium
- Full company research summaries
- Dividend View
- Earnings Scorecard
- Watchlists
- Weekly market insights
- Saved companies
- Limited analyst call history

### Pro
- Advanced filters
- Portfolio planning
- Analyst scoreboard
- Exports
- Deeper research archive
- Advanced company comparisons

### Diaspora Investor Pack
- JSE investing guide
- Broker access flow
- Account-opening checklist
- Dividend/income education
- Company research pack
- Market orientation guide

Institution-facing packages:
- Lead Referral Package
- Account Opening Package
- Funded Account Package
- Research Distribution Package
- White-label Education Package

Disclosures required:
- whether content is sponsored
- whether a broker paid for placement
- whether a referral fee may be earned
- JSE Market Lab does not provide personal investment advice
- users should review fees, risks, and requirements directly with the institution

---

## Phase 9 — Documentation and Operating System

Purpose:
Create the internal documents needed to guide future build chats, protect the product direction, and support the portfolio story.

Documents to maintain:
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

## Build Priority

### First
- Continue Sprint 18A readiness-gate research layer
- Continue richer market scraper work
- Send JSE data/licensing email
- Send FSC/legal compliance query
- Create Broker Referral Revenue Model doc
- Create Research Hub MVP structure
- Create Brokerage Access Flow spec

### Second
- Build FastAPI backend foundation
- Keep Streamlit running during migration
- Add soft CTA prototype only after compliance language is validated
- Start manual broker/advisor research
- Start research index manually
- Define analyst scoring methodology before public leaderboard

### Third
- Build Company Pages
- Build Market Pulse
- Add Dividend View
- Add Earnings Scorecard
- Add Float / Tradability View

### Later
- Launch broker referral pilot
- Launch paid subscription
- Launch analyst profiles
- Launch public analyst leaderboard only after enough data
- Add AI-assisted explanation workflows after structured outputs and guardrails are stable

---

## Notes

- Backlog reflects priority order based on trust, usability, compliance, and platform scalability
- Risk-exit logic must be backtested before it becomes user-facing guidance
- Readiness gating must be tested before it affects funding eligibility
- AI context should be source-grounded and should not become a recommendation engine
- User profile features require persistence and privacy decisions before implementation
- Broker/referral workflows require JSE/FSC/legal/compliance validation before launch
