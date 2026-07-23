import subprocess
import sys
import unittest
from pathlib import Path


class ReleaseTreeTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent

    def test_tree_contains_no_private_markers(self):
        result = subprocess.run(
            [sys.executable, "scripts/validate_release_tree.py"],
            cwd=self.root,
        )
        self.assertEqual(result.returncode, 0)

    def test_public_document_set_is_small_and_exact(self):
        documents = {
            path.relative_to(self.root).as_posix()
            for path in (self.root / "docs").glob("*.md")
        }
        self.assertEqual(
            documents,
            {
                "docs/architecture-and-controls.md",
                "docs/corpus-training-evaluation.md",
                "docs/flywheel-and-extensions.md",
                "docs/limitations-and-evidence.md",
            },
        )

    def test_readme_links_each_authoritative_document_once(self):
        readme = (self.root / "README.md").read_text()
        for relative in (
            "docs/architecture-and-controls.md",
            "docs/corpus-training-evaluation.md",
            "docs/flywheel-and-extensions.md",
            "docs/limitations-and-evidence.md",
        ):
            self.assertEqual(readme.count(relative), 1)
            self.assertTrue((self.root / relative).is_file())

    def test_full_agpl_text_is_present(self):
        licence = (self.root / "LICENSE").read_text()
        self.assertIn("GNU AFFERO GENERAL PUBLIC LICENSE", licence)
        self.assertIn("Version 3, 19 November 2007", licence)
        self.assertIn("Local Model Workforce", licence)
        self.assertGreater(len(licence.splitlines()), 600)


if __name__ == "__main__":
    unittest.main()
