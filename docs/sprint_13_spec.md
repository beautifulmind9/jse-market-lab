# Sprint 13 — Decision Layer, Execution Framework, and Adaptive Portfolio Understanding

## Sprint Goal

Turn the dashboard from a stable public-facing analytics product into a clearer decision-support system by helping users understand:

- what they are supposed to do with the information
- why certain trades are selected
- what makes one setup stronger than another
- why some capital is held back
- how a trade would typically be entered and exited
- how funded-trade count relates to opportunity quality and capital discipline
- what ticker behavior means without needing analyst-level interpretation
- whether the plan followed its own intended rules

Sprint 13 is a **user understanding sprint**, an **execution framing sprint**, and an **adaptive portfolio explanation sprint**.

It is not:
- a new data ingestion sprint
- a new strategy-model sprint
- a live data sprint
- a user upload / custom-data sprint
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

### 1. First-time users still asked:
- “What is a trader supposed to do with this?”
- “What do these tables mean?”
- “Why is some cash reserved?”
- “What makes this a strong setup?”

### 2. Ticker Analysis was still too table-heavy
Users still needed clearer interpretation and stronger execution framing.

### 3. Analyst Insights was under-defined
Some sections looked empty, placeholder-like, or under-explained.

### 4. Execution framing was missing
The app needed to answer more clearly:
- what entry reference is based on
- what the planned exit logic is
- how execution should be interpreted in real conditions

### 5. Average return was still too prominent in places
For this product, median return should be the primary “typical outcome” metric.

### 6. Portfolio funding felt too static
A visible “max funded trades: 3” style experience risked making the plan feel arbitrary rather than adaptive.

### 7. Review still felt too raw
The review surface needed to become a human-readable decision audit rather than a raw internal table.

---

## Product Principle

The app should not make users decode internal system labels or grouped backend tables.

Instead of showing:
- Tier A
- High confidence
- Reserved cash
- Avg Return
- raw matrices
- backend-style review fields

the product should explain:
- why the setup is strong or weak
- what confidence / reliability means
- why some money is held back
- how the trade would typically be approached
- what the data means in plain language
- whether the plan followed intended discipline

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
- adaptive funded-trade explanation
- Ticker Analysis interpretation refinement
- Analyst Insights redesign / purpose clarification
- Review tab redesign into a decision-audit surface
- global display-label cleanup
- median-first presentation rule
- stronger Beginner vs Analyst separation
- stability fixes required to keep Portfolio live and usable

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
As a Jamaican retail investor with limited time and limited capital, I want to open the dashboard and quickly understand whether there are worthwhile trades, why they stand out, why capital is being handled the way it is, and how I would realistically approach them, so I can make more disciplined decisions.

### Analyst user story
As a more advanced user, I want to validate how the system behaves across setup quality, holding periods, execution framing, grouped outcomes, and review discipline, so I can judge whether the strategy logic looks reliable enough to trust.

### Portfolio user story
As a user viewing the Portfolio tab, I want to know which trades are strongest, why they were chosen, why some cash is not invested, and how the trade would typically be entered and exited, so I can understand the plan without decoding internal system labels.

### Ticker Analysis user story
As a user viewing a ticker, I want to understand how that stock usually behaves, which holding style fits it best, what execution would generally look like, and what risks stand out, so I can interpret the stock’s behavior more clearly.

### Analyst Insights user story
As an analyst-mode user, I want grouped historical results to be explained in context, so I can understand what the performance groupings and exit behavior are saying instead of just seeing raw tables.

### Review / decision-audit user story
As a user reviewing the plan, I want to understand whether the strategy followed its own rules and where rank, quality, or liquidity discipline mattered, so I can trust the system more deeply.

---

## User Questions Sprint 13 Must Answer

### Portfolio must answer:
- What are the best opportunities right now?
- Why were these selected?
- Why is some money not invested?
- How would this trade usually be entered and exited?
- Why did the plan fund this many trades?

### Ticker Analysis must answer:
- What is this stock generally like?
- Which holding style fits it best?
- What usually happens after a signal?
- What should I watch out for?
- What does execution usually look like?

### Analyst Insights must answer:
- Does grouped historical evidence support the strategy?
- Which setup classes and holding periods look stronger?
- How do trades usually exit?
- Are there meaningful feature-level insights yet?

### Review must answer:
- Did the plan follow intended rules?
- Where did discipline matter?
- What happened when tradeoffs occurred?

---

## Sprint Deliverables

### 1. Portfolio Snapshot block
Interpretation-first block explaining:
- how many trades were found
- how many were funded
- whether strong setups dominate
- whether cash is being held back intentionally
- whether capital is being concentrated or spread across stronger setups

---

### 2. Reserved Cash explanation
Dedicated block answering:
**Why is some capital not invested?**

Framed as discipline, not as a system problem.

Examples:
- not enough strong setups
- stronger-ranked trades consumed disciplined capital
- stronger controls prevented forced trades
- mixed conditions led to reserve behavior

---

### 3. Setup Strength translation
Internal quality tiers translated into plain language.

Examples:
- Strong setup — more of the key conditions are aligned
- Mixed setup — some conditions are supportive, some are weaker
- Weak setup — risk is higher and quality is lower

---

### 4. Confidence / Reliability translation
Confidence translated into meaning.

Examples:
- High confidence — similar setups have behaved more reliably in the past
- Medium confidence — history is mixed
- Low confidence — outcomes have been less reliable

