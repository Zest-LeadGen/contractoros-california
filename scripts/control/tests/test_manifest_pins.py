#!/usr/bin/env python3
"""Adversarial tests for check_manifest_pins.py (H6-B.1, issue #64).

Copies the checker into a synthetic tree and exercises the pin matrix:
exact versions pass; dist-tags, ranges, wildcards, OR bars, URLs, git and
file specifiers all fail; absent manifests skip. Deterministic;
network-free; scratch dirs only.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "check_manifest_pins.py"


class ManifestPinTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "scripts/control").mkdir(parents=True)
        shutil.copy(CHECKER, self.tmp / "scripts/control/check_manifest_pins.py")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def write(self, rel, deps, section="dependencies"):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps({"name": "t", "private": True, section: deps}))

    def run_checker(self):
        return subprocess.run(
            [sys.executable, "scripts/control/check_manifest_pins.py"],
            cwd=self.tmp, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def test_exact_versions_pass(self):
        self.write("apps/web/package.json", {"react": "19.2.8", "vite": "8.2.1"})
        self.write("apps/mobile/package.json", {"expo": "57.0.11", "react-native": "0.86.2"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("all exact", r.stdout)

    def test_prerelease_exact_passes(self):
        self.write("apps/web/package.json", {"lib": "1.2.3-rc.1+build.5"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_latest_dist_tag_fails(self):
        self.write("apps/mobile/package.json", {"expo": "latest"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("expo", r.stdout)

    def test_caret_range_fails(self):
        self.write("apps/web/package.json", {"react": "^19.2.8"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_tilde_range_fails(self):
        self.write("apps/web/package.json", {"react": "~19.2.8"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_wildcard_and_x_fail(self):
        self.write("apps/web/package.json", {"a": "*", "b": "1.x"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("a", r.stdout)
        self.assertIn("b", r.stdout)

    def test_comparator_and_or_fail(self):
        self.write("apps/web/package.json", {"a": ">=1.0.0", "b": "1.0.0 || 2.0.0"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_url_git_file_specifiers_fail(self):
        self.write("apps/web/package.json", {
            "a": "https://example.com/a.tgz",
            "b": "git+https://example.com/b.git",
            "c": "file:../c"})
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_devdependencies_scanned(self):
        self.write("apps/web/package.json", {"vite": "latest"}, section="devDependencies")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)

    def test_absent_manifests_skip(self):
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("SKIP", r.stdout)

    def test_unparseable_manifest_fails(self):
        p = self.tmp / "apps/web/package.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("{not json")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("unparseable", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
