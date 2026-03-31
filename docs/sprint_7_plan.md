# Sprint 7 — Streamlit App Shell + Portfolio Plan UI

## Goal
Make the dashboard runnable and visible to users, and present allocation outputs as a usable portfolio plan instead of backend-only logic.

## Why this sprint matters
The core decision engine already exists:
- signal generation
- quality scoring
- risk awareness
- guidance
- confidence
- allocation
- analyst insights

What is missing is the visible product surface:
- no top-level Streamlit app entrypoint
- no clear portfolio plan review layer

This sprint bridges the gap between engine and user experience.

## Scope

### In Scope
- Create a runnable Streamlit app entrypoint
- Load the latest dataset into the app
- Add a simple app shell with navigation / sections
- Render analyst insights through the app shell
- Add a Portfolio Plan section
- Display funded vs unfunded trades
- Display capital summary and cash reserve
- Show clear reason labels for funding / non-funding

### Out of Scope
- Changes to signal logic
- Changes to scoring logic
- Changes to confidence logic
- Changes to allocation engine logic
- Plan history / persistence
- Public content generation automation
- Advanced styling

## Expected Outcome
By the end of this sprint:
- the dashboard can be launched in Streamlit
- users can see the product live
- allocation outputs are presented as a readable portfolio plan
- the app starts to feel like a usable product, not just a collection of helpers

## Product Impact
Moves the project from:
- engine + docs

to:
- visible app + user-facing portfolio decision tool
