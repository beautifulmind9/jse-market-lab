# Prioritized Backlog

This backlog reflects the current state of the JSE Decision Support Dashboard after completion of the core strategy engine, risk-awareness layers, confidence system, allocation engine, and analyst validation surfaces.

The focus is now shifting from building the engine to making the product visible, understandable, and usable for real investors.

---

## Priority Definitions

- **Critical** = blocks the product from being properly used or seen
- **High** = directly increases user value, trust, or usability
- **Medium** = important extension of the product, but not immediate blocker
- **Low** = nice to have after core experience is complete

---

## Active Prioritized Backlog

| Epic / Feature | Why It Matters | Priority |
|----------------|----------------|----------|
| Streamlit App Shell | Makes the product runnable and visible to users; currently the main blocker to seeing the dashboard live | Critical |
| Portfolio Plan UI | Turns allocation outputs into a usable weekly portfolio plan instead of raw logic | High |
| Insight Translation Layer | Converts dashboard outputs into simple, shareable insights for everyday Jamaican investors | High |
| Explanation Layer | Builds trust by answering “why this trade?” and “why this allocation?” in clear language | High |
| Analyst Insights Refinement | Improves readability, interpretation, and usability of the Feature Insights / Matrix / Exit Analysis layer | Medium |
| Ticker Drilldown / Security Report | Adds stock-specific historical context so users can assess how individual names behave | Medium |
| Plan History / Review Workflow | Supports saving, revisiting, and reviewing weekly plans over time | Medium |
| Public Documentation Alignment | Keeps README, case study, overview, and user flow aligned with the actual product experience | Medium |
| Advanced Styling | Improves polish after the product surface and explanation layers are stable | Low |

---

## Epic Breakdown

### 1. Streamlit App Shell
**Goal:** Create the runnable user-facing app layer.

**Why this exists:**  
The repo currently contains logic and UI helpers, but no top-level Streamlit entrypoint that loads and displays the dashboard.

**Candidate backlog items:**
- Create `app.py` or `streamlit_app.py`
- Load latest dataset into the app
- Add navigation / mode selection
- Wire planner, analyst insights, and future portfolio plan views into a single app shell

---

### 2. Portfolio Plan UI
**Goal:** Present allocations as a clear portfolio decision artifact.

**Why this exists:**  
The allocation engine is built, but the user still needs a visible plan showing:
- funded trades
- unfunded trades
- reasons
- cash reserve
- constraints applied

**Candidate backlog items:**
- Portfolio summary section
- Funded vs unfunded trade tables
- Reason labels for funding / non-funding
- Constraints section
- Allocation totals and reserve display

---

### 3. Insight Translation Layer
**Goal:** Turn analysis outputs into simple insights for public and everyday investor use.

**Why this exists:**  
The dashboard can already calculate a lot, but it still needs to speak clearly to normal users.

**Candidate backlog items:**
- Generate 3–5 key insights in simple language
- Identify surprising / unexpected findings
- Surface common mistakes the data reveals
- Explain one feature in plain language
- Format outputs for public sharing / educational content

---

### 4. Explanation Layer
**Goal:** Make system outputs more trustworthy and understandable.

**Why this exists:**  
Users need more than labels and allocations — they need to understand why the system arrived at them.

**Candidate backlog items:**
- Explain confidence labels
- Explain allocation decisions
- Explain risk flags in plain language
- Add “why this trade?” support using existing logic and history

---

### 5. Analyst Insights Refinement
**Goal:** Improve the usefulness of the validation layer added in Sprint 6.

**Why this exists:**  
Feature Insights, Performance Matrix, and Exit Analysis now exist, but the experience can still be improved.

**Candidate backlog items:**
- Improve table readability
- Refine best-setup interpretation
- Add analyst-friendly navigation
- Improve handling of partial or messy datasets
- Add supporting captions / interpretation prompts

---

### 6. Ticker Drilldown / Security Report
**Goal:** Add stock-specific historical context.

**Why this exists:**  
Users may trust the system overall but still want to understand how a specific stock behaves historically.

**Candidate backlog items:**
- Signal history per security
- Win rate by security
- Median return by security
- Tier distribution by security
- Holding-window comparison per security

---

