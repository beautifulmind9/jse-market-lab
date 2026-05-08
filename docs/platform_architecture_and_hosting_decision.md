# Platform Architecture and Hosting Decision — JSE Market Lab

## Purpose

This document connects the Vercel/FastAPI migration to the expanded JSE Market Lab platform strategy.

JSE Market Lab is no longer only a trading dashboard. It is evolving into a market intelligence, research, decision-support, education, brokerage-access, simulation, and monetization platform for Jamaican, Caribbean, and diaspora investors.

The dashboard remains the decision engine. The platform around it will add Research Hub, Company Pages, Market Pulse, Dividend View, Earnings Scorecard, Float / Tradability View, Analyst Call Tracker, Brokerage Access Flow, User Profiles, Setup Tester / Paper Portfolio, and future AI-assisted explanation workflows.

This document should guide backend hosting, database, storage, and platform architecture decisions before more infrastructure is deployed.

---

## Current State

Completed migration work:

- FastAPI backend foundation exists.
- Initial backend endpoints exist:
  - `GET /health`
  - `GET /api/data/status`
  - `POST /api/portfolio/plan`
  - `GET /api/ticker/{ticker}/analysis`
  - `GET /api/review/decision-audit`
- Next.js frontend exists in `frontend/`.
- Vercel frontend deployment is live.
- Frontend can deploy without a hosted backend.
- `NEXT_PUBLIC_API_BASE_URL` is reserved for the future hosted API URL.
- Streamlit remains available during migration.

Current architecture:

```text
Vercel
Next.js frontend shell
        ↓
Local / future hosted FastAPI backend
        ↓
Existing Python decision engine
        ↓
Local/demo/generated data
```

---

## Target Platform Architecture

Longer-term target:

```text
Vercel Frontend
  Next.js platform UI
  public pages
  logged-in user areas
  education flows
  research/company pages
  setup testing UI
  AI helper interface
        ↓
FastAPI Backend
  decision-engine APIs
  market intelligence APIs
  research APIs
  company APIs
  user profile APIs
  simulation/paper portfolio APIs
  broker-access APIs, compliance-gated
  AI helper context APIs
        ↓
Database / Storage Layer
  market prices
  ticker master
  events/news
  research index
  company metadata
  user profiles
  saved watchlists
  saved setups
  simulated positions
  decision review history
  broker leads, compliance-gated
  AI helper logs/evaluations
        ↓
External / Controlled Inputs
  JSE data sources or licensed feeds
  company filings and public notices
  research links / licensed content
  broker partner data, if approved
  future AI provider, if approved
```

---

## Platform Boundary

JSE Market Lab provides:

- educational market context
- historical market analysis
- decision-support tools
- research discovery
- company context
- portfolio planning support
- trade readiness context
- simulated setup testing
- paper portfolio / decision practice workflows
- account-opening education
- referral/routing workflows to licensed institutions, only if approved

JSE Market Lab does not:

- provide personal investment advice
- recommend buy/sell actions
- guarantee outcomes
- predict future prices
- execute trades
- open brokerage accounts directly
- hold client funds
- act as a broker-dealer
- recommend a specific broker as best
- route users to brokers based on a simulated trade result

---

## Architecture Principles

### 1. Keep Vercel focused on frontend experience

Vercel should own:

- public marketing/product pages
- dashboard interface
- Research Hub UI
- Company Pages UI
- Market Pulse UI
- Setup Tester / Paper Portfolio UI
- onboarding and education flows
- AI helper chat/interface surface

Vercel should not own:

- long-running scraping jobs
- heavy Python computation
- secure backend decision logic
- database-heavy operations
- broker lead processing logic
- AI context retrieval and guardrail evaluation

### 2. Keep FastAPI as the platform service layer

FastAPI should own:

- decision engine API
- portfolio planning API
- ticker analysis API
- research and company data API
- setup testing and simulation API
- paper portfolio API
- user profile API
- market intelligence API
- AI helper tool/context API
- compliance-gated broker access API

### 3. Use a real database before user accounts

User profiles, saved setups, watchlists, simulations, research saves, and broker leads require persistent storage.

Do not add real user accounts until the database model and privacy/security posture are clear.

### 4. Keep compliance-gated features separated

