# Market-Data UI Design Research — JSE Market Lab

## Purpose

This document captures market-data, financial-news, brokerage, and investor-education UI patterns that should guide JSE Market Lab’s design direction.

It supports Issue #153:

```text
Research market-data UI patterns and user behavior for JSE Market Lab design direction
```

This first version is a structured research and recommendation framework based on the product direction, current platform surfaces, screenshots already reviewed in product discussion, and known design needs.

It does not claim that a full live review of every external platform has been completed. Future research passes should add detailed notes from reviewed platforms where permitted.

---

## Product Context

JSE Market Lab is no longer only a dashboard.

It is becoming a guided market intelligence, research, education, decision-support, demo, and future simulation platform for:

- Jamaican investors
- Caribbean investors
- diaspora investors
- beginners learning how to approach the JSE
- more advanced users who want structured decision support
- advisors, partners, schools, and institutions evaluating the product

The UI must support:

- fast market context
- beginner clarity
- analyst usefulness
- mobile readability
- trust and data-status transparency
- demo/internal/live-data distinctions
- guided next steps
- safe decision-support language
- future monetization and advisor walkthroughs

---

## Design Principle

The platform should feel like:

```text
Market intelligence first
Research second
Decision tools third
Education and AI guidance always nearby
```

Not:

```text
A signal-selling dashboard
A broker execution screen
A prediction engine
A cluttered professional terminal
```

---

## Reference Platforms to Review

Future research passes should review these platforms and document findings.

## Global Financial Media / Market Data

| Platform | Why it matters | What to observe |
|---|---|---|
| CNBC | Market-first homepage, news hierarchy, live-feeling information density. | Homepage hierarchy, ticker strips, market snapshots, article blocks, mobile layout. |
| Bloomberg | Dense institutional information design and market/news blending. | Information hierarchy, confidence, typography, table density, professional tone. |
| Yahoo Finance | Accessible retail-investor finance UX. | Ticker pages, watchlists, summary cards, charts, news integration. |
| MarketWatch | Retail-friendly financial news and market pages. | Homepage sections, market data tables, news cards, investor language. |
| Morningstar | Research and fundamentals-driven investor UX. | Ratings presentation, funds/stocks research structure, disclaimers. |
| Seeking Alpha | Research/community-oriented stock pages. | Article/research structure, premium prompts, source attribution, watchlists. |
| TradingView | Chart-first market interface. | Watchlists, chart controls, ticker search, community ideas, mobile density. |
| Koyfin | Professional market analytics. | Dashboards, modular tiles, charts, screener behavior. |
| Simply Wall St | Beginner-friendly visual investing interface. | Visual summaries, risk flags, education-oriented presentation. |

## Local / Regional References

| Platform | Why it matters | What to observe |
|---|---|---|
| Jamaica Stock Exchange website | Official source environment. | Data presentation, notices, listed-company pages, official wording. |
| JTrader / broker portals, where accessible | Local investor workflow expectations. | Watchlists, order-entry boundaries, portfolio views, cost/fee visibility. |
| Jamaican broker websites | Account-opening and education language. | How fees, products, and disclosures are presented. |
| Caribbean financial news sites | Regional market literacy and investor behavior. | Headline style, mobile readability, audience assumptions. |
| Social media finance creators | How Jamaican users consume finance education. | Simple language, examples, common confusion points, engagement hooks. |

---

## What to Capture in Future Research Passes

For each reviewed platform, capture:

```text
Platform name
Audience type
Primary use case
Homepage structure
Navigation model
Ticker/company page structure
Market data display patterns
News/research presentation
Watchlist/portfolio patterns
Education/onboarding pattern
Mobile behavior
Trust/disclosure pattern
What works for JSE Market Lab
What would not fit JSE Market Lab
Screenshots or links, only where usage rights are clear
```

---

## Patterns Worth Borrowing

## 1. Market information should appear immediately

The homepage should not begin with abstract product marketing only. Users should quickly see market context.

For JSE Market Lab, this means:

- market snapshot near the top
- demo/internal/live data status visible
- latest available date visible
- market notes or signal clusters visible
- clear path to Market Pulse

Current implementation direction:

```text
Homepage market snapshot first
→ user-intent paths below
```

This aligns with the advisor feedback that live-looking market information should live on the homepage.

---

## 2. Use information density carefully

Financial platforms often show dense pages. This builds credibility for experienced users, but can overwhelm beginners.

JSE Market Lab should use layered density:

```text
Beginner first impression: simple labels, clear CTAs, what to check next
Analyst layer: metrics, tables, rules, risk context, audit explanations
```

