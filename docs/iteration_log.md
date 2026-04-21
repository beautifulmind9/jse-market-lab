# Iteration Log

| Version | Change                                | Reason                         |
|--------|----------------------------------------|--------------------------------|
| V1     | Signal detection                       | Identify opportunities         |
| V2     | Ranking system                         | Improve selection              |
| V3     | Cost engine                            | Add realism                    |
| V4     | Earnings tagging                       | Add event context              |
| V5     | Earnings warning logic                 | Highlight risk                 |
| V6     | Planner warning UI (Sprint 1)          | Improve user decision-making   |
| V6.1   | Null-handling patch (post-review fix)  | Prevent crashes and false alerts |
| V7     | Decision guidance layer                | Converts warnings into user-facing decision support |
| V8 | Jamaican clarity layer (Clear vs Pro) | Improved local readability and moved guidance mode control to the planner level for stable multi-card rendering |
| V9 | Trade confidence layer | Introduced prioritization logic to classify trades by strength and guide capital allocation decisions |
| V10 | Allocation layer | Converted trade prioritization into a portfolio-level capital plan |
| V11 | Analyst Intelligence Layer | Added feature validation, tier-window performance analysis, and exit analysis without changing core decision engines |
| V12 | Streamlit App Shell + Portfolio Plan UI | Made the dashboard runnable and turned allocation outputs into a visible portfolio review surface |
| V12.1 | Sprint 7 review hardening + validation | Corrected visible app wiring, resolved local duplicate-repo test collection issue, and confirmed full regression pass |
| V13 | Scope clarification for post-Sprint 7 work | Clarified that public-facing insight prompts were created for marketing/content support and are not automatically the next in-app sprint scope |
| V13.1 | Sprint 8 review hardening | Tightened explanation-priority logic so hard-stop rule failures are not mislabeled as generic portfolio constraints |
| V13.2 | Sprint 8 constraint classification refinement | Narrowed constraint detection to explicit portfolio-limit signals only, preventing false constrained classification from generic allocator wording |
| V13.3 | Sprint 8 ranking explanation extension | Added ranking and allocation-priority reasoning so the Portfolio Plan can explain why funded trades were selected ahead of other eligible trades |
| V13.4 | Sprint 8 embedded insight layer | Added in-app embedded insights and identified follow-up fixes for eligibility-aware decision status and more natural plain-language wording |
| V13.5 | Sprint 8 wording and status refinement | Improved embedded insight wording and identified the need to separate hard-stop ineligibility from zero-allocation risk sizing outcomes |
| V13.6 | Sprint 8 decision-status refinement | Added a distinct “reduced to zero” status so trades sized down to 0% are not misclassified as hard-stop ineligible |
| V13.7 | Sprint 8 closeout | Completed decision clarity layer with simplified wording, improved status model, and embedded insights that make the portfolio immediately understandable |
| V14 | Sprint 9 ticker intelligence first slice | Added ticker-level summary, stats, and behavior insights in a new Ticker Analysis tab, with follow-up review needed for comparison logic and wording quality |
| V14.1 | Sprint 10 return normalization hardening | Improved return alias support and distribution bucketing, with one final follow-up identified to normalize return units across all drilldown calculations |
| V14.2 | Sprint 10 closeout | Completed ticker drilldown with schema-consistent return handling, grouped stock behavior breakdowns, and stable pattern-summary logic across supported return aliases |
| V15 | Sprint 11 started | Introduced Review & Discipline Layer to evaluate user decision behavior and detect mistakes |
| V15.1 | Sprint 11 review hardening | Fixed decision-review edge cases around missing allocation percentages and overlapping trade/allocation inputs so mistake detection stays accurate and empty-safe |
| V15.3 | Sprint 11 UX refinement | Moved Decision Review into a Review subtab, added interpretation and improvement guidance, and grouped repeated mistakes into clearer summary output |
| V15.4 | Sprint 11 closeout | Completed the Review & Discipline Layer with separate Plan/Review subtabs, interpretation guidance, grouped mistake summaries, and hardened mistake-detection logic |
| V16 | Sprint 12 started | Began final Phase 1 sprint focused on public readiness, language clarity, first-run experience, product framing, and public deployment |
| V16.1 | Sprint 12 deployment hardening | Added Streamlit dependency and hardened demo artifact writes so restricted hosted filesystems do not break the app while unexpected I/O failures still surface |
| V16.2 | Sprint 12 public deployment | Deployed the JSE Dashboard to Streamlit Community Cloud and made the product accessible through a public URL |
| V16.3 | Sprint 12 JSE data integration | Replaced the generic demo source with bundled historical JSE data and preserved backward compatibility by exposing both ticker and instrument through the loader |
| V17.0 | Sprint 13 planning started | Reframed the next sprint around user understanding, execution framing, Analyst Insights purpose, label cleanup, and median-first interpretation |
| V17.1 | Sprint 13 execution layer added to scope | Expanded Sprint 13 from a pure explanation sprint into a decision + execution framing sprint so the product answers not only what looks strong, but how a trade would typically be approached |
| V17.2 | Sprint 13 closeout | Completed Phase 2 clarity foundation: improved interpretation, execution framing, and surface-level understanding across Portfolio and Ticker Analysis |
| V18.0 | Sprint 14 UI architecture refresh started | Introduced Guided vs Advanced structure, onboarding improvements, and product-surface simplification |
| V18.1 | Sprint 14 scanability pass | Reduced visible clutter, improved snapshot readability, and shifted Guided portfolio to compact cards |
| V18.2 | Sprint 14 compatibility hardening | Stabilized onboarding and UI behavior across environments |
| V18.3 | Sprint 14 portfolio decision-surface redesign | Implemented comparison-first structure: compact Guided cards, compact Advanced tables with drilldowns, optional full analyst table |
| V18.4 | Sprint 14 first-run clarity closeout | Added capital input guidance, clearer ownership wording, helper text, and accurate loaded-data messaging |
| V18.5 | Phase 2A complete | Clarity, scanability, onboarding, and portfolio decision-surface redesign are complete; product now functions as a clear decision-support tool |
