# Portfolio Case Study — JSE Market Lab

## Product summary
JSE Market Lab is a beta-stage decision-support product designed for retail investors in the Jamaican Stock Exchange. The product does not attempt to predict outcomes or automate trades. It helps users run a clearer, repeatable portfolio decision process with visible assumptions and constraints.

## Problem
Retail investors often have access to prices and headlines but lack a reliable process for deciding:
- which opportunities are actionable,
- how much risk is acceptable,
- and how positions should be sized under real constraints.

In the Jamaican market, thinner liquidity, uneven coverage, and execution friction increase the cost of weak decision processes.

## Users
- **Primary:** self-directed beginner and intermediate retail investors.
- **Secondary:** analyst-oriented users who want transparent, rule-based evaluation before committing capital.

## Product goal
Turn noisy market information into a consistent decision workflow that improves clarity and discipline without overstating certainty.

## Solution approach
The core flow is intentionally explicit:

`Data -> Signal -> Quality Score -> Risk Context -> Confidence -> Allocation -> Plan/Review`

Key system layers:
- signal detection,
- tiered quality scoring,
- earnings- and liquidity-aware risk context,
- cost-aware return framing,
- allocation constraints and planner outputs,
- post-decision review for behavior and discipline.

## Key product decisions
- Keep the product positioned as **decision support**, not signal-selling.
- Keep Tier C visible for context, while generally not funding it.
- Use hard-stop constraints for quality and liquidity failures.
- Embed costs so outputs reflect more realistic outcomes.
- Use informative warnings instead of blocking actions to preserve user agency.
- Tune language for Jamaican readability while remaining globally understandable.

Decision history: [Product decisions](./product_decisions.md).

## Product evolution (phase view)
- **Phase 1:** baseline signal detection and ranking.
- **Phase 2:** market realism through costs, liquidity, and event context.
- **Phase 3:** decision clarity via guidance, confidence, and prioritization.
- **Phase 4:** translation into action through allocation and planner surfaces.
- **Phase 5:** review-and-discipline loop, then public-beta hardening.

## UAT evidence and iteration quality
Three UAT checkpoints capture progression from correctness to product readiness:
- [Sprint 1 UAT](./uat/uat_sprint_1.md): baseline logic validation and early trust gaps.
- [Sprint 7 UAT](./uat/uat_sprint_7.md): usability tightening for structure, navigation, and flow.
- [Sprint 13 UAT](./uat/uat_sprint_13.md): pre-beta consistency, clarity, and release confidence checks.

These checkpoints are representative milestones; the full sprint record remains available for traceability.

## Beta-stage launch framing
At public beta, the repo is structured to support external evaluation:
- product-facing docs emphasize user value, decision logic, and trade-offs,
- sprint-heavy operational artifacts are archived for reference,
- core materials remain readable for recruiters, collaborators, and beta users.

## Portfolio artifact value
As a portfolio artifact, JSE Market Lab demonstrates:
- end-to-end product ownership from framing to beta release quality,
- product judgment through explicit trade-offs under market constraints,
- iteration discipline that connects analytics to practical decision workflows,
- documentation quality aimed at both local relevance and global readability.
