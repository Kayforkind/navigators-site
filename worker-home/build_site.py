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

# Cloudflare Web Analytics beacon (cookieless, privacy-friendly aggregate stats).
# Scoped ONLY to pages served by the navigatorslab-home worker (/ and /apps/*).
# NEVER add analytics to pdf-studio or any worker outside this file's scope.
# The token below is a public site token (visible in page source by design).
CF_BEACON_TOKEN = "88ed5dc71a4d4f1ebd8470181e554cd9"
CF_BEACON = (
    "<!-- Cloudflare Web Analytics -->"
    "<script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
    "data-cf-beacon='{\"token\": \"" + CF_BEACON_TOKEN + "\"}'></script>"
    "<!-- End Cloudflare Web Analytics -->"
)


def with_beacon(html: str) -> str:
    """Insert the analytics beacon just before </body> (staging + production)."""
    assert "</body>" in html, "no </body> to attach beacon to"
    return html.replace("</body>", CF_BEACON + "</body>", 1)

# ---------------------------------------------------------------- data ---
# glyph: single display character for card art. c1/c2: unique gradient stops.
# open: (label, url) primary CTA. Every example/feature below is real.
APPS = [
 dict(
  slug="reimagine-it", name="reimagine-it", glyph="R",
  c1="#7c3aed", c2="#db2777", angle="135deg",
  badge="FLAGSHIP", matchline="The lab's flagship",
  blurb="Rebuilds any web page's design from its own content",
  logline=("The design engine that refuses to invent facts. Point it at any HTML "
           "page and it rebuilds the design from the page's own nouns, dates, numbers "
           "and colors — seventeen directions, zero dependencies, fully offline."),
  meta=[("v2.15.0", "ver"), ("MIT", "lic"), ("CLI + Web", "plat")],
  open=("Open playground", "https://navigatorslab.com/reimagine/"),
  github="https://github.com/Kayforkind/reimagine-it",
  stories=[
   ("Generates", "Six government pages, seventeen directions",
    "NPS, NASA, NOAA, Census, Federal Register and Smithsonian pages were each regenerated in 17 design directions — byte-identically reproducible in CI.",
    ["17 content-derived design directions", "Rebuilds from the page’s own nouns, dates, numbers and colors"]),
   ("Verifies", "The 19-rule deterministic audit",
    "Every output is scored against 19 design rules with no model in the loop. This very site scored 19/19 CLEAN.",
    ["No LLM in the loop", "Byte-identical regeneration across a 168-file corpus in CI"]),
   ("Generates", "Live playground, no install",
    "Paste any HTML into the playground, pick a direction, and take home a standalone redesigned page.",
    ["Zero runtime dependencies", "Works fully offline"]),
   ("Plays well with agents", "An agent skill, not just a CLI",
    "Ships with a Claude Code / Cursor skill and an MCP server, so coding agents can drive redesigns themselves.",
    ["MCP server", "Agent skill for Claude Code and Cursor"]),
  ],
  also=[],
  likes=["integration-rot", "design-health-action", "liecatchers"],
 ),
 dict(
  slug="integration-rot", name="integration-rot", glyph="I",
  c1="#f59e0b", c2="#ef4444", angle="115deg",
  badge="NEW", matchline="The newest build",
  blurb="Autopilot that migrates your dying API calls",
  logline=("Dependencies rot silently. This autopilot watches yours: it finds every "
           "use of a dying API, drafts the migration, and proves the fix with "
           "generated contract tests before anything is kept."),
  meta=[("v0.4.4", "ver"), ("131 tests", "star"), ("MIT", "lic"), ("CLI + REST + MCP", "plat")],
  open=("Read the docs", "https://navigatorslab.com/Integrationrot"),
  github="https://github.com/Kayforkind/integration-rot",
  waitlist="https://navigatorslab.com/Integrationrot#waitlist",
  note="A managed cloud version is in the works — monitoring, PRs and all.",
  stories=[
   ("Detects", "Stripe Charges becomes PaymentIntents",
    "The scanner finds client.charges.create calls, the fixer drafts the PaymentIntents rewrite, and contract tests prove it before the fix is kept.",
    ["Deprecation DB: 76 SDK packages", "Finds every use of a dying API"]),
   ("Repairs", "SendGrid v2 mail.send, retired",
    "The v2 JSON endpoint pattern is detected and rewritten for the v3 API — including the endpoint URL itself.",
    ["Deterministic loop: scan, draft, test, keep-or-revert"]),
   ("Repairs", "Proof, not promises",
    "Each fix is applied to a temp copy and exercised by generated contract tests. Green keeps it; red reverts it, automatically.",
    ["Contract tests generated per fix", "Run hermetically"]),
  ],
  also=["CLI, REST API and MCP server interfaces", "Zero runtime dependencies"],
  likes=["liecatchers", "design-health-action", "reimagine-it"],
 ),
 dict(
  slug="pdf-studio", name="PDF Studio", glyph="P",
  c1="#dc2626", c2="#7c2d12", angle="150deg",
  badge="ORIGINAL", matchline="A lab original",
  blurb="Full PDF editor — your file never uploads",
  logline=("A complete PDF editor that never uploads your file. Edit the text inside "
           "your PDF, fill forms, OCR scans, sign, redact and diff revisions — "
           "entirely in your browser."),
  meta=[("Web app", "plat"), ("100% client-side", "star"), ("MIT", "lic"), ("No account", "ver")],
  open=("Open the editor", "https://navigatorslab.com/pdf-studio/"),
  github="https://github.com/Kayforkind/NavigatorsLab-PDF-Studio",
  stories=[
   ("Edit", "Edit the text itself",
    "Change the words already inside the PDF — true content-stream edits, not annotations layered on top.",
    ["Table cells stay independent when you edit"]),
   ("Edit", "Fill and sign a W-9",
    "Complete form fields and add your signature without printing a page.",
    ["Fill real AcroForms, then flatten them", "Sign with the on-page signature pad"]),
   ("Protect", "Redact a contract",
    "Burn social security and bank numbers out of a PDF so they can never be recovered.",
    ["Redaction burns content — not covers it", "Your file never leaves the device"]),
   ("Understand", "OCR a phone scan",
    "Turn a crooked photo of a document into searchable, selectable text.",
    ["On-device OCR", "Ask an on-device LLM about the document"]),
   ("Understand", "Diff two revisions",
    "Compare proposal v2 against v3 and see exactly what changed.",
    ["Line-by-line diff"]),
  ],
  also=["Reorder, rotate, merge and split pages", "Page numbers, watermarks, headers and footers", "Full-text search across the document"],
  likes=["tools", "reimagine-it", "liecatchers"],
  security=(
   "A\u2212",
   ("Independent security audit, 2026-09-28 \u2014 every claim verified against the source code. "
    "Zero network calls carry document bytes, and the Content-Security-Policy makes exfiltration "
    "structurally impossible: even a bug couldn't phone home."),
   ["Exfiltration: A", "XSS: A", "Supply chain: A\u2212",
    "Dependencies: A", "Local data: A\u2212", "Headers: A"],
   [("Read the full assessment",
     "https://github.com/Kayforkind/NavigatorsLab-PDF-Studio/blob/main/docs/SECURITY_ASSESSMENT.md"),
    ("Report a vulnerability",
     "https://github.com/Kayforkind/NavigatorsLab-PDF-Studio/blob/main/SECURITY.md")],
  ),
 ),
 dict(
  slug="tools", name="23 Tools", glyph="T",
  c1="#0d9488", c2="#0ea5e9", angle="125deg",
  badge="ORIGINAL", matchline="Twenty-three deep",
  blurb="23 private tools for everyday files",
  logline=("Twenty-three tools, games and projects for everyday files. "
           "Strip photo GPS, shrink images, OCR receipts to CSV, diff contracts word "
           "by word — nothing leaves your device."),
  meta=[("23 tools, games & projects", "ver"), ("100% client-side", "star"), ("MIT", "lic"), ("MCP endpoint", "plat")],
  open=("Browse the tools", "https://navigatorslab.com/tools/"),
  github="https://github.com/Kayforkind/NavigatorsLab-Tools",
  stories=[
   ("The collection", "Strip GPS before sharing",
    "Remove location data from vacation photos before they go anywhere.",
    ["23 tools, games and projects"]),
   ("The collection", "Receipt photo becomes a spreadsheet",
    "Snap a receipt; get clean CSV rows for expenses.",
    ["Documents, text, data, images, media and files — plus games"]),
   ("The collection", "Contract diff, word by word",
    "Redline two drafts and catch the one changed clause that matters.",
    []),
   ("Made for flow", "Shrink a folder for the web",
    "Batch images down to size with no uploads and no quality surprises.",
    ["Deep links with parameters drive any tool from a URL", "A QR code for every tool — phone handoff in one scan", "Fully offline once loaded; zero telemetry"]),
  ],
  also=["MCP endpoint so AI agents can operate every tool"],
  likes=["pdf-studio", "book-guide-mcp", "reimagine-it"],
 ),
 dict(
  slug="book-guide-mcp", name="book-guide-mcp", glyph="B",
  c1="#059669", c2="#a3e635", angle="140deg",
  badge="ORIGINAL", matchline="Agents, meet your library",
  blurb="Your trusted books, as agent skills",
  logline=("Turn the books you trust into skills your coding agent can call. "
           "Playbooks, frameworks and Socratic tutors — every claim cited with a "
           "locator, everything running locally."),
  meta=[("v0.2.0", "ver"), ("MCP server", "plat"), ("MIT", "lic"), ("No API keys", "star")],
  open=("View on GitHub", "https://github.com/Kayforkind/book-guide-mcp"),
  github="https://github.com/Kayforkind/book-guide-mcp",
  stories=[
   ("The library", "skill_match routes the question",
    "Ask how to price a launch; the server routes it to the pricing book’s skill, not generic advice.",
    ["Turn the books you trust into agent skills", "L0 Library to L4 Mentor skill packages"]),
   ("Cited, not invented", "skill_cite with locators",
    "Every claim the agent makes carries a book locator you can verify.",
    ["skill_match, skill_search and skill_cite tools"]),
   ("The library", "The Socratic tutor",
    "Learns by questioning — the agent teaches you instead of telling you.",
    ["Playbooks, frameworks, Socratic and Avicenna tutors"]),
   ("The library", "The Avicenna tutor",
    "Teaches from first principles, step by step, from texts you own.",
    []),
  ],
  also=["MCP hosts: Cursor, Claude Code, VS Code and Zed", "Local-first; no API keys for the core loop"],
  likes=["liecatchers", "tools", "design-health-action"],
 ),
 dict(
  slug="design-health-action", name="design-health-action", glyph="D",
  c1="#0284c7", c2="#6366f1", angle="120deg",
  badge="ORIGINAL", matchline="The CI gate",
  blurb="A design-quality gate for CI",
  logline=("Eighteen deterministic design-quality checks as a GitHub Action. It fails "
           "your build when the palette drifts, motion support is missing, or content "
           "is fabricated — no LLM, no API key, seconds per run."),
  meta=[("v1.0.1", "ver"), ("18 checks", "star"), ("MIT", "lic"), ("GitHub Action", "plat")],
  open=("View on GitHub", "https://github.com/Kayforkind/design-health-action"),
  github="https://github.com/Kayforkind/design-health-action",
  stories=[
   ("The gate", "Off-palette accent fails the build",
    "More than five non-neutral colors, or an accent outside the palette — blocked.",
    ["18 checks: Typography, Palette, Motion, Content, Structure, Performance"]),
   ("The gate", "Motion support is mandatory",
    "Missing prefers-reduced-motion or focus-visible styles get flagged before merge.",
    []),
   ("The gate", "Fabricated content caught",
    "Placeholder labels and invented copy are detected as content failures.",
    []),
   ("Deterministic", "verdict: CLEAN",
    "Each run posts a summary table — verdict, failures, warnings — to the workflow.",
    ["No model, no network, no API key", "verdict / failures / warnings / summary outputs"]),
  ],
  also=["fail-on-warnings and strict modes for tight gates", "The CI-quality-gate half of reimagine-it"],
  likes=["reimagine-it", "liecatchers", "integration-rot"],
 ),
 dict(
  slug="liecatchers", name="liecatchers", glyph="L",
  c1="#3f3f46", c2="#b91c1c", angle="155deg",
  badge="ORIGINAL", matchline="Trust, verified",
  blurb="Proves your agent actually did the work",
  logline=("Your agent said \u201cdone.\u201d Prove it. Ten sensors interrogate the "
           "workspace after every agent run — and hand you a signed RECEIPT.json you "
           "can paste straight into the next turn."),
  meta=[("CLI", "plat"), ("10 sensors", "star"), ("MIT", "lic"), ("Windows-first", "ver")],
  open=("View on GitHub", "https://github.com/Kayforkind/liecatchers"),
  github="https://github.com/Kayforkind/liecatchers",
  stories=[
   ("The sensors", "The tests never ran",
    "The agent printed “Done”; the sensor shows no test process ever executed. Exit code 1.",
    ["10 sensors: commands, git diff, lockfiles, native modules, handoffs"]),
   ("The sensors", "Invented paths in the PR",
    "The PR references files that are not in the git diff — caught and listed.",
    []),
   ("The sensors", "Green npm, missing binaries",
    "Install looks fine but native modules are absent. The sensor knows.",
    ["Catches unrun tests, invented paths, missing binaries"]),
   ("The receipt", "RECEIPT.json",
    "One signed machine-readable receipt: paste it into the next agent turn and continue honestly.",
    ["Signed RECEIPT.json — the one source of truth"]),
  ],
  also=["30-second fail-demo proves the detection works", "Cursor stop-hook runs it automatically", "Zero API keys, Windows-first"],
  likes=["integration-rot", "book-guide-mcp", "design-health-action"],
 ),
 dict(
  slug="data-insights", name="Data Insights", glyph="Δ",
  c1="#4f46e5", c2="#0ea5e9", angle="130deg",
  badge="ORIGINAL", matchline="The morning brief",
  blurb="Daily founder-intelligence briefs",
  logline=("A founder intelligence platform that reads the public web for you. Daily "
           "5W1H briefs and weekly synthesis from technology, startup, research and "
           "security signals — with agent APIs on top."),
  meta=[("Web + CLI", "plat"), ("Daily briefs", "star"), ("JSON APIs", "ver")],
  open=("View on GitHub", "https://github.com/Kayforkind/data-insights"),
  github="https://github.com/Kayforkind/data-insights",
  stories=[
   ("Briefs", "The daily 5W1H",
    "Every morning: who, what, when, where, why and how across the signals that matter.",
    ["/report: daily 5W1H brief"]),
   ("Briefs", "The weekly synthesis",
    "Themes, momentum, opportunities, risks and experiments — plus a print-ready edition.",
    ["/weekly: synthesis with themes, risks, experiments"]),
   ("Research", "Search any topic",
    "Follow a topic into its live signals and source history.",
    ["Topic search across live signals and source history", "/portal: headline river without licensed full text"]),
   ("For agents", "The agent CLI",
    "The same intelligence, scriptable.",
    ["JSON APIs + CLI for agents"]),
  ],
  also=[],
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
  text-transform:uppercase;white-space:nowrap;display:flex;align-items:center;gap:12px}
.brand-logo{width:40px;height:40px;border-radius:10px;flex:none}
.brand-text{display:block}
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
.d-hero{position:relative;min-height:74vh;display:flex;align-items:flex-end;overflow:hidden}
.d-glyph{position:absolute;top:2%;z-index:1;font-family:var(--serif);font-weight:700;
  font-size:min(34vw,380px);line-height:1;color:rgba(255,255,255,.09);
  pointer-events:none;user-select:none}
.d-glyph.l{left:2vw}.d-glyph.r{right:2vw}
.d-shade{position:absolute;inset:0;background:linear-gradient(77deg,rgba(6,6,10,.95) 25%,rgba(6,6,10,.45) 55%,transparent 80%),
  linear-gradient(0deg,var(--bg) 4%,transparent 34%),linear-gradient(180deg,rgba(6,6,10,.55),transparent 30%)}
.d-body{position:relative;z-index:2;padding:0 4vw 6vh;max-width:900px}
.d-title{font-family:var(--serif);font-size:clamp(44px,6vw,84px);font-weight:700;letter-spacing:-.5px;
  line-height:1.02;margin:12px 0 18px}
.d-log{font-size:clamp(16px,1.8vw,19px);line-height:1.6;color:#e2e2e9;max-width:62ch;margin-bottom:28px}
.d-btns{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:8px}
.d-note{margin:16px 0 0;font-size:14px;color:var(--mut);max-width:60ch}
.d-note .tri{color:var(--brand);font-size:11px;margin-right:6px}
.d-note a{color:var(--brand);font-weight:700}
.d-note a:hover{text-decoration:underline}
.specbar{display:flex;flex-wrap:wrap;gap:10px 30px;margin-top:24px;padding-top:18px;
  border-top:1px solid rgba(255,255,255,.14)}
.specbar .spec{font-size:14.5px;color:#ececf1;font-weight:600}
.specbar .spec b{display:block;font-size:10px;letter-spacing:2px;text-transform:uppercase;
  color:var(--dim);font-weight:800;margin-bottom:4px}
/* stories: one merged Capabilities+Examples narrative per app */
.d-stories{padding:54px 4vw 6px;max-width:1060px}
.story{display:grid;grid-template-columns:110px 1fr;gap:28px;padding:36px 0;border-top:1px solid var(--line)}
.story:first-child{border-top:0;padding-top:6px}
.story.flip{grid-template-columns:1fr 110px}
.story.flip .s-num{order:2;text-align:right}
.story.flip .s-main{order:1}
.s-num{font-family:var(--serif);font-size:62px;font-weight:700;line-height:1;color:#26262f}
.s-kicker{font-size:11px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:10px}
.story h3{font-family:var(--serif);font-size:clamp(22px,2.6vw,30px);font-weight:700;
  letter-spacing:-.3px;margin-bottom:10px;line-height:1.2}
.story p{font-size:15px;color:var(--mut);line-height:1.65;max-width:60ch;margin-bottom:14px}
.s-tags{display:flex;flex-wrap:wrap;gap:8px}
.tag{font-size:12px;font-weight:600;color:#d7d7de;border:1px solid var(--line);
  background:var(--bg2);border-radius:20px;padding:6px 13px}
.tag.ghost{border-style:dashed;color:var(--mut)}
.also{margin:34px 0 12px;padding:22px;border:1px dashed var(--line);border-radius:12px}
.also-k{display:block;font-size:11px;font-weight:800;letter-spacing:2.5px;
  text-transform:uppercase;color:var(--dim);margin-bottom:12px}
/* related: slim rows, no cloned homepage cards */
.d-rel{padding:44px 4vw 6px;max-width:1060px}
.d-rel h2{font-size:22px;margin-bottom:16px}
.rel-list{border-top:1px solid var(--line)}
.rel-row{display:flex;align-items:center;gap:16px;padding:15px 6px;border-bottom:1px solid var(--line)}
.rel-row:hover{background:rgba(255,255,255,.03)}
.rel-glyph{flex:0 0 44px;width:44px;height:44px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-family:var(--serif);font-weight:700;font-size:21px;color:rgba(255,255,255,.92)}
.rel-main{display:flex;flex-direction:column;gap:2px;min-width:0}
.rel-main b{font-size:15px}
.rel-main i{font-style:normal;font-size:13px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.rel-go{margin-left:auto;color:var(--dim);font-size:18px;transition:transform .15s,color .15s;flex:0 0 auto}
.rel-row:hover .rel-go{color:var(--brand);transform:translateX(4px)}

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

LOGO_DATA = "data:image/png;base64,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"
LOGO_IMG = '<img class="brand-logo" src="' + LOGO_DATA + '" alt="NavigatorsLab logo">'
LOGO_FAVICON = '<link rel="icon" type="image/png" href="' + LOGO_DATA + '">'


# ------------------------------------------------------------- templates ---

def art_style(a, big=False):
    return (f"background:linear-gradient({a['angle']},{a['c1']},{a['c2']});")

NAV = """
<header class="nav" id="nav">
  <a class="brand" href="/">' + LOGO_IMG + '<span class="brand-text">NavigatorLabs<small>local-first software</small></span></a>
  <nav class="nav-links">
    <a href="/" class="on">Home</a>
    <a href="/apps/reimagine-it/">Apps</a>
    <a href="/apps/integration-rot/">Developers</a>
    <a href="https://github.com/Kayforkind">GitHub</a>
  </nav>
  <div class="nav-right"><span class="pill"><b>7</b> apps · free · local-first</span></div>
</header>
<script>/* nav shade on scroll needs JS; static gradient is fine without it */</script>
"""

# NOTE: no-JS build — the script tag above is a comment-only placeholder; drop it.
NAV = NAV.replace("' + LOGO_IMG + '", LOGO_IMG)
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
                  "book-guide-mcp", "design-health-action", "liecatchers"]
    grid = "\n".join(card(BY_SLUG[s]) for s in collection)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>{LOGO_FAVICON}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NavigatorLabs — local-first, private-by-default software</title>
<meta name="description" content="Seven free, local-first apps: reimagine-it, integration-rot, PDF Studio, 23 private tools and more. No uploads, no accounts, no telemetry.">
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
  <p class="sub">Seven apps. One standard: free, local-first, no telemetry. Each appears once — pick yours.</p>
  <div class="grid">{grid}</div>
</section>
{FOOT}
</body>
</html>"""

def story_block(a, i, k, t, d, tags):
    tag_html = "".join(f'<span class="tag">{x}</span>' for x in tags)
    tags_row = f'<div class="s-tags">{tag_html}</div>' if tag_html else ""
    flip = " flip" if i % 2 else ""
    return (f'<article class="story{flip}">'
            f'<div class="s-num" aria-hidden="true">{i+1:02d}</div>'
            f'<div class="s-main"><div class="s-kicker" style="color:{a["c1"]}">{k}</div>'
            f"<h3>{t}</h3><p>{d}</p>{tags_row}</div></article>")


def detail(a):
    stories = "\n".join(
        story_block(a, i, k, t, d, tags)
        for i, (k, t, d, tags) in enumerate(a["stories"]))
    also = ""
    if a.get("also"):
        chips = "".join(f'<span class="tag ghost">{x}</span>' for x in a["also"])
        also = (f'<div class="also"><span class="also-k">Also in the box</span>'
                f'<div class="s-tags">{chips}</div></div>')
    meta_labels = {"ver": "Version", "lic": "License", "plat": "Platform", "star": "Notable"}
    key_order = {"ver": 0, "lic": 1, "plat": 2, "star": 3}
    specs = "".join(
        f'<span class="spec"><b>{meta_labels.get(k, k)}</b>{v}</span>'
        for v, k in sorted(a["meta"], key=lambda vk: key_order.get(vk[1], 9)))
    rel = "\n".join(
        f'<a class="rel-row" href="/apps/{s}/">'
        f'<span class="rel-glyph" style="background:linear-gradient('
        f'{BY_SLUG[s]["angle"]},{BY_SLUG[s]["c1"]},{BY_SLUG[s]["c2"]})">'
        f'{BY_SLUG[s]["glyph"]}</span>'
        f'<span class="rel-main"><b>{BY_SLUG[s]["name"]}</b>'
        f'<i>{BY_SLUG[s]["blurb"]}</i></span>'
        f'<span class="rel-go">&rarr;</span></a>'
        for s in a["likes"])
    note = ""
    if "note" in a:
        note = (f'<p class="d-note"><span class="tri">&diams;</span> {a["note"]} '
                f'<a href="{a["waitlist"]}">Join the waitlist &rarr;</a></p>')
    sec = ""
    if a.get("security"):
        grade, summary, tags, links = a["security"]
        tag_html = "".join(f'<span class="tag">{x}</span>' for x in tags)
        link_html = " &nbsp;&middot;&nbsp; ".join(
            f'<a href="{u}" style="color:{a["c1"]}">{t} &nearr;</a>' for t, u in links)
        sec = (f'<section class="d-stories" id="security">'
               f'<article class="story"><div class="s-num" aria-hidden="true">S</div>'
               f'<div class="s-main"><div class="s-kicker" style="color:{a["c1"]}">Security</div>'
               f"<h3>Audited, not promised &mdash; overall grade: {grade}</h3>"
               f"<p>{summary}</p>"
               f'<div class="s-tags">{tag_html}</div>'
               f'<p style="margin-top:14px">{link_html}</p>'
               f"</div></article></section>")
    flip = " r" if sum(ord(c) for c in a["slug"]) % 2 else " l"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>{LOGO_FAVICON}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{a['name']} &mdash; NavigatorLabs</title>
<meta name="description" content="{a['logline']}">
<link rel="stylesheet" href="/apps/style.css">
</head>
<body>
<div class="backbar"><a class="back" href="/">&lsaquo; All apps</a></div>
<section class="d-hero">
  <div class="slide-art" style="{art_style(a)}"></div>
  <div class="d-glyph{flip}" aria-hidden="true">{a['glyph']}</div>
  <div class="d-shade"></div>
  <div class="d-body">
    <div class="kicker"><span class="n">N</span><span class="tag">{a['badge']} &middot; {a['matchline']}</span></div>
    <h1 class="d-title">{a['name']}</h1>
    <p class="d-log">{a['logline']}</p>
    <div class="d-btns">
      <a class="btn btn-play" href="{a['open'][1]}"><span class="tri">&rtrif;</span> {a['open'][0]}</a>
      <a class="btn btn-more" href="{a['github']}">GitHub &nearr;</a>
    </div>
    {note}
    <div class="specbar">{specs}</div>
  </div>
</section>
<section class="d-stories">
{stories}
{also}
</section>
{sec}
<section class="d-rel">
  <h2>Elsewhere in the lab</h2>
  <div class="rel-list">{rel}</div>
</section>
{FOOT}
</body>
</html>"""

WORKER = """/* navigatorslab-home — Netflix-style NavigatorLabs site.
 * Routes:  /                 -> homepage
 *          /apps/style.css   -> shared stylesheet
 *          /apps/<slug>/     -> dedicated app page (7 apps)
 * Zone routes `navigatorslab.com/` and `navigatorslab.com/apps*` both point
 * here; every other path keeps serving via navigatorslab-tools.
 * Zero JavaScript, zero external fetches — all motion is CSS.
 */
addEventListener("fetch", function (event) { event.respondWith(handle(event.request)); });

var HEADERS_HTML = {
  "content-type": "text/html; charset=utf-8",
  "x-served-by": "navigatorslab-home",
  "content-security-policy": "default-src 'none'; script-src https://static.cloudflareinsights.com; connect-src https://static.cloudflareinsights.com https://cloudflareinsights.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; worker-src 'self' blob:; child-src 'self' blob:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
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
var HEADERS_SW = {
  "content-type": "text/javascript; charset=utf-8",
  "x-served-by": "navigatorslab-home",
  "cache-control": "no-store"
};
// Kill switch for the legacy "NavigatorsLab Tools" service worker (scope /)
// that used to serve the SPA homepage. Any browser still running it fetches
// this script on its update check, installs it, and on activate it unregisters
// itself, wipes the stale caches, and reloads controlled pages to the new site.
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
  if (p === "/apps/__diag__") { var hd = {}; req.headers.forEach(function (v, k) { hd[k] = v; }); return new Response(JSON.stringify({ worker: "navigatorslab-home", url: url.toString(), host: url.host, ray: hd["cf-ray"] || null, ip: hd["cf-connecting-ip"] || null, country: hd["cf-ipcountry"] || null }), { status: 200, headers: { "content-type": "application/json", "x-served-by": "navigatorslab-home", "cache-control": "no-store" } }); }
  if (p === "/") return new Response(PAGES.home, { status: 200, headers: HEADERS_HTML });
  if (p === "/apps/style.css") return new Response(CSS, { status: 200, headers: HEADERS_CSS });
  if (p === "/sw.js") return new Response(SW_KILL, { status: 200, headers: HEADERS_SW });
  var m = p.match(/^\\/apps\\/([a-z0-9-]+)\\/?$/);
  if (m && PAGES[m[1]]) return new Response(PAGES[m[1]], { status: 200, headers: HEADERS_HTML });
  if (p === "/apps" || p === "/apps/") return Response.redirect(url.origin + "/", 302);
  return new Response("not found", { status: 404, headers: HEADERS_HTML });
}
"""

def main():
    DIST.mkdir(exist_ok=True)
    (DIST / "apps").mkdir(exist_ok=True)
    pages = {"home": with_beacon(home())}
    (DIST / "home.html").write_text(pages["home"], encoding="utf-8")
    for a in APPS:
        html = with_beacon(detail(a))
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
