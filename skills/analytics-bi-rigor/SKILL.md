---
name: analytics-bi-rigor
description: >-
  Metric, SQL, dbt, dashboard, semantic-layer, and BI validation discipline for
  high-stakes analytics work. Use for grain, joins, nulls, filters, freshness,
  lineage, reconciliation, dashboard semantics, and decision relevance checks.
model: claude-opus-4-8
effort: high
---

# Analytics BI Rigor

Do not treat a number as a result until its definition, grain, and evidence are
clear.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your checks
feed `data-bi-reviewer-high`, `verification-runner-high`, and the final report.

## Required checks

- Metric contract: name, owner, purpose, formula, numerator, denominator, grain,
  time window, dimensionality.
- Filters and exclusions: status, deleted/test data, geography, cohorts, privacy.
- Time logic: timezone, fiscal calendar, inclusive/exclusive boundaries, lag.
- Join safety: keys, duplicates, many-to-many risks, fanout, missing keys.
- Null and zero behavior: denominator zero, null categories, missing facts.
- Freshness: update cadence, latest partition, late-arriving data.
- Reconciliation: compare to trusted reports, source systems, or prior totals.
- Lineage: upstream sources, transforms, downstream dashboards.
- BI semantics: dashboard filters, drill paths, totals, row-level security.
- Decision relevance: what business decision the analysis supports.

Final analytics outputs must include what not to conclude.
