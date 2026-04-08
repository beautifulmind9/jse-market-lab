# Sprint 11 — Review & Discipline Layer

## Goal
Introduce a post-decision evaluation layer that helps users understand how they are using the system, identify mistakes, and improve decision discipline.

## Problem
Users can:
- see signals
- understand explanations
- analyze stock behavior

But cannot:
- evaluate their own decisions
- identify mistakes in trade selection
- detect patterns in their behavior

This leads to:
- misuse of the system
- misattribution of poor outcomes
- lack of learning over time

## Solution
Add a Review & Discipline Layer that:
- evaluates trade decisions against system rules
- highlights mistakes and deviations
- summarizes behavioral patterns
- introduces a discipline score

## Scope
- Trade Review (per trade evaluation)
- Mistake Detection (rule violations)
- Behavior Summary (pattern insights)
- Discipline Score (optional scoring layer)
- UI section: Decision Review

## Out of Scope
- predictive coaching
- automated recommendations
- performance attribution beyond existing metrics

## Success Criteria
- users can identify at least one mistake in their behavior
- users can understand if they followed system logic
- outputs remain observational (no advisory tone)