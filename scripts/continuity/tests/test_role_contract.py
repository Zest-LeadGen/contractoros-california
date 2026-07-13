import copy
import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    "role_contract", ROOT / "scripts/continuity/role_contract.py"
)
rc = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(rc)

NOW = "2026-07-13T12:00:00Z"


def valid_contract():
    return rc.red_team_contract(
        repository="Zest-LeadGen/contractoros-california",
        issue=55,
        pull_request=56,
        branch="stage-a-red-team-role-isolation",
        exact_sha="a" * 40,
        lifecycle_state="EXTERNAL_EXACT_SHA_REVIEW",
        authority_source="GITHUB_ISSUE_55",  # scope
        observation_timestamp=NOW,
        program_next_action="External exact-SHA review is next.",
        next_authorized_actor="RED_TEAM",  # scope
        developer_next_action="NONE",
        red_team_next_action="REVIEW_EXACT_SHA",
        human_approver_next_action="NONE",
        merge_operator_next_action="NONE",
        requested_action_class="EXACT_SHA_REVIEW",
    )


def expected(contract=None):
    contract = contract or valid_contract()
    value = {key: contract[key] for key in rc.EXPECTED_KEYS if key != "CURRENT_TIME"}
    value["CURRENT_TIME"] = NOW
    return value


