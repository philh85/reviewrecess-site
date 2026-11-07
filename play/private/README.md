# Private registry directory

JSON files in this directory are gitignored. They hold unlisted play tokens and Apps Script destinations.

Do not commit them, and do not force-add them. This repository is public.

Keep a copy in a password manager or in the Cloudflare KV namespace (key `registry` for the full file, key `active` for the route map the worker reads). The worker does not read the `registry` key.

Mint tokens once with `node play/scripts/manage.mjs init`. A later product update uses `update-destination`. Rollback uses `rollback`. Neither command changes a token.
