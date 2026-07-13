import copy
import io
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SPEC = importlib.util.spec_from_file_location(
    "red_team_continuity", ROOT / "scripts/continuity/red_team_continuity.py"
)
rtc = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(rtc)
OBSERVED_AT = "2026-07-13T00:00:00Z"
ACTIVE_HEAD = "c" * 40
PROMPT_CONVENTION = ROOT / "docs/project-control/PROMPT_CONVENTION.md"
OPERATING_MODEL = ROOT / "docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md"
RED_TEAM_PROTOCOL = ROOT / "docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md"
HANDOFF_PLAYBOOK = ROOT / "docs/project-control/HANDOFF_PLAYBOOK.md"
TRACKER = ROOT / "docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md"
SOURCE_REGISTER = ROOT / "docs/project-control/SOURCE_REGISTER.md"
PHASE_REPORT = ROOT / "docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md"


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def marker_block(name, fields, omit=(), duplicate=None):
    lines = [name]
    for field, value in fields:
        if field not in omit:
            lines.append(f"{field}: {value}")
    if duplicate:
        lines.append(f"{duplicate[0]}: {duplicate[1]}")
    return "\n".join(lines) + "\n"


def red_team_marker(**overrides):
    fields = [
        ("PR number", "#50"),
        ("PR head SHA", ACTIVE_HEAD),
        ("Decision", "APPROVED"),
        ("Reviewer role", "External red-team reviewer"),
        ("Review date", "2026-07-12"),
        ("Scope reviewed", "Marker parsing and classification."),
        ("Conditions", "None."),
        ("Forbidden-scope confirmation", "Confirmed."),
        ("SHA-bound statement", rtc.RED_TEAM_SHA_BOUND_STATEMENT),
    ]
    values = dict(fields)
    values.update({key: value for key, value in overrides.items() if key not in {"omit", "duplicate"}})
    return marker_block(
        "RED_TEAM_DECISION",
        [(field, values[field]) for field, _ in fields],
        omit=overrides.get("omit", ()),
        duplicate=overrides.get("duplicate"),
    )


def owner_trigger_marker(**overrides):
    fields = [
        ("Owner interruption required", "YES"),
        ("Trigger categories", "ARCHITECTURE_THRESHOLD"),
        ("Lane eligibility", "NOT_AUTOMATION_ELIGIBLE"),
        ("Human approval required", "YES"),
        ("Auto-merge eligible", "NO"),
        ("Rationale", "Marker semantics remain owner-triggered and not automation eligible."),
    ]
    values = dict(fields)
    values.update({key: value for key, value in overrides.items() if key not in {"omit", "duplicate"}})
    return marker_block(
        "OWNER_TRIGGER_REVIEW",
        [(field, values[field]) for field, _ in fields],
        omit=overrides.get("omit", ()),
        duplicate=overrides.get("duplicate"),
    )


