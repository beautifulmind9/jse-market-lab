# Product Backlog

## Phase 2 — Post-Beta Refinement

### Sprint 16 — Live Context & Trade Timing
Status: Complete

Completed:
- Viewed timestamp
- Dataset recency visibility
- Entry-based holding-window interpretation clarity

Follow-up backlog:
- Signal timing awareness
- Signal age in trading days
- Fresh / Active / Late / Stale timing status
- Remaining holding-window context

---

### Sprint 17 — Trade Readiness, Liquidity & Data Foundations
Status: Complete

Completed:
- Trade Readiness UI layer
- Liquidity / volume / spread / volatility context without overclaiming
- Sample-size context without undermining funded trades
- Funding decision vs supporting analysis copy
- Signal-date readiness audit
- Canonical market date fallback for signal timing readiness

Follow-up backlog:
- stronger numeric liquidity model research
- calibrated liquidity thresholds by market/board/ticker behavior
- signal freshness implementation after signal-date fields are stable

---

### Sprint 18 — Readiness Gating Research & Risk Control Design
- Research whether Trade Readiness should affect funding eligibility
- Backtest minimum readiness gates before changing allocation logic
- Define Ready / Watch / Incomplete / Not fundable labels
- Design price-based and downside exit rules
- Design signal invalidation exits
- Design liquidity deterioration exits
- Design event-risk exits

---

### Sprint 19 — Exit Logic Implementation & Review Guidance
- Implement validated exit logic from Sprint 18 research
- Show risk-exit context in Execution Behavior
- Clarify that holding windows are review checkpoints, not unconditional holds
- Add reviewed-earlier-if-risk-changes guidance

---

### Sprint 20 — Portfolio Economics Layer
- Allocation-based fee calculation
- Estimated net returns based on capital
- Portfolio-level cost summary
- Net outcome scenarios

---

### Sprint 21 — AI Event, Earnings, News & Economic Context Layer
- Earnings season review cards
- Dividend and corporate action context
- Company news summaries
- Economic context summaries
- Source/date-grounded AI outputs
- AI guardrails to prevent buy/sell recommendations

---

### Sprint 22 — User Profile, Decision History & Adaptive Guidance
- User profile storage
- Saved decisions and planned trades
- Review outcomes over time
- Track whether user followed plan rules
- Update guidance when market data changes
- Compare old saved decisions against new loaded market data
- Personal decision discipline feedback

---

### Sprint 23 — Decision Audit & Transparency
- Ranking transparency
- Score breakdown visibility
- Structured comparison across trades

---

## Notes

- Backlog reflects priority order based on trust and usability gaps
- Items are sequenced to avoid premature optimization
- Each sprint builds on user understanding, not just feature expansion
- Risk-exit logic must be backtested before it becomes user-facing guidance
- Readiness gating must be tested before it affects funding eligibility
- AI context should be source-grounded and should not become a recommendation engine
- User profile features require persistence and privacy decisions before implementation
