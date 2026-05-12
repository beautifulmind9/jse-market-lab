# Current Platform Status — JSE Market Lab

## Purpose

This document summarizes the current state of JSE Market Lab after the recent platform expansion work.

It is intended to be a source of truth for:

- what exists now
- what is demo/mockup vs working
- what remains future work
- what needs JSE/FSC/legal/compliance validation
- which open GitHub issues should stay open, close, merge, or be reframed

---

## Current Product Positioning

JSE Market Lab has evolved from a trading dashboard into a broader platform for:

- Jamaican market intelligence
- company research entry points
- decision-support tools
- investor education
- demo-safe product walkthroughs
- future setup testing and paper portfolio workflows
- future AI-assisted platform guidance and public-source research
- future income/dividend context
- future brokerage-access education

The product remains decision-support only.

It must not:

- provide personal investment advice
- recommend buy/sell actions
- guarantee outcomes
- recommend a broker as best
- execute trades
- hold client funds
- imply official live JSE feed access before authorization
- imply JSE/FSC approval before confirmed

---

## Current Architecture

```text
Next.js frontend on Vercel
        ↓
FastAPI backend on Render
        ↓
Existing Python decision engine
        ↓
Demo/internal/generated JSE market dataset
```

Current public frontend surfaces are Next.js pages.

Current backend API exposes structured decision-support JSON for data status, portfolio planning, ticker analysis, and decision audit.

Streamlit may still exist in the repo/history, but the active product direction is the Vercel + FastAPI architecture.

---

## Current Frontend Pages

## Homepage `/`

Status: working / demo-safe market-front page

Current behavior:

- market snapshot appears first
- demo/internal labels are visible
- market board style gives immediate information from the first screen
- user-intent paths route to Learn, Market, Companies, Tools, Income, Research, and Demo
- decision-support notice remains visible

Data status:

- API-backed where configured
- polished demo fallback if API is unavailable or missing
- clearly not an official live JSE feed

---

## Market `/market`

Status: working demo Market Pulse page

Current behavior:

- demo/internal market tape
- Market Pulse lede panel
- Pulse Board with signal clusters
- market movers mockup
- liquidity watch
- latest market notes
- next-step guidance into Companies and Tools
- demo/internal disclaimer

Future direction:

- connect to real market summary endpoint
- add actual gainers/decliners/most active when data source supports it
- add market breadth and sector view later

---

## Companies `/companies`

Status: working demo company research entry page

Current behavior:

- demo/internal company research status tape
- company research lede panel
- Research Board
- sample company cards
- links into existing ticker analysis pages
- company-page module previews
- research flow guidance
- demo/internal company research disclaimer

Future direction:

- true company pages by ticker
- dividend context by ticker
- earnings scorecard
- float/tradability view
- official source links and research notes after rights/compliance validation

---

## Tools `/tools`

Status: working decision-support hub

Current behavior:

- decision-support status tape
- Tools hub lede panel
- Tool Board
- working tools clearly separated from future tools
- links to Portfolio Plan, Ticker Analysis, and Decision Audit
- future Setup Tester, Paper Portfolio, and AI Helper previews
- cost assumptions panel
- responsible-use checklist
- decision-support disclaimer

Future direction:

- Setup Tester
- Paper Portfolio
- saved setup workflows
- user profile/practice settings
- deeper cost assumptions and broker-fee range controls

---

## Portfolio Plan `/portfolio`

Status: working API-backed page

Current behavior:

- consumes portfolio planning API
- shows funded and unfunded setups
- exposes cost profile assumptions
- keeps neutral/non-broker-preference cost language
- uses decision-support framing

Future direction:

- editable capital/settings UX
- user profile connection
- setup saving
- simulated position tracking

---

## Ticker Analysis `/ticker/[ticker]`

Status: working API-backed page

Current behavior:

- displays ticker-level decision-support context
- links from company cards and helper shell
- used as the current working substitute for future company pages

Future direction:

- integrate into full company pages
- add dividend, earnings, tradability, and source-link context
- allow richer search/select ticker behavior

---

## Review `/review`

Status: working API-backed Decision Audit page

Current behavior:

- explains how rules affected portfolio outputs
- supports review and rationale rather than blind action

Future direction:

- connect to saved setup tests
- compare user-planned vs system-reviewed rationale
- monthly review workflows

---