class ContinuityCollectorTests(unittest.TestCase):
    def generate(self, name, data=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        value = fixture(name) if data is None else data
        code, evidence, packet = rtc.generate(value, OBSERVED_AT, Path(temporary.name), ROOT)
        return code, evidence, packet, Path(temporary.name)

    def test_consistent_closed_gate_exit_zero(self):
        code, evidence, _, _ = self.generate("consistent_closed_gate.json")
        self.assertEqual(code, 0)
        self.assertEqual(evidence["consistency_classification"], "consistent")

    def test_active_pr_requires_live_verification_exit_zero(self):
        code, evidence, packet, _ = self.generate("active_pr_requires_live_verification.json")
        self.assertEqual(code, 0)
        self.assertEqual(evidence["consistency_classification"], "requires_live_verification")
        self.assertIn("External exact-SHA review", packet)

    def test_stale_main_exit_two(self):
        code, evidence, _, _ = self.generate("stale_main.json")
        self.assertEqual(code, 2)
        self.assertEqual(evidence["consistency_classification"], "stale")

    def test_moved_pr_head_exit_two(self):
        code, evidence, _, _ = self.generate("moved_pr_head.json")
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_missing_evidence_exit_three(self):
        code, evidence, _, _ = self.generate("missing_evidence.json")
        self.assertEqual(code, 3)
        self.assertEqual(evidence["consistency_classification"], "blocked")

    def test_unsafe_private_evidence_exit_four(self):
        with self.assertRaises(rtc.UnsafeEvidenceError) as caught:
            rtc._load_fixture(FIXTURES / "unsafe_private_value.json")
        self.assertEqual(caught.exception.exit_code, 4)

    def test_malformed_json_exit_five(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "malformed.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(rtc.CollectorError) as caught:
                rtc._load_fixture(path)
        self.assertEqual(caught.exception.exit_code, 5)

    def test_malformed_canonical_state_exit_five(self):
        data = fixture("active_pr_requires_live_verification.json")
        del data["canonical_state"]["schema_version"]
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(rtc.CollectorError) as caught:
                rtc.generate(data, OBSERVED_AT, Path(temporary), ROOT)
        self.assertEqual(caught.exception.exit_code, 5)

    def test_identical_runs_are_byte_for_byte_identical(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            data = fixture("consistent_closed_gate.json")
            rtc.generate(data, OBSERVED_AT, Path(first), ROOT)
            rtc.generate(data, OBSERVED_AT, Path(second), ROOT)
            for name in rtc.OUTPUT_NAMES:
                self.assertEqual((Path(first) / name).read_bytes(), (Path(second) / name).read_bytes())

    def test_changed_evidence_changes_packet_hash(self):
        data = fixture("active_pr_requires_live_verification.json")
        _, first, _, _ = self.generate("active_pr_requires_live_verification.json", data)
        changed = copy.deepcopy(data)
        changed["checks"].append(
            {"name": "scope", "state": "SUCCESS", "bucket": "pass", "link": "https://example.test/check"}
        )
        _, second, _, _ = self.generate("active_pr_requires_live_verification.json", changed)
        self.assertNotEqual(first["packet_hash"], second["packet_hash"])

    def test_packet_hash_recomputation(self):
        _, evidence, packet, _ = self.generate("consistent_closed_gate.json")
        self.assertEqual(rtc.recompute_packet_hash(packet), evidence["packet_hash"])

    def test_expected_packet_fixture_is_stable(self):
        _, _, packet, _ = self.generate("active_pr_requires_live_verification.json")
        self.assertEqual(packet, (FIXTURES / "expected_startup_packet.md").read_text(encoding="utf-8"))

    def test_packet_headings_appear_exactly_once(self):
        _, _, packet, _ = self.generate("active_pr_requires_live_verification.json")
        for heading in (
            "# RED_TEAM_STARTUP_PACKET",
            "## Derived Evidence Notice",
            "## Classification",
            "## Single Next Required Action",
            "## Packet Hash",
        ):
            self.assertEqual(packet.count(heading), 1)

    def test_packet_derived_notice_is_bounded(self):
        _, _, packet, _ = self.generate("active_pr_requires_live_verification.json")
        self.assertIn("derived evidence, provides no authority", packet)
        self.assertIn("no write authorization", packet)
        self.assertNotIn("provides write authorization", packet)  # no write authorization is granted

    def test_evidence_ordering_is_stable(self):
        _, _, _, output = self.generate("active_pr_requires_live_verification.json")
        text = (output / "continuity-evidence.json").read_text(encoding="utf-8")
        self.assertEqual(text, json.dumps(json.loads(text), indent=2, sort_keys=True) + "\n")

    def test_unknown_executable_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["curl", "https://example.invalid"])

    def test_unknown_subcommand_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["gh", "repo", "clone", "x", "--repo", "x", "--json", "name"])

    def test_prohibited_git_command_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["git", "fetch", "origin"])  # forbidden fetch is rejected

    def test_prohibited_github_mutation_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["gh", "pr", "merge", "50", "--repo", "x", "--json", "state"])

    def test_subprocess_uses_argument_array_without_shell(self):
        completed = subprocess.CompletedProcess(["git", "rev-parse", "HEAD"], 0, "a" * 40 + "\n", "")
        with mock.patch.object(rtc.subprocess, "run", return_value=completed) as called:
            rtc._run_read_command(["git", "rev-parse", "HEAD"], ROOT)
        args, kwargs = called.call_args
        self.assertIsInstance(args[0], list)
        self.assertIs(kwargs["shell"], False)
        self.assertEqual(kwargs["timeout"], 20)

    def test_output_inside_repository_is_rejected(self):
        data = fixture("active_pr_requires_live_verification.json")
        with self.assertRaises(rtc.UnsafeEvidenceError) as caught:
            rtc.generate(data, OBSERVED_AT, ROOT / "scripts/continuity/tests", ROOT)
        self.assertEqual(caught.exception.exit_code, 4)

    def test_symlink_into_repository_is_rejected(self):
        data = fixture("active_pr_requires_live_verification.json")
        with tempfile.TemporaryDirectory() as temporary:
            link = Path(temporary) / "inside"
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc.generate(data, OBSERVED_AT, link, ROOT)

    def test_output_file_symlink_is_rejected(self):
        data = fixture("active_pr_requires_live_verification.json")
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / rtc.OUTPUT_NAMES[0]
            target.symlink_to(ROOT / "AGENTS.md")
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc.generate(data, OBSERVED_AT, Path(temporary), ROOT)

    def test_absolute_home_path_is_rejected(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["repository"]["name"] = "/Users/example/private/repository"
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc.generate(data, OBSERVED_AT, Path(temporary), ROOT)

    def test_marker_bound_to_another_sha_is_quarantined(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["markers"] = {
            "owner_trigger_status": "valid",
            "red_team_status": "stale",
            "red_team_bound_sha": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        }
        code, evidence, _, _ = self.generate("active_pr_requires_live_verification.json", data)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_contradictory_lifecycle_is_quarantined(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["issue"]["state"] = "closed"
        data["issue"]["closeout_state"] = "closed"
        code, evidence, _, _ = self.generate("active_pr_requires_live_verification.json", data)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_active_auto_merge_is_quarantined(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["auto_merge"]["active"] = True
        code, evidence, _, _ = self.generate("active_pr_requires_live_verification.json", data)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_raw_chat_input_is_rejected_as_a_source(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["raw_chat_status"] = "claimed source"
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(rtc.CollectorError):
                rtc.generate(data, OBSERVED_AT, Path(temporary), ROOT)

    def test_approval_claim_without_required_evidence_is_quarantined(self):
        data = fixture("active_pr_requires_live_verification.json")
        data["lifecycle_claim"] = "merge_ready"
        code, evidence, _, _ = self.generate("active_pr_requires_live_verification.json", data)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_only_two_output_files_are_generated(self):
        _, _, _, output = self.generate("active_pr_requires_live_verification.json")
        self.assertEqual(sorted(path.name for path in output.iterdir()), sorted(rtc.OUTPUT_NAMES))


class MarkerSemanticsTests(unittest.TestCase):
    def evaluations(self, body):
        return rtc._marker_evaluations(body, ACTIVE_HEAD, 50)

    def classify(self, body):
        data = fixture("active_pr_requires_live_verification.json")
        data["markers"] = rtc._marker_summary(body, ACTIVE_HEAD, 50)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def test_complete_current_head_red_team_marker_is_valid(self):
        summary = rtc._marker_summary(owner_trigger_marker() + red_team_marker(), ACTIVE_HEAD, 50)
        self.assertEqual(summary["red_team_status"], "valid")
        self.assertEqual(summary["red_team_bound_sha"], ACTIVE_HEAD)

    def test_missing_red_team_marker_remains_pending(self):
        code, evidence, _ = self.classify(owner_trigger_marker())
        self.assertEqual(code, 0)
        self.assertEqual(evidence["consistency_classification"], "requires_live_verification")
        self.assertIn("External exact-SHA red-team review is pending", evidence["blockers"])

    def test_red_team_marker_missing_required_field_is_rejected(self):
        result = self.evaluations(red_team_marker(omit=("Reviewer role",)))["red_team"]
        self.assertEqual(result["status"], "malformed")
        self.assertIn("RT_REQUIRED_FIELD_MISSING_OR_EMPTY:Reviewer role", result["reasons"])

    def test_red_team_marker_empty_required_field_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"Conditions": ""}))["red_team"]
        self.assertIn("RT_REQUIRED_FIELD_MISSING_OR_EMPTY:Conditions", result["reasons"])

    def test_red_team_marker_missing_forbidden_confirmation_is_rejected(self):
        result = self.evaluations(red_team_marker(omit=("Forbidden-scope confirmation",)))["red_team"]
        self.assertIn(
            "RT_REQUIRED_FIELD_MISSING_OR_EMPTY:Forbidden-scope confirmation", result["reasons"]
        )

    def test_red_team_marker_malformed_pr_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"PR number": "fifty"}))["red_team"]
        self.assertIn("RT_PR_NUMBER_MALFORMED", result["reasons"])

    def test_red_team_marker_wrong_pr_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"PR number": "#51"}))["red_team"]
        self.assertIn("RT_PR_NUMBER_MISMATCH", result["reasons"])

    def test_red_team_marker_malformed_sha_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"PR head SHA": "not-a-sha"}))["red_team"]
        self.assertIn("RT_SHA_MALFORMED", result["reasons"])

    def test_red_team_marker_abbreviated_sha_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"PR head SHA": ACTIVE_HEAD[:12]}))["red_team"]
        self.assertIn("RT_SHA_MALFORMED", result["reasons"])

    def test_red_team_marker_stale_sha_is_quarantined(self):
        code, evidence, _ = self.classify(
            owner_trigger_marker() + red_team_marker(**{"PR head SHA": "e" * 40})
        )
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_red_team_unsupported_decision_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"Decision": "PASS"}))["red_team"]
        self.assertIn("RT_DECISION_UNSUPPORTED", result["reasons"])

    def test_red_team_blocked_decision_is_not_approval(self):
        result = self.evaluations(red_team_marker(**{"Decision": "BLOCKED"}))["red_team"]
        self.assertEqual(result["status"], "adverse")
        self.assertIn("RT_DECISION_BLOCKED", result["reasons"])

    def test_red_team_changes_requested_is_not_approval(self):
        result = self.evaluations(red_team_marker(**{"Decision": "CHANGES_REQUESTED"}))["red_team"]
        self.assertEqual(result["status"], "adverse")
        self.assertIn("RT_DECISION_CHANGES_REQUESTED", result["reasons"])

    def test_red_team_marker_malformed_review_date_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"Review date": "07/12/2026"}))["red_team"]
        self.assertIn("RT_REVIEW_DATE_MALFORMED", result["reasons"])

    def test_red_team_marker_wrong_bound_statement_is_rejected(self):
        result = self.evaluations(red_team_marker(**{"SHA-bound statement": "Applies forever."}))[
            "red_team"
        ]
        self.assertIn("RT_SHA_BOUND_STATEMENT_INVALID", result["reasons"])

    def test_red_team_duplicate_field_is_rejected(self):
        result = self.evaluations(red_team_marker(duplicate=("Decision", "APPROVED")))["red_team"]
        self.assertIn("RT_DUPLICATE_FIELD:Decision", result["reasons"])

    def test_conflicting_red_team_markers_are_quarantined(self):
        body = owner_trigger_marker() + red_team_marker() + red_team_marker(**{"Decision": "BLOCKED"})
        result = self.evaluations(body)["red_team"]
        self.assertEqual(result["status"], "conflicting")
        code, evidence, _ = self.classify(body)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_duplicate_red_team_markers_are_ambiguous(self):
        body = red_team_marker() + red_team_marker()
        result = self.evaluations(body)["red_team"]
        self.assertEqual(result["status"], "ambiguous")
        self.assertIn("RT_DUPLICATE_GOVERNING_MARKERS", result["reasons"])

    def test_fenced_red_team_marker_example_is_ignored(self):
        body = owner_trigger_marker() + "```text\n" + red_team_marker() + "```\n"
        self.assertEqual(rtc._marker_summary(body, ACTIVE_HEAD, 50)["red_team_status"], "missing")

    def test_html_comment_red_team_marker_example_is_ignored(self):
        body = owner_trigger_marker() + "<!--\n" + red_team_marker() + "-->\n"
        self.assertEqual(rtc._marker_summary(body, ACTIVE_HEAD, 50)["red_team_status"], "missing")

    def test_complete_owner_trigger_marker_is_valid(self):
        result = self.evaluations(owner_trigger_marker())["owner"]
        self.assertEqual(result, {"status": "valid", "reasons": []})

    def test_owner_trigger_missing_rationale_is_rejected(self):
        body = owner_trigger_marker(omit=("Rationale",))
        result = self.evaluations(body)["owner"]
        self.assertIn("OWNER_REQUIRED_FIELD_MISSING_OR_EMPTY:Rationale", result["reasons"])
        code, evidence, _ = self.classify(body)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_owner_trigger_unknown_category_is_rejected(self):
        result = self.evaluations(owner_trigger_marker(**{"Trigger categories": "MAGIC"}))["owner"]
        self.assertIn("OWNER_CATEGORY_UNKNOWN", result["reasons"])

    def test_owner_trigger_category_interruption_conflict_is_rejected(self):
        result = self.evaluations(owner_trigger_marker(**{"Trigger categories": "NONE"}))["owner"]
        self.assertIn("OWNER_INTERRUPTION_CATEGORY_CONFLICT", result["reasons"])

    def test_owner_trigger_category_lane_conflict_is_rejected(self):
        result = self.evaluations(
            owner_trigger_marker(**{"Lane eligibility": "FUTURE_LOW_RISK_CANDIDATE"})
        )["owner"]
        self.assertIn("OWNER_CATEGORY_LANE_CONFLICT", result["reasons"])

    def test_owner_trigger_unknown_lane_is_rejected(self):
        result = self.evaluations(owner_trigger_marker(**{"Lane eligibility": "UNKNOWN"}))["owner"]
        self.assertIn("OWNER_LANE_VALUE_INVALID", result["reasons"])

    def test_owner_trigger_human_approval_no_is_rejected(self):
        result = self.evaluations(owner_trigger_marker(**{"Human approval required": "NO"}))[
            "owner"
        ]
        self.assertIn("OWNER_HUMAN_APPROVAL_MUST_BE_YES", result["reasons"])

    def test_owner_trigger_auto_merge_yes_is_rejected(self):
        result = self.evaluations(owner_trigger_marker(**{"Auto-merge eligible": "YES"}))["owner"]
        self.assertIn("OWNER_AUTO_MERGE_MUST_BE_NO", result["reasons"])

    def test_conflicting_owner_trigger_markers_are_quarantined(self):
        body = owner_trigger_marker() + owner_trigger_marker(**{"Trigger categories": "LEGAL"})
        result = self.evaluations(body)["owner"]
        self.assertEqual(result["status"], "conflicting")
        code, evidence, _ = self.classify(body)
        self.assertEqual(code, 2)
        self.assertTrue(evidence["quarantine"])

    def test_duplicate_owner_trigger_markers_are_ambiguous(self):
        result = self.evaluations(owner_trigger_marker() + owner_trigger_marker())["owner"]
        self.assertEqual(result["status"], "ambiguous")
        self.assertIn("OWNER_DUPLICATE_GOVERNING_MARKERS", result["reasons"])

    def test_fenced_owner_trigger_example_is_ignored(self):
        body = "```text\n" + owner_trigger_marker() + "```\n"
        self.assertEqual(self.evaluations(body)["owner"]["status"], "missing")

    def test_html_comment_owner_trigger_example_is_ignored(self):
        body = "<!--\n" + owner_trigger_marker() + "-->\n"
        self.assertEqual(self.evaluations(body)["owner"]["status"], "missing")


