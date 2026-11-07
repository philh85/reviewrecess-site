import { randomInt as cryptoRandomInt } from 'node:crypto';
import {
  PRIORITY_EDITION_IDS,
  TOKEN_ALPHABET,
  TOKEN_LENGTH,
  WELL_KNOWN_SLUGS,
  deploymentIdFromDestination,
  isAdverbSource,
  isAllowedDestination,
  isThemeEdition,
  isToken,
} from './policy.js';

export class RegistryError extends Error {
  constructor(message) {
    super(message);
    this.name = 'RegistryError';
  }
}

function editionId(slug, edition) {
  return `${slug}:${edition}`;
}

function requireFields(row, index) {
  const missing = ['game_slug', 'edition', 'source_game_key', 'display_name', 'current_deployment_url', 'deployment_id']
    .filter((key) => typeof row[key] !== 'string' || !row[key].trim());
  if (missing.length) {
    throw new RegistryError(`edition ${index + 1} is missing ${missing.join(', ')}`);
  }
}

function mintToken(used, randomInt) {
  for (let attempt = 0; attempt < 50; attempt += 1) {
    let token = '';
    for (let i = 0; i < TOKEN_LENGTH; i += 1) token += TOKEN_ALPHABET[randomInt(TOKEN_ALPHABET.length)];
    if (!used.has(token)) {
      used.add(token);
      return token;
    }
  }
  throw new RegistryError('could not mint a unique token');
}

function holdReason(row) {
  if (!isAdverbSource(row.source_game_key)) return '';
  return 'Adverb-game product names are unresolved (full: What Does It Modify?; free: Review Recess Word Magnets). The site slug word-magnets is well known, but this mapping is not published until the names are confirmed.';
}

/**
 * Build a private registry from a deployment inventory.
 * One token per distinct product edition. Themes are rejected.
 * Word Morph and telling-time are not given extra editions here; only rows
 * present in the inventory are issued. Adverb-game rows are held, not published.
 */
export function buildRegistry(inventory, options = {}) {
  const rows = inventory && Array.isArray(inventory.editions) ? inventory.editions : null;
  if (!rows || rows.length === 0) throw new RegistryError('inventory has no editions');
  const randomInt = options.randomInt || ((max) => cryptoRandomInt(max));
  const now = options.now || (() => new Date().toISOString());
  const createdAt = now();
  const usedTokens = new Set();
  const seenIds = new Set();
  const seenDeployments = new Set();

  const indexed = rows.map((row, index) => {
    if (!row || typeof row !== 'object') throw new RegistryError(`edition ${index + 1} is not an object`);
    requireFields(row, index);
    const slug = row.game_slug.trim();
    const edition = row.edition.trim();
    if (!WELL_KNOWN_SLUGS.has(slug)) {
      throw new RegistryError(`${slug} is not a well-known game slug`);
    }
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(edition)) {
      throw new RegistryError(`${slug} has an invalid edition name`);
    }
    if (isThemeEdition(edition)) {
      throw new RegistryError(`${slug}:${edition} is a theme, not an edition`);
    }
    const id = editionId(slug, edition);
    if (seenIds.has(id)) throw new RegistryError(`${id} is duplicated`);
    seenIds.add(id);
    const destination = row.current_deployment_url.trim();
    if (!isAllowedDestination(destination)) {
      throw new RegistryError(`${id} destination is not an allowlisted script.google.com /exec URL`);
    }
    const deploymentId = row.deployment_id.trim();
    if (deploymentId !== deploymentIdFromDestination(destination)) {
      throw new RegistryError(`${id} deployment_id does not match its destination`);
    }
    if (seenDeployments.has(deploymentId)) throw new RegistryError(`${id} reuses a deployment id`);
    seenDeployments.add(deploymentId);
    return { row, index, id, slug, edition, destination, deploymentId };
  });

  indexed.sort((a, b) => {
    const rank = (item) => {
      const priority = PRIORITY_EDITION_IDS.indexOf(item.id);
      return priority === -1 ? PRIORITY_EDITION_IDS.length + item.index : priority;
    };
    return rank(a) - rank(b);
  });

  const editions = indexed.map((item) => {
    const reason = holdReason(item.row);
    const token = mintToken(usedTokens, randomInt);
    const status = reason ? 'held' : 'active';
    return {
      id: item.id,
      game_slug: item.slug,
      edition: item.edition,
      source_game_key: item.row.source_game_key.trim(),
      display_name: item.row.display_name.trim(),
      token,
      status,
      hold_reason: reason,
      destination: item.destination,
      deployment_id: item.deploymentId,
      source_version: typeof item.row.source_version === 'string' ? item.row.source_version.trim() : '',
      notes: typeof item.row.notes === 'string' ? item.row.notes.trim() : '',
      path: `/${item.slug}/${token}`,
      play_url: `https://play.reviewrecess.com/${item.slug}/${token}`,
      created_at: createdAt,
      updated_at: createdAt,
      history: [
        {
          at: createdAt,
          action: 'create',
          destination: item.destination,
          deployment_id: item.deploymentId,
          source_version: typeof item.row.source_version === 'string' ? item.row.source_version.trim() : '',
          note: reason
            ? 'Token reserved. Route is held and is not in the active map.'
            : 'Initial destination from the deployment inventory. Token is permanent.',
        },
      ],
    };
  });

  return {
    schema: 1,
    host: 'play.reviewrecess.com',
    created_at: createdAt,
    updated_at: createdAt,
    notes: [
      'Tokens are unlisted bearer access to a product edition. They are not purchase authentication.',
      'A product update changes destination only. The token stays. A new edition is a new token.',
      'Picture themes are not editions.',
      'word-morph and telling-time have only the edition listed in the inventory.',
      'adverb-game editions stay held until the product names are confirmed.',
    ],
    editions,
  };
}

