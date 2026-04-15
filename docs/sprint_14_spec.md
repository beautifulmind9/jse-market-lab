# Sprint 14 — Onboarding, Clarity, and Guided Product Flow

## Sprint Goal

Make the dashboard easier to understand on first load by improving onboarding, reducing text overload, clarifying section purpose, refining product language, and turning the app into a more guided decision-support experience.

Sprint 14 is not about changing the trading model.

It is about helping users quickly understand:
- what this dashboard is
- what it helps them do
- where to start
- what each section is for
- how to use the information with more confidence

---

## Why this sprint exists

Beta feedback exposed a clear pattern:

### 1. The product is useful, but first-time clarity is still weak
Users are still asking:
- “What is this page about?”
- “What am I supposed to do first?”
- “Beginner to what?”
- “What conditions are being used to come up with the recommendations?”

### 2. Too much explanation is visible at once
The current UI has:
- long vertical reading
- repeated explanation blocks
- too much always-visible text
- not enough progressive disclosure

### 3. Product language still needs refinement
The product should sound:
- confident
- specific
- useful
- historically grounded

It should avoid:
- vague phrases like “based on past data”
- defensive language focused on what the product does not do
- unclear dataset-period claims like “since 2018” when the active dataset may not actually support that

### 4. Some deeper surfaces still feel underdefined
This applies especially to:
- Feature Insights
- Performance Matrix
- Exit Analysis
- Decision Audit / Review evolution

### 5. The app needs to use Streamlit widgets more intentionally
The current product still relies too heavily on:
- headings
- full-width text
- always-visible tables

It needs more:
- expanders
- columns
- metrics
- compact cards
- guided view vs advanced view branching

---

## Sprint Theme

**From product explanation to product guidance**

This sprint is about helping the user feel:
- oriented
- guided
- less overwhelmed
- more confident about how to use the dashboard

---

## Core Product Principle

The product should lead with:
- what users can do
- what the system highlights
- what the analysis helps them understand

The product should not rely on:
- negative framing
- vague references to historical data
- long first-run reading before users reach the actual decision surfaces

---

## In Scope

### Homepage / onboarding
- redesign top-of-page onboarding
- shorten visible first-run content
- embed the Start Here video prominently
- add a simple “Where to start” guide
- add optional explanation expanders
- improve first-load mobile readability

### View naming / product framing
- Guided View replaces Beginner in user-facing naming
- Advanced View replaces Analyst in user-facing naming
- add helper text explaining the difference
- preserve internal behavior as needed

### Product language refinement
- replace defensive/negative phrasing with positive, useful framing
- make system explanations more specific
- describe evaluation factors clearly
- make data source period wording dynamic or dataset-aware

### Portfolio tab clarity
- lighter, cleaner flow
- more widget-based layout
- shorter visible explanation
- metrics-led snapshot
- better use of expanders
- Guided View lighter by default

### Review / Decision Audit direction
- preserve current review usefulness
- clarify purpose in the UI
- define next-step evolution toward more transparent selection logic

### Ticker Analysis clarification
- keep interpretation-first structure
- increase section clarity
- reduce raw-table overload in Guided View

### Advanced View / Analyst Insights clarification
- better define:
  - Feature Insights
  - Performance Matrix
  - Exit Analysis
- make each section answer a clear question
- reduce “dead page” or “placeholder” feeling

### Widget-led UI cleanup
- expanders
- columns
- metrics
- info / warning blocks
- more progressive disclosure

---

## Out of Scope

- changing ranking logic
- changing allocation outcomes
- changing execution calculations
- new signal-generation logic
- new dataset ingestion mode
- user-uploaded datasets
- monetization features
- portfolio persistence
- broker integrations
- earnings intelligence
- dividends intelligence

These remain outside Sprint 14 scope.

---

## Core User Stories

### First-time user story
As a first-time user, I want to understand what the dashboard is for and where to start within a few seconds, so I do not feel lost or overwhelmed.

