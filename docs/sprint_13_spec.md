# Sprint 13 — Decision Layer & Execution Framework

## Sprint Goal

Turn the dashboard from a stable public-facing analytics product into a clearer decision-support system by helping users understand:

- what they are supposed to do with the information
- why certain trades are selected
- what makes one setup stronger than another
- why some capital is held back
- how a trade would typically be executed
- what ticker behavior means without needing analyst-level interpretation

Sprint 13 is a **user understanding sprint** and an **execution framing sprint**.

It is not:
- a new data ingestion sprint
- a new strategy-model sprint
- a live data sprint
- a dividend/earnings intelligence sprint

---

## Why This Sprint Exists

Sprint 12 proved that the app can:
- load real bundled JSE data
- run reliably in a hosted environment
- preserve canonical ticker behavior
- separate beginner and analyst experiences
- present a cleaner product surface

But live review exposed major decision-layer gaps:

### 1. First-time users still ask:
- “What is a trader supposed to do with this?”
- “What do these tables mean?”
- “Why is some cash reserved?”
- “What makes this a strong setup?”

### 2. Ticker Analysis was too table-heavy
Even after improvements, users still need clearer interpretation.

### 3. Analyst Insights is under-defined
Some sections look empty, placeholder-like, or under-explained.

### 4. Execution framing is missing
The app explains:
- setup quality
- holding period behavior

But still does not answer clearly:
- what price reference is the entry based on
- what the planned exit logic is
- how execution should be interpreted in real conditions

### 5. Average return is still too prominent in places
For this product, median return should be the primary “typical outcome” metric.

---

## Product Principle

The app should not make users decode internal system labels or raw grouped tables.

Instead of showing:
- Tier A
- High confidence
- Reserved cash
- Avg Return
- raw matrices

the product should explain:
- why the setup is strong or weak
- what confidence means
- why some money is held back
- what the likely execution framework is
- what the data means in plain language

---

## Core Scope

### In scope
- user-story-driven Portfolio redesign
- Portfolio Snapshot
- Reserved Cash Explanation
- Setup Strength Translation
- Confidence Translation
- “Why this trade” explanations
- Execution Layer
- Ticker Analysis interpretation refinement
- Analyst Insights redesign / purpose clarification
- global display-label cleanup
- median-first presentation rule
- stronger Beginner vs Analyst separation

### Out of scope
- live market data
- user upload/data-mode system
- saved portfolio tracking
- external broker/API integration
- dividend intelligence
- earnings intelligence
- AI interpretation layer
- new signal-generation models

---

## Core User Stories

### Beginner user story
As a Jamaican retail investor with limited time and limited capital, I want to open the dashboard and quickly understand whether there are worthwhile trades, why they stand out, and how I would realistically approach them, so I can make more disciplined decisions.

### Analyst user story
As a more advanced user, I want to validate how the system behaves across setup quality, holding periods, execution framing, and trade outcomes, so I can judge whether the strategy logic looks reliable enough to trust.

### Portfolio user story
As a user viewing the Portfolio tab, I want to know which trades are strongest, why they were chosen, why some cash is not invested, and how the trade would typically be executed, so I can understand the plan without decoding internal system labels.

### Ticker Analysis user story
As a user viewing a ticker, I want to understand how that stock usually behaves, which holding style fits it best, what execution would generally look like, and what risks stand out, so I can interpret the stock’s behavior more clearly.

### Analyst Insights user story
As an analyst-mode user, I want grouped historical results to be explained in context, so I can understand what the performance groupings and exit behavior are saying instead of just seeing raw tables.

---

## User Questions Sprint 13 Must Answer

### Portfolio must answer:
- What are the best opportunities right now?
- Why were these selected?
- Why is some money not invested?
- How would this trade usually be executed?

### Ticker Analysis must answer:
- What is this stock generally like?
- Which holding style fits it best?
- What usually happens after a signal?
- What should I watch out for?

### Analyst Insights must answer:
- Does grouped historical evidence support the strategy?
- Which setup classes and holding periods look stronger?
- How do trades usually exit?
- Are there meaningful feature-level insights yet?

---

## Sprint Deliverables

### 1. Portfolio Snapshot block
A new interpretation-first block at the top of Portfolio explaining:
- how many trades were found
- how many were selected
- whether strong setups dominate
- whether cash is being held back intentionally

This should appear before the table.

---

### 2. Reserved Cash explanation
A dedicated block answering:
**Why is some capital not invested?**

Examples:
- not enough strong setups
- stronger risk controls applied
- mixed conditions
- avoiding forced trades

This should frame reserved cash as discipline, not as a system problem.

---

### 3. Setup Strength translation
Internal quality tiers must be translated into plain language.

Examples:
- Strong setup — more of the key conditions are aligned
- Mixed setup — some conditions are supportive, some are weaker
- Weak setup — risk is higher and quality is lower

---

### 4. Confidence translation
Confidence must be translated into meaning.

Examples:
- High confidence — similar setups have behaved more reliably in the past
- Medium confidence — history is mixed
- Low confidence — outcomes have been less reliable

