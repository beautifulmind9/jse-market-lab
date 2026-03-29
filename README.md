# 📈 JSE Decision Support Dashboard

> A rule-based decision-support system that helps investors on the Jamaican Stock Exchange (JSE) **identify, evaluate, and prioritize trades** using structured signals, risk awareness, and simplified guidance.

---

## 🚀 Overview

This project is a **data-driven product**, not just a dashboard.

It is designed to help investors move from:

> “What looks interesting?” → **“What should I actually do with my money?”**

Unlike typical market dashboards, this system:

* focuses on **decision-making**, not just data display
* incorporates **real-world constraints** (fees, liquidity, execution risk)
* translates signals into **clear guidance and prioritization**

> ⚠️ This is a **decision-support tool**, not financial advice or a signal-selling platform.

---

## 🧠 Problem

Retail investors in Jamaica often face:

* Limited access to structured analysis tools
* Low liquidity across many securities
* High noise in short-term price movements
* Overestimation of returns due to ignoring costs
* Difficulty interpreting technical signals

As a result, decisions are often:

* inconsistent
* reactive
* not grounded in historical behavior

---

## 🎯 Solution

This dashboard provides a **structured decision framework** that:

* Identifies trading opportunities
* Evaluates signal quality
* Flags risk (earnings, volatility, liquidity)
* Provides **behavioral guidance**
* **Prioritizes trades by confidence**

---

## 🧩 System Flow

```text
Data → Signal → Score → Risk → Guidance → Confidence → Decision
```

---

## ⚙️ Core Features

### 1. Signal Engine

* Event-based signals using **median crossover logic**
* More robust to noise than moving averages

---

### 2. Quality Scoring (Tier A / B / C)

Signals are evaluated using:

* Trend strength (slope)
* Spread widening (momentum)
* Volume confirmation
* Volatility filtering

👉 Tier A = strongest
👉 Tier C = watchlist only (not funded)

---

### 3. Earnings Risk Awareness

Trades are tagged by earnings phase:

* pre
* reaction
* post
* non

The system flags trades that **overlap with earnings windows**, highlighting uncertainty.

---

### 4. Trade Guidance Layer (Sprint 2–3)

Transforms risk into **clear actions**:

* Reduce exposure
* Monitor closely
* No immediate action

Supports:

* **Clear mode** (simple, everyday language)
* **Pro mode** (more technical phrasing)

---

### 5. Confidence Layer (Sprint 4)

Introduces **trade prioritization**:

Each trade is classified as:

* **Stronger setup** → consider funding
* **Decent setup** → proceed carefully
* **Watch closely** → do not fund yet
* **Avoid this setup** → skip

This helps answer:

> “Which trades deserve my capital first?”

---

### 6. Weekly Trade Planner

Applies structure to execution:

* Holding windows: **5D, 10D, 20D, 30D**
* Capital discipline rules
* Trade-level evaluation

---

### 7. Cost-Aware Modeling

All results account for:

* Broker fee: **0.50%**
* CESS: **0.35%**

👉 Prevents unrealistic expectations

---

### 8. Backtesting & Validation

The system evaluates:

* Win rate
* Median vs average returns
* Performance by holding window
* Net outcomes after costs

---

## 🧠 Key Product Decisions

* **Median over Average** → More robust in volatile markets
* **Tier System** → Simplifies prioritization
* **Liquidity Filters** → Ensures trades are executable
* **Cost Inclusion** → Reflects real outcomes
* **Confidence Layer** → Converts analysis into prioritization
* **Clear vs Pro Modes** → Improves accessibility across user levels

---

## 🧪 Product Development Approach

Built using an **iterative product approach**:

* **V1** → Signal generation
* **V2** → Scoring + ranking
* **V3** → Cost & liquidity realism
* **V4** → Planner + earnings risk
* **V5** → Guidance layer (Clear vs Pro)
* **V6** → Confidence layer (trade prioritization)

Each iteration improved:

* clarity
* usability
* decision quality

---

## 🧠 Learnings

* Median returns are more reliable than averages
* High volatility reduces consistency
* Liquidity significantly affects execution
* Costs materially change profitability
* Users need **guidance and prioritization**, not just signals

---

## 🚀 Roadmap

### Next (Sprint 5)

* Portfolio allocation layer
* Position sizing logic
* Capital distribution across trades

### Future

* AI-assisted insights
* Pattern recognition
* Personalized strategies

---

## 💼 Skills Demonstrated

* Product thinking & system design
* Decision-support system design
* Data modeling & backtesting
* Risk-aware financial logic
* Agile development (sprint-based)
* UAT and product validation
* UI/UX thinking for clarity

---

## 🛠️ Tech Stack

* Python (Pandas, NumPy)
* Streamlit (UI prototype)
* GitHub Actions (automation)
* CSV/JSON pipelines

---

## ▶️ Running the Project

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔗 Links

* Live App (Streamlit)
* Portfolio Case Study
* Resume

---

## 👤 Author

**Taneen Lewis**
Product-focused builder specializing in decision-support systems, data workflows, and practical financial tools.
