# Sprint 7 Requirements — Streamlit App Shell + Portfolio Plan UI

## Functional Requirements

1. The system must provide a top-level Streamlit app entrypoint.
2. The app must load a dataset from the project data layer.
3. The app must expose at least:
   - a main dashboard surface
   - analyst insights
   - a portfolio plan view
4. The portfolio plan view must display:
   - total capital
   - total allocated amount
   - total allocated percentage
   - cash reserve amount
   - cash reserve percentage
5. The portfolio plan view must separate:
   - funded trades
   - unfunded trades
6. Funded trades must display:
   - instrument / symbol
   - quality tier
   - confidence label
   - allocation percentage
   - allocation amount
   - funding reason / note
7. Unfunded trades must display:
   - instrument / symbol
   - quality tier (if available)
   - reason not funded
8. The app must handle partial or missing fields gracefully without crashing.

## Non-Functional Requirements

- The app must be Streamlit-native and lightweight
- The UI must be readable and table-first
- The implementation must not modify allocation engine logic
- The implementation must not modify confidence or warning engines

## Definition of Done

- App entrypoint exists and runs
- Dataset loads into the app
- Analyst Insights render from the app shell
- Portfolio Plan UI renders funded and unfunded sections
- Summary totals are visible
- Reason labels are visible
- Tests for helper functions pass
