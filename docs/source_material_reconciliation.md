# Source Material Reconciliation — JSE Market Lab

## Purpose

This document reconciles the project source material, current repo docs, and new Phase 3–9 platform pathway so future chats and build work do not lose context.

Use this document when deciding which project sources to keep, archive, replace, or edit.

---

## Current Strategic State

JSE Market Lab is now evolving from a Streamlit-first JSE decision dashboard into a broader platform:

- decision-support dashboard
- market intelligence layer
- research hub
- company pages
- brokerage-access guidance
- analyst accountability tracker
- dividend and earnings views
- AI-assisted explanation workflows
- subscription / referral / research-distribution monetization

The dashboard remains the decision engine.

The expanded platform must remain decision-support only:

- no personal investment advice
- no buy/sell instructions
- no guaranteed outcomes
- no trade execution
- no holding client funds
- no hidden sponsored content or referral incentives
- no hosting third-party research without permission/licensing

---

## Project Sources Reviewed

### 1. `product_context.md`

Status:
- Useful but now incomplete.

What it covers well:
- core engine
- median crossover signals
- ranking logic
- holding windows
- portfolio logic
- execution layer
- review layer
- Ticker Analysis
- Guided vs Advanced structure
- trading costs

What needs editing:
- Add Trade Readiness from Sprint 17
- Add Sprint 18 readiness-gating research
- Add richer market data / scraper direction
- Add platform expansion: Research Hub, Company Pages, Brokerage Access, Market Intelligence
- Add architecture migration to FastAPI/Next.js
- Add AI as future explanation workflow, not prediction engine

Recommendation:
- Replace or update with a new version that references the platform roadmap.
- Keep the current content but move it under “Decision Engine Foundation.”

---

### 2. `strategy_context.md`

Status:
- Useful but now too narrow.

What it covers well:
- decision-support positioning
- target users
- short/mid/long-term goals
- communication strategy
- user behavior shift from guessing to structured evaluation

What needs editing:
- Expand target users to include Caribbean and diaspora investors
- Add research, company pages, account-opening education, and market intelligence
- Add monetization paths
- Add compliance validation with JSE/FSC/legal counsel
- Add institution-facing partnerships

Recommendation:
- Update, do not delete.
- It should become the high-level business/product strategy source.

---

### 3. `ux_learnings.md`

Status:
- Still useful and mostly current.

What it covers well:
- product identity confusion
- capital input confusion
- system behavior clarity
- tab flow expectations
- Guided/Advanced distinction
- Ticker Analysis as a strong entry point

What needs editing:
- Add Trade Readiness user confusion: funded vs incomplete readiness
- Add brokerage CTA caution: avoid users thinking CTA is advice
- Add Company Pages / Research Hub UX principles
- Add mobile-first workflow expectations for new frontend
- Add need for source/date/rights visibility in research surfaces

Recommendation:
- Update after Phase 3–9 docs settle.
- Keep as UX evidence source.

---

### 4. `jse_project_master_context.md`

Status:
- Very important but now needs a major refresh.

What it covers well:
- project identity
- core product goal
- decision-support philosophy
- core system flow
- dashboard capabilities
- strategy concepts
- trading costs
- sprint history context

What needs editing:
- Add Phase 3–9 platform strategy
- Add architecture migration track
- Add data foundation split: market_prices, ticker_master, events_news
- Add brokerage-access and compliance boundaries
- Add Research Hub / Company Pages / Market Intelligence
- Add AI product direction and guardrails
- Add current sprint sequence after Sprint 17/18

Recommendation:
- This should be replaced with a new master context file for future project chats.
- Keep the old version as archive if desired, but do not rely on it as the only source.

---

### 5. `AI-Product-Trajectory-Source-Document---JSE-Market-Lab.txt`

Status:
- Still highly relevant.

What it covers well:
- AI Product Manager / Product Ops positioning
- responsible AI feature selection
- AI guardrails
- AI evaluation thinking
- AI architecture principles
- use cases such as data quality assistant, signal explanation assistant, portfolio rationale assistant, trade readiness assistant, event/news risk assistant, weekly market insight assistant

What needs editing:
- Add new Phase 3–9 platform surfaces as future AI contexts
- Add Research Hub / Company Pages as structured data sources for AI
- Add events_news.csv and ticker_master.csv as AI grounding sources
- Add broker-access guardrails: AI must not recommend brokers or guide investment decisions
- Add monetization / sponsored-content disclosure guardrails

Recommendation:
- Keep and update later.
- This remains the AI portfolio positioning source.

---

### 6. `deep-research-report.md`

Status:
- Useful as product management / marketing reference material, not app-specific source-of-truth.

