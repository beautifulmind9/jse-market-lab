# Feature Breakdown — JSE Dashboard

## Core Systems

### 1. Signal Engine
- Detects median crossover events
- Generates trade opportunities

### 2. Ranking Engine
- Scores opportunities based on:
  - trend strength
  - volume confirmation
  - volatility
  - spread behavior

### 3. Cost Engine
- Applies:
  - broker fee (0.50%)
  - CESS (0.35%)
- Produces net-of-cost returns

### 4. Weekly Trade Planner
- Displays active opportunities
- Assigns holding windows (5D, 10D, 20D, 30D)
- Tracks entry/exit assumptions

### 5. Earnings Intelligence Layer
- Tags earnings phases:
  - pre
  - reaction
  - post
  - non
- Detects overlap with holding windows

### 6. Earnings Warning System
- Generates:
  - warning title
  - warning body
  - severity level
- Signals risk during earnings overlap