Brokerage Access Flow, broker referrals, sponsored placements, paid research distribution, analyst scoring, and public AI helper outputs should remain behind explicit gates until reviewed.

### 5. Prefer boring, clear infrastructure first

The platform should avoid over-engineering in the early hosted phase. Use infrastructure that is simple, inspectable, and easy to explain in a product/implementation case study.

---

## Backend Hosting Options

### Option A — Render

Best for:

- simple FastAPI deployment
- GitHub-connected backend service
- low-friction public API hosting
- early beta and portfolio demonstration

Pros:

- straightforward mental model
- Python/FastAPI friendly
- easy environment variables
- good fit for a single backend service
- simple to explain and maintain

Cons:

- low/free tiers may sleep
- background jobs and database scaling may require upgrades or additional services
- less flexible than infrastructure-heavy options

Fit for JSE Market Lab:

Strong first backend host for the current phase.

Recommended if the immediate goal is:

- host FastAPI publicly
- connect Vercel to backend
- keep infrastructure simple
- avoid distracting from product/platform design

### Option B — Railway

Best for:

- fast developer experience
- backend + database workflows
- quick iteration across app and Postgres services

Pros:

- smooth DX
- easy environment variable management
- convenient database/service setup
- good for early product iteration

Cons:

- usage-based costs require monitoring
- easy to leave services running without noticing cost growth
- less ideal if cost predictability is the priority

Fit for JSE Market Lab:

Good option if database and backend are moved together quickly, especially if speed matters more than cost predictability.

### Option C — Fly.io

Best for:

- Docker-based deployment
- regional control
- more advanced infrastructure needs

Pros:

- powerful
- flexible
- good for more serious infrastructure control
- useful if regional performance becomes important

Cons:

- more technical setup
- more operational responsibility
- likely overkill for the current beta/platform foundation stage

Fit for JSE Market Lab:

Good later, not first choice now.

### Option D — DigitalOcean App Platform

Best for:

- more production-oriented app hosting
- predictable cloud-provider path

Pros:

- stable platform
- predictable upgrade path
- good for apps that may later need broader cloud resources

Cons:

- more setup/ops than Render for the first hosted API
- may be more than needed at this stage

Fit for JSE Market Lab:

Viable later if the platform needs more managed infrastructure.

---

## Database and Storage Options

### Option A — Supabase

Best for:

- Postgres database
- authentication
- row-level security
- storage
- dashboard-based admin
- quick product iteration

Pros:

- strong fit for user profiles and saved objects
- authentication support can reduce custom auth work
- Postgres is suitable for structured platform data
- good dashboard/admin tooling
- supports future public/private data separation

Cons:

- requires careful security rules
- auth/RLS design must be done properly
- product can become dependent on Supabase patterns

Fit for JSE Market Lab:

Very strong candidate because the platform needs profiles, saved setups, watchlists, paper portfolios, research saves, and possibly role-based access.

### Option B — Neon Postgres

Best for:

- managed serverless Postgres
- clean database layer independent of auth provider

Pros:

- strong Postgres option
- good if auth is handled separately
- database can remain portable

Cons:

- auth/user-management must be solved elsewhere
- more pieces to connect manually

Fit for JSE Market Lab:

Good if the team wants a clean Postgres backend and separate auth provider.

### Option C — Railway Postgres

Best for:

- combined Railway app + database setup

Pros:

- convenient if backend is also on Railway
- fast to connect services

Cons:

- cost monitoring needed
- less separation between app platform and database vendor

Fit for JSE Market Lab:

Good if Railway is chosen as the backend host.

### Option D — Render Postgres

Best for:

- combined Render app + database setup

Pros:

- simple if backend is on Render
- fewer vendors to manage

Cons:

- may be less feature-rich for auth/product workflows than Supabase
- auth still needs separate planning

Fit for JSE Market Lab:

Good for simplicity if the first hosted version only needs backend + database without user auth immediately.

---

## Recommended First Architecture Decision

### Short-term recommendation

Use:

```text
Frontend: Vercel
Backend: Render
Database/Auth: Supabase, evaluated before profiles launch
```

Why:

- Vercel already works for the frontend.
- Render is the simplest first FastAPI backend host.
- Supabase is the strongest early candidate for profiles, saved setups, watchlists, paper portfolios, and future logged-in workflows.
- This split keeps each tool doing what it is good at.

