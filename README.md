# Project Surgeon — Codex cleanup plugin

A reusable **audit → evidence → safe refactor → verification** workflow. Find duplicate code, investigate dead code, simplify structure, and optimize measured bottlenecks. It never blindly deletes files.

## Installation on Windows

Clone or download this repository, open PowerShell in its root, then run:

```powershell
.\install.ps1 -Scope User
```

Restart Codex and enable the local plugin if needed. Alternative: copy `plugins/project-surgeon/skills/project-surgeon` to `$HOME\.codex\skills\project-surgeon` and restart Codex.

## Use in Codex

```text
Use the project-surgeon skill in audit mode to inspect this entire repository.
Report repeated logic, unnecessary code and performance opportunities. Do not edit files.
```

For low-risk corrections only, on a clean Git worktree:

```text
Use project-surgeon in cleanup mode. Make small, verified low-risk improvements.
Preserve behavior and leave finance, authentication and migrations untouched.
```

## Scanner

```bash
python plugins/project-surgeon/skills/project-surgeon/scripts/scan.py --repo . --format markdown
```

Use `--format json` for machine-readable findings. Python 3, no third-party packages. Reports are read-only and contain **candidates**, not proof of unused code or runtime improvements. Codex must trace dependencies and run project-specific tests.

## Tests

```bash
python -m unittest discover -s tests -v
```

Includes plugin manifests, skill, safety checklist, read-only scanner, Windows installer, unit tests and GitHub Actions checks. MIT license.

**Safety:** No unapproved edits to payments, invoices, balances, reconciliation, authentication, RLS, migrations, deployment or production data.

This is an on-demand Codex plugin, not a continuously running background service.
