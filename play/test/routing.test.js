import assert from 'node:assert/strict';
import test from 'node:test';
import { APPROVED_JOIN_PARAMS, TOKEN_ALPHABET } from '../src/policy.js';
import { handlePlayRequest, loadActiveMap, normalizeMap } from '../src/redirect.js';
import worker from '../src/worker.js';
import { activeMap, buildRegistry, rollbackDestination, updateDestination } from '../src/registry.js';
import { INVENTORY, fakeDestination, seededRandomInt } from './inventory-fixture.js';

const HOST = 'https://play.reviewrecess.com';

function registry() {
  return buildRegistry(INVENTORY, {
    now: () => '2026-11-07T00:00:00.000Z',
    randomInt: seededRandomInt(0xA11CE),
  });
}

function routeMap(source = registry()) {
  return normalizeMap(activeMap(source));
}

async function bodyOf(response) {
  return response.text();
}

test('production join allowlist is explicit and empty', () => {
  assert.deepEqual(APPROVED_JOIN_PARAMS, []);
});

test('every active fixture edition redirects to its own destination', async () => {
  const source = registry();
  const map = routeMap(source);
  for (const edition of source.editions) {
    const response = handlePlayRequest(new Request(`${HOST}${edition.path}`), map);
    if (edition.status !== 'active') {
      assert.equal(response.status, 404, edition.id);
      assert.equal(await bodyOf(response), 'Not found\n');
      continue;
    }
    assert.equal(response.status, 302, edition.id);
    assert.equal(response.headers.get('Location'), edition.destination);
    assert.equal(await bodyOf(response), '');
  }
});

test('priority Answer Armada editions are distinct routes', () => {
  const source = registry();
  const ids = [
    'answer-armada:free',
    'answer-armada:grade-3-multiplication-division-facts',
    'answer-armada:editable',
  ];
  const tokens = new Set();
  for (const id of ids) {
    const edition = source.editions.find((item) => item.id === id);
    assert.equal(edition.status, 'active');
    assert.equal(source.editions.indexOf(edition), ids.indexOf(id));
    tokens.add(edition.token);
    const response = handlePlayRequest(new Request(`${HOST}${edition.path}`), routeMap(source));
    assert.equal(response.status, 302);
    assert.equal(response.headers.get('Location'), edition.destination);
    const slashed = handlePlayRequest(new Request(`${HOST}${edition.path}/`), routeMap(source));
    assert.equal(slashed.status, 302);
    assert.equal(slashed.headers.get('Location'), edition.destination);
  }
  assert.equal(tokens.size, 3);
});

test('redirect headers are 302 and no-store, with an empty body', async () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'answer-armada:free');
  const response = handlePlayRequest(new Request(`${HOST}${edition.path}`), routeMap(source));
  assert.equal(response.status, 302);
  assert.equal(response.headers.get('Cache-Control'), 'no-store');
  assert.equal(response.headers.get('CDN-Cache-Control'), 'no-store');
  assert.equal(response.headers.get('Cloudflare-CDN-Cache-Control'), 'no-store');
  assert.equal(response.headers.get('Pragma'), 'no-cache');
  assert.equal(response.headers.get('Expires'), '0');
  assert.equal(response.headers.get('Referrer-Policy'), 'no-referrer');
  assert.equal(response.headers.get('X-Robots-Tag'), 'noindex, nofollow, noarchive');
  assert.equal(response.headers.get('Content-Type'), null);
  assert.equal(response.headers.get('Set-Cookie'), null);
  assert.equal(await bodyOf(response), '');
  const names = [...response.headers.keys()];
  assert.equal(names.includes('location'), true);
  for (const name of names) assert.equal(name.startsWith('x-edition'), false);
});

test('HEAD redirects with no body', async () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'answer-armada:editable');
  const response = handlePlayRequest(new Request(`${HOST}${edition.path}`, { method: 'HEAD' }), routeMap(source));
  assert.equal(response.status, 302);
  assert.equal(response.headers.get('Location'), edition.destination);
  assert.equal(await bodyOf(response), '');
});