Short-term architecture:

```text
Vercel Next.js frontend
        ↓
Render FastAPI backend
        ↓
Existing Python decision engine
        ↓
Demo/generated data first
        ↓
Supabase/Postgres later for profiles and saved platform data
```

### Why not database immediately?

The next infrastructure move should be backend hosting, but user-profile features should not be built until the data model, auth model, privacy rules, and compliance boundaries are documented.

Deploying the backend first lets the Vercel frontend connect to real API endpoints without forcing premature user-account design.

---

## Feature-to-Infrastructure Map

| Feature area | Needs frontend | Needs backend | Needs database | Needs compliance gate |
|---|---:|---:|---:|---:|
| Portfolio Plan | Yes | Yes | Later | No, if decision-support only |
| Ticker Analysis | Yes | Yes | Later | No, if decision-support only |
| Review / Decision Audit | Yes | Yes | Later | No, if decision-support only |
| Data Status | Yes | Yes | No | No |
| Research Hub | Yes | Yes | Yes | Yes, for hosting/rights |
| Company Pages | Yes | Yes | Yes | Yes, for source/data rights |
| Market Pulse | Yes | Yes | Yes | Yes, if public redistribution depends on JSE data |
| Dividend View | Yes | Yes | Yes | Yes, if public data rights unclear |
| Earnings Scorecard | Yes | Yes | Yes | Yes, if derived public summaries are unclear |
| Float / Tradability View | Yes | Yes | Yes | Yes, for source/data rights |
| Analyst Call Tracker | Yes | Yes | Yes | Yes |
| Brokerage Access Flow | Yes | Yes | Yes | Yes |
| User Profiles | Yes | Yes | Yes | Privacy/security review |
| Setup Tester | Yes | Yes | Yes | Compliance language review |
| Paper Portfolio | Yes | Yes | Yes | Compliance language review |
| AI Helper | Yes | Yes | Yes/logging later | Yes, before public launch |
| Gamification | Yes | Yes | Yes | Trust/compliance review |
| Subscriptions | Yes | Yes | Yes | Legal/payment/disclosure review |

---

## User Profiles, Setup Tester, and Paper Portfolio Architecture

These features are a future platform layer and should be treated as education, simulation, and decision practice.

### User Profile

Stores:

- user_id
- experience level
- focus area: dividends, short-term trading, medium-term trading, learning, mixed
- preferred holding windows
- simulated capital amount
- saved tickers
- saved setup rules
- learning progress
- consent/disclosure acknowledgements, if needed

### Setup Tester

Allows a user to test one simulated idea using actual historical JSE data.

Inputs:

- ticker
- entry date or signal date
- holding window
- simulated allocation amount
- strategy rule/setup type
- notes

Outputs:

- simulated entry reference price
- simulated exit/reference price
- gross return
- estimated costs using broker fee 0.50% and CESS 0.35%
- net simulated return
- JMD simulated profit/loss
- liquidity warning
- data completeness warning
- event/earnings/dividend context where available

### Paper Portfolio

Tracks simulated positions over time.

Fields:

- position_id
- user_id
- ticker
- entry date
- planned review date
- holding window
- simulated cost basis
- estimated current value
- net simulated P/L
- status: open / closed / reviewed
- reason entered
- reason closed
- lesson learned

Required language:

- simulated trade
- paper portfolio
- historical test
- setup test
- past performance does not guarantee future results
- no trade was executed
- this is decision support only

---

## AI Helper Architecture Implications

The AI helper should be a platform guide, explanation assistant, and grounded insight helper.

It should support:

- platform navigation
- dashboard explanations
- research/company context explanations
- data quality explanations
- setup tester and paper portfolio review
- weekly market insight summaries
- safe next-step CTAs

It must not:

- recommend stocks
- recommend brokers
- tell users to buy or sell
- predict future prices
- guarantee outcomes
- invent market facts
- hide missing data
- execute trades
- route users into brokerage access based on simulated trade performance

Preferred AI workflow:

```text
User question
  ↓
Intent classification
  ↓
Tool/function selection
  ↓
Structured platform data retrieval
  ↓
AI-generated explanation
  ↓
Guardrail/safety check
  ↓
User-facing response
  ↓
Feedback/evaluation logging
```

