import assert from 'node:assert/strict';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { TOKEN_ALPHABET, isAllowedDestination } from '../src/policy.js';
import { handlePlayRequest } from '../src/redirect.js';
import { activeMap, rollbackDestination, updateDestination } from '../src/registry.js';
import { INVENTORY, fakeDestination } from './inventory-fixture.js';

const registryPath = process.env.PLAY_REGISTRY_PATH
  || path.join(import.meta.dirname, '..', 'private', 'registry.json');

test('private registry matches the inventory and routes every active edition', { skip: !existsSync(registryPath) }, async () => {
  const registry = JSON.parse(readFileSync(registryPath, 'utf8'));
  const expected = INVENTORY.editions.map((row) => `${row.game_slug}:${row.edition}:${row.source_game_key}`).sort();
  const actual = registry.editions.map((row) => `${row.game_slug}:${row.edition}:${row.source_game_key}`).sort();
  assert.deepEqual(actual, expected);
  const tokens = new Set();
  const deployments = new Set();
  for (const edition of registry.editions) {
    assert.equal(edition.token.length, 12);
    assert.equal([...edition.token].every((ch) => TOKEN_ALPHABET.includes(ch)), true);
    assert.equal(tokens.has(edition.token), false, edition.id);
    tokens.add(edition.token);
    assert.equal(deployments.has(edition.deployment_id), false, edition.id);
    deployments.add(edition.deployment_id);
    assert.equal(isAllowedDestination(edition.destination), true, edition.id);
    assert.equal(edition.play_url, `https://play.reviewrecess.com/${edition.game_slug}/${edition.token}`);
  }
  const map = activeMap(registry);
  assert.equal(Object.keys(map.routes).length, 27);
  const host = 'https://play.reviewrecess.com';
  for (const edition of registry.editions) {
    const response = handlePlayRequest(new Request(`${host}${edition.path}`), map);
    if (edition.status === 'held') {
      assert.equal(response.status, 404, edition.id);
      assert.equal(await response.text(), 'Not found\n');
    } else {
      assert.equal(response.status, 302, edition.id);
      assert.equal(response.headers.get('Cache-Control'), 'no-store');
      assert.equal(response.headers.get('Location'), edition.destination);
    }
  }
  const copy = structuredClone(registry);
  const editable = copy.editions.find((item) => item.id === 'answer-armada:editable');
  const token = editable.token;
  updateDestination(copy, 'answer-armada:editable', {
    destination: fakeDestination('FAKErollbackcheck1'),
    deploymentId: 'FAKErollbackcheck1',
    now: () => '2026-11-07T06:00:00.000Z',
  });
  rollbackDestination(copy, 'answer-armada:editable', { now: () => '2026-11-07T07:00:00.000Z' });
  assert.equal(copy.editions.find((item) => item.id === 'answer-armada:editable').token, token);
  assert.equal(copy.editions.find((item) => item.id === 'answer-armada:editable').destination, editable.destination);
  assert.equal(JSON.parse(readFileSync(registryPath, 'utf8')).editions.find((item) => item.id === 'answer-armada:editable').token, token);
});
