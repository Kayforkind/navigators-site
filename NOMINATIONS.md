# NavigatorLabs — nominations & submissions kit

Paste-ready copy for the directories, newsletters, and communities that accept
listings. Every number is verified as of **v2.13.1 (Sep 2026)**: 85★, 1,732
npm downloads/week, 23 releases, OpenSSF Scorecard 7.0, 116 tests, 96.8%
pairwise distinctness. Update numbers before submitting if time has passed.

Already merged (do not resubmit): VoltAgent/awesome-agent-skills (#966, #988),
nullorder/agenthub (#35).

---

## 1. Console.dev (newsletter + library)

**Where:** https://console.dev/submit/ — they feature dev tools with a strong
opinion on craft; reimagine-it fits their "developer tools that respect you" beat.

**Short pitch (their style, ~60 words):**

> reimagine-it turns an existing HTML page into a redesigned, standalone page
> built from that page's own content — its headings, dates, numbers, and
> colors. No AI-generated filler, no invented facts: the source file is the
> design brief. 17 design directions, a deterministic 19-rule audit, an MCP
> server, and a live playground. Offline, zero dependencies, MIT.

**Details form:**
- Name: reimagine-it
- Link: https://github.com/Kayforkind/reimagine-it
- Docs/Playground: https://kayforkind.github.io/reimagine-it/#playground
- npm: `npx reimagine-it --auto -i page.html -o redesign.html`
- Category: Design / Developer tools / AI agents
- Pricing: Free, MIT

---

## 2. dev.to article (publish-ready)

**Title:** `I built a design engine that refuses to invent facts (85★, zero dependencies)`

**Tags:** `webdev`, `css`, `ai`, `opensource`

**Intro (paste + expand):**

> Every "AI redesign" tool does the same trick: it throws your content away
> and hallucinates a prettier page. reimagine-it goes the other direction —
> it extracts the nouns, dates, numbers, emails, and hex colors already in
> your HTML and builds the design *around them*. A bakery cannot come out
> marine-teal. The engine is deterministic, offline, zero-dependency, and
> audited: 19 rules, 116 tests, and 17 committed artifacts that regenerate
> byte-identically in CI — including six real government pages (NPS, NASA,
> NOAA, Census, Federal Register, Smithsonian).
>
> This post walks through how Content-Derived Design works, why "never
> invent facts" is a harder engineering constraint than it sounds, and what
> shipping with SLSA provenance + an OpenSSF Scorecard of 7.0 looks like
> for a solo-maintained open-source project.

**Cover image:** `docs/og.png` from the reimagine-it repo (14-source wall).

---

## 3. Hacker News (Show HNC)

**Title:** `Show HN: Reimagine-it – redesign HTML from its own content, offline, no AI API`

**Comment body (first comment, factual tone):**

> Hi HN — I built reimagine-it because every "AI redesign" tool I tried
> invented content. This one treats the source file as the design brief:
> it extracts real headings, dates, numbers, emails, and colors, and
> generates a standalone redesign in one of 17 directions. Deterministic,
> offline, zero runtime dependencies, no API keys.
>
> Try it without installing: https://kayforkind.github.io/reimagine-it/#playground
> Repo: https://github.com/Kayforkind/reimagine-it (MIT, OpenSSF Scorecard 7.0,
> npm releases with SLSA provenance)
>
> The honest limits: HTML in, HTML out (no PDF/PPTX/DOCX), and the audit
> checks markup contracts — it can't tell you if a design is *beautiful*,
> only that it's complete, accessible, and faithful to the source.
>
> Happy to answer questions about the extraction pipeline or the
> reproducibility setup (17 artifacts regenerate byte-identically in CI).

---

## 4. Reddit

**r/webdev** — title: `I built an offline design engine that never invents facts — it redesigns HTML using only the content already in the file (MIT, no API keys)`

**r/SideProject** — title: `I spent 3 months building a deterministic alternative to AI mood-board redesigners. 85★, 1.7k npm downloads/week, zero dependencies.`

**Body (both subs, ~150 words):**

> The idea: your HTML file is already the design brief. reimagine-it extracts
> the actual nouns, dates, numbers, emails, and hex colors from your page and
> generates a redesign from them — 17 directions (infographic, dashboard,
> lookbook, simulation, landing...), all deterministic and seeded, so the
> same input + seed always produces the same output. Byte-identical proofs
> run in CI, including six real government pages.
>
> - Live playground (no install): https://kayforkind.github.io/reimagine-it/#playground
> - Repo: https://github.com/Kayforkind/reimagine-it
> - CLI: `npx reimagine-it --auto -i page.html -o out.html`
>
> It also ships as an Agent Skill for Claude Code / Cursor / Codex / Copilot
> / Gemini CLI, an MCP server, and a GitHub Action. MIT, zero runtime
> dependencies, no API keys, no telemetry.

---

## 5. GitHub Trending (organic — how to position for it)

Not submittable; driven by stars/velocity in a window. Levers that are legit:
- Announce v2.14.0 with the new site (navigators.com) on the same day as a
  dev.to post + HN Show HN — concentrated traffic beats spread-out mentions.
- Pin the playground link in every surface (README already does).
- Ask early stargazers (the 85) to try the playground — engagement signals.

---

## 6. Other listings (quick forms)

| Directory | Action | Notes |
|---|---|---|
| [AlternativeTo](https://alternativeto.net/) | Add as alternative to "Figma AI" / "Relume" | Angle: offline + deterministic |
| [Product Hunt](https://www.producthunt.com/) | Launch when v2.14 + site ship | Note: name collision with reimagineit.ai — tagline must lead with "Content-Derived Design" |
| [awesome-claude-skills](https://github.com/hesreallyhim/awesome-claude-skills) | PR adding reimagine-it under Design | Same copy as VoltAgent PR (#966) |
| [mcp.so](https://mcp.so/) + [Smithery](https://smithery.ai/) | Submit the MCP server | Book-guide-mcp AND reimagine-it's MCP |
| [OpenAlternative](https://openalternative.co/) | Submit PDF Studio + Tools | Angle: private alternatives to Adobe/SmallPDF |
| [There's An AI For That](https://theresanaiforthat.com/) | Submit reimagine-it | Category: design/dev tools |

---

## Posting checklist (before any submit)

1. Numbers current? (stars, downloads — update from live APIs, not memory)
2. Playground link works?
3. The two install doors in README still match the copy? (`npx reimagine-it`, `npx skills add Kayforkind/reimagine-it`)
4. Not the same week as a name-collision competitor launch — check reimagineit.ai
