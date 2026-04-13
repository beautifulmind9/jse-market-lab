# JSE Market Lab

JSE Market Lab is a **public-beta decision-support product** for retail investors in the Jamaican Stock Exchange. It helps users make clearer portfolio decisions by turning market signals, costs, and risk context into a transparent workflow they can review and challenge.

## Beta status
This repository is a **public beta**: stable enough for evaluation, still evolving through documented iteration and user feedback.

## What problem it solves
Many retail investors can access market data but still struggle to:
- compare opportunities consistently,
- account for costs and liquidity,
- handle earnings-related uncertainty,
- convert signals into disciplined portfolio actions.

## What the product does
For each instrument, JSE Market Lab:
- ingests price behavior, earnings context, liquidity conditions, and fee assumptions,
- applies explicit rules to detect and score setups,
- surfaces risk flags and confidence levels,
- translates output into allocation guidance and portfolio plan options.

Workflow:

`Data -> Signal -> Score -> Risk Flags -> Confidence -> Allocation -> Portfolio Plan`

## Core features
- Identifies rule-based setups for listed JSE instruments.
- Scores opportunities with a transparent Tier A/B/C quality model.
- Estimates net outcomes using Jamaican broker-fee and CESS assumptions.
- Flags earnings phases and event-related risk conditions.
- Prioritizes candidates by confidence and decision relevance.
- Generates allocation plans within cash and exposure constraints.
- Supports post-decision review for consistency and discipline.

## Why it is different
- Prioritizes **explainability**: outputs are tied to explicit logic, not black-box predictions.
- Prioritizes **clarity**: signals, scores, and risk flags are structured for fast interpretation.
- Prioritizes **user judgment**: the product supports decisions; it does not replace investor discretion.
- Reflects Jamaican market realities, including trading frictions, liquidity, and event risk.

## Positioning and non-goals
This project is:
- a structured decision-support tool,
- a product portfolio artifact that shows end-to-end product thinking from framing to iteration.

This project is **not**:
- financial advice,
- a prediction engine,
- an auto-trading or signal-selling service.

## Key docs
- [Product Brief](docs/product_brief.md)
- [Feature Breakdown](docs/feature_breakdown.md)
- [Product Decisions](docs/product_decisions.md)
- [Iteration Log](docs/iteration_log.md)
- [Portfolio Case Study](docs/portfolio_case_study.md)
- [User Flow](docs/user_flow.md)
- [UAT](docs/uat/)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