This must stay non-predictive.

---

### 5. “Why this trade” explanation layer
Each trade should clearly explain:
- why it was selected
- why it ranked ahead of others
- whether volume/trend/quality conditions were supportive
- why it was held out if not selected

---

### 6. Execution Layer
A new rule-based execution framing layer.

The system should explain:
- **Entry reference**
- **Planned exit**
- **Typical outcome**
- **Execution risk**

#### Entry reference
Use signal-day close / signal-time reference language, not prediction.

#### Exit framework
Use the selected holding window / time-based exit logic.

#### Typical outcome
Use **median return** as the primary typical outcome metric.

#### Execution risk
Include spread/liquidity cautions where relevant.

This should appear in:
- Portfolio
- Ticker Analysis
- Analyst mode in richer form where appropriate

---

### 7. Median-first metric rule
The product should use:

- **Median return = primary “typical outcome” metric**
- **Average return = supporting context only**

If average differs meaningfully from median, explain that:
- a few large moves are affecting averages
- most trades cluster closer to the median

This rule should apply especially to:
- Portfolio summaries
- Ticker summaries
- execution framing
- analyst interpretation copy

---

### 8. Portfolio table cleanup
Portfolio should feel like a plan, not a raw report.

Needed improvements:
- cleaner labels
- explanation-first framing
- less dependence on users decoding internal fields
- clearer first-screen decision meaning

---

### 9. Ticker Analysis refinement
Ticker Analysis should continue the interpretation-first structure:

1. Quick Take
2. Best Holding Strategy
3. Risk Profile
4. What Usually Happens
5. What to Watch
6. Execution Behavior
7. Analyst Deep Dive (Analyst mode only)

Each remaining table must have a short explanation before it.

---

### 10. Analyst Insights redesign
Analyst Insights should stop feeling like a placeholder dump.

#### Feature Insights
- hide unless real meaningful feature-tag data exists
- or replace with a clear note that feature-level insight is not available yet

#### Performance Matrix
- explain what question it answers
- explain what grouped setup/holding-period behavior means

#### Exit Analysis
- explain how trades usually end
- simplify or hide if nearly everything is just a time-based exit

The tab should be deeper, but still interpretable.

---

### 11. Global display-label cleanup
Raw snake_case / backend labels must not leak into the UI.

Examples:
- holding_window → Holding Window
- win_rate → Win Rate
- avg_return → Average Return
- median_return → Median Return
- exit_reason → Exit Reason
- quality_tier → Setup Strength

This should be handled through shared display helpers where possible.

---

## UX Structure

### Portfolio target structure

1. Portfolio Snapshot
2. Capital Summary
3. Why some cash is reserved
4. Trade table / trade cards
5. Why this trade
6. Execution Summary
7. Optional deeper support in Analyst mode

### Ticker Analysis target structure

1. Quick Take
2. Best Holding Strategy
3. Risk Profile
4. What Usually Happens
5. What to Watch
6. Execution Behavior
7. Analyst Deep Dive

### Analyst Insights target structure

1. Strategy Summary
2. Performance Matrix
3. Exit Behavior
4. Feature Insights (only if meaningful)

---

## Beginner vs Analyst Behavior

### Beginner mode
- explanation-first
- lighter tables
- no empty or placeholder analytical sections
- no raw-table overload
- no backend-style labels
- median-first interpretation

### Analyst mode
- keeps richer tables
- still explains meaning before detail
- preserves grouped evidence and raw breakdowns where useful
- can show supporting counts and averages after the interpretation

---

## Files Likely Involved

- `app.py`
- `app/planner/portfolio_ui.py`
- `app/planner/explanations.py`
- `app/analysis/ticker_intelligence.py`
- `app/analysis/ticker_drilldown.py`
- `app/insights/embedded.py`
- `app/insights/analyst.py`
- new helper modules if useful:
  - `app/insights/portfolio_snapshot.py`
  - `app/insights/translation.py`
  - `app/insights/trade_explainer.py`
  - `app/insights/execution.py`
  - `app/ui/display_labels.py`

---

## UAT Focus

### Portfolio understanding
- user understands why trades are selected
- user understands setup strength
- user understands confidence
- user understands why cash is reserved
- user understands how a trade is intended to be executed

### Ticker understanding
- user understands the stock’s general behavior
- user understands which holding style looks strongest
- user understands execution behavior at a high level
- Beginner mode is not overwhelming

### Analyst understanding
- analyst sections answer clear questions
- Performance Matrix is interpretable
- Exit Analysis is interpretable
- empty / placeholder sections are hidden or explained

### Language / labels
- wording is simple and Jamaican-friendly
- no advisory language is introduced
- no snake_case labels leak into the UI
- median is primary where “typical outcome” is discussed

---

## Definition of Done

Sprint 13 is complete when a first-time user can open the Portfolio and Ticker Analysis sections and understand:

- why trades are selected
- what makes a setup stronger or weaker
- why some money is held back
- how the trade would typically be executed
- what the stock behavior means

without needing prior trading knowledge or analyst-level interpretation.
