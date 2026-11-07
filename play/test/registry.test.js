import assert from 'node:assert/strict';
import { mkdtemp, readFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { spawnSync } from 'node:child_process';
import { TOKEN_ALPHABET, TOKEN_LENGTH, isAllowedDestination } from '../src/policy.js';
import {
  RegistryError,
  activeMap,
  addEdition,
  buildRegistry,
  rollbackDestination,
  updateDestination,
} from '../src/registry.js';
import { INVENTORY, fakeDestination, seededRandomInt } from './inventory-fixture.js';

function build() {
  return buildRegistry(INVENTORY, {
    now: () => '2026-11-07T00:00:00.000Z',
    randomInt: seededRandomInt(0xC0FFEE),
  });
}

test('one permanent token per inventory edition, with no invented splits', () => {
  const registry = build();
  assert.equal(registry.editions.length, 29);
  const tokens = registry.editions.map((item) => item.token);
  assert.equal(new Set(tokens).size, 29);
  for (const token of tokens) {
    assert.equal(token.length, TOKEN_LENGTH);
    assert.equal([...token].every((ch) => TOKEN_ALPHABET.includes(ch)), true);
    assert.equal(/[0OolI1Li]/.test(token), false);
  }
  for (const slug of ['word-morph', 'telling-time']) {
    const rows = registry.editions.filter((item) => item.game_slug === slug);
    assert.deepEqual(rows.map((item) => item.edition), ['full']);
  }
  assert.equal(registry.editions.some((item) => item.edition === 'dino' || item.edition === 'theme'), false);
  const active = registry.editions.filter((item) => item.status === 'active');
  const held = registry.editions.filter((item) => item.status === 'held');
  assert.equal(active.length, 27);
  assert.deepEqual(held.map((item) => item.id).sort(), ['word-magnets:free', 'word-magnets:full']);
  assert.equal(Object.keys(activeMap(registry).routes).length, 27);
  assert.deepEqual(registry.editions.slice(0, 3).map((item) => item.id), [
    'answer-armada:free',
    'answer-armada:grade-3-multiplication-division-facts',
    'answer-armada:editable',
  ]);
});

test('a theme row and a duplicate edition are rejected', () => {
  const theme = structuredClone(INVENTORY);
  theme.editions.push({
    game_slug: 'answer-armada',
    edition: 'dino',
    source_game_key: 'battleships-dino',
    display_name: 'Dino theme',
    current_deployment_url: fakeDestination('FAKEthemedino0001'),
    deployment_id: 'FAKEthemedino0001',
  });
  assert.throws(() => buildRegistry(theme, { randomInt: () => 1 }), RegistryError);

  const duplicate = structuredClone(INVENTORY);
  duplicate.editions.push({ ...duplicate.editions[1] });
  assert.throws(() => buildRegistry(duplicate, { randomInt: () => 1 }), /duplicated/);
});

test('an update is not a new edition, and rollback restores the previous destination', () => {
  const registry = build();
  const before = registry.editions.map((item) => [item.id, item.token]);
  const id = 'answer-armada:editable';
  const original = registry.editions.find((item) => item.id === id);
  const originalDestination = original.destination;
  updateDestination(registry, id, {
    destination: fakeDestination('FAKEupdateditable1'),
    deploymentId: 'FAKEupdateditable1',
    sourceVersion: '@12',
    now: () => '2026-11-07T03:00:00.000Z',
    note: 'new deployment of the same editable product',
  });
  assert.deepEqual(registry.editions.map((item) => [item.id, item.token]), before);
  assert.equal(registry.editions.find((item) => item.id === id).destination, fakeDestination('FAKEupdateditable1'));
  assert.throws(() => updateDestination(registry, id, {
    destination: fakeDestination('FAKEupdateditable1'),
    deploymentId: 'FAKEupdateditable1',
  }), /not a new edition/);
  assert.throws(() => addEdition(registry, {
    game_slug: 'answer-armada',
    edition: 'editable',
    source_game_key: 'battleships',
    display_name: 'Review Recess Answer Armada',
    destination: fakeDestination('FAKEothereditable1'),
    deployment_id: 'FAKEothereditable1',
  }, { randomInt: () => 2 }), /already exists/);

  rollbackDestination(registry, id, { now: () => '2026-11-07T04:00:00.000Z' });
  const restored = registry.editions.find((item) => item.id === id);
  assert.equal(restored.destination, originalDestination);
  assert.equal(restored.token, before.find(([itemId]) => itemId === id)[1]);
  assert.equal(restored.history.at(-1).action, 'rollback');
  assert.equal(isAllowedDestination(restored.destination), true);
});

test('adding a new edition does not rotate existing tokens', () => {
  const registry = build();
  const before = new Map(registry.editions.map((item) => [item.id, item.token]));
  addEdition(registry, {
    game_slug: 'answer-armada',
    edition: 'grade-4-sample',
    source_game_key: 'battleships-grade-4',
    display_name: 'Grade 4 sample pack',
    destination: fakeDestination('FAKEgrade4sample01'),
    deployment_id: 'FAKEgrade4sample01',
  }, { randomInt: () => 4, now: () => '2026-11-07T05:00:00.000Z' });
  for (const [id, token] of before) {
    assert.equal(registry.editions.find((item) => item.id === id).token, token);
  }
  assert.equal(registry.editions.at(-1).id, 'answer-armada:grade-4-sample');
  assert.notEqual(registry.editions.at(-1).token, '');
});

test('init refuses to replace an existing registry', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'rr-play-'));
  const inventory = path.join(dir, 'inventory.json');
  const out = path.join(dir, 'registry.json');
  const { writeFile } = await import('node:fs/promises');
  await writeFile(inventory, JSON.stringify(INVENTORY));
  const cli = path.join(import.meta.dirname, '..', 'scripts', 'manage.mjs');
  const first = spawnSync(process.execPath, [cli, 'init', '--inventory', inventory, '--out', out], { encoding: 'utf8' });
  assert.equal(first.status, 0, first.stderr);
  const firstText = await readFile(out, 'utf8');
  const second = spawnSync(process.execPath, [cli, 'init', '--inventory', inventory, '--out', out], { encoding: 'utf8' });
  assert.equal(second.status, 1);
  assert.match(second.stderr, /refusing to mint new tokens/);
  assert.equal(await readFile(out, 'utf8'), firstText);
});

