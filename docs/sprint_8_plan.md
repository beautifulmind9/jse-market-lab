# Sprint 8 Plan — Explanation Layer

## Sprint
Sprint 8

## Status
Planned

## Sprint goal
Make the dashboard easier to trust by clearly explaining why decisions are made.

## Context
Sprint 7 delivered:
- Streamlit app shell
- Analyst Insights tab
- Portfolio Plan UI
- funded vs unfunded trades
- working visible product

The system now produces decisions, but does not yet explain them clearly.

## Core Sprint 8 theme
**Add explanation and reasoning to the product**

## In scope
- explain why a trade is considered strong or weak
- explain why a trade is funded or not funded
- explain allocation decisions
- explain warnings and constraints
- explain confidence labels
- provide plain-language reasoning blocks

## Out of scope
- marketing insight generation
- full insight translation layer (Sprint 9)
- replacing demo data
- signal engine changes
- allocation logic changes
- major UI redesign

## Key features

### 1. Trade-level explanation
For each trade:
- why it received its quality tier
- what factors contributed (trend, volume, volatility, etc.)
- what makes it strong or risky

### 2. Allocation explanation
For funded/unfunded trades:
- why it was funded
- why it was not funded
- which constraint applied (capital, rules, limits)

### 3. Confidence explanation
- explain what confidence means
- why a trade is high / medium / low confidence
- connect confidence to real factors (not abstract labels)

### 4. Warning explanation
- earnings-related warnings explained in plain language
- timing risks explained
- holding window implications explained

### 5. Plain-language reasoning blocks
Add small explanation sections such as:
- “Why this trade?”
- “Why this allocation?”
- “What this means”

## Acceptance criteria
- each trade can be explained in simple language
- funded vs unfunded decisions are understandable
- confidence labels are clearly explained
- warnings are understandable without technical knowledge
- explanations are grounded in real logic (no invented reasoning)

## Risks
- over-explaining or cluttering UI
- introducing incorrect or misleading explanations
- disconnect between logic and explanation

## Definition of done
Sprint 8 is complete when:
- users can understand *why* the system made decisions
- explanations match actual logic
- the product feels more transparent and trustworthy

## Constraint
Sprint 8 must not include marketing-style insights or external storytelling.

All explanations must:
- describe system logic
- remain neutral
- avoid directional advice
