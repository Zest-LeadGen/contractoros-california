# Governance Contract Consumption — H1_B1B_P

```text
GATE=H1_B1B_P
PHASE_ISSUE=99
SOURCE_OF_TRUTH=Zest-ContractorOS/contractoros-governance@e907a76f1297e3541672de2424ed2984b03cf0d1
PIN_FILE=docs/project-control/state/governance-contract-pin.json
CONSUMPTION_CHECK=scripts/control/check_contract_consumption.py
PARALLEL_FORMAT_CREATION=PROHIBITED
```

## Consumption model (H1B1-GATE-006)

The product repository consumes the four provider-neutral AI contracts (output, prompt, developer, red-team) and their closed schema exclusively by exact-SHA pin plus per-file SHA-256 digest. Contract text is never duplicated into this repository, and no parallel response or prompt format may be created here. The pin advances only by owner decision. Verification is the declared live command: `python3 scripts/control/check_contract_consumption.py --live` (documentation scope: fetches each pinned blob at the pinned commit and fail-closes on any digest mismatch).

CI wiring of this check is deliberately deferred to H1_B4 (enforcement cutover) per the gate ladder; until then it is a declared-command control.

## Enforcement boundary record (H1B1-OUT-014)

Official ContractorOS output enforcement is possible only through controlled surfaces. GitHub alone cannot intercept or validate arbitrary private AI chats; committed contracts and status blocks are derived reporting and create no authority over uncontrolled conversations. A later controlled surface — an app, wrapper, CLI, MCP service, or web console performing official pre-display validation against the pinned contracts — is planned but not selected, designed, or built by this record (documentation scope).

## Owner decision records (resolved by the Issue #99 phase authorization)

- **H1B1-OD-011 — controlled official runtime target**: candidate surface classes recorded (CLI wrapper, MCP service, web console); binding selection deferred to the Phase 4K-9 era; no runtime is selected or built now (documentation scope).
- **H1B1-OD-019 — Phase 4K-9 contract-consumption mechanism**: exact governance SHA pin plus per-file digest verification via the pin file of this phase; this is the mechanism H1B1-4K-001 will consume when Phase 4K-9 is separately activated (documentation scope; grants Phase 4K-9 no start authority).
