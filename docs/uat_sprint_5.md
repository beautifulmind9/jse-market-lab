# UAT — Sprint 5: Allocation Layer

## Objective

Validate that the allocation layer turns planner trades into a clear, rule-based capital plan without violating risk limits.

## Scope

This UAT covers:

* allocation percentages
* capital amounts
* exposure caps
* cash reserve enforcement
* trade prioritization

Out of scope:

* signal generation
* confidence generation
* earnings detection

## Test Scenarios

### 1. Strong trade gets larger allocation

Expected:

* strong > moderate
* strong > high risk

### 2. Tier C gets zero

Expected:

* no allocation assigned

### 3. Liquidity fail gets zero

Expected:

* no allocation assigned

### 4. High earnings severity reduces allocation

Expected:

* reduced from base amount

### 5. High volatility reduces allocation

Expected:

* reduced from base amount

### 6. Max funded trades enforced

Expected:

* no more than 3 funded trades

### 7. Max exposure enforced

Expected:

* total allocated <= 70%

### 8. Cash reserve enforced

Expected:

* cash >= 30%

## Validation Questions

* Does the output clearly show where money should go?
* Does the logic feel disciplined and understandable?
* Does the plan remain usable for a normal investor?

## Risks to Watch

* Users may treat allocations as guarantees
* Users may want more customization too early
* Allocation wording may need simpler Jamaican phrasing in Clear mode

## Final UAT Status

(To be completed after implementation review)