class ApprovalEvidenceTests(unittest.TestCase):
    def data(self):
        return fixture("active_pr_requires_live_verification.json")

    def record(self, review_id=10, login="reviewer", state="APPROVED", **overrides):  # scope-bound approval evidence
        value = {
            "review_id": review_id,
            "reviewer_login": login,  # scope-bound approval evidence
            "reviewer_type": "User",
            "state": state,
            "submitted_at": "2026-07-12T22:00:00Z",
            "commit_id": ACTIVE_HEAD,
            "author_association": "MEMBER",  # scope-bound approval evidence
        }
        value.update(overrides)
        return value

    def permission(self, login="reviewer", permission="write", **overrides):  # scope-bound approval evidence
        value = {
            "reviewer_login": login,  # scope-bound approval evidence
            "permission": permission,
            "role_name": permission,
            "account_type": "User",
        }
        value.update(overrides)
        return value

    def set_review(self, data, records, permissions=(), decision=None, claimed=()):
        data["review"] = {
            "decision": decision,
            "evidence_status": "complete",
            "review_records": list(records),
            "permission_records": list(permissions),
            "qualifying_approvals": list(claimed),
            "disqualified_approvals": [],
            "disqualification_reasons": {},
        }
        return data

    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def evaluation(self, data):
        return rtc._approval_evaluation(data["pr"], data["review"])

    def test_current_head_approved_write_user_qualifies(self):
        data = self.set_review(self.data(), [self.record()], [self.permission()], claimed=["reviewer"])
        code, evidence, _ = self.classify(data)
        self.assertEqual(code, 0)
        self.assertEqual(evidence["live_state"]["review"]["qualifying_approvals"], ["reviewer"])

    def test_current_head_approved_admin_user_qualifies(self):
        data = self.set_review(self.data(), [self.record()], [self.permission(permission="admin")], claimed=["reviewer"])
        self.assertEqual(self.evaluation(data)["review"]["qualifying_approvals"], ["reviewer"])

    def test_write_permission_mapping_accepts_maintain_base_permission(self):
        data = self.set_review(
            self.data(), [self.record()], [self.permission(permission="write", role_name="maintain")], claimed=["reviewer"]
        )
        self.assertEqual(self.evaluation(data)["review"]["qualifying_approvals"], ["reviewer"])

    def test_read_permission_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record()], [self.permission(permission="read")])
        result = self.evaluation(data)["review"]
        self.assertEqual(result["qualifying_approvals"], [])
        self.assertIn("APPROVAL_PERMISSION_READ_ONLY", result["disqualification_reasons"]["reviewer"])

    def test_none_permission_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record()], [self.permission(permission="none")])
        self.assertIn("APPROVAL_PERMISSION_NONE", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_unknown_permission_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record()], [self.permission(permission="triage")])
        self.assertIn("APPROVAL_PERMISSION_UNKNOWN", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_stale_head_approval_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(commit_id="d" * 40)])
        self.assertIn("APPROVAL_STALE_HEAD", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_pr_author_approval_does_not_qualify(self):  # scope-bound approval evidence
        data = self.set_review(self.data(), [self.record(login="pr-author-scope")])  # scope-bound approval evidence
        self.assertIn("APPROVAL_PR_AUTHOR", self.evaluation(data)["review"]["disqualification_reasons"]["pr-author-scope"])  # scope-bound approval evidence

    def test_bot_approval_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(reviewer_type="Bot")])
        self.assertIn("APPROVAL_BOT_ACCOUNT", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_decisive_review_without_timestamp_is_malformed(self):
        data = self.set_review(self.data(), [self.record(submitted_at=None)])
        with self.assertRaises(rtc.CollectorError):
            self.evaluation(data)

    def test_dismissed_review_does_not_qualify(self):
        records = [self.record(), self.record(11, state="DISMISSED", submitted_at="2026-07-12T23:00:00Z")]
        data = self.set_review(self.data(), records, [self.permission()])
        self.assertIn("APPROVAL_DISMISSED", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_later_changes_requested_supersedes_approval(self):
        records = [self.record(), self.record(11, state="CHANGES_REQUESTED", submitted_at="2026-07-12T23:00:00Z")]
        data = self.set_review(self.data(), records, [self.permission()])
        self.assertIn("APPROVAL_SUPERSEDED_BY_CHANGES_REQUESTED", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_later_comment_does_not_erase_approval(self):
        records = [self.record(), self.record(11, state="COMMENTED", submitted_at="2026-07-12T23:00:00Z")]
        data = self.set_review(self.data(), records, [self.permission()], claimed=["reviewer"])
        self.assertEqual(self.evaluation(data)["review"]["qualifying_approvals"], ["reviewer"])

    def test_author_association_alone_does_not_qualify(self):  # scope-bound approval evidence
        data = self.set_review(self.data(), [self.record(author_association="OWNER")])  # scope-bound approval evidence
        result = self.evaluation(data)
        self.assertEqual(result["review"]["qualifying_approvals"], [])
        self.assertTrue(result["blocked"])

    def test_duplicate_review_id_is_quarantined(self):
        record = self.record()
        data = self.set_review(self.data(), [record, copy.deepcopy(record)], [self.permission()])
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_conflicting_duplicate_review_is_quarantined(self):
        data = self.set_review(self.data(), [self.record(), self.record(state="CHANGES_REQUESTED")], [self.permission()])
        self.assertTrue(self.evaluation(data)["quarantined"])

    def test_permission_login_mismatch_is_quarantined(self):  # scope-bound approval evidence
        data = self.set_review(self.data(), [self.record()], [self.permission(login="other")])  # scope-bound approval evidence
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_missing_permission_evidence_is_blocked(self):
        data = self.set_review(self.data(), [self.record()])
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (3, "blocked"))

    def test_review_evidence_truncation_is_blocked(self):
        data = self.set_review(self.data(), [])
        data["review"]["evidence_status"] = "truncated"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (3, "blocked"))

    def test_review_decision_approved_without_qualified_approval_is_quarantined(self):
        data = self.set_review(self.data(), [], decision="APPROVED")
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_active_pr_without_approval_remains_pending(self):
        code, evidence, _ = self.classify(self.data())
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))
        self.assertIn("Human/write-access approval is pending", evidence["blockers"])

    def test_externally_approved_claim_requires_qualified_approval(self):
        data = self.data()
        data["lifecycle_claim"] = "externally_approved"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_merge_ready_claim_requires_qualified_approval(self):
        data = self.data()
        data["lifecycle_claim"] = "merge_ready"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_qualifying_approvals_are_unique_and_sorted(self):
        records = [self.record(20, "zeta"), self.record(10, "alpha")]
        permissions = [self.permission("zeta"), self.permission("alpha")]
        data = self.set_review(self.data(), records, permissions, claimed=["zeta", "alpha"])
        self.assertEqual(self.evaluation(data)["review"]["qualifying_approvals"], ["alpha", "zeta"])

    def test_review_records_are_deterministically_sorted(self):
        records = [self.record(20, submitted_at="2026-07-12T23:00:00Z"), self.record(10)]
        data = self.set_review(self.data(), records, [self.permission()], claimed=["reviewer"])
        self.assertEqual([r["review_id"] for r in self.evaluation(data)["review"]["review_records"]], [10, 20])

    def test_review_body_is_not_persisted(self):
        record = rtc._normalized_review_record({"id": 10, "user": {"login": "reviewer", "type": "User"}, "state": "APPROVED", "submitted_at": OBSERVED_AT, "commit_id": ACTIVE_HEAD, "author_association": "MEMBER", "body": "private prose"})  # scope-bound approval evidence
        self.assertNotIn("body", record)
        self.assertNotIn("private prose", json.dumps(record))

    def test_unrestricted_gh_api_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["gh", "api", "--method", "GET", "repos/Zest-LeadGen/contractoros-california/issues"])

    def test_mutating_gh_api_shape_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["gh", "api", "--method", "POST", "repos/Zest-LeadGen/contractoros-california/pulls/50/reviews"])

    def test_api_pagination_above_bound_is_rejected(self):
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(["gh", "api", "--method", "GET", "repos/Zest-LeadGen/contractoros-california/pulls/50/reviews?per_page=100&page=6"])

    def test_permission_endpoint_for_unsourced_login_is_rejected(self):  # scope-bound approval evidence
        command = ["gh", "api", "--method", "GET", "repos/Zest-LeadGen/contractoros-california/collaborators/reviewer/permission"]
        with self.assertRaises(rtc.CommandRejectedError):
            rtc._validate_command(command, {"another-reviewer"})


