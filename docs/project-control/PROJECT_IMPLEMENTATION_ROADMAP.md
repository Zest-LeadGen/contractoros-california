# ContractorOS Project Implementation Roadmap

## 1. Purpose

Preserve how the full modular app vision is intended to be implemented over time, without allowing premature scope expansion.

This roadmap preserves implementation intent. It does not prove implementation. It does not authorize future modules now. It does not override `PHASE_ONE_SCOPE.md`, `PROJECT_SCOPE_BOUNDARIES.md`, `CLAIM_LEVELS_AND_RELEASE_GATES.md`, or `DEVELOPMENT_CONTROL_MODEL_V3.md`.

## 2. Implementation Principle

Build one fixed app shell.

Do not create multiple disconnected apps.

Do not download executable native code per role.

Future role/module expansion must happen through approved content packs, UI configuration, source registry updates, module manifests, and controlled backend services only after explicit approval.

## 3. One-App Modular Architecture

Long-term ContractorOS California / California TradeOS is intended to use one fixed app shell with role-based modules, role-based downloadable content packs, role-based UI configuration, and versioned updates.

## 4. Fixed App Shell

Future fixed-shell capabilities may include:

- role selector
- module catalog
- quiz engine
- flashcard engine
- source viewer
- update center
- offline content downloads
- settings/support
- admin-controlled configuration

These are future capabilities unless already proven by source, runtime, build, or install evidence.

## 5. Role-Based Module System

Future role/module examples may include:

- C10 Candidate
- C46 Candidate
- C39 Candidate
- Law & Business Candidate
- Commercial Solar / Property Owner
- Solar EPC Operator
- Government Contracting User
- Homeowner Energy User

These are roadmap categories only. They are not current implementation scope.

## 6. Content Pack Strategy

Future modules should use approved content packs, not separate disconnected apps or executable native-code downloads.

Content packs may later include questions, explanations, flashcards, source references, UI labels, and module metadata after content governance approval.

## 7. UI Configuration Strategy

Role-specific UI should be controlled by approved configuration and module manifests after explicit approval.

## 8. Source Registry Strategy

Future source registry work may track official sources, source categories, effective dates, review dates, and content ownership. This is not current runtime scope.

## 9. AI Source-Watch / Update Pipeline

Future update pipeline may include:

- source registry
- source watcher
- AI diff engine
- AI drafting layer
- verification layer
- human approval layer
- versioned publishing
- rollback

This is future/not current scope.

## 10. Human Approval Layer

Human approval remains required before publishing or claiming content/currentness. AI output is not authoritative without review.

## 11. Versioned Publishing and Rollback

Future publishing should use versioned content, auditable approvals, and rollback paths. No publishing system exists until approved and implemented.

## 12. Security / Backend Future Architecture

Future backend/security architecture may include:

- Firebase Auth
- Firestore
- Cloud Storage
- Cloud Functions
- Remote Config
- App Check
- Crashlytics
- Analytics
- Test Lab
- signed content manifests
- role-based access control
- admin-only publishing
- audit logs

These are not current Phase One scope.

## 13. Offline Download Strategy

Future offline downloads should use approved signed content packs and version tracking. No offline download system is currently approved by this roadmap.

## 14. Testing Strategy

Future gates may include:

- source inspection
- citation validation
- question validation
- role-switching tests
- offline-download tests
- Firestore/security-rules tests if backend approved
- visual QA
- device/emulator QA
- Firebase Test Lab if approved
- build artifact gate
- install test gate

## 15. Tooling Strategy

Tooling should support evidence, auditability, and controlled publishing. Tooling does not replace human approval or red-team review.

## 16. Phase-Based Implementation Sequence

- Phase One: internal scaffold and control foundation
- Next product phase: return to mobile/web internal UX and QA work
- Later: content governance
- Later: visual QA
- Later: dependency control
- Later: backend/security design only when approved
- Later: module/content pack implementation only when approved
- Later: build/distribution only when approved

## 17. Blocked Until Explicit Approval

Future modules, backend, Firebase, auth, scoring, readiness, public content, APK, EAS, deployment, and production claims remain blocked until explicit approval and evidence gates.

## 18. Current Phase Constraint

Current Phase 4E work is documentation/control only. It does not change app source, dependencies, packages, build, runtime, backend, or public content.

## 19. Final Rule

Implementation intent is not implementation proof.

Roadmap categories are not approved scope.

Verified GitHub evidence controls the claim level.
