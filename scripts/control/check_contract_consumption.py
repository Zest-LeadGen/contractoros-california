#!/usr/bin/env python3
"""H1-B1B-P contract-consumption check.

Validates the governance-contract pin file: structure, required fields,
exact-SHA and digest formats, and prohibition flags. With --live, also
re-fetches each pinned blob (read-only scope) from the pinned governance commit and compares
its SHA-256 digest, failing closed on any mismatch or fetch failure (read-only scope).

Read-only. Exit 0 = PASS, exit 1 = validation failure, exit 2 = environment
failure in --live mode (fail closed; no fallback).
"""
import argparse
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIN = ROOT / "docs/project-control/state/governance-contract-pin.json"

REQUIRED_ROLES = {
    "OUTPUT_CONTRACT",
    "PROMPT_CONTRACT",
    "DEVELOPER_CONTRACT",
    "RED_TEAM_CONTRACT",
    "CONTRACTS_SCHEMA",
}
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA64 = re.compile(r"^[0-9a-f]{64}$")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true",
                        help="re-fetch pinned blobs and verify digests (read-only scope)")
    args = parser.parse_args()

    failures = []

    if not PIN.exists():
        print("FAIL:\n- pin file missing: docs/project-control/state/governance-contract-pin.json")
        return 1
    try:
        pin = json.loads(PIN.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"FAIL:\n- pin parse failure: {exc}")
        return 1

    if pin.get("pin_semantics") != "exact_sha_and_digest_consumption_no_parallel_format":
        failures.append("pin_semantics must declare no-parallel-format consumption")
    repo = pin.get("source_repository", "")
    if repo != "Zest-ContractorOS/contractoros-governance":
        failures.append(f"unexpected source repository: {repo!r}")
    sha = pin.get("pinned_main_sha", "")
    if not SHA40.fullmatch(sha):
        failures.append("pinned_main_sha must be a 40-hex commit SHA")

    contracts = pin.get("contracts", [])
    roles = {c.get("role") for c in contracts}
    if roles != REQUIRED_ROLES:
        failures.append(f"contract roles mismatch: missing {sorted(REQUIRED_ROLES - roles)}, unexpected {sorted(roles - REQUIRED_ROLES)}")
    for c in contracts:
        if not c.get("path", "").startswith(("policy/contracts/", "schemas/contracts/")):
            failures.append(f"unexpected contract path: {c.get('path')!r}")
        if not SHA64.fullmatch(c.get("sha256", "")):
            failures.append(f"invalid sha256 for {c.get('role', '?')}")

    rules = pin.get("consumption_rules", {})
    for key in ("parallel_format_creation", "contract_text_duplication"):
        if rules.get(key) != "PROHIBITED":
            failures.append(f"consumption_rules.{key} must be PROHIBITED")
    if rules.get("pin_update_control") != "OWNER_DECISION_REQUIRED":
        failures.append("consumption_rules.pin_update_control must be OWNER_DECISION_REQUIRED")

    live_results = []
    if args.live and not failures:
        for c in contracts:
            url = f"https://raw.githubusercontent.com/{repo}/{sha}/{c['path']}"
            try:
                with urllib.request.urlopen(url, timeout=30) as resp:
                    data = resp.read()
            except Exception as exc:
                path = c["path"]
                print(f"ENVIRONMENT_FAILURE:\n- fetch failed, no fallback path exists, for {path}: {exc}")
                return 2
            digest = hashlib.sha256(data).hexdigest()
            match = digest == c["sha256"]
            live_results.append({"path": c["path"], "match": match})
            if not match:
                failures.append(f"LIVE DIGEST MISMATCH: {c['path']} expected {c['sha256'][:12]}… got {digest[:12]}…")

    if failures:
        print("FAIL:")
        for item in failures:
            print(f"- {item}")
        return 1

    mode = "live-digest" if args.live else "structural"
    print(f"Pinned: {repo}@{sha[:7]} corpus_version={pin.get('corpus_version')}")
    if live_results:
        for r in live_results:
            print(f"- {r['path']}: digest MATCH")
    print(f"PASS: contract-consumption {mode} check completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
