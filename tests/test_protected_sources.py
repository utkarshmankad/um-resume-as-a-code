"""Prevent edits to protected wording while permitting harmless source rewraps."""
from pathlib import Path
import tempfile
import unittest

from scripts.validate_resume import ROOT, validate_protected_sources


class ProtectedSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "sections").mkdir()
        for name in ("competencies.tex", "summary.tex"):
            (self.root / "sections" / name).write_text((ROOT / "sections" / name).read_text())

    def edit(self, name, transform):
        path = self.root / "sections" / name
        path.write_text(transform(path.read_text()))

    def test_approved_sources_pass(self):
        validate_protected_sources(self.root)

    def test_whitespace_only_rewrap_passes(self):
        for name in ("competencies.tex", "summary.tex"):
            self.edit(name, lambda source: source.replace(" | ", " |\n   ").replace("\n", "\n\n"))
        validate_protected_sources(self.root)

    def test_skill_deletion_fails(self):
        self.edit("competencies.tex", lambda source: source.replace(" | Redis", ""))
        with self.assertRaisesRegex(ValueError, "Core Competencies changed"):
            validate_protected_sources(self.root)

    def test_wording_change_fails(self):
        self.edit("competencies.tex", lambda source: source.replace("Talent Development", "Talent Growth"))
        with self.assertRaisesRegex(ValueError, "Core Competencies changed"):
            validate_protected_sources(self.root)

    def test_reordered_skills_fail(self):
        self.edit("competencies.tex", lambda source: source.replace("Spark | Kafka", "Kafka | Spark"))
        with self.assertRaisesRegex(ValueError, "Core Competencies changed"):
            validate_protected_sources(self.root)

    def test_summary_wording_change_still_fails(self):
        self.edit("summary.tex", lambda source: source.replace("16 years", "17 years"))
        with self.assertRaisesRegex(ValueError, "summary changed"):
            validate_protected_sources(self.root)


if __name__ == "__main__":
    unittest.main()