### 7. Plan History / Review Workflow
**Goal:** Add longer-term discipline and retention to the product.

**Why this exists:**  
A real decision-support workflow should let users save plans, review them later, and learn over time.

**Candidate backlog items:**
- Save weekly plans
- Reload previous plans
- Compare planned vs actual outcomes
- Monthly review / history view

---

### 8. Public Documentation Alignment
**Goal:** Keep the product narrative aligned with the actual product.

**Why this exists:**  
The repo already has strong documentation, but it must stay current as the product becomes visible and usable.

**Candidate backlog items:**
- Keep README aligned with live app experience
- Keep case study aligned with completed sprints
- Add screenshots after the app shell exists
- Add public walkthrough / how-to-use section

---

### 9. Advanced Styling
**Goal:** Improve polish after core usability is complete.

**Why this exists:**  
Styling matters, but it should not take priority over visibility, clarity, or explanation.

**Candidate backlog items:**
- UI polish
- improved spacing
- minor visual enhancements
- better section hierarchy

---

## What Is Already Delivered

The following work is already substantially completed and should no longer drive the top of the backlog:

- Signal engine
- Ranking / scoring engine
- Cost engine
- Earnings warning system
- Planner warning UI
- Decision guidance layer
- Jamaican clarity layer
- Confidence classification
- Allocation engine
- Analyst intelligence layer

These remain part of the product foundation, but the backlog should now focus on turning the engine into a visible, explainable, user-facing product.

---

## Backlog Direction by Next Likely Sprints

### Sprint 7
- Streamlit App Shell
- Portfolio Plan UI

### Sprint 8
- Explanation Layer
- First public insight outputs

### Sprint 9
- Insight Translation Layer refinement
- Public / educational formatting

### Later
- Ticker Drilldown
- Plan History
- Documentation walkthrough
- Advanced styling

---

## Product Principle Going Forward

The dashboard is no longer just an analytics engine.

It is becoming:

- a decision-support system
- a portfolio-planning tool
- an education product
- a public insight platform

### Sprint 7 — Review hardening
**Status:** In progress  
**Priority:** High

**Open follow-ups**
- Fix unfunded trade reason resolution to prefer allocator explanation fields before helper fallback
- Wire Analyst Insights to a return-bearing performance/demo dataset instead of raw canonical price data
- Extend tests for portfolio reason resolution and analyst data wiring
- Keep scope limited to UI/data wiring only; no engine logic changes

**Acceptance criteria**
- Unfunded trades show allocator-produced reason when available
- Analyst Insights tab renders from a dataset with supported return columns
- Existing fallback behavior remains graceful
- Tests pass

### Sprint 7 — Streamlit App Shell and Portfolio Plan UI
**Status:** Done with minor follow-up  
**Priority:** High

**Delivered**
- Added root `app.py` Streamlit entrypoint
- Added visible dashboard shell
- Added Analyst Insights tab to the app surface
- Added Portfolio Plan tab with funded vs unfunded sections
- Added portfolio summary and constraints display
- Added portfolio UI helper coverage with tests
- Completed Sprint 7 review hardening for reason resolution and analyst data wiring

**Validation**
- Sprint 7 targeted tests passed
- Full regression suite passed locally after duplicate nested repo cleanup

**Minor follow-up**
- UI polish and styling refinement
- richer explanation copy in the visible app
- more user-friendly summary surfaces for everyday investors

  ### Sprint 8 — Next scope to be finalized
**Status:** Draft / To refine  
**Priority:** High

**Context**
A public-facing insight prompt was created to support marketing and public sharing:
- 3–5 key insights
- anything surprising or unexpected
- common mistakes the data reveals
- short explanation of one feature

This prompt is valuable, but it was created for another chat’s marketing/documentation workflow and should not automatically define the next in-app sprint.

**Current options under consideration**
- Option A: build an in-app Explanation + Insight Translation Layer
- Option B: use dashboard outputs externally for marketing/documentation first
- Option C: do both, but in separate phases

**Immediate need**
- decide whether the next sprint is product implementation, content support, or a staged combination of both

**Acceptance criteria for scope decision**
- next sprint objective is clearly identified
- in-app work and content/marketing work are separated where necessary
- backlog reflects actual implementation scope rather than blended ideas
