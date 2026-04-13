# Sprint 13 — Information Architecture

## Top-level tabs

### Portfolio
Role: Decision + capital deployment  
Question answered: What are the best current opportunities, why are they selected, how is capital being handled, and how would a trade typically be approached?

### Review
Role: Discipline / decision audit  
Question answered: Did the plan follow the intended rules, where did discipline matter, and where were tradeoffs or gaps introduced?

### Ticker Analysis
Role: Behavior + execution context  
Question answered: How does this stock usually behave, which holding style fits it best, and what would execution generally look like?

### Analyst Insights
Role: Strategy validation  
Question answered: Does grouped historical evidence support the strategy logic?

### Data
Role: Transparency  
Question answered: What dataset is the app using and is the system healthy?

---

## Portfolio target section order

1. Portfolio Snapshot
2. Capital Summary
3. Why some cash is reserved
4. Funded Trades
5. Unfunded Trades
6. Portfolio rules / funding approach
7. Optional deeper support in Analyst mode

### Sprint 13 update
Portfolio now uses:
- adaptive funded-trade behavior
- execution-aware summaries
- translated setup strength / confidence wording
- explicit holding-window / exit framing

The Portfolio surface is intended to feel like a plan, not a report.

---

## Review target section order

1. Summary interpretation
2. What to improve
3. Mistakes detected
4. Decision Audit table

### Decision Audit table purpose
The review table should no longer act like a backend dump.

It should answer:
- what happened
- whether rules were followed
- why it matters

Target columns:
- Ticker
- Status
- What happened
- Why it matters

---

## Ticker Analysis target section order

1. Quick Take
2. Best Holding Strategy
3. Risk Profile
4. What Usually Happens
5. What to Watch
6. Execution Behavior
7. Analyst Deep Dive

### Sprint 13 update
Ticker Analysis is now expected to:
- explain before showing tables
- use median-first framing
- separate beginner readability from analyst depth
- include execution-aware behavior rather than only historical tables

---

## Analyst Insights intended structure

### Feature Insights
Purpose: explain whether specific setup tags are associated with stronger or weaker outcomes  
Sprint 13 rule: show only when meaningful feature-tag data exists, otherwise explain clearly that it is not available yet

### Performance Matrix
Purpose: show how setup quality and holding-period combinations behave historically  
Requirement: interpretation before the matrix

### Exit Analysis
Purpose: explain how trades typically end and whether exit behavior reveals anything important  
Requirement: simplify or clearly explain if time-based exits dominate

### Strategy-validation framing
Analyst Insights should feel like a grouped-evidence layer for validating the system, not a raw matrix dump.

---

## Data tab structure

1. Data Status summary
2. warnings / errors if present
3. data preview

The Data tab remains a transparency layer, not a first-stop decision surface.