## Learn `/learn`

Status: working educational landing page

Current behavior:

- introduces core education topics
- links to sample ticker and tools
- beginner-friendly direction

Future direction:

- full learning guide
- glossary pages
- quizzes or micro-lessons
- diaspora investor path

---

## Income `/income`

Status: demo/future landing page

Current behavior:

- explains dividend/income context direction
- labels modules as future

Future direction:

- Dividend View
- dividend calendar
- company income profile
- portfolio income estimate

---

## Research `/research`

Status: demo/future landing page with compliance caution

Current behavior:

- frames Research Hub direction
- clearly warns that research hosting and source redistribution need validation

Future direction:

- Research Hub
- company notes
- market notes
- source/date tracking
- public-source search support through AI Helper later

---

## Demo `/demo` and Platform Preview `/platform-preview`

Status: working demo/advisor surfaces

Current behavior:

- supports advisor/partner walkthroughs
- shows future modules as platform preview
- demo language remains clear

Future direction:

- more polished advisor walkthrough
- compliance/data access roadmap page
- monetization path page

---

## AI Helper

Status: working shell MVP

Implemented:

- persistent floating `Guide Me` button
- page-aware helper panel
- route-specific guidance
- suggested questions
- helpful links
- future research mode note
- decision-support disclaimer

Current limitation:

- rule-based only
- no live AI calls
- no internet search
- no API calls from helper
- no user profile/memory behavior

Source of truth:

```text
docs/ai_helper_definition.md
```

Future stages:

1. platform retrieval from docs/glossary/methodology
2. safe internet research mode with citations
3. user profile/practice settings integration
4. deeper AI explanation workflows

---

## Data and Compliance Status

Current status:

- demo/internal/latest-available dataset used for product demonstration
- Render backend is API-backed
- Vercel frontend is live
- official JSE data/API authorization remains pending
- compliance validation remains needed before public claims, broker referral, paid research, sponsored content, or official data integrations

Required language:

```text
Demo/internal/latest-available data
Not an official live JSE feed
Decision support only
Not investment advice
Actual broker fees may vary
Confirm official information with JSE/FSC/company/broker sources
```

---

## Current Open Issue Review

This review is based on the open issues available after PR #169 was merged.

## Recommended Issue Actions

| Issue | Title | Status Review | Recommended Action |
|---|---|---|---|
| #120 | Backlog: exit stop logic and downside risk exits | Still valid future risk-control work. | Keep open. Later roadmap under readiness/risk controls. |
| #125 | Backlog: require trade-readiness completeness before funding | Still valid, but overlaps with #126. | Keep open or merge into #126 after research scope is finalized. |
| #126 | Sprint 18: Readiness Gating Research & Risk Control Design | Still valid as research/design sprint. | Keep open. Strong candidate for next engine/risk research sprint. |
| #130 | Architecture migration: Next.js frontend on Vercel + FastAPI backend | Largely completed by Vercel/Render/API-backed frontend work. | Candidate to close after confirming no remaining migration checklist items. |
| #131 | Sprint: Backend API Foundation for Vercel migration | Largely completed. Health/data/portfolio/ticker/review endpoints exist and have tests. | Candidate to close after confirming backend API test coverage remains current. |
| #136 | Add user profiles and setup testing / paper portfolio workflows | Still valid major future product track. | Keep open. Needs breakdown into profile, database, setup tester, paper portfolio, review workflows. |
| #137 | Define AI helper for platform navigation, explanations, and grounded insights | Superseded by #166 / PR #167 and implemented shell in PR #169. | Candidate to close as superseded/completed, linking to `docs/ai_helper_definition.md` and PR #169. |
| #138 | Explore future gamification for guided investor education and retention | Still valid future engagement/education research. | Keep open as later exploration, after profiles/simulation foundation. |
| #143 | Set up GitHub product management workflow for JSE Market Lab roadmap | Duplicate/older version of #148. | Candidate to close as duplicate of #148. |
| #144 | Create demo/mockup mode for product demos before official JSE API authorization | Duplicate/older version of #149, and much has been implemented. | Candidate to close as duplicate or partially completed under #149. |
| #145 | Align cost profiles for broker fee and CESS assumptions | Largely completed by cost profile work and PR #154. | Candidate to close after confirming docs and frontend cost displays are satisfactory. |
| #147 | Business ops: resolve public brand name and JSE attribution approach | Still valid and important. | Keep open. This is compliance/brand risk work before major outreach. |
| #148 | Set up GitHub product management workflow for JSE Market Lab roadmap | Still valid. | Keep open. Needs project board/milestones/templates/labels work. |
| #149 | Create demo / mockup mode for advisor and partner walkthroughs before JSE authorization | Partially completed by demo banner, homepage market snapshot, Market/Companies/Tools, AI Helper shell. | Keep open until demo/advisor walkthrough and data-status fields are fully consolidated. |
| #153 | Research market-data UI patterns and user behavior for JSE Market Lab design direction | Still valid. The first design iteration used CNBC/Bloomberg inspiration, but formal research doc not done. | Keep open. Recommended next doc/research task. |
| #166 | Define AI Helper as persistent platform guide with safe web research mode | Completed by PR #167. | Should be closed automatically if PR linked correctly; otherwise close manually. |
| #168 | Add AI Helper shell with page-aware guidance | Completed by PR #169. | Should be closed automatically if PR linked correctly; otherwise close manually. |