This remains non-predictive.

---

### 5. “Why this trade” explanation layer
Each trade should explain:
- why it was selected
- how ranking / quality supported it
- whether it was held out due to stronger-ranked trades, quality rules, or liquidity rules

---

### 6. Execution Layer
Rule-based execution framing layer.

The system should explain:
- **Entry reference**
- **Planned exit**
- **Typical outcome**
- **Execution risk**

#### Entry reference
Use signal-day close / reference-area language, not prediction.

#### Planned exit
Use explicit holding-window language such as:
- 5 trading days
- 10 trading days
- 20 trading days
- 30 trading days

#### Typical outcome
Use **median return** as the primary typical outcome metric.

#### Execution risk
Include spread / liquidity cautions where relevant.

This should appear in:
- Portfolio
- Ticker Analysis
- Analyst mode in richer form where appropriate

---

### 7. Median-first metric rule
The product should use:
- **Median return = primary “typical outcome” metric**
- **Average return = supporting context only**

If average differs meaningfully from median, explain that a few large moves are affecting the average.

---

### 8. Portfolio table cleanup
Portfolio should feel like a plan, not a raw report.

Needed improvements:
- cleaner labels
- explanation-first framing
- clearer holding-window / exit language
- less dependence on users decoding internal fields

---

### 9. Adaptive funded-trade behavior
Portfolio funding should no longer feel permanently fixed at 3 trades.

Funding should now be explained as adaptive to:
- setup quality
- rank order
- capital discipline
- reserve behavior

Beginner mode keeps disciplined defaults.
Analyst mode may expose a controlled trade-count cap override without bypassing hard quality rules.

---

### 10. Ticker Analysis refinement
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

### 11. Analyst Insights redesign
Analyst Insights should stop feeling like a placeholder dump.

#### Feature Insights
- hide unless meaningful feature-tag data exists
- otherwise explain clearly that feature-level insight is not available yet

#### Performance Matrix
- explain what question it answers
- explain what grouped setup / holding-period behavior means

#### Exit Analysis
- explain how trades usually end
- simplify or clearly explain if time-based exits dominate

---

### 12. Review redesign into Decision Audit
Review should stop feeling like a backend table.

Replace raw review output with a decision-audit surface that answers:
- what happened
- whether rules were followed
- why it matters

Preferred audit columns:
- Ticker
- Status
- What happened
- Why it matters

---

### 13. Global display-label cleanup
Raw snake_case / backend labels must not leak into the UI.

This should be handled through shared display helpers where possible.

---

### 14. Stability hardening
Sprint 13 also includes the stability work required to keep the new user-facing surfaces live and usable, including:
- compact execution-summary crash fixes
- sentence-splitting hardening
- holding-window propagation restoration
- safe fallback behavior for missing planned-exit text

---

## UX Structure

### Portfolio target structure
1. Portfolio Snapshot
2. Capital Summary
3. Why some cash is reserved
4. Funded Trades
5. Unfunded Trades
6. Funding approach / rules
7. Optional deeper support in Analyst mode

### Review target structure
1. Summary interpretation
2. What to improve
3. Mistakes detected
4. Decision Audit table

### Ticker Analysis target structure
1. Quick Take
2. Best Holding Strategy
3. Risk Profile
4. What Usually Happens
5. What to Watch
6. Execution Behavior
7. Analyst Deep Dive

### Analyst Insights target structure
1. Strategy-validation framing
2. Performance Matrix
3. Exit Analysis
4. Feature Insights (only if meaningful)

---

## Beginner vs Analyst Behavior

### Beginner mode
- explanation-first
- lighter tables
- no empty / placeholder analytical sections
- no raw-table overload
- no backend-style labels
- median-first interpretation
- no manual funded-trade override

### Analyst mode
- keeps richer tables
- still explains meaning before detail
- preserves grouped evidence and deeper breakdowns
- can show supporting counts and averages after interpretation
- may expose a controlled funded-trade cap override

---

## UAT Focus

### Portfolio understanding
- user understands why trades are selected
- user understands setup strength
- user understands confidence / reliability
- user understands why cash is reserved
- user understands how the trade is intended to be entered and exited
- user understands that funded-trade count is adaptive, not arbitrary

### Ticker understanding
- user understands the stock’s general behavior
- user understands which holding style looks strongest
- user understands execution behavior at a high level
- Beginner mode is not overwhelming

### Analyst understanding
- analyst sections answer clear questions
- Performance Matrix is interpretable
- Exit Analysis is interpretable
- empty / placeholder sections are hidden or clearly explained

### Review understanding
- users can understand what happened in the audit
- users can understand why discipline mattered
- review wording does not invert or confuse the meaning of rule checks

### Language / labels
- wording is simple and Jamaican-friendly
- no advisory language is introduced
- no snake_case labels leak into the UI
- median is primary where “typical outcome” is discussed

---

## Definition of Done

Sprint 13 is complete when a first-time user can open the Portfolio, Review, and Ticker Analysis sections and understand:

- why trades are selected
- what makes a setup stronger or weaker
- why some money is held back
- how the trade would typically be approached
- what the stock behavior means
- whether the plan followed intended discipline

without needing prior trading knowledge or analyst-level interpretation.

Sprint 13 closes with the app live and ready for beta testing, with remaining minor issues treated as beta hardening rather than unfinished feature scope.
