# Sprint 1 — UAT Notes

## Objective
Validate that earnings warnings improve decision clarity without adding noise.

## Test Scenarios

### Case 1 — Overlap = True, Severity = High
- Warning displays clearly
- User understands risk immediately

### Case 2 — Overlap = True, Severity = Caution
- Warning visible but not overwhelming

### Case 3 — Overlap = True, Severity = Info
- Subtle informational message

### Case 4 — Overlap = False
- No warning displayed

### Case 5 — Overlap = Null / Unknown
- No warning displayed

## Observations
- Warning placement improves awareness before decision
- Expander keeps UI clean
- Severity levels help differentiate urgency

## Improvements Identified
- Handle pandas null values safely
- Ensure no false positives on overlap
