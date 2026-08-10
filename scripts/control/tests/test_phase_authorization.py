#!/usr/bin/env python3
"""Adversarial tests for check_phase_authorization.py (H3 #60, H5-D #118).

Builds a synthetic git repository with an authorization record on the base
branch, then exercises the checker across the positive cases and the
adversarial matrix: the original #60 rules plus the H5-D bootstrap,
supersession-closure, and exact-path relocation extensions. Deterministic;
network-free; scratch dirs only.
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
PA_DIR = "docs/project-control/authorizations"
MOVABLE = "docs/movable/src.md"


def sh(args, cwd, env=None):
    return subprocess.run(args, cwd=cwd, text=True, env=env,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def base_permit(base_sha):
    return {
        "schema_version": "1.0.0", "policy_version": "1.0.0",
        "authorization_id": "PA-0009", "evidence_id": "test-evidence-0009",
        "repository": "Zest-LeadGen/contractoros-california", "issue": 999,
        "base_branch": "main", "base_sha": base_sha, "lane": "Control / Infrastructure",
        "expiry": "2099-01-01", "developer_principal": "danidon-wq",
        "approver_principals": ["Zest-LeadGen"],
        "allowed_paths": [
            {"rule_id": "ALLOW-001", "pattern": "docs/notes/**", "change_kinds": ["add", "modify"]},
            {"rule_id": "ALLOW-002", "pattern": "README.md", "change_kinds": ["modify"]},
            {"rule_id": "ALLOW-003", "pattern": MOVABLE, "to": "docs/notes/moved.md",
             "change_kinds": ["relocate"]},
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
        movable = self.repo / MOVABLE
        movable.parent.mkdir(parents=True)
        movable.write_text("".join(f"movable content line {i}\n" for i in range(20)))
        (self.repo / PA_DIR).mkdir(parents=True)
        sh(["git", "add", "-A"], self.repo)
        sh(["git", "commit", "-qm", "seed"], self.repo)
        self.seed_sha = sh(["git", "rev-parse", "HEAD"], self.repo).stdout.strip()
        (self.repo / PA_DIR / "PA-0009.json").write_text(json.dumps(base_permit(self.seed_sha)))
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

    def run_checker(self, body="Phase issue: #999", today="2026-01-01", repo_env=None):
        event = Path(self.tmp) / "event.json"
        event.write_text(json.dumps({"pull_request": {"body": body, "base": {"ref": "main"}}}))
        env = dict(os.environ)
        env.pop("GITHUB_REPOSITORY", None)
        env.update({"GITHUB_EVENT_PATH": str(event), "GITHUB_EVENT_NAME": "pull_request",
                    "GITHUB_BASE_REF": "main", "PA_TODAY": today})
        if repo_env is not None:
            env["GITHUB_REPOSITORY"] = repo_env
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

    def move(self, old, new, edit_line=None):
        dest = self.repo / new
        dest.parent.mkdir(parents=True, exist_ok=True)
        sh(["git", "mv", old, new], self.repo)
        if edit_line is not None:
            lines = dest.read_text().splitlines(keepends=True)
            lines[0] = edit_line
            dest.write_text("".join(lines))
            sh(["git", "add", new], self.repo)
        sh(["git", "commit", "-qm", f"move {old} -> {new}"], self.repo)

    def new_record(self, rec_id, issue, allowed, supersedes=(), evidence=None,
                   filename=None, revoked=False):
        r = base_permit(self.seed_sha)
        r["authorization_id"] = rec_id
        r["issue"] = issue
        r["evidence_id"] = evidence if evidence is not None else f"issue-{issue}-comment-424242"
        r["allowed_paths"] = allowed
        r["supersession"] = {"supersedes": list(supersedes), "revoked": revoked,
                             "revocation_evidence": None}
        self.commit(f"{PA_DIR}/{filename or rec_id + '.json'}", json.dumps(r))
        return r

    def close_base_record(self, evidence, extra=None):
        rec = base_permit(self.seed_sha)
        rec["supersession"] = {"supersedes": [], "revoked": True,
                               "revocation_evidence": evidence}
        if extra:
            rec.update(extra)
        self.commit(f"{PA_DIR}/PA-0009.json", json.dumps(rec))

    # ---- H3 base-mode matrix (#60) ----

    def test_allowed_add_passes(self):
        self.commit("docs/notes/a.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('"PASS"', r.stdout)
        self.assertIn('"base"', r.stdout)

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
        self.commit(f"{PA_DIR}/PA-0009.json", content="{}")
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

    def test_authorization_delete_denied(self):
        self.commit(f"{PA_DIR}/PA-0009.json", delete=True)
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("AUTHORIZATION_DELETE_DENIED", r.stdout)

    def test_base_mode_pa_add_for_other_issue_denied(self):
        self.new_record("PA-0110", 777, [
            {"rule_id": "ALLOW-001", "pattern": f"{PA_DIR}/PA-0110.json", "change_kinds": ["add"]},
        ])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("AUTHORIZATION_SELF_MODIFICATION_DENIED", r.stdout)

    # ---- H5-D relocation matrix ----

    def test_relocate_exact_passes(self):
        self.move(MOVABLE, "docs/notes/moved.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('"PASS"', r.stdout)

    def test_relocate_unauthorized_denied(self):
        self.move("README.md", "docs/notes/readme.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("RELOCATE_DENIED", r.stdout)

    def test_relocate_wrong_target_denied(self):
        self.move(MOVABLE, "docs/notes/other.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("RELOCATE_DENIED", r.stdout)

    def test_relocate_content_drift_denied(self):
        self.move(MOVABLE, "docs/notes/moved.md", edit_line="tampered first line\n")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("RELOCATE_CONTENT_DRIFT_DENIED", r.stdout)

    # ---- H5-D bootstrap matrix ----

    def bootstrap_allowed(self, rec_id="PA-0110", closure=True):
        rules = [
            {"rule_id": "ALLOW-001", "pattern": f"{PA_DIR}/{rec_id}.json", "change_kinds": ["add"]},
            {"rule_id": "ALLOW-002", "pattern": "docs/notes/**", "change_kinds": ["add", "modify"]},
        ]
        if closure:
            rules.append({"rule_id": "ALLOW-003", "pattern": f"{PA_DIR}/PA-0009.json",
                          "change_kinds": ["modify"]})
        return rules

    def test_bootstrap_new_issue_passes(self):
        self.new_record("PA-0110", 998, [
            {"rule_id": "ALLOW-001", "pattern": f"{PA_DIR}/PA-0110.json", "change_kinds": ["add"]},
            {"rule_id": "ALLOW-002", "pattern": "docs/notes/**", "change_kinds": ["add", "modify"]},
        ])
        self.commit("docs/notes/a.md")
        r = self.run_checker(body="Phase issue: #998")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('"bootstrap"', r.stdout)

    def test_bootstrap_with_closure_passes(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        self.commit("docs/notes/a.md")
        r = self.run_checker()
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn('"bootstrap"', r.stdout)
        self.assertIn("PA-0009", r.stdout)

    def test_bootstrap_requires_closure(self):
        self.new_record("PA-0110", 999, self.bootstrap_allowed(closure=False),
                        supersedes=["PA-0009"])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("BOOTSTRAP_CLOSURE_REQUIRED", r.stdout)

    def test_bootstrap_supersedes_listing_required(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=[])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("SUPERSEDES_MISSING", r.stdout)

    def test_closure_extra_edit_denied(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242",
                               extra={"expiry": "2100-01-01"})
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("CLOSURE_CONTENT_MISMATCH", r.stdout)

    def test_closure_evidence_must_name_superseder(self):
        self.close_base_record("revoked for reasons")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("CLOSURE_EVIDENCE_INVALID", r.stdout)

    def test_bootstrap_evidence_format_denied(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"],
                        evidence="off-platform-note")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("BOOTSTRAP_EVIDENCE_FORMAT", r.stdout)

    def test_bootstrap_two_records_denied(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        self.new_record("PA-0111", 999, self.bootstrap_allowed("PA-0111"), supersedes=["PA-0009"])
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("BOOTSTRAP_MULTIPLE_RECORDS", r.stdout)

    def test_bootstrap_filename_mismatch_denied(self):
        self.close_base_record("superseded-by:PA-0111 issue-999-comment-424242")
        self.new_record("PA-0111", 999, self.bootstrap_allowed("PA-0110"),
                        supersedes=["PA-0009"], filename="PA-0110.json")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("BOOTSTRAP_FILENAME_MISMATCH", r.stdout)

    def test_bootstrap_repository_mismatch_denied(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        self.commit("docs/notes/a.md")
        r = self.run_checker(repo_env="attacker/other-repo")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("BOOTSTRAP_REPOSITORY_MISMATCH", r.stdout)

    def test_bootstrap_unauthorized_extra_path_denied(self):
        self.close_base_record("superseded-by:PA-0110 issue-999-comment-424242")
        self.new_record("PA-0110", 999, self.bootstrap_allowed(), supersedes=["PA-0009"])
        self.commit("apps/web/evil.ts")
        r = self.run_checker()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("UNMATCHED_PATH", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
