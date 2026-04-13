# Portfolio Case Study — JSE Market Lab

## Problem
Retail investors often have access to prices and headlines but lack a reliable process for deciding:
- which opportunities are truly actionable,
- how much risk is acceptable,
- and how to size positions under real constraints.

In the Jamaican market, lower liquidity, uneven coverage, and execution friction make weak decision processes materially more expensive.

## Target users
- **Primary:** self-directed beginner and intermediate retail investors.
- **Secondary:** analyst-minded users who want transparent, rule-based evaluation before committing capital.

## Product goal
Build a decision-support product that turns noisy market information into a consistent portfolio process, without presenting certainty or pretending to predict outcomes.

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
- The product remained positioned as **decision support**, not signal-selling.
- Tier C setups stayed visible but were generally not funded.
- Hard-stop constraints (for example, quality/liquidity failures) prevented forced allocation.
- Costs were embedded so outputs reflected realistic outcomes.
- Warnings were informative rather than blocking, preserving user agency.
- Language and UI were tuned for Jamaican readability while staying credible to a broader audience.

(See full decision history in [Product Decisions](product_decisions.md).)

## Product evolution across phases
- **Phase 1:** established a credible baseline for signal detection and ranking.
- **Phase 2:** added market realism through costs, liquidity, and event-aware context.
- **Phase 3:** shifted from analysis to clearer decision-making with guidance, confidence, and prioritization.
- **Phase 4:** translated insight into action through allocation and planner surfaces.
- **Phase 5:** closed the loop with review-and-discipline feedback, then hardened the experience for public beta.

## UAT and iteration highlights
Selected UAT checkpoints show progression from feature validation to product readiness:
- baseline validation to confirm core logic and identify early trust gaps ([Sprint 1 UAT](uat/uat_sprint_1.md)),
- mid-cycle usability checks to tighten structure, navigation, and decision flow ([Sprint 7 UAT](uat/uat_sprint_7.md)),
- pre-beta readiness checks to verify consistency, clarity, and release confidence ([Sprint 13 UAT](uat/uat_sprint_13.md)).

The broader sprint history remains available for traceability, while these milestones capture how feedback shaped product direction.

## Beta launch context
At beta launch, the project is framed as a focused product portfolio in a real market context:
- public-facing docs highlight decision logic and user value,
- sprint-heavy operational artifacts are archived,
- core artifacts remain visible for recruiters, collaborators, and beta users evaluating stage-appropriate maturity.

## What this demonstrates as a portfolio artifact
JSE Market Lab demonstrates:
- end-to-end product ownership from framing the problem to shaping beta scope,
- product judgment through explicit trade-offs under market and data constraints,
- iterative refinement that connects analytics to a usable investor decision workflow,
- disciplined documentation that translates internal build history into a recruiter-readable product narrative.
