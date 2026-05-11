# Platform Information Architecture & User Journeys — JSE Market Lab

## Purpose

This document defines the user-centered information architecture for JSE Market Lab now that the product has evolved beyond a dashboard.

The earlier migration-era sequence:

```text
Start Here → Demo Mode → Portfolio Plan → Ticker Analysis → Review → Platform Preview
```

was useful for proving the Vercel/Render migration, but it should not become the long-term website structure.

JSE Market Lab is now positioned as a broader platform for:

- market intelligence
- research
- decision support
- investor education
- income/dividend context
- setup testing and simulation, future
- brokerage-access education, future and compliance-gated
- AI-assisted explanation workflows, future and compliance-gated
- monetization through education/research/product tiers, future

The website should be organized around how users come to the platform, not around the order the product was built.

---

## Core Product Principle

JSE Market Lab should answer user intent:

```text
What am I trying to do today?
```

not simply:

```text
Which dashboard page do I open next?
```

The platform must remain decision-support only.

It must not:

- recommend buy/sell actions
- guarantee outcomes
- imply certainty
- execute trades
- hold client funds
- recommend a broker as best
- imply official JSE authorization before confirmed
- publish unverified broker or market-data claims as final

---

## Primary User Intents

Users may arrive with different needs.

### 1. I want to learn how the JSE works

This user needs education, definitions, examples, and simple explanations.

Likely user:

- beginner investor
- student
- young professional
- diaspora investor new to Jamaica’s market
- user who has heard about stocks but does not know where to start

Main needs:

- JSE basics
- how prices/volume work
- what a broker does
- what fees mean
- how dividends work
- what a signal is and is not
- why liquidity matters
- how to avoid blind following

### 2. I want to see what is happening in the market

This user wants broad market context before drilling into a company.

Likely user:

- active retail investor
- analyst-minded user
- advisor reviewing market conditions
- returning dashboard user

Main needs:

- Market Pulse
- unusual activity
- volume/liquidity context
- sector movement
- top movers/watch areas
- data warnings
- broad signals and risk context

### 3. I want to research a company

This user starts with a specific ticker or company.

Likely user:

- investor checking a stock they already know
- user who saw a company in the news
- dividend-focused investor
- research/analyst user

Main needs:

- company page
- ticker analysis
- historical signal behavior
- earnings context
- dividend context
- tradability/liquidity context
- research links
- what to watch

### 4. I want to plan or test a setup

This user wants to turn information into a structured decision-support workflow.

Likely user:

- short-to-medium term active investor
- user testing a trading idea
- future paper-portfolio user
- disciplined retail investor

Main needs:

- Portfolio Plan
- Ticker Analysis
- Decision Audit
- setup testing, future
- paper portfolio, future
- review calendar, future
- cost assumptions
- risk flags

### 5. I want income/dividend context

This user is interested in income generation, distributions, and portfolio yield context.

Likely user:

- income-focused investor
- long-term holder
- retiree or pre-retiree
- diaspora investor seeking Jamaican income assets

Main needs:

- Dividend View
- payment history
- ex-dividend/payment dates
- yield context
- company page
- income risk notes
- portfolio income estimate, future

### 6. I want to understand brokerage/access steps

This user needs education about access, accounts, and process.

Likely user:

- beginner investor
- diaspora investor
- person without a brokerage account
- user who wants to act but does not know the process

Main needs:

- broker/access education
- account-opening checklist
- questions to ask a licensed broker
- fee estimate education
- compliance-safe links
- no broker recommendation unless approved/compliance-cleared

### 7. I want to see the product vision/demo

This user is reviewing the product itself.

Likely user:

- advisor
- investor/partner
- JSE/FSC/legal contact
- academic reviewer
- potential employer
- grant or accelerator reviewer

Main needs:

- Demo Mode
- Platform Preview
- architecture/compliance roadmap
- product modules
- monetization path
- data-rights status
- safe explanation of what is built vs future

---

## Proposed Top-Level Navigation

The long-term navigation should be organized by user intent.

Recommended primary nav:

```text
Start Here
Learn
Market
Companies
Portfolio Tools
Income
Research
Demo
```

Alternative shorter nav if space is tight:

```text
Start Here
Learn
Market
Companies
Tools
Research
Demo
```

On mobile, a compact grouped menu should be used instead of forcing all items into a horizontal bar.

---

## Top-Level Sections

## 1. Start Here

Purpose:

Orient the user and route them to the right path.

Start Here should not be a generic homepage. It should ask:

```text
What are you trying to do today?
```

Recommended CTA cards:

- Learn how the JSE works
- See what is happening in the market
- Research a company
- Plan or test a setup
- Track dividend/income context
- Understand brokerage access
- View the product demo

Recommended page behavior:

