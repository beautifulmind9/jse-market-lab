# UAT — Sprint 8

## Overall Status
Not started

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Not started | |
| Allocation explanations present | Not started | |
| Confidence explanations clear | Not started | |
| Warning explanations understandable | Not started | |
| Explanations match system logic | Not started | |
| UI remains readable | Not started | |

## Pass condition
Sprint 8 passes when:
- users can understand why decisions are made
- explanations are accurate and grounded in logic
- trust in the system is improved

# UAT — Sprint 8

## Overall Status
In progress — review fix outstanding

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Pass | Explanation helpers and UI layer added |
| Allocation explanations present | Pass | Portfolio Plan includes explanation output |
| Confidence explanations clear | Pass | Confidence explanation support added |
| Warning explanations understandable | Pass | Warning explanation support added |
| Explanations match system logic | In progress | Review flagged possible misclassification of hard-stop rule failures as generic constraints |
| UI remains readable | Pass | Explanation layer added in table-first format |

## Open issue
Explanation-priority logic must be corrected so trades blocked by hard-stop rules such as Tier C or liquidity failure are not explained as if they were only blocked by portfolio constraints.

## Pass condition
Sprint 8 passes when:
- users can understand why decisions are made
- explanations are accurate and grounded in logic
- hard-stop rule failures are clearly separated from portfolio-constraint cases
- tests pass after the review fix
