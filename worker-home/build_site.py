#!/usr/bin/env python3
"""Build the Netflix-style NavigatorLabs site.

Generates dist/home.html, dist/style.css, dist/apps/<slug>.html from the
APPS data below. Every fact is verified (see README); no invented products,
no repeated copy. deploy.py embeds dist/ into the navigatorslab-home worker.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"

# ---------------------------------------------------------------- data ---
# glyph: single display character for card art. c1/c2: unique gradient stops.
# open: (label, url) primary CTA. Every example/feature below is real.
APPS = [
 dict(
  slug="reimagine-it", name="reimagine-it", glyph="R",
  c1="#7c3aed", c2="#db2777", angle="135deg",
  badge="FLAGSHIP", matchline="The lab's flagship",
  logline=("The design engine that refuses to invent facts. Point it at any HTML "
           "page and it rebuilds the design from the page's own nouns, dates, numbers "
           "and colors — seventeen directions, zero dependencies, fully offline."),
  meta=[("v2.15.0", "ver"), ("MIT", "lic"), ("CLI + Web", "plat")],
  open=("Open playground", "https://navigatorslab.com/reimagine/"),
  github="https://github.com/Kayforkind/reimagine-it",
  examples=[
   ("Six government pages, seventeen directions",
    "NPS, NASA, NOAA, Census, Federal Register and Smithsonian pages were each "
    "regenerated in 17 design directions — byte-identically reproducible in CI."),
   ("The 19-rule deterministic audit",
    "Every output is scored against 19 design rules with no model in the loop. "
    "This very site scored 19/19 CLEAN."),
   ("Live playground, no install",
    "Paste any HTML into the playground, pick a direction, and take home a "
    "standalone redesigned page."),
   ("An agent skill, not just a CLI",
    "Ships with a Claude Code / Cursor skill and an MCP server, so coding agents "
    "can drive redesigns themselves."),
  ],
  features=["17 content-derived design directions", "19-rule deterministic audit (no LLM)",
            "MCP server + agent skill for Claude Code and Cursor",
            "Byte-identical regeneration across 168-file corpus in CI",
            "Zero runtime dependencies, offline, MIT-licensed"],
  likes=["integration-rot", "design-health-action", "liecatchers"],
 ),
 dict(
  slug="integration-rot", name="integration-rot", glyph="I",
  c1="#f59e0b", c2="#ef4444", angle="115deg",
  badge="NEW", matchline="The newest build",
  logline=("Dependencies rot silently. This autopilot watches yours: it finds every "
           "use of a dying API, drafts the migration, and proves the fix with "
           "generated contract tests before anything is kept."),
  meta=[("v0.4.4", "ver"), ("131 tests", "star"), ("MIT", "lic"), ("CLI + REST + MCP", "plat")],
  open=("Read the docs", "https://navigatorslab.com/Integrationrot"),
  github="https://github.com/Kayforkind/integration-rot",
  waitlist="https://navigatorslab.com/Integrationrot#waitlist",
  examples=[
   ("Stripe Charges becomes PaymentIntents",
    "The scanner finds client.charges.create calls, the fixer drafts the "
    "PaymentIntents rewrite, and contract tests prove it before the fix is kept."),
   ("SendGrid v2 mail.send, retired",
    "The v2 JSON endpoint pattern is detected and rewritten for the v3 API — "
    "including the endpoint URL itself."),
   ("Proof, not promises",
    "Each fix is applied to a temp copy and exercised by generated contract "
    "tests. Green keeps it; red reverts it, automatically."),
   ("The hosted waitlist",
    "A managed version is coming — monitoring, PRs and all. Join the waitlist "
    "from the docs page."),
  ],
  features=["Deprecation DB covering 76 SDK packages", "Deterministic planner: scan, draft, test, keep-or-revert",
            "Contract tests generated per fix, run hermetically",
            "CLI, REST API and MCP server interfaces", "Zero runtime dependencies"],
  likes=["liecatchers", "design-health-action", "reimagine-it"],
 ),
 dict(
  slug="pdf-studio", name="PDF Studio", glyph="P",
  c1="#dc2626", c2="#7c2d12", angle="150deg",
  badge="ORIGINAL", matchline="A lab original",
  logline=("A complete PDF editor that never uploads your file. Edit the text inside "
           "your PDF, fill forms, OCR scans, sign, redact and diff revisions — "
           "entirely in your browser."),
  meta=[("Web app", "plat"), ("100% client-side", "star"), ("MIT", "lic"), ("No account", "ver")],
  open=("Open the editor", "https://navigatorslab.com/pdf-studio/"),
  github="https://github.com/Kayforkind/NavigatorsLab-PDF-Studio",
  examples=[
   ("Redact a contract",
    "Burn social security and bank numbers out of a PDF so they can never be recovered."),
   ("Fill and sign a W-9",
    "Complete form fields and add your signature without printing a page."),
   ("OCR a phone scan",
    "Turn a crooked photo of a document into searchable, selectable text."),
   ("Diff two revisions",
    "Compare proposal v2 against v3 and see exactly what changed."),
  ],
  features=["Edit PDF text in place", "Form filling + e-signature",
            "On-device OCR for scans", "True redaction (burned, not covered)",
            "Revision diffing, on-device LLM helpers"],
  likes=["tools", "reimagine-it", "data-insights"],
 ),
 dict(
  slug="tools", name="23 Tools", glyph="T",
  c1="#0d9488", c2="#0ea5e9", angle="125deg",
  badge="ORIGINAL", matchline="Twenty-three deep",
  logline=("Twenty-three tools, games and projects for everyday files. "
           "Strip photo GPS, shrink images, OCR receipts to CSV, diff contracts word "
           "by word — nothing leaves your device."),
  meta=[("23 tools, games & projects", "ver"), ("100% client-side", "star"), ("MIT", "lic"), ("MCP endpoint", "plat")],
  open=("Browse the tools", "https://navigatorslab.com/tools/"),
  github="https://github.com/Kayforkind/NavigatorsLab-Tools",
  examples=[
   ("Strip GPS before sharing",
    "Remove location data from vacation photos before they go anywhere."),
   ("Receipt photo becomes a spreadsheet",
    "Snap a receipt; get clean CSV rows for expenses."),
   ("Contract diff, word by word",
    "Redline two drafts and catch the one changed clause that matters."),
   ("Shrink a folder for the web",
    "Batch images down to size with no uploads and no quality surprises."),
  ],
  features=["Documents, text, data, images, media and files — plus games",
            "Deep links with parameters drive any tool from a URL",
            "MCP endpoint so AI agents can operate every tool",
            "QR code for every tool — phone handoff in one scan",
            "Fully offline once loaded; zero telemetry"],
  likes=["pdf-studio", "book-guide-mcp", "reimagine-it"],
 ),
 dict(
  slug="book-guide-mcp", name="book-guide-mcp", glyph="B",
  c1="#059669", c2="#a3e635", angle="140deg",
  badge="ORIGINAL", matchline="Agents, meet your library",
  logline=("Turn the books you trust into skills your coding agent can call. "
           "Playbooks, frameworks and Socratic tutors — every claim cited with a "
           "locator, everything running locally."),
  meta=[("v0.2.0", "ver"), ("MCP server", "plat"), ("MIT", "lic"), ("No API keys", "star")],
  open=("View on GitHub", "https://github.com/Kayforkind/book-guide-mcp"),
  github="https://github.com/Kayforkind/book-guide-mcp",
  examples=[
   ("skill_match routes the question",
    "Ask how to price a launch; the server routes it to the pricing book's skill, not generic advice."),
   ("skill_cite with locators",
    "Every claim the agent makes carries a book locator you can verify."),
   ("The Socratic tutor",
    "Learns by questioning — the agent teaches you instead of telling you."),
   ("The Avicenna tutor",
    "Teaches from first principles, step by step, from texts you own."),
  ],
  features=["L0 Library to L4 Mentor skill packages", "skill_match, skill_search and skill_cite tools",
            "Socratic and Avicenna mentor modes", "MCP hosts include Cursor, Claude Code, VS Code and Zed",
            "Local-first; no API keys for the core loop"],
  likes=["liecatchers", "tools", "design-health-action"],
 ),
 dict(
  slug="design-health-action", name="design-health-action", glyph="D",
  c1="#0284c7", c2="#6366f1", angle="120deg",
  badge="ORIGINAL", matchline="The CI gate",
  logline=("Eighteen deterministic design-quality checks as a GitHub Action. It fails "
           "your build when the palette drifts, motion support is missing, or content "
           "is fabricated — no LLM, no API key, seconds per run."),
  meta=[("v1.0.1", "ver"), ("18 checks", "star"), ("MIT", "lic"), ("GitHub Action", "plat")],
  open=("View on GitHub", "https://github.com/Kayforkind/design-health-action"),
  github="https://github.com/Kayforkind/design-health-action",
  examples=[
   ("Off-palette accent fails the build",
    "More than five non-neutral colors, or an accent outside the palette — blocked."),
   ("Motion support is mandatory",
    "Missing prefers-reduced-motion or focus-visible styles get flagged before merge."),
   ("Fabricated content caught",
    "Placeholder labels and invented copy are detected as content failures."),
   ("verdict: CLEAN",
    "Each run posts a summary table — verdict, failures, warnings — to the workflow."),
  ],
  features=["18 checks across Typography, Palette, Motion, Content, Structure, Performance",
            "Deterministic: no model, no network, no API key",
            "verdict / failures / warnings / summary outputs",
            "fail-on-warnings and strict modes for tight gates",
            "The CI-quality-gate half of reimagine-it"],
  likes=["reimagine-it", "liecatchers", "integration-rot"],
 ),
 dict(
  slug="liecatchers", name="liecatchers", glyph="L",
  c1="#3f3f46", c2="#b91c1c", angle="155deg",
  badge="ORIGINAL", matchline="Trust, verified",
  logline=("Your agent said \u201cdone.\u201d Prove it. Ten sensors interrogate the "
           "workspace after every agent run — and hand you a signed RECEIPT.json you "
           "can paste straight into the next turn."),
  meta=[("CLI", "plat"), ("10 sensors", "star"), ("MIT", "lic"), ("Windows-first", "ver")],
  open=("View on GitHub", "https://github.com/Kayforkind/liecatchers"),
  github="https://github.com/Kayforkind/liecatchers",
  examples=[
   ("The tests never ran",
    "The agent printed \u201cDone\u201d; the sensor shows no test process ever executed. Exit code 1."),
   ("Invented paths in the PR",
    "The PR references files that are not in the git diff — caught and listed."),
   ("Green npm, missing binaries",
    "Install looks fine but native modules are absent. The sensor knows."),
   ("RECEIPT.json",
    "One signed machine-readable receipt: paste it into the next agent turn and continue honestly."),
  ],
  features=["10 sensors: commands, git diff, lockfiles, native modules, handoffs",
            "Signed RECEIPT.json — the one source of truth",
            "30-second fail-demo proves the detection works",
            "Cursor stop-hook runs it automatically",
            "Zero API keys, Windows-first"],
  likes=["integration-rot", "book-guide-mcp", "design-health-action"],
 ),
 dict(
  slug="data-insights", name="Data Insights", glyph="Δ",
  c1="#4f46e5", c2="#0ea5e9", angle="130deg",
  badge="ORIGINAL", matchline="The morning brief",
  logline=("A founder intelligence platform that reads the public web for you. Daily "
           "5W1H briefs and weekly synthesis from technology, startup, research and "
           "security signals — with agent APIs on top."),
  meta=[("Web + CLI", "plat"), ("Daily briefs", "star"), ("JSON APIs", "ver")],
  open=("View on GitHub", "https://github.com/Kayforkind/data-insights"),
  github="https://github.com/Kayforkind/data-insights",
  examples=[
   ("The daily 5W1H",
    "Every morning: who, what, when, where, why and how across the signals that matter."),
   ("The weekly synthesis",
    "Themes, momentum, opportunities, risks and experiments — plus a print-ready edition."),
   ("Search any topic",
    "npm run cli -- search robotics — follow a topic into its live signals and source history."),
   ("The agent CLI",
    "npm run cli -- search robotics — the same intelligence, scriptable."),
  ],
  features=["/report: daily 5W1H brief", "/weekly: synthesis with themes, risks, experiments",
            "Topic search across live signals and source history", "/portal: headline river without licensed full text",
            "JSON APIs + CLI for agents"],
  likes=["tools", "pdf-studio", "book-guide-mcp"],
 ),
]

BY_SLUG = {a["slug"]: a for a in APPS}

CSS = r"""
:root{
  --bg:#0b0b0f; --bg2:#121218; --panel:#17171f; --line:#26262f;
  --txt:#f5f5f7; --mut:#a7a7b3; --dim:#6d6d7a;
  --brand:#2dd4bf; --brand-d:#0d9488;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --cond:"Arial Narrow","Helvetica Neue Condensed",Impact,sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font-family:var(--sans);
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
::selection{background:var(--brand);color:#04211d}

/* ---------- nav ---------- */
.nav{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;gap:34px;
  padding:0 4vw;height:68px;background:linear-gradient(180deg,rgba(5,5,8,.92),rgba(5,5,8,.55) 70%,transparent);
  transition:background .3s}
.nav.scrolled{background:rgba(8,8,11,.96)}
.brand{font-family:var(--cond);font-weight:800;font-size:21px;letter-spacing:5px;color:var(--brand);
  text-transform:uppercase;white-space:nowrap}
.brand small{display:block;font-size:8px;letter-spacing:6px;color:var(--dim);font-weight:400}
.nav-links{display:flex;gap:26px;font-size:14px;color:#d7d7de}
.nav-links a{opacity:.75;transition:opacity .2s}
.nav-links a:hover,.nav-links a.on{opacity:1;color:#fff}
.nav-right{margin-left:auto;display:flex;align-items:center;gap:18px;font-size:13px;color:var(--mut)}
.pill{border:1px solid var(--line);border-radius:20px;padding:6px 14px;font-size:12px;color:var(--txt)}
.pill b{color:var(--brand)}

/* ---------- billboard ---------- */
.billboard{position:relative;height:92vh;min-height:620px;overflow:hidden}
.slide{position:absolute;inset:0;opacity:0;animation:hero 24s infinite}
.slide:nth-child(2){animation-delay:8s}
.slide:nth-child(3){animation-delay:16s}
@keyframes hero{0%{opacity:0}2.5%{opacity:1}31%{opacity:1}35.5%{opacity:0}100%{opacity:0}}
.slide-art{position:absolute;inset:0}
.slide-shade{position:absolute;inset:0;
  background:linear-gradient(77deg,rgba(6,6,10,.94) 20%,rgba(6,6,10,.55) 45%,rgba(6,6,10,.05) 75%),
             linear-gradient(0deg,var(--bg) 2%,transparent 30%),
             linear-gradient(180deg,rgba(6,6,10,.6),transparent 26%)}
.slide-body{position:absolute;left:4vw;bottom:16vh;max-width:640px;z-index:2}
.kicker{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.kicker .n{font-family:var(--cond);font-weight:800;color:var(--brand);font-size:15px;letter-spacing:3px}
.kicker .tag{font-size:11px;letter-spacing:2.5px;color:var(--mut);text-transform:uppercase}
.bill-title{font-family:var(--serif);font-weight:700;font-size:clamp(46px,6.5vw,88px);
  line-height:1.02;letter-spacing:-.5px;margin-bottom:16px;text-wrap:balance}
.bill-meta{display:flex;align-items:center;gap:12px;margin-bottom:14px;font-size:14px}
.maturity{border:1px solid var(--dim);color:var(--mut);font-size:11px;padding:3px 9px;border-radius:3px;letter-spacing:1px}
.bill-desc{color:#d9d9e0;font-size:clamp(15px,1.6vw,18px);line-height:1.55;max-width:56ch;margin-bottom:26px}
.bill-btns{display:flex;gap:12px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:10px;font-weight:700;font-size:16px;
  border-radius:6px;padding:12px 28px;transition:transform .15s,background .2s;cursor:pointer;border:0}
.btn:active{transform:scale(.97)}
.btn-play{background:#fff;color:#0b0b0f}
.btn-play:hover{background:rgba(255,255,255,.82)}
.btn-more{background:rgba(109,109,122,.55);color:#fff}
.btn-more:hover{background:rgba(109,109,122,.38)}
.btn .tri{font-size:13px}

.card{position:relative;scroll-snap-align:start;border-radius:8px;overflow:hidden;
  background:var(--panel);transition:transform .25s ease,box-shadow .25s;cursor:pointer}
.card:hover{transform:translateY(-6px);z-index:10;box-shadow:0 18px 50px rgba(0,0,0,.65)}
.card-art{position:relative;aspect-ratio:16/9;overflow:hidden}
.card-art .glyph{position:absolute;right:6px;bottom:-24px;font-family:var(--serif);font-weight:700;
  font-size:150px;line-height:1;color:rgba(255,255,255,.16)}
.card-art .gname{position:absolute;left:14px;bottom:10px;font-family:var(--cond);font-weight:800;
  font-size:15px;letter-spacing:2.5px;color:rgba(255,255,255,.92);text-transform:uppercase;text-shadow:0 2px 8px rgba(0,0,0,.5)}
.card-badge{position:absolute;top:10px;left:10px;font-size:10px;font-weight:800;letter-spacing:1.8px;
  background:rgba(0,0,0,.55);border:1px solid rgba(255,255,255,.25);padding:4px 10px;border-radius:4px;color:#fff}
.card-info{padding:12px 14px 14px}
.card-info h3{font-size:15px;margin-bottom:6px}
.card-info p{font-size:12.5px;color:var(--mut);line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;
  -webkit-box-orient:vertical;overflow:hidden}
.card-hover{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:center;gap:10px;
  padding-bottom:14px;background:linear-gradient(0deg,rgba(0,0,0,.72),transparent 55%);
  opacity:0;transition:opacity .2s}
.card:hover .card-hover{opacity:1}
.mini-btn{font-size:12px;font-weight:700;border-radius:20px;padding:8px 16px;border:1px solid rgba(255,255,255,.4);
  background:rgba(10,10,14,.7);color:#fff}
.mini-btn.solid{background:#fff;color:#0b0b0f;border-color:#fff}
/* ---------- collection shelf ---------- */
.shelf{padding:36px 4vw 12px;max-width:1280px;margin:0 auto}
.shelf h2{font-size:22px;margin-bottom:6px}
.shelf h2 .nlab{color:var(--brand)}
.shelf .sub{color:var(--mut);font-size:14px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(272px,1fr));gap:14px}

/* ---------- detail page ---------- */
.backbar{position:absolute;top:0;left:0;right:0;z-index:50;padding:18px 4vw;
  background:linear-gradient(180deg,rgba(5,5,8,.9),transparent)}
.back{display:inline-flex;align-items:center;gap:8px;font-size:15px;font-weight:600;color:#fff;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:8px 18px}
.back:hover{background:rgba(255,255,255,.16)}
.d-hero{position:relative;min-height:78vh;display:flex;align-items:flex-end;overflow:hidden}
.d-shade{position:absolute;inset:0;background:linear-gradient(77deg,rgba(6,6,10,.95) 25%,rgba(6,6,10,.45) 55%,transparent 80%),
  linear-gradient(0deg,var(--bg) 4%,transparent 34%),linear-gradient(180deg,rgba(6,6,10,.55),transparent 30%)}
.d-body{position:relative;z-index:2;padding:0 4vw 8vh;max-width:900px}
.d-title{font-family:var(--serif);font-size:clamp(44px,6vw,84px);font-weight:700;letter-spacing:-.5px;
  line-height:1.02;margin:12px 0 18px}
.d-meta{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-bottom:16px;font-size:14px;color:#d7d7de}
.d-meta .m{border:1px solid var(--line);background:rgba(255,255,255,.05);padding:5px 12px;border-radius:5px;font-size:12.5px}
.d-meta .m b{color:var(--brand);font-weight:700}
.d-log{font-size:clamp(16px,1.8vw,19px);line-height:1.6;color:#e2e2e9;max-width:62ch;margin-bottom:28px}
.d-btns{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.d-sec{padding:34px 4vw;max-width:1200px}
.d-sec h2{font-size:22px;margin-bottom:6px}
.d-sec .sub{color:var(--mut);font-size:14px;margin-bottom:20px}
.ex-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.ex{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:20px;transition:border-color .2s,transform .2s}
.ex:hover{border-color:#3a3a48;transform:translateY(-3px)}
.ex .k{font-size:11px;font-weight:800;letter-spacing:2px;color:var(--brand);margin-bottom:10px}
.ex h3{font-size:16px;margin-bottom:8px;line-height:1.35}
.ex p{font-size:13.5px;color:var(--mut);line-height:1.55}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;list-style:none}
.feat li{background:var(--bg2);border:1px solid var(--line);border-radius:8px;padding:14px 16px;font-size:13.5px;color:#d7d7de}
.feat li::before{content:"✓ ";color:var(--brand);font-weight:800}
.like-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}

/* ---------- footer ---------- */
footer{margin-top:60px;padding:40px 4vw 60px;color:var(--dim);font-size:13px;border-top:1px solid #17171e}
footer .fbrand{font-family:var(--cond);letter-spacing:4px;color:var(--brand);font-weight:800;margin-bottom:14px}
footer p{max-width:70ch;line-height:1.7;margin-bottom:8px}
footer nav{display:flex;gap:22px;flex-wrap:wrap;margin-top:16px}
footer nav a{color:var(--mut)}
footer nav a:hover{color:#fff}

/* ---------- responsive / motion ---------- */
@media (max-width:760px){
  .nav-links{display:none}
  .billboard{height:88vh;min-height:560px}
  .grid{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}
  .card:hover{transform:translateY(-4px)}
}
@media (prefers-reduced-motion:reduce){
  .slide{animation:none;opacity:0}
  .slide:first-child{opacity:1}
  *{transition:none!important}
}
"""

# ------------------------------------------------------------- templates ---

def art_style(a, big=False):
    return (f"background:linear-gradient({a['angle']},{a['c1']},{a['c2']});")

NAV = """
<header class="nav" id="nav">
  <a class="brand" href="/">NavigatorLabs<small>local-first software</small></a>
  <nav class="nav-links">
    <a href="/" class="on">Home</a>
    <a href="/apps/reimagine-it/">Apps</a>
    <a href="/apps/integration-rot/">Developers</a>
    <a href="https://github.com/Kayforkind">GitHub</a>
  </nav>
  <div class="nav-right"><span class="pill"><b>8</b> apps · free · local-first</span></div>
</header>
<script>/* nav shade on scroll needs JS; static gradient is fine without it */</script>
"""

# NOTE: no-JS build — the script tag above is a comment-only placeholder; drop it.
NAV = NAV.replace('<script>/* nav shade on scroll needs JS; static gradient is fine without it */</script>\n', '')

FOOT = """
<footer>
  <div class="fbrand">NAVIGATORLABS</div>
  <p>A one-person software lab. Every app is free and local-first:
  it runs on your machine or in your browser — your files are never uploaded,
  because there is no server to trust. Most apps are MIT-licensed; each
  repository carries its own license.</p>
  <nav>
    <a href="/apps/reimagine-it/">reimagine-it</a>
    <a href="/apps/integration-rot/">integration-rot</a>
    <a href="/apps/pdf-studio/">PDF Studio</a>
    <a href="/apps/tools/">23 Tools</a>
    <a href="https://github.com/Kayforkind">GitHub</a>
  </nav>
</footer>
"""

def card(a):
    return f"""
<article class="card">
  <a class="card-main" href="/apps/{a['slug']}/" aria-label="{a['name']} details">
    <div class="card-art" style="{art_style(a)}">
      <span class="card-badge">{a['badge']}</span>
      <span class="glyph">{a['glyph']}</span>
      <span class="gname">{a['name']}</span>
    </div>
    <div class="card-info"><h3>{a['name']}</h3><p>{a['logline']}</p></div>
  </a>
  <div class="card-hover">
    <a class="mini-btn solid" href="{a['open'][1]}">▶ Open</a>
    <a class="mini-btn" href="/apps/{a['slug']}/">ⓘ Details</a>
  </div>
</article>"""

def slide(a):
    metas = " · ".join(m[0] for m in a["meta"][:3])
    return f"""
<div class="slide">
  <div class="slide-art" style="{art_style(a)}"></div>
  <div class="slide-shade"></div>
  <div class="slide-body">
    <div class="kicker"><span class="n">N</span><span class="tag">Labs original · {a['matchline']}</span></div>
    <h1 class="bill-title">{a['name']}</h1>
    <div class="bill-meta">
      <span class="maturity">{a['badge']}</span><span style="color:#a7a7b3;font-size:13px">{metas}</span>
    </div>
    <p class="bill-desc">{a['logline']}</p>
    <div class="bill-btns">
      <a class="btn btn-play" href="{a['open'][1]}"><span class="tri">▶</span> {a['open'][0]}</a>
      <a class="btn btn-more" href="/apps/{a['slug']}/">ⓘ Details &amp; examples</a>
    </div>
  </div>
</div>"""

def home():
    bill = [BY_SLUG[s] for s in ("reimagine-it", "integration-rot", "pdf-studio")]
    # Every app appears exactly once on the homepage — no repeats, no rankings.
    collection = ["reimagine-it", "integration-rot", "pdf-studio", "tools",
                  "book-guide-mcp", "design-health-action", "liecatchers", "data-insights"]
    grid = "\n".join(card(BY_SLUG[s]) for s in collection)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NavigatorLabs — local-first, private-by-default software</title>
<meta name="description" content="Eight free, local-first apps: reimagine-it, integration-rot, PDF Studio, 23 private tools and more. No uploads, no accounts, no telemetry.">
<link rel="stylesheet" href="/apps/style.css">
</head>
<body>
{NAV}
<section class="billboard">
{slide(bill[0])}
{slide(bill[1])}
{slide(bill[2])}
</section>
<section class="shelf">
  <h2><span class="nlab">NavigatorLabs</span> Originals</h2>
  <p class="sub">Eight apps. One standard: free, local-first, no telemetry. Each appears once — pick yours.</p>
  <div class="grid">{grid}</div>
</section>
{FOOT}
</body>
</html>"""

def detail(a):
    ex = "\n".join(
        f'<div class="ex"><div class="k">EXAMPLE {i+1}</div><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(a["examples"]))
    feats = "\n".join(f"<li>{f}</li>" for f in a["features"])
    likes = "\n".join(card(BY_SLUG[s]) for s in a["likes"])
    metas = "\n".join(f'<span class="m"><b>{k}</b> · {v}</span>' for v, k in a["meta"])
    waitlist = (f'<a class="btn btn-play" href="{a["waitlist"]}"><span class="tri">✦</span> Join the waitlist</a>'
                if "waitlist" in a else "")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{a['name']} — NavigatorLabs</title>
<meta name="description" content="{a['logline']}">
<link rel="stylesheet" href="/apps/style.css">
</head>
<body>
<div class="backbar"><a class="back" href="/">‹ All apps</a></div>
<section class="d-hero">
  <div class="slide-art" style="{art_style(a)}"></div>
  <div class="d-shade"></div>
  <div class="d-body">
    <div class="kicker"><span class="n">N</span><span class="tag">Labs original · {a['matchline']}</span></div>
    <h1 class="d-title">{a['name']}</h1>
    <div class="d-meta">{metas}</div>
    <p class="d-log">{a['logline']}</p>
    <div class="d-btns">
      <a class="btn btn-play" href="{a['open'][1]}"><span class="tri">▶</span> {a['open'][0]}</a>
      <a class="btn btn-more" href="{a['github']}">GitHub ↗</a>
      {waitlist}
    </div>
  </div>
</section>
<section class="d-sec">
  <h2>Examples</h2><p class="sub">Real things {a['name']} does — drawn from the docs, the demos and the repos.</p>
  <div class="ex-grid">{ex}</div>
</section>
<section class="d-sec">
  <h2>Details</h2><p class="sub">What ships with it.</p>
  <ul class="feat">{feats}</ul>
</section>
<section class="d-sec">
  <h2>More Like This</h2><p class="sub">From the same lab, same guarantees.</p>
  <div class="like-row">{likes}</div>
</section>
{FOOT}
</body>
</html>"""

WORKER = """/* navigatorslab-home — Netflix-style NavigatorLabs site.
 * Routes:  /                 -> homepage
 *          /apps/style.css   -> shared stylesheet
 *          /apps/<slug>/     -> dedicated app page (8 apps)
 * Zone routes `navigatorslab.com/` and `navigatorslab.com/apps*` both point
 * here; every other path keeps serving via navigatorslab-tools.
 * Zero JavaScript, zero external fetches — all motion is CSS.
 */
addEventListener("fetch", function (event) { event.respondWith(handle(event.request)); });

var HEADERS_HTML = {
  "content-type": "text/html; charset=utf-8",
  "content-security-policy": "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; worker-src 'self' blob:; child-src 'self' blob:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "no-referrer",
  "cross-origin-opener-policy": "same-origin",
  "cross-origin-resource-policy": "same-origin",
  "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  "cache-control": "public, max-age=600"
};
var HEADERS_CSS = {
  "content-type": "text/css; charset=utf-8",
  "cache-control": "public, max-age=3600"
};

var PAGES = __PAGES__;
var CSS = __CSS__;

function handle(req) {
  var url = new URL(req.url);
  var p = url.pathname;
  if (p === "/") return new Response(PAGES.home, { status: 200, headers: HEADERS_HTML });
  if (p === "/apps/style.css") return new Response(CSS, { status: 200, headers: HEADERS_CSS });
  var m = p.match(/^\\/apps\\/([a-z0-9-]+)\\/?$/);
  if (m && PAGES[m[1]]) return new Response(PAGES[m[1]], { status: 200, headers: HEADERS_HTML });
  if (p === "/apps" || p === "/apps/") return Response.redirect(url.origin + "/", 302);
  return new Response("not found", { status: 404, headers: HEADERS_HTML });
}
"""

def main():
    DIST.mkdir(exist_ok=True)
    (DIST / "apps").mkdir(exist_ok=True)
    pages = {"home": home()}
    (DIST / "home.html").write_text(pages["home"], encoding="utf-8")
    for a in APPS:
        html = detail(a)
        pages[a["slug"]] = html
        (DIST / "apps" / (a["slug"] + ".html")).write_text(html, encoding="utf-8")
    (DIST / "style.css").write_text(CSS, encoding="utf-8")
    # safety: worker embeds pages in a JS template literal
    for name, html in list(pages.items()) + [("css", CSS)]:
        assert "`" not in html, f"backtick in {name}"
        assert "${" not in html, f"${{ in {name}"
    import json
    worker = WORKER.replace("__PAGES__", json.dumps(pages)).replace("__CSS__", json.dumps(CSS))
    (DIST / "worker.js").write_text(worker, encoding="utf-8")
    total = sum(len(v) for v in pages.values()) + len(CSS)
    print(f"built {len(pages)} pages + css: {total/1024:.0f} KB total, worker.js {len(worker)/1024:.0f} KB")

if __name__ == "__main__":
    main()
