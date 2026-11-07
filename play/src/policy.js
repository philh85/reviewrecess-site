/**
 * Redirect policy for play.reviewrecess.com.
 *
 * Destinations are allowlisted to a Google Apps Script web app /exec URL.
 * Live mode is not available yet, and this repo does not define a join code,
 * so no query parameter is approved. The list below is the only place a
 * future join parameter may be added. Request query strings are never copied
 * through as a whole.
 */

export const PLAY_HOST = 'play.reviewrecess.com';

/** Unambiguous URL-safe alphabet: no 0/O/o, 1/I/l/L/i. */
export const TOKEN_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789';
export const TOKEN_LENGTH = 12;

export const DESTINATION_PATTERN = /^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/;

/**
 * Approved live-mode join parameters.
 * Each entry is { name, pattern }. Values that fail the pattern are dropped.
 * Keep this empty until a real join parameter ships with live mode.
 */
export const APPROVED_JOIN_PARAMS = Object.freeze([]);

const THEME_EDITIONS = new Set([
  'theme',
  'classic',
  'dino',
  'sea',
  'skeleton',
  'baby',
  'bear',
  'jack',
  'high-contrast',
  'picture-style',
]);

/** Slugs already used on reviewrecess.com, plus the two single-edition games in the deployment inventory. */
export const WELL_KNOWN_SLUGS = new Set([
  'answer-armada',
  'brain-board-blitz',
  'five-second-battle',
  'forbidden-words',
  'letter-lifeline',
  'million-point-climb',
  'mystery-cat',
  'pass-the-bomb',
  'sentence-slot-machine',
  'sentence-snap',
  'telling-time',
  'tic-tac-toe-quiz-game',
  'word-magnets',
  'word-morph',
  'word-scramble',
]);

export const PRIORITY_EDITION_IDS = Object.freeze([
  'answer-armada:free',
  'answer-armada:grade-3-multiplication-division-facts',
  'answer-armada:editable',
]);

export function isToken(value) {
  return typeof value === 'string'
    && value.length === TOKEN_LENGTH
    && [...value].every((ch) => TOKEN_ALPHABET.includes(ch));
}

export function isAllowedDestination(value) {
  if (typeof value !== 'string' || !DESTINATION_PATTERN.test(value)) return false;
  let url;
  try {
    url = new URL(value);
  } catch {
    return false;
  }
  if (url.protocol !== 'https:') return false;
  if (url.username || url.password || url.port) return false;
  if (url.hostname !== 'script.google.com') return false;
  if (url.search || url.hash) return false;
  if (!/^\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(url.pathname)) return false;
  return url.href === value || url.toString() === value;
}

export function deploymentIdFromDestination(value) {
  if (!isAllowedDestination(value)) return '';
  return value.split('/')[5] || '';
}

export function isThemeEdition(edition) {
  return THEME_EDITIONS.has(String(edition || '').toLowerCase());
}

export function isAdverbSource(sourceGameKey) {
  const key = String(sourceGameKey || '');
  return key === 'adverb-game' || key.startsWith('adverb-game-');
}

/**
 * Copy only explicitly approved join parameters onto a destination.
 * Returns the original destination string when nothing is approved, so the
 * stored URL is not re-encoded. Returns null when the destination itself is
 * not allowlisted.
 */
export function locationFor(destination, searchParams, joinParams = APPROVED_JOIN_PARAMS) {
  if (!isAllowedDestination(destination)) return null;
  const rules = Array.isArray(joinParams) ? joinParams : [];
  if (rules.length === 0) return destination;
  const url = new URL(destination);
  for (const rule of rules) {
    if (!rule || typeof rule.name !== 'string' || !(rule.pattern instanceof RegExp)) continue;
    if (rule.name !== rule.name.trim() || rule.name.includes('=') || rule.name.includes('&')) continue;
    const values = searchParams.getAll(rule.name);
    if (values.length !== 1) continue;
    if (!rule.pattern.test(values[0])) continue;
    url.searchParams.append(rule.name, values[0]);
  }
  if (url.username || url.password || url.hostname !== 'script.google.com') return null;
  if (!/^\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(url.pathname)) return null;
  return url.toString();
}
