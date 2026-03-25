# 📈 JSE Decision Support Dashboard

> A rule-based decision-support system for evaluating short- to medium-term trading opportunities on the Jamaican Stock Exchange (JSE).

---

## 🚀 Overview

This project is a **data-driven product** designed to help investors make **structured, risk-aware trading decisions**.

Unlike typical dashboards, this system:
- focuses on **decision-making**, not just data display  
- incorporates **real-world constraints** (fees, liquidity)  
- uses **rule-based logic validated through backtesting**

> ⚠️ This is a **decision-support tool**, not financial advice or a signal-selling platform.

---

## 🧠 Problem

Retail investors in Jamaica often face:

- Limited access to structured analysis tools  
- Low liquidity across many securities  
- High noise in short-term price movements  
- Overestimation of returns due to ignoring costs  

As a result, decisions are:
- inconsistent  
- reactive  
- not grounded in historical behavior  

---

## 🎯 Solution

This dashboard provides a **structured framework** to:

- Identify trading opportunities  
- Evaluate signal quality  
- Incorporate risk factors (earnings, volatility, liquidity)  
- Simulate real-world outcomes (net of fees + CESS)

---

## ⚙️ Core Features

### 1. Signal Engine
- Event-based signals using **median crossover logic**
- Reduces sensitivity to short-term noise

---

### 2. Quality Scoring (Tier A / B / C)

Signals are evaluated based on:

- Trend strength (slope)  
- Spread widening (momentum)  
- Volume confirmation  
- Volatility filtering  

👉 Tier A = strongest, Tier C = weakest (watchlist only)

---

### 3. Weekly Trade Planner

Transforms signals into actionable decisions:

- Holding windows: **5D, 10D, 20D, 30D**  
- Capital allocation logic  
- Net P/L after:
  - Broker fee: **0.50%**
  - CESS: **0.35%**

---

### 4. Earnings Risk Awareness

Signals are tagged by earnings phase:

- pre  
- reaction  
- post  
- non  

The system flags trades that **overlap with earnings windows**, highlighting increased uncertainty.

---

### 5. Backtesting & Validation

The system evaluates:

- Win rate  
- Median vs average returns  
- Performance by holding window  
- Cost-adjusted outcomes  

---

## 🧩 System Design
Data → Signal → Score → Filter → Planner → Decision


### Components:
- Data ingestion & validation  
- Cost engine (realistic trading drag)  
- Ranking/scoring engine  
- Earnings phase module  
- Weekly planner (decision layer)  

---

## 📊 Key Product Decisions

- **Median vs Average** → More robust to outliers  
- **Tier System** → Simplifies prioritization  
- **Liquidity Filters** → Ensures tradability  
- **Cost Inclusion** → Prevents unrealistic expectations  
- **Tier C Exclusion** → Focus on higher-quality opportunities  

---

## 🧪 Product Development Approach

This project was built using an **iterative, product-focused approach**:

### Iterations:
- V1 → Signal generation  
- V2 → Scoring + ranking  
- V3 → Cost & liquidity realism  
- V4 → Planner + earnings risk layer  

Each iteration improved:
- clarity  
- usability  
- decision quality  

---

## 🧠 Learnings

- Median returns are more reliable than averages in volatile markets  
- High volatility reduces consistency of outcomes  
- Liquidity constraints significantly affect execution  
- Including costs materially changes perceived profitability  
- Users need **explanations**, not just signals  

---

## 🚀 Roadmap

### V1 (Current)
- Core decision engine  
- Signal ranking  
- Weekly Trade Planner  
- Earnings warnings  

### V2
- Enhanced UI/UX  
- Explanation layer (“why this signal”)  
- Portfolio-level insights  

### V3
- AI-assisted insights  
- Pattern recognition  
- Personalization  

---

## 💼 Skills Demonstrated

- Product thinking & system design  
- Data-driven decision-making  
- Financial modeling (cost-aware)  
- Agile development (iterative builds)  
- Requirement definition & UAT  
- Risk-aware strategy design  

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)  
- Streamlit (prototype UI)  
- GitHub Actions (automation)  
- CSV/JSON pipelines (data outputs)  

---

## ▶️ Running the Project

```bash
pip install -r requirements.txt
streamlit run app.py

---

## 🔗 Links

- Live App (Streamlit)
- Portfolio Case Study (Notion)
- Resume

---

## 👤 Author

- Taneen Lewis
- Product-focused builder specializing in decision-support systems and data-driven workflows.
