# JSE Project Master Context

## Project identity
JSE Market Lab is a decision-support dashboard for the Jamaican Stock Exchange.

It is designed to help users make more structured trading decisions using historical market behavior, ranking logic, risk checks, and portfolio-allocation rules.

This product is not positioned as a signal-selling service. It is a decision-support tool that helps users review opportunities with more structure, clarity, and context.

---

## Core product goal
Transform the dashboard into:
- a decision-support platform for short- to medium-term trading
- an education tool for Caribbean investors
- a scalable product for monetization
- a portfolio-management aid for income generation

The platform should support:
- flexible capital allocation
- multiple holding periods
- risk-aware decision making
- realistic costs and execution constraints

---

## Core philosophy
- Decision support, not hype
- Structured guidance based on historical behavior
- Real-world execution constraints matter
- Trust comes from clarity, specificity, and transparency
- Simplicity for newer users, depth for advanced users
- Guidance should focus on what the user can do with the information
- Product language should avoid vague or defensive phrasing

---

## Core system flow
Data -> Signal -> Score -> Risk -> Confidence -> Allocation -> Portfolio Plan

---

## What the dashboard already does
- Scrapes and uses JSE market data
- Generates median crossover signals
- Applies liquidity and cooldown rules
- Backtests across multiple holding windows
- Scores opportunities using quality tiers (A/B/C)
- Provides Portfolio, Review, Ticker Analysis, Analyst/Advanced views
- Uses ranking and allocation logic to determine funded and unfunded trades
- Includes explanation layers to help users understand why trades appear

Tier C setups are tracked but not prioritized for income-focused strategies.

---

## Strategy concepts that must remain consistent
The product should consistently use and explain:
- holding windows (5D, 10D, 20D, 30D)
- win rate
- median return
- average return as supporting context
- cooldown
- volume confirmation
- spread widening
- volatility buckets
- quality tiers
- liquidity filters
- broker fee + CESS trading cost assumptions

Explanations should be beginner-friendly but still accurate.

---

## Trading cost assumptions
Weekly Trade Planner / portfolio assumptions currently use:
- Broker fee: 0.50%
- CESS: 0.35%

Outputs should reflect net trading reality where relevant.

---

## Portfolio framework
Assume:
- hybrid income strategy
- short + medium-term trades
- capital split across multiple positions
- Tier A and B prioritized
- Tier C monitored but not prioritized

Advice and product language should emphasize risk management and sustainable growth.

---

## UX and language principles
- Use simple Jamaican-friendly English, not Patois
- Avoid sounding academic, robotic, or over-explained
- Do not overload users with long reading everywhere
- Break content into clearer sections, cards, expanders, or side content when helpful
- Keep the main flow focused on what the user needs to do next
- Move secondary information into collapsed/optional areas
- Avoid negative framing such as focusing on what users cannot do
- Be specific about what factors the system uses
- If the dataset period changes, wording should be dataset-aware and not hard-coded incorrectly

---

## Current UI direction
The product has been moving from a text-heavy beta interface toward a clearer guided experience.

Recent UI decisions include:
- Beginner / Analyst renamed to Guided View / Advanced View
- Start Here / onboarding video embedded near the top
- “Where to start” cards added
- Guided View simplified for scanability
- Secondary explanatory content moved into expanders
- Guided portfolio surfaces shifted toward metric-first and lighter presentation
- Mobile readability prioritized

---

## Important product learnings from building so far
### 1. Users need clearer product identity
Some users may read the dashboard like a report instead of an interactive decision tool.

Implication:
The product must clearly show when the user is meant to input their own capital and use the outputs as a planning aid.

### 2. Capital input needs clearer labeling
A user did not immediately understand that the capital input referred to their own money.

Recommended fix direction:
- Rename “Total Capital” to something closer to “Enter your investment amount (JMD)”
- Add helper text explaining what the input is used for

### 3. Tab order should follow user mental flow
Feedback suggested Review should likely come later in the flow.

Recommended flow:
- Portfolio
- Ticker Analysis
- Review
- Advanced surfaces where appropriate

### 4. System behavior needs explanation
A user asked whether the information changes after following trades.

Implication:
The product should clearly explain that the plan is based on current available market data and can be refreshed as new data is captured.

### 5. Guided vs Advanced segmentation is working
A user understood Guided View and found Advanced View deeper/harder, which is acceptable.

Implication:
The segmentation is serving its purpose.

### 6. Ticker Analysis is a strong entry point
User feedback suggests Ticker Analysis feels intuitive and engaging.

Implication:
Ticker Analysis may be one of the product’s strongest hook features.

### 7. Current structure is not overwhelming
Feedback indicated the dashboard is understandable in Guided View and not overwhelming.

Implication:
The product does not need another full redesign. It needs focused clarity and validation work.

---

## Known UX / product direction themes
- Users should understand what the dashboard is quickly
- Users should know where to start without needing outside explanation
- The dashboard should feel like a tool that supports decisions, not just an information display
- Trust should come from clear factor explanations, data-scope clarity, and visible reasoning
- Advanced tabs should clearly explain what question each section answers
- Review should eventually become a more transparent decision-audit surface

---

## Decision Audit direction (future direction)
The current Review / Decision Audit area should evolve over time.

Near term:
- human-readable review of how ranking, quality, and liquidity rules were applied

Later phase:
- clearer numeric or semi-numeric transparency into selection logic
- more visible explanation of what the system looked at when selecting or not funding trades

---

## Analyst / Advanced surfaces needing continued clarification
These sections have required product clarification work:
- Feature Insights
- Performance Matrix
- Exit Analysis

The key question for each section is:
- what is this page for?
- what is the user supposed to look at?
- how does it help with decisions?

---

## Validation mindset going forward
The product is now in a validation loop, not just a feature-building loop.

Main question:
Can someone open the dashboard and understand what to do without outside explanation?

Ongoing validation should capture:
- confusion points
- what users ignore
- what they naturally engage with
- what they misinterpret
- what increases trust

---

## Suggested working rhythm for future chats
When opening a new project chat, use this file as baseline context.

Then add one of:
- current sprint goal
- current UX problem
- current product decision to make
- current user feedback round

This helps new chats start with correct project memory and avoids repeating the full history.
