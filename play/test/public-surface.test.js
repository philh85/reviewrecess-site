import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';
import { TOKEN_ALPHABET } from '../src/policy.js';

const ROOT = path.join(import.meta.dirname, '..', '..');

function trackedFiles() {
  const result = spawnSync('git', ['ls-files', '--cached', '--others', '--exclude-standard'], { cwd: ROOT, encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  return result.stdout.split('\n').filter(Boolean);
}

test('git does not track a plaintext token registry', () => {
  const files = trackedFiles();
  for (const file of files) {
    assert.equal(file.endsWith('registry.json'), false, file);
    assert.equal(file.includes('active-map'), false, file);
    assert.equal(file.startsWith('play/private/') && file.endsWith('.json'), false, file);
  }
});

test('tracked files do not contain Apps Script deployment ids or paid play tokens', () => {
  const files = trackedFiles();
  const registryPath = path.join(ROOT, 'play', 'private', 'registry.json');
  let paidTokens = [];
  let deploymentIds = [];
  let destinations = [];
  let freeToken = '';
  if (existsSync(registryPath)) {
    const registry = JSON.parse(readFileSync(registryPath, 'utf8'));
    for (const edition of registry.editions) {
      deploymentIds.push(edition.deployment_id);
      destinations.push(edition.destination);
      if (edition.id === 'answer-armada:free') freeToken = edition.token;
      else paidTokens.push(edition.token);
    }
  }
  for (const file of files) {
    const text = readFileSync(path.join(ROOT, file), 'utf8');
    assert.equal(text.includes(`AKfyc${'b'}`), false, file);
    for (const id of deploymentIds) assert.equal(text.includes(id), false, `${file} contains a deployment id`);
    for (const destination of destinations) assert.equal(text.includes(destination), false, `${file} contains a destination`);
    for (const token of paidTokens) assert.equal(text.includes(token), false, `${file} contains a paid token`);
    if (freeToken && text.includes(freeToken)) {
      assert.equal(file, 'site/assets/js/config.js');
    }
  }
  if (freeToken) {
    const config = readFileSync(path.join(ROOT, 'site', 'assets', 'js', 'config.js'), 'utf8');
    assert.equal(config.includes(`https://play.reviewrecess.com/answer-armada/${freeToken}`), true);
    const ignored = spawnSync('git', ['check-ignore', '-q', 'play/private/registry.json'], { cwd: ROOT });
    assert.equal(ignored.status, 0);
  }
});

test('the public site has at most the free Answer Armada play URL', () => {
  const config = readFileSync(path.join(ROOT, 'site', 'assets', 'js', 'config.js'), 'utf8');
  const matches = config.match(/https:\/\/play\.reviewrecess\.com\/[a-z0-9-]+\/[A-Za-z0-9]{12}/g) || [];
  assert.ok(matches.length <= 1);
  if (matches.length === 1) {
    assert.match(matches[0], new RegExp(`^https://play\\.reviewrecess\\.com/answer-armada/[${TOKEN_ALPHABET}]{12}$`));
  }
  const siteJs = readFileSync(path.join(ROOT, 'site', 'assets', 'js', 'site.js'), 'utf8');
  assert.equal(siteJs.includes(TOKEN_ALPHABET), true);
  const htmlFiles = trackedFiles().filter((file) => file.startsWith('site/') && file.endsWith('.html'));
  for (const file of htmlFiles) {
    const text = readFileSync(path.join(ROOT, file), 'utf8');
    assert.equal(text.includes('play.reviewrecess.com/'), false, file);
  }
  const robots = readFileSync(path.join(ROOT, 'site', 'robots.txt'), 'utf8');
  const sitemap = readFileSync(path.join(ROOT, 'site', 'sitemap.xml'), 'utf8');
  assert.equal(robots.includes('play.reviewrecess.com'), false);
  assert.equal(sitemap.includes('play.reviewrecess.com'), false);
});
