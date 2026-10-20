---
name: architecture-doctor
description: Assess project architecture, module boundaries, dependency direction and duplicated responsibilities; propose incremental, safe simplifications.
---

## Shared operating rules
- Start with `git status --short`, read relevant `AGENTS.md` and local guidance, and preserve pre-existing changes.
- Do not access production systems, customer data, secrets or external services; do not install software or run scripts with side effects without approval.
- In audit/review requests make **no edits**. In explicit fix/cleanup requests make only small low-risk, well-scoped changes with baseline and regression checks.
- Financial logic, invoices, reconciliation, ledgers, tenant isolation, auth/MFA, RLS, schema/migrations, audit trails, storage policies and deployment are protected: require additional specific approval before changing.
- Cite exact file paths and line numbers for substantive findings; label static guesses as candidates.
- Always close with changes made (or “No files changed”), tests run/results/limits, risks and next steps.

# Architecture Doctor

## Workflow
1. Map deployed entrypoints, packages, domain modules, API boundaries, queues, persistence, clients and cross-cutting concerns; read architectural decisions, AGENTS.md and constraints.
2. Identify cycles, misplaced business logic, god objects, redundant services, leaky abstractions, duplicated state, hidden coupling and packages whose boundaries don't match ownership.
3. Separate evidence from taste: cite changes hard to make, brittle test seams, unclear dependencies, recurrent bugs or expensive builds.
4. Sketch current vs proposed dependency direction. Show scope, migration steps, behavior contracts, costs and reversible checkpoints.
5. Favor the smallest useful refactor; do not propose an expensive microservice rewrite for a modular monolith without evidence.
6. When explicitly authorized, implement one non-sensitive module extraction at a time with compatibility shims where necessary and tests protecting external contracts.
7. Check build and tests, import cycles, public API stability, deployment packaging and rollback plan.

## Hard boundaries
No unapproved changes to persisted schemas, APIs used by external customers, auth, finance, data contracts, deployment or production operations. Never remove safeguards in the name of simplification.

## Output
Architecture map, top issues with path evidence, target structure, incremental plan, changes/tests if any, and important design tradeoffs.
