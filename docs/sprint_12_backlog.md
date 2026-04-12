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