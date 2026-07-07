# Claim Downgrade Matrix

Purpose: prevent overclaims by matching claims to evidence.

## Claim Levels

- Level 0 — Not verified
- Level 1 — Source verified
- Level 2 — Command verified
- Level 3 — Runtime visually verified
- Level 4 — Build artifact verified
- Level 5 — Install/distribution verified

## Matrix

| Claim attempted | Minimum evidence required | If missing, downgrade to |
|---|---|---|
| Source contains banner | Source file inspection | Source verified only |
| Metro reached localhost | Command output | Command verified only |
| App is visually okay | Runtime visual evidence | Source or command verified only |
| APK ready | Build artifact evidence | Not build verified |
| Install works | Install evidence | Not install verified |
| Production ready | Production gate evidence | Not production verified |
| Public MVP ready | Public/release gate evidence | Not public MVP verified |

## Review Rule

When evidence is missing, downgrade the claim and explain the missing evidence.