class WorkflowProvenanceTests(unittest.TestCase):
    def data(self):
        return fixture("active_pr_requires_live_verification.json")

    def job(self, data):
        return data["workflow_run"]["jobs"][0]

    def step(self, data, name):
        return next(step for step in self.job(data)["steps"] if step["name"] == name)

    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def make_full_success(self, data, marker=True):
        run = data["workflow_run"]
        job = self.job(data)
        run["conclusion"] = "success"
        job["conclusion"] = "success"
        for step in job["steps"]:
            step["conclusion"] = "success"
        data["checks"][0].update({"state": "SUCCESS", "bucket": "pass"})
        if marker:
            data["markers"] = {
                "owner_trigger_status": "valid",
                "red_team_status": "valid",
                "red_team_bound_sha": ACTIVE_HEAD,
            }
        return data

    def assert_quarantined(self, data):
        code, evidence, _ = self.classify(data)
        self.assertEqual(code, 2)
        self.assertEqual(evidence["consistency_classification"], "quarantined")
        self.assertTrue(evidence["quarantine"])
        return evidence

    def test_expected_control_workflow_identity_is_accepted(self):
        code, evidence, _ = self.classify(self.data())
        self.assertEqual(code, 0)
        self.assertEqual(evidence["consistency_classification"], "requires_live_verification")

    def test_wrong_repository_is_quarantined(self):
        data = self.data()
        data["repository"]["name"] = "Zest-LeadGen/another-repository"
        evidence = self.assert_quarantined(data)
        self.assertIn("Workflow provenance mismatch: repository", evidence["comparison_findings"])

    def test_wrong_workflow_name_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["name"] = "Another Workflow"
        self.assert_quarantined(data)

    def test_wrong_workflow_id_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["workflow_id"] = 1
        self.assert_quarantined(data)

    def test_push_event_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["event"] = "push"
        self.assert_quarantined(data)

    def test_wrong_run_head_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["head_sha"] = "d" * 40
        self.assert_quarantined(data)

    def test_wrong_run_branch_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["head_branch"] = "another-branch"
        self.assert_quarantined(data)

    def test_pr_check_link_to_another_run_is_quarantined(self):
        data = self.data()
        data["checks"][0]["link"] = (
            "https://github.com/Zest-LeadGen/contractoros-california/actions/runs/999/job/1"
        )
        self.assert_quarantined(data)

    def test_missing_expected_job_is_blocked(self):
        data = self.data()
        data["workflow_run"]["jobs"] = []
        code, evidence, _ = self.classify(data)
        self.assertEqual(code, 3)
        self.assertIn("Missing expected ContractorOS workflow job", evidence["blockers"])

    def test_duplicate_expected_job_is_quarantined(self):
        data = self.data()
        data["workflow_run"]["jobs"].append(copy.deepcopy(self.job(data)))
        self.assert_quarantined(data)

    def test_missing_required_step_is_blocked(self):
        data = self.data()
        self.job(data)["steps"] = [
            step for step in self.job(data)["steps"] if step["name"] != "Python version"
        ]
        code, evidence, _ = self.classify(data)
        self.assertEqual(code, 3)
        self.assertIn("Missing required workflow step: Python version", evidence["blockers"])

    def test_duplicate_required_step_is_quarantined(self):
        data = self.data()
        self.job(data)["steps"].append(copy.deepcopy(self.step(data, "Python version")))
        self.assert_quarantined(data)

    def test_required_step_order_mismatch_is_quarantined(self):
        data = self.data()
        self.step(data, "Python version")["number"] = 20
        self.assert_quarantined(data)

    def test_failed_pre_marker_step_is_quarantined(self):
        data = self.data()
        self.step(data, "Forbidden-scope check")["conclusion"] = "failure"
        self.assert_quarantined(data)

    def test_expected_missing_marker_failure_remains_pending(self):
        code, evidence, _ = self.classify(self.data())
        self.assertEqual(code, 0)
        self.assertIn("External exact-SHA red-team review is pending", evidence["blockers"])

    def test_marker_step_success_without_marker_is_quarantined(self):
        data = self.make_full_success(self.data(), marker=False)
        self.assert_quarantined(data)

    def test_valid_marker_with_marker_step_failure_is_quarantined(self):
        data = self.data()
        data["markers"] = {
            "owner_trigger_status": "valid",
            "red_team_status": "valid",
            "red_team_bound_sha": ACTIVE_HEAD,
        }
        self.assert_quarantined(data)

    def test_post_marker_success_before_marker_is_quarantined(self):
        data = self.data()
        self.step(data, rtc.POST_MARKER_STEPS[0])["conclusion"] = "success"
        self.assert_quarantined(data)

    def test_valid_marker_with_skipped_post_marker_steps_is_quarantined(self):
        data = self.data()
        data["markers"] = {
            "owner_trigger_status": "valid",
            "red_team_status": "valid",
            "red_team_bound_sha": ACTIVE_HEAD,
        }
        self.step(data, rtc.MARKER_STEP)["conclusion"] = "success"
        data["workflow_run"]["conclusion"] = "success"
        self.job(data)["conclusion"] = "success"
        data["checks"][0].update({"state": "SUCCESS", "bucket": "pass"})
        self.assert_quarantined(data)

    def test_full_success_matrix_is_accepted(self):
        code, evidence, _ = self.classify(self.make_full_success(self.data()))
        self.assertEqual(code, 0)
        self.assertEqual(evidence["consistency_classification"], "requires_live_verification")

    def test_pending_run_cannot_support_approval(self):
        data = self.make_full_success(self.data())
        data["workflow_run"].update({"status": "in_progress", "conclusion": None})
        code, evidence, _ = self.classify(data)
        self.assertEqual(code, 3)
        self.assertIn("ContractorOS workflow run is pending or in progress", evidence["blockers"])

    def test_check_state_conflict_is_quarantined(self):
        data = self.data()
        data["checks"][0].update({"state": "SUCCESS", "bucket": "pass"})
        self.assert_quarantined(data)

    def test_unknown_failed_check_is_quarantined(self):
        data = self.data()
        data["checks"].append(
            {
                "name": "unexpected-check",
                "state": "FAILURE",
                "bucket": "fail",
                "link": "https://github.com/Zest-LeadGen/contractoros-california/actions/runs/30000000001",
            }
        )
        self.assert_quarantined(data)

    def test_completed_run_with_pending_required_step_is_quarantined(self):
        data = self.data()
        self.step(data, "Python version")["status"] = "in_progress"
        self.assert_quarantined(data)

    def test_workflow_success_with_failed_step_is_quarantined(self):
        data = self.make_full_success(self.data())
        self.step(data, "Changed-file allowlist / lane check")["conclusion"] = "failure"
        self.assert_quarantined(data)

    def test_workflow_failure_without_explaining_step_is_quarantined(self):
        data = self.make_full_success(self.data())
        data["workflow_run"]["conclusion"] = "failure"
        self.job(data)["conclusion"] = "failure"
        data["checks"][0].update({"state": "FAILURE", "bucket": "fail"})
        self.assert_quarantined(data)

    def test_unknown_contradictory_step_is_quarantined(self):
        data = self.data()
        self.job(data)["steps"].append(
            {"name": "Unexpected control", "number": 13, "status": "completed", "conclusion": "failure"}
        )
        self.assert_quarantined(data)

    def test_step_and_finding_order_is_deterministic(self):
        data = self.data()
        data["workflow_run"].update(
            {"name": "Wrong", "workflow_id": 1, "event": "push", "head_branch": "wrong"}
        )
        first = self.assert_quarantined(copy.deepcopy(data))["comparison_findings"]
        second = self.assert_quarantined(copy.deepcopy(data))["comparison_findings"]
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first))


