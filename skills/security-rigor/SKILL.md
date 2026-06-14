---
name: security-rigor
description: >-
  Security review discipline for auth, authorization, injection, secrets,
  permissions, dependency, supply-chain, privacy, logging, and data exposure
  risks in high-rigor code and architecture work.
model: claude-opus-4-8
effort: high
---

# Security Rigor

Review the change as an attacker and as an operator responsible for recovery.

## Fleet context

This skill is part of `ultracode-high`. For the full orchestration map, tool
catalog, agent roster, and card schemas, read
`../ultracode-high/references/runtime-context.md` when available. Security
findings must be concrete enough for the final integrator to block, fix, or
accept explicitly as risk.

## Checks

- Authn/authz boundaries and privilege changes.
- Injection, deserialization, path traversal, SSRF, XSS, CSRF, and command risks.
- Secrets in code, logs, config, tests, docs, and generated artifacts.
- PII handling, retention, masking, aggregation thresholds, and access controls.
- Dependency and supply-chain exposure.
- Error handling and logging that could leak sensitive data.
- Backward compatibility of permissions and migrations.
- Tests or manual checks that demonstrate the risk is controlled.

Escalate production-affecting or sensitive-data operations for explicit approval.
