# 🧭 Sprint 5 Plan — Allocation Layer

---

## 🎯 Objective

Introduce a **portfolio allocation layer** that determines:

* How much capital to assign to each trade
* How many trades to take at once
* How to manage total portfolio risk

This moves the system from **trade evaluation → capital decision-making**.

---

## 🧠 Problem

Even when users have good trade signals, they still struggle with:

* How much to invest per trade
* Overexposure to a single position
* Taking too many trades at once
* Poor capital distribution across opportunities

Result:

* inconsistent performance
* higher risk of losses
* lack of portfolio discipline

---

## 🎯 Solution

The system will:

* Allocate capital based on **confidence + risk**
* Limit total exposure
* Enforce portfolio discipline
* Provide a **clear investment plan**

---

## ⚙️ Core Features

### 1. Capital Allocation Engine

Inputs:

* Confidence level (Strong / Decent / Watch / Avoid)
* Quality tier (A / B / C)
* Risk flags (earnings overlap, volatility, liquidity)

Outputs:

* % allocation per trade
* Suggested dollar amount

---

### 2. Allocation Rules (v1 — Simple & Clear)

#### Default Portfolio Rules:

* Max active trades: **3–5**
* Max per trade:

  * Strong → up to **30–40%**
  * Decent → up to **15–25%**
  * Watch → **0% (no allocation)**
  * Avoid → **0%**

---

### 3. Portfolio Constraints

* Total active exposure: **60–70% max**
* Cash reserve: **30–40% minimum**

Purpose:

* protect against uncertainty
* allow flexibility

---

### 4. Risk Adjustments

Reduce allocation if:

* Earnings overlap = TRUE
* High volatility
* Low liquidity

Example:

```text
Strong setup (40%)  
→ Earnings risk → reduce to 25%
```

---

### 5. Allocation Output (User View)

User sees:

```text
📊 Portfolio Plan

Trade A → $40,000 (Strong)  
Trade B → $20,000 (Decent)  
Trade C → $15,000 (Decent)  

Cash Reserve → $25,000
```

---

### 6. Clear Mode vs Pro Mode

#### Clear Mode:

* “Put more money here”
* “Smaller position here”
* “Skip this one”

#### Pro Mode:

* Exact percentages
* Allocation reasoning
* Risk adjustments

---

## 🧪 Acceptance Criteria

### Functional

* System assigns allocation to each trade
* Total allocation does not exceed max exposure
* Risk flags reduce allocation appropriately
* Tier C trades receive no allocation

---

### Behavioral

* User understands:

  * where to put money
  * how much to invest
* Output feels:

  * simple
  * structured
  * actionable

---

## ⚠️ Constraints

* Must remain simple (v1)
* No complex optimization models yet
* No dynamic portfolio rebalancing (future)

---

## 🚀 Future Enhancements

* Dynamic allocation based on performance
* Portfolio rebalancing
* Risk-adjusted optimization
* Personal risk profiles

---

## 🧠 Product Impact

This layer answers the most important question:

> “How do I actually use my money?”

It transforms the product into:

👉 A **true decision system**, not just analysis
