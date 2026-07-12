# AI Decision-Power Model And Tool Security

## Documentation Scope

This documentation defines future decision-power and tool controls; it does not implement agents, identities, credentials, production actions, or services.

## Level A — Bounded Autonomous Work

Reversible, deterministic, narrowly scoped preparation where inputs, outputs, changed files, and rollback are testable. Existing phase scope and protected review still apply.

## Level B — Autonomous Preparation With Final Gate

AI may prepare branches, commits, pull requests, drafts and evidence. Consequential writes and release require all mandatory system controls plus protected human/write-access approval under current policy. A system gate does not replace human approval unless a later owner-approved governance amendment explicitly authorizes that change.

## Level C — Supervised High-Impact Evidence

AI may prepare recommendations and evidence packets for legal, security, privacy, financial, architecture, or public-release decisions. A qualified human makes the decision.

## Level D — Prohibited Autonomous Action

AI must not independently give individualized legal advice, make licensing determinations, file regulatory documents, bind the company, accept material security/privacy risk, change payment credentials, change customer-data use, perform irreversible production actions, override branch protection, approve its own work, or conceal uncertainty.

## Tool Security Controls

Future tools require least privilege, strict schemas, separate read/write identities, explicit sensitive-action approval, prompt-injection defenses, source classification, execution traces, rate and cost limits, kill switches, time bounds, idempotency, rollback, and deny-by-default capability grants. Read-only collection is the first permissible implementation target.

## Human And Review Boundaries

Independent red-team review and human/write-access approval remain distinct. AI may create a scoped developer branch, commit, and PR under an approved gate but may not self-review, approve, merge, release, change budgets, manage credentials, or amend governing policy.
