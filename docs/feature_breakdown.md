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

### 7. Portfolio Decision Surface Layer

This layer translates allocation outputs into a user-facing decision interface.

#### Guided View (Beginner-friendly)
- Uses compact trade cards
- Prioritizes scanability and clarity
- Shows only core decision fields:
  - Ticker
  - Setup Strength
  - Confidence / Reliability
  - Holding Window
  - Why this trade / Why not funded
- Moves secondary fields into collapsed detail sections

#### Advanced View (Analyst-friendly)
- Uses a compact comparison table for first-pass scanning
- Avoids horizontal scrolling for critical fields
- Provides row-level drilldowns for deeper context

Primary comparison fields:
- Ticker
- Setup Strength / Tier
- Confidence / Reliability
- Holding Window
- Decision Status
- Allocation %
- Selection Rank

#### Drilldown Detail Layer
- Reveals deeper reasoning per trade:
  - Why this trade / Why not funded
  - Execution Summary
  - Rule Note
  - Allocation Amount
  - Allocation %
  - Selection Rank

#### Full Analyst Table (Optional)
- Provides full raw data view
- May include horizontal scrolling
- Not used as the primary decision surface

#### Purpose
This layer ensures the dashboard:
- supports fast comparison
- prevents hidden critical information
- preserves analytical depth without overwhelming users
