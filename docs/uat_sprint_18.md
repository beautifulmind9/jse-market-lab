# UAT — Sprint 18 (Readiness Gating Research & Risk Control Design)

Sprint 18 is a research/design sprint. UAT should confirm that the proposed rules are measurable, grounded in available data, and safe to implement later.

---

## Test Area 1 — Dataset Reality

- [ ] Current dataset fields are listed clearly
- [ ] Supported analysis is separated from unsupported analysis
- [ ] Missing data needed for future logic is documented
- [ ] No rule assumes bid/ask spread, high/low, trade count, or news data unless those fields are available

---

## Test Area 2 — Readiness Gating Proposal

- [ ] Proposed hard requirements are listed
- [ ] Proposed watch-only conditions are listed
- [ ] Ready / Watch / Incomplete / Not fundable labels are defined
- [ ] Small sample size is not automatically treated as a hard block unless intentionally decided

---

## Test Area 3 — Liquidity Research Plan

- [ ] Liquidity metrics can be calculated from available data
- [ ] Volume-derived liquidity rules are proposed cautiously
- [ ] Rules are marked as research candidates, not live funding logic
- [ ] JSE-specific data gaps are acknowledged

---

## Test Area 4 — Risk-Control Design

- [ ] Candidate exit reasons are listed
- [ ] Dataset-supported exits are separated from future-data-dependent exits
- [ ] Price/downside logic is designed as research first
- [ ] No stop rule is presented as final without backtesting

---

## Test Area 5 — Backtest / Comparison Plan

- [ ] Proposed metrics include trade count, excluded trades, win rate, median return, average return, downside behavior, and tradeability realism
- [ ] Current funding behavior can be compared against proposed readiness gates
- [ ] Recommendation output is defined for Sprint 19

---

## Test Area 6 — Product Language

- [ ] Guidance avoids buy/sell recommendations
- [ ] Guidance explains readiness as discipline, not prediction
- [ ] Guidance does not imply funded trades are risk-free
- [ ] Guidance does not imply incomplete trades are automatically bad without evidence

---

## Overall Result

- [ ] Pass
- [ ] Needs iteration
