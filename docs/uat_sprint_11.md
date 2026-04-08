# UAT — Sprint 11

## Areas to Validate

| Area | Check |
|-----|------|
| Trade Review | Each trade shows evaluation |
| Mistake Detection | Mistakes correctly identified |
| Behavior Summary | Insights are clear and relevant |
| Discipline Score | Score reflects behavior |
| UI Rendering | Section loads correctly |
| Empty State | No trades handled gracefully |

## Test Scenarios

### Scenario 1 — Perfect adherence
- user follows all rules
→ no mistakes
→ high discipline score

### Scenario 2 — Ignored better trade
→ mistake appears
→ summary reflects behavior

### Scenario 3 — Low quality trade
→ flagged correctly

### Scenario 4 — No trades
→ empty-safe output

## Closeout Criteria
- all scenarios pass
- no contradictory outputs
- language remains observational