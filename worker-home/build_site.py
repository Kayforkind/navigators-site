#!/usr/bin/env python3
"""Build the NavigatorLabs Product Library site (navigatorslab-home worker).

Generates dist/home.html, dist/style.css, dist/apps/<slug>.html, and dist/worker.js
from the 16 verified public products in PRODUCTS below.
Every product carries its real GitHub repository URL, version, live app link (where
hosted on navigatorslab.com), and an explicit limitation caveat.
"""
from __future__ import annotations

import html as html_lib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

PRODUCTS = [
    {
        "slug": "reimagine-it",
        "repo": "reimagine-it",
        "name": "reimagine-it",
        "version": "v2.15.0",
        "platform": "CLI + Web + MCP",
        "live_url": "/reimagine/",
        "live_label": "Open playground",
        "description": "Rebuild web-page design from its own content, preserving source facts, numbers, dates and meaning across 17 deterministic directions.",
        "caveat": "Design generation should be reviewed against the source page.",
    },
    {
        "slug": "integration-rot",
        "repo": "integration-rot",
        "name": "integration-rot",
        "version": "v0.4.4",
        "platform": "Developer CLI + MCP",
        "live_url": "/Integrationrot",
        "live_label": "Open docs & waitlist",
        "description": "Find uses of aging APIs across 76 SDK packages, draft migrations and verify changes with generated contract tests.",
        "caveat": "Review generated migrations and test assumptions before merging.",
    },
    {
        "slug": "pdf-studio",
        "repo": "NavigatorsLab-PDF-Studio",
        "name": "PDF Studio",
        "version": "v1.2.0",
        "platform": "Browser app + CLI + MCP",
        "live_url": "/pdf-studio/",
        "live_label": "Open PDF Studio",
        "description": "A 100% client-side PDF editor for true content-stream text edits, AcroForms, OCR, signing, vector redaction and revision comparison.",
        "caveat": "Keep a verified original and review exported documents before sharing.",
    },
    {
        "slug": "tools",
        "repo": "NavigatorsLab-Tools",
        "name": "24 Tools",
        "version": "v1.8.0",
        "platform": "Browser tools + MCP",
        "live_url": "/tools/",
        "live_label": "Open 24 Tools",
        "description": "Twenty-four local-first utilities for images, PDFs, receipts, EXIF privacy, OCR, passwords and everyday documents — nothing leaves your device.",
        "caveat": "Review each tool’s limits before relying on its output.",
    },
    {
        "slug": "redact-lint",
        "repo": "redact-lint",
        "name": "redact-lint",
        "version": "v0.3.2",
        "platform": "Rust CLI + Python + Action",
        "description": "Catch fake PDF redactions before they ship — detects painted-over black rectangles where underlying text streams remain extractable.",
        "caveat": "Scans extractable PDF text streams and vector geometry; raster-only image leaks require OCR review.",
    },
    {
        "slug": "liecatchers",
        "repo": "liecatchers",
        "name": "liecatchers",
        "version": "v0.2.0",
        "platform": "Developer CLI",
        "description": "Collect workspace signals across ten sensors and emit signed RECEIPT.json files to review an coding agent’s completion claims.",
        "caveat": "A signed receipt is evidence from its signer, not independent proof of execution.",
    },
    {
        "slug": "book-guide-mcp",
        "repo": "book-guide-mcp",
        "name": "book-guide-mcp",
        "version": "v0.2.0",
        "platform": "MCP server",
        "description": "Turn trusted books and frameworks into agent-callable playbooks, Socratic tutors and cited locators.",
        "caveat": "Check citations and source permissions; generated guidance needs human review.",
    },
    {
        "slug": "design-health-action",
        "repo": "design-health-action",
        "name": "design-health-action",
        "version": "v1.0.1",
        "platform": "GitHub Action",
        "description": "Eighteen deterministic design-quality checks for pull requests and continuous integration — no LLM or API key required.",
        "caveat": "Automated checks do not replace visual and accessibility review.",
    },
    {
        "slug": "api-watch",
        "repo": "api-watch",
        "name": "api-watch",
        "version": "v0.2.2",
        "platform": "Node 20+ CLI",
        "description": "API response contracts with secret-safe environment references, bounded reads and CI reports.",
        "caveat": "Targets are trusted configuration; this is not a public SSRF-safe URL proxy.",
    },
    {
        "slug": "pdf-a11y-check",
        "repo": "pdf-a11y-check",
        "name": "pdf-a11y-check",
        "version": "v1.1.2",
        "platform": "Node 20+ CLI",
        "description": "Bounded PDF accessibility pre-flight checks for language, tags, title, figure alternatives and tab order.",
        "caveat": "Heuristic pre-flight only — not PDF/UA certification or malware clearance.",
    },
    {
        "slug": "design-gate",
        "repo": "design-gate",
        "name": "design-gate",
        "version": "v1.1.2",
        "platform": "Node 20+ CLI",
        "description": "Bounded structural checks for generated HTML with escaped reports and configurable CI thresholds.",
        "caveat": "Not an HTML sanitizer or accessibility certification.",
    },
    {
        "slug": "skills-registry",
        "repo": "skills-registry",
        "name": "skills-registry",
        "version": "v1.1.2",
        "platform": "Node CLI + static HTML",
        "description": "Build a searchable static index of agent skills with heuristic risk checks and SHA-256 digests.",
        "caveat": "Risk patterns are heuristics; “checked” is not safety approval.",
    },
    {
        "slug": "share-safe",
        "repo": "share-safe",
        "name": "share-safe",
        "version": "v1.1.2",
        "platform": "Node 20+ CLI",
        "description": "Remove selected PDF metadata and actions, prune unreachable payloads and recheck the saved output.",
        "caveat": "Not full anonymization, content redaction, or malware scanning; manually review forms, annotations, visible content and media.",
    },
    {
        "slug": "privacy-plugin",
        "repo": "privacy-plugin",
        "name": "navigatorslab-privacy-tools",
        "version": "v0.2.2",
        "platform": "Claude Code plugin",
        "description": "Read-only local PDF parsing, extraction and search through bundled MCP tools.",
        "caveat": "Extracted text enters the AI client context and may reach its model provider.",
    },
    {
        "slug": "agent-receipts",
        "repo": "agent-receipts",
        "name": "agent-receipts",
        "version": "v0.2.2",
        "platform": "Node 20+ CLI",
        "description": "Record bounded check outcomes and root-confined artifact hashes; verify receipts and optional Ed25519 signatures.",
        "caveat": "Signatures show possession of a key, not that checks ran honestly; verification never executes commands.",
    },
    {
        "slug": "health-claims",
        "repo": "health-claims",
        "name": "sourced-claims",
        "version": "v0.1.2",
        "platform": "Node 20+ CLI",
        "description": "Validate sourced-claim data, calendar dates, human review fields and review freshness; render a safe report template.",
        "caveat": "Not medical advice or scientific evaluation; a passing schema does not establish claim truth.",
    },
]