class RoleContractValidationTests(unittest.TestCase):
    def classify(self, contract=None, context=None, repair=False):
        contract = valid_contract() if contract is None else contract
        context = expected(contract) if context is None else context
        return rc.validate_role_contract(contract, context, repair=repair)

    def assert_denied(self, result, reason=None):
        self.assertFalse(result["valid"])
        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["role_conflict_status"], "ROLE_CONFLICT")
        if reason:
            self.assertIn(reason, result["reasons"])

    def test_valid_red_team_role_declaration_passes(self):
        result = self.classify()
        self.assertTrue(result["valid"])
        self.assertEqual(result["actor_role"], "RED_TEAM")
        self.assertEqual(result["role_repair_state"], "NORMAL")

    def test_missing_role_declaration_fails(self):
        contract = valid_contract()
        del contract["ROLE"]
        self.assert_denied(self.classify(contract, expected()), "MISSING_GOVERNING_KEY")

    def test_missing_actor_identity_fails(self):
        contract = valid_contract()
        contract["ACTOR_ROLE"] = ""
        contract["ROLE"] = ""
        self.assert_denied(self.classify(contract, expected()), "MISSING_ACTOR_IDENTITY")

    def test_unknown_actor_fails(self):
        contract = valid_contract()
        contract["ACTOR_ROLE"] = "ROGUE"
        contract["ROLE"] = "ROGUE"
        result = self.classify(contract, expected())
        self.assert_denied(result, "UNKNOWN_ACTOR_IDENTITY")
        self.assertEqual(result["actor_role"], "UNKNOWN")

    def test_actor_and_role_must_match(self):
        contract = valid_contract()
        contract["ROLE"] = "CODEX_DEVELOPER"
        self.assert_denied(self.classify(contract), "ROLE_IDENTITY_MISMATCH")

    def test_unknown_governing_key_fails(self):
        contract = valid_contract()
        contract["EXTRA"] = "NO"
        self.assert_denied(self.classify(contract), "UNKNOWN_GOVERNING_KEY")

    def test_missing_governing_key_fails(self):
        contract = valid_contract()
        del contract["BRANCH"]
        self.assert_denied(self.classify(contract, expected()), "MISSING_GOVERNING_KEY")

    def test_duplicate_governing_actor_field_fails(self):
        contract = valid_contract()
        result = rc.validate_role_contract_pairs(
            [*contract.items(), ("ACTOR_ROLE", "CODEX_DEVELOPER")], expected(contract)
        )
        self.assert_denied(result, "DUPLICATE_GOVERNING_FIELD")

    def test_developer_action_assigned_to_red_team_fails(self):
        contract = valid_contract()
        contract["RED_TEAM_NEXT_ACTION"] = "IMPLEMENT_ISSUE_55_STAGE_A"
        self.assert_denied(self.classify(contract), "INVALID_ACTOR_NEXT_ACTION")

    def test_program_next_action_never_becomes_actor_authority(self):  # scope
        contract = valid_contract()
        contract["PROGRAM_NEXT_ACTION"] = contract["RED_TEAM_NEXT_ACTION"]
        result = self.classify(contract)
        self.assert_denied(result, "PROGRAM_ACTION_IS_NOT_ACTOR_AUTHORITY")  # scope
        self.assertFalse(result["program_next_action_is_authority"])  # scope

    def test_prompt_authoring_remains_allowed_for_red_team(self):  # scope
        contract = valid_contract()
        contract["PROGRAM_NEXT_ACTION"] = "A separate developer may implement the bounded issue."
        contract["RED_TEAM_NEXT_ACTION"] = "AUTHOR_BOUNDED_DEVELOPER_PROMPT"  # scope
        contract["REQUESTED_ACTION_CLASS"] = "PROMPT_AUTHORING"  # scope
        result = self.classify(contract)
        self.assertTrue(result["valid"])
        self.assertEqual(result["decision"], "ALLOW")

    def test_exact_sha_review_remains_allowed_for_red_team(self):
        self.assertTrue(self.classify()["valid"])

    def test_implementation_remains_prohibited_for_red_team(self):
        contract = valid_contract()
        contract["REQUESTED_ACTION_CLASS"] = "IMPLEMENTATION"
        self.assert_denied(self.classify(contract), "RED_TEAM_ACTION_NOT_AUTHORIZED")  # scope

    def test_all_red_team_mutation_classes_are_denied(self):
        prohibited = rc.ACTION_CLASSES - rc.RED_TEAM_ALLOWED_ACTION_CLASSES
        for action in sorted(prohibited):
            with self.subTest(action=action):
                contract = valid_contract()
                contract["REQUESTED_ACTION_CLASS"] = action
                result = self.classify(contract)
                self.assert_denied(result, "RED_TEAM_ACTION_NOT_AUTHORIZED")  # scope
                self.assertEqual(result["incident"]["requested_action_class"], action)

    def test_contradictory_authority_fields_fail(self):  # scope
        contradictions = {
            "DEVELOPER_ROLE": "SELF",
            "REPOSITORY_WRITE_AUTHORITY": "BOUNDED",  # scope
            "GITHUB_WRITE_AUTHORITY": "PR_ONLY",  # scope
            "TERMINAL_MUTATION_AUTHORITY": "BOUNDED",  # scope
            "IMPLEMENTATION_AUTHORITY": "YES",  # scope
            "PROMPT_AUTHORING_AUTHORITY": "NO",  # scope
            "EXACT_SHA_REVIEW_AUTHORITY": "NO",  # scope
            "HUMAN_APPROVAL_AUTHORITY": "YES",  # scope
            "MERGE_AUTHORITY": "YES",  # scope
            "ISSUE_CLOSEOUT_AUTHORITY": "YES",  # scope
        }
        for field, value in contradictions.items():
            with self.subTest(field=field):
                contract = valid_contract()
                contract[field] = value
                self.assert_denied(self.classify(contract), f"CONTRADICTORY_{field}")

    def test_invalid_binding_shapes_fail(self):
        invalid = {
            "REPOSITORY": "not-a-repository",
            "ISSUE": True,
            "PULL_REQUEST": 0,
            "BRANCH": "bad branch",
            "EXACT_SHA": "A" * 40,
            "LIFECYCLE_STATE": "UNKNOWN",
            "AUTHORITY_SOURCE": "CHAT",  # scope
        }
        for field, value in invalid.items():
            with self.subTest(field=field):
                contract = valid_contract()
                contract[field] = value
                self.assert_denied(self.classify(contract, expected()))

    def test_missing_authority_source_fails_closed(self):  # scope
        contract = valid_contract()
        contract["AUTHORITY_SOURCE"] = ""  # scope
        self.assert_denied(self.classify(contract, expected()), "MISSING_AUTHORITY_SOURCE")  # scope

    def test_stale_bindings_fail_closed(self):
        changes = {
            "REPOSITORY": "Other/repository",
            "ISSUE": 54,
            "PULL_REQUEST": 57,
            "BRANCH": "other-branch",
            "EXACT_SHA": "b" * 40,
            "LIFECYCLE_STATE": "HUMAN_APPROVAL_PENDING",
            "AUTHORITY_SOURCE": "VERSIONED_PROJECT_CONTROL",  # scope
        }
        reason_names = {
            "REPOSITORY": "STALE_REPOSITORY_BINDING",
            "ISSUE": "STALE_ISSUE_BINDING",
            "PULL_REQUEST": "STALE_PULL_REQUEST_BINDING",
            "BRANCH": "STALE_BRANCH_BINDING",
            "EXACT_SHA": "STALE_EXACT_SHA_BINDING",
            "LIFECYCLE_STATE": "STALE_LIFECYCLE_BINDING",
            "AUTHORITY_SOURCE": "STALE_AUTHORITY_SOURCE_BINDING",  # scope
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                contract = valid_contract()
                contract[field] = value
                self.assert_denied(self.classify(contract, expected()), reason_names[field])

    def test_stale_observation_timestamp_fails(self):
        contract = valid_contract()
        contract["OBSERVATION_TIMESTAMP"] = "2026-07-13T10:00:00Z"
        self.assert_denied(self.classify(contract), "STALE_OBSERVATION_TIMESTAMP")

    def test_future_observation_timestamp_fails(self):
        contract = valid_contract()
        contract["OBSERVATION_TIMESTAMP"] = "2026-07-13T12:10:00Z"
        self.assert_denied(self.classify(contract), "FUTURE_OBSERVATION_TIMESTAMP")

    def test_malformed_observation_timestamp_fails(self):
        contract = valid_contract()
        contract["OBSERVATION_TIMESTAMP"] = "not-time"
        self.assert_denied(self.classify(contract), "INVALID_OBSERVATION_TIMESTAMP")

    def test_exactly_one_bounded_next_action_is_present_for_each_actor(self):
        result = self.classify()
        self.assertEqual(set(result["next_actions"]), set(rc.ACTORS))
        self.assertEqual(result["next_actions"]["RED_TEAM"], "REVIEW_EXACT_SHA")
        self.assertEqual(
            [actor for actor, action in result["next_actions"].items() if action != "NONE"],
            ["RED_TEAM"],
        )

    def test_none_is_used_when_no_actor_action_is_authorized(self):  # scope
        contract = valid_contract()
        contract.update(
            {
                "NEXT_AUTHORIZED_ACTOR": "NONE",  # scope
                "RED_TEAM_NEXT_ACTION": "NONE",
                "REQUESTED_ACTION_CLASS": "NONE",
            }
        )
        result = self.classify(contract)
        self.assertTrue(result["valid"])
        self.assertEqual(set(result["next_actions"].values()), {"NONE"})

    def test_multiple_actor_actions_fail_closed(self):
        contract = valid_contract()
        contract["DEVELOPER_NEXT_ACTION"] = "CORRECT_ISSUE_55_PR"
        self.assert_denied(self.classify(contract), "AMBIGUOUS_ACTOR_NEXT_ACTION")

    def test_invalid_program_next_action_is_bounded(self):
        contract = valid_contract()
        contract["PROGRAM_NEXT_ACTION"] = "x" * (rc.MAX_TEXT_LENGTH + 1)
        self.assert_denied(self.classify(contract), "INVALID_PROGRAM_NEXT_ACTION")

    def test_role_repair_restores_only_read_only_red_team_profile(self):
        contract = valid_contract()
        contract.update(
            {
                "REPOSITORY_WRITE_AUTHORITY": "BOUNDED",  # scope
                "GITHUB_WRITE_AUTHORITY": "PR_ONLY",  # scope
                "TERMINAL_MUTATION_AUTHORITY": "BOUNDED",  # scope
                "IMPLEMENTATION_AUTHORITY": "YES",  # scope
                "HUMAN_APPROVAL_AUTHORITY": "YES",  # scope
                "MERGE_AUTHORITY": "YES",  # scope
                "ISSUE_CLOSEOUT_AUTHORITY": "YES",  # scope
                "REQUESTED_ACTION_CLASS": "REPOSITORY_MUTATION",
            }
        )
        result = self.classify(contract, repair=True)
        self.assertFalse(result["valid"])
        self.assertEqual(result["role_repair_state"], "READ_ONLY_ROLE_RESTORED")
        for field in (
            "REPOSITORY_WRITE_AUTHORITY",  # scope
            "GITHUB_WRITE_AUTHORITY",  # scope
            "TERMINAL_MUTATION_AUTHORITY",  # scope
        ):
            self.assertEqual(result["effective_authority"][field], "NONE")  # scope
        for field in (
            "IMPLEMENTATION_AUTHORITY",  # scope
            "HUMAN_APPROVAL_AUTHORITY",  # scope
            "MERGE_AUTHORITY",  # scope
            "ISSUE_CLOSEOUT_AUTHORITY",  # scope
        ):
            self.assertEqual(result["effective_authority"][field], "NO")  # scope
        self.assertIsNotNone(result["incident"])

    def test_repair_does_not_erase_conflict_reasons(self):
        contract = valid_contract()
        contract["IMPLEMENTATION_AUTHORITY"] = "YES"  # scope
        original = self.classify(contract)
        repaired = self.classify(contract, repair=True)
        self.assertEqual(original["reasons"], repaired["reasons"])

    def test_mutation_attempt_creates_public_safe_incident(self):
        contract = valid_contract()
        contract["REQUESTED_ACTION_CLASS"] = "GITHUB_MUTATION"
        incident = self.classify(contract)["incident"]
        self.assertEqual(
            set(incident),
            {
                "actor",
                "observation_timestamp",
                "requested_action_class",
                "lifecycle_state",
                "authority_source",  # scope
                "result",
                "denial_reasons",
                "required_repair_state",
            },
        )
        self.assertEqual(incident["result"], "DENIED")

    def test_incident_excludes_private_and_secret_looking_input(self):
        for private in (
            "/Users/example/private/repository",
            "api_key=secret-value",
            "authorization: bearer value",  # scope
            "chain_of_thought=private",
        ):
            with self.subTest(private=private):
                contract = valid_contract()
                contract["PROGRAM_NEXT_ACTION"] = private
                contract["REQUESTED_ACTION_CLASS"] = "REPOSITORY_MUTATION"
                result = self.classify(contract)
                self.assert_denied(result, "UNSAFE_PRIVATE_INPUT")
                rendered = rc.canonical_json(result)
                self.assertNotIn(private, rendered)
                self.assertNotIn("secret-value", rendered)

    def test_review_approval_merge_and_closeout_authorities_remain_separate(self):  # scope
        result = self.classify()
        authority = result["effective_authority"]  # scope
        self.assertEqual(authority["EXACT_SHA_REVIEW_AUTHORITY"], "YES")  # scope
        self.assertEqual(authority["HUMAN_APPROVAL_AUTHORITY"], "NO")  # scope
        self.assertEqual(authority["MERGE_AUTHORITY"], "NO")  # scope
        self.assertEqual(authority["ISSUE_CLOSEOUT_AUTHORITY"], "NO")  # scope

    def test_permission_or_account_ownership_is_not_a_governing_key(self):
        contract = valid_contract()
        contract["REPOSITORY_PERMISSION"] = "ADMIN"
        self.assert_denied(self.classify(contract), "UNKNOWN_GOVERNING_KEY")

    def test_identical_inputs_produce_byte_identical_json(self):
        first = rc.canonical_json(self.classify())
        second = rc.canonical_json(self.classify())
        self.assertEqual(first.encode(), second.encode())

    def test_actor_contract_change_alters_json(self):
        first = rc.canonical_json(self.classify())
        contract = valid_contract()
        contract["PROGRAM_NEXT_ACTION"] = "A separate developer may receive a bounded prompt."
        contract["RED_TEAM_NEXT_ACTION"] = "AUTHOR_BOUNDED_DEVELOPER_PROMPT"  # scope
        contract["REQUESTED_ACTION_CLASS"] = "PROMPT_AUTHORING"  # scope
        second = rc.canonical_json(self.classify(contract))
        self.assertNotEqual(first, second)

    def test_conflict_reason_order_is_stable(self):
        contract = valid_contract()
        contract["IMPLEMENTATION_AUTHORITY"] = "YES"  # scope
        contract["MERGE_AUTHORITY"] = "YES"  # scope
        contract["REQUESTED_ACTION_CLASS"] = "MERGE"
        first = self.classify(contract)["reasons"]
        second = self.classify(copy.deepcopy(contract))["reasons"]
        self.assertEqual(first, second)
        self.assertEqual(first, rc._ordered_reasons(first))

    def test_repair_reason_order_is_stable(self):
        contract = valid_contract()
        contract["REPOSITORY_WRITE_AUTHORITY"] = "BOUNDED"  # scope
        contract["REQUESTED_ACTION_CLASS"] = "REPOSITORY_MUTATION"
        first = self.classify(contract, repair=True)["reasons"]
        second = self.classify(copy.deepcopy(contract), repair=True)["reasons"]
        self.assertEqual(first, second)

    def test_output_contains_only_json_compatible_values(self):
        json.loads(json.dumps(self.classify()))

    def test_bounded_stage_a_claim_is_explicit(self):
        claim = self.classify()["bounded_claim"]
        self.assertEqual(claim["actor_bound_role_contract"], "IMPLEMENTED_IN_REVIEW")
        self.assertEqual(claim["full_runtime_isolation"], "NOT_PROVEN")
        self.assertEqual(claim["stage_b_required"], "YES")


class RoleContractCliTests(unittest.TestCase):
    def test_self_test_passes(self):
        stream = io.StringIO()
        with redirect_stdout(stream):
            code = rc.main(["--self-test"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(stream.getvalue())["result"], "PASS")

    def test_malformed_input_returns_documented_result_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary:
            contract = Path(temporary) / "contract.json"
            context = Path(temporary) / "expected.json"
            contract.write_text("{", encoding="utf-8")
            context.write_text("{}", encoding="utf-8")
            stdout = io.StringIO()
            stderr = io.StringIO()
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = rc.main(["--contract", str(contract), "--expected", str(context)])
        self.assertEqual(code, 5)
        self.assertEqual(json.loads(stdout.getvalue())["error"], "INVALID_INPUT")
        self.assertNotIn("Traceback", stdout.getvalue() + stderr.getvalue())

    def test_valid_cli_input_is_deterministic(self):
        contract_value = valid_contract()
        expected_value = expected(contract_value)
        with tempfile.TemporaryDirectory() as temporary:
            contract = Path(temporary) / "contract.json"
            context = Path(temporary) / "expected.json"
            contract.write_text(json.dumps(contract_value), encoding="utf-8")
            context.write_text(json.dumps(expected_value), encoding="utf-8")
            outputs = []
            for _ in range(2):
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    code = rc.main(["--contract", str(contract), "--expected", str(context)])
                self.assertEqual(code, 0)
                outputs.append(stdout.getvalue())
        self.assertEqual(outputs[0], outputs[1])


if __name__ == "__main__":
    unittest.main()
