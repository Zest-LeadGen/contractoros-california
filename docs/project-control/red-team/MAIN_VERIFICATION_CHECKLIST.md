# Main Verification Checklist

Purpose: post-merge verification checklist.

## Checklist

1. Verify PR state is closed.
2. Verify merged is true.
3. Verify merge commit SHA.
4. Verify merged timestamp.
5. Verify expected files exist on main.
6. Verify forbidden files are absent on main.
7. Verify report exists on main.
8. Verify claims still match evidence.
9. Verify next phase is either allowed or blocked.
10. Record decision.

## Required Forbidden Path Checks

```text
apps/mobile/package-lock.json
apps/web/package-lock.json
eas.json
android/build.gradle
ios/Podfile
```

## Decision Output

Record whether main verification passed, failed, or requires a patch.
