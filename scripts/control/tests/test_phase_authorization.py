#!/usr/bin/env python3
"""Adversarial tests for check_phase_authorization.py (H3, issue #60).

Builds a synthetic git repository with an authorization record on the base
branch, then exercises the checker across the positive case and the #60
adversarial matrix. Deterministic; network-free; scratch dirs only.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "check_phase_authorization.py"
AUTH_DIR = "docs/project-control/authorizations"


def sh(args, cwd, env=None):
    return subprocess.run(args, cwd=cwd, text=True, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def base_auth(base_sha):
    return {
        "schema_version": "1.0.0", "policy_version": "1.0.0",
        "authorization_id": "AUTH-0009", "evidence_id": "test-evidence-0009",
        "repository": "Zest-LeadGen/contractoros-california", "issue": 999,
        "base_branch": "main", "base_sha": base_sha, "lane": "Control / Infrastructure",
        "expiry": "2099-01-01", "developer_principal": "danidon-wq",
        "approver_principals": ["Zest-LeadGen"],
        "allowed_paths": [
            {"rule_id": "ALLOW-001", "pattern": "docs/notes/**", "change_kinds": ["add", "modify"]},
            {"rule_id": "ALLOW-002", "pattern": "README.md", "change_kinds": ["modify"]},
        ],
        "forbidden_paths": ["docs/notes/secret.md"],
        "required_checks": ["contractoros-control-gates"],
        "review_classes": ["owner_human_approval"],
        "owner_trigger_categories": ["NONE"],
        "classifications": {"dependency": "NONE", "build": "NONE", "release": "NONE",
                            "data": "NONE", "security": "NONE"},
        "supersession": {"supersedes": [], "revoked": False, "revocation_evidence": None},
    }


class PhaseAuthorizationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.repo = Path(self.tmp) / "repo"
        self.repo.mkdir()
        sh(["git", "init", "-q", "-b", "main", "."], self.repo)
        sh(["git", "config", "user.email", "t@example.invalid"], self.repo)
        sh(["git", "config", "user.name", "test"], self.repo)
        (self.repo / "README.md").write_text("readme\n")
        (self.repo / AUTH_DIR).mkdir(parents=True)
        sh(["git", "add", "-A"], self.repo)
        sh(["git", "commit", "-qm", "seed"], self.repo)
        seed_sha = sh(["git", "rev-parse", "HEAD"], self.repo).stdout.strip()
        (self.repo / AUTH_DIR / "AUTH-0009.json").write_text(json.dumps(base_auth(seed_sha)))
        sh(["git", "add", "-A"], self.repo)
        sh(["git", "commit", "-qm", "authorization"], self.repo)
        # simulate origin/main
        sh(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], self.repo)
        sh(["git", "checkout", "-qb", "feature"], self.repo)
        # copy the checker into the synthetic repo layout
        (self.repo / "scripts/control").mkdir(parents=True)
        shutil.copy(CHECKER, self.repo / "scripts/control/check_phase_authorization.py")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def run_checker(self, body="Phase issue: #999", today="2026-01-01"):
        event = Path(self.tmp) / "event.json"
        event.write_text(json.dumps({"pull_request": {"body": body, "base": {"ref": "main"}}}))
        env = dict(os.environ)
        env.update({"GITHUB_EVENT_PATH": str(event), "GITHUB_EVENT_NAME": "pull_request",
                    "GITHUB_BASE_REF": "main", "AUTH_TODAY": today})
        return sh([sys.executable, "scripts/control/check_phase_authorization.py"], self.repo, env)

    def commit(self, path, content="x\n", delete=False):
        p = self.repo / path
        if delete:
            sh(["git", "rm", "-q", path], self.repo)
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content)
            sh(["git", "add", path], self.repo)
        sh(["git", "commit", "-qm", f"change {path}"], self.repo)

    def test_allowed_add_passes(self):
        self.commit("docs/notes/a.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('"PASS"', r.stdout)

    def test_unmatched_path_denied(self):
        self.commit("src/evil.py")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("UNMATCHED_PATH", r.stdout)

    def test_forbidden_overrides_allow(self):
        self.commit("docs/notes/secret.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FORBIDDEN_PATH", r.stdout)

    def test_delete_requires_exact_rule(self):
        self.commit("README.md", delete=True)
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("DELETE_DENIED", r.stdout)

    def test_expired_authorization_denied(self):
        self.commit("docs/notes/a.md")
        r = self.run_checker(today="2099-06-01")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("AUTHORIZATION_EXPIRED", r.stdout)

    def test_self_modification_denied(self):
        self.commit(f"{AUTH_DIR}/AUTH-0009.json", content="{}")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("AUTHORIZATION_SELF_MODIFICATION_DENIED", r.stdout)  # documentation scope token

    def test_missing_linked_issue_denied(self):
        self.commit("docs/notes/a.md")
        r = self.run_checker(body="no issue reference here")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("NO_LINKED_ISSUE", r.stdout)

    def test_unknown_issue_denied(self):
        self.commit("docs/notes/a.md")
        r = self.run_checker(body="Phase issue: #123")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("AUTHORIZATION_RESOLUTION", r.stdout)  # documentation scope token


if __name__ == "__main__":
    unittest.main(verbosity=1)
