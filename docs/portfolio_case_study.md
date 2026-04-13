# Portfolio Case Study — JSE Market Lab

## Problem
Retail investors often have access to prices and headlines but lack a reliable framework for deciding:
- which opportunities are actionable,
- how much risk is acceptable,
- and how to size positions under real constraints.

In the JSE context, this is amplified by lower liquidity, uneven coverage, and execution friction.

## Target users
- **Primary:** self-directed beginner and intermediate retail investors.
- **Secondary:** analyst-minded users who want transparent, rule-based evaluation before deploying capital.

## Product goal
Build a decision-support product that turns noisy market information into a consistent portfolio decision process without pretending to predict outcomes.

## System overview
The product flow is intentionally simple:

`Data -> Signal -> Quality Score -> Risk Context -> Confidence -> Allocation -> Plan/Review`

Key layers:
- signal detection,
- tiered quality scoring,
- earnings and liquidity-aware risk context,
- cost-aware return framing,
- allocation constraints and portfolio planning,
- post-decision review for user discipline.

## Key product decisions
- Positioning stayed firmly in **decision support**, not signal-selling.
- Tier C setups remain visible but generally unfunded.
- Hard-stop constraints (for example, quality/liquidity failures) prevent forced allocation.
- Costs are included so output reflects realistic outcomes.
- Warnings are informative rather than blocking, preserving user agency.
- Language and UI are tuned for Jamaican readability while remaining professional for a broader audience.

(See full decision history in [Product Decisions](product_decisions.md).)

## Product evolution across sprints/phases
- **Phase 1:** signal and ranking foundation.
- **Phase 2:** realism upgrades (costs, liquidity, event-aware context).
- **Phase 3:** decision clarity layers (guidance, confidence, prioritization).
- **Phase 4:** allocation and planner surfaces.
- **Phase 5:** review-and-discipline feedback plus beta hardening and deployment framing.

## UAT and iteration highlights
Selected UAT checkpoints were preserved to show product maturity over time:
- early baseline validation ([Sprint 1 UAT](uat/uat_sprint_1.md)),
- middle-phase usability and structure checks ([Sprint 7 UAT](uat/uat_sprint_7.md)),
- late-stage beta readiness and quality checks ([Sprint 13 UAT](uat/uat_sprint_13.md)).

Broader sprint history remains archived for traceability.

## Beta launch context
This repo now represents a cleaner beta-stage product portfolio:
- public-facing docs emphasize product value and system logic,
- sprint-heavy operational artifacts are archived,
- core artifacts remain visible for recruiters, collaborators, and beta users.

## What this demonstrates as a portfolio artifact
JSE Market Lab demonstrates:
- end-to-end product ownership,
- iterative decision-making under constraints,
- practical translation of analytics into user-facing workflow,
- documentation discipline from internal build history to public product narrative.
