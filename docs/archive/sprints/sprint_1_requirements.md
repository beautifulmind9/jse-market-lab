# Sprint 1 — Requirements & Acceptance Criteria

## Feature
Planner Earnings Warning UI

## Requirement
The Weekly Trade Planner must display an earnings warning when a trade’s holding window overlaps with an earnings event.

## Acceptance Criteria

- Warning is shown only when `earnings_overlaps_window == True`
- Warning includes:
  - title
  - severity (info, caution, high)
  - explanation body
- Severity is visually distinguishable
- Warning appears below the trade header and before trade details
- Warning does not clutter the planner
- Missing or invalid severity defaults to "info"
- Null or unknown overlap values do not trigger warnings
- UI implementation does not modify engine logic