AI helper backend needs later:

- context retrieval endpoints
- prompt/response logging, with privacy controls
- guardrail tests
- evaluation cases
- source/date grounding
- user-facing disclosure language

Do not launch public AI helper until structured data, source-grounding, and safety tests are stable.

---

## CTA and Revenue-Aware Navigation Principle

The platform should guide users at every important angle so they are not lost.

Every major surface should answer:

1. What am I looking at?
2. Why does it matter?
3. What can I safely do next?
4. What part of the platform should I visit next?
5. Is there a revenue-supporting action that is appropriate here?

Revenue-aware navigation can point users toward:

- learning content
- saved watchlists
- Setup Tester
- Paper Portfolio
- Research Hub
- Company Pages
- Market Pulse
- Dividend View
- Earnings Scorecard
- premium research features
- account-opening education, if compliance-approved
- licensed institution contact flows, if compliance-approved

It must not point users toward:

- buying a specific stock
- selling a specific stock
- choosing a best broker
- treating a simulated setup as a real recommendation

---

## Gamification Architecture Implications

Gamification is future exploration only.

Good gamification should reward:

- learning
- review discipline
- reading disclosures
- checking data quality
- understanding costs
- reviewing liquidity
- recording decision rationale
- using simulation before real-world action

It should not reward:

- trading frequency
- real trade execution
- chasing signals
- profit-only outcomes
- beating other users
- broker selection based on nudges

Possible future features:

- onboarding progress
- learning paths
- badges/milestones
- careful review streaks
- simulated decision discipline score
- quizzes / micro-lessons
- safe challenge mode

Gamification should not be implemented before profiles, database, compliance language, and trust guardrails are stable.

---

## Backend Deployment Plan

### Step 1 — Prepare backend for hosting

Add or verify:

- backend start command
- CORS settings for Vercel domain
- environment variable handling
- health endpoint
- requirements file compatibility
- safe error handling
- no dependency on local-only files unless bundled or configured

Expected start command:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Step 2 — Deploy FastAPI backend

Recommended first host:

```text
Render
```

Deploy as a web service connected to GitHub.

### Step 3 — Verify hosted API

Test:

- `/health`
- `/api/data/status`
- `/api/portfolio/plan`
- `/api/ticker/{ticker}/analysis`
- `/api/review/decision-audit`

### Step 4 — Connect Vercel to backend

Add in Vercel project settings:

```text
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend-url
```

Then redeploy Vercel.

### Step 5 — Replace placeholder frontend pages

After backend is hosted:

- connect Data Status card to hosted backend
- connect Portfolio page to API
- connect Ticker page to API
- connect Review page to API

Do not build Research Hub, Profiles, Paper Portfolio, Brokerage Access, or AI Helper until data/compliance/storage foundations are ready.

---

## Immediate Recommendation

Proceed in this order:

1. Merge this architecture decision doc.
2. Create a backend deployment prep branch.
3. Add CORS and Render deployment configuration.
4. Deploy FastAPI backend on Render.
5. Add hosted backend URL to Vercel as `NEXT_PUBLIC_API_BASE_URL`.
6. Confirm Vercel frontend can read hosted `/api/data/status`.
7. Only then begin replacing placeholder pages with API-backed UI.
8. Start separate database/auth decision before building profiles, setup tester, paper portfolio, research saves, or AI helper.

---

## Open Decisions

1. Confirm backend host: Render first, unless a stronger reason emerges.
2. Confirm database/auth stack: likely Supabase, but not final.
3. Decide whether research index starts as static/CSV/manual admin or database table.
4. Decide how market data is legally stored, transformed, displayed, and refreshed.
5. Confirm JSE data rights and redistribution limits.
6. Confirm FSC/legal boundaries for broker referral and research scoring.
7. Define privacy and consent requirements before user accounts.
8. Define AI helper evaluation plan before public AI launch.

---

## Product Rule

When in doubt, choose the architecture that preserves trust, auditability, compliance review, and user agency.

JSE Market Lab should earn revenue by helping users understand, test, save, compare, learn, and connect with licensed institutions where appropriate — not by pushing trades, hiding incentives, or overstating certainty.