BY_SLUG = {p["slug"]: p for p in PRODUCTS}

CSS = """:root{color-scheme:dark;--bg:#0b0b0f;--panel:#17171f;--line:#2b2b35;--text:#f5f5f7;--muted:#aaaab5;--accent:#2dd4bf}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.6 system-ui,-apple-system,Segoe UI,sans-serif}a{color:inherit}header,main,footer{max-width:1180px;margin:auto;padding:24px}header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line);gap:16px;flex-wrap:wrap}.brand{font-size:20px;font-weight:800;letter-spacing:.18em;color:var(--accent);text-decoration:none}.header-nav{display:flex;align-items:center;gap:14px;flex-wrap:wrap}.header-link{color:var(--muted);text-decoration:none;font-size:14px}.header-link:hover{color:var(--text)}.count{border:1px solid var(--line);border-radius:999px;padding:6px 14px;color:var(--muted);font-size:14px}.intro{padding:64px 24px 34px}h1{font-size:clamp(38px,7vw,76px);line-height:1.05;margin:10px 0 20px;letter-spacing:-.04em}.intro p,.lede{color:var(--muted);font-size:18px;max-width:760px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,270px),1fr));gap:16px;padding:0 24px 64px}.card,.story,.spec{background:var(--panel);border:1px solid var(--line);border-radius:16px}.card{padding:20px;text-decoration:none;display:flex;flex-direction:column;transition:transform .2s,border-color .2s}.card:hover{transform:translateY(-3px);border-color:var(--accent)}.card-top{display:flex;align-items:center;justify-content:space-between;gap:8px}.ver-pill{font-size:11px;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:2px 8px}.eyebrow{color:var(--accent);font-size:12px;font-weight:700;letter-spacing:.16em;text-transform:uppercase}.card h2{font-size:20px;margin:12px 0 7px;overflow-wrap:anywhere}.card p,.story p{color:var(--muted);margin:0}.caveat{margin-top:auto;padding-top:12px;border-top:1px solid var(--line);font-size:13px;color:#d2c9b0;margin-top:14px}.details{padding:42px 24px 80px}.back{color:var(--accent);text-decoration:none}.actions{display:flex;flex-wrap:wrap;gap:12px;margin:26px 0;align-items:center}.button{border-radius:9px;padding:11px 16px;background:var(--text);color:#101014;text-decoration:none;font-weight:700}.button-accent{background:var(--accent);color:#04211d}.button-ghost{border:1px solid var(--line);background:var(--panel);color:var(--text)}.specs{display:flex;flex-wrap:wrap;gap:10px;margin:28px 0}.spec{padding:12px 16px;min-width:150px}.spec b{display:block;color:var(--muted);font-size:11px;letter-spacing:.1em;text-transform:uppercase}.stories{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:14px;margin-top:34px}.story{padding:20px}.story h2{font-size:21px;margin:10px 0}.story .caveat{border:0;padding:0;font-size:14px}footer{border-top:1px solid var(--line);color:var(--muted);padding-top:28px;padding-bottom:40px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}@media(max-width:600px){header{padding:18px}.intro{padding:40px 20px 24px}.grid{padding:0 20px 48px}.details{padding:30px 20px 56px}}"""


def esc(s: str) -> str:
    return html_lib.escape(str(s or ""), quote=True)


def shell(title: str, body: str) -> str:
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="description" content="NavigatorLabs product library and product details.">'
        f"<title>{esc(title)}</title>"
        '<link rel="stylesheet" href="/apps/style.css"></head>'
        f"<body>{body}</body></html>"
    )


def render_home() -> str:
    cards = []
    for p in PRODUCTS:
        ver_html = f'<span class="ver-pill">{esc(p["version"])}</span>' if p.get("version") else ""
        cards.append(
            f'<a class="card" href="/apps/{p["slug"]}/" aria-label="{esc(p["name"])} details">'
            f'<div class="card-top"><span class="eyebrow">{esc(p["platform"])}</span>{ver_html}</div>'
            f'<h2>{esc(p["name"])}</h2>'
            f'<p>{esc(p["description"])}</p>'
            f'<div class="caveat">{esc(p["caveat"])}</div>'
            f"</a>"
        )
    cards_str = "".join(cards)
    body = (
        '<header>'
        '<a class="brand" href="/">NAVIGATORLABS</a>'
        '<div class="header-nav">'
        '<a class="header-link" href="/reimagine/">reimagine-it</a>'
        '<a class="header-link" href="/pdf-studio/">PDF Studio</a>'
        '<a class="header-link" href="/tools/">24 Tools</a>'
        '<a class="header-link" href="https://github.com/Kayforkind">GitHub</a>'
        f'<span class="count">{len(PRODUCTS)} apps · free · local-first</span>'
        '</div>'
        '</header>'
        '<main>'
        '<section class="intro">'
        '<span class="eyebrow">THE FULL CATALOG</span>'
        '<h1>Product library</h1>'
        '<p>Browse every tool, CLI, MCP server and browser app built by NavigatorsLab. '
        'Each product runs locally or client-side with zero uploads, and documents what it does, '
        'where its source lives, and its important operational limits.</p>'
        '</section>'
        f'<section class="grid" aria-label="All products">{cards_str}</section>'
        '</main>'
        '<footer>'
        '<span>NAVIGATORLABS · Free, local-first software. Review each product’s limitations before relying on its output.</span>'
        '<a class="back" href="https://github.com/Kayforkind">github.com/Kayforkind ↗</a>'
        '</footer>'
    )
    return shell("NavigatorLabs Product library", body)


def render_detail(p: dict) -> str:
    version = p.get("version") or "See repository"
    gh = f'https://github.com/Kayforkind/{p["repo"]}'
    live_btn = ""
    if p.get("live_url"):
        live_btn = (
            f'<a class="button button-accent" href="{esc(p["live_url"])}">'
            f'{esc(p.get("live_label", "Open live app"))} →</a>'
        )
    body = (
        '<header><a class="brand" href="/">NAVIGATORLABS</a><a class="back" href="/">‹ All apps</a></header>'
        '<main class="details">'
        f'<span class="eyebrow">{esc(p["platform"])}</span>'
        f'<h1>{esc(p["name"])}</h1>'
        f'<p class="lede">{esc(p["description"])}</p>'
        '<div class="actions">'
        f'{live_btn}'
        f'<a class="button" href="{esc(gh)}">View repository</a>'
        '<a class="back" href="#how">How it works ↓</a>'
        '</div>'
        '<div class="specs">'
        f'<div class="spec"><b>Version</b>{esc(version)}</div>'
        '<div class="spec"><b>License</b>MIT</div>'
        f'<div class="spec"><b>Platform</b>{esc(p["platform"])}</div>'
        f'<div class="spec"><b>Repository</b>Kayforkind/{esc(p["repo"])}</div>'
        '</div>'
        '<section class="stories" id="how">'
        '<article class="story"><span class="eyebrow">OVERVIEW</span><h2>What it does</h2>'
        f'<p>{esc(p["description"])}</p></article>'
        '<article class="story"><span class="eyebrow">LIMITS</span><h2>Important caveat</h2>'
        f'<p class="caveat">{esc(p["caveat"])}</p></article>'
        '<article class="story"><span class="eyebrow">NEXT</span><h2>Review before use</h2>'
        '<p>Read the repository documentation, run the project’s verification steps, and review output before using it in a production workflow.</p>'
        '</article>'
        '</section>'
        '</main>'
        '<footer><a href="/">← Product library</a>'
        f'<a class="back" href="{esc(gh)}">Kayforkind/{esc(p["repo"])} ↗</a></footer>'
    )
    return shell(f'{p["name"]} — NavigatorLabs', body)


