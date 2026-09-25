# navigators-site

The [NavigatorLabs](https://navigatorslab.com) landing site — **one static
HTML file, zero external fetches**, scoring **19/19 CLEAN** on
[reimagine-it](https://github.com/Kayforkind/reimagine-it)'s own deterministic
design audit (the lab eats its own cooking).

Deployed to **[navigatorslab.com](https://navigatorslab.com)** on Cloudflare Pages
(origin of record: the `navigators` Pages project — see DEPLOY.md). The
`navigators.com` domain is **not owned by the lab** and must not be referenced
as a lab surface.

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