What it covers well:
- product ownership practice
- positioning
- product-market fit
- marketing channels
- monetization thinking
- trust/compliance themes

What needs editing:
- No urgent edit required unless it is being used as project-specific build context.
- It should be treated as a reference library, not a current product spec.

Recommendation:
- Keep as reference source.
- Do not use it as implementation priority unless a decision is explicitly pulled into product docs.

---

### 7. `Sprint 7 Execution.txt` / Phase two sprint breakdown

Status:
- Historical and partially outdated.

What it covers well:
- Phase 2 framing
- UI clarity
- Guided vs Advanced structure
- Sprint 13–15 thinking
- early usability direction

What needs editing:
- It should not remain a current sprint map.
- Current sprint map is now in `docs/backlog.md` and Phase 3–9 docs.

Recommendation:
- Archive as historical context.
- Do not use as current roadmap.

---

### 8. `Pasted text.txt` / Phase 3–9 pathway

Status:
- Newly incorporated into repo docs.

What it covers:
- Brokerage Access Flow
- Research Hub
- Company Pages
- Analyst Accountability Scoreboard
- Market Intelligence Features
- Monetization Packaging
- Documentation and Operating System
- build priority
- strategic summary for future chats

Repo action taken:
- Incorporated into `docs/backlog.md`
- Incorporated into `docs/product_decisions.md`
- Incorporated into `docs/feature_breakdown.md`
- Created `docs/phase_3_9_platform_strategy.md`
- Created `docs/compliance_disclosure_playbook.md`

Recommendation:
- Keep the pasted file as an archived source, but rely on the repo docs as the maintained version.

---

## Repo Docs Now Acting as Source of Truth

### Updated docs

- `docs/backlog.md`
- `docs/product_decisions.md`
- `docs/feature_breakdown.md`
- `docs/market_data_requirements.md`

### New docs

- `docs/phase_3_9_platform_strategy.md`
- `docs/compliance_disclosure_playbook.md`
- `docs/source_material_reconciliation.md`

---

## Project Sources That Should Be Edited or Replaced

### Highest priority to update

1. `jse_project_master_context.md`
2. `product_context.md`
3. `strategy_context.md`

These are likely to mislead future chats if they remain dashboard-only.

### Medium priority to update

4. `ux_learnings.md`
5. `AI-Product-Trajectory-Source-Document---JSE-Market-Lab.txt`

These are still useful but need Phase 3–9 context added.

### Archive / historical

6. `Sprint 7 Execution.txt`
7. `Phase two sprint breakdown`

These should be treated as historical Phase 2 context, not current roadmap.

### Reference only

8. `deep-research-report.md`
9. Product Ownership / Product Management PDF

These are useful for product/marketing thinking but should not override project-specific docs.

---

## Recommended Project Source Replacement Strategy

If the ChatGPT Project allows source management, replace or add these updated source docs:

1. `phase_3_9_platform_strategy.md`
2. `source_material_reconciliation.md`
3. `compliance_disclosure_playbook.md`
4. updated `backlog.md`
5. updated `product_decisions.md`
6. updated `feature_breakdown.md`
7. updated `market_data_requirements.md`

Then either archive or de-prioritize:

- old Sprint 7/Phase 2-only execution files
- any old source that says the product is only a dashboard without mentioning the platform expansion

---

## Future Chat Opening Context

Use this when moving to another chat:

> JSE Market Lab has evolved from a JSE trading dashboard into a market intelligence, research, decision-support, education, brokerage-access, and monetization platform for Jamaican, Caribbean, and diaspora investors. The dashboard remains the decision engine, while the expanded platform adds Research Hub, Company Pages, Market Pulse, Dividend View, Earnings Scorecard, Float/Tradability View, Analyst Call Tracker, Brokerage Access Flow, and future AI-assisted explanation workflows. The product remains decision-support only and must not provide personal investment advice, guarantee outcomes, recommend buy/sell actions, execute trades, or hold client funds. Compliance validation is needed with JSE/FSC/legal counsel before broker referral, research hosting, analyst scoring, or sponsored monetization features go live.

---

## Build Direction After Reconciliation

Immediate priorities:

1. Continue Sprint 18A readiness-gate research.
2. Continue richer market scraper work.
3. Continue FastAPI backend foundation for architecture migration.
4. Keep Streamlit working during migration.
5. Use Phase 3–9 docs for strategy, not immediate implementation unless compliance and data foundations are ready.

Do not jump directly into broker referral or paid research features until:
- JSE data rights are clarified
- FSC/legal boundaries are clarified
- consent/disclosure flow is reviewed
- research hosting rights policy is operationalized
- source-grounding and auditability are stable
