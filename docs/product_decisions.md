# Product Decisions

## Median vs Average
Median is used to reduce sensitivity to extreme values and outliers.

## Tier System (A/B/C)
- Tier A/B prioritized for trading
- Tier C tracked but not used for income strategies

## Liquidity Filter
Ensures trades are realistic and executable.

## Cost Inclusion
All returns are net of fees and CESS to reflect real outcomes.

## Earnings Warnings
Warnings are shown instead of blocking trades to preserve user agency.

## UI Philosophy
- Decision support, not signal pushing
- Clear, minimal, structured

## Decision Guidance Philosophy
Guidance is provided as optional decision support, not as automatic execution logic. The system suggests possible responses to risk while preserving user agency.

## Language Localization Decision
Guidance should sound natural to Jamaican users without using patois or overly foreign financial language. The product uses a Clear mode for everyday readability and a Pro mode for more concise interpretation. Both modes should remain locally understandable.

## Guidance Mode Ownership
Clear vs Pro guidance is controlled at the planner level, not inside each trade card. This keeps the UI stable, avoids repeated widget creation, and applies one consistent reading mode across a planner view.

## Confidence Layer Philosophy
The confidence layer converts signals and risk factors into a clear prioritization system. It does not predict outcomes but helps users decide which trades deserve attention and capital first.

## Allocation Philosophy
The allocation layer uses simple, rule-based sizing to prioritize stronger trades while preserving cash and limiting exposure. It is designed to support disciplined portfolio decisions, not optimize returns through complex models.

## Validation Layer Philosophy
The dashboard should not only produce decisions but also provide analyst-facing views that help validate whether current rules, filters, and setup classifications are supported by historical behavior.
