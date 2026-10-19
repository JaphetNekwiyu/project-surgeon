import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/project-surgeon/skills/project-surgeon/scripts/scan.py"
spec = importlib.util.spec_from_file_location("project_surgeon_scan", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ScannerTests(unittest.TestCase):
    def test_duplicate_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "one.py").write_text("a = 1\n")
            (p / "two.py").write_text("a = 1\n")
            result = module.scan(p)
            self.assertEqual(len(result["exact_duplicate_files"]), 1)
    def test_ignores_sensitive_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / ".env").write_text("SECRET=example")
            (p / "one.py").write_text("a = 1\n")
            self.assertEqual(module.scan(p)["source_files"], 1)
    def test_detects_large_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / "large.py").write_text("print(1)\n" * 451)
            self.assertEqual(module.scan(p)["large_file_candidates"][0]["lines"], 451)
    def test_read_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            f = p / "one.py"
            f.write_text("a = 2\n")
            before = f.read_bytes()
            module.scan(p)
            self.assertEqual(before, f.read_bytes())

if __name__ == "__main__":
    unittest.main()