---

## Issues That Can Likely Be Closed Soon

Recommended closure candidates after quick review:

```text
#130 Architecture migration
#131 Backend API Foundation
#137 AI helper definition, superseded by #166/#167
#143 duplicate of #148
#144 duplicate/older version of #149
#145 cost profile alignment
#166 AI Helper definition, completed
#168 AI Helper shell, completed
```

Do not close all blindly. For each, leave a short closing comment referencing the relevant PR/doc.

---

## Issues That Should Stay Open

```text
#120 exit stop logic and downside risk exits
#125 trade-readiness completeness before funding
#126 readiness gating research and risk-control design
#136 user profiles and setup testing / paper portfolio workflows
#138 gamification for education and retention
#147 brand name and JSE attribution approach
#148 GitHub product management workflow
#149 demo/mockup advisor walkthrough mode
#153 market-data UI research
```

---

## Recommended Next Roadmap Order

## 1. Clean GitHub product management

Recommended branch:

```text
chore/github-product-management-cleanup
```

Tasks:

- close/merge duplicate completed issues
- standardize labels
- create issue templates
- define milestones
- create or update product roadmap/project board

Why next:

The repo now has many product tracks. GitHub should become the operating system for the build.

---

## 2. Formal UI market-data research

Recommended branch:

```text
docs/ui-market-data-design-research
```

Tasks:

- document patterns from CNBC, Bloomberg, Yahoo Finance, TradingView, JSE, broker portals, etc.
- translate findings into JSE Market Lab page-template recommendations
- protect against copying while learning from the information hierarchy

Why next:

The platform now has market-front pages. Formal research will guide better design iterations.

---

## 3. Demo/advisor walkthrough consolidation

Recommended branch:

```text
feature/demo-advisor-walkthrough
```

Tasks:

- create a polished guided demo flow
- show what is built vs future
- include data/compliance roadmap
- create advisor/partner-friendly path

Why next:

Useful for meetings with advisors, institutions, and potential partners.

---

## 4. Profiles and simulation planning

Recommended branch:

```text
docs/profiles-simulation-architecture
```

Tasks:

- split #136 into database/auth/profile/setup tester/paper portfolio issues
- define user practice settings
- define data model
- define safety language

Why next:

Setup Tester and Paper Portfolio are major product pillars and require careful design before code.

---

## 5. Readiness/risk control research

Recommended branch:

```text
docs/readiness-risk-control-research
```

Tasks:

- scope #126
- define readiness gates
- define risk-control candidates
- define backtest comparison plan

Why next:

Before more advanced simulation, the engine should have a clearer risk-control research path.

---

## Current Product Summary

JSE Market Lab now has a credible platform shell:

```text
Homepage market snapshot
→ Market Pulse
→ Companies research entry
→ Tools decision-support hub
→ Portfolio/Ticker/Review engine pages
→ AI Helper guidance layer
```

The platform is still demo/internal-data based and compliance-gated, but it is now structured like a real market intelligence and decision-support product rather than a standalone dashboard.

---

## Immediate Recommendation

After this doc is merged:

1. Close or mark completed duplicate issues.
2. Keep core future roadmap issues open.
3. Build GitHub product-management structure next.
4. Then continue with either UI research or demo/advisor walkthrough.
