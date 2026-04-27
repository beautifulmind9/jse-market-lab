# UAT — Sprint 16 (Live Context & Trade Timing)

## Test Area 1: Viewed Timestamp

- [ ] Timestamp is visible on Portfolio tab
- [ ] Timestamp is visible on Ticker Analysis tab
- [ ] Timestamp updates on refresh
- [ ] Timestamp is clearly labeled

---

## Test Area 2: Dataset Date

- [ ] Latest market data date is displayed
- [ ] Matches max dataset date
- [ ] Does not show incorrect ranges

---

## Test Area 3: Holding Window Clarity

- [ ] Copy explicitly references trading days
- [ ] Copy clarifies that holding windows are **review periods**, not fixed holding deadlines
- [ ] Copy clarifies that users are not expected to hold until month-end
- [ ] Appears in both Portfolio and Ticker Analysis

---

## Test Area 4: No Misleading Behavior

- [ ] No wording suggests live market feed
- [ ] No wording suggests real-time signals
- [ ] System still behaves as static dataset

---

## Test Area 5: Stability

- [ ] No crashes from missing date fields
- [ ] Safe fallback if dataset date missing
- [ ] UI loads correctly in Guided and Advanced views

---

## Overall Result

- [ ] Pass
- [ ] Needs iteration
