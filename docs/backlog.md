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

The backlog should reflect that shift.

## Sprint 7 — review hardening
Status: In progress

Open follow-ups:
- fix unfunded reason resolution to prefer allocator explanation fields (`allocation_reason_clear`, `allocation_reason_pro`, etc.) before helper fallback
- wire Analyst Insights to return-bearing performance/demo output instead of raw canonical dataset
- extend tests for both fixes
- keep scope limited to UI/data wiring only
