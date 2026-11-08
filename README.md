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

## 🎬 Live Scrolltide Library & NotebookLM Video Overview

- **Live Product Library (`16 apps`):** [https://navigatorslab.com/](https://navigatorslab.com/)
- **NotebookLM Audio & Video Deep Dive (`16:9 MP4`):** [https://navigatorslab.com/tools/videos/notebooklm-overview.mp4](https://navigatorslab.com/tools/videos/notebooklm-overview.mp4)
- **24-Tool Interactive Video & Output Showcase:** [https://navigatorslab.com/tools/#library](https://navigatorslab.com/tools/#library)
- **Worker Home Verification Suite (`29/29 checks`):** `python worker-home/verify.py`
