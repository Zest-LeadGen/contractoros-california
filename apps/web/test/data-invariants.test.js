// H6-B.2 unit layer (issue #64 items 6-7): invariants of the pure data
// modules, run by Node's built-in test runner — zero test dependencies.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { claimEligibilityMatrix } from '../src/data/claimEligibilityMatrix.js';
import { internalFixtureItems } from '../src/data/internalFixtureItems.js';

const OFFICIAL_PREFIX = 'https://leginfo.legislature.ca.gov/';
const RISK_RATINGS = new Set(['High', 'Medium', 'Low']);

test('claim matrix is non-empty with unique CLM- claim ids', () => {
  assert.ok(claimEligibilityMatrix.length > 0);
  const ids = claimEligibilityMatrix.map((row) => row.claim_id);
  assert.equal(new Set(ids).size, ids.length, 'duplicate claim_id');
  for (const id of ids) assert.match(id, /^CLM-/);
});

test('every claim cites an official ca.gov source only', () => {
  for (const row of claimEligibilityMatrix) {
    assert.ok(row.source_url.startsWith(OFFICIAL_PREFIX), `${row.claim_id}: ${row.source_url}`);
    assert.match(row.contamination_status, /official source/i);
  }
});

test('claim risk ratings and required fields are valid', () => {
  for (const row of claimEligibilityMatrix) {
    assert.ok(RISK_RATINGS.has(row.risk_rating), `${row.claim_id}: ${row.risk_rating}`);
    for (const field of ['track', 'domain_category', 'statute_section_anchor', 'phase_2e_status']) {
      assert.ok(typeof row[field] === 'string' && row[field].length > 0, `${row.claim_id}: ${field}`);
    }
  }
});

test('claims stay non-public and non-verified until review gates pass', () => {
  for (const row of claimEligibilityMatrix) {
    assert.match(row.public_use_status, /not public/i, row.claim_id);
    assert.match(row.currentness_status, /not legally\/currently verified/i, row.claim_id);
  }
});

test('fixture items have unique ids and well-formed choices', () => {
  const ids = internalFixtureItems.map((item) => item.itemId);
  assert.equal(new Set(ids).size, ids.length, 'duplicate itemId');
  for (const item of internalFixtureItems) {
    assert.equal(item.choices.length, 4, item.itemId);
    const letters = item.choices.map((c) => c.letter);
    assert.deepEqual([...letters].sort(), ['A', 'B', 'C', 'D'], item.itemId);
    assert.ok(letters.includes(item.correctAnswer), `${item.itemId}: correctAnswer ${item.correctAnswer}`);
  }
});

test('fixture items cite official sources and stay internal-only', () => {
  for (const item of internalFixtureItems) {
    assert.ok(item.sourceUrl.startsWith(OFFICIAL_PREFIX), item.itemId);
    assert.match(item.contentStatus, /internal fixture only/i, item.itemId);
    assert.match(item.publicEligibilityStatus, /not public/i, item.itemId);
  }
});
