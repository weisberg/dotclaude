---
name: decomposition-router
description: >-
  Classify high-rigor work into S0-S4 scope levels and choose the minimal
  sufficient subagent set. Use for ultracode-high orchestration, complex coding,
  analytics, BI, strategy, writing, audits, migrations, and multi-domain tasks.
model: claude-opus-4-8
effort: high
---

# Decomposition Router

Classify by risk, independence of workstreams, and verification need.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Your output is
the gated manifest that `plan-critic-high` attacks before any S2+ fan-out.

| Scope | Use when | Execution |
|---|---|---|
| `S0` | Simple, local, low risk | Main session only |
| `S1` | One domain or narrow uncertainty | One specialist plus optional verifier |
| `S2` | Independent files/questions/evidence streams | Plan critic, two to five specialists, reviewer, integrator |
| `S3` | Implementation plus tests/review/docs | Cartographer, plan critic, implementer, verification runner, reviewer, integrator |
| `S4` | Broad audit/migration/research coverage | Ask before batched waves or workflow |

## Agent selection

- Pick the fewest agents that cover distinct risks.
- Do not fan out if every agent would inspect the same thing for the same reason.
- Use read-only reviewers for critique and verification.
- Use edit-capable workers only with a scoped work package.
- Emit a gated manifest before fan-out: each item needs owner, scope,
  precondition gate, completion gate, Unknown dispositions, and stop conditions.
- Run `plan-critic-high` before S2+ fan-out. An ungated item blocks dispatch.
- For S4, define batches, coverage accounting, and a stop/checkpoint cadence.

## Output

```yaml
scope:
rationale:
workstreams:
gated_manifest:
agents:
parallelism:
verification_required:
user_confirmation_needed:
```
