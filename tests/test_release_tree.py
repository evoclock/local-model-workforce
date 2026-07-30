import re
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


    def test_publication_set_uses_stable_names(self):
        publication_dir = self.root / "docs" / "publications"
        publications = {
            path.relative_to(publication_dir).as_posix()
            for path in publication_dir.rglob("*")
            if path.is_file()
        }
        self.assertIn("technical-report.html", publications)
        self.assertIn("project-brief.html", publications)
        self.assertIn("presentation.html", publications)
        self.assertFalse(any("GENERATED_V" in name for name in publications))
        self.assertFalse(any(re.search(r"(?:^|[_-])v\d+(?:[_.-]|$)", name, re.I) for name in publications))

    def test_publication_local_links_resolve(self):
        publication_dir = self.root / "docs" / "publications"
        for document in publication_dir.glob("*.html"):
            content = document.read_text(errors="replace")
            for target in re.findall(r'(?:src|href)="([^"]+)"', content):
                if target.startswith(("http://", "https://", "data:", "#", "mailto:")):
                    continue
                self.assertTrue(
                    (document.parent / target).resolve().is_file(),
                    f"missing link from {document.name}: {target}",
                )

    def test_publications_contain_no_private_versioned_filenames(self):
        for document in (self.root / "docs" / "publications").glob("*.html"):
            content = document.read_text(errors="replace")
            self.assertNotIn("GENERATED_V", content)
            self.assertNotIn("final_fifteen_pair_review_bundle", content)
            self.assertNotIn("local-assist-model", content)

    def test_diagram_sets_are_complete(self):
        diagram_dir = self.root / "docs" / "diagrams"
        expected = {
            "00_workforce_overview",
            "01_evidence_to_deployment",
            "02_architecture_and_controls",
            "03_executable_evidence_path",
            "04_evidence_flywheel",
        }
        source_stems = {
            path.stem
            for suffix in (".d2", ".py")
            for path in diagram_dir.glob(f"*{suffix}")
        }
        self.assertEqual(source_stems, expected)
        self.assertEqual(
            len(list(diagram_dir.glob("*.d2"))) + len(list(diagram_dir.glob("*.py"))),
            len(expected),
        )
        for suffix in (".svg", ".png"):
            actual = {path.stem for path in diagram_dir.glob(f"*{suffix}")}
            self.assertEqual(actual, expected)

    def test_readme_links_current_publications(self):
        readme = (self.root / "README.md").read_text()
        for relative in (
            "docs/publications/technical-report.html",
            "docs/publications/project-brief.html",
            "docs/publications/presentation.html",
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
