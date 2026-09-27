# Homepage worker (`navigatorslab-home`)

Serves the Netflix-style NavigatorLabs site: the homepage at the **exact root**
`https://navigatorslab.com/` plus a dedicated page per app at
`https://navigatorslab.com/apps/<slug>/`.

## How it works

- `build_site.py` is the source of truth: the `APPS` table (8 verified products —
  every example and feature drawn from the repos/docs, nothing invented) generates
  `dist/home.html`, `dist/apps/<slug>.html` and `dist/style.css`.
- `deploy.py` rebuilds via `build_site.py`, embeds everything into `dist/worker.js`,
  uploads it as the `navigatorslab-home` worker, and ensures the zone routes
  `navigatorslab.com/` and `navigatorslab.com/apps*`.
- Both routes are more specific than the existing `navigatorslab.com/*` catch-all,
  so only `/` and `/apps/*` are served here. Everything else — `/tools/`,
  `/pdf-studio/`, `/Integrationrot`, `/mcp`, `/reimagine/` — keeps flowing to its
  existing worker untouched.
- The existing `navigatorslab-tools` worker was **not modified** (its static
  assets are bound to its deployment; re-uploading its script via API could
  orphan them).
- Zero JavaScript, zero external fetches — all motion is CSS (the strict CSP has
  no `unsafe-inline` for scripts).

## Files

| File | Purpose |
|---|---|
| `build_site.py` | Source of truth: app data + templates → `dist/` |
| `deploy.py` | Builds, uploads worker, ensures routes. Env: `NAV_HOME_WORKER` (default `navigatorslab-home`), `NAV_HOME_SKIP_ROUTES=1` to skip route changes (staging) |
| `verify.py` | Post-deploy checks: homepage, all 8 app pages, old surfaces intact |
| `rollback.py` | Removes both routes — the catch-all immediately serves everything again |

## Redeploy

```bash
cd worker-home
python3 deploy.py   # builds + uploads worker + ensures routes
python3 verify.py   # confirm homepage + app pages + old surfaces
```

Staging (does not touch the live site):

```bash
NAV_HOME_WORKER=navigatorslab-home-staging NAV_HOME_SKIP_ROUTES=1 python3 deploy.py
# preview at https://navigatorslab-home-staging.kazim-r-merchant.workers.dev/
```

Auth uses the vault-backed `custom.cloudflare` credential. Rollback is one call:
`python3 rollback.py`.

## Quality bar

- No invented products, no repeated copy: each card has unique art and each
  detail page has unique examples.
- Every number on the site is measured, not remembered (see `scripts/`).
