# Documentation Maintenance Protocol

## Purpose

Define how ContractorOS documentation and control files stay synchronized with development.

Anchors do not maintain themselves.
Every PR must declare documentation impact.
No paperwork impact = documented no-op, not silence.

## Protocol

1. Identify what changed.
2. Classify the phase lane.
3. Check the machine-readable matrix.
4. Update required control files.
5. Mark non-applicable files as reviewed/no-update-required.
6. Run the control gate.
7. Red-team verifies documentation impact.
8. No merge approval unless paperwork impact is resolved.

## Control Gate Commands

```bash
python3 scripts/control/check_changed_files.py
python3 scripts/control/check_forbidden_scope.py
python3 scripts/control/check_required_control_updates.py
python3 scripts/control/check_pr_contract.py
```

## Enforcement Principle

The project does not rely on developer memory for scope discipline. Every PR must carry its own documentation and control evidence.
