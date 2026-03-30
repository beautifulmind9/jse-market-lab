# 🧭 Product Overview — JSE Decision Support Dashboard

---

## 📌 What this product is

The JSE Decision Support Dashboard is a **rule-based system** that helps investors:

* Identify trading opportunities
* Understand the quality of those opportunities
* Recognize risk before entering trades
* Decide what action to take
* Prioritize which trades deserve capital

This is not just a dashboard.

It is a **decision-support system** built for real-world investing conditions on the Jamaican Stock Exchange.

---

## 🎯 What problem it solves

Many investors can see market data, but still struggle with:

* Knowing which opportunities are worth acting on
* Understanding risk (especially around earnings)
* Interpreting technical signals
* Deciding how to prioritize multiple trades
* Avoiding inconsistent or emotional decisions

This product closes that gap by turning **market data → structured decisions**.

---

## 🧩 How the system works

The system follows a clear flow:

```text id="flow1"
Data → Signal → Score → Risk → Guidance → Confidence → Decision
```

Each layer adds meaning:

* **Signal** → Detects potential opportunities
* **Score** → Evaluates quality (Tier A/B/C)
* **Risk** → Flags uncertainty (earnings, volatility, liquidity)
* **Guidance** → Tells the user what to do
* **Confidence** → Helps prioritize trades
* **Decision** → Final output for action

---

## ⚙️ Core Product Layers

### 1. Signal Engine

* Uses median crossover logic
* Focuses on event-based opportunities
* Designed to reduce noise in JSE data

---

### 2. Quality Scoring

* Tier A → strongest setups
* Tier B → moderate setups
* Tier C → watchlist only

Scoring is based on:

* trend direction
* momentum (spread widening)
* volume confirmation
* volatility behavior

---

### 3. Risk Layer (Earnings Awareness)

* Tags trades by earnings phase:

  * pre
  * reaction
  * post
  * non

Flags trades that may behave unpredictably.

---

### 4. Guidance Layer (Clarity Layer)

Translates signals into **simple actions**:

* Reduce exposure
* Monitor closely
* No action

Includes:

* **Clear Mode** → simple, everyday language
* **Pro Mode** → more technical interpretation

---

### 5. Confidence Layer (Prioritization)

Helps users decide:

> “Which trade should I act on first?”

Outputs include:

* Stronger setup
* Decent setup
* Watch closely
* Avoid this setup

---

### 6. Planner Layer

Adds execution structure:

* Holding windows (5D, 10D, 20D, 30D)
* Trade evaluation discipline
* Real-world constraints

---

### 7. Cost Engine

Includes:

* Broker fee (0.50%)
* CESS (0.35%)

Ensures all results reflect **real outcomes**, not ideal scenarios.

---

## 🧠 Product Philosophy

This system is built on a few key beliefs:

* Data alone is not enough → users need **guidance**
* Signals are not decisions → users need **structure**
* More options create confusion → users need **prioritization**
* Ignoring costs leads to bad decisions → realism is required
* Simplicity increases usability → clarity matters

---

## 🧪 How this product was built

This product follows an **iterative development approach**:

* Sprint 1 → Signal generation
* Sprint 2 → Scoring and ranking
* Sprint 3 → Clarity (guidance layer)
* Sprint 4 → Confidence (prioritization layer)

Each sprint improved:

* usability
* interpretability
* decision quality

---

## 📂 How to navigate this repo

* `docs/product_brief.md` → Vision and purpose
* `docs/feature_breakdown.md` → Feature structure
* `docs/product_decisions.md` → Why decisions were made
* `docs/sprint_X_requirements.md` → Build specifications
* `docs/uat_sprint_X.md` → Validation and testing
* `docs/iteration_log.md` → Product evolution

---

## 🚀 What comes next

Next phase of development:

### Sprint 5 → Allocation Layer

* Capital distribution
* Position sizing
* Portfolio-level decision-making

---

## 💡 What this project demonstrates

This project shows:

* Product thinking (problem → solution → iteration)
* Real-world system design
* Data-driven decision frameworks
* Risk-aware modeling
* User-focused clarity and guidance
* End-to-end product development

---

## 👤 Author

Taneen Lewis
Building practical, decision-support systems that turn complex data into clear actions.

## 🔄 System Flow

Signal → Quality → Risk → Confidence → Allocation → Decision
