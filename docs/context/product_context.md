# Product Context

## Core engine
The dashboard uses structured historical market behavior to identify and compare trade setups on the Jamaican Stock Exchange.

Core engine components include:
- median crossover signals
- event-based signal generation
- cooldown logic
- liquidity checks
- volume confirmation
- spread-widening context
- volatility buckets
- historical outcome comparisons

---

## Signal and ranking logic
Signals are evaluated using a combination of setup quality, confidence context, volatility context, and eligibility rules.

The platform is designed to:
- highlight stronger setups first
- separate funded and unfunded opportunities
- avoid forcing lower-quality setups into the plan
- explain why some trades are chosen over others

Tier handling:
- Tier A: strongest setup quality
- Tier B: supportive but less aligned
- Tier C: tracked, but not prioritized for income-focused portfolio use

---

## Holding windows
The platform compares behavior across multiple holding windows:
- 5D
- 10D
- 20D
- 30D

Median return is the primary typical-outcome metric.
Average return may appear as supporting context, but it should not be treated as the main expected outcome.

---

## Portfolio logic
Portfolio generation currently includes:
- ranked opportunity selection
- adaptive funding behavior
- reserve cash logic
- funded vs unfunded trade separation
- explanation layers for setup strength, confidence, and trade reasoning

The portfolio is meant to act as a structured planning surface, not just a report.

---

## Execution layer
The execution layer is designed to provide structured historical guidance around:
- entry reference
- holding window / planned review timing
- typical outcome behavior
- execution risks such as liquidity and spread effects

This layer should remain guidance-first, historically grounded, and non-hype in tone.

---

## Review layer
The Review tab is intended to show how the plan applied its rules and where discipline mattered.

Current direction:
- human-readable decision-audit framing
- explanation of ranking / quality / liquidity application

Future direction:
- more transparent numeric decision-audit detail
- stronger visibility into what the system looked at when selecting or not funding trades

---

## Ticker Analysis
Ticker Analysis is one of the clearest product surfaces so far.

It is designed to help a user understand one stock through:
- quick take
- best holding strategy
- risk profile
- what usually happens
- what to watch
- execution behavior

This surface is both educational and decision-supportive.

---

## Guided vs Advanced structure
Guided View should:
- prioritize simplicity
- reduce visible detail
- keep interpretation first
- work well for users with limited market experience

Advanced View should:
- preserve deeper breakdowns
- expose grouped evidence and analytical tables
- still explain what each section helps the user understand

---

## Trading costs
Current assumptions:
- Broker fee: 0.50%
- CESS: 0.35%

Trading-cost realism remains part of the product’s credibility and should continue to be reflected in outputs where applicable.
