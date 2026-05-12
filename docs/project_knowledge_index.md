# Project Knowledge Index — JSE Market Lab

## Purpose

This index maps the `docs/` folder so future build sessions, product planning, technical work, and compliance reviews can find the right source material quickly.

The repo now contains both active source-of-truth documents and historical sprint/archive material. Historical files are useful, but they should not override current product direction unless explicitly brought forward into a current source-of-truth doc.

---

## How to Use This Index

When starting a new build session, read the docs in this order:

1. `docs/current_platform_status.md`
2. `docs/project_knowledge_index.md`
3. `docs/platform_information_architecture_user_journeys.md`
4. `docs/product_decisions.md`
5. The specific topic doc for the work being done

For AI Helper work, also read:

```text
docs/ai_helper_definition.md
```

For deployment or architecture work, also read:

```text
docs/platform_architecture_and_hosting_decision.md
docs/backend_render_deployment.md
```

For compliance, data, research, broker, or monetization work, also read:

```text
docs/compliance_disclosure_playbook.md
docs/market_data_requirements.md
docs/source_material_reconciliation.md
docs/cost_assumptions_alignment.md
```

For older sprint context, use `docs/archive/`, `docs/sprints/`, and `docs/uat/` as supporting evidence only.

---

## Current Start-Here Docs

These documents should guide the current platform direction.

| Document | Role | Status |
|---|---|---|
| `docs/current_platform_status.md` | Current source-of-truth summary of the platform, pages, architecture, open issues, and roadmap. | Active source of truth |
| `docs/project_knowledge_index.md` | This index. Explains how docs are organized and which files to read for each type of work. | Active source of truth |
| `docs/platform_information_architecture_user_journeys.md` | Defines user intent, navigation logic, page flows, and the shift from dashboard to platform. | Active source of truth |
| `docs/product_decisions.md` | Captures major platform decisions, positioning, boundaries, and current product direction. | Active source of truth |
| `docs/source_material_reconciliation.md` | Helps reconcile earlier source material with the newer platform direction. | Active reference |

---

## Product Strategy Docs

Use these when discussing product direction, roadmap, monetization, platform expansion, or positioning.

| Document | Use For | Status |
|---|---|---|
| `docs/phase_3_9_platform_strategy.md` | Medium-to-long-term product expansion from dashboard to market intelligence platform. | Active strategy reference |
| `docs/feature_breakdown.md` | Feature inventory and platform modules. | Active strategy reference |
| `docs/backlog.md` | Backlog and future feature ideas. | Active roadmap reference |
| `docs/product_brief.md` | Product framing and high-level concept. | Historical/current reference, check against current status doc |
| `docs/user_flow.md` | Earlier user-flow documentation. | Supporting reference, check against current IA doc |
| `docs/portfolio_case_study.md` | Portfolio case-study framing. | Supporting reference |

---

## Architecture and Deployment Docs

Use these when working on Vercel, Render, FastAPI, Next.js, API routing, environment variables, or hosting choices.

| Document | Use For | Status |
|---|---|---|
| `docs/platform_architecture_and_hosting_decision.md` | Vercel + FastAPI/Render architecture, deployment decision, and platform hosting rationale. | Active source of truth |
| `docs/backend_render_deployment.md` | Render backend deployment guide and API hosting notes. | Active deployment reference |
| `docs/github_product_management_setup.md` | GitHub workflow setup, issue templates, labels, and roadmap-management direction. | Active product-ops reference |

---

## Compliance, Data Rights, and Disclosure Docs

Use these when discussing JSE/FSC/legal validation, data rights, public claims, research hosting, broker referrals, sponsored content, or disclaimers.

