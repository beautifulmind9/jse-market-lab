# Sprint 3 — Jamaican Clarity Layer

## Feature
Dual-language guidance view: Clear vs Pro

## Objective
Make decision guidance understandable to an average Jamaican reader while still offering a more concise version for experienced users.

## Problem
The guidance layer explains what the user can do when earnings risk is present, but some of the wording may still sound too technical or unfamiliar. If the language feels foreign or too “finance-heavy,” users may ignore the guidance or misunderstand it.

## Requirement
The planner must provide two versions of each guidance message:
- a Clear version written in natural, everyday English
- a Pro version written more concisely for experienced users

## Acceptance Criteria
- Guidance output includes:
  - guidance_title
  - guidance_body_clear
  - guidance_body_pro
  - guidance_type
- Clear mode uses plain, everyday wording
- Clear mode avoids jargon such as:
  - exposure
  - holding window
  - catalyst
  - event-driven volatility
- Pro mode remains readable and locally appropriate
- Default UI mode favors Clear
- No changes are made to overlap logic
- No changes are made to warning-generation logic
- Null severity still falls back safely
- Null or unknown overlap still returns no guidance
