from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/project-surgeon'
ROLES = (
    'frontend-developer', 'backend-developer', 'ai-ml-engineer',
    'data-engineer', 'devops-cloud-engineer', 'security-engineer',
    'ui-ux-designer', 'qa-engineer',
)

class TeamWorkflowTests(unittest.TestCase):
    def test_all_eight_agents_define_handoff_and_wait(self):
        for role in ROLES:
            with self.subTest(role=role):
                content = (PLUGIN / 'agents' / (role + '.toml')).read_text(encoding='utf-8')
                self.assertIn('MANDATORY TEAM HANDOFF', content)
                self.assertIn('PASS/FAIL/SKIPPED', content)
                self.assertIn('ACCEPTED', content)
                self.assertIn('smallest correct maintainable', content)
                self.assertEqual(content.count('developer_instructions = """'), 1)
                self.assertTrue(content.rstrip().endswith('"""'))

    def test_tech_lead_blocks_unaccepted_dependents(self):
        workflow = (PLUGIN / 'skills/tech-lead/references/engineering-workflow.md').read_text(encoding='utf-8')
        for value in ('SUBMITTED', 'ACCEPTED', 'REWORK', 'BLOCKED', 'UNVERIFIED', 'simplest correct', 'MANDATORY'):
            if value != 'MANDATORY':
                self.assertIn(value, workflow)
        self.assertIn('Never advance a dependent milestone', workflow)

    def test_master_skill_uses_lead_gate(self):
        master = (PLUGIN / 'skills/project-surgeon/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Mandatory Tech Lead handoff loop', master)
        self.assertIn('Only ACCEPTED', master)

if __name__ == '__main__':
    unittest.main()
