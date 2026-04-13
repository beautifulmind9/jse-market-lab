# JSE Market Lab

JSE Market Lab is a public-beta decision-support product that helps retail investors evaluate Jamaican Stock Exchange opportunities with explicit rules, constraints, and trade-offs.

## Beta status
This repository is a **public beta**: stable enough for evaluation, still evolving through documented iteration and user feedback.

## What problem it solves
Many retail investors can access market data but still struggle to:
- compare opportunities consistently,
- account for costs and liquidity,
- handle earnings-related uncertainty,
- convert signals into disciplined portfolio actions.

## What the product does
JSE Market Lab converts price action, earnings context, liquidity signals, and trading costs into a repeatable decision workflow:

`Data -> Signal -> Score -> Risk Flags -> Confidence -> Allocation -> Portfolio Plan`

## Core features
- Detects rule-based signals for JSE instruments.
- Scores each setup using a Tier A/B/C quality model.
- Applies broker-fee and CESS assumptions to frame net outcomes.
- Tags earnings phases and surfaces relevant risk warnings.
- Ranks candidates with confidence and prioritization signals.
- Plans allocations with cash and exposure constraints.
- Supports post-decision review to reinforce discipline.

## Why it is different
- Built as a **decision-support system**, not a pick-selling feed.
- Shows how each output is derived, so users can audit the logic.
- Models Jamaican market frictions directly (costs, liquidity, and event risk).

## Positioning and non-goals
This project is:
- a structured decision-support tool,
- a product portfolio artifact that shows end-to-end product thinking from framing to iteration.

This project is **not**:
- financial advice,
- a prediction engine,
- an auto-trading or signal-selling service.

## Key docs
- [Product Brief](./docs/product_brief.md)
- [Feature Breakdown](./docs/feature_breakdown.md)
- [Product Decisions](./docs/product_decisions.md)
- [Iteration Log](./docs/iteration_log.md)
- [Portfolio Case Study](./docs/portfolio_case_study.md)
- [User Flow](./docs/user_flow.md)
- [Selected UAT Samples](./docs/uat/)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
