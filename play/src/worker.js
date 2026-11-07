import { handlePlayRequest, loadActiveMap } from './redirect.js';

/**
 * Cloudflare Worker for play.reviewrecess.com only.
 * The marketing site stays on the existing Pages project. This worker reads
 * the active route map from the PLAY_MAP KV key "active" (or, for a local
 * binding, the PLAY_MAP_JSON secret). It never reads a full registry and it
 * has no list, homepage, or sitemap.
 */
export default {
  async fetch(request, env) {
    const map = await loadActiveMap(env);
    return handlePlayRequest(request, map);
  },
};
