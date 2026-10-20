---
name: bug-hunter
description: Find reproducible bugs, crashes, incorrect state transitions and broken edge cases across an existing project; investigate or safely fix them with regression tests.
---

## Shared operating rules
- Start with `git status --short`, read relevant `AGENTS.md` and local guidance, and preserve pre-existing changes.
- Do not access production systems, customer data, secrets or external services; do not install software or run scripts with side effects without approval.
- In audit/review requests make **no edits**. In explicit fix/cleanup requests make only small low-risk, well-scoped changes with baseline and regression checks.
- Financial logic, invoices, reconciliation, ledgers, tenant isolation, auth/MFA, RLS, schema/migrations, audit trails, storage policies and deployment are protected: require additional specific approval before changing.
- Cite exact file paths and line numbers for substantive findings; label static guesses as candidates.
- Always close with changes made (or “No files changed”), tests run/results/limits, risks and next steps.

# Bug Hunter

**Goal:** turn suspected defects into reproducible, ranked findings, then repair only verified low-risk defects when expressly asked.

## Workflow
1. Inventory routes, entry points, services, workers, tests, and error handling. Examine build or runtime failures and existing issue evidence first.
2. Establish baseline checks without production access; preserve pre-existing failures. Review `git status --short`.
3. Trace inputs through parsing → validation → business logic → persistence → response. Inspect null/undefined values, stale state, asynchronous races, error handling, boundary arithmetic, timezone transitions, pagination and retries.
4. For every candidate, create a **minimal reproduction** or a test scenario with observed and expected behavior. Distinguish probable bugs from confirmed defects.
5. Estimate user impact, reachability, confidence and blast radius. Prioritize data loss, security and crashes over style.
6. In an explicitly requested fix session, patch one proven low-risk defect at a time, add a regression test that failed before the fix, and check the entire affected call chain.
7. Run targeted tests, typecheck, lint and other safe available gates; record skips and limitations.

## Rules
- Do not modify financial calculations, reconciliation, auth, tenant separation, RLS, database migrations, storage policies or other protected logic without separate scoped approval.
- Never change production data, run destructive tests, remove error handling, or modify assertions merely to obtain a green run.
- Report reproduction steps and exact path/line evidence, not unsupported claims.

## Output
A severity-ranked defect table: location, reproduction, expected/actual result, impact, confidence, fix status, tests run and unresolved risk.