Do not overload the first screen with every metric.

---

## 3. Separate market context, company research, and decision tools

Users need a mental model:

```text
Market Pulse = what is happening broadly
Companies = what should I research
Tools = how do I test/review a setup responsibly
```

This is now reflected in the current platform navigation:

```text
Homepage → Market → Companies → Tools
```

---

## 4. Make data status part of the UI, not hidden copy

Financial trust depends on data clarity.

JSE Market Lab should always show:

- demo/internal/live status
- latest market date
- dataset source
- data-rights caveat where relevant
- official-feed caveat where relevant

This is especially important before JSE authorization.

---

## 5. Use guidance instead of recommendation language

Good financial UX often guides users toward the next thing to review without saying what they should buy.

JSE Market Lab should use:

```text
Review this
Check this
Compare this
Understand this
Use this as context
```

Avoid:

```text
Buy this
Sell this
Best stock
Guaranteed
Winning setup
Act now
```

---

## 6. Put risk and assumptions close to outputs

Any page showing signals, setups, allocation, returns, or simulated outcomes should also show:

- costs
- liquidity
- holding window
- data completeness
- volatility/spread context where available
- past-performance disclaimer

Do not separate risk language into a hidden footer only.

---

## 7. Use repeatable card/table patterns

The current market-front visual system uses:

- status tape
- lede panel
- board/quote panel
- modules
- cards
- tables
- notices

This should become a consistent page template system.

Suggested platform patterns:

```text
Status tape
→ Page lede
→ Summary board
→ Main table/cards
→ Risk/data note
→ Next-step CTA
```

---

## 8. Mobile-first matters for Jamaican users

Many users will interact from a phone.

Mobile UX should prioritize:

- one-column layouts
- short labels
- tap-friendly cards
- visible Guide Me button
- clear page title
- reduced table clutter
- quick links to next action

Tables should degrade into readable stacked rows where needed.

---

## Patterns to Avoid

## 1. Terminal-like complexity too early

Avoid copying professional terminals wholesale. Bloomberg-like density can inspire confidence, but the JSE Market Lab audience includes beginners.

Use professional credibility without making the interface feel inaccessible.

---

## 2. Signal-selling presentation

Avoid layouts that make a ticker list look like instructions to buy or sell.

Do not overemphasize:

- green/red hype
- leaderboards of “best picks”
- countdown urgency
- profit-first rankings

---

## 3. Hidden disclaimers

Do not rely only on footer disclaimers.

Important caveats should appear next to the relevant data:

- demo/internal data
- costs are estimates
- not an official live feed
- not advice
- future modules are previews

---

## 4. Over-navigation

Too many navigation items can confuse users.

The platform can support many modules, but the top-level path should remain simple:

```text
Learn
Market
Companies
Tools
Income
Research
Demo
```

The AI Helper can guide users through complexity without crowding the main nav.

---

## 5. Charts without interpretation

Charts can look impressive, but users need context.

Every chart or market visual should answer:

- what am I looking at?
- why does it matter?
- what should I check next?
- what are the limitations?

---

## JSE Market Lab Audience Implications

## Everyday Jamaican investor

Needs:

- simple language
- examples
- visible risk/cost reminders
- confidence using the platform without finance jargon

Design response:

- plain-English labels
- Learn links
- Guide Me button
- short next-step cards

---

## Diaspora investor

Needs:

- market orientation
- broker/account-access education
- confidence that the platform is independent and not pretending to be a broker

Design response:

- strong demo/compliance boundaries
- future brokerage-access education flow
- company/research summaries
- glossary and learning paths

---

## Short/medium-term trader

Needs:

- holding windows
- win rate
- median return
- liquidity
- execution realism
- costs

Design response:

- Ticker Analysis and Portfolio Plan as core tools
- Decision Audit for rationale
- readiness/risk-control work before stronger trade planning

---

## Income/dividend investor

Needs:

- dividend context
- payout timing
- income reliability caveats
- company history

Design response:

- future Dividend View
- income page
- company-page dividend modules
- “history is not a guarantee” language

---

## Advisor/partner/institution reviewer

Needs:

- what is built vs future
- compliance/data boundaries
- product seriousness
- roadmap clarity

Design response:

- Demo page
- Platform Preview page
- Project docs
- clear gates and non-advisory positioning

---

## Recommended Navigation Model

Current navigation should remain:

```text
Learn
Market
Companies
Tools
Income
Research
Demo
```

Suggested user path:

```text
Homepage
→ Market Pulse
→ Companies
→ Tools
→ Portfolio/Ticker/Review
→ Platform Preview or Learn as needed
```

