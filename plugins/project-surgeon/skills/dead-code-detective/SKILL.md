---
name: dead-code-detective
description: Investigate allegedly unused functions, modules, exports and dependencies; prove reachability before suggesting safe removal.
---

## Shared operating rules
- Start with `git status --short`, read relevant `AGENTS.md` and local guidance, and preserve pre-existing changes.
- Do not access production systems, customer data, secrets or external services; do not install software or run scripts with side effects without approval.
- In audit/review requests make **no edits**. In explicit fix/cleanup requests make only small low-risk, well-scoped changes with baseline and regression checks.
- Financial logic, invoices, reconciliation, ledgers, tenant isolation, auth/MFA, RLS, schema/migrations, audit trails, storage policies and deployment are protected: require additional specific approval before changing.
- Cite exact file paths and line numbers for substantive findings; label static guesses as candidates.
- Always close with changes made (or “No files changed”), tests run/results/limits, risks and next steps.

# Dead Code Detective

**Default: investigate first; delete only with proof and explicit cleanup intent.**

## Workflow
1. Enumerate source, routes, public APIs, config, scripts, migrations, asset manifests, tests, package exports and background jobs. Capture `git status --short`.
2. Run the bundled Project Surgeon scanner for duplicate-file candidates; use installed language analyzers (compiler unused warnings, coverage, dependency graphs) when safe.
3. Trace each candidate through direct and indirect imports, reflection, string-based lookups, dynamic imports, framework conventions, plugin registration, CLI scripts, bundler configuration, side effects and external consumers.
4. Mark candidates **confirmed removable**, **likely unused** or **cannot prove unused**. Require concrete reference evidence for the first category, not only zero text matches.
5. Never delete databases, historical migrations, event records, legal evidence, fixtures required by downstream tooling or config based only on static scans.
6. For explicitly authorized low-risk changes, remove one self-contained proven-unused item at a time, run checks and inspect the diff. When in doubt, report rather than delete.

## Output
An inventory of candidates: path/export, evidence, reachability assumptions, removal confidence, potential impact, action taken and verification. Distinguish saved code from merely moved code.
