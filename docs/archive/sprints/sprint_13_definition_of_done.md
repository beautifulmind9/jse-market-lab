# Sprint 13 Definition of Done

Sprint 13 is done when the following conditions are true:

## Portfolio
- Portfolio starts with a clear summary of what the plan is doing
- users can understand setup strength without decoding tiers
- users can understand confidence / reliability without reading raw metrics
- users can understand why some cash is reserved
- users can understand why trades were funded or not funded
- users can understand how a trade would typically be entered and exited
- funded-trade count feels adaptive to setup quality and capital discipline, not arbitrarily fixed

## Ticker Analysis
- Ticker Analysis reads as interpretation before detail
- users can understand best holding style
- users can understand execution behavior at a high level
- Beginner mode does not overload users with raw tables
- Analyst mode preserves deeper evidence without losing context
- median return is presented as the typical outcome metric

## Analyst Insights
- Analyst Insights has a clear purpose
- Performance Matrix is explained
- Exit Analysis is explained or simplified
- empty Feature Insights no longer feel broken or placeholder-like
- grouped historical outputs feel like strategy validation, not backend tables

## Review / Decision Audit
- Review clearly answers whether the plan followed intended rules
- review output is human-readable
- raw backend-style review columns are not exposed directly
- users can understand what happened and why it matters

## Labels and language
- user-facing labels are clean and readable
- no raw snake_case leaks into the UI
- wording is plain, Jamaican-friendly, and non-advisory

## Metric integrity
- median return is the primary typical-outcome metric
- average return is supporting context only where shown

## Stability
- no deployment-blocking Portfolio crash remains
- compact execution summary renders safely
- holding-window / exit wording remains explicit for valid rows
- beta users can reach the live app and use the main decision surfaces

Sprint 13 is complete when a first-time user can understand what the dashboard is telling them, why the Portfolio looks the way it does, and how a trade would typically be approached, without needing to decode internal system logic.
