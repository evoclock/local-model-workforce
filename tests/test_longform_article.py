import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path


class ArticleParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.details = 0
        self.images = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "details":
            self.details += 1
        elif tag == "img":
            self.images.append(attributes)
        elif tag == "a":
            self.links.append(attributes.get("href", ""))


class LongformArticleTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parent.parent
        self.output = (
            self.root
            / "docs"
            / "articles"
            / "local-multi-model-workforce.html"
        )
        self.landing = self.root / "docs" / "index.html"

    def test_generator_reproduces_self_contained_article(self):
        result = subprocess.run(
            [sys.executable, "scripts/build_longform_article.py", "--check"],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.output.is_file())
        self.assertTrue(self.landing.is_file())

        parser = ArticleParser()
        article = self.output.read_text()
        parser.feed(article)

        self.assertGreaterEqual(parser.details, 8)
        self.assertEqual(len(parser.images), 9)
        self.assertEqual(
            len({image.get("src", "") for image in parser.images}),
            8,
        )
        self.assertTrue(
            all(image.get("src", "").startswith("data:image/") for image in parser.images)
        )
        self.assertTrue(all(image.get("alt", "").strip() for image in parser.images))
        self.assertTrue(all(link for link in parser.links))

        landing = self.landing.read_text()
        self.assertIn(
            'content="0; url=articles/local-multi-model-workforce.html"',
            landing,
        )
        self.assertIn(
            'content="https://evoclock.github.io/local-model-workforce/"',
            landing,
        )
        self.assertIn('property="og:image"', landing)

    def test_article_preserves_approved_claim_boundaries(self):
        article = self.output.read_text()
        normalised = " ".join(article.split())
        required = (
            "task-bound",
            "29 June 2026",
            "30 June 2026",
            "The timing was coincidental",
            "does not establish that the files improve task success",
            "did not generally improve task success",
            "fine-tuned Qwen3.5-4B model, this instruction bundle, and this evaluation",
            "larger or more capable model might manage the additional context better",
            "founder of SID",
            "constant supervision for alleged automated tasks",
            "20,574 real coding agent sessions from 1,639 repositories",
            "38.33% involved a developer-constraint violation",
            "91.49% required explicit developer correction",
            "Every individually beneficial rule in their analysis was a negative constraint",
            "The diagram may look a little intimidating",
            "86-task heldout test set",
            "additional realistic capability testing",
            "MCP server functionality",
            "new fine-tune version",
            "the gaps I identified",
            "The screenshot, I hope, communicates the product shape",
            "before the pattern was even part of the current discourse",
            "None of this work was derived from my current role",
            "I conceived and developed it independently through my own efforts",
            "opportunities they stand to gain from this type of framework",
            "internal roles starting to appear within the next six to twelve months",
            "I fully expect large siloed organisations will continue",
            "regardless of size, are used to thinking like lean operators",
            "Finally, I hope you realise that the products described here",
            "long before it has had the chance to become a common industry theme",
            "models show a stronger tendency to add unrequested scope",
            "Scope creep should not be something that users tolerate",
            "you are not using our tool right",
            "convergence toward the same type of solution",
            "privately developed, clean-room Bayesian stochastic block model engine",
            "I am now looking for an opportunity to develop this capability",
        )
        for phrase in required:
            self.assertIn(phrase, normalised)

        rejected = (
            "Graph-Tool",
            "View the presentation",
            "bounded implementation",
            "consumer-neutral",
            "production-complete system",
            "Jeff Wang",
            "15 paired HumanEval+ runs",
            "loss-producing task types",
            "the gaps we identified",
            "\u2014",
            "load-bearing",
            "the tell is",
        )
        for phrase in rejected:
            self.assertNotIn(phrase, normalised)

        self.assertLess(
            normalised.index("Pengz"),
            normalised.index("John Myles White"),
        )
        self.assertIn('class="detail-body practitioner-grid"', article)
        self.assertIn('class="evidence-stack"', article)

    def test_article_uses_stable_unversioned_name(self):
        self.assertEqual(self.output.name, "local-multi-model-workforce.html")
        self.assertIsNone(re.search(r"(?:^|[_-])v\d+(?:[_.-]|$)", self.output.name, re.I))


if __name__ == "__main__":
    unittest.main()
