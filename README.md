# 📈 JSE Decision Support Dashboard

> A rule-based decision-support system that translates market signals into structured, risk-aware portfolio decisions on the Jamaican Stock Exchange (JSE).

---

## 🚀 Overview

This project is a **decision-support system**, not just a dashboard.

It helps investors move from:
❌ reacting to price movements  
➡️ to  
✅ making structured, rule-based portfolio decisions  

The system integrates:
- signal detection  
- quality evaluation  
- risk awareness  
- portfolio allocation  

> ⚠️ This is **not financial advice**. It is a structured thinking tool.

---

## 🧠 Problem

Retail investors often:
- react emotionally to price movements  
- ignore costs and liquidity  
- lack structured decision frameworks  
- overestimate returns  

---

## 🎯 Solution

A system that:

1. Identifies signals  
2. Evaluates quality  
3. Applies real-world constraints  
4. Translates outputs into **portfolio allocation decisions**

---

## ⚙️ Core System Flow

Data → Signal → Score → Filter → Confidence → Allocation → Portfolio Decision

---

## 🔑 Key Features

### 1. Signal Engine
- Median crossover (event-based)
- Reduces noise vs traditional moving averages

---

### 2. Quality Scoring (Tier A / B / C)
Evaluates:
- Trend strength  
- Momentum (spread widening)  
- Volume confirmation  
- Volatility  

👉 Tier C = watchlist only (not funded)

---

### 3. Confidence System
Each trade is classified as:

- **Strong**
- **Moderate**
- **High Risk / Avoid**

---

### 4. Portfolio Allocation Engine 🧠

A deterministic system that:

- Allocates capital based on confidence  
- Applies risk reductions  
- Enforces constraints  

#### Key Rules:
- Max **70% total exposure**
- Min **30% cash reserve**
- Max **3 active trades**
- Tier C → **0 allocation**
- Liquidity fail → **0 allocation**

---

### 5. Earnings Risk Layer
Trades are tagged:

- pre  
- reaction  
- post  
- non  

The system flags trades overlapping earnings windows.

---

### 6. Backtesting & Validation
Evaluates:
- win rate  
- median vs average returns  
- performance by tier  
- cost-adjusted outcomes  

---

## 🧩 System Components

- Signal engine  
- Scoring engine  
- Liquidity filter  
- Cost model (fees + CESS)  
- Earnings phase module  
- Allocation engine  
- Planner (decision layer)  

---

## 🧠 Key Product Decisions

- Median over average (robustness)
- Tier system (clarity)
- Liquidity filters (execution realism)
- Cost inclusion (true profitability)
- Deterministic allocation (consistency)

---

## 🧪 Product Evolution

| Version | Focus |
|--------|------|
| V1 | Signal generation |
| V2 | Scoring + ranking |
| V3 | Risk realism (fees, liquidity) |
| V4 | Planner + earnings |
| V5 | Allocation + decision system |

---

## 🚀 Roadmap

### Next:
- Analyst Insights (feature validation)
- Ticker-level reports
- Plan history tracking
- Explanation engine (“why this trade”)

---

## 💼 Skills Demonstrated

- Product thinking  
- System design  
- Decision modeling  
- Risk-aware strategy  
- Data analysis (Python)  
- Agile delivery (sprints + UAT)  

---

## 🛠️ Tech Stack

- Python (Pandas, NumPy)  
- Streamlit  
- GitHub Actions  
- CSV / JSON pipelines  

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

👤 Author
Taneen Lewis
Product-focused builder creating data-driven decision systems.


---

# 📄 portfolio_allocation_rules.md

```markdown
# 🧠 Portfolio Allocation Rules

---

## 🎯 Objective

To ensure capital is deployed:
- consistently  
- realistically  
- with controlled risk  

---

## 🚫 Hard Stops (No Allocation)

The system assigns **0% allocation** if:

- quality_tier == "C"  
- liquidity_pass == False  

---

## 📊 Base Allocation (by Confidence)

| Confidence | Allocation |
|-----------|-----------|
| Strong    | High (≈25–30%) |
| Moderate  | Medium (≈15–20%) |
| Avoid     | 0% |

---

## ⚠️ Risk Adjustments

Allocation is reduced when:

- Earnings risk present  
- High volatility  
- Weak structure signals  

---

## 📌 Funding Order

Trades are funded in this order:

1. Strong confidence  
2. Moderate confidence  
3. Lower-risk profiles  
4. Tier A before Tier B  

---

## 🧱 Portfolio Constraints

- Max **3 funded trades**  
- Max **70% total exposure**  
- Min **30% cash reserve**  

---

## 🔄 Allocation Logic

1. Calculate base allocation  
2. Apply risk reductions  
3. Sort trades by priority  
4. Allocate sequentially  
5. Stop when constraints are reached  

---

## 🧠 Output

Each trade includes:
- allocation_pct  
- allocation_amount  
- confidence_label  
- reasoning  

---

## 💡 Design Philosophy

This system prioritizes:
- discipline over intuition  
- consistency over prediction  
- risk control over maximization  
