# Portfolio Case Study — JSE Market Lab

## Problem
Retail investors often have prices and headlines but lack a reliable framework for deciding:
- which opportunities are actionable,
- how much risk is acceptable,
- and how to size positions under real constraints.

In the JSE, lower liquidity, uneven coverage, and execution friction make this gap more costly.

## Target users
- **Primary:** self-directed beginner and intermediate retail investors.
- **Secondary:** analyst-minded users who want transparent, rule-based evaluation before deploying capital.

## Product goal
Build a decision-support product that turns noisy market information into a consistent portfolio process without claiming to predict outcomes.

## System overview
The product flow is intentionally explicit:

`Data -> Signal -> Quality Score -> Risk Context -> Confidence -> Allocation -> Plan/Review`

Key layers:
- signal detection,
- tiered quality scoring,
- earnings- and liquidity-aware risk context,
- cost-aware return framing,
- allocation constraints and portfolio planning,
- post-decision review for discipline and accountability.

## Key product decisions
- Positioning stayed firmly in **decision support**, not signal-selling.
- Tier C setups remain visible but generally unfunded.
- Hard-stop constraints (for example, quality/liquidity failures) prevent forced allocation.
- Costs are included so output reflects realistic outcomes.
- Warnings are informative rather than blocking, preserving user agency.
- Language and UI are tuned for Jamaican readability while remaining credible to a broader audience.

(See full decision history in [Product Decisions](product_decisions.md).)

## Product evolution across sprints/phases
- **Phase 1:** established the signal and ranking foundation.
- **Phase 2:** added realism through costs, liquidity, and event-aware context.
- **Phase 3:** improved decision clarity with guidance, confidence, and prioritization.
- **Phase 4:** introduced allocation and planner surfaces for portfolio action.
- **Phase 5:** added review-and-discipline feedback, then hardened for public beta.

## UAT and iteration highlights
Selected UAT checkpoints show how the product matured from concept to beta:
- early baseline validation to confirm core logic ([Sprint 1 UAT](uat/uat_sprint_1.md)),
- mid-cycle usability and structure checks to improve decision flow ([Sprint 7 UAT](uat/uat_sprint_7.md)),
- late-stage readiness checks to verify beta quality and consistency ([Sprint 13 UAT](uat/uat_sprint_13.md)).

The broader sprint history is retained for traceability and context.

## Beta launch context
At beta launch, the project is presented as a focused product portfolio:
- public-facing docs emphasize product logic and decision value,
- sprint-heavy operational artifacts are archived,
- core artifacts remain visible for recruiters, collaborators, and beta users.

## What this demonstrates as a portfolio artifact
JSE Market Lab demonstrates:
- end-to-end product ownership,
- iterative decision-making under constraints,
- practical translation of analytics into a user-facing decision workflow,
- documentation discipline from internal build history to public product narrative.
