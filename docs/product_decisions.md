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

## Product Surface Philosophy
The engine is not enough on its own. The dashboard must present outputs in a way that lets users understand funded trades, unfunded trades, cash reserve, and allocation reasoning at a glance.

## Decision — Portfolio surface must separate comparison from explanation

### Context
Sprint 14 improved overall UI clarity, onboarding, and Guided vs Advanced structure.

However, the initial implementation revealed a key usability issue:

Advanced portfolio tables contained important fields that were only visible through horizontal scrolling.

This created a risk where users could miss critical decision information such as:
- why a trade was selected or not funded
- holding window context
- allocation reasoning

### Decision
The portfolio surface must follow this structure:

**comparison first, explanation second**

This means:
- essential decision fields must be visible without horizontal scrolling
- deeper reasoning should be accessible through drilldowns or expanders
- full raw tables should exist only as optional analyst depth

### Implementation direction

#### Guided View
- uses compact trade cards
- shows core fields immediately
- moves secondary details into collapsed sections

#### Advanced View
- uses a compact comparison table for first-pass scanning
- provides row-level drilldowns for detailed reasoning
- includes a full analyst table only as an optional secondary surface

### Rationale
This structure:
- improves scanability
- reduces cognitive load
- prevents hidden critical information
- preserves analytical depth without overwhelming users

### Outcome
The portfolio becomes a true decision surface rather than a data display.

Users can:
- compare trades quickly
- understand why trades appear
- access deeper reasoning only when needed

## Decision — Phase 2A focused on clarity before workflow connection

### Context
After public-beta release, the next risk was not lack of engine capability. It was user confusion.

Observed issues included:
- product identity confusion
- capital input confusion
- uncertainty about what to do first
- risk of treating the dashboard like a static report instead of an interactive planning tool

### Decision
Phase 2 begins by improving:
- first-run clarity
- onboarding structure
- scanability
- product identity
- portfolio readability

before introducing deeper connected workflow behavior.

### Rationale
Users must first understand:
- what the dashboard is
- what the portfolio is for
- where to start
- what inputs belong to them

before more advanced workflow links are added.

### Outcome
Sprint 13 and Sprint 14 prioritize clarity and interpretation first, creating the base for a more connected decision journey later.

## Decision — Capital input must read as user-owned

### Context
User feedback showed that at least one tester did not understand that the capital field referred to their own money.

This made the Portfolio surface feel more like a report than a planning tool.

### Decision
The capital input must use user-owned wording and visible directional support.

### Implementation direction
- use wording such as `Enter your investment amount (JMD)`
- include helper text explaining that this is the amount the user wants to allocate across trades
- add a visible cue near the top of Portfolio that tells the user where to start

### Rationale
This reinforces:
- ownership
- interactivity
- planning intent

### Outcome
The Portfolio tab becomes easier to understand as a user-driven planning surface.

## Decision — Product state wording must be accurate to loaded data

### Context
Users asked whether the system updates or changes after trades are followed.

The current product does not yet support true user-facing refresh or user-controlled date-range regeneration of opportunity sets.

### Decision
System-behavior wording must stay accurate to the current product state.

### Implementation direction
Use wording that explains the plan is built from the currently loaded market data, without implying:
- live updates
- on-demand refresh
- user-controlled regeneration of opportunities

### Rationale
Trust depends on not overstating system behavior.

### Outcome
The UI remains transparent and credible while the product is still in a validation stage.

## Decision — Phase 2B should connect Portfolio to Ticker Analysis

### Context
By the end of Sprint 14, the main clarity and scanability problems were largely resolved.

At that point, the next product gap becomes workflow continuity rather than basic explanation.

Ticker Analysis is one of the clearest and strongest product surfaces, while Portfolio is the main decision surface.

### Decision
The next workflow improvement should connect Portfolio directly to Ticker Analysis.

### Rationale
This turns the product journey into:
- Portfolio = what was selected
- Ticker Analysis = why this stock deserves attention

It reduces friction and strengthens the feeling of one connected decision-support system.

### Outcome
Sprint 15 should focus on workflow connection rather than another general clarity pass.

## Decision correction: public-facing insight prompts are not automatically in-app scope

A prompt was defined to generate:
- 3–5 key insights
- anything surprising or unexpected
- common mistakes the data reveals
- a short explanation of one feature and why it exists

This prompt is useful for public sharing and marketing support, but it should not be assumed to represent the next in-app sprint scope by default.

This output can serve three different purposes:
1. marketing/content generation
2. public documentation and sharing
3. a future in-app explanation layer

The product team should explicitly decide which of these is in scope before assigning it as implementation work.

### Current decision
At this stage, the prompt is recognized primarily as a **content/communication aid** unless intentionally promoted into the app roadmap.

## Decision: marketing insight data needs do not automatically define app sprint scope

A requirement emerged to generate simple public-facing insights such as:
- 3–5 key insights
- anything surprising or unexpected
- common mistakes the data reveals
- short explanation of one feature

This requirement was created for marketing/public-sharing support.

Because of that, the need for real historical data in that workflow does not automatically mean the next app sprint must replace demo data as the default visible source.

### Current interpretation
- real historical data may be needed for credible external insight generation
- app-level replacement of demo-default behavior remains a separate product decision
- marketing input needs and app implementation priorities should be evaluated independently

## Decision — Introduce Review Layer

### Context
Sprint 14 improved overall UI clarity, onboarding, and Guided vs Advanced structure.

However, the initial implementation revealed a key usability issue:

Advanced portfolio tables contained important fields that were only visible through horizontal scrolling.

This created a risk where users could miss critical decision information such as:
- why a trade was selected or not funded
- holding window context
- allocation reasoning

### Decision
The portfolio surface must follow this structure:

**comparison first, explanation second**

This means:
- essential decision fields must be visible without horizontal scrolling
- deeper reasoning should be accessible through drilldowns or expanders
- full raw tables should exist only as optional analyst depth

### Implementation direction

#### Guided View
- uses compact trade cards
- shows core fields immediately
- moves secondary details into collapsed sections

#### Advanced View
- uses a compact comparison table for first-pass scanning
- provides row-level drilldowns for detailed reasoning
- includes a full analyst table only as an optional secondary surface

### Rationale
This structure:
- improves scanability
- reduces cognitive load
- prevents hidden critical information
- preserves analytical depth without overwhelming users

### Outcome
The portfolio becomes a true decision surface rather than a data display.

Users can:
- compare trades quickly
- understand why trades appear
- access deeper reasoning only when needed

---

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

## Product Surface Philosophy
The engine is not enough on its own. The dashboard must present outputs in a way that lets users understand funded trades, unfunded trades, cash reserve, and allocation reasoning at a glance.
