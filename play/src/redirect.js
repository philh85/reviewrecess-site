import { APPROVED_JOIN_PARAMS, PLAY_HOST, locationFor } from './policy.js';

const NOT_FOUND_BODY = 'Not found\n';

const BASE_HEADERS = Object.freeze({
  'Cache-Control': 'no-store',
  'CDN-Cache-Control': 'no-store',
  'Cloudflare-CDN-Cache-Control': 'no-store',
  'Expires': '0',
  'Pragma': 'no-cache',
  'Referrer-Policy': 'no-referrer',
  'X-Content-Type-Options': 'nosniff',
  'X-Robots-Tag': 'noindex, nofollow, noarchive',
  'Content-Security-Policy': "default-src 'none'; frame-ancestors 'none'",
  'X-Frame-Options': 'DENY',
});

function notFound(method) {
  return new Response(method === 'HEAD' ? null : NOT_FOUND_BODY, {
    status: 404,
    headers: {
      ...BASE_HEADERS,
      'Content-Type': 'text/plain; charset=utf-8',
    },
  });
}

function redirect(location) {
  return new Response(null, {
    status: 302,
    headers: {
      ...BASE_HEADERS,
      Location: location,
    },
  });
}

export function normalizeMap(input) {
  const routes = Object.create(null);
  const source = input && typeof input === 'object' ? input.routes : null;
  if (!source || typeof source !== 'object') return { routes };
  for (const [key, value] of Object.entries(source)) {
    if (!/^[a-z0-9]+(?:-[a-z0-9]+)*\/[A-Za-z0-9]{12}$/.test(key)) continue;
    const location = locationFor(value, new URLSearchParams());
    if (!location) continue;
    routes[key] = value;
  }
  return { routes };
}

export async function loadActiveMap(env) {
  try {
    if (env && env.PLAY_MAP && typeof env.PLAY_MAP.get === 'function') {
      const text = await env.PLAY_MAP.get('active');
      if (typeof text === 'string' && text.trim()) return normalizeMap(JSON.parse(text));
    }
    if (env && typeof env.PLAY_MAP_JSON === 'string' && env.PLAY_MAP_JSON.trim()) {
      return normalizeMap(JSON.parse(env.PLAY_MAP_JSON));
    }
  } catch {
    console.error('play map unavailable');
  }
  return normalizeMap(null);
}

function parsePlayPath(pathname) {
  const match = pathname.match(/^\/([a-z0-9]+(?:-[a-z0-9]+)*)\/([A-Za-z0-9]{12})\/?$/);
  if (!match) return null;
  return { slug: match[1], token: match[2] };
}

/**
 * Resolve one play-host request to a 302 or a generic 404.
 * `map` is `{ routes: { "slug/token": "https://script.google.com/macros/s/.../exec" } }`.
 * `joinParams` defaults to the production allowlist (empty).
 */
export function handlePlayRequest(request, map, options = {}) {
  const method = request.method || 'GET';
  if (method !== 'GET' && method !== 'HEAD') return notFound(method);

  let url;
  try {
    url = new URL(request.url);
  } catch {
    return notFound(method);
  }

  if (url.hostname !== PLAY_HOST) return notFound(method);
  if (url.pathname.length > 80) return notFound(method);
  if (url.pathname.includes('\\') || url.pathname.includes('//')) return notFound(method);
  const pathOnly = request.url.split('?')[0];
  if (/%[0-9a-fA-F]{2}/.test(pathOnly)) return notFound(method);

  const parsed = parsePlayPath(url.pathname);
  if (!parsed) return notFound(method);

  const routes = map && map.routes ? map.routes : Object.create(null);
  const destination = routes[`${parsed.slug}/${parsed.token}`];
  const location = locationFor(destination, url.searchParams, options.joinParams || APPROVED_JOIN_PARAMS);
  if (!location) return notFound(method);
  return redirect(location);
}
