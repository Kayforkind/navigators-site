# Deploying reimagine on navigatorslab.com — runbook

Status as of Sep 7, 2026 — measured, not aspirational.

**Decision (Sep 7):** reimagine lives **on the main site** as a path —
`https://navigatorslab.com/reimagine/` — exactly like `/tools/`. No new
subdomain, no DNS records needed at all. The earlier subdomain plan
(`reimagine.navigatorslab.com`) is retired; its Pages-domain attach was
never validated and is inert (delete it in the dashboard whenever).

| Surface | State |
|---|---|
| `navigatorslab.com/reimagine/` | **live** — worker `reimagine-lab` proxies the reimagine-it GitHub Pages origin |
| `/reimagine` (no slash) and `/Reimagine` | 301 → `/reimagine/` (case-insensitive match on the first segment) |
| Pages project `navigators` | still live at https://navigators-dvr.pages.dev/ (origin of record for the landing page) |
| Stale `reimagine.navigatorslab.com` attach | inert — dashboard-only cleanup |

## How it works

Two zone routes on the already-proxied `navigatorslab.com` hostname send
`/reimagine*` and `/Reimagine*` to the `reimagine-lab` worker, which
proxies `https://kayforkind.github.io/reimagine-it/…` (path joined
manually, mount prefix stripped, redirect Location rewritten back under
`/reimagine`). Zone routes need **no DNS changes** — the hostname is
already proxied. This is the same mechanism `/tools/` uses.

## Redeploys

```bash
# reimagine docs proxy — from this repo
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID \
  npx wrangler deploy --config worker/wrangler.toml

# Pages (landing page origin of record) — from the repo root
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID \
  npx wrangler pages deploy . --project-name navigators --branch main
```

The docs content itself deploys independently: pushes to
`Kayforkind/reimagine-it` main rebuild GitHub Pages; the proxy picks the
new content up automatically (cache max-age 600).

## Adding a new external path like this (the pattern)

1. Deploy a worker (or reuse one) that proxies the origin.
2. `POST /zones/{zone_id}/workers/routes` with pattern
   `navigatorslab.com/<path>*` → script name. Done — no DNS.
3. If the path should be discoverable from the hub, add it to
   `public/tools.json` with a `url:` field (the grid honors `url`
   instead of `./<id>.html`).

## Why not a subdomain

A same-account Pages custom domain needs a CNAME record in the zone.
Every Cloudflare credential available locally is Pages/Workers/AI-scoped
(wrangler's OAuth catalog has no DNS scope at all), so the record could
not be created programmatically. The path approach removes the
dependency entirely.
