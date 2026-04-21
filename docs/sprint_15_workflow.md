# Sprint 15 — Workflow & Decision Flow

## Objective

Turn the dashboard into a connected decision workflow instead of separate sections.

By the end of this sprint, users should naturally move from:

Portfolio → Ticker Analysis → Decision → Review

without feeling lost.

---

## Context

Sprint 14 focused on:
- onboarding clarity
- portfolio readability
- guided vs advanced structure
- capital ownership clarity

That work is complete.

The next gap is not understanding — it is navigation and flow.

---

## Core Problem

Right now:
- Portfolio shows what was selected
- Ticker Analysis explains behavior

But:
- they are not connected
- users must manually switch tabs
- the flow feels fragmented

---

## Core Principle

**Portfolio = what the system selected**  
**Ticker Analysis = why the stock deserves attention**

---

## Deliverables

### 1. Clickable Portfolio Tickers

Users must be able to click a stock from Portfolio and move directly into Ticker Analysis.

Guided View:
- ticker or CTA button should be clickable

Advanced View:
- equivalent interaction in compact table or drilldown

---

### 2. Session State Handoff

On click:
- store selected ticker
- switch to Ticker Analysis tab
- preload ticker

---

### 3. Instruction Layer (Light)

Portfolio:
- "Click a stock to review its behavior in Ticker Analysis"

Ticker Analysis:
- "Viewing analysis for [TICKER] from your portfolio plan"

---

### 4. Preserve Simplicity

Do not:
- add heavy text
- clutter UI
- change existing logic

---

## Acceptance Criteria

- clicking a stock opens Ticker Analysis
- correct ticker loads
- flow feels intentional
- no logic changes

---

## Out of Scope

- Decision Audit Table (Sprint 16)
- Feature Insights upgrades
- Exit analysis redesign
- refresh/regeneration system

---

## Success Definition

A user should:

1. open Portfolio
2. click a stock
3. immediately understand:
   - what the stock has done historically
   - why it was selected

No confusion. No guessing.

---

## Sprint Positioning

Sprint 15 is a **connection sprint**, not a clarity sprint.

It links the system together into a usable flow.