- show data/demo status clearly
- explain decision-support boundary
- route users by intent
- show beginner and analyst paths
- avoid overwhelming first-time users with too many metrics

Current related pages:

- `/`
- `/demo`
- `/platform-preview`

Future pages:

- `/start`
- `/getting-started`

---

## 2. Learn

Purpose:

Education for beginners and users who need context before interpreting the platform.

Recommended content clusters:

- JSE Basics
- How stocks trade in Jamaica
- What volume and liquidity mean
- What spread widening means
- What holding windows mean
- What win rate means
- Average vs median return
- What costs do to returns
- What dividends are
- How to read a company page
- How to use decision support responsibly

Recommended pages:

```text
/learn
/learn/jse-basics
/learn/holding-windows
/learn/liquidity
/learn/trading-costs
/learn/dividends
/learn/how-to-read-a-company-page
```

Key product rule:

Education should empower users to make their own decisions, not tell them what to buy or sell.

---

## 3. Market

Purpose:

Give users broad market context before they drill into a company or setup.

Recommended surfaces:

- Market Pulse
- top movers/context
- liquidity watch
- unusual volume
- volatility buckets
- recent signals summary
- market data status
- data warnings

Recommended pages:

```text
/market
/market/pulse
/market/liquidity-watch
/market/signals
```

Current related page:

- Ticker Analysis is currently linked directly but should eventually be discoverable from Market and Companies.

Future features:

- weekly market summary
- sector view
- market breadth
- event calendar

---

## 4. Companies

Purpose:

Make the company/ticker the anchor for research, decision-support, and market context.

Recommended surfaces:

- Company Pages
- Ticker Analysis
- Earnings Scorecard
- Dividend View by company
- Float / Tradability View
- research links
- analyst-call tracker, future

Recommended pages:

```text
/companies
/companies/[ticker]
/ticker/[ticker]
/companies/[ticker]/earnings
/companies/[ticker]/dividends
/companies/[ticker]/tradability
```

Near-term direction:

The existing `/ticker/[ticker]` page can remain, but the product should eventually move toward company-centered pages with ticker analysis embedded inside them.

---

## 5. Portfolio Tools

Purpose:

House the decision-support engine and planning workflows.

Recommended surfaces:

- Portfolio Plan
- Ticker Analysis
- Decision Audit
- Setup Tester, future
- Paper Portfolio, future
- Review history, future
- cost assumptions
- holding-window comparisons

Recommended pages:

```text
/tools
/tools/portfolio-plan
/tools/decision-audit
/tools/setup-tester
/tools/paper-portfolio
/portfolio
/review
```

Current related pages:

- `/portfolio`
- `/review`
- `/ticker/[ticker]`

Product rule:

Portfolio Tools should be framed as planning and testing, not as instructions to trade.

---

## 6. Income

Purpose:

Serve income-focused investors who care about dividends, distributions, and cash-flow potential.

Recommended surfaces:

- Dividend View
- dividend calendar
- company dividend profile
- income-focused watchlist, future
- portfolio income estimate, future
- payout reliability context, future

Recommended pages:

```text
/income
/income/dividends
/income/calendar
/income/company/[ticker]
```

Product rule:

Income tools must still show risk context. Dividend history does not guarantee future dividends.

---

## 7. Research

Purpose:

Organize market research, company notes, source links, event context, and future premium research.

Recommended surfaces:

- Research Hub
- company research index
- market notes
- event notes
- earnings notes
- saved reports, future
- analyst call tracker, future

Recommended pages:

```text
/research
/research/company-notes
/research/market-notes
/research/events
/research/analyst-calls
```

Compliance/data-rights note:

Research hosting and redistribution should remain gated until JSE/FSC/legal/data-rights review is clearer.

---

## 8. Demo

Purpose:

Support advisor, partner, grant, academic, and stakeholder walkthroughs.

Recommended surfaces:

- Demo Mode
- Platform Preview
- Product roadmap
- data-rights status
- compliance roadmap
- monetization overview

Recommended pages:

```text
/demo
/platform-preview
/demo/walkthrough
/demo/compliance-roadmap
```

Product rule:

Demo should not be treated as the main investor journey. It is a stakeholder/product-review journey.

---

## User Journey Maps

## Beginner Investor Journey

```text
Start Here
→ Learn
→ JSE Basics
→ How to read a company page
→ Try a sample company
→ Review what signals mean
→ Portfolio Tools, optional
```

Key CTA language:

```text
I want to understand the market before making decisions.
```

---

## Opportunity-Seeking Investor Journey

```text
Start Here
→ Market
→ Market Pulse
→ Ticker Analysis
→ Portfolio Plan
→ Decision Audit
```

Key CTA language:

```text
I want to review possible setups with structure.
```

---

## Company Research Journey