| Document | Use For | Status |
|---|---|---|
| `docs/compliance_disclosure_playbook.md` | Decision-support disclaimers, compliance-sensitive language, and disclosure boundaries. | Active compliance reference |
| `docs/market_data_requirements.md` | Market-data needs, field assumptions, and JSE-derived data considerations. | Active data reference |
| `docs/source_material_reconciliation.md` | Ensuring older content and new platform decisions do not conflict. | Active reference |
| `docs/cost_assumptions_alignment.md` | Broker fee/CESS assumptions and neutral cost-profile alignment. | Active reference |

Important boundary:

JSE Market Lab must not present itself as an official JSE data feed, investment advisor, broker, or trade execution service before required authorization and legal/compliance validation.

---

## AI Helper Docs

Use these when building, describing, or extending the platform AI Helper.

| Document | Use For | Status |
|---|---|---|
| `docs/ai_helper_definition.md` | Defines AI Helper as persistent platform guide, page-aware explainer, and future safe web research agent. | Active source of truth |
| `docs/current_platform_status.md` | Confirms current AI Helper shell status and future stages. | Active source of truth |

Current AI Helper status:

- persistent `Guide Me` shell exists
- page-aware rule-based content exists
- no live AI calls yet
- no internet search yet
- no user profile or memory behavior yet

Future AI Helper stages:

1. platform retrieval from docs/glossary/methodology
2. safe internet research with citations
3. user practice-profile integration
4. advanced explanation workflows

---

## Market/Data Methodology Docs

Use these when working on strategy logic, signal interpretation, holding windows, readiness checks, cost assumptions, or backtesting.

| Document | Use For | Status |
|---|---|---|
| `docs/market_data_requirements.md` | Data fields and market-data assumptions. | Active data reference |
| `docs/cost_assumptions_alignment.md` | Cost profile, broker fee, and CESS assumptions. | Active reference |
| `docs/sprint_17_trade_readiness.md` | Trade-readiness layer context. | Current/near-current sprint reference |
| `docs/sprint_17_signal_date_readiness_audit.md` | Signal-date/readiness audit context. | Current/near-current sprint reference |
| `docs/sprint_18_readiness_gating_risk_design.md` | Readiness gating and risk-control design. | Active research reference |

Use older archive sprint files for background only.

---

## Active Context Docs

Files in `docs/context/` are active project memory. They should be used to understand the product and user context, especially when a future chat needs continuity.

| Document | Use For | Status |
|---|---|---|
| `docs/context/jse_project_master_context.md` | Master project context and overarching direction. | Active context |
| `docs/context/product_context.md` | Product context and user/product framing. | Active context |
| `docs/context/strategy_context.md` | Strategy and decision-support context. | Active context |
| `docs/context/ux_learnings.md` | User testing, UX observations, and language/flow learnings. | Active context |

These files are not the same as `docs/archive/`. Treat them as important project memory.

---

## UAT and User-Testing Evidence

Files in `docs/uat/` capture UAT/user-testing history. Use them when evaluating UX decisions, language, onboarding clarity, and page-flow decisions.

| Document | Use For | Status |
|---|---|---|
| `docs/uat/README.md` | UAT folder guide. | Supporting reference |
| `docs/uat/uat_sprint_1.md` | Early UAT notes. | Historical UAT evidence |
| `docs/uat/uat_sprint_7.md` | Sprint 7 UAT notes. | Historical UAT evidence |
| `docs/uat/uat_sprint_13.md` | Sprint 13 UAT notes. | Historical UAT evidence |

UAT evidence is valuable, but it should be interpreted against the current product direction in `docs/current_platform_status.md`.

---

## Current Sprint / Recent Sprint Docs

Files in `docs/sprints/` are current or near-current sprint history.

| Document | Use For | Status |
|---|---|---|
| `docs/sprints/sprint_14_closeout.md` | Sprint 14 closeout history. | Sprint history |

Recent top-level sprint docs also matter:

