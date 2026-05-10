# GitHub Product Management Setup — JSE Market Lab

## Purpose

This document defines how GitHub should be used as the product management workspace for JSE Market Lab.

JSE Market Lab is now more than a code repository. It is a live product build with frontend, backend, decision-engine, market-data, education, compliance, monetization, and future AI workstreams.

GitHub should help track:

- strategy decisions
- sprint scope
- implementation work
- research tasks
- compliance gates
- product risks
- roadmap priorities
- release notes
- advisor/demo readiness

---

## Current Product Stage

The Vercel migration foundation is complete.

Current architecture:

```text
Vercel Next.js frontend
        ↓
Render FastAPI backend
        ↓
Existing Python decision engine / data layer
```

Completed foundation:

- FastAPI backend foundation
- Next.js frontend foundation
- Vercel deployment
- Render backend deployment
- API-backed homepage data status
- API-backed Portfolio Plan
- API-backed Ticker Analysis
- API-backed Decision Audit
- mobile/desktop page polish
- expanded platform architecture document

The next product-management priority is to organize the roadmap before deeper features are added.

---

## Recommended GitHub Project

Create a GitHub Project named:

```text
JSE Market Lab Product Roadmap
```

This project should track all product, technical, research, and compliance work.

### Recommended Status Columns

```text
Inbox
Ready
In Progress
In Review
Merged / Done
Blocked
Later
```

### Recommended Custom Fields

```text
Phase
Priority
Workstream
Risk level
Compliance gate
Target milestone
```

### Suggested Field Values

#### Phase

```text
Migration
Trust & Cost Alignment
Platform Shell
Demo / Mockup
Data Foundation
Profiles & Simulation
Market Intelligence
AI Helper
Brokerage / Monetization
```

#### Priority

```text
P0 — urgent / blocker
P1 — important next
P2 — planned
P3 — later
```

#### Workstream

```text
Frontend
Backend
Data
Product
UX
Compliance
AI
Monetization
Research
Documentation
```

#### Risk level

```text
Low
Medium
High
Compliance-sensitive
```

#### Compliance gate

```text
None
Needs language review
Needs JSE validation
Needs FSC/legal validation
Needs broker/legal validation
Blocked until approved
```

---

## Recommended Milestones

### M1 — Vercel Migration Foundation

Status: mostly complete.

Scope:

- FastAPI backend foundation
- Next.js frontend foundation
- Vercel deployment
- Render backend deployment
- API-backed Portfolio/Ticker/Review pages
- frontend polish

Related PRs:

- #132 Backend API foundation
- #133 Next.js frontend foundation
- #135 Vercel-safe API configuration
- #139 Platform architecture and hosting decision
- #140 Render deployment prep
- #141 API-backed frontend pages
- #142 API-backed frontend polish

### M2 — Trust & Cost Alignment

Scope:

- cost-profile alignment
- broker fee research table
- neutral cost estimates
- custom fee slider concept
- clear cost disclosure language
- API/frontend cost-profile consistency

Primary issue:

- #150 Align broker fee and CESS cost profiles

### M3 — Platform Navigation Shell

Scope:

- stronger Start Here page
- CTA map
- page-to-page guidance
- platform preview navigation
- user journey structure
- beginner/analyst path clarity

### M4 — Demo / Mockup Experience

Scope:

- demo mode banner
- advisor walkthrough path
- platform preview page
- future-surface mockups
- data rights / authorization note
- safe demo wording before JSE authorization

Primary issue:

- #149 Create demo / mockup mode

### M5 — Data Foundation

Scope:

- ticker master
- company metadata
- source/date fields
- market-data lineage
- events/news structure
- research index structure
- dividend and earnings data contracts

### M6 — Profiles & Simulation

Scope:

- auth/database decision
- user profile schema
- watchlists
- setup tester
- paper portfolio
- decision review history
- consent/disclosure tracking

Primary issue:

