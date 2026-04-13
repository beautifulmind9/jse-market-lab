# JSE Market Lab

A beta-stage decision-support product that helps retail investors evaluate Jamaican Stock Exchange opportunities using structured rules instead of guesswork.

## Beta status
This repository reflects a **public beta** release: stable enough to explore, still evolving through documented iteration.

## What problem it solves
Many retail investors can see market data but still struggle to:
- compare opportunities consistently,
- account for costs and liquidity,
- handle earnings-related uncertainty,
- turn signals into disciplined portfolio actions.

## What the product does
JSE Market Lab converts market inputs into a structured decision workflow:

`Data -> Signal -> Score -> Risk Flags -> Confidence -> Allocation -> Portfolio Plan`

## Core features
- Rule-based signal detection for JSE instruments.
- Trade quality scoring (Tier A/B/C).
- Cost-aware outputs (broker fee + CESS assumptions).
- Earnings phase tagging and warning context.
- Confidence and prioritization layer.
- Portfolio allocation planner with cash/exposure constraints.
- Review layer for post-decision discipline feedback.

## Why it is different
- Built as a **decision-support system**, not a pick-selling feed.
- Emphasizes explainability and product clarity over prediction claims.
- Anchored in Jamaican market context while using globally understandable product design.

## Positioning and non-goals
This project is:
- a structured decision-support tool,
- a product portfolio artifact showing end-to-end product thinking.

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
- [Selected UAT Samples](docs/uat/)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
