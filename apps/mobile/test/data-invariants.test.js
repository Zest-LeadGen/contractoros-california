// H6-B.2 unit layer (issue #64 items 6-7): invariants of the mobile data
// module, run by Node's built-in test runner — zero test dependencies.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { trackStatuses, internalQuestion } from '../src/data/internalFixtureItems.js';

test('track statuses are non-empty with unique ids', () => {
  assert.ok(trackStatuses.length > 0);
  const ids = trackStatuses.map((t) => t.id);
  assert.equal(new Set(ids).size, ids.length, 'duplicate track id');
});

test('C10 track remains explicitly blocked until its approval gate', () => {
  const c10 = trackStatuses.find((t) => t.id === 'c10-electrical');
  assert.ok(c10, 'c10-electrical track missing');
  assert.match(c10.status, /deferred|blocked/i);
});

test('internal question is well-formed and self-labeled internal', () => {
  assert.equal(internalQuestion.choices.length, 4);
  const ids = internalQuestion.choices.map((c) => c.id);
  assert.equal(new Set(ids).size, ids.length, 'duplicate choice id');
  assert.ok(ids.includes(internalQuestion.correctChoiceId));
  assert.match(internalQuestion.label, /internal fixture/i);
  assert.match(internalQuestion.feedback, /internal/i);
});