class GovernanceHardeningTests(unittest.TestCase):
    def text(self, path):
        return path.read_text(encoding="utf-8")

    def test_prompt_profile_has_all_ten_fields_in_order(self):
        text = self.text(PROMPT_CONVENTION)
        fields = (
            "Recommended Codex model:",
            "Recommended reasoning effort:",
            "Why this model/effort:",
            "Do not change model/effort unless:",
            "Recommended speed mode:",
            "Agent strategy:",
            "Plan/quota mode:",
            "Context-window strategy:",
            "Checkpoint cadence:",
            "Maximum scope:",
        )
        positions = [text.index(field) for field in fields]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(len(set(positions)), 10)
        self.assertIn("exact ordered, non-empty fields", text)

    def test_medium_and_standard_are_normal_defaults(self):
        text = self.text(PROMPT_CONVENTION)
        self.assertIn("Medium | Default for inspection, recovery, bounded implementation", text)
        self.assertIn("`STANDARD` is the default for ContractorOS Plus-plan work", text)

    def test_fast_requires_explicit_justification_and_owner_approval(self):
        text = self.text(PROMPT_CONVENTION)
        self.assertIn("Fast may be used only when", text)
        self.assertIn("latency is materially important", text)
        self.assertIn("the owner approves it", text)

    def test_one_lead_agent_is_default_and_ultra_is_not(self):
        text = self.text(PROMPT_CONVENTION)
        self.assertIn("One lead agent is the default", text)
        self.assertIn("Ultra | Owner-approved parallelizable exception; never the default", text)

    def test_hidden_execution_metadata_does_not_stop_or_get_fabricated(self):
        text = self.text(PROMPT_CONVENTION)
        self.assertIn("ACTUAL_CODEX_MODEL=GPT-5 family; exact identifier not exposed", text)
        self.assertIn("ACTUAL_REASONING_EFFORT=NOT_EXPOSED", text)
        self.assertIn("SPEED_MODE=NOT_EXPOSED", text)
        self.assertIn("Hidden metadata alone must never stop permitted work", text)
        self.assertIn("Do not guess a hidden model, effort, or speed value", text)

    def test_atomic_packet_fields_are_durable(self):
        text = self.text(PROMPT_CONVENTION)
        for field in (
            "Primary objective:", "Permitted files/functions:", "Model:",
            "Reasoning effort:", "Speed:", "Agent count:", "Focused validation:",
            "Checkpoint:", "Stop conditions:", "Next packet:",
        ):
            self.assertIn(field, text)

    def test_79_percent_requires_new_window(self):
        self.assertIn("A reported 79% requires a new Codex window", self.text(HANDOFF_PLAYBOOK))

    def test_85_percent_requires_handoff_only(self):
        text = self.text(HANDOFF_PLAYBOOK)
        self.assertIn("85-100%: handoff-only; no new implementation", text)

    def test_compact_tables_are_required_and_paragraph_compression_is_prohibited(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("a compact Markdown table", text)
        self.assertIn("must not be flattened into delimiter-separated or compressed paragraph strings", text)

    def test_active_phase_and_program_categories_are_required(self):
        text = self.text(RED_TEAM_PROTOCOL)
        for value in (
            "durable intake/scope", "implementation", "tests/validation",
            "documentation reconciliation", "external exact-SHA review", "human approval",
            "merge/main verification", "issue closeout", "governance/control",
            "workflow automation", "product implementation", "content governance/production",
            "dependency/runtime", "backend/data platform", "build/distribution",
            "business/market validation", "overall program",
        ):
            self.assertIn(value, text)

    def test_interactive_chart_is_actual_single_and_last_where_supported(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("exactly one actual detailed interactive chart at the absolute bottom", text)
        self.assertIn("Nothing may appear after the chart", text)

    def test_raw_chart_configuration_is_prohibited(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("Raw chart JSON, widget arguments, terminal representations", text)
        self.assertIn("must never be presented as the chart", text)

    def test_percentage_categories_remain_separate(self):
        text = self.text(TRACKER)
        self.assertIn("Current-phase reporting must remain separate from program-capability reporting", text)
        self.assertIn("Overall program | Must not inherit governance-only gains", text)

    def test_governance_inflation_is_prohibited(self):
        text = self.text(OPERATING_MODEL)
        self.assertIn("Governance documentation cannot increase actual product or operational capability", text)

    def test_workflow_and_control_script_changes_remain_forbidden(self):
        agents = self.text(ROOT / "AGENTS.md")
        report = self.text(
            ROOT / "docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md"
        )
        self.assertIn("workflow", agents.lower())
        self.assertIn("no existing workflow or control script changed", report.lower())

    def test_red_team_protocol_requires_complete_prompt_profile(self):
        text = self.text(RED_TEAM_PROTOCOL)
        fields = (
            "Recommended Codex model:",
            "Recommended reasoning effort:",
            "Why this model/effort:",
            "Do not change model/effort unless:",
            "Recommended speed mode:",
            "Agent strategy:",
            "Plan/quota mode:",
            "Context-window strategy:",
            "Checkpoint cadence:",
            "Maximum scope:",
        )
        positions = [text.index(field) for field in fields]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("Each field must have a non-empty value", text)
        for prompt_type in (
            "implementation prompt", "correction prompt", "continuation prompt",
            "review-remediation prompt", "new-window handoff", "automation prompt",
        ):
            self.assertIn(prompt_type, text)

    def test_red_team_protocol_requires_hidden_metadata_fallback(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("ACTUAL_CODEX_MODEL=GPT-5 family; exact identifier not exposed", text)
        self.assertIn("ACTUAL_REASONING_EFFORT=NOT_EXPOSED", text)
        self.assertIn("SPEED_MODE=NOT_EXPOSED", text)
        self.assertIn("must never be guessed", text)

    def test_red_team_protocol_requires_visible_selector_preservation(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("preserve a visible selector choice", text)
        self.assertIn("must not silently change or downgrade it", text)
        self.assertIn("Medium reasoning, Standard speed, and one lead agent", text)
        self.assertIn("quota-aware atomic packet", text)

    def test_official_source_review_is_dated(self):
        text = self.text(PROMPT_CONVENTION)
        self.assertIn("Current official-source review date: 2026-07-12", text)
        self.assertIn("dated snapshot, not permanent policy", text)
        self.assertIn("must be reverified before recommendation", text)

    def test_official_model_pricing_and_speed_sources_are_recorded(self):
        text = self.text(SOURCE_REGISTER)
        for url in (
            "https://developers.openai.com/codex/models/",
            "https://developers.openai.com/codex/pricing/",
            "https://learn.chatgpt.com/docs/agent-configuration/speed",
        ):
            self.assertIn(url, text)
        self.assertGreaterEqual(text.count("Verified 2026-07-12; time-sensitive"), 3)
        self.assertGreaterEqual(text.count("Reverify"), 3)

    def test_stable_policy_is_separate_from_dated_guidance(self):
        text = self.text(PROMPT_CONVENTION)
        stable = text.index("## Stable Policy")
        dated = text.index("## Dated Current Guidance")
        self.assertLess(stable, dated)
        self.assertIn("do not depend on a current model catalog", text[stable:dated])
        self.assertIn("Sol 15-90, Terra 20-110, and Luna 50-280", text[dated:])

    def test_stale_gpt55_guidance_is_marked_superseded(self):
        text = self.text(SOURCE_REGISTER)
        self.assertIn("SRC-4J0-008", text)
        self.assertIn("Historical; superseded for current guidance on 2026-07-12", text)
        self.assertIn("GPT-5.5-only guidance is not current routing policy", text)

    def test_interactive_chart_does_not_require_unsupported_expandability(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("expand/collapse or drill-down only when the response surface explicitly supports", text)
        self.assertIn("use compact Markdown tables", text)
        self.assertNotIn("actual detailed and expandable chart", text)

    def test_hoverability_is_not_claimed_as_expandability(self):
        text = self.text(RED_TEAM_PROTOCOL)
        self.assertIn("Use hover details or tooltips where supported", text)
        self.assertIn("Hoverability is not evidence of expandability", text)

    def test_prior_head_workflow_evidence_is_recorded_truthfully(self):
        text = self.text(PHASE_REPORT)
        self.assertIn("29203963944", text)
        self.assertIn("9a684f427bc45e5cf8575e4bd105671a22baf1fd", text)
        self.assertIn("completed with overall conclusion `failure`", text)
        self.assertIn("all pre-marker controls passed", text)
        self.assertIn("mandatory SHA-bound red-team marker step failed", text)
        self.assertIn("post-marker checks were skipped", text)
        self.assertIn("created no review, approval, merge, or release decision power", text)


class CollectorCorrectionCluster3Tests(unittest.TestCase):
    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def active(self):
        return fixture("active_pr_requires_live_verification.json")

    def approved_workflow(self, data):
        data["markers"] = {
            "owner_trigger_status": "valid",
            "red_team_status": "valid",
            "red_team_bound_sha": data["pr"]["head"],
        }
        data["workflow_run"]["conclusion"] = "success"
        data["workflow_run"]["jobs"][0]["conclusion"] = "success"
        for step in data["workflow_run"]["jobs"][0]["steps"]:
            step["conclusion"] = "success"
        data["checks"][0].update({"state": "SUCCESS", "bucket": "pass"})
        return data

    def add_approval(self, data):
        source = fixture("consistent_closed_gate.json")["review"]
        data["review"] = copy.deepcopy(source)
        for record in data["review"]["review_records"]:
            record["commit_id"] = data["pr"]["head"]
        return data

    def raw_approval(self):
        return {
            "id": 1,
            "user": {"login": "reviewer", "type": "User"},  # scope-bound approval evidence
            "state": "APPROVED",
            "submitted_at": "2026-07-13T00:00:00Z",
            "commit_id": ACTIVE_HEAD,
            "author_association": "MEMBER",  # scope-bound approval evidence
        }

    def collect_permission_with(self, permission_result):
        with mock.patch.object(
            rtc, "_json_command", side_effect=[[self.raw_approval()], permission_result]
        ):
            return rtc._collect_review_evidence(ROOT, [], ACTIVE_HEAD, "author")  # scope-bound approval evidence

    def test_live_repository_name_empty_is_blocked(self):
        repo = {"nameWithOwner": "", "defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_live_repository_name_missing_is_blocked(self):
        repo = {"defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_default_branch_ref_wrong_type_is_blocked(self):
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(
                {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": []},
                rtc.EXPECTED_REPOSITORY,
            )

    def test_default_branch_name_missing_is_blocked(self):
        repo = {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": {"target": {"oid": "a" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_default_branch_target_missing_is_blocked(self):
        repo = {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": {"name": "main"}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_default_branch_target_oid_missing_is_blocked(self):
        repo = {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": {"name": "main", "target": {}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_default_branch_target_oid_malformed_is_blocked(self):
        repo = {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": {"name": "main", "target": {"oid": "A" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_live_default_branch_never_falls_back_to_origin_main(self):
        repo = {"nameWithOwner": rtc.EXPECTED_REPOSITORY, "defaultBranchRef": {"name": "", "target": {"oid": None}}}
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)

    def test_permission_command_rejection_remains_exit_5_through_collection(self):
        with self.assertRaises(rtc.CommandRejectedError) as caught:
            self.collect_permission_with(rtc.CommandRejectedError("rejected"))
        self.assertEqual(caught.exception.exit_code, 5)

    def test_permission_unsafe_evidence_remains_exit_4(self):
        with self.assertRaises(rtc.UnsafeEvidenceError) as caught:
            self.collect_permission_with(rtc.UnsafeEvidenceError("unsafe"))
        self.assertEqual(caught.exception.exit_code, 4)

    def test_permission_read_unavailable_returns_exit_3(self):
        with self.assertRaises(rtc.ApprovalEvidenceUnavailableError) as caught:
            self.collect_permission_with(rtc.EvidenceUnavailableError("unavailable"))
        self.assertEqual(caught.exception.exit_code, 3)

    def test_permission_response_wrong_type_is_blocked(self):
        with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
            self.collect_permission_with([])

    def test_permission_response_missing_permission_is_blocked(self):
        with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
            self.collect_permission_with({"role_name": "write", "user": {"type": "User"}})

    def test_permission_response_missing_user_type_is_blocked(self):
        with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
            self.collect_permission_with({"permission": "write", "role_name": "write", "user": {}})

    def test_canonical_linked_issue_wrong_type_returns_exit_5(self):
        data = self.active()
        data["canonical_state"]["linked_issue"] = []
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_canonical_linked_issue_missing_number_returns_exit_5(self):
        data = self.active()
        del data["canonical_state"]["linked_issue"]["number"]
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_canonical_linked_issue_invalid_state_returns_exit_5(self):
        data = self.active()
        data["canonical_state"]["linked_issue"]["state"] = "unknown"
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_canonical_linked_pr_wrong_type_returns_exit_5(self):
        data = self.active()
        data["canonical_state"]["linked_pr"] = "open"
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_canonical_linked_pr_missing_number_returns_exit_5(self):
        data = self.active()
        del data["canonical_state"]["linked_pr"]["number"]
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_canonical_linked_pr_invalid_observed_head_returns_exit_5(self):
        data = self.active()
        data["canonical_state"]["linked_pr"]["observed_head_sha"] = "not-a-sha"
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_malformed_nested_canonical_cli_returns_exit_5_without_traceback(self):
        data = self.active()
        data["canonical_state"]["linked_pr"] = []
        with tempfile.TemporaryDirectory() as temporary:
            fixture_path = Path(temporary) / "fixture.json"
            fixture_path.write_text(json.dumps(data), encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch("sys.stderr", stderr):
                code = rtc.main(
                    [
                        "fixture", "--fixture", str(fixture_path), "--observed-at", OBSERVED_AT,
                        "--output-dir", str(Path(temporary) / "output"),
                    ]
                )
        self.assertEqual(code, 5)
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_closed_gate_requires_canonical_linked_pr_identity(self):
        data = fixture("consistent_closed_gate.json")
        data["canonical_state"]["linked_pr"]["number"] = 51
        self.assertEqual(self.classify(data)[0], 2)

    def test_exact_https_origin_is_verified(self):
        self.assertTrue(rtc._normalize_origin("https://github.com/Zest-LeadGen/contractoros-california")["remote_verified"])

    def test_https_dot_git_origin_is_verified(self):
        self.assertTrue(rtc._normalize_origin("https://github.com/Zest-LeadGen/contractoros-california.git")["remote_verified"])

    def test_scp_ssh_origin_is_verified(self):
        result = rtc._normalize_origin("git@github.com:Zest-LeadGen/contractoros-california.git")
        self.assertEqual((result["remote_verified"], result["remote_transport"]), (True, "ssh"))

    def test_ssh_url_origin_is_verified(self):
        self.assertTrue(rtc._normalize_origin("ssh://git@github.com/Zest-LeadGen/contractoros-california.git")["remote_verified"])

    def test_wrong_repository_origin_is_quarantined(self):
        self.assertFalse(rtc._normalize_origin("https://github.com/Zest-LeadGen/other.git")["remote_verified"])

    def test_wrong_github_owner_is_quarantined(self):
        self.assertFalse(rtc._normalize_origin("https://github.com/Other/contractoros-california.git")["remote_verified"])

    def test_non_github_host_is_quarantined(self):
        self.assertFalse(rtc._normalize_origin("https://example.com/Zest-LeadGen/contractoros-california.git")["remote_verified"])

    def test_local_path_remote_is_quarantined(self):
        self.assertFalse(rtc._normalize_origin("../contractoros-california")["remote_verified"])

    def test_embedded_remote_credentials_are_rejected(self):
        with self.assertRaises(rtc.UnsafeEvidenceError):
            rtc._normalize_origin("https://user:secret@github.com/Zest-LeadGen/contractoros-california.git")

    def test_git_top_level_mismatch_is_quarantined(self):
        data = self.active()
        data["repository"]["root_verified"] = False
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_verified_root_absolute_path_is_not_persisted(self):
        _, evidence, _ = self.classify(self.active())
        self.assertNotIn(str(ROOT), json.dumps(evidence))

    def test_repository_argument_cannot_select_another_repository(self):
        data = self.active()
        data["repository"]["requested_name"] = "Other/repository"
        with self.assertRaises(rtc.CollectorError):
            self.classify(data)

    def test_missing_git_executable_returns_exit_3(self):
        with mock.patch.object(rtc.subprocess, "run", side_effect=FileNotFoundError()):
            with self.assertRaises(rtc.EvidenceUnavailableError) as caught:
                rtc._run_read_command(["git", "rev-parse", "HEAD"], ROOT)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_allowed_git_timeout_returns_exit_3(self):
        with mock.patch.object(rtc.subprocess, "run", side_effect=subprocess.TimeoutExpired("git", 1)):
            with self.assertRaises(rtc.EvidenceUnavailableError) as caught:
                rtc._run_read_command(["git", "rev-parse", "HEAD"], ROOT)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_allowed_gh_nonzero_returns_exit_3(self):
        completed = subprocess.CompletedProcess([], 1, "", "unavailable")
        with mock.patch.object(rtc.subprocess, "run", return_value=completed):
            with self.assertRaises(rtc.EvidenceUnavailableError):
                rtc._run_read_command(["gh", "issue", "view", "49", "--repo", rtc.EXPECTED_REPOSITORY, "--json", "number"], ROOT)

    def test_allowed_live_json_malformed_returns_exit_3(self):
        with mock.patch.object(rtc, "_run_read_command", return_value=("{", {})):
            with self.assertRaises(rtc.EvidenceUnavailableError):
                rtc._json_command(["git", "rev-parse", "HEAD"], ROOT, [])

    def test_live_output_bound_exceeded_returns_exit_3(self):
        completed = subprocess.CompletedProcess([], 0, "x" * (rtc.MAX_COMMAND_OUTPUT_BYTES + 1), "")
        with mock.patch.object(rtc.subprocess, "run", return_value=completed):
            with self.assertRaises(rtc.EvidenceUnavailableError):
                rtc._run_read_command(["git", "rev-parse", "HEAD"], ROOT)

    def test_command_allowlist_rejection_remains_exit_5(self):
        with self.assertRaises(rtc.CommandRejectedError) as caught:
            rtc._run_read_command(["git", "push"], ROOT)
        self.assertEqual(caught.exception.exit_code, 5)

    def test_malformed_fixture_json_remains_exit_5(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "bad.json"
            path.write_text("{", encoding="utf-8")
            with self.assertRaises(rtc.CollectorError) as caught:
                rtc._load_fixture(path)
        self.assertEqual(caught.exception.exit_code, 5)

    def test_approval_unavailable_remains_exit_3(self):
        self.assertEqual(rtc.ApprovalEvidenceUnavailableError.exit_code, 3)

    def test_nonexistent_repo_descendant_is_rejected_before_creation(self):
        candidate = ROOT / ".c3-test-output" / "a" / "b"
        self.assertFalse(candidate.parent.parent.exists())
        with self.assertRaises(rtc.UnsafeEvidenceError):
            rtc._validate_output_dir(candidate, ROOT)
        self.assertFalse(candidate.parent.parent.exists())

    def test_nested_repo_descendant_creates_no_parent(self):
        candidate = ROOT / ".c3-test-output-two" / "nested"
        with self.assertRaises(rtc.UnsafeEvidenceError):
            rtc._validate_output_dir(candidate, ROOT)
        self.assertFalse(ROOT.joinpath(".c3-test-output-two").exists())

    def test_existing_repo_output_dir_is_rejected(self):
        with self.assertRaises(rtc.UnsafeEvidenceError):
            rtc._validate_output_dir(ROOT, ROOT)

    def test_symlink_output_dir_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            real = base / "real"
            real.mkdir()
            link = base / "link"
            link.symlink_to(real, target_is_directory=True)
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc._validate_output_dir(link, ROOT)

    def test_symlink_ancestor_into_repo_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            link = Path(temporary) / "repo"
            link.symlink_to(ROOT, target_is_directory=True)
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc._validate_output_dir(link / ".c3-child", ROOT)
            self.assertFalse((ROOT / ".c3-child").exists())

    def test_external_nonexistent_output_dir_is_created_after_preflight(self):
        with tempfile.TemporaryDirectory() as temporary:
            candidate = Path(temporary) / "new" / "nested"
            self.assertEqual(rtc._validate_output_dir(candidate, ROOT), candidate.resolve())
            self.assertTrue(candidate.is_dir())

    def test_existing_target_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / rtc.OUTPUT_NAMES[0]
            target.symlink_to(Path(temporary) / "elsewhere")
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc._validate_output_dir(Path(temporary), ROOT)

    def test_existing_non_regular_target_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / rtc.OUTPUT_NAMES[0]
            target.mkdir()
            with self.assertRaises(rtc.UnsafeEvidenceError):
                rtc._validate_output_dir(Path(temporary), ROOT)

    def test_rejected_output_creates_no_temporary_file(self):
        candidate = ROOT / ".c3-test-output-three"
        with self.assertRaises(rtc.UnsafeEvidenceError):
            rtc._validate_output_dir(candidate, ROOT)
        self.assertFalse(candidate.exists())

    def test_atomic_write_cleans_temporary_file_on_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "result"
            with mock.patch.object(rtc.os, "replace", side_effect=OSError("failure")):
                with self.assertRaises(OSError):
                    rtc._atomic_write(path, "content")
            self.assertEqual(list(Path(temporary).iterdir()), [])

    def test_active_missing_marker_matrix_remains_pending(self):
        code, evidence, _ = self.classify(self.active())
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))

    def test_active_approved_workflow_without_human_approval_remains_pending(self):
        data = self.approved_workflow(self.active())
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))

    def test_externally_approved_does_not_require_human_approval(self):
        data = self.approved_workflow(self.active())
        data["lifecycle_claim"] = "externally_approved"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))
        self.assertIn("Human/write-access approval is pending", evidence["blockers"])

    def test_merge_ready_requires_qualified_human_approval(self):
        data = self.approved_workflow(self.active())
        data["lifecycle_claim"] = "merge_ready"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))

    def test_merge_ready_accepts_complete_separated_evidence(self):
        data = self.add_approval(self.approved_workflow(self.active()))
        data["lifecycle_claim"] = "merge_ready"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))

    def test_draft_pr_cannot_be_merge_ready(self):
        data = self.add_approval(self.approved_workflow(self.active()))
        data["lifecycle_claim"] = "merge_ready"
        data["pr"]["draft"] = True
        self.assertEqual(self.classify(data)[0], 2)

    def test_auto_merge_active_is_quarantined(self):
        data = self.active()
        data["auto_merge"]["active"] = True
        self.assertEqual(self.classify(data)[0], 2)

    def test_closed_gate_requires_merged_at(self):
        data = fixture("consistent_closed_gate.json")
        data["pr"]["merged_at"] = None
        self.assertEqual(self.classify(data)[0], 2)

    def test_closed_gate_requires_completed_issue_reason(self):
        data = fixture("consistent_closed_gate.json")
        data["issue"]["state_reason"] = "not_planned"
        self.assertEqual(self.classify(data)[0], 2)

    def test_closed_gate_requires_merge_commit_at_verified_main(self):
        data = fixture("consistent_closed_gate.json")
        data["pr"]["merge_commit"] = "d" * 40
        self.assertEqual(self.classify(data)[0], 2)

    def test_closed_issue_before_merge_is_quarantined(self):
        data = self.active()
        data["issue"].update({"state": "closed", "state_reason": "completed", "closeout_state": "closed"})
        self.assertEqual(self.classify(data)[0], 2)

    def test_merged_pr_with_incomplete_closeout_is_quarantined(self):
        data = fixture("consistent_closed_gate.json")
        data["issue"].update({"state": "open", "state_reason": None, "closeout_state": "open"})
        self.assertEqual(self.classify(data)[0], 2)

    def test_complete_closed_gate_is_consistent(self):
        code, evidence, _ = self.classify(fixture("consistent_closed_gate.json"))
        self.assertEqual((code, evidence["consistency_classification"]), (0, "consistent"))

    def test_lifecycle_findings_are_deterministically_sorted(self):
        data = self.active()
        data["repository"].update({"root_verified": False, "remote_verified": False})
        _, evidence, _ = self.classify(data)
        self.assertEqual(evidence["comparison_findings"], sorted(evidence["comparison_findings"]))

    def test_response_layout_keeps_product_stage(self):
        self.assertIn("`Product development stage`", RED_TEAM_PROTOCOL.read_text(encoding="utf-8"))

    def test_response_layout_keeps_current_lifecycle_table(self):
        text = RED_TEAM_PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("`Current lifecycle`", text)
        self.assertIn("one compact Markdown table", text)

    def test_separate_current_readiness_section_is_prohibited(self):  # scope-bound reporting evidence
        self.assertIn("A separate `Current readiness` section or table is prohibited", RED_TEAM_PROTOCOL.read_text(encoding="utf-8"))  # scope-bound reporting evidence

    def test_bottom_chart_requires_delivery_evidence_and_readiness(self):  # scope-bound reporting evidence
        text = RED_TEAM_PROTOCOL.read_text(encoding="utf-8")
        for value in ("`Delivery progress`", "`Evidence confidence`", "`Operational readiness`"):  # scope-bound reporting evidence
            self.assertIn(value, text)

    def test_operational_readiness_cannot_inherit_governance_progress(self):  # scope-bound reporting evidence
        self.assertIn("Operational readiness must not inherit governance-only", RED_TEAM_PROTOCOL.read_text(encoding="utf-8"))  # scope-bound reporting evidence

    def test_nothing_may_follow_the_chart(self):
        self.assertIn("Nothing may appear after the chart or fallback table", RED_TEAM_PROTOCOL.read_text(encoding="utf-8"))

    def test_unsupported_chart_uses_one_combined_bottom_fallback(self):
        text = RED_TEAM_PROTOCOL.read_text(encoding="utf-8")
        self.assertIn("exactly one compact bottom fallback table", text)
        self.assertIn("INTERACTIVE_CHART=UNSUPPORTED_IN_CURRENT_SURFACE", text)


class FinalStructuralValidationCorrectionTests(unittest.TestCase):
    def active(self):
        return fixture("active_pr_requires_live_verification.json")

    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def assert_invalid(self, mutate):
        data = self.active()
        mutate(data)
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(rtc.CollectorError) as caught:
                rtc.generate(data, OBSERVED_AT, Path(temporary), ROOT)
        self.assertEqual(caught.exception.exit_code, 5)

    def assert_cli_invalid(self, mutate):
        data = self.active()
        mutate(data)
        with tempfile.TemporaryDirectory() as temporary:
            fixture_path = Path(temporary) / "fixture.json"
            fixture_path.write_text(json.dumps(data), encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch("sys.stderr", stderr):
                code = rtc.main(
                    [
                        "fixture", "--fixture", str(fixture_path), "--observed-at", OBSERVED_AT,
                        "--output-dir", str(Path(temporary) / "output"),
                    ]
                )
        self.assertEqual(code, 5)
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_missing_live_repository_name_is_blocked_exit_3(self):
        repo = {"defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError) as caught:
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_malformed_live_repository_name_is_blocked_exit_3(self):
        repo = {"nameWithOwner": "malformed", "defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        with self.assertRaises(rtc.EvidenceUnavailableError) as caught:
            rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)
        self.assertEqual(caught.exception.exit_code, 3)

    def test_valid_wrong_live_repository_name_is_not_unavailable(self):
        repo = {"nameWithOwner": "Other/repository", "defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        self.assertEqual(rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)[0], "Other/repository")

    def test_valid_wrong_live_repository_name_is_quarantined_exit_2(self):
        data = self.active()
        data["repository"]["name"] = "Other/repository"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"], evidence["quarantine"]), (2, "quarantined", True))

    def test_valid_wrong_live_repository_reaches_compare_identity_check(self):
        data = self.active()
        data["repository"]["name"] = "Other/repository"
        with mock.patch.object(rtc, "_compare", wraps=rtc._compare) as compared:
            self.classify(data)
        compared.assert_called_once()

    def test_live_repository_identity_never_falls_back_to_requested_name(self):
        repo = {"nameWithOwner": "Other/repository", "defaultBranchRef": {"name": "main", "target": {"oid": "a" * 40}}}
        observed, _, _ = rtc._validate_live_repository(repo, rtc.EXPECTED_REPOSITORY)
        self.assertNotEqual(observed, rtc.EXPECTED_REPOSITORY)

    def test_checks_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data.__setitem__("checks", {}))

    def test_check_item_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data.__setitem__("checks", ["bad"]))

    def test_check_item_missing_name_returns_exit_5(self):
        self.assert_invalid(lambda data: data["checks"][0].pop("name"))

    def test_check_item_unknown_field_returns_exit_5(self):
        self.assert_invalid(lambda data: data["checks"][0].__setitem__("unknown", "bad"))

    def test_workflow_jobs_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"].__setitem__("jobs", {}))

    def test_workflow_job_item_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"].__setitem__("jobs", ["bad"]))

    def test_workflow_job_missing_name_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0].pop("name"))

    def test_workflow_steps_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0].__setitem__("steps", {}))

    def test_workflow_step_item_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0].__setitem__("steps", ["bad"]))

    def test_workflow_step_missing_number_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0]["steps"][0].pop("number"))

    def test_workflow_step_invalid_number_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0]["steps"][0].__setitem__("number", 0))

    def test_workflow_step_unknown_field_returns_exit_5(self):
        self.assert_invalid(lambda data: data["workflow_run"]["jobs"][0]["steps"][0].__setitem__("unknown", "bad"))

    def test_repository_nested_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["repository"].__setitem__("remote_verified", "true"))

    def test_issue_nested_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["issue"].__setitem__("number", "49"))

    def test_pr_nested_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["pr"].__setitem__("draft", 0))

    def test_markers_nested_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data.__setitem__("markers", []))

    def test_auto_merge_active_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data["auto_merge"].__setitem__("active", "false"))

    def test_source_command_item_wrong_type_returns_exit_5(self):
        self.assert_invalid(lambda data: data.__setitem__("source_commands", ["bad"]))

    def test_malformed_check_cli_returns_exit_5_without_traceback(self):
        self.assert_cli_invalid(lambda data: data.__setitem__("checks", ["bad"]))

    def test_malformed_job_cli_returns_exit_5_without_traceback(self):
        self.assert_cli_invalid(lambda data: data["workflow_run"].__setitem__("jobs", ["bad"]))

    def test_malformed_step_cli_returns_exit_5_without_traceback(self):
        self.assert_cli_invalid(lambda data: data["workflow_run"]["jobs"][0].__setitem__("steps", ["bad"]))

    def test_valid_active_fixture_still_requires_live_verification(self):
        code, evidence, _ = self.classify(self.active())
        self.assertEqual((code, evidence["consistency_classification"]), (0, "requires_live_verification"))

    def test_valid_closed_fixture_still_consistent(self):
        code, evidence, _ = self.classify(fixture("consistent_closed_gate.json"))
        self.assertEqual((code, evidence["consistency_classification"]), (0, "consistent"))

    def test_valid_current_workflow_matrix_is_unchanged(self):
        data = self.active()
        evaluation = rtc._control_workflow_evaluation(data)
        self.assertEqual(evaluation, {"blocked": [], "quarantined": []})