| Document | Use For | Status |
|---|---|---|
| `docs/sprint_14_backlog.md` | Sprint 14 backlog. | Historical/near-current reference |
| `docs/sprint_14_closeout_template.md` | Sprint closeout template. | Historical/process reference |
| `docs/sprint_14_definition_of_done.md` | Sprint 14 DoD. | Historical/process reference |
| `docs/sprint_14_spec.md` | Sprint 14 specification. | Historical sprint reference |
| `docs/sprint_14_uat.md` | Sprint 14 UAT. | Historical UAT reference |
| `docs/sprint_14_user_stories.md` | Sprint 14 user stories. | Historical sprint reference |
| `docs/sprint_15_workflow.md` | Sprint 15 workflow. | Historical sprint reference |
| `docs/sprint_16_spec.md` | Sprint 16 specification. | Historical/near-current reference |
| `docs/sprint_17_trade_readiness.md` | Sprint 17 trade readiness. | Current/near-current reference |
| `docs/sprint_17_signal_date_readiness_audit.md` | Sprint 17 signal-date audit. | Current/near-current reference |
| `docs/sprint_18_readiness_gating_risk_design.md` | Sprint 18 readiness/risk design. | Active research reference |
| `docs/uat_sprint_15.md` | Sprint 15 UAT checklist. | Historical UAT reference |
| `docs/uat_sprint_16.md` | Sprint 16 UAT checklist. | Historical UAT reference |
| `docs/uat_sprint_17.md` | Sprint 17 UAT checklist. | Historical UAT reference |
| `docs/uat_sprint_18.md` | Sprint 18 UAT checklist. | Active/near-current UAT reference |

---

## Archive and Legacy Docs

Files in `docs/archive/` are historical references. They explain how the project evolved, but should not override current docs unless a decision is deliberately revived.

Important archive areas:

| Path | Use For | Status |
|---|---|---|
| `docs/archive/README.md` | Archive folder guide. | Historical reference |
| `docs/archive/legacy/overview.md` | Legacy product overview. | Historical reference |
| `docs/archive/legacy/case_study.md` | Legacy case study. | Historical reference |
| `docs/archive/sprints/` | Older sprint plans, requirements, UAT, UX notes, closeouts, handoffs, and backlog files. | Historical reference |

Examples of archived sprint material include:

```text
docs/archive/sprints/sprint_1_requirements.md
docs/archive/sprints/sprint_2_requirements.md
docs/archive/sprints/sprint_3_brief.md
docs/archive/sprints/sprint_3_requirements.md
docs/archive/sprints/sprint_4_plan.md
docs/archive/sprints/sprint_5_plan.md
docs/archive/sprints/sprint_5_requirements.md
docs/archive/sprints/sprint_6_plan.md
docs/archive/sprints/sprint_6_requirements.md
docs/archive/sprints/sprint_7_plan.md
docs/archive/sprints/sprint_7_requirements.md
docs/archive/sprints/sprint_7_closeout.md
docs/archive/sprints/sprint_7_review_fixes.md
docs/archive/sprints/sprint_8_plan.md
docs/archive/sprints/sprint_8_requirements.md
docs/archive/sprints/sprint_9_scope.md
docs/archive/sprints/sprint_9_ux_notes.md
docs/archive/sprints/sprint_10_scope.md
docs/archive/sprints/sprint_10_requirements.md
docs/archive/sprints/sprint_10_ux_notes.md
docs/archive/sprints/sprint_10_closeout.md
docs/archive/sprints/sprint_11_overview.md
docs/archive/sprints/sprint_11_backlog.md
docs/archive/sprints/sprint_11_user_flow.md
docs/archive/sprints/sprint_12.md
docs/archive/sprints/sprint_12_backlog.md
docs/archive/sprints/sprint_12_carry_forward.md
docs/archive/sprints/sprint_12_closeout.md
docs/archive/sprints/sprint_12_handoff.md
docs/archive/sprints/sprint_12_release_notes.md
docs/archive/sprints/sprint_13_spec.md
docs/archive/sprints/sprint_13_backlog.md
docs/archive/sprints/sprint_13_user_stories.md
docs/archive/sprints/sprint_13_handoff_start.md
docs/archive/sprints/sprint_13_closeout.md
docs/archive/sprints/backlog.md
```