test('unknown paths, folder roots, and bad tokens are a generic 404 with no list', async () => {
  const source = registry();
  const map = routeMap(source);
  const edition = source.editions.find((item) => item.id === 'answer-armada:free');
  const paths = [
    '/',
    '/robots.txt',
    '/sitemap.xml',
    '/favicon.ico',
    '/active',
    '/registry',
    '/map',
    '/answer-armada',
    '/answer-armada/',
    '/word-morph',
    '/word-morph/',
    '/telling-time/',
    `/answer-armada/${'A'.repeat(11)}`,
    `/answer-armada/${'A'.repeat(13)}`,
    `/answer-armada/${edition.token}extra`,
    `/answer-armada/${edition.token}/more`,
    `/word-morph/${edition.token}`,
    `/answer-armada/${edition.token[0] === 'A' ? 'B' : 'A'}${edition.token.slice(1)}`,
    '/Answer-Armada/' + edition.token,
  ];
  const secretBits = source.editions.flatMap((item) => [item.token, item.destination, item.display_name, item.deployment_id]);
  for (const path of paths) {
    const response = handlePlayRequest(new Request(`${HOST}${path}`), map);
    assert.equal(response.status, 404, path);
    assert.equal(response.headers.get('Cache-Control'), 'no-store');
    assert.equal(response.headers.get('Location'), null);
    const text = await bodyOf(response);
    assert.equal(text, 'Not found\n');
    for (const secret of secretBits) assert.equal(text.includes(secret), false, path);
    assert.equal(text.includes('<'), false);
    assert.equal(text.toLowerCase().includes('script.google'), false);
  }
});

test('a token is not accepted under a different game slug', () => {
  const source = registry();
  const pack = source.editions.find((item) => item.id === 'answer-armada:grade-3-multiplication-division-facts');
  const response = handlePlayRequest(new Request(`${HOST}/five-second-battle/${pack.token}`), routeMap(source));
  assert.equal(response.status, 404);
});

test('arbitrary query values are not forwarded', () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'answer-armada:free');
  const queries = [
    '?url=https://evil.example/phish',
    '?redirect=https://evil.example',
    '?next=https://evil.example',
    '?dest=https://script.google.com.evil.example',
    '?join=ABC234',
    '?room=ABC234&code=XYZ234',
    '?answer-armada=1',
  ];
  for (const query of queries) {
    const response = handlePlayRequest(new Request(`${HOST}${edition.path}${query}`), routeMap(source));
    assert.equal(response.status, 302, query);
    assert.equal(response.headers.get('Location'), edition.destination);
    assert.equal(response.headers.get('Location').includes('?'), false);
    assert.equal(response.headers.get('Location').includes('evil'), false);
  }
});

test('an explicitly approved join parameter is appended only when its value matches', () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'answer-armada:free');
  const joinParams = [{ name: 'join', pattern: /^[ABCDEFGHJKLMNPQRSTUVWXYZ23456789]{6}$/ }];
  const ok = handlePlayRequest(
    new Request(`${HOST}${edition.path}?join=AB2345&next=https://evil.example&join_code=nope`),
    routeMap(source),
    { joinParams },
  );
  assert.equal(ok.headers.get('Location'), `${edition.destination}?join=AB2345`);
  const bad = handlePlayRequest(
    new Request(`${HOST}${edition.path}?join=has-bad&url=https://evil.example`),
    routeMap(source),
    { joinParams },
  );
  assert.equal(bad.headers.get('Location'), edition.destination);
  const duplicated = handlePlayRequest(
    new Request(`${HOST}${edition.path}?join=AB2345&join=CD6789`),
    routeMap(source),
    { joinParams },
  );
  assert.equal(duplicated.headers.get('Location'), edition.destination);
});

test('held adverb editions and wrong hosts do not redirect', () => {
  const source = registry();
  const map = routeMap(source);
  for (const id of ['word-magnets:full', 'word-magnets:free']) {
    const edition = source.editions.find((item) => item.id === id);
    assert.equal(edition.status, 'held');
    assert.equal(handlePlayRequest(new Request(`${HOST}${edition.path}`), map).status, 404);
    assert.equal(Object.hasOwn(map.routes, `${edition.game_slug}/${edition.token}`), false);
  }
  const free = source.editions.find((item) => item.id === 'answer-armada:free');
  for (const url of [
    `https://reviewrecess-play.workers.dev${free.path}`,
    `https://www.reviewrecess.com${free.path}`,
    `https://reviewrecess.com${free.path}`,
    `https://play.reviewrecess.com.evil.example${free.path}`,
  ]) {
    assert.equal(handlePlayRequest(new Request(url), map).status, 404, url);
  }
});

