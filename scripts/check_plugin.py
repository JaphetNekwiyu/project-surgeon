#!/usr/bin/env python3
"""Validate Project Surgeon packaging and safe skill metadata (stdlib only)."""
import json
import re
import sys
from pathlib import Path

REQUIRED_SKILLS = (
    'project-surgeon', 'bug-hunter', 'security-guardian', 'test-engineer',
    'dead-code-detective', 'performance-engineer', 'architecture-doctor',
    'dependency-doctor', 'database-inspector', 'documentation-keeper',
    'regression-guardian', 'financial-integrity-guardian',
)
VERSION = '2.0.0'


def validate(root: Path) -> list[str]:
    errors = []
    plugin = root / 'plugins' / 'project-surgeon'
    try:
        portable = json.loads((plugin / 'plugin.json').read_text(encoding='utf-8'))
        codex = json.loads((plugin / '.codex-plugin' / 'plugin.json').read_text(encoding='utf-8'))
        marketplace = json.loads((root / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return [f'Invalid or missing manifest: {exc}']
    for label, data in [('portable', portable), ('codex', codex)]:
        if data.get('name') != 'project-surgeon':
            errors.append(f'{label} manifest name mismatch')
        if data.get('version') != VERSION:
            errors.append(f'{label} manifest version is not {VERSION}')
    if portable.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':
        errors.append('Invalid portable manifest schema')
    if codex.get('skills') != './skills/':
        errors.append('Codex manifest must expose ./skills/')
    entries = marketplace.get('plugins', [])
    if not any(e.get('name') == 'project-surgeon' and e.get('source', {}).get('path') == './plugins/project-surgeon' for e in entries):
        errors.append('Repo marketplace entry missing or misconfigured')
    skills = plugin / 'skills'
    for name in REQUIRED_SKILLS:
        path = skills / name / 'SKILL.md'
        if not path.is_file():
            errors.append(f'Missing skill: {name}')
            continue
        content = path.read_text(encoding='utf-8')
        match = re.match(r'\A---\s*\n(.*?)\n---\s*\n', content, flags=re.S)
        if not match:
            errors.append(f'Invalid frontmatter: {name}')
            continue
        metadata = match.group(1)
        if not re.search(r'^name:\s*' + re.escape(name) + r'\s*$', metadata, flags=re.M):
            errors.append(f'Skill name mismatch: {name}')
        if not re.search(r'^description:\s*\S', metadata, flags=re.M):
            errors.append(f'Missing skill description: {name}')
        if len(content) < 600:
            errors.append(f'Skill guidance too short: {name}')
    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    for error in errors:
        print('ERROR:', error, file=sys.stderr)
    if errors:
        print(f'Plugin validation failed ({len(errors)} issue(s)).', file=sys.stderr)
        return 1
    print(f'Project Surgeon {VERSION}: all {len(REQUIRED_SKILLS)} skills and manifests validated.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
