# Cost Assumptions Alignment — JSE Market Lab

## Purpose

This note records the platform direction for aligning cost assumptions across the engine, API, frontend, documentation, and future simulation workflows.

It exists so future setup-testing, paper-portfolio, portfolio-economics, and API work do not accidentally mix different fee assumptions.

---

## Current Direction

JSE Market Lab should not use one broker as the universal default.

Broker fees can vary by:

- broker
- trading channel
- manual vs online workflow
- transaction size
- account type
- taxes and other charges
- future platform changes such as JTrader or broker portals

Therefore, the product should support:

1. Neutral planning profiles
2. Broker-specific profiles only where verified
3. A custom estimate / range-slider direction later
4. Clear disclosure that all costs are estimates until confirmed by the broker

---

## Neutral Cost Profiles

The active cost profile source lives in:

```text
app/costs/profiles.py
```

The product should use neutral names such as:

```text
Legacy default estimate
Low-cost estimate
Conservative estimate
High-cost estimate
Custom estimate, future
Select broker profile, future once verified
```

Avoid naming a broker as the default planning profile.

---

## Legacy Engine Default

The earlier engine default was:

```python
DEFAULT_PROFILE = {"broker_fee": 0.001, "cess": 0.0005}
```

This equals:

```text
Service charge estimate: 0.10%
Market charge estimate: 0.05%
```

This should be treated as a legacy internal estimate, not a universal market fee.

---

## Planning Estimates

Several product strategy and platform-planning notes previously referred to:

```text
Broker fee: 0.50%
CESS: 0.35%
```

These should now be treated as one possible planning estimate, not a universal broker profile and not a default named after any one broker.

---

## Broker Fee Research Table

A broker fee research scaffold exists at:

```text
data/reference/broker_fee_profiles.csv
```

This file should capture:

- broker name
- channel
- broker commission percentage
- minimum fee, if known
- market/exchange/cess assumptions, if stated
- tax treatment, if stated
- source URL
- source date
- verification status
- notes

Broker-specific fee profiles should only be exposed in the product after values are verified from official broker materials or direct broker confirmation.

---

## Product Risk

If future Setup Tester, Paper Portfolio, Portfolio Economics, or frontend P/L views use one assumption while backend logic uses another, simulated net return and JMD P/L outputs will diverge.

This could confuse users and weaken trust.

---

## Required Follow-Up

Cost work should continue in stages:

1. Keep neutral cost profiles explicit in the engine/API/frontend.
2. Research broker-specific fee schedules from official sources.
3. Mark unverified broker data as unavailable / confirm with broker.
4. Add a custom estimate slider later.
5. Ensure portfolio, ticker, review, setup testing, and paper portfolio outputs use the same source of truth.

---

## Recommended UI Direction

Use a cost selector with options such as:

```text
Cost profile:
- Low-cost estimate
- Conservative estimate
- High-cost estimate
- Custom estimate, future
- Select broker profile, future once verified
```

For custom estimate later:

```text
Service charge slider
Market charge / fee slider
Minimum fee field, optional
Other charges / taxes field, optional
```

---

## Product Language Rule

Use:

```text
Estimated costs are based on the selected cost profile. Actual fees may vary by broker, channel, transaction size, taxes, and account terms. Confirm fees with your licensed broker before acting.
```

Avoid:

```text
These are the exact fees every investor will pay.
This broker is best.
This broker should be used by default.
```
