# UAT — Sprint 17 (Trade Readiness, Liquidity & Data Foundations)

## Test Area 1: Trade Readiness Visibility

- [ ] Trade Readiness section appears where expected
- [ ] Liquidity data status appears if available
- [ ] Volume support status appears if available
- [ ] Spread / volatility context appears if available
- [ ] Missing fields use safe fallback wording

---

## Test Area 2: No Overclaiming

- [ ] UI does not say `liquidity confirmed` unless a true numeric threshold exists
- [ ] UI does not imply trade execution is guaranteed
- [ ] UI does not imply the stock is safe to enter
- [ ] Missing or limited data is described honestly

---

## Test Area 3: Funding vs Analysis Separation

- [ ] Ticker Analysis explains that the trade was selected by portfolio rules
- [ ] Supporting historical analysis does not contradict funded status
- [ ] Copy remains decision-support oriented, not advisory

---

## Test Area 4: Sample-Size Context

- [ ] Small sample notes include interpretation
- [ ] Small samples do not make funded trades sound invalid
- [ ] Broader samples are described as more mature where applicable

---

## Test Area 5: Signal-Date Readiness

- [ ] Existing signal-date fields are inspected
- [ ] Available fields are documented
- [ ] Missing fields are documented for future freshness logic
- [ ] Fresh / Active / Late / Stale labels are not implemented unless data is reliable

---

## Test Area 6: Regression Safety

- [ ] Ranking logic unchanged
- [ ] Allocation logic unchanged
- [ ] Signal generation unchanged
- [ ] Backtesting logic unchanged
- [ ] Existing Portfolio and Ticker Analysis flows still work

---

## Overall Result

- [ ] Pass
- [ ] Needs iteration
