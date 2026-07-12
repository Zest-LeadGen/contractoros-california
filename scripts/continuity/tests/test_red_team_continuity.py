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
PROMPT_CONVENTION = ROOT / "docs/project-control/PROMPT_CONVENTION.md"
OPERATING_MODEL = ROOT / "docs/project-control/AI_DEVELOPMENT_OPERATING_MODEL.md"
RED_TEAM_PROTOCOL = ROOT / "docs/project-control/RED_TEAM_OPERATING_PROTOCOL.md"
HANDOFF_PLAYBOOK = ROOT / "docs/project-control/HANDOFF_PLAYBOOK.md"
TRACKER = ROOT / "docs/project-control/PROJECT_VISION_AND_PHASE_TRACKER.md"
SOURCE_REGISTER = ROOT / "docs/project-control/SOURCE_REGISTER.md"
PHASE_REPORT = ROOT / "docs/project-control/phase_pre_4k_9_read_only_red_team_continuity_collector_startup_packet_gate_report.md"


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
