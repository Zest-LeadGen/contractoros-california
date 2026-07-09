# Documentation Maintenance Protocol

## Purpose

Define how ContractorOS documentation and control files stay synchronized with development.

Anchors do not maintain themselves.
Every PR must declare documentation impact.
No paperwork impact = documented no-op, not silence.

## Maintained Automation Route

The approved operating route is:

```text
GitHub Issue → Developer PR → Control Gates → Red-Team Decision → Human Approval → Merge
```

This route exists to reduce owner copy/paste and manual supervision while preserving protected PR governance, red-team accountability, and human approval for major decisions.

The route does not authorize direct-to-main work, automated merge, automated approval, bypassed branch protection, app-store/build release work, backend work, dependency work, or product-scope expansion.

## Companion Report Protocol

A non-control PR may include exactly one current phase report under:

```text
docs/project-control/phase_*_report.md
```

When that report accompanies a Product / QA change, it is treated as companion documentation for the Product / QA lane.

The report must still include all required sections, exact no-update-required markers, command evidence, dependency/lockfile handling, claim level, known limitations, and forbidden-scope confirmation.

Historical phase reports do not satisfy current PR requirements.

Report-only project-control PRs remain Control / Infrastructure.

Non-report project-control changes remain Control / Infrastructure.

## Protocol

1. Identify what changed.
2. Classify the phase lane.
3. Check the machine-readable matrix.
4. Add or update the current phase report.
5. Update required control files.
6. Mark non-applicable required files as reviewed/no-update-required in the current phase report.
7. Run the control gate.
8. Red-team verifies documentation impact.
9. Human approval is required before merge when protected branch rules require it or when the owner requests it.
10. No merge approval unless paperwork impact is resolved.

## Control Gate Commands

```bash
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
python3 scripts/control/check_forbidden_scope.py --lockfiles-only
python3 scripts/control/check_pr_contract.py --claims-only
```

## Enforcement Principle

The project does not rely on developer memory for scope discipline. Every PR must carry its own documentation and control evidence.

The companion report route reduces manual relay work but does not reduce review, approval, or evidence requirements.
