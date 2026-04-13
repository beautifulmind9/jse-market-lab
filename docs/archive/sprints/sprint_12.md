# Sprint 12 — Public-Ready Product

## Goal
Make the JSE Dashboard ready for public use by improving clarity, first-run understanding, deployment, and product framing.

---

## Context
The product now includes:
- signal engine
- allocation engine
- explanation layer
- embedded insights
- ticker analysis and drilldown
- review & discipline layer

The system works, but it still needs:
- a cleaner public-facing experience
- simplified entry for first-time users
- clearer product positioning
- deployment to a public URL

Sprint 12 is the final Phase 1 sprint.

---

## Core objective
Turn the dashboard from a working internal tool into a public-ready decision-support product that users can open from a link and understand quickly.

---

## Scope

### 1. Public-ready UI refinement
- improve spacing and layout
- reduce clutter
- remove redundant labels or repeated information
- keep structure consistent across tabs and views

---

### 2. Final insight structure
Each run should present a clear public-ready insight block made up of:

#### What’s happening
- 2–3 simple observations about current conditions

#### What to watch
- 2–3 clear risk or instability signals

#### Common mistakes
- 1–2 behavioral warnings or pitfalls

#### Feature explanation
- 1 short explanation of a core feature or concept

These should remain:
- observational
- non-advisory
- simple
- useful for both product understanding and public demo purposes

---

### 3. Beginner vs Analyst mode
Introduce a clearer split between:

#### Beginner Mode
- fewer columns
- simpler wording
- more guidance
- focus on understanding and decision clarity

#### Analyst Mode
- full tables
- detailed metrics
- richer breakdowns
- focus on depth and validation

---

### 4. First-run experience
The first experience should:
- load with demo data automatically
- open into a sensible default view
- show useful insight immediately
- require no technical setup

The product should feel understandable within the first few seconds.

---

### 5. Language standardization
All user-facing language should be reviewed and simplified so it feels:
- clear
- natural
- Jamaican-friendly
- not slang-heavy
- not overly technical

The goal is not Patois.
The goal is plain, familiar English that feels local and easy to follow.

---

### 6. Product framing and monetization surface
Sprint 12 should introduce clear product framing inside the experience:

#### Free tier (light surface)
- simplified view
- limited features
- education and trust-building

#### Pro tier (future main product)
- full signal rankings
- portfolio planning
- deeper decision support

This should be presented lightly.
No aggressive paywall behavior is needed in Sprint 12.

---

### 7. Deployment
The dashboard must be accessible through a public link.

#### Requirements
- root `app.py` remains the entry point
- `requirements.txt` includes all required dependencies
- demo dataset is bundled
- no local-only file paths break deployment
- public app loads successfully

Deployment target for Sprint 12:
- Streamlit Community Cloud

---

## Out of scope
The following are intentionally deferred to Phase 2:
- AI summarization
- earnings intelligence
- dividend intelligence
- event-aware overlays
- news ingestion
- qualitative-data intelligence layer

---

## Product positioning guardrail
Sprint 12 must reinforce that the dashboard is:
- a decision-support platform
- a structured analytics tool
- a risk-aware trading framework

It must not drift into:
- pick selling
- recommendation service behavior
- hype-style investor messaging

---

## Outcome
After Sprint 12, users should be able to:
- open the app from a public link
- understand what the product does quickly
- explore opportunities and risk clearly
- use the product without technical setup
- experience a product that feels structured, credible, and public-ready

## 8. Language System + Mode Differentiation

Sprint 12 introduces a shared language system so the dashboard feels clear, consistent, and Jamaican-friendly across major user-facing surfaces.

### Core language principles
- simple, conversational English
- not Patois
- not academic
- not jargon-heavy
- short and direct
- explanation before numbers
- observational, not advisory

### Translation approach
Technical terms should be translated into familiar language where possible.

Examples:
- Win Rate → How often this works
- Median Return → Typical return
- Volatility → How much price moves
- Liquidity Filter → Enough trading activity
- Cooldown → Wait time before next trade
- Tier A → Strong setup
- Tier B → Decent setup
- Tier C → Weak setup

### Mode differentiation

#### Beginner Mode
- fewer numbers
- simpler wording
- focus on meaning and risk
- minimal technical phrasing

#### Analyst Mode
- explanation first
- key metrics second
- includes percentages and holding-window detail
- still avoids unnecessary jargon

### Sprint 12 implementation focus
The language system should first be applied to:
- first-run header
- insight sections
- Portfolio Plan
- Decision Review
- Ticker Analysis summaries

A broader full-app wording pass can continue later if needed.