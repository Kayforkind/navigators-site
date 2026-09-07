# Deploying navigators.com

The site is **one static file** (`index.html`, zero external fetches, 19/19 on
reimagine-it's own design audit). This doc is the exact runbook.

## Current state (measured Sep 7, 2026)

| Host | What serves it today |
|---|---|
| `navigatorslab.com` | Cloudflare (CF-Cache-Status header) — PDF Studio landing + `/tools/`. **Untouched by this work; stays as is.** |
| `navigators.com` | 2017 Apache/AlmaLinux box serving "Russ Haynal - Internet Instructor" HTML 3.2 — **this is what we replace** |
| `www.navigators.com` | Same old box |

## 0. One-time token fix (the only blocker)

The `CLOUDFLARE_API_TOKEN` in the environment is **valid but too narrow** — it
authenticates yet returns zero zones, zero accounts, and an authentication
error on Pages. Wrangler cannot deploy with it.

Fix in the Cloudflare dashboard → *My Profile → API Tokens*. Either edit the
existing token or create one with **minimum**:

| Permission | Why |
|---|---|
| Account · Account Settings · Read | wrangler account resolution |
| Account · Cloudflare Pages · **Edit** | create project + deploy |
| Zone · Zone · Read | find the `navigators.com` zone |
| Zone · DNS · Edit | add the CNAME for the custom domain |

Then set the zone scope to *All zones* (or at least `navigators.com`).

**Is navigators.com even in this Cloudflare account?** Check with:

```bash
curl -s -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=navigators.com"
```

- `count: 1` → good, go to step 1.
- `count: 0` after the token fix → the domain is still on registrar default
  nameservers / another provider. Add it: dashboard → *Add a site* →
  `navigators.com` → follow the nameserver change at the registrar. Once the
  zone is active in Cloudflare, go to step 1.

## 1. Deploy (one command)

```bash
cd D:/Projects/navigators-site
bash deploy.sh
```

Creates the Pages project `navigators-labs`, uploads this directory as the
production deployment, and prints the `*.pages.dev` URL. Idempotent — safe to
re-run.

## 2. Attach the domain

```bash
bash deploy.sh --attach
```

Adds `navigators.com` as a Pages custom domain and creates the proxied apex
CNAME → `navigators-labs.pages.dev`. Cloudflare issues the edge certificate
automatically (give it a couple of minutes).

If the old Apache host still holds the DNS records, delete the stale `A`/`AAAA`
records for `@` and `www` in the DNS tab (or re-point them per Cloudflare's
prompt when adding the custom domain).

## 3. Verify

```bash
curl -sI https://navigators.com | head -4          # server: cloudflare + 200
curl -s  https://navigators.com | grep -c NavigatorLabs
curl -s https://navigators.com | head -c 300       # new title
```

## 4. Optional: git-connected auto-deploy

Direct upload is fine for a one-file site. If you want pushes to auto-deploy,
connect the repo in the Pages dashboard (*Set up a Git integration*) — the
`github.com/Kayforkind/navigators-site` repo is the deployable source, build
command empty, output dir `/`.

## Repo

Everything in this folder belongs on GitHub (`Kayforkind/navigators-site`):
`index.html` (the site), `one-pager.html` + `NavigatorLabs-one-pager.pdf`
(client one-pager), `ORG-README.md` (NavigatorLabs account profile text),
`NOMINATIONS.md` (submissions kit), this runbook, `deploy.sh`.
