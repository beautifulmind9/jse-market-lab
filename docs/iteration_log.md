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
