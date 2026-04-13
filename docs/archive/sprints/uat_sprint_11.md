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

# UAT — Sprint 11

## Overall Status
In progress — review UX materially improved

## UAT Checklist

| Area | Status | Notes |
|---|---|---|
| Decision Review renders | Pass | Review content now appears in its own subtab under Portfolio Plan |
| Trade Review output renders | In progress | Needs app-level validation across multiple scenarios |
| Mistake Detection renders | Pass | Mistake output is now grouped and more readable |
| Behavior Summary renders | Pass | Summary bullets appear clearly |
| Interpretation layer renders | Pass | “What this means” and “What to improve” now connect review output to user behavior |
| Discipline Score renders | In progress | Needs app-level validation across scenarios |
| Empty state is safe | Pass | Covered by unit tests |
| Over-allocation check stays safe without allocation_pct | Pass | Review hardening completed |
| Cooldown violation detection survives overlapping trade/allocation inputs | Pass | Review hardening completed |
| UI remains readable | Pass with note | Structure is much better after subtab split; final scenario-based review still needed |
| Language remains observational | Pass with note | Tone is neutral and useful, though a later language pass may still improve naturalness |

## Validation completed
- Decision Review moved into a dedicated Review subtab
- Interpretation layer added so users understand what review output means
- Improvement guidance added without drifting into trade advice
- Repeated mistake types now render as grouped summary lines

## Pass condition
Sprint 11 passes when:
- Review tab feels useful across multiple review scenarios
- discipline score and summary feel believable
- mistake detection feels accurate and readable
- no contradictory or confusing review output appears

# UAT — Sprint 11

## Overall Status
Complete

## Final Assessment

| Area | Status | Notes |
|---|---|---|
| Decision Review renders | Pass | Review content appears in its own subtab under Portfolio Plan |
| Trade Review output renders | Pass | Review table appears and loads correctly |
| Mistake Detection renders | Pass | Mistake output is grouped and readable |
| Behavior Summary renders | Pass | Summary bullets appear clearly |
| Interpretation layer renders | Pass | “What this means” and “What to improve” connect review output to user behavior |
| Discipline Score renders | Pass | Score displays clearly and feels useful in context |
| Empty state is safe | Pass | Covered by unit tests |
| Over-allocation check stays safe without allocation_pct | Pass | Review hardening completed |
| Cooldown violation detection survives overlapping trade/allocation inputs | Pass | Review hardening completed |
| UI remains readable | Pass | Review now has a clearer structure after subtab split |
| Language remains observational | Pass with note | Tone is useful and neutral; a later language pass may further localize the voice |

## Summary
Sprint 11 successfully adds a Review & Discipline Layer that helps users reflect on how they are using the system, not just what the system selected.

The Review tab now:
- separates reflection from planning
- explains what the detected behavior means
- shows what users can improve without drifting into trade advice
- presents mistakes in a cleaner, more useful format

## Closeout Decision
Sprint 11 is complete.
