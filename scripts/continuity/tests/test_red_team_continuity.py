import copy
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
        changed["checks"].append({"name": "scope", "state": "SUCCESS", "bucket": "pass"})
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

    def record(self, review_id=10, login="reviewer", state="APPROVED", **overrides):
        value = {
            "review_id": review_id,
            "reviewer_login": login,
            "reviewer_type": "User",
            "state": state,
            "submitted_at": "2026-07-12T22:00:00Z",
            "commit_id": ACTIVE_HEAD,
            "author_association": "MEMBER",
        }
        value.update(overrides)
        return value

    def permission(self, login="reviewer", permission="write", **overrides):
        value = {
            "reviewer_login": login,
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

    def test_pr_author_approval_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(login="pr-author")])
        self.assertIn("APPROVAL_PR_AUTHOR", self.evaluation(data)["review"]["disqualification_reasons"]["pr-author"])

    def test_bot_approval_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(reviewer_type="Bot")])
        self.assertIn("APPROVAL_BOT_ACCOUNT", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

    def test_unsubmitted_review_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(submitted_at=None)])
        self.assertIn("APPROVAL_NOT_SUBMITTED", self.evaluation(data)["review"]["disqualification_reasons"]["reviewer"])

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

    def test_author_association_alone_does_not_qualify(self):
        data = self.set_review(self.data(), [self.record(author_association="OWNER")])
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

    def test_permission_login_mismatch_is_quarantined(self):
        data = self.set_review(self.data(), [self.record()], [self.permission(login="other")])
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
        record = rtc._normalized_review_record({"id": 10, "user": {"login": "reviewer", "type": "User"}, "state": "APPROVED", "submitted_at": OBSERVED_AT, "commit_id": ACTIVE_HEAD, "author_association": "MEMBER", "body": "private prose"})
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

    def test_permission_endpoint_for_unsourced_login_is_rejected(self):
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


if __name__ == "__main__":
    unittest.main()
