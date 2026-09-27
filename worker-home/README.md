# Homepage worker (`navigatorslab-home`)

Serves the NavigatorLabs landing page at the **exact root** `https://navigatorslab.com/`.

## How it works

- Worker `navigatorslab-home` embeds `landing.html` and returns it for `GET /`.
- Zone route `navigatorslab.com/` (exact path) is more specific than the
  existing `navigatorslab.com/*` catch-all, so **only `/`** is served by this
  worker. Everything else — `/tools/`, `/pdf-studio/`, `/Integrationrot`,
  `/mcp`, `/reimagine/` — keeps flowing to its existing worker untouched.
- The existing `navigatorslab-tools` worker was **not modified** (its static
  assets are bound to its deployment; re-uploading its script via API could
  orphan them).

## Files

| File | Purpose |
|---|---|
| `landing.html` | Source of truth for the homepage. Single static file: no JS, no external fetches. |
| `deploy.py` | Builds the worker (embeds `landing.html`), uploads it, and ensures the `navigatorslab.com/` zone route exists. |
| `verify.py` | Post-deploy checks: new landing at `/`, old surfaces intact. |
| `rollback.py` | Removes the `navigatorslab.com/` route — the catch-all immediately serves `/` again. |

## Redeploy

```bash
cd worker-home
python3 deploy.py   # builds + uploads worker + ensures route
python3 verify.py   # confirm root + all other surfaces
```

Auth uses the vault-backed `custom.cloudflare` credential (same as the
integration-rot worker deploys). Rollback is one call: `python3 rollback.py`.

## Design notes

- Black/glass editorial aesthetic, teal/cyan aurora, serif display accents.
- Zero JavaScript: all motion is CSS (page must keep working under the strict
  CSP, which has no `unsafe-inline` for scripts).
- Keep the six proof numbers honest — every stat on the page is measured in
  this repo's scripts (`scripts/check-links.cjs`, `scripts/verify-claims.cjs`),
  not remembered.
