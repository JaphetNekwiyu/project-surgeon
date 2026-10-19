---
name: project-surgeon
description: Audit full repositories for duplicate code, unused modules, architecture issues, quality risks and measurable performance opportunities. Safely implement verified cleanup.
---

# Project Surgeon

Audit → evidence → small safe refactor → verify. Never confuse shorter code with faster or safer code.

## Modes
- **audit** (default): read-only investigation; no modifications.
- **cleanup**: audit then small, low-risk code changes, with regression checks.
- **duplicates**: identify repeated components, helpers and code.
- **review**: report correctness, security, architecture and quality findings.
- **performance**: measure actual bottlenecks before recommending improvements.

If unclear, choose audit. An explicit request to clean authorizes only low-risk source edits, NOT production-sensitive changes.

## Before touching code
1. Read AGENTS.md and relevant project docs. Inventory framework, packages, entrypoints, route definitions, background jobs, tests, deployment targets, APIs, database schemas and integrations.
2. Run git status --short. Never discard, reset, clean, rebase or overwrite user edits. On dirty worktrees use audit mode unless specific, isolated modifications are approved.
3. Establish safe test/typecheck/lint/build baselines. Inspect scripts for production side effects before running.
4. Do not read secrets, print credentials, connect to production, install packages, change remote settings, deploy, or run destructive migrations.

## Discovery
Run the bundled scanner (Python 3, stdlib only):
```bash
python plugins/project-surgeon/skills/project-surgeon/scripts/scan.py --repo . --format markdown
```
Or locate the installed skill directory if running outside the plugin repository. JSON output: --format json. Scanner output contains **candidates**, never proof of dead code.

Review all application packages, including dynamically loaded modules, config files, entrypoints, migrations, registries, public APIs and tests. In large repositories, cover all packages while prioritizing hotspots; don't claim every line was manually inspected without evidence.

Investigate:
1. Repeated code: equivalent business logic, React components, hooks, API clients, queries, validation and calculations.
2. Unused code: use local search, dependency graphs and available installed linters or dead-code checkers; check reflection, dynamic imports, scripts, framework conventions and downstream dependencies before removal.
3. Design problems: circular deps, overly complex conditionals, misleading naming, large modules, unnecessary abstractions and duplicate configuration.
4. Reliability and security: weak validation, broken authorization, races, exceptions, leakage, missing idempotency and insufficient tests.
5. Performance: N+1 queries, unnecessary renders, repeated I/O, bundle bloat, inefficient loops, missing pagination. Gather benchmark/profiling evidence before promising gains.

Read references/safety.md and references/review-checklist.md.

## Protected code: NEVER change automatically
Treat invoices, monetary calculations, ledgers, reconciliation, payments, taxation, tenant isolation, auth/MFA, access controls, RLS, rate limits, audit logs, event streams, migrations, schemas, storage policies, production config, background schedules, secrets, legal/regulatory evidence and integrations as protected. Require separate explicit, scoped approval before editing. Never delete migrations that appear obsolete. In Vlei projects preserve immutable records and financial evidence.

## Safe cleanup
- Rank findings by severity, confidence, path:line evidence, benefit and behavioral risk.
- Change one low-risk, clearly understood component at a time. Do not change observable behavior, APIs, accessibility, error semantics or logs.
- Before removing code, prove no dynamic/runtime/external dependency exists.
- Run targeted checks after each change, then safe full verification. Compare to baseline and inspect git diff --check.
- If tests regress, stop. Never discard other people's work or rewrite tests to hide failures.
- Don't claim total cleanup or guaranteed performance increases.

## Report
- Coverage and limitations.
- Ranked findings with exact file/line and evidence; distinguish *candidate* from *proven*.
- Changes and any deletions (or state "No files changed").
- Verification: test/lint/typecheck/build/benchmark pass/fail/skip details.
- Remaining uncertainty and protected areas.

If subagents are available, parallelize **read-only** investigation. Never let multiple writers edit the same file.
