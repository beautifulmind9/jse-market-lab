# Sprint 12 Backlog

## UI refinement
- [ ] improve spacing and readability across the app
- [ ] reduce clutter in main surfaces
- [ ] remove or consolidate redundant labels and columns
- [ ] keep page structure consistent

---

## Final insight structure
- [ ] implement final public-ready insight layout:
  - what’s happening
  - what to watch
  - common mistakes
  - feature explanation
- [ ] ensure insight text is simple and readable
- [ ] keep tone observational and non-advisory

---

## Beginner vs Analyst mode
- [ ] design mode split clearly
- [ ] implement Beginner Mode
- [ ] implement Analyst Mode
- [ ] validate that each mode shows the right level of detail

---

## First-run experience
- [ ] auto-load demo dataset
- [ ] confirm default landing view
- [ ] show useful insight immediately
- [ ] remove unnecessary friction for first-time users

---

## Language standardization
- [ ] review wording across app
- [ ] simplify technical phrasing
- [ ] align tone to plain Jamaican-friendly English
- [ ] keep tone neutral and clear

---

## Product framing / monetization surface
- [ ] define light Free vs Pro framing in UI
- [ ] highlight what is available in Free
- [ ] lightly signal what deeper access would unlock
- [ ] avoid aggressive upgrade prompts

---

## Deployment
- [ ] add `streamlit` to `requirements.txt`
- [ ] confirm `app.py` works from repo root
- [ ] verify demo data paths work in cloud deployment
- [ ] connect GitHub repo to Streamlit Community Cloud
- [ ] deploy app
- [ ] test public URL

---

## Documentation
- [ ] update README for public use
- [ ] add screenshots
- [ ] add simple product walkthrough
- [ ] align docs with final Phase 1 scope

## Language system + mode differentiation
- [ ] define shared language rules for Jamaican-friendly English
- [ ] define Beginner vs Analyst wording patterns
- [ ] create lightweight language formatting module
- [ ] apply mode-aware language to first-run experience
- [ ] apply mode-aware language to insights
- [ ] apply mode-aware language to Portfolio Plan
- [ ] apply mode-aware language to Decision Review
- [ ] apply mode-aware language to Ticker Analysis summaries
- [ ] add language-mode tests

## Sprint 12 Step 2 — First-run experience + language system + mode differentiation
- [ ] add first-run header and “How to read this” block
- [ ] extend insight block to final structure:
  - what’s happening
  - what to watch
  - common mistakes
  - why this matters
- [ ] create lightweight language formatting module
- [ ] add Beginner vs Analyst mode toggle
- [ ] apply mode-aware language to:
  - first-run experience
  - insights
  - Portfolio Plan
  - Decision Review
  - Ticker Analysis summaries
- [ ] add language-mode tests

## Sprint 12 Step 4 — Mode-based tab access + visual polish
- [ ] restrict Analyst Insights to Analyst mode
- [ ] restrict Data tab to Analyst mode
- [ ] build mode-aware top-level tabs
- [ ] improve visual polish of:
  - first-run intro
  - final insight block
  - Portfolio summary
  - Review summary
- [ ] add one restrained accent color
- [ ] improve spacing and section hierarchy
- [ ] reduce harsh black/white/grey feel
- [ ] add/update tests for mode-based tab visibility

## Ticker Analysis redesign
- [ ] redesign Ticker Analysis around decision-first summaries
- [ ] add Quick Take section
- [ ] add Best Holding Strategy section
- [ ] add Risk Profile section
- [ ] add What Usually Happens section
- [ ] add What to Watch section
- [ ] keep Analyst deep-dive tables in Analyst mode only
- [ ] simplify/hide raw Signal Breakdown for Beginner mode
- [ ] remove duplicate insight bullets
- [ ] normalize XD-style ticker markers into canonical tickers
- [ ] update tests for ticker normalization and mode-based Ticker Analysis behavior

# Sprint 12 Backlog

## Goal
Make the dashboard public-ready by improving deployment stability, user understanding, app structure, and trust in the data layer.

---

## Completed

### Deployment / Stability
- [x] prepare app for hosted deployment
- [x] harden restricted-filesystem artifact writes
- [x] remove silent failure risks around artifact generation
- [x] handle missing legacy event file safely
- [x] add zero-entry-price guard

### First-run experience
- [x] add product framing at top of app
- [x] add “How to read this” section
- [x] surface final insight early in app flow

### Language / Modes
- [x] add shared explanation formatting
- [x] introduce Beginner vs Analyst mode
- [x] simplify Beginner experience
- [x] keep Analyst experience richer

### Information architecture
- [x] remove duplicated/nested rendering
- [x] move technical/raw content out of Review
- [x] add Data tab
- [x] improve tab structure

### Data trust
- [x] integrate bundled internal JSE dataset
- [x] surface dataset source in UI
- [x] make fallback behavior visible
- [x] improve data status presentation

### Canonical normalization
- [x] standardize canonical ticker
- [x] preserve `instrument` as alias
- [x] normalize XD marker variants
- [x] preserve raw symbol metadata

### Insights / Ticker Analysis
- [x] remove duplicate insight bullets
- [x] redesign Ticker Analysis around interpretation-first structure
- [x] reduce raw-table overload in Beginner mode

---

## Carry-forward / Not fully addressed

- [ ] strengthen Portfolio Plan interpretation-first layer
- [ ] explain setup strength clearly in Portfolio
- [ ] explain confidence clearly in Portfolio
- [ ] explain reserved cash clearly in Portfolio
- [ ] continue visual polish
- [ ] tighten global explanation consistency across sections
