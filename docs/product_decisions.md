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
Users could interpret outputs but had no feedback on their own decisions.

### Decision
Add a post-decision evaluation layer focused on:
- behavior
- mistakes
- discipline

### Rationale
Improves:
- user learning
- trust in system
- differentiation from basic dashboards

### Trade-offs
- adds complexity
- requires careful tone control (no advisory language)

## Decision — Separate planning from review inside Portfolio Plan

### Context
When Decision Review was first added, it appeared inline with the main portfolio output.

This made the review layer feel secondary and mixed a forward-looking workflow with a backward-looking workflow.

### Decision
Portfolio Plan is split into two subtabs:
- Plan
- Review

### Rationale
This separates:
- planning decisions
- post-decision reflection

It makes the app flow clearer:
- Plan = what the system is doing now
- Review = how the decisions held up

### Outcome
The review layer now feels intentional rather than appended, and users can move between planning and reflection more naturally.

## Decision — Add interpretation to review outputs

### Context
The first version of Decision Review showed:
- discipline score
- behavior summary
- mistake list
- trade review table

However, this left a “so what?” gap. Users could see the review data but not clearly understand what it meant for their behavior.

### Decision
Add two interpretation sections to the Review tab:
- What this means
- What to improve

### Rationale
The review layer should not only detect mistakes. It should help users understand:
- what the detected behavior implies
- what kind of discipline gaps are showing up

This remains observational and non-advisory, while making the review output more useful.

### Outcome
Decision Review now supports reflection, not just detection.

## Decision — Group repeated mistake types in review output

### Context
The first review-layer version displayed repeated mistake entries line by line.

This made the review output noisy and harder to scan.

### Decision
Group repeated mistake types into count-based summary lines where possible.

Example:
- “3 trade(s) did not meet the quality tier rule.”

### Rationale
The goal of the review layer is clarity and learning, not log-style output.

Grouped mistakes reduce clutter and make patterns easier to understand.

### Outcome
Mistake presentation is cleaner, more readable, and better aligned with the product’s discipline-focused purpose.

## Decision — Sprint 11 review layer is observational, not judgmental

### Context
The Review & Discipline Layer evaluates user behavior against system rules.

That creates a tone risk: the feature could feel accusatory or overly prescriptive.

### Decision
Sprint 11 outputs must remain:
- observational
- neutral
- discipline-focused
- non-advisory

### Rationale
The product is a decision-support system, not a scolding tool.

The review layer should help users reflect on:
- whether they followed the system
- where discipline broke down
- what patterns are emerging

without becoming harsh or giving direct investment advice.

### Outcome
The review layer supports learning and trust rather than blame.

## Decision — Phase 1 ends with public readiness, not intelligence expansion

### Context
Advanced ideas were proposed for:
- earnings intelligence
- dividend intelligence
- news and qualitative data integration
- AI-assisted event interpretation

These ideas are valuable and strongly aligned with future differentiation.

### Decision
These features are deferred to Phase 2.

Sprint 12 closes Phase 1 by focusing on:
- usability
- clarity
- first-run understanding
- deployment
- public-ready product framing

### Rationale
Public readiness requires a stable, understandable, accessible product first.

Adding event-aware intelligence now would:
- expand scope too far
- delay public release
- increase complexity before the core experience is fully polished

### Outcome
The product launches as a clear decision-support system first, with a defined path for future intelligence expansion.

## Decision — Deployment is required for Sprint 12 completion

### Context
The dashboard currently runs through a local Streamlit workflow.

### Decision
Public deployment is a required Sprint 12 deliverable.

### Rationale
A public-ready product must be accessible without local setup.

This enables:
- portfolio use
- user testing
- public sharing
- product validation

### Outcome
Sprint 12 includes deployment to a public URL using Streamlit Community Cloud.

## Decision — Product positioning must stay away from pick-selling

### Context
The Jamaican market gap includes limited accessible research and strong appetite for guidance.

This creates a temptation to drift toward “top picks” or signal-selling behavior.

### Decision
Sprint 12 must reinforce the dashboard as:
- a decision-support product
- a structured analytics platform
- an education + execution tool

It must not present itself as:
- a recommendation engine
- a stock-pick subscription
- a hype-driven investor tool

### Rationale
This protects:
- credibility
- user expectations
- product trust
- long-term monetization quality

### Outcome
Public-ready messaging remains centered on structured decision-making rather than conviction-selling.

## Decision — Public deployment is part of Phase 1 completion

### Context
The dashboard had been usable only through a local Streamlit workflow.

### Decision
Phase 1 is not complete until the app is accessible through a public URL.

### Rationale
A public-ready product must remove technical setup friction for users.

This supports:
- easier testing
- easier sharing
- better validation
- stronger portfolio presentation

### Outcome
Sprint 12 includes deployment to Streamlit Community Cloud as part of product completion.

## Decision — Phase 2 intelligence features are deferred until after public-ready launch

### Context
Advanced ideas were proposed for:
- earnings intelligence
- dividend intelligence
- news and qualitative-data intelligence
- AI-powered event interpretation

### Decision
These ideas are deferred to Phase 2.

Sprint 12 remains focused on:
- clarity
- usability
- onboarding
- deployment
- public-ready positioning

### Rationale
The core product must be understandable and accessible before advanced intelligence layers are added.

### Outcome
Phase 1 ends with a clean, public-ready decision-support product, while Phase 2 becomes a clear expansion path.

## Decision — Use Jamaican-friendly English instead of generic finance language

### Context
The product is built for Jamaican users, but much of the current wording still sounds generic, technical, or globally templated.

### Decision
Sprint 12 introduces a language standard based on:
- simple, conversational English
- Jamaican-friendly tone
- explanation before numbers
- no slang-heavy phrasing
- no advisory language

### Rationale
The goal is to make the dashboard feel local, accessible, and easy to understand without reducing credibility.

### Outcome
The product becomes easier to use for everyday Jamaicans while still supporting analyst users through a separate mode.

## Decision — Beginner and Analyst modes should differ by language as well as detail

### Context
Different users need different levels of explanation and numerical detail.

### Decision
Sprint 12 Beginner vs Analyst mode should affect both:
- what information is shown
- how information is explained

### Rationale
A simple column toggle is not enough. The product should speak differently depending on the user’s needs.

### Outcome
Beginner Mode prioritizes clarity and meaning, while Analyst Mode keeps precision without losing readability.

## Sprint 13 product decisions

### 1. User stories drive structure
Sprint 13 is designed around what beginner and analyst users are scanning for, not around internal engine outputs.

### 2. Portfolio is the main decision surface
The Portfolio tab is treated as the primary “what do I do with this?” screen and must explain why trades are selected, why cash is reserved, and how trades are typically approached.

### 3. Execution framing is part of decision support
The dashboard should not stop at setup quality and holding periods. It must also explain entry reference, planned exit logic, and execution caveats in a rule-based, non-predictive way.

### 4. Median return is the primary typical-outcome metric
For this product, median return is treated as the primary “what usually happens” metric. Average return is supporting context only.

### 5. Analyst mode is deeper, not raw
Analyst mode should preserve richer detail, but still explain what grouped evidence is saying. It is not a license for confusing data dumps.

### 6. Empty or placeholder analytical sections reduce trust
Feature-level views that are not meaningful yet should be hidden or clearly explained, not left as confusing empty areas.

### 7. UI labels must be product-facing
Backend-style snake_case fields should not appear directly in the interface. User-facing labels must be readable and intentional.
