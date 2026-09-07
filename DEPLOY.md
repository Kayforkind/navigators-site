# Deploying the lab landing (reimagine.navigatorslab.com)

Status as of Sep 7, 2026 — measured, not aspirational.

| Surface | State |
|---|---|
| Pages project `navigators` | live at https://navigators-dvr.pages.dev/ (origin of record) |
| Worker `reimagine-lab` (assets mirror) | live at https://reimagine-lab.kazim-r-merchant.workers.dev/ |
| `reimagine.navigatorslab.com` | attached to the Pages project, **pending CNAME** |

## The one remaining step (owner, 30 seconds)

Cloudflare dashboard → navigatorslab.com → DNS → Records → **Add record**:

    Type:   CNAME
    Name:   reimagine
    Target: navigators-dvr.pages.dev
    Proxy:  ON (orange cloud)

The Pages domain then validates automatically and the certificate is issued
(1–5 min). The site is **public** — the earlier "locked to owner" plan was
dropped by decision (Sep 7): the audience flows from GitHub (README quick-nav
row + docs footer funnel link) to this page.

## Why the CNAME could not be automated

Every Cloudflare credential available locally is Pages/Workers/AI-scoped:
wrangler's OAuth catalog has no DNS scope at all (`zone:read` only), and the
vault tokens are Pages/AI-scoped. Workers custom-domain attach (which would
auto-create DNS) is API-token-only (`10405: Method not allowed for this
authentication scheme` under OAuth). A token with **Zone · DNS · Edit**
(navigatorslab.com) would let future deploys add records programmatically.

## Redeploys

```bash
# Pages (origin of record) — from the repo root
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID \
  npx wrangler pages deploy . --project-name navigators --branch main

# Worker mirror — from the worker/ directory
env -u CLOUDFLARE_API_TOKEN -u CLOUDFLARE_ACCOUNT_ID npx wrangler deploy
```

`worker/` contains wrangler.toml + public/index.html (a copy of the root
index.html — keep the two in sync on edits, or drop the mirror).