### Guided View user story
As a less advanced user, I want a simpler view that shows me what matters first and hides unnecessary detail, so I can use the dashboard without needing analyst-level knowledge.

### Advanced View user story
As a more advanced user, I want deeper grouped evidence and analytical detail, but I still want each section to explain what question it is answering.

### Trust / methodology user story
As a user, I want the dashboard to explain what factors are used and what period of data is being analyzed, so I can trust how the output is being produced.

### Product flow user story
As a user, I want the app to guide me through what to look at first, second, and third, so using the dashboard feels like a process and not a random collection of tabs.

---

## What Sprint 14 must answer

### Homepage must answer
- What is this?
- What does it help me do?
- Where do I start?
- How do I learn it quickly?

### Portfolio must answer
- What is happening right now?
- Why are these trades funded?
- Why is some cash reserved?
- What should I focus on first?

### Ticker Analysis must answer
- What is this section for?
- What behavior should I look for?
- What does risk mean here?
- What does execution behavior help me understand?

### Advanced View must answer
- What is different from Guided View?
- What am I validating here?
- What does each deeper section help me compare?

### Methodology must answer
- What factors are being used?
- Over what dataset period?
- How are opportunities being compared?

---

## Sprint Deliverables

### 1. Homepage / onboarding redesign
Top of app should be reduced to:
- title
- one-line description
- embedded Start Here video
- where-to-start guide
- optional explanation expanders

### 2. Guided View / Advanced View naming refinement
Replace confusing mode naming with clearer user-facing labels and short helper text.

### 3. Product voice upgrade
All core user-facing language should:
- lead with value
- emphasize guidance using historical patterns
- avoid vague “past data” phrasing
- avoid incorrect hard-coded date claims

### 4. Methodology explanation block
A clear explanation of:
- price behavior
- volume participation
- volatility
- liquidity
- realized outcomes / historical consistency

with dataset-period wording tied to the actual active dataset, not a hard-coded year claim.

### 5. Widget-led homepage cleanup
Use:
- expanders
- columns
- metrics
- cards / compact blocks
to reduce always-visible reading.

### 6. Portfolio surface cleanup
Portfolio should:
- use snapshot metrics
- shorten visible explanation
- use expanders for glossary and rules
- keep Guided View lighter
- keep Advanced View deeper

### 7. Review tab clarification
Clarify that Review is a discipline / decision-audit surface.
Also define the next-step direction for a more transparent numeric selection-audit layer in a later sprint.

### 8. Ticker Analysis clarification
Continue reducing overload and ensuring each section answers a clear question.

### 9. Advanced View section clarification
Feature Insights, Performance Matrix, and Exit Analysis should each explain:
- what question they answer
- why they matter
- what the user is supposed to do with them

### 10. Feature Insights interim handling
Improve the “not available” state so it feels informative rather than dead or broken.

---

## Section-specific design direction

### Homepage
Use compact scan-friendly layout and progressive disclosure.

### Portfolio
Use metrics, compact interpretation, lighter Guided View, and smaller visible rule burden.

### Review
Keep it human-readable and purposeful.

### Ticker Analysis
Interpretation first, dense detail later.

### Advanced View
Deeper evidence, but still guided.

---

## Data Source / Period Rule

Do not hard-code “since 2018” unless the active dataset truly supports it.

Use one of these approaches:
- dynamic range from dataset min/max date
- or safe wording such as:
  “using historical JSE data available in the current dataset”

This is required for trust and accuracy.

---

## Definition of Done

Sprint 14 is complete when:
- a first-time user can understand what the dashboard is and where to start quickly
- Guided View feels lighter and easier to scan
- Advanced View feels deeper without feeling purposeless
- the product uses more widgets and less always-visible long reading
- user-facing language feels specific, confident, and historically grounded
- data source / time range messaging is no longer misleading
- the app feels more guided and less like a dense stack of explanations

Sprint 14 closes when the product feels easier to enter, easier to scan, and easier to trust.