WORKER_TEMPLATE = """/* navigatorslab-home — NavigatorLabs Product Library worker.
 * Routes:  /                 -> homepage (16 products)
 *          /apps/style.css   -> shared stylesheet
 *          /apps/<slug>/     -> dedicated product page (16 products)
 *          /sw.js            -> service-worker kill-switch
 *          /apps/__diag__    -> routing diagnostics JSON
 */
addEventListener("fetch", function (event) { event.respondWith(handle(event.request)); });

var HEADERS_HTML = {
  "content-type": "text/html; charset=utf-8",
  "x-served-by": "navigatorslab-home",
  "content-security-policy": "default-src 'none'; style-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "no-referrer",
  "cross-origin-opener-policy": "same-origin",
  "cross-origin-resource-policy": "same-origin",
  "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  "cache-control": "no-store"
};
var HEADERS_CSS = {
  "content-type": "text/css; charset=utf-8",
  "x-served-by": "navigatorslab-home",
  "x-content-type-options": "nosniff",
  "cache-control": "no-store"
};
var HEADERS_SW = {
  "content-type": "text/javascript; charset=utf-8",
  "x-served-by": "navigatorslab-home",
  "cache-control": "no-store"
};
var SW_KILL = "self.addEventListener('install',function(e){self.skipWaiting()});"
  + "self.addEventListener('activate',function(e){e.waitUntil((async function(){"
  + "try{var k=await caches.keys();await Promise.all(k.map(function(x){return caches.delete(x)}))}catch(e){}"
  + "try{await self.registration.unregister()}catch(e){}"
  + "try{var cs=await self.clients.matchAll({includeUncontrolled:true});"
  + "for(var i=0;i<cs.length;i++){try{cs[i].navigate(cs[i].url)}catch(e){}}}catch(e){}"
  + "})())});";

var PAGES = __PAGES__;
var CSS = __CSS__;

function handle(req) {
  var url = new URL(req.url);
  var p = url.pathname;
  if (p === "/apps/__diag__") {
    var hd = {};
    req.headers.forEach(function (v, k) { hd[k] = v; });
    return new Response(JSON.stringify({
      worker: "navigatorslab-home",
      products: Object.keys(PAGES).length - 1,
      url: url.toString(),
      host: url.host,
      ray: hd["cf-ray"] || null
    }), {
      status: 200,
      headers: { "content-type": "application/json", "x-served-by": "navigatorslab-home", "cache-control": "no-store" }
    });
  }
  if (p === "/") return new Response(PAGES.home, { status: 200, headers: HEADERS_HTML });
  if (p === "/apps/style.css") return new Response(CSS, { status: 200, headers: HEADERS_CSS });
  if (p === "/sw.js") return new Response(SW_KILL, { status: 200, headers: HEADERS_SW });
  var m = p.match(/^\\/apps\\/([a-z0-9-]+)\\/?$/);
  if (m && PAGES[m[1]]) return new Response(PAGES[m[1]], { status: 200, headers: HEADERS_HTML });
  if (p === "/apps" || p === "/apps/") return Response.redirect(url.origin + "/", 302);
  return new Response("not found", { status: 404, headers: HEADERS_HTML });
}
"""


def main() -> None:
    DIST.mkdir(exist_ok=True)
    (DIST / "apps").mkdir(exist_ok=True)
    pages = {"home": render_home()}
    (DIST / "home.html").write_text(pages["home"], encoding="utf-8")
    for p in PRODUCTS:
        html = render_detail(p)
        pages[p["slug"]] = html
        (DIST / "apps" / f'{p["slug"]}.html').write_text(html, encoding="utf-8")
    (DIST / "style.css").write_text(CSS, encoding="utf-8")
    worker = WORKER_TEMPLATE.replace("__PAGES__", json.dumps(pages)).replace("__CSS__", json.dumps(CSS))
    (DIST / "worker.js").write_text(worker, encoding="utf-8")
    total = sum(len(v) for v in pages.values()) + len(CSS)
    print(f"built {len(pages)} pages ({len(PRODUCTS)} products) + css: {total/1024:.1f} KB total, worker.js {len(worker)/1024:.1f} KB")


if __name__ == "__main__":
    main()
