# UAT — Sprint 4: Trade Confidence Layer

## Objective

Validate that the Trade Confidence layer correctly classifies trades into clear, understandable priority levels and integrates properly into the planner UI without breaking existing functionality.

---

## Feature Under Test

Trade Confidence Classification

* Function: `generate_trade_confidence(trade_row)`
* UI Placement: Between Warning and Guidance blocks in each trade card
* Modes: Clear (default) and Pro

---

## Scope

This UAT covers:

* Confidence classification logic
* Output structure correctness
* UI rendering and order
* Clear vs Pro language switching
* Integration with existing planner flow

Out of scope:

* Strategy signal generation
* Earnings detection logic
* Guidance logic (already tested in Sprint 3)

---

## Test Environment

* Local Streamlit app
* Test suite via pytest
* Planner view with multiple trade rows

---

## Test Scenarios

### 1. Liquidity Fail → Avoid

**Input**

* liquidity_pass = False

**Expected Result**

* Confidence level = "avoid"
* UI shows error-style block
* Title: "Avoid this setup"
* Clear message emphasizes difficulty entering/exiting trade

**Status**
✅ Pass

---

### 2. High Severity → High Risk

**Input**

* liquidity_pass = True
* severity = "high"

**Expected Result**

* Confidence level = "high risk"
* UI shows error-style block
* Message reflects elevated uncertainty

**Status**
✅ Pass

---

### 3. Strong Setup (Tier A + Controlled Volatility)

**Input**

* quality_tier = "A"
* volatility_bucket != "high"
* severity != "high"

**Expected Result**

* Confidence level = "strong"
* UI shows info-style block
* Message indicates stronger setup relative to others

**Status**
✅ Pass

---

### 4. Moderate Setup (Tier A/B with Conditions)

**Input**

* quality_tier in ["A", "B"]
* severity in ["info", "caution"]

**Expected Result**

* Confidence level = "moderate"
* UI shows info-style block
* Message suggests balanced or cautious sizing

**Status**
✅ Pass

---

### 5. Watchlist Setup (Tier C)

**Input**

* quality_tier = "C"

**Expected Result**

* Confidence level = "watch"
* UI shows warning-style block
* Message clearly indicates “do not fund yet”

**Status**
✅ Pass

---

### 6. Fallback Handling

**Input**

* Unknown tier (e.g., "D")

**Expected Result**

* Defaults to "moderate"
* No crash or missing fields

**Status**
✅ Pass

---

## UI Validation

### 7. Rendering Order

**Expected Order**

1. Header
2. Warning
3. Confidence
4. Guidance
5. Trade math

**Status**
✅ Pass

---

### 8. Confidence Block Visibility

**Expected**

* Always renders (no conditional hiding)
* Appears consistently across all trade cards

**Status**
✅ Pass

---

### 9. Clear vs Pro Mode Switching

**Steps**

* Toggle between Clear and Pro modes

**Expected**

* Confidence text changes accordingly
* No layout shifts or duplication

**Status**
✅ Pass

---

### 10. No Duplicate UI Elements

**Expected**

* No additional toggles introduced
* No repeated widgets per trade card

**Status**
✅ Pass

---

## Data Integrity Validation

### 11. Output Structure

**Expected Keys**

* confidence_label
* confidence_title
* confidence_body_clear
* confidence_body_pro
* confidence_level

**Status**
✅ Pass

---

### 12. Deterministic Behavior

**Expected**

* Same input always produces same output
* No randomness or dependency on external state

**Status**
✅ Pass

---

## Edge Cases

### 13. Missing Fields

**Input**

* Missing severity, tier, or volatility

**Expected**

* No crash
* Defaults applied safely

**Status**
✅ Pass

---

### 14. Mixed Risk Signals

**Example**

* Tier A but high severity

**Expected**

* High risk overrides strength

**Status**
✅ Pass

---

## User Experience Observations

* Confidence layer makes it easier to scan trades quickly
* Clear mode is significantly more readable for non-technical users
* Pro mode still useful for experienced investors
* Users are likely to prioritize “Strong” setups immediately
* “Watch” label effectively prevents premature entries

---

## Risks Identified

* Users may interpret "Strong" as guaranteed success
* Over-reliance on labels without reading guidance
* Language may still need further localization tuning for broader Jamaican audience

---

## Recommendations

* Consider softening wording:

  * "Strong confidence" → "Stronger setup"
  * "Moderate confidence" → "Decent setup"
* Future enhancement:

  * Add explanation tooltip: “What makes this strong?”
* Monitor user behavior around “Strong” classification

---

## Acceptance Criteria

* All classification branches behave correctly
* UI renders confidence in correct position
* Clear/Pro switching works consistently
* No UI duplication or widget conflicts
* Tests pass successfully

---

## Final UAT Status

## ✅ Approved for Release

The Trade Confidence layer successfully adds prioritization to the planner without breaking existing functionality. It improves usability, decision clarity, and aligns with the product’s goal of guiding real-world investment behavior.

---

## Product Impact

This feature transitions the dashboard from:

* Insight tool → Decision-support system

Users can now:

* Identify opportunities
* Understand risk
* Receive guidance
* Prioritize capital allocation

This marks a significant step toward a fully guided investing workflow.
