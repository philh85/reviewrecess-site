#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import {
  activeMap,
  addEdition,
  buildRegistry,
  publishHeld,
  rollbackDestination,
  updateDestination,
} from '../src/registry.js';

const [command, ...args] = process.argv.slice(2);

function flag(name) {
  const index = args.indexOf(name);
  if (index === -1 || index + 1 >= args.length) return '';
  return args[index + 1];
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, { mode: 0o600 });
  fs.chmodSync(file, 0o600);
}

function requireFlag(name) {
  const value = flag(name);
  if (!value) {
    console.error(`missing ${name}`);
    process.exit(1);
  }
  return value;
}

function fail(error) {
  console.error(error.message || String(error));
  process.exit(1);
}

function writeInstructions(registry, file) {
  const active = registry.editions.filter((item) => item.status === 'active');
  const held = registry.editions.filter((item) => item.status !== 'active');
  const lines = [];
  lines.push('# Review Recess play links — private operator record');
  lines.push('');
  lines.push('This file contains unlisted bearer tokens and Apps Script destinations.');
  lines.push('Do not commit it, paste it into a pull request, or upload it to the marketing site.');
  lines.push('Tokens are not purchase authentication. Knowing a paid URL is not a TpT receipt.');
  lines.push('');
  lines.push('Generated from the private registry. Generating this file does not deploy anything and does not prove the hostname is live.');
  lines.push('');
  lines.push('## Active play URLs');
  lines.push('');
  lines.push('Priority order is Answer Armada free, then the grade-3 multiplication and division pack, then the editable edition, then the rest of the inventory.');
  lines.push('');
  lines.push('| Edition | Play URL |');
  lines.push('|---|---|');
  for (const edition of active) {
    lines.push(`| ${edition.id} | ${edition.play_url} |`);
  }
  lines.push('');
  lines.push('## Held (do not print on kits)');
  lines.push('');
  if (held.length === 0) lines.push('None.');
  for (const edition of held) {
    lines.push(`- ${edition.id} (${edition.display_name}): token reserved at ${edition.play_url}. ${edition.hold_reason}`);
  }
  lines.push('');
  lines.push('## Destination map');
  lines.push('');
  lines.push('Updates replace the destination only. Do not delete the old Apps Script deployment.');
  lines.push('');
  lines.push('| Edition | Deployment | Destination |');
  lines.push('|---|---|---|');
  for (const edition of registry.editions) {
    lines.push(`| ${edition.id} | ${edition.deployment_id} | ${edition.destination} |`);
  }
  lines.push('');
  lines.push('## TpT kits');
  lines.push('');
  lines.push('Do this only after a real request to the play host returns HTTP 302. This infrastructure change does not rebuild ZIPs and does not edit game source.');
  lines.push('');
  lines.push('For each active edition, replace that product\'s script.google.com `/exec` link in the teacher PDF or quick start with the play URL in the table above. One URL per edition. Picture themes share that edition\'s URL. word-morph and telling-time each have one edition. Leave both adverb-game products on their current links until the names are confirmed, then publish the held route without minting a new token.');
  lines.push('');
  lines.push('## Website');
  lines.push('');
  lines.push('The marketing site may publish only the Answer Armada free play URL, in `site/assets/js/config.js` as `ANSWER_ARMADA.FREE_PLAY_URL`. Upload that site change only after the free URL returns 302. Paid play URLs stay out of the site, the sitemap, and git.');
  lines.push('');
  const text = `${lines.join('\n')}\n`;
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text, { mode: 0o600 });
  fs.chmodSync(file, 0o600);
}

try {
  if (command === 'init') {
    const inventoryPath = requireFlag('--inventory');
    const out = requireFlag('--out');
    if (fs.existsSync(out)) {
      console.error('registry already exists; refusing to mint new tokens. A product update changes the destination, not the token.');
      process.exit(1);
    }
    const registry = buildRegistry(readJson(inventoryPath));
    writeJson(out, registry);
    const active = registry.editions.filter((item) => item.status === 'active').length;
    const held = registry.editions.length - active;
    console.log(`wrote ${registry.editions.length} editions (${active} active, ${held} held) to ${out}`);
  } else if (command === 'export-active') {
    const registry = readJson(requireFlag('--registry'));
    const out = requireFlag('--out');
    const map = activeMap(registry);
    writeJson(out, map);
    const compact = out.replace(/\.json$/, '.min.json');
    fs.writeFileSync(compact, JSON.stringify(map), { mode: 0o600 });
    fs.chmodSync(compact, 0o600);
    console.log(`wrote ${Object.keys(map.routes).length} routes (${Buffer.byteLength(JSON.stringify(map))} bytes compact) to ${out}`);
  } else if (command === 'update-destination') {
    const registryPath = requireFlag('--registry');
    const registry = readJson(registryPath);
    updateDestination(registry, requireFlag('--id'), {
      destination: requireFlag('--destination'),
      deploymentId: requireFlag('--deployment-id'),
      sourceVersion: args.includes('--source-version') ? flag('--source-version') : undefined,
      note: flag('--note'),
    });
    writeJson(registryPath, registry);
    console.log('destination updated; token unchanged');
  } else if (command === 'rollback') {
    const registryPath = requireFlag('--registry');
    const registry = readJson(registryPath);
    rollbackDestination(registry, requireFlag('--id'), { note: flag('--note') });
    writeJson(registryPath, registry);
    console.log('rolled back to the previous destination; token unchanged');
  } else if (command === 'add-edition') {
    const registryPath = requireFlag('--registry');
    const registry = readJson(registryPath);
    const before = new Map(registry.editions.map((item) => [item.id, item.token]));
    addEdition(registry, {
      game_slug: requireFlag('--game-slug'),
      edition: requireFlag('--edition'),
      source_game_key: requireFlag('--source-game-key'),
      display_name: requireFlag('--display-name'),
      destination: requireFlag('--destination'),
      deployment_id: requireFlag('--deployment-id'),
      source_version: flag('--source-version'),
      notes: flag('--notes'),
    });
    for (const [id, token] of before) {
      const current = registry.editions.find((item) => item.id === id);
      if (!current || current.token !== token) throw new Error(`token changed for ${id}`);
    }
    writeJson(registryPath, registry);
    console.log('new edition added; existing tokens unchanged');
  } else if (command === 'publish-held') {
    const registryPath = requireFlag('--registry');
    const registry = readJson(registryPath);
    publishHeld(registry, requireFlag('--id'), { note: flag('--note') });
    writeJson(registryPath, registry);
    console.log('held edition published; token unchanged');
  } else if (command === 'instructions') {
    const registry = readJson(requireFlag('--registry'));
    const out = requireFlag('--out');
    writeInstructions(registry, out);
    console.log(`wrote instructions to ${out}`);
  } else if (command === 'free-play-url') {
    const registry = readJson(requireFlag('--registry'));
    const edition = registry.editions.find((item) => item.id === 'answer-armada:free' && item.status === 'active');
    if (!edition) throw new Error('answer-armada:free is not an active edition');
    process.stdout.write(`${edition.play_url}\n`);
  } else {
    console.error('commands: init | export-active | update-destination | rollback | add-edition | publish-held | instructions | free-play-url');
    process.exit(1);
  }
} catch (error) {
  fail(error);
}
