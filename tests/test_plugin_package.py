import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_plugin.py'
spec = importlib.util.spec_from_file_location('project_surgeon_validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PackageTests(unittest.TestCase):
    def test_plugin_structure_and_metadata(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_missing_manifest_is_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            errors = validator.validate(Path(temp))
            self.assertTrue(errors)
            self.assertIn('manifest', errors[0].lower())

    def test_finance_guard_has_read_only_language(self):
        doc = ROOT / 'plugins/project-surgeon/skills/financial-integrity-guardian/SKILL.md'
        text = doc.read_text(encoding='utf-8')
        self.assertIn('READ-ONLY', text)
        self.assertIn('No financial code changed', text)


if __name__ == '__main__':
    unittest.main()
