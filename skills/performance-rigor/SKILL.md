---
name: performance-rigor
description: >-
  Performance review discipline for algorithms, database queries, rendering,
  network behavior, caching, concurrency, memory, benchmarks, and scalability
  risks in code, data, and frontend work.
model: claude-opus-4-8
effort: high
---

# Performance Rigor

Identify the bottleneck before optimizing.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Performance
claims should become measurements or clearly labeled hypotheses.

## Checks

- Complexity and input-size assumptions.
- Database indexes, partitions, predicate pushdown, join order, and cross joins.
- Network waterfalls, payload size, caching, retries, and timeouts.
- Frontend rendering, re-render frequency, virtualization, layout shifts.
- Concurrency, locks, queues, backpressure, and resource cleanup.
- Memory growth, streaming vs buffering, and large-file behavior.
- Benchmark or profiling evidence where feasible.
- Before/after comparison for changes intended to improve performance.

Do not trade correctness, security, or maintainability for unmeasured speed.