Older UAT archive examples include:

```text
docs/archive/sprints/uat_sprint_2.md
docs/archive/sprints/uat_sprint_3.md
docs/archive/sprints/uat_sprint_4.md
docs/archive/sprints/uat_sprint_5.md
docs/archive/sprints/uat_sprint_6.md
docs/archive/sprints/uat_sprint_8.md
docs/archive/sprints/uat_sprint_9.md
docs/archive/sprints/uat_sprint_10.md
docs/archive/sprints/uat_sprint_11.md
docs/archive/sprints/uat_sprint_12.md
```

Archive rule:

```text
Use archive docs to understand history, not to set current product direction.
```

---

## Docs That May Need Future Cleanup

The repo has a mix of top-level sprint docs and folder-based sprint docs. Future cleanup can improve structure without deleting important context.

Potential future cleanup:

1. Move older top-level sprint 14–18 files into `docs/sprints/` or `docs/archive/sprints/` once no longer active.
2. Add README files to `docs/context/`, `docs/sprints/`, and `docs/uat/` if needed.
3. Add status headers to old docs:
   - Active
   - Supporting
   - Historical
   - Superseded
4. Create a `docs/README.md` that points to this index.
5. Keep `docs/current_platform_status.md` updated after major platform changes.

---

## Topic-Based Reading Guide

## If working on homepage, navigation, or user journeys

Read:

```text
docs/current_platform_status.md
docs/platform_information_architecture_user_journeys.md
docs/product_decisions.md
docs/context/ux_learnings.md
```

## If working on Market Pulse or company pages

Read:

```text
docs/current_platform_status.md
docs/platform_information_architecture_user_journeys.md
docs/feature_breakdown.md
docs/market_data_requirements.md
docs/compliance_disclosure_playbook.md
```

## If working on Tools, Portfolio Plan, Ticker Analysis, or Review

Read:

```text
docs/current_platform_status.md
docs/sprint_17_trade_readiness.md
docs/sprint_17_signal_date_readiness_audit.md
docs/sprint_18_readiness_gating_risk_design.md
docs/cost_assumptions_alignment.md
```

## If working on AI Helper

Read:

```text
docs/current_platform_status.md
docs/ai_helper_definition.md
docs/platform_information_architecture_user_journeys.md
docs/compliance_disclosure_playbook.md
```

## If working on data access, broker fees, research hosting, or compliance

Read:

```text
docs/current_platform_status.md
docs/compliance_disclosure_playbook.md
docs/market_data_requirements.md
docs/cost_assumptions_alignment.md
docs/source_material_reconciliation.md
```

## If working on product roadmap or monetization

Read:

```text
docs/current_platform_status.md
docs/phase_3_9_platform_strategy.md
docs/feature_breakdown.md
docs/backlog.md
docs/product_decisions.md
```

## If working on UX language or beginner experience

Read:

```text
docs/context/ux_learnings.md
docs/uat/README.md
docs/uat/uat_sprint_7.md
docs/uat/uat_sprint_13.md
docs/platform_information_architecture_user_journeys.md
```

---

## Maintenance Rule

Update this index when:

- a new major doc is added
- a doc becomes the new source of truth
- a doc is superseded
- a sprint closes
- a feature moves from future to working
- compliance/data-rights status changes
- AI Helper gains platform retrieval or web research mode

---

## Current Source-of-Truth Stack

For most future work, the current source-of-truth stack is:

```text
docs/current_platform_status.md
docs/project_knowledge_index.md
docs/platform_information_architecture_user_journeys.md
docs/product_decisions.md
docs/ai_helper_definition.md
```

Do not let older archive docs override these unless the decision is reviewed and intentionally re-adopted.
