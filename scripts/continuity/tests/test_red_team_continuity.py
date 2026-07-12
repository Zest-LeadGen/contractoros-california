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


def fixture(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


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


if __name__ == "__main__":
    unittest.main()