export function findEdition(registry, id) {
  const edition = registry.editions.find((item) => item.id === id);
  if (!edition) throw new RegistryError(`unknown edition ${id}`);
  return edition;
}

export function activeMap(registry) {
  const routes = {};
  for (const edition of registry.editions) {
    if (edition.status !== 'active') continue;
    if (!isToken(edition.token) || !isAllowedDestination(edition.destination)) continue;
    routes[`${edition.game_slug}/${edition.token}`] = edition.destination;
  }
  return { schema: 1, routes };
}

function applyDestination(edition, fields, action, now, note) {
  const destination = String(fields.destination || '').trim();
  if (!isAllowedDestination(destination)) {
    throw new RegistryError(`${edition.id} destination is not an allowlisted script.google.com /exec URL`);
  }
  const deploymentId = String(fields.deploymentId || fields.deployment_id || '').trim();
  if (deploymentId !== deploymentIdFromDestination(destination)) {
    throw new RegistryError(`${edition.id} deployment_id does not match its destination`);
  }
  if (destination === edition.destination && deploymentId === edition.deployment_id) {
    throw new RegistryError(`${edition.id} destination is unchanged; this is not a new edition`);
  }
  const at = now();
  const previous = edition.destination;
  const token = edition.token;
  edition.destination = destination;
  edition.deployment_id = deploymentId;
  if (typeof fields.sourceVersion === 'string') edition.source_version = fields.sourceVersion.trim();
  edition.updated_at = at;
  edition.history.push({
    at,
    action,
    destination,
    deployment_id: deploymentId,
    source_version: edition.source_version,
    previous_destination: previous,
    note: note || (action === 'rollback'
      ? 'Restored the previous destination. Token unchanged.'
      : 'Destination updated. Token unchanged.'),
  });
  if (edition.token !== token) throw new RegistryError(`${edition.id} token changed`);
}

/**
 * Point an existing edition at a new Apps Script deployment.
 * The token, slug, and edition id do not change.
 */
export function updateDestination(registry, id, fields) {
  const edition = findEdition(registry, id);
  const now = fields.now || (() => new Date().toISOString());
  applyDestination(edition, fields, 'update-destination', now, fields.note);
  registry.updated_at = edition.updated_at;
  return registry;
}

/** Restore the destination recorded immediately before the latest history entry. */
export function rollbackDestination(registry, id, fields = {}) {
  const edition = findEdition(registry, id);
  if (edition.history.length < 2) {
    throw new RegistryError(`${id} has no previous destination to restore`);
  }
  const previous = edition.history[edition.history.length - 2];
  const now = fields.now || (() => new Date().toISOString());
  applyDestination(edition, {
    destination: previous.destination,
    deploymentId: previous.deployment_id,
    sourceVersion: previous.source_version,
  }, 'rollback', now, fields.note);
  registry.updated_at = edition.updated_at;
  return registry;
}

/**
 * Add a brand-new product edition. Refuses ids that already exist.
 * Does not alter tokens of existing editions.
 */
export function addEdition(registry, fields, options = {}) {
  const slug = String(fields.game_slug || '').trim();
  const editionName = String(fields.edition || '').trim();
  const id = editionId(slug, editionName);
  if (registry.editions.some((item) => item.id === id)) {
    throw new RegistryError(`${id} already exists; update the destination instead of minting a token`);
  }
  const draft = buildRegistry({
    editions: [{
      game_slug: slug,
      edition: editionName,
      source_game_key: fields.source_game_key,
      display_name: fields.display_name,
      current_deployment_url: fields.destination || fields.current_deployment_url,
      deployment_id: fields.deployment_id,
      source_version: fields.source_version || '',
      notes: fields.notes || '',
    }],
  }, options);
  const created = draft.editions[0];
  const taken = new Set(registry.editions.map((item) => item.token));
  if (taken.has(created.token)) {
    throw new RegistryError(`${id} collided with an existing token`);
  }
  if (registry.editions.some((item) => item.deployment_id === created.deployment_id)) {
    throw new RegistryError(`${id} reuses a deployment id`);
  }
  registry.editions.push(created);
  registry.updated_at = created.created_at;
  return registry;
}

/** Publish a held edition without changing its token. */
export function publishHeld(registry, id, fields = {}) {
  const edition = findEdition(registry, id);
  if (edition.status !== 'held') throw new RegistryError(`${id} is not held`);
  const at = (fields.now || (() => new Date().toISOString()))();
  const token = edition.token;
  edition.status = 'active';
  edition.hold_reason = '';
  edition.updated_at = at;
  edition.history.push({
    at,
    action: 'publish',
    destination: edition.destination,
    deployment_id: edition.deployment_id,
    source_version: edition.source_version,
    note: fields.note || 'Naming confirmed. Token unchanged.',
  });
  if (edition.token !== token) throw new RegistryError(`${id} token changed`);
  registry.updated_at = at;
  return registry;
}
