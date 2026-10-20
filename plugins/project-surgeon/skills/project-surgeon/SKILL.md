---
name: project-surgeon
description: Orchestrate a complete, safety-first codebase audit and small verified cleanup across bugs, security, tests, duplication, performance, architecture, dependencies, database, documentation, regression and financial integrity.
---

# Project Surgeon 2.0 — Master Orchestrator

**Objective:** diagnose, prioritize, safely repair, and verify. This plugin is a collection of focused Codex skills, not a background auto-fix daemon. Never equate removing code with improving quality.

## Modes
- **audit** (default): comprehensive read-only review, nothing changed.
- **cleanup**: perform read-only review, then make narrowly scoped, low-risk fixes with evidence and verification.
- **review**: findings and test gaps only.
- **duplicates**: identify exact and semantic duplication candidates.
- **performance**: measure first, optimize only with a reproducible baseline.
- **full-surgeon**: coordinate all specialists, merging their findings into one ranked report. Read-only unless the user separately requests fixes.
- **vlei-safety**: perform protected-finance read-only audit and report integrity gaps without changing money-handling logic.

If the request is ambiguous, use audit mode.

## Use specialist skills
Read the corresponding `SKILL.md` under `../<skill-name>/` for detailed methods. Subskills are independently invokable; do not assume their mere existence means checks were executed.

| Workstream | Specialist |
| --- | --- |
| Reproducible defects | `bug-hunter` |
| Threat model, access and validation | `security-guardian` |
| Coverage and regression test authoring | `test-engineer` |
| Duplicated and potentially unused code | `dead-code-detective` |
| Measured latency and resource use | `performance-engineer` |
| Modularity and dependency boundaries | `architecture-doctor` |
| Package and lockfile health | `dependency-doctor` |
| Schema, SQL, RLS and transactions | `database-inspector` |
| Documentation drift | `documentation-keeper` |
| Review of a change against baseline | `regression-guardian` |
| Exact money and immutable evidence | `financial-integrity-guardian` |

Use all applicable specialists in `full-surgeon`. For a pure frontend project, mark database/finance workstreams not applicable instead of inventing findings. Read-only investigation can be parallelized when subagents are available; editing is strictly sequential, and only one writer touches any file.

## Mandatory Tech Lead handoff loop

When implementing significant cleanup or improvements, first load the `tech-lead` skill and `tech-lead/references/engineering-workflow.md`. Break multi-module or multi-checkpoint tasks into independently verifiable subtasks; when actual subagent tools are available, delegate at least one appropriate specialist and use QA/security reviewers as warranted. Do not claim delegated execution if the environment does not support it.

After each specialist returns, the primary Tech Lead reviews its exact diff, simplicity, scope, test evidence, acceptance criteria and protected boundaries. Mark ACCEPTED / REWORK / BLOCKED / UNVERIFIED. **Only ACCEPTED unblocks dependent tasks.** Rework failing tasks rather than rushing ahead, and do not silently omit uncompleted work. Independent tasks with disjoint file ownership may continue. Prefer reuse and the simplest correct implementation to new abstractions or dependencies; never sacrifice safety or tests for fewer lines.

## Shared preparation
1. Read relevant `AGENTS.md`, project docs, scripts, dependency manifests, deployment boundaries and current architecture.
2. Run `git status --short`; preserve every pre-existing edit. If the worktree is dirty, remain in audit mode unless an isolated edit scope is explicitly approved.
3. Inventory routes, shared packages, business logic, background jobs, APIs, persistence, tests, dynamic entrypoints and generated code.
4. Establish baseline: run only **safe** local lint, typecheck, test, build and profiling commands. Inspect scripts for side effects first. Record existing failures and skips.
5. Run the bundled read-only source scanner, using the resolved path of `scripts/scan.py` adjacent to this skill:
   `python <skill-directory>/scripts/scan.py --repo . --format markdown`
   JSON format is supported. The scanner finds syntax-based **candidates** only, not proof of unused code or security.
6. Build a coverage ledger: packages investigated, tests actually run, skipped/unavailable checks, and dynamic/plugin/external consumers still uncertain.

## Evidence-driven review
- For suspected bugs, require a safe reproduction or failing test.
- For dead code, trace indirect, dynamic, framework and external use before removing it.
- For duplication, verify identical responsibilities and behavior, not only matching syntax.
- For performance, measure representative workload before and after any change; do not claim improvement without data.
- For dependency security, distinguish unchecked advisories from verified ones.
- For architecture, propose incremental steps with explicit contract protection.
- For docs, compare instructions to actual code; do not invent features.
- For financial systems, check monetary exactness, immutable source records, reversals, reconciliation idempotency, concurrency, approval gates, auditability and tenant isolation.

## Protected boundaries: stop and request separate scoped approval
Never automatically modify or delete: invoice/payment/ledger/tax/reconciliation calculations; bank evidence; issued financial documents; RLS, tenancy, access controls and authentication/MFA; encryption, rate limiting, security checks or audit logs; migrations, database schema and storage policies; background financial jobs; production secrets, deployment, or legal/compliance evidence. Do not connect to live databases or services, print secrets, run destructive commands, force push, install dependencies or deploy during a routine cleanup.

**Vlei-specific:** protect existing staged and production Supabase connections; no migration, live import, data repair, release or financial feature-gate changes as part of housekeeping. Synthetic local tests only.

## Approved cleanup
1. Rank every finding by impact, confidence, scope and risk; separate confirmed from hypothetical.
2. Choose the smallest non-sensitive fix that preserves all externally observable behavior.
3. Add targeted regression tests where appropriate, apply one isolated change, and run tests before the next.
4. Compare with baseline; check `git diff --check` and inspect exact diff for unintended modifications.
5. If verification regresses, stop and report; never rewrite tests to hide failures, reset user changes or assert success without passing evidence.
6. Use `regression-guardian` as the final release gate. Report NO-GO if protected changes lack approval or tests fail.

## Required final report
Summarize:
- Project scope and audit coverage (including not-inspected code)
- Ranked findings: severity, confidence, file:line and supporting evidence
- Candidate vs confirmed defects, unused code and performance issues
- Files modified/deleted (or exactly “No files changed”)
- Before/after tests, lint/typecheck/build/benchmarks with pass/fail/skip
- Protected areas not touched, risk, rollback and outstanding work
- Final disposition: **GO**, **NO-GO**, or **UNVERIFIED** based on checks actually performed

See `references/safety.md` and `references/review-checklist.md`; subskills inherit these rules.