```text
Start Here
→ Companies
→ Company Page
→ Ticker Analysis
→ Earnings / Dividend / Tradability context
→ Decision Audit or Portfolio Plan
```

Key CTA language:

```text
I want to research a specific company.
```

---

## Income-Focused Journey

```text
Start Here
→ Income
→ Dividend View
→ Company Page
→ Portfolio Plan
→ Income notes / risk context
```

Key CTA language:

```text
I want dividend and income context.
```

---

## Diaspora Investor Journey

```text
Start Here
→ Learn
→ Jamaica market overview
→ Brokerage access education
→ Companies
→ Research
→ Demo Mode, optional
```

Key CTA language:

```text
I want to understand how investing in Jamaica works.
```

---

## Advisor / Partner Journey

```text
Demo
→ Platform Preview
→ Decision Engine overview
→ Data rights and compliance status
→ Monetization path
→ Roadmap
```

Key CTA language:

```text
I want to understand the product vision and readiness.
```

---

## Future Simulation Journey

```text
Start Here
→ Portfolio Tools
→ Setup Tester
→ Paper Portfolio
→ Review outcome
→ Lessons learned
```

Key CTA language:

```text
I want to test a setup before acting in the real market.
```

---

## Analyst / Research Journey

```text
Research
→ Company Pages
→ Earnings Scorecard
→ Float / Tradability View
→ Market Pulse
→ Decision Audit
```

Key CTA language:

```text
I want deeper company and market intelligence.
```

---

## Recommended Homepage Structure

The homepage should eventually become a routing page, not just a static hero.

Recommended sections:

1. Clear positioning statement
2. Data/demo status banner
3. “What are you trying to do today?” CTA cards
4. Working product surfaces
5. Future platform surfaces, clearly labelled
6. Decision-support boundary
7. Demo/advisor pathway

Recommended CTA cards:

```text
Learn the JSE
Explore the market
Research a company
Plan or test a setup
Track dividends/income
Understand brokerage access
View product demo
```

---

## Recommended Navigation Hierarchy

## Primary Navigation

```text
Start Here
Learn
Market
Companies
Portfolio Tools
Income
Research
Demo
```

## Utility / Secondary Navigation

```text
Data Status
Cost Assumptions
Demo Mode
Disclosures
Roadmap
```

## Mobile Navigation

Mobile should use grouped sections:

```text
Start
Learn
Market
Companies
Tools
More
```

Where “More” includes:

```text
Income
Research
Demo
Disclosures
```

---

## Near-Term Frontend Implementation Direction

Do not build every page at once.

Recommended next frontend branch after this doc:

```text
feature/platform-navigation-shell
```

MVP scope:

- Update homepage to user-intent routing cards
- Update nav labels to broader platform sections
- Add placeholder landing pages for Learn, Market, Companies, Portfolio Tools, Income, Research, Demo if not already present
- Preserve existing working pages
- Clearly mark future surfaces as preview/gated
- Keep Demo Mode and Platform Preview accessible but not primary investor path

Suggested MVP pages:

```text
/learn
/market
/companies
/tools
/income
/research
```

Existing pages to preserve:

```text
/portfolio
/ticker/JMMBGL
/review
/demo
/platform-preview
```

---

## Out of Scope for Navigation Shell MVP

Do not add yet:

- user authentication
- saved profiles
- Setup Tester logic
- Paper Portfolio logic
- official JSE API integration
- broker referral forms
- paid products
- AI helper responses
- research hosting as a public product

Those should remain future work after data/compliance foundations.

---

## Product Copy Rules

Use phrases like:

```text
Review
Explore
Understand
Compare
Test
Learn
Plan
```

Avoid phrases like:

```text
Buy
Sell
Guaranteed
Best broker
Sure return
Must act now
```

---

## Acceptance Criteria for Future Navigation Shell

A future navigation-shell PR should satisfy:

- user can choose a path based on intent
- beginner user is not forced into analyst-heavy pages first
- advisor/demo user has a clear walkthrough path
- portfolio/ticker/review pages remain available
- future modules are labelled as future/preview/gated
- compliance-sensitive areas are clearly marked
- mobile navigation is usable
- no navigation label implies advice, execution, or broker recommendation

---

## Open Product Questions

1. Should “Income” be a top-level nav item from the start, or nested under Companies/Research until Dividend View is built?
2. Should “Research” be visible before research hosting is compliance-cleared, or should it remain a preview surface?
3. Should “Portfolio Tools” be named “Tools,” “Plan,” or “Portfolio Tools” for beginner clarity?
4. Should diaspora-specific content live under Learn, Start Here, or its own future path?
5. Should AI Helper appear in navigation before it exists, or only as a preview card?

These questions should be resolved before large frontend navigation changes are finalized.
