# JSE Market Lab

JSE Market Lab is a **public-beta decision-support product** for self-directed investors in the Jamaican Stock Exchange (JSE). It turns market signals, cost assumptions, and risk context into a transparent workflow users can review, challenge, and use in their own decision process.

## Beta status
This repository is in **public beta**: stable enough for evaluation, still improving through documented iteration and UAT feedback.

## Problem it addresses
Many retail investors can access prices and market commentary, but still struggle to:
- compare opportunities consistently,
- account for costs and liquidity,
- handle earnings-related uncertainty,
- convert analysis into disciplined portfolio actions.

## What the product does
For each JSE instrument, JSE Market Lab:
- ingests price behavior, earnings context, liquidity conditions, and fee assumptions,
- applies explicit rules to detect and score setups,
- surfaces risk flags and confidence levels,
- translates outputs into allocation guidance and a portfolio plan.

Workflow:

`Data -> Signal -> Score -> Risk Flags -> Confidence -> Allocation -> Portfolio Plan`

## Product scope
### In scope
- Rule-based setup detection for listed JSE instruments.
- Tier A/B/C quality scoring with transparent logic.
- Cost-aware framing using Jamaican broker-fee and CESS assumptions.
- Earnings-phase and event-risk warning context.
- Allocation planning under cash and exposure constraints.
- Decision review outputs to support consistency and discipline.

### Non-goals
JSE Market Lab is **not**:
- financial advice,
- a prediction engine,
- an auto-trading or signal-selling service.

## Why this product is useful
- **Explainable:** outputs map to explicit rules rather than black-box predictions.
- **Decision-oriented:** the product supports judgment; it does not replace investor discretion.
- **Jamaican-market aware:** framing reflects local trading frictions, liquidity realities, and event risk.
- **Portfolio-ready artifact:** documentation shows end-to-end product thinking from problem framing through beta hardening.

## Key docs
- [Product brief](./docs/product_brief.md)
- [Feature breakdown](./docs/feature_breakdown.md)
- [Product decisions](./docs/product_decisions.md)
- [Iteration log](./docs/iteration_log.md)
- [Portfolio case study](./docs/portfolio_case_study.md)
- [User flow](./docs/user_flow.md)
- [UAT summary and links](./docs/uat/README.md)

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
