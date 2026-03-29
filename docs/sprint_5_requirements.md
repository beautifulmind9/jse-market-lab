# 📋 Sprint 5 Requirements — Allocation Layer

---

## Functional Requirements

1. System must assign allocation % to each trade

2. Allocation must be based on:

   * Confidence level
   * Quality tier
   * Risk flags

3. System must enforce:

   * Max active trades
   * Max allocation per trade
   * Total portfolio exposure

4. System must calculate:

   * Suggested dollar allocation

---

## Non-Functional Requirements

* Output must be easy to understand
* Clear Mode must avoid technical jargon
* System must remain fast and responsive

---

## Acceptance Criteria

* No trade exceeds max allocation
* Total exposure ≤ 70%
* Cash reserve ≥ 30%
* Tier C trades receive 0 allocation
* Risk flags reduce allocation

---

## Definition of Done

* Allocation logic implemented
* Output visible in dashboard
* UAT completed
* Results align with rules