AI Helper should be persistent across all pages as a guidance layer.

---

## Recommended Page Templates

## Homepage Template

Purpose:

- immediate market context
- product positioning
- user intent routing

Recommended layout:

```text
Market snapshot
User-intent path cards
Decision-support notice
Demo/data status
```

---

## Market Pulse Template

Purpose:

- broad market context
- what is moving
- liquidity and data awareness

Recommended layout:

```text
Market status tape
Market lede
Pulse board
Movers / most active / signal clusters
Liquidity watch
Market notes
Data-status note
Next step to Companies or Tools
```

---

## Companies Template

Purpose:

- company/ticker research entry

Recommended layout:

```text
Company status tape
Company research lede
Sample/company search cards
Research modules preview
Dividend/earnings/tradability modules
Next step to Ticker Analysis or Tools
```

---

## Tools Template

Purpose:

- decision-support action center

Recommended layout:

```text
Tools status tape
Tool board
Working tools
Future simulation tools
Cost assumptions
Responsible-use checklist
Decision-support disclaimer
```

---

## Ticker Analysis Template

Purpose:

- one ticker view

Recommended layout:

```text
Ticker header
Quick take
Holding-window comparison
Median vs average return
Win rate
Liquidity/readiness flags
Cost context
What to watch
Decision-support disclaimer
```

---

## Portfolio Plan Template

Purpose:

- rule-based allocation review

Recommended layout:

```text
Capital input/settings
Funded setups
Unfunded setups
Reserve cash
Cost assumptions
Why funded/unfunded
Risk/readiness notes
Decision Audit link
```

---

## Review / Decision Audit Template

Purpose:

- trust and explainability

Recommended layout:

```text
Decision summary
Rules applied
Funded rationale
Unfunded rationale
Cost/risk assumptions
What to review next
Disclaimer
```

---

## Mobile-First Recommendations

- Collapse multi-column grids into single-column cards.
- Keep status tapes readable and stacked.
- Avoid horizontal scrolling where possible.
- Use short card titles.
- Keep the Guide Me button visible but not intrusive.
- Use tables only when they remain readable on small screens.
- Prioritize one next action per section.

---

## Advisor/Demo Walkthrough Implications

The demo flow should remain:

```text
Homepage
→ Market Pulse
→ Companies
→ Tools
→ Portfolio Plan
→ Ticker Analysis
→ Decision Audit
→ Guide Me / AI Helper shell
→ Platform Preview
```

When presenting to advisors, emphasize:

- what is built now
- what is demo/internal
- what is future
- what is compliance-gated
- what needs JSE/FSC/legal validation
- what the product does not do

---

## Compliance/Disclosure UI Patterns

Use visible notices for:

- demo/internal data
- official-feed status
- cost assumptions
- future module previews
- AI Helper limits
- broker/referral boundaries
- research/source validation

Preferred wording style:

```text
This is decision support, not investment advice.
This is demo/internal data, not an official live JSE feed.
Future research and broker-access features require validation before launch.
Costs are estimates and may vary by broker/account/product.
```

---

## Future Design Backlog

## Near-term

- Improve market-front visual hierarchy based on user testing.
- Add richer Market Pulse sections once backend market summary data exists.
- Improve Companies with search/filter behavior.
- Add stronger mobile table patterns.
- Add “what to check next” microcopy near tools.

## Medium-term

- Full company pages by ticker.
- Research Hub layout.
- Dividend View layout.
- Earnings Scorecard layout.
- Float/Tradability layout.
- Broker fee comparison/slider UI after source validation.

## Longer-term

- User profile onboarding.
- Setup Tester UX.
- Paper Portfolio UX.
- AI Helper platform retrieval and safe web research mode.
- Gamified learning paths focused on discipline and education.

---

## Research Gaps to Fill Later

This first version should be expanded with specific observations from at least 8 reference platforms.

Future pass should include:

- date reviewed
- platform screenshots/notes where allowed
- specific homepage patterns
- specific ticker/company page patterns
- specific mobile findings
- what to borrow
- what to avoid
- how findings translate to JSE Market Lab

Do not commit copyrighted screenshots unless usage rights are clear.

---

## Current Recommendation

For the next UI iteration, focus on improving the already-built platform surfaces rather than adding more pages immediately:

```text
Homepage market snapshot polish
Market Pulse content hierarchy
Companies search/card behavior
Tools decision-support clarity
Mobile readability
AI Helper prompts and links
```

This keeps the product grounded in the current platform and avoids spreading the UI too thin.
