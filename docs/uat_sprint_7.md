# UAT — Sprint 7: Streamlit App Shell + Portfolio Plan UI

## Objective
Validate that the dashboard can be launched as a Streamlit app and that allocation outputs are presented as a clear, usable portfolio plan.

## Test Scenarios

### 1. App Launch
Expected:
- Streamlit app launches successfully
- No missing entrypoint error
- Main dashboard surface renders

### 2. Data Load
Expected:
- Dataset loads into the app
- Helpful message shown if data is missing or empty

### 3. Analyst Insights Access
Expected:
- Analyst Insights section renders through the app shell
- Existing insights remain usable

### 4. Portfolio Summary
Expected:
- Total capital displays
- Allocated capital displays
- Cash reserve displays
- Values reconcile correctly

### 5. Funded Trades Section
Expected:
- Only funded trades appear here
- Trades are sorted clearly
- Allocation amount and percentage are shown

### 6. Unfunded Trades Section
Expected:
- Only unfunded trades appear here
- Reason not funded is shown

### 7. Reason Labels
Expected:
- Reasons are human-readable
- Examples:
  - Not funded — Tier C
  - Not funded — Liquidity
  - Reduced allocation — Earnings risk
  - Eligible — meets criteria

### 8. Missing Field Handling
Expected:
- No app crash when optional columns are missing
- Helpful fallback messages appear where needed

## Validation Questions
- Can a user understand the portfolio plan at a glance?
- Does the app feel like a real product rather than a set of raw tables?
- Are funding and non-funding decisions easy to understand?

## Final UAT Status
(To be completed after implementation review)