test('disallowed destinations and non-GET methods fail closed', () => {
  const source = registry();
  const free = source.editions.find((item) => item.id === 'answer-armada:free');
  const key = `${free.game_slug}/${free.token}`;
  const map = normalizeMap({
    routes: {
      [key]: 'https://evil.example/macros/s/not-google/exec',
      'answer-armada/ZZZZZZZZZZZZ': 'https://script.google.com/macros/s/GOODID123/exec?next=https://evil.example',
      'answer-armada/YYYYYYYYYYYY': 'https://user:pass@script.google.com/macros/s/GOODID123/exec',
      'answer-armada/XXXXXXXXXXXX': 'http://script.google.com/macros/s/GOODID123/exec',
      'answer-armada/WWWWWWWWWWWW': 'https://script.google.com/macros/s/GOODID123/dev',
      __proto__: 'https://script.google.com/macros/s/GOODID123/exec',
    },
  });
  assert.equal(handlePlayRequest(new Request(`${HOST}${free.path}`), map).status, 404);
  assert.equal(handlePlayRequest(new Request(`${HOST}/answer-armada/ZZZZZZZZZZZZ`), map).status, 404);
  assert.equal(handlePlayRequest(new Request(`${HOST}${free.path}`, { method: 'POST' }), routeMap(source)).status, 404);
  assert.equal(map.routes[key], undefined);
});

test('a good route survives a bad sibling in the stored map', () => {
  const source = registry();
  const free = source.editions.find((item) => item.id === 'answer-armada:free');
  const map = normalizeMap({
    routes: {
      [`${free.game_slug}/${free.token}`]: free.destination,
      'mystery-cat/BADBADBADBAD': 'https://example.com',
    },
  });
  const response = handlePlayRequest(new Request(`${HOST}${free.path}`), map);
  assert.equal(response.status, 302);
  assert.equal(response.headers.get('Location'), free.destination);
});

test('rollback changes the destination and keeps the token', () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'answer-armada:grade-3-multiplication-division-facts');
  const token = edition.token;
  const original = edition.destination;
  const next = fakeDestination('packupdated0001');
  updateDestination(source, edition.id, {
    destination: next,
    deploymentId: 'packupdated0001',
    sourceVersion: '@9',
    now: () => '2026-11-07T01:00:00.000Z',
  });
  assert.equal(edition.token, token);
  assert.equal(edition.id, 'answer-armada:grade-3-multiplication-division-facts');
  let response = handlePlayRequest(new Request(`${HOST}${edition.path}`), routeMap(source));
  assert.equal(response.headers.get('Location'), next);

  rollbackDestination(source, edition.id, { now: () => '2026-11-07T02:00:00.000Z' });
  assert.equal(edition.token, token);
  assert.equal(edition.destination, original);
  assert.equal(edition.history.at(-1).action, 'rollback');
  assert.equal(edition.history.length, 3);
  response = handlePlayRequest(new Request(`${HOST}${edition.path}`), routeMap(source));
  assert.equal(response.status, 302);
  assert.equal(response.headers.get('Location'), original);
  assert.equal([...edition.token].every((ch) => TOKEN_ALPHABET.includes(ch)), true);
});

test('the worker reads only the active KV key', async () => {
  const source = registry();
  const edition = source.editions.find((item) => item.id === 'telling-time:full');
  const seen = [];
  const env = {
    PLAY_MAP: {
      async get(key) {
        seen.push(key);
        return JSON.stringify(activeMap(source));
      },
    },
    PLAY_MAP_JSON: JSON.stringify({ routes: { 'answer-armada/SHOULDNOTUSE0': fakeDestination('secretfallback1') } }),
  };
  const response = await worker.fetch(new Request(`${HOST}${edition.path}`), env);
  assert.deepEqual(seen, ['active']);
  assert.equal(response.status, 302);
  assert.equal(response.headers.get('Location'), edition.destination);
});

test('a missing or corrupt map is a generic 404', async () => {
  const broken = { PLAY_MAP: { async get() { throw new Error('down'); } } };
  const missing = {};
  const corrupt = { PLAY_MAP_JSON: '{not json' };
  for (const env of [broken, missing, corrupt]) {
    const response = await worker.fetch(new Request(`${HOST}/`), env);
    assert.equal(response.status, 404);
    assert.equal(await response.text(), 'Not found\n');
  }
  const fromSecret = await loadActiveMap({ PLAY_MAP_JSON: JSON.stringify(activeMap(registry())) });
  assert.equal(typeof fromSecret.routes, 'object');
});
