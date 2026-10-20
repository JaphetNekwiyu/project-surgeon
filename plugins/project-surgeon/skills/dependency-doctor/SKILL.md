---
name: dependency-doctor
description: Inspect package manifests and lockfiles for unused, duplicate, conflicting and potentially vulnerable dependencies with an offline-first workflow.
---

## Shared operating rules
- Start with `git status --short`, read relevant `AGENTS.md` and local guidance, and preserve pre-existing changes.
- Do not access production systems, customer data, secrets or external services; do not install software or run scripts with side effects without approval.
- In audit/review requests make **no edits**. In explicit fix/cleanup requests make only small low-risk, well-scoped changes with baseline and regression checks.
- Financial logic, invoices, reconciliation, ledgers, tenant isolation, auth/MFA, RLS, schema/migrations, audit trails, storage policies and deployment are protected: require additional specific approval before changing.
- Cite exact file paths and line numbers for substantive findings; label static guesses as candidates.
- Always close with changes made (or “No files changed”), tests run/results/limits, risks and next steps.

# Dependency Doctor

**Default to inventory and recommendations; no package install, removal or network update without explicit approval.**

## Workflow
1. Detect all ecosystems (npm/pnpm/yarn, pip/uv/poetry, Cargo, Go, Maven, etc.), workspaces, package lockfiles, build plugins and generated code.
2. Inventory production vs development dependencies, versions, overlap, duplicated libraries, direct imports, dynamic imports, scripts, plugin registrations and transitive paths.
3. Inspect available **local** audit/SBOM tools and lockfile metadata. An outdated version does not prove a vulnerability; report advisory ID and verification source only when actually checked.
4. Distinguish confirmed removable dependencies from suspicious ones. Validate build-tool, CSS, framework and deployment-only use and peer-dependency constraints before removal.
5. For an explicitly requested low-risk fix, update one package group with an approved, reproducible, lockfile-preserving strategy. Require approval before network access, package installation or running untrusted lifecycle scripts.
6. Compare lockfile diff, size, license impacts, API compatibility and safe test/build results. Never silently perform large major-version upgrades.

## Output
Dependency inventory, suspects with evidence/confidence, conflicts, verified security advisories vs unchecked risks, proposed smallest changes, validation and unresolved ecosystem constraints.
