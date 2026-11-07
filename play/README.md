# play.reviewrecess.com

Permanent game links for Review Recess. A link looks like:

`https://play.reviewrecess.com/<game-slug>/<12-character-token>`

The worker answers with **HTTP 302** to that edition's Google Apps Script `/exec` URL and sets `Cache-Control: no-store`. Unknown paths, folder roots (`/answer-armada/`), the site root, `robots.txt`, and `sitemap.xml` return a plain `Not found` with no list of games or tokens.

This is a Cloudflare Worker on the **same Cloudflare zone that already serves the website**. It is not a second website, and it is not a custom domain on the Pages project. The marketing site stays on Pages. `play.reviewrecess.com` had **no DNS record** when this was added; nothing in this repo can create that record.

## What is public, and what is not

The GitHub repository is public. The route map is a bearer secret, so it is **not** committed.

| Data | Where it lives |
|---|---|
| Worker code, allowlist, tests | this directory (public) |
| Token, destination, and history | `play/private/registry.json` (gitignored) and KV key `registry` |
| Map the worker reads | KV key `active` only |

Tokens are unlisted access to a product edition. They do not prove that someone bought the product.

## Rules baked into the worker

- Destination host must be `script.google.com` and the path must be `/macros/s/<id>/exec`. Anything else is a 404.
- Query strings are dropped. No `url`, `redirect`, or other parameter can change the destination.
- Live mode is not shipped. `APPROVED_JOIN_PARAMS` in `src/policy.js` is empty on purpose. A future join code is added there as an exact name plus a value pattern. Until then, nothing is forwarded.
- The only accepted host is `play.reviewrecess.com`.
- Adverb-game editions (full display name "What Does It Modify?", free display name "Word Magnets") are **held**. Their tokens exist in the private registry and are not in the active map until the names are confirmed. Do not run `publish-held` before that.
- Word Morph and What's the Time each have the one full edition from the inventory. Picture themes are not editions.
- Answer Armada free, the grade-3 multiplication and division pack, and the editable edition are three editions and three tokens.

## Commands

From the repository root, with the private inventory file you were given (it is not in git):

```bash
node play/scripts/manage.mjs init --inventory /path/to/store-editions.json --out play/private/registry.json
node play/scripts/manage.mjs export-active --registry play/private/registry.json --out play/private/active-map.json
node --test play/test/*.test.js
```

`init` refuses to run if the registry file already exists, so it cannot silently replace tokens.

Update the same edition to a new Apps Script deployment (token stays):

```bash
node play/scripts/manage.mjs update-destination \
  --registry play/private/registry.json \
  --id answer-armada:free \
  --destination 'https://script.google.com/macros/s/NEW_DEPLOYMENT_ID/exec' \
  --deployment-id NEW_DEPLOYMENT_ID \
  --source-version @7
node play/scripts/manage.mjs export-active --registry play/private/registry.json --out play/private/active-map.json
```

Then write the new `active-map.json` to KV (command in the next section). Do not delete the old Apps Script deployment.

Rollback the last destination change:

```bash
node play/scripts/manage.mjs rollback --registry play/private/registry.json --id answer-armada:free
node play/scripts/manage.mjs export-active --registry play/private/registry.json --out play/private/active-map.json
```

History is the `history` array on that edition, newest last. Rollback copies the destination from the entry before the latest one and appends a `rollback` entry. Put the exported active map into KV again. KV reads can stay cached for about 60 seconds, so check the `Location` header again after a minute. The token in the path does not change.

A brand-new product edition (not an update) is `add-edition`, which mints a new token and leaves every existing token alone.

## Deploy on the existing Cloudflare account

Use the Cloudflare account that already hosts the zone. The live nameservers are `junade.ns.cloudflare.com` and `selah.ns.cloudflare.com`. Leave MX, SPF, and the existing Pages project alone. The apex host currently 301-redirects to `www.reviewrecess.com`; do not change that rule as part of this work.

1. Install Wrangler and log in with that account: `npx wrangler login`.
2. From `play/`: `npx wrangler kv namespace create PLAY_MAP`.
3. Paste the namespace id into `play/wrangler.toml` and uncomment the `[[kv_namespaces]]` block. Commit that id only (it is not a secret). Do not commit `play/private/*.json`.
4. `npx wrangler deploy` from `play/`. `workers_dev` is false, so this does not publish a `*.workers.dev` URL.
5. In the dashboard: Workers & Pages → `reviewrecess-play` → Settings → Domains & Routes → Add → Custom domain → `play.reviewrecess.com`.

   That button creates the proxied DNS record. Do not attach this hostname to the Pages project named in the site README, or the marketing homepage will be served here and these redirects will not run.

The full private registry is about 40 KB, so it does not fit in a Worker secret (5 KB limit). The compact active map is about 4 KB today. Use KV for both, so later editions do not outgrow a secret and so a destination change does not require a new Worker version.

6. Upload the maps:

   ```bash
   npx wrangler kv key put --namespace-id PASTE_NAMESPACE_ID active --path play/private/active-map.json
   npx wrangler kv key put --namespace-id PASTE_NAMESPACE_ID registry --path play/private/registry.json
   ```

   The second key is a private backup. The worker never reads it.

7. Prove it before sending the links to anyone:

   ```bash
   curl -sI "https://play.reviewrecess.com/answer-armada/FREE_TOKEN"
   curl -sI "https://play.reviewrecess.com/"
   curl -sI "https://play.reviewrecess.com/answer-armada/"
   curl -sI "https://play.reviewrecess.com/answer-armada/FREE_TOKEN?next=https://example.com"
   ```

   The free token request must be **302**, `cache-control: no-store`, and `location` exactly the free edition's `/exec` URL with no query string. The other three must be **404** with the body `Not found` and no list of games. This repository cannot do that check until the custom domain exists.

8. Only after step 7 succeeds, upload the `site/` folder to the **existing** Pages project so the Answer Armada "Play the free version now" button goes live. Paid play URLs stay out of the website.

9. After that same 302 check, update TpT kits by replacing each product's `/exec` link with the play URL for that edition. Do not rebuild game source and do not delete old script deployments as part of the URL swap. Kit files are not in this repo.

## Tests

`node --test play/test/*.test.js`

Covers per-edition routing, 302 and no-store headers, bad tokens, folder roots, no directory or sitemap, query stripping, the join-parameter hook, held adverb routes, and rollback. If `play/private/registry.json` is present, the private-registry test checks that file too. It is not in git, so CI without the file skips that one test.