class FinalAuthorityBindingScopeC33Tests(unittest.TestCase):
    def active(self):
        return fixture("active_pr_requires_live_verification.json")

    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def assert_quarantined(self, data):
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))
        return evidence

    def live_pr(self):
        return {
            "number": 50, "state": "OPEN", "baseRefName": "main", "headRefName": "collector-branch",
            "headRefOid": ACTIVE_HEAD, "isDraft": False, "mergeCommit": None, "mergedAt": None,
            "autoMergeRequest": None, "reviewDecision": None, "url": "https://example.test/pr/50",
            "author": {"login": "pr-author-scope", "is_bot": False}, "body": "",
        }

    def live_run(self, status="completed", conclusion="failure"):
        return {
            "databaseId": 1, "name": "ContractorOS Control Gates", "workflowDatabaseId": 1,
            "event": "pull_request", "status": status, "conclusion": conclusion,
            "headSha": ACTIVE_HEAD, "headBranch": "collector-branch", "url": "https://example.test/run/1",
        }

    def test_active_local_head_must_equal_pr_head(self):
        data = self.active()
        data["source_shas"]["local_head"] = "d" * 40
        self.assertIn("Local HEAD differs", " ".join(self.assert_quarantined(data)["comparison_findings"]))

    def test_externally_approved_local_head_must_equal_pr_head(self):
        data = self.active()
        data["lifecycle_claim"] = "externally_approved"
        data["source_shas"]["local_head"] = "d" * 40
        self.assert_quarantined(data)

    def test_merge_ready_local_head_must_equal_pr_head(self):
        data = self.active()
        data["lifecycle_claim"] = "merge_ready"
        data["source_shas"]["local_head"] = "d" * 40
        self.assert_quarantined(data)

    def test_changed_default_branch_is_quarantined(self):
        data = self.active()
        data["repository"]["default_branch"] = "trunk"
        self.assert_quarantined(data)

    def test_missing_local_head_is_blocked(self):
        data = self.active()
        data["source_shas"]["local_head"] = None
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (3, "blocked"))

    def test_closed_gate_local_head_must_equal_verified_main(self):
        data = fixture("consistent_closed_gate.json")
        data["source_shas"]["local_head"] = "a" * 40
        self.assert_quarantined(data)

    def test_closed_gate_pr_head_remains_pre_merge_head(self):
        data = fixture("consistent_closed_gate.json")
        self.assertNotEqual(data["pr"]["head"], data["source_shas"]["local_main"])
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (0, "consistent"))

    def test_live_pr_nullable_fields_must_be_present(self):
        fields = ("mergeCommit", "mergedAt", "autoMergeRequest", "reviewDecision")
        for field in fields:
            with self.subTest(field=field):
                value = self.live_pr()
                value.pop(field)
                with self.assertRaises(rtc.EvidenceUnavailableError):
                    rtc._require_live_fields(value, fields, "pull-request")

    def test_empty_auto_merge_request_is_active(self):
        value = self.live_pr()
        value["autoMergeRequest"] = {}
        rtc._validate_live_pr(value)
        self.assertTrue(value["autoMergeRequest"] is not None)

    def test_null_auto_merge_request_is_inactive(self):
        value = self.live_pr()
        rtc._validate_live_pr(value)
        self.assertFalse(value["autoMergeRequest"] is not None)

    def test_malformed_auto_merge_request_is_blocked(self):
        value = self.live_pr()
        value["autoMergeRequest"] = []
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_pr(value)

    def test_completed_workflow_conclusions_must_be_present(self):
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._validate_live_run(self.live_run(conclusion=None))
        jobs = [{"name": "job", "status": "completed", "conclusion": None, "steps": []}]
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._normalized_jobs(jobs)
        jobs = [{"name": "job", "status": "completed", "conclusion": "failure", "steps": [{"name": "step", "number": 1, "status": "completed", "conclusion": None}]}]
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._normalized_jobs(jobs)

    def test_pending_workflow_conclusions_allow_null(self):
        rtc._validate_live_run(self.live_run(status="in_progress", conclusion=None))
        jobs = [{"name": "job", "status": "queued", "conclusion": None, "steps": [{"name": "step", "number": 1, "status": "pending", "conclusion": None}]}]
        self.assertEqual(rtc._normalized_jobs(jobs)[0]["conclusion"], None)

    def test_live_decisive_review_timestamp_is_required_and_valid(self):
        base = {"id": 1, "user": {"login": "reviewer", "type": "User"}, "state": "APPROVED", "commit_id": ACTIVE_HEAD, "author_association": "MEMBER"}  # scope-bound review timestamp evidence
        for timestamp in (None, "not-a-timestamp", 3):
            with self.subTest(timestamp=timestamp):
                value = dict(base, submitted_at=timestamp)
                with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
                    rtc._normalized_review_record(value)

    def test_live_pending_review_allows_null_timestamp(self):
        value = {"id": 1, "user": {"login": "reviewer", "type": "User"}, "state": "PENDING", "submitted_at": None, "commit_id": ACTIVE_HEAD, "author_association": "MEMBER"}  # scope-bound review timestamp evidence
        self.assertIsNone(rtc._normalized_review_record(value)["submitted_at"])

    def test_fixture_invalid_review_timestamp_returns_exit_five_without_traceback(self):
        data = self.active()
        data["review"]["review_records"] = [{"review_id": 1, "reviewer_login": "reviewer", "reviewer_type": "User", "state": "APPROVED", "submitted_at": "invalid", "commit_id": ACTIVE_HEAD, "author_association": "MEMBER"}]  # scope-bound malformed fixture evidence
        with tempfile.TemporaryDirectory() as temporary:
            fixture_path = Path(temporary) / "invalid.json"
            fixture_path.write_text(json.dumps(data), encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch("sys.stderr", stderr):
                code = rtc.main(["fixture", "--fixture", str(fixture_path), "--observed-at", OBSERVED_AT, "--output-dir", str(Path(temporary) / "output")])
        self.assertEqual(code, 5)
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_active_canonical_lifecycle_and_consistency_mismatches_are_visible(self):
        data = self.active()
        data["canonical_state"].update({"lifecycle_state": "other", "consistency_status": "consistent"})
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "stale"))
        self.assertIn("lifecycle", " ".join(evidence["comparison_findings"]).lower())
        self.assertIn("consistency", " ".join(evidence["comparison_findings"]).lower())

    def test_closed_gate_requires_closed_canonical_values(self):
        data = fixture("consistent_closed_gate.json")
        data["canonical_state"].update({"lifecycle_state": "developer_implementation_in_review", "consistency_status": "requires_live_verification"})
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "stale"))

    def test_malformed_canonical_scalars_return_exit_five(self):
        for key, value in (("schema_version", 1), ("schema_version", ""), ("lifecycle_state", 1), ("lifecycle_state", "")):
            with self.subTest(key=key, value=value):
                data = self.active()
                data["canonical_state"][key] = value
                with self.assertRaises(rtc.CollectorError):
                    self.classify(data)


