# Sprint 13 Backlog

## Goal
Improve user understanding by adding a stronger decision layer and a rule-based execution layer across Portfolio, Ticker Analysis, and Analyst Insights.

---

## Portfolio
- [ ] add Portfolio Snapshot block
- [ ] add Reserved Cash explanation block
- [ ] explain setup strength in plain language
- [ ] explain confidence in plain language
- [ ] add “Why this trade” support
- [ ] add Execution Summary support
- [ ] clean up Portfolio table labels
- [ ] reduce first-screen interpretation burden

---

## Execution Layer
- [ ] define entry reference framing
- [ ] define planned exit framing
- [ ] define typical outcome framing
- [ ] use median return as primary typical-outcome metric
- [ ] add spread / liquidity execution notes where relevant

---

## Ticker Analysis
- [ ] refine Quick Take wording
- [ ] strengthen Best Holding Strategy explanation
- [ ] add Execution Behavior section
- [ ] ensure every table has interpretation before it
- [ ] continue simplifying Beginner mode
- [ ] preserve deeper analyst detail in Analyst mode

---

## Analyst Insights
- [ ] define Strategy Summary section
- [ ] add interpretation around Performance Matrix
- [ ] clarify / simplify Exit Analysis
- [ ] hide or clearly explain Feature Insights when empty

---

## Shared explanation / labels
- [ ] add reusable explanation helpers
- [ ] add global display-label formatter
- [ ] remove snake_case labels from user-facing UI
- [ ] enforce median-first display rule where typical outcome is discussed
- [ ] keep wording simple and non-technical

# Sprint 13 Backlog

## Goal
Improve user understanding by turning the app into a clearer decision-support system with stronger Portfolio interpretation, an execution-aware layer, median-first logic, adaptive funding, and a more human-readable Review / Decision Audit surface.

---

## Portfolio
- [x] add Portfolio Snapshot block
- [x] add Reserved Cash explanation block
- [x] explain setup strength in plain language
- [x] explain confidence / reliability in plain language
- [x] add “Why this trade” support
- [x] add Execution Summary support
- [x] clean up Portfolio table labels
- [x] reduce first-screen interpretation burden
- [x] make funded-trade count adaptive instead of effectively fixed at 3
- [x] add analyst-only funded-trade cap support
- [x] explain adaptive funding / reserve behavior in Portfolio copy
- [x] restore explicit holding-window propagation and display in Portfolio
- [x] clarify compact exit timing wording in Portfolio tables

---

## Execution Layer
- [x] define entry reference framing
- [x] define planned exit framing
- [x] define typical outcome framing
- [x] use median return as primary typical-outcome metric
- [x] add spread / liquidity execution notes where relevant
- [x] ensure compact execution wording is stable in table view
- [x] ensure compact execution summary avoids runtime crashes and stale row references

---

## Ticker Analysis
- [x] refine Quick Take wording
- [x] strengthen Best Holding Strategy explanation
- [x] add Execution Behavior section
- [x] ensure every table has interpretation before it
- [x] continue simplifying Beginner mode
- [x] preserve deeper analyst detail in Analyst mode
- [x] enforce median-first behavior in ticker interpretation

---

## Analyst Insights
- [x] add clear interpretation captions to each section
- [x] add interpretation around Performance Matrix
- [x] clarify / simplify Exit Analysis
- [x] hide or clearly explain Feature Insights when empty
- [x] use shared display-label cleanup in analyst-facing tables
- [x] make Analyst Insights feel less placeholder-like and more strategy-validation oriented

---

## Review / Decision Audit
- [x] redefine Review tab purpose as discipline / decision audit
- [x] replace raw backend-style review table with human-readable audit columns
- [x] translate statuses into user-readable explanations
- [x] improve “what happened” and “why it matters” framing
- [ ] final hardening pass for any remaining review-message edge cases discovered during beta

---

## Shared explanation / labels
- [x] add reusable explanation helpers
- [x] add global display-label formatter
- [x] remove snake_case labels from user-facing UI
- [x] enforce median-first display rule where typical outcome is discussed
- [x] keep wording simple and non-technical
- [x] preserve falsy display labels like `0` and `False` correctly

---

## Sprint closeout note
Sprint 13 feature scope is complete.

Any remaining small issues after release are considered:
- beta hardening
- wording cleanup
- performance tightening
- edge-case stabilization

These are not new Sprint 13 features.
