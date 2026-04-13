# 🧪 UAT — Sprint 5 (Allocation Engine)

---

## 🎯 Objective

Validate that the allocation engine behaves correctly under real-world constraints.

---

## ✅ Test Cases

### 1. Tier C Handling
- Input: Tier C trade  
- Expected: allocation = 0%  

---

### 2. Liquidity Fail
- Input: liquidity_pass = False  
- Expected: allocation = 0%  

---

### 3. Confidence Priority
- Input: Strong vs Moderate  
- Expected: Strong > Moderate allocation  

---

### 4. Risk Reduction
- Input: earnings + high volatility  
- Expected: reduced allocation  

---

### 5. Exposure Cap
- Input: multiple strong trades  
- Expected: total allocation ≤ 70%  

---

### 6. Reserve Floor
- Expected: cash ≥ 30%  

---

### 7. Max Trades
- Input: 5 valid trades  
- Expected: only top 3 funded  

---

### 8. Deterministic Ordering
- Same input → same output always  

---

### 9. Output Structure

Each trade must include:
- allocation_pct  
- allocation_amount  
- confidence_label  
- explanation fields  

---

## ✅ Success Criteria

- All constraints enforced  
- Output stable and predictable  
- No invalid allocations

### 10. Allocation Reconciliation

- Expected:  
  sum(allocation_amount) == total_allocated_amount  

- Tolerance:  
  max difference ≤ $0.01  

- Result:  
  PASS if consistent
