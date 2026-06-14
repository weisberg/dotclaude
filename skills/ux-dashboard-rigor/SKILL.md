---
name: ux-dashboard-rigor
description: >-
  Enterprise dashboard and operational UI review discipline for information
  hierarchy, first-screen answers, accessibility, scanning, filters, drill paths,
  annotations, alerts, and misread risks.
model: claude-opus-4-8
effort: high
---

# UX Dashboard Rigor

Operational users need fast, repeatable comprehension.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. UX/dashboard
findings are judgment gates, so make evidence and decision impact explicit.

## Checks

- First screen answers the primary decision.
- KPI hierarchy separates outcome, drivers, and guardrails.
- Filters have safe defaults and visible state.
- Drill paths match how users investigate problems.
- Units, time windows, definitions, and freshness are visible.
- Colors encode meaning consistently and accessibly.
- Tables support scanning, sorting, comparison, and exception-finding.
- Alerts and annotations reduce ambiguity, not noise.
- The design prevents common misreads of totals, rates, cohorts, and partial data.

Prefer dense, calm, work-focused UI for SaaS, BI, and operations tools.
