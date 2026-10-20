# Project Surgeon 2.0 — Codex code maintenance toolkit

**Scan → Diagnose → Prioritize → Safely Repair → Verify**

Project Surgeon packages **12 Codex skills**: a master orchestrator and 11 focused specialists. It inspects large codebases for bugs, duplication, potential dead code, security, performance and architecture problems, package issues, database risk, stale docs and regressions.

**Safety-first:** audit is read-only by default. Cleanup requires an explicit request. No automatic edits to financial calculations, invoices, reconciliation, auth/MFA, RLS, tenant permissions, DB migrations, audit records or production configuration. A syntactic finding is a **candidate**, not proof that something should be deleted.

## Skills

| Skill | Purpose |
| --- | --- |
| `project-surgeon` | Coordinates complete reviews, low-risk cleanup and verification |
| `bug-hunter` | Reproduces and ranks real defects |
| `security-guardian` | Examines trust boundaries, access controls and vulnerability candidates |
| `test-engineer` | Builds focused unit/integration/regression test plans |
| `dead-code-detective` | Traces reachability before suggesting deletions |
| `performance-engineer` | Measures bottlenecks and verifies improvements |
| `architecture-doctor` | Reviews module boundaries, coupling and incremental simplifications |
| `dependency-doctor` | Evaluates package dependencies and lockfiles |
| `database-inspector` | Reviews schemas, SQL, transactions, indexes and RLS |
| `documentation-keeper` | Finds outdated docs and verifies setup instructions |
| `regression-guardian` | Checks diffs, test results, external contracts and release risk |
| `financial-integrity-guardian` | Protects monetary accuracy, immutable evidence and reconciliation invariants (especially Vlei) |

Skills are **Codex instructions**, not eleven independently running background scanners. The included Python scanner identifies exact duplicate files, repeated blocks and large-file candidates. Deeper investigations require Codex to read the project and run its own installed tools.

## Installation

### Option A: Codex marketplace (supported versions)

From a terminal:

```bash
codex plugin marketplace add JaphetNekwiyu/project-surgeon
```

Select Project Surgeon from the plugin marketplace in a supported client and install/enable it. To refresh an installed Git marketplace:

```bash
codex plugin marketplace upgrade
```

### Option B: Windows local installer

```powershell
git clone https://github.com/JaphetNekwiyu/project-surgeon.git
cd project-surgeon
.\install.ps1 -Scope User
```

If v1 is already installed:

```powershell
git pull
.\install.ps1 -Scope User -Force
```

The PowerShell installer backs up the previous plugin and marketplace catalog before replacing them. Restart your Codex/ChatGPT desktop client after installation. Windows installer operation should be checked on your own PC; CI does not execute PowerShell installation.

For development inside this repository, use its `.agents/plugins/marketplace.json` as a local marketplace source.

## Use

**Full review (read-only):**

```text
Use project-surgeon in full-surgeon mode. Review every applicable workstream in my repository and give a ranked report with file:line evidence, missing tests and changes worth making. Do not edit any files.
```

**Safe cleanup:**

```text
Use project-surgeon in cleanup mode. Review the whole repository, then fix only proven low-risk duplication or dead code, with tests after each change. Never change financial, authentication, RLS or migration logic. Report every file changed.
```

**Vlei financial integrity audit (read-only):**

```text
Use financial-integrity-guardian to audit Vlei Business invoice totals, bank evidence, reconciliation idempotency, reversals, tenant RLS and audit events. Use synthetic local tests and do not change protected code.
```

## Read-only scanner

Python 3, standard library only:

```bash
python plugins/project-surgeon/skills/project-surgeon/scripts/scan.py --repo . --format markdown
```

JSON output: `--format json`. If running from a different project, use the absolute path to the installed plugin's `skills/project-surgeon/scripts/scan.py`.

This scan does **not** determine unused imports, confirm defects, prove security, or measure runtime performance. It never deletes source files.

## Test and maintain the plugin

```bash
python scripts/check_plugin.py
python -m unittest discover -s tests -v
```

GitHub Actions runs these checks on each push/PR. All workflows should remain offline and read-only. A passing plugin test confirms package structure/scanner behavior, **not** the correctness of any target project.

## Safety & limitations

- Never assume zero references means dead code: consider dynamic routes, import registries and external consumers.
- Never execute database migrations, contact production, read secret contents, install dependencies or force-push as part of an ordinary cleanup.
- Preserve user worktrees and compare baseline test results. Fixes are reversible, scoped and individually verified.
- Protected finance, auth, database and compliance code requires its own explicit approval and stronger test plan.
- Report `GO`, `NO-GO` or `UNVERIFIED` based on evidence, not optimism.

See `plugins/project-surgeon/skills/project-surgeon/SKILL.md` for the complete orchestration workflow.

**License:** MIT.
