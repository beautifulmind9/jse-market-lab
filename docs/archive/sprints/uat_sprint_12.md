# UAT — Sprint 12

## Overall Status
Not started

## Public-readiness checklist

| Area | Status | Notes |
|---|---|---|
| App loads from a public URL | Not started | |
| No technical setup required | Not started | |
| Demo data loads automatically | Not started | |
| Default landing view feels sensible | Not started | |
| Insight section is visible immediately | Not started | |
| UI feels clean and readable | Not started | |
| Beginner Mode works | Not started | |
| Analyst Mode works | Not started | |
| Language is simple and clear | Not started | |
| Language feels Jamaican-friendly | Not started | |
| No confusing labels remain | Not started | |
| Free vs Pro framing is understandable | Not started | |
| App runs without deployment errors | Not started | |

## Pass criteria
Sprint 12 passes when:
- users can open the app through a public link
- first-time users can understand what they are seeing quickly
- the dashboard feels clear, structured, and credible
- the product is clearly positioned as a decision-support system

# UAT — Sprint 12

## Overall Status
In progress — deployment-readiness hardening complete

## Public-readiness checklist

| Area | Status | Notes |
|---|---|---|
| App loads from a public URL | Not started | |
| No technical setup required | Not started | |
| Demo data loads automatically | Not started | |
| Default landing view feels sensible | Not started | |
| Insight section is visible immediately | Not started | |
| UI feels clean and readable | Not started | |
| Beginner Mode works | Not started | |
| Analyst Mode works | Not started | |
| Language is simple and clear | Not started | |
| Language feels Jamaican-friendly | Not started | |
| No confusing labels remain | Not started | |
| Free vs Pro framing is understandable | Not started | |
| Deployment dependencies are complete | Pass | `requirements.txt` now includes Streamlit and runtime imports |
| Restricted filesystem behavior is safe | Pass | Demo artifact writes tolerate PermissionError and read-only filesystem conditions |

## Open item
- unrelated pre-existing failing planner explanation test should be resolved or explicitly documented before final closeout

## Pass criteria
Sprint 12 passes when:
- users can open the app through a public link
- first-time users can understand what they are seeing quickly
- the dashboard feels clear, structured, and credible
- the product is clearly positioned as a decision-support system

# UAT — Sprint 12

## Overall Status
In progress — public deployment complete

## Public-readiness checklist

| Area | Status | Notes |
|---|---|---|
| App loads from a public URL | Pass | https://jsemarketlab.streamlit.app/ |
| No technical setup required | Pass | Public deployment complete |
| Demo data loads automatically | In progress | Needs live validation |
| Default landing view feels sensible | In progress | Needs live validation |
| Insight section is visible immediately | In progress | Needs live validation |
| UI feels clean and readable | In progress | Needs live validation |
| Beginner Mode works | Not started | |
| Analyst Mode works | Not started | |
| Language is simple and clear | In progress | Needs live validation |
| Language feels Jamaican-friendly | In progress | Needs live validation |
| No confusing labels remain | In progress | Needs live validation |
| Free vs Pro framing is understandable | Not started | |
| Deployment dependencies are complete | Pass | Streamlit deployment succeeded |
| Restricted filesystem behavior is safe | Pass | Deployment hardening completed |

## Pass criteria
Sprint 12 passes when:
- users can open the app through a public link
- first-time users can understand what they are seeing quickly
- the dashboard feels clear, structured, and credible
- the product is clearly positioned as a decision-support system

## Language + mode checks

| Area | Status | Notes |
|---|---|---|
| Beginner Mode avoids jargon | Not started | |
| Beginner Mode explains meaning before metrics | Not started | |
| Analyst Mode includes key percentages where helpful | Not started | |
| Analyst Mode still reads clearly | Not started | |
| Jamaican-friendly tone feels natural | Not started | |
| No advisory language appears | Not started | |
| Core sections use consistent tone | Not started | |

# Sprint 12 — UAT Checklist

## Objective
Validate that the dashboard is stable, understandable, and trustworthy enough for public-facing Phase 1 use.

---

## 1. App Startup

- [x] App loads without requiring user upload
- [x] App starts with bundled internal dataset
- [x] App does not crash on startup
- [x] Missing legacy demo event files do not break app startup
- [x] First-run section renders correctly
- [x] Mode toggle renders correctly

---

## 2. Data Trust

- [x] Data source label is visible
- [x] Default dataset uses bundled JSE historical data
- [x] Fallback warning appears only if fallback dataset is used
- [x] Data tab shows:
  - [x] Source
  - [x] Rows loaded
  - [x] Errors
  - [x] Warnings
  - [x] Dataset ID in Analyst mode
- [x] No technical JSON/debug dump shown to users in core flow

---

## 3. Canonical Data Integrity

- [x] Canonical ticker is stable
- [x] `instrument` remains backward-compatible alias
- [x] Marker variants do not split instruments:
  - [x] CARXD
  - [x] CAR XD
  - [x] CAR-XD
  - [x] CAR (XD)
- [x] Raw symbol metadata is preserved:
  - [x] raw_symbol
  - [x] symbol_marker
  - [x] display_symbol

---

## 4. Portfolio / Review

- [x] Portfolio tab loads correctly
- [x] Review tab loads correctly
- [x] Total capital control appears in Portfolio only
- [x] Review tab no longer contains raw data dump
- [x] Portfolio and Review use same capital context
- [x] Decision review still renders when legacy events file is absent

---

## 5. Ticker Analysis

- [x] Ticker dropdown loads from canonical ticker universe
- [x] No duplicate ticker variants appear
- [x] Metrics change when ticker changes
- [x] Beginner mode hides deeper raw-table-heavy content
- [x] Analyst mode preserves deeper analysis
- [x] Ticker Analysis uses interpretation-first structure
- [x] No broken sections when no volatility data exists
- [x] Signal breakdown remains available in Analyst mode

---

## 6. Insights / Language

- [x] Final insight block renders near top of app
- [x] Duplicate bullet lines are removed
- [x] Beginner mode is simpler than Analyst mode
- [x] No advisory language added
- [x] Explanation-first language is used in high-visibility surfaces

---

## 7. Stability / Safety

- [x] App does not crash when `earnings_events.csv` is missing
- [x] Legacy demo dependencies degrade gracefully
- [x] Zero-entry-price guard prevents invalid return calculation crash
- [x] No silent fallback behavior for trust-critical paths

---

## Verdict

✅ Pass

Sprint 12 meets the Phase 1 public-ready baseline:
- stable startup
- real bundled JSE data
- cleaner public app structure
- canonical data integrity
- improved user-facing interpretation
