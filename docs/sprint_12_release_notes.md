# Sprint 12 Release Notes

## Release summary
Sprint 12 moved the JSE Dashboard from an internal prototype toward a public-ready Phase 1 product surface.

This release focused on:
- hosted-app readiness
- real bundled JSE historical data
- clearer first-run experience
- beginner vs analyst mode separation
- canonical ticker/data cleanup
- interpretation-first Ticker Analysis
- stability and trust improvements

---

## Highlights

### Real internal JSE dataset
The app now uses bundled historical JSE data by default instead of a generic demo-style dataset.

### Better first-run experience
Users now see:
- what the dashboard is
- how to read it
- an early insight block before diving into tabs

### Cleaner app structure
The app is now organized more clearly across:
- Portfolio
- Review
- Ticker Analysis
- Analyst Insights
- Data

### Canonical ticker cleanup
Temporary marker variants like XD no longer split the ticker universe.

### Ticker Analysis redesign
Ticker Analysis now leads with interpretation and meaning before deeper analyst detail.

### Stability improvements
- missing legacy events file no longer crashes the app
- zero-entry-price safety added
- fallback behavior is surfaced more clearly

---

## User impact

Users should now see:
- more trustworthy data behavior
- clearer app navigation
- less prototype-like structure
- stronger separation between beginner and analyst experiences

---

## Known limitations

- no live data feeds yet
- no upload/data-mode system yet
- no earnings/dividend intelligence layer yet
- Portfolio Plan still needs stronger explanation-first framing
