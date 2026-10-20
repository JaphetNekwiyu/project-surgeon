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

## Codex development team (Tech Lead + 8 subagents)

Project Surgeon also includes the `tech-lead` coordination skill and **eight optional Codex custom agent profiles** in `plugins/project-surgeon/agents/`:

- `frontend-developer`: UI, components, accessibility
- `backend-developer`: server APIs and business logic
- `ai-ml-engineer`: AI systems and evaluations
- `data-engineer`: pipeline and data contracts
- `devops-cloud-engineer`: CI and infrastructure review (no unapproved deployment)
- `security-engineer`: independent read-only security review
- `ui-ux-designer`: design flows and usability guidance
- `qa-engineer`: independent read-only QA and regression review

The **main Codex session is the Tech Lead**; the `tech-lead` skill directs delegation. These roles are not automatically spawned on every request. Use only the specialists a task requires.

### Install subagent profiles in Windows PowerShell

After cloning the repository and installing the plugin:

```powershell
.\install-agents.ps1 -Scope User
```

For an existing installation, `git pull` first; to replace already installed profiles while saving timestamped backups:

```powershell
.\install-agents.ps1 -Scope User -Force
```

To install only in a particular project rather than globally:

```powershell
.\install-agents.ps1 -Scope Project -ProjectPath "C:\\path\\to\\your-project"
```

The installer detects collisions before any write; it **does not edit `config.toml`**, alter existing non-team agents or enable multi-agent support itself. Restart Codex afterward. Confirm that your Codex version supports custom agents and that multi-agent tools are enabled. See the [official subagents docs](https://developers.openai.com/codex/subagents).

Example prompt:

```text
Use the tech-lead skill to plan and implement this feature. Delegate frontend and backend work with disjoint file ownership, have security review the changes and QA independently verify them. Do not deploy or change protected finance/auth/database code without my specific approval.
```

Custom agent prompts guide behavior but do not grant separate sandbox permissions. All agents inherit the parent session's effective permissions. **Do not assume read-only instructions are a technical security boundary**; inspect their output and use appropriate Codex approval/sandbox settings.

## Mandatory engineering-team handoff workflow

The Tech Lead coordinates each substantial task with the **smallest useful set of specialist subagents** (usually 2–3, only when supported). Each agent owns disjoint files and must send a structured summary of what it changed, checks run, risks and whether its acceptance criteria were met.

**After every handoff, the main Tech Lead inspects the work and chooses ACCEPTED, REWORK, BLOCKED or UNVERIFIED.** Only ACCEPTED tasks can unblock dependent milestones. Independent work may continue in parallel when file ownership is separate. QA and Security give independent evidence where relevant.

Project Surgeon favors the simplest **correct and maintainable** solution: reuse existing code, prefer small local changes, extract shared helpers only when justified, and avoid premature frameworks or extra dependencies. Do not compromise correctness, security, tests or financial integrity for fewer lines.

These are instructions for Codex, **not runtime-enforced permissions or an automatic task scheduler**. If actual subagent delegation isn't available, the main Codex session follows equivalent sequential gates and reports that limitation. All protected changes still require separate authorization.

See [engineering workflow](plugins/project-surgeon/skills/tech-lead/references/engineering-workflow.md) and [Tech Lead skill](plugins/project-surgeon/skills/tech-lead/SKILL.md).