class C34EvidenceHardeningTests(unittest.TestCase):
    def active(self):
        return fixture("active_pr_requires_live_verification.json")

    def classify(self, data):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return rtc.generate(data, OBSERVED_AT, Path(temporary.name), ROOT)

    def assert_fixture_invalid(self, mutate):
        data = self.active()
        mutate(data)
        with self.assertRaises(rtc.CollectorError) as caught:
            self.classify(data)
        self.assertEqual(caught.exception.exit_code, 5)

    def permission_response(self, login="reviewer", account_type="User"):  # scope-bound approval evidence
        return {"permission": "write", "role_name": "write", "user": {"login": login, "type": account_type}}  # scope-bound approval evidence

    def test_permission_response_exact_identity_succeeds(self):
        self.assertEqual(
            rtc._validate_permission_response(self.permission_response(), "reviewer"),
            ("reviewer", "write", "write", "User"),
        )

    def test_permission_response_case_only_identity_is_canonicalized(self):
        self.assertEqual(
            rtc._validate_permission_response(self.permission_response("ReViEwEr"), "reviewer")[0],
            "reviewer",
        )

    def test_permission_response_different_or_missing_identity_blocks(self):
        for response in (self.permission_response("other"), {"permission": "write", "role_name": "write", "user": {"type": "User"}}):
            with self.subTest(response=response):
                with self.assertRaises(rtc.ApprovalEvidenceUnavailableError) as caught:
                    rtc._validate_permission_response(response, "reviewer")
                self.assertEqual(caught.exception.exit_code, 3)

    def test_permission_response_malformed_login_and_unsupported_type_block(self):  # scope-bound approval evidence
        for response in (self.permission_response("bad login"), self.permission_response(account_type="Organization")):  # scope-bound approval evidence
            with self.subTest(response=response):
                with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
                    rtc._validate_permission_response(response, "reviewer")

    def test_permission_identity_mismatch_never_qualifies(self):
        raw = {"id": 1, "user": {"login": "reviewer", "type": "User"}, "state": "APPROVED", "submitted_at": OBSERVED_AT, "commit_id": ACTIVE_HEAD, "author_association": "MEMBER"}  # scope-bound approval evidence
        with mock.patch.object(rtc, "_json_command", side_effect=[[raw], self.permission_response("other")]):
            with self.assertRaises(rtc.ApprovalEvidenceUnavailableError):
                rtc._collect_review_evidence(ROOT, [], ACTIVE_HEAD, "author")  # scope-bound approval evidence

    def test_worktree_clean_header_is_not_a_dirty_entry_and_hash_is_deterministic(self):
        first = rtc._normalized_worktree_status("## collector...origin/collector\n")
        second = rtc._normalized_worktree_status("## collector...origin/collector\n")
        self.assertEqual(first, second)
        self.assertEqual(first["clean"], True)

    def test_worktree_tracked_staged_and_untracked_entries_block(self):
        for status in ("## branch\n M file\n", "## branch\nM  file\n", "## branch\n?? file\n"):
            with self.subTest(status=status):
                before = rtc._normalized_worktree_status(status)
                with self.assertRaises(rtc.EvidenceUnavailableError):
                    rtc._require_clean_unchanged_worktree(before)

    def test_worktree_changed_status_blocks_without_persisting_raw_listing(self):
        before = rtc._normalized_worktree_status("## branch\n")
        after = rtc._normalized_worktree_status("## branch...origin/branch\n")
        with self.assertRaises(rtc.EvidenceUnavailableError):
            rtc._require_clean_unchanged_worktree(before, after)
        data = self.active()
        self.assertNotIn("file", json.dumps(data["source_shas"]))

    def test_review_structure_rejects_exact_key_enum_and_record_failures(self):
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("extra", True))
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("decision", "COMMENTED"))
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("review_records", [{"review_id": 1}]))

    def test_review_structure_rejects_permission_and_claim_failures(self):
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("permission_records", [{"reviewer_login": "reviewer", "permission": "owner", "role_name": "owner", "account_type": "User"}]))  # scope-bound approval evidence
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("qualifying_approvals", ["Reviewer", "reviewer"]))
        self.assert_fixture_invalid(lambda data: data["review"].__setitem__("disqualification_reasons", {"reviewer": ["UNSUPPORTED"]}))

    def test_review_ordering_uses_utc_instant_then_review_id(self):
        earlier_offset = {"submitted_at": "2026-07-13T00:30:00+01:00", "review_id": 2}
        later_zulu = {"submitted_at": "2026-07-13T00:00:00Z", "review_id": 1}
        self.assertLess(rtc._review_sort_key(earlier_offset), rtc._review_sort_key(later_zulu))
        same_instant_low_id = {"submitted_at": "2026-07-13T00:00:00Z", "review_id": 1}
        same_instant_high_id = {"submitted_at": "2026-07-12T19:00:00-05:00", "review_id": 2}
        self.assertLess(rtc._review_sort_key(same_instant_low_id), rtc._review_sort_key(same_instant_high_id))

    def test_live_closed_at_requires_valid_rfc3339(self):
        base = {"number": 49, "state": "OPEN", "stateReason": None, "url": "https://example.test/49", "closedAt": None}
        rtc._validate_live_issue(base)
        for value in ("2026-07-13T00:00:00Z", "2026-07-12T19:00:00-05:00"):
            issue = dict(base, state="CLOSED", closedAt=value)
            rtc._validate_live_issue(issue)
        for value in ("", "not-a-date", "2026-02-30T00:00:00Z", 1):
            with self.subTest(value=value):
                with self.assertRaises(rtc.EvidenceUnavailableError):
                    rtc._validate_live_issue(dict(base, state="CLOSED", closedAt=value))

    def test_closed_gate_base_must_bind_to_verified_default_branch(self):
        data = fixture("consistent_closed_gate.json")
        data["pr"]["base"] = "release"
        code, evidence, _ = self.classify(data)
        self.assertEqual((code, evidence["consistency_classification"]), (2, "quarantined"))


if __name__ == "__main__":
    unittest.main()