- #136 User profiles and setup testing / paper portfolio workflows

### M7 — Market Intelligence MVP

Scope:

- Research Hub
- Company Pages
- Market Pulse
- Dividend View
- Earnings Scorecard
- Float / Tradability View
- Analyst Call Tracker

### M8 — AI Helper Foundation

Scope:

- AI helper product spec
- navigation-only prototype
- grounding/context tools
- guardrails
- evaluation plan
- safe CTA logic

Primary issue:

- #137 AI helper for navigation, explanations, and grounded insights

### M9 — Brokerage Access / Monetization

Scope:

- brokerage-access education flow
- compliance-approved referral model
- premium research/education tiers
- sponsor disclosure rules
- diaspora investor pack
- payment/subscription design

This milestone should remain blocked until JSE/FSC/legal/commercial validation is clearer.

---

## Recommended Labels

### Type Labels

```text
type: docs
type: frontend
type: backend
type: data
type: product
type: compliance
type: ai
type: monetization
type: research
type: ux
type: bug
type: tech-debt
```

### Status Labels

```text
status: needs-review
status: blocked
status: ready
status: in-progress
status: validated
```

### Phase Labels

```text
phase: migration
phase: trust
phase: platform-shell
phase: demo
phase: data-foundation
phase: profiles
phase: intelligence
phase: ai
phase: monetization
```

### Risk Labels

```text
risk: low
risk: medium
risk: high
risk: compliance-sensitive
```

---

## Issue Workflow

### 1. Inbox

Use for raw ideas, chat captures, research links, and unsorted opportunities.

### 2. Ready

Move here only when the issue has:

- clear goal
- scope
- acceptance criteria
- guardrails
- relevant milestone or phase

### 3. In Progress

Move here once a branch or active task starts.

### 4. In Review

Move here when a PR is open or a doc/spec needs review.

### 5. Merged / Done

Move here when the PR is merged or the issue is closed as completed.

### 6. Blocked

Use when a task depends on:

- JSE authorization
- FSC/legal review
- broker confirmation
- missing data
- unresolved product decision
- dependency setup

### 7. Later

Use for good ideas that should not distract the current build phase.

---

## PR Workflow

Every PR should include:

- summary
- what changed
- how to test
- product guardrails
- what is out of scope
- related issue(s)

Example:

```text
Closes #150
Related to #149
```

For compliance-sensitive work, the PR should explicitly say whether the change is:

```text
internal only
public-facing
demo-only
compliance-gated
```

---

## Issue Template Usage

Use these templates:

- Feature Spec
- Bug Report
- Research Task
- Compliance Review
- UX Improvement
- Technical Debt
- Sprint Closeout

Each issue should be written so a future ChatGPT/Codex session can continue without needing the full chat history.

---

## Roadmap Guardrails

The product must remain:

- decision-support only
- non-advisory
- non-executional
- transparent about data limitations
- clear about demo/mockup status before authorization
- explicit about cost assumptions
- careful with broker/referral language

The platform must not:

- recommend buy/sell actions
- guarantee outcomes
- predict future prices as certainty
- execute trades
- hold client funds
- recommend a broker as best
- imply official JSE authorization before confirmed
- publish broker fee data without source/verification status

---

## Immediate Operating Plan

### Next 3 work items

1. Complete GitHub product management setup.
2. Build demo/mockup mode for advisor walkthroughs.
3. Align cost profiles across engine/API/frontend/docs.

### Near-term build order

```text
M2 — Trust & Cost Alignment
M4 — Demo / Mockup Experience
M3 — Platform Navigation Shell
M5 — Data Foundation
M6 — Profiles & Simulation
```

The order may shift slightly, but compliance-sensitive features should not jump ahead of trust/data foundations.

---

## Product Management Rule

Every new idea should become one of the following:

```text
Issue
PR
Doc
Milestone
Project card
```

If it is not tracked, it is not part of the roadmap yet.