test('cli rollback round-trips a copy without touching the fixture', async () => {
  const dir = await mkdtemp(path.join(tmpdir(), 'rr-play-rb-'));
  const inventory = path.join(dir, 'inventory.json');
  const registryPath = path.join(dir, 'registry.json');
  const { writeFile } = await import('node:fs/promises');
  await writeFile(inventory, JSON.stringify(INVENTORY));
  const cli = path.join(import.meta.dirname, '..', 'scripts', 'manage.mjs');
  assert.equal(spawnSync(process.execPath, [cli, 'init', '--inventory', inventory, '--out', registryPath], { encoding: 'utf8' }).status, 0);
  const before = JSON.parse(await readFile(registryPath, 'utf8'));
  const target = before.editions.find((item) => item.id === 'word-morph:full');
  const next = fakeDestination('FAKEwordmorphnext1');
  const updated = spawnSync(process.execPath, [
    cli, 'update-destination', '--registry', registryPath, '--id', 'word-morph:full',
    '--destination', next, '--deployment-id', 'FAKEwordmorphnext1', '--source-version', '@4',
  ], { encoding: 'utf8' });
  assert.equal(updated.status, 0, updated.stderr);
  const mid = JSON.parse(await readFile(registryPath, 'utf8'));
  assert.equal(mid.editions.find((item) => item.id === 'word-morph:full').token, target.token);
  assert.equal(mid.editions.find((item) => item.id === 'word-morph:full').destination, next);
  const rolled = spawnSync(process.execPath, [cli, 'rollback', '--registry', registryPath, '--id', 'word-morph:full'], { encoding: 'utf8' });
  assert.equal(rolled.status, 0, rolled.stderr);
  const after = JSON.parse(await readFile(registryPath, 'utf8'));
  const edition = after.editions.find((item) => item.id === 'word-morph:full');
  assert.equal(edition.token, target.token);
  assert.equal(edition.destination, target.destination);
  assert.equal(edition.history.at(-1).action, 'rollback');
  const activeOut = path.join(dir, 'active.json');
  assert.equal(spawnSync(process.execPath, [cli, 'export-active', '--registry', registryPath, '--out', activeOut], { encoding: 'utf8' }).status, 0);
  const map = JSON.parse(await readFile(activeOut, 'utf8'));
  assert.equal(map.routes[`word-morph/${target.token}`], target.destination);
  assert.equal(Object.hasOwn(map.routes, `word-magnets/${before.editions.find((item) => item.id === 'word-magnets:full').token}`), false);
});
