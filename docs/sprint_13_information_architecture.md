# Sprint 13 — Information Architecture

## Top-level tabs

### Portfolio
Role: Decision
Question answered: What are the best current opportunities, why are they selected, and how is capital being handled?

### Review
Role: Discipline / validation
Question answered: Did the plan follow the intended rules and where does discipline matter?

### Ticker Analysis
Role: Behavior + execution context
Question answered: How does this stock usually behave, which holding style fits it best, and what would execution generally look like?

### Analyst Insights
Role: Strategy validation
Question answered: Does the grouped historical evidence support the strategy logic?

### Data
Role: Transparency
Question answered: What dataset is the app using and is the system healthy?

---

## Portfolio target section order

1. Portfolio Snapshot
2. Capital Summary
3. Why some cash is reserved
4. Trade table / trade cards
5. Why this trade
6. Execution Summary
7. Optional deeper support in Analyst mode

---

## Ticker Analysis target section order

1. Quick Take
2. Best Holding Strategy
3. Risk Profile
4. What Usually Happens
5. What to Watch
6. Execution Behavior
7. Analyst Deep Dive

---

## Analyst Insights intended structure

### Strategy Summary
Purpose: explain what the grouped analyst view is trying to answer

### Performance Matrix
Purpose: show how setup quality and holding-period combinations behave historically
Requirement: interpretation before and after the matrix

### Exit Analysis
Purpose: explain how trades typically end and whether exit behavior reveals anything important
Requirement: simplify or hide if nearly all exits are time-based

### Feature Insights
Current state: often empty / under-defined
Sprint 13 decision: hide unless meaningful feature-tag data exists, or replace with a clear “not available yet” explanation
