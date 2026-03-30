# UAT — Sprint 6: Analyst Intelligence Layer

## Objective
Validate that the Analyst Insights layer helps explain and assess system behavior using existing trade history.

## Test Scenarios

### 1. Feature Insights render
Expected:
- grouped summaries appear for available feature fields

### 2. Missing feature fields
Expected:
- dashboard shows a helpful message, not an error

### 3. Performance Matrix render
Expected:
- grouped summary table appears
- win-rate matrix appears
- median-return matrix appears

### 4. Missing holding_window
Expected:
- helpful fallback behavior or message

### 5. Exit Analysis render
Expected:
- grouped exit-reason table appears when exit_reason is available

### 6. Missing exit_reason
Expected:
- helpful message, not a crash
  
### 7. Exit Analysis Missing Tier

Input:
- exit_reason present
- quality_tier missing

Expected:
- No crash
- Informational message displayed
- Exit Analysis not rendered

### 8. Pandas Index Input Handling

Input:
- preferred = df.columns (pandas Index)

Expected:
- No crash
- Return column resolves correctly

Result:
- PASS if stable
  
## Validation Questions
- Does this help explain why the system favors certain setups?
- Are the tables readable and useful for analyst review?
- Do the outputs help identify potential rule improvements?

## Observations
- The dashboard now has a stronger analyst workflow
- Historical behavior is easier to inspect without leaving the app
- Feature-level summaries should help refine scoring rules later
- Tier × holding-window views improve confidence in planner decisions

## Final UAT Status

## ✅ Approved for Release

The Analyst Intelligence Layer successfully adds validation views for feature behavior, tier-window performance, and exit outcomes without modifying the underlying decision engines.
