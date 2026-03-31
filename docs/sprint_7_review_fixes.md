# Sprint 7 Review Fixes

## Context
Sprint 7 delivered the first visible product surface for the JSE Dashboard:
- root `app.py`
- Streamlit app shell
- Portfolio Plan UI
- funded vs unfunded trade sections
- portfolio summary
- Analyst Insights tab wiring
- unit tests for portfolio UI helpers

Post-review, two important issues were identified that needed correction before Sprint 7 could be considered complete.

## Review fix 1 — allocator reason truthfulness
The Portfolio Plan UI initially relied too heavily on helper-generated funding reasons. That was acceptable as fallback logic, but not always sufficient for unfunded trades.

A trade may be individually eligible but still remain unfunded due to portfolio constraints such as:
- max funded trades reached
- exposure cap reached
- reserve rule preserved cash
- other trades prioritized first

To keep the dashboard truthful, unfunded reason resolution must prefer allocator-produced explanation fields before using helper fallback labels.

### Required resolution order
1. `allocation_reason_clear`
2. `allocation_reason_pro`
3. `allocator_reason`
4. `allocation_reason`
5. `reason`
6. fallback: `generate_funding_reason(trade)`

## Review fix 2 — Analyst Insights data handoff
The app shell originally passed the raw canonical dataset into `render_analyst_insights(...)`.

That dataset is suitable for shell preview and data status, but not for analyst rendering because it does not reliably contain return fields such as:
- `return_pct`
- `net_return_pct`

The fix is to keep the canonical dataset for status/preview while feeding Analyst Insights from the return-bearing demo/performance dataset.

## Scope guard
These fixes remain within Sprint 7 and do not change:
- signal logic
- scoring logic
- allocation engine logic
- analyst logic internals

The work is limited to:
- UI wiring
- explanation wiring
- data handoff correctness
- test updates

## Sprint 7 closeout condition
Sprint 7 is complete only when:
- unfunded trades display allocator-produced reasons where available
- Analyst Insights renders from return-bearing data
- fallback behavior remains graceful
- tests are updated and passing

## Product lesson
Two product lessons were reinforced:
1. A decision-support tool must explain the true reason behind outcomes.
2. A visible feature is only complete when it is wired to the correct data contract.
