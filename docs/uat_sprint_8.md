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

# UAT — Sprint 8

## Overall Status
In progress — portfolio explanation logic validated

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Pass | Explanation helpers added |
| Allocation explanations present | Pass | Portfolio Plan explanation output added |
| Hard-stop vs constraint distinction is accurate | Pass | Tier C, liquidity failure, true portfolio constraints, and generic unfunded cases now separate correctly |
| False constrained labeling avoided | Pass | Generic wording such as “pre-constraints reduced allocation to zero” no longer auto-classifies as constrained |
| Confidence explanations clear | In progress | Added, but still needs broader app-level validation |
| Warning explanations understandable | In progress | Added, but still needs broader app-level validation |
| Explanations match system logic | In progress | Portfolio explanation classification validated; broader end-to-end validation still pending |
| UI remains readable | In progress | Needs app-level visual confirmation |

## Validation completed
- Tier C hard-stop case no longer mislabels as portfolio constraint
- Liquidity hard-stop case no longer mislabels as portfolio constraint
- Genuine max funded trades case remains classified as constrained
- Genuine max portfolio exposure case remains classified as constrained
- Generic wording such as “pre-constraints reduced allocation to zero” falls back to generic unfunded rather than false constrained classification
- Sparse fallback behavior remains supported

## Pass condition
Sprint 8 passes when:
- users can understand why portfolio decisions are made
- confidence and warning explanations are also validated in-app
- explanations remain accurate and readable across the full explanation layer

# UAT — Sprint 8

## Overall Status
In progress — portfolio explanation layer materially advanced

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Pass | Explanation helpers added |
| Allocation explanations present | Pass | Portfolio Plan explanation output added |
| Hard-stop vs constraint distinction is accurate | Pass | Tier C, liquidity failure, true portfolio constraints, and generic unfunded cases now separate correctly |
| False constrained labeling avoided | Pass | Generic wording such as “pre-constraints reduced allocation to zero” no longer auto-classifies as constrained |
| Ranking / allocation-priority explanations present | Pass | Portfolio Plan now explains why funded trades were selected ahead of other eligible trades |
| Eligible-but-not-funded ranking explanation present | Pass | Eligible trades can now be explained as ranking outside funded positions when limits were reached |
| Confidence explanations clear | In progress | Added, but still needs broader app-level validation |
| Warning explanations understandable | In progress | Added, but still needs broader app-level validation |
| Explanations match system logic | In progress | Portfolio explanation classification and ranking logic validated; broader end-to-end validation still pending |
| UI remains readable | In progress | Needs final app-level visual confirmation |

## Validation completed
- Tier C hard-stop case no longer mislabels as portfolio constraint
- Liquidity hard-stop case no longer mislabels as portfolio constraint
- Genuine max funded trades case remains classified as constrained
- Genuine max portfolio exposure case remains classified as constrained
- Generic wording such as “pre-constraints reduced allocation to zero” falls back to generic unfunded rather than false constrained classification
- Ranking-aware explanations now distinguish between funded priority and eligible-but-outside-funded positions

## Pass condition
Sprint 8 passes when:
- users can understand why portfolio decisions were made
- users can understand why some eligible trades were selected ahead of others
- confidence and warning explanations are also validated in-app
- explanations remain accurate and readable across the full explanation layer

# UAT — Sprint 8

## Overall Status
In progress — embedded insight layer added, review fixes outstanding

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Pass | Explanation helpers added |
| Allocation explanations present | Pass | Portfolio Plan explanation output added |
| Ranking / allocation-priority explanations present | Pass | Funded vs eligible-but-outside-funded logic added |
| Embedded insights present | Pass | App now renders “what_is_happening” and “what_to_watch” |
| Decision status aligns with allocator metadata | In progress | Review flagged that `eligible_for_funding` should be used in classification |
| Embedded insight wording feels natural | In progress | Structure is correct, but some sentence templates need cleaner Jamaican-friendly English |
| Confidence explanations clear | In progress | Still needs app-level validation |
| Warning explanations understandable | In progress | Still needs app-level validation |
| UI remains readable | In progress | Needs final visual review after wording cleanup |

## Open issues
- decision-status classification should incorporate `eligible_for_funding` to avoid metadata/UI mismatch
- embedded insight wording needs to sound more natural and less templated

## Pass condition
Sprint 8 passes when:
- portfolio and embedded insight outputs are accurate
- decision status matches actual allocator metadata
- wording is clear, natural, and easy to understand
- explanations and insights remain neutral and non-advisory

# UAT — Sprint 8

## Overall Status
In progress — wording improved, decision-status refinement still needed

## UAT Checklist

| Area | Status | Notes |
|-----|--------|------|
| Trade explanations present | Pass | Explanation helpers added |
| Allocation explanations present | Pass | Portfolio Plan explanation output added |
| Ranking / allocation-priority explanations present | Pass | Funded vs eligible-but-outside-funded logic added |
| Embedded insights present | Pass | App now renders “what_is_happening” and “what_to_watch” |
| Embedded insight wording feels natural | Pass with note | Wording is stronger and more natural, though minor future refinement may still help |
| Decision status aligns with hard-stop logic | Pass | Tier C, liquidity, and explicit ineligible cases remain separated correctly |
| Decision status distinguishes zero-allocation risk sizing from not eligible | In progress | `eligible_for_funding=False` may still collapse risk-sized zero trades into `not eligible` |
| Confidence explanations clear | In progress | Still needs app-level validation |
| Warning explanations understandable | In progress | Still needs app-level validation |
| UI remains readable | In progress | Needs final visual review after status refinement |

## Open issue
Trades that pass hard rules but are reduced to 0 allocation by sizing/risk logic should not be grouped under the same status as true hard-stop ineligibility.

## Pass condition
Sprint 8 passes when:
- portfolio and embedded insight outputs are accurate
- decision status distinguishes hard-stop ineligibility, portfolio constraints, and zero-allocation sizing outcomes clearly
- wording is clear, natural, and easy to understand
- explanations and insights remain neutral and non-advisory
