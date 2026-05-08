# Cost Assumptions Alignment — JSE Market Lab

## Purpose

This note records a current mismatch between product/planning assumptions and the active engine cost defaults.

It exists so future setup-testing, paper-portfolio, portfolio-economics, and API work do not accidentally mix different fee assumptions.

---

## Current Engine Defaults

The active default cost profile currently lives in:

```text
app/costs/profiles.py
```

Current implementation:

```python
DEFAULT_PROFILE = {"broker_fee": 0.001, "cess": 0.0005}
```

This equals:

```text
Broker fee: 0.10%
CESS: 0.05%
```

These are the values currently used by existing backend calculations unless another profile is introduced.

---

## Product / Planning Assumption

Several product strategy and platform-planning notes refer to a future or target planning assumption:

```text
Broker fee: 0.50%
CESS: 0.35%
```

These values should be treated as target/planning assumptions until the engine profile is explicitly updated and tested.

---

## Product Risk

If future Setup Tester, Paper Portfolio, Portfolio Economics, or frontend P/L views use the planning assumptions while the backend engine uses the current defaults, simulated net return and JMD P/L outputs will diverge.

This could confuse users and weaken trust.

---

## Required Follow-Up

Create a separate implementation PR to decide and align cost profiles.

That PR should:

1. Confirm the intended broker fee and CESS assumptions.
2. Decide whether to update `DEFAULT_PROFILE` or add named broker profiles.
3. Update tests for cost calculations.
4. Update all product docs to distinguish current defaults from planning assumptions.
5. Ensure portfolio, ticker, review, setup testing, and paper portfolio outputs use the same source of truth.

---

## Recommended Direction

Prefer named cost profiles instead of silently changing defaults.

Example:

```python
PROFILES = {
    "Default": {"broker_fee": 0.001, "cess": 0.0005},
    "JMMB planning": {"broker_fee": 0.005, "cess": 0.0035},
}
```

This allows the dashboard to preserve historical behavior while introducing clearer real-world broker assumptions.

---

## Product Language Rule

Until the cost engine is aligned, user-facing outputs should avoid implying that one fee profile is universal.

Use:

```text
Estimated costs are based on the selected cost profile.
```

Avoid:

```text
These are the exact fees every investor will pay.
```
