# navigators-site

The [NavigatorLabs](https://navigatorslab.com) landing site — **one static
HTML file, zero external fetches**, scoring **19/19 CLEAN** on
[reimagine-it](https://github.com/Kayforkind/reimagine-it)'s own deterministic
design audit (the lab eats its own cooking).

Deployed to **[navigators.com](https://navigators.com)** on Cloudflare Pages.
Runbook: [DEPLOY.md](DEPLOY.md).

## Contents

| File | What it is |
|---|---|
| `index.html` | The landing site (single file, self-contained, offline) |
| `one-pager.html` | Client-facing one-pager (print to PDF at Letter size) |
| `NavigatorLabs-one-pager.pdf` | The rendered PDF |
| `ORG-README.md` | Profile text for the NavigatorLabs GitHub account |
| `NOMINATIONS.md` | Paste-ready submissions for directories/newsletters |
| `deploy.sh` | Idempotent Cloudflare Pages deploy + optional domain attach |
| `DEPLOY.md` | The exact runbook (token scopes, DNS, verification) |

## Local check

```bash
npx reimagine-it audit index.html   # expect: 19 passed, 0 warnings, 0 failures
```
