# Sprint 14 Closeout — UI Architecture, Scanability, and Portfolio Surface Refinement

## Sprint goal
Sprint 14 focused on making the public-beta product easier to understand on first use without changing the core decision engine.

The sprint objective was to improve:
- first-run clarity
- Guided vs Advanced separation
- mobile readability
- portfolio scanability
- product trust through clearer presentation

This sprint was intentionally presentation-layer only.

It did **not** change:
- ranking logic
- allocation logic
- execution logic
- eligibility logic
- signal generation

---

## What Sprint 14 completed

### 1. Guided vs Advanced structure was clarified
The app now more clearly separates:
- **Guided View** for simpler interpretation and lower cognitive load
- **Advanced View** for deeper comparison and analyst-style inspection

This resolved earlier ambiguity where different users were seeing similar surfaces with different amounts of confusion.

### 2. First-run onboarding was tightened
The always-visible top area was shortened and secondary methodology content was moved into collapsed help surfaces.

This made the dashboard feel lighter on first load while preserving educational support for users who want it.

### 3. Portfolio Snapshot became more scanable
The portfolio area now surfaces a compact first-pass summary using:
- Trades Found
- Funded Trades
- Allocated %
- Cash Reserved %

This improved first-glance understanding of what the plan is doing.

### 4. Guided trade rendering moved away from heavy tables
Guided portfolio rows were moved into stacked trade cards to improve:
- scanability
- mobile readability
- beginner friendliness

This was the correct direction for Guided View, but it revealed a follow-up tradeoff around how much detail should remain visible by default.

### 5. Advanced sections received clearer purpose framing
Deeper surfaces such as Feature Insights, Performance Matrix, and Exit Analysis received clearer purpose captions so they feel more intentional and less like broken or unfinished pages.

### 6. Onboarding compatibility was hardened
The onboarding refactor initially created compatibility risk for older test stubs and partial Streamlit-like objects.

Sprint 14 included a defensive compatibility pass so onboarding falls back safely without breaking startup or lightweight tests.

---

## Key product learning from Sprint 14
Sprint 14 confirmed that reducing overload is not only about removing information.

It is about deciding:
- what should be compared first
- what should be explained second
- what can remain optional depth

This became most visible in the Portfolio surface.

The first Sprint 14 Guided/Advanced redesign improved readability, but it also exposed a new problem:

> Important portfolio information could still be missed when users had to horizontally scroll across wide analyst tables.

That meant the product still had a decision-surface issue even after the broader layout polish was complete.

---

## Sprint 14 follow-up refinement
A follow-up refinement was required to complete the sprint properly.

### Problem identified
The initial Sprint 14 design split became:
- **Guided View** = stacked cards
- **Advanced View** = full wide tables

This preserved depth, but it left one important usability problem:

**critical information in Advanced View could remain off-screen unless the user knew to scroll horizontally**

That behavior was considered unacceptable for the main decision surface.

### Product decision made
The portfolio surface should use:

**comparison first, explanation second**

This means:
- essential decision fields must be visible immediately
- deeper reasoning should be available through drilldown or expanders
- the full raw table can still exist, but only as an optional deeper layer

### Final Sprint 14 portfolio direction

#### Guided View
Guided View should remain card-based, but the cards should be compact and structured.

Primary visible fields:
- Ticker
- Setup Strength
- Confidence / Reliability
- Holding Window
- Why this trade / Why not funded

Collapsed detail fields:
- Execution Summary
- Rule Note
- Allocation %
- Allocation Amount
- Selection Rank
- Decision Status

#### Advanced View
Advanced View should no longer rely on one wide primary table.

The main analyst surface should become:
- a compact comparison table for immediate scanning
- per-row detail drilldowns for reasoning and context
- an optional full analyst table for raw depth

Primary comparison columns:
- Ticker
- Setup Strength or Tier
- Confidence / Reliability
- Holding Window
- Decision Status
- Allocation %
- Selection Rank

Secondary detail fields:
- Why this trade / Why not funded
- Execution Summary
- Rule Note
- Allocation Amount
- Allocation %
- Selection Rank
- Decision Status

---

## Current status at closeout
Sprint 14 is best understood as:

### Completed
- Guided/Advanced structure
- first-run onboarding polish
- top-area simplification
- portfolio snapshot simplification
- Guided mobile-first trade card direction
- analyst-section purpose captions
- onboarding compatibility hardening

### Completed through open refinement path
- portfolio decision-surface refinement was identified as a necessary follow-up within Sprint 14, not as a separate new sprint

### Current implementation status
PR #108 contains the implementation of the final Sprint 14 portfolio refinement:
- compact Guided cards with collapsed details
- compact Advanced comparison table
- inline drilldowns for advanced row details
- full analyst table kept as optional deeper surface

This preserves the intent of Sprint 14 while resolving its most important remaining usability gap.

---

## Why this sprint matters
Sprint 14 is important because it marks a shift from feature-building to product-surface refinement.

The work was not about adding a new engine.
It was about making the existing engine usable, understandable, and trustworthy in a real product context.

This sprint improved the dashboard in ways users directly feel:
- lighter first use
- clearer mode separation
- better scanability
- less hidden critical information
- better alignment between product depth and user type

---

## Final closeout note
Sprint 14 strengthened the dashboard’s product maturity by making the UI architecture more intentional.

The key lesson was that a strong engine is not enough.
The main decision surface must help users:
- compare quickly
- understand why a trade appears
- access deeper reasoning without being overwhelmed

That principle now becomes part of the product’s ongoing UI philosophy.
