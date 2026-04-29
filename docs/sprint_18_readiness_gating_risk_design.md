# Sprint 18 — Readiness Gating Research & Risk Control Design

## Objective

Research and design whether Trade Readiness should affect funding eligibility, allocation sizing, warning labels, and early-exit/risk-control logic before changing the strategy engine.

Sprint 18 is a research/design sprint. It should produce rule proposals, comparison outputs, and implementation recommendations for Sprint 19.

---

## Why This Sprint Exists

Sprint 17 made Trade Readiness visible. During UAT, funded trades could still show incomplete readiness context, such as:

- liquidity data available
- volume support present
- spread behavior not available
- volatility context not available
- small evidence base
- signal timing not yet assessed

This creates a new product question:

> Should a trade receive funding if important readiness context is incomplete?

At the same time, Sprint 16 clarified that holding windows are review checkpoints, not unconditional hold instructions. That means the system also needs a risk-control framework for cases where a trade deteriorates before its planned review window.

---

## Product Principle

Do not change funding, allocation, or exit logic until the rule is researched and backtested.

Readiness gating and risk exits are strategy changes, not copy changes.

---

## Dataset Reality

The current market dataset includes:

- date
- market code
- market name
- table title
- symbol
- close price
- volume

This supports:

- close-price trend calculations
- volume participation checks
- trading-day counts
- zero-volume / low-volume analysis
- close-to-close downside testing
- signal-date readiness work

This does not yet support:

- true bid-ask spread analysis
- intraday stop testing using high/low
- order book depth
- trade count
- value traded, unless added later
- corporate event/news interpretation without external sources

Sprint 18 must therefore avoid overclaiming spread, liquidity, or intraday stop precision.

---

## Workstream 1 — Readiness Gating Research

### Question
Should Trade Readiness affect funding eligibility or allocation sizing?

### Candidate minimum funding requirements to test

Potential hard requirements:

- liquidity data available
- volume support present or sufficient
- signal timing assessable

### Candidate watch-only fields

Potential watch flags rather than hard blockers:

- spread behavior unavailable
- volatility context unavailable
- small evidence base

### Candidate readiness labels

Potential labels:

- Ready
- Watch
- Incomplete
- Not fundable

---

## Workstream 2 — Liquidity Model Research

Because the uploaded dataset includes close price and volume, liquidity should first be researched using volume-derived fields.

Potential liquidity metrics:

- 20D average volume
- 20D median volume
- positive-volume trading-day ratio
- zero-volume day count
- 20D traded value if value traded is later available
- price * volume as an estimated turnover proxy where value traded is missing

Potential rule ideas to test:

- minimum positive-volume day ratio
- minimum 20D median volume
- minimum turnover proxy
- no funding when volume is consistently zero or sparse

No hard liquidity threshold should be adopted until tested against JSE behavior.

---

## Workstream 3 — Backtest / Comparison Design

Compare current funding behavior against proposed readiness gates.

Measure:

- number of funded trades
- number of excluded trades
- win rate
- median return
- average return
- downside behavior
- liquidity realism
- trade count by market / board

The goal is not to eliminate all risk. The goal is to see whether readiness rules improve discipline without removing too many valid opportunities.

---

## Workstream 4 — Risk-Control Design

Define early-review or exit rules for cases where conditions deteriorate before the assigned holding-window review date.

Candidate exit reasons:

- planned holding-window exit
- price stop / downside threshold exit
- signal invalidation exit
- liquidity deterioration exit
- event-risk exit

### Dataset-supported candidates now

With close price and volume data, Sprint 18 can design and test:

- close-to-close downside threshold
- price decline from entry reference
- volume deterioration after entry
- signal invalidation using available signal fields

### Data needed later for stronger exits

For more advanced exits, the system needs:

- high price
- low price
- bid price
- ask price
- spread
- trade count
- value traded
- news / corporate event dates

---

## Workstream 5 — Product Guidance Design

Design user-facing guidance that explains:

- funded does not mean risk-free
- holding windows are review checkpoints
- trades may need earlier review if conditions deteriorate
- readiness gates are part of discipline, not prediction

Suggested future wording:

> This trade passed the current portfolio rules, but readiness is not complete. Review liquidity, volume, and timing before treating it as actionable.

or

> This trade is ready for closer review. Liquidity and volume data are available, and no major readiness gaps were detected.

---

## Out of Scope

Do not implement in Sprint 18:

- final funding-gate logic
- final stop-loss logic
- final exit execution engine
- user profile persistence
- AI news/earnings summaries
- portfolio economics calculations

---

## Deliverables

Sprint 18 should produce:

1. Readiness gate proposal
2. Liquidity metric proposal
3. Backtest/comparison plan
4. Risk-control design proposal
5. Recommendation for Sprint 19 implementation

---

## Success Criteria

Sprint 18 is complete when the project can answer:

- Which readiness fields should be hard requirements?
- Which readiness fields should remain warnings?
- What liquidity metrics can be supported by the current dataset?
- What price/risk exit rules can be tested with current data?
- What extra data is needed for stronger future logic?
