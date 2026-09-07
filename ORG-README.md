<p align="center">
  <img alt="NavigatorLabs" src="https://img.shields.io/badge/NavigatorLabs-local%E2%80%91first%20%C2%B7%20private%E2%80%91by%E2%80%91default-2dd4bf?style=for-the-badge&labelColor=0d1117">
</p>

<h1 align="center">NavigatorLabs</h1>

<p align="center">
  <strong>The lab where local-first, private-by-default software gets built, shipped, and documented.</strong><br>
  Founded and run by <a href="https://github.com/Kayforkind">Kazim Merchant</a> · <a href="https://navigatorslab.com">navigatorslab.com</a> · <a href="https://navigators.com">navigators.com</a>
</p>

---

## What we make

Every product is free, MIT-licensed, and runs where your data already lives — your machine, your browser. There is no server to trust because there is no server.

| Product | What it is | Try it |
|---|---|---|
| **[reimagine-it](https://github.com/Kayforkind/reimagine-it)** | Content-Derived Design — an engine that redesigns HTML from its own nouns, dates, numbers, and colors. 17 directions, deterministic audit, MCP server, live playground. CLI + Agent Skill for Claude Code, Cursor, Codex, Copilot, Gemini CLI. | [Playground](https://kayforkind.github.io/reimagine-it/#playground) · [npm](https://www.npmjs.com/package/reimagine-it) |
| **[PDF Studio](https://github.com/Kayforkind/NavigatorsLab-PDF-Studio)** | The free PDF editor that runs 100% in your browser — edits the text inside your PDF, fills forms, OCRs scans, signs, redacts, diffs revisions, on-device LLM. | [Open the editor](https://kayforkind.github.io/NavigatorsLab-PDF-Studio/) |
| **[Tools](https://github.com/Kayforkind/NavigatorsLab-Tools)** | Fifteen private in-browser utilities: GPS strip, image shrink, PDF sign/pages/merge, receipt OCR→CSV, private QR, word-level contract diff, audio trim, invoices, print prep. | [Use them](https://navigatorslab.com/tools/) |
| **[book-guide-mcp](https://github.com/Kayforkind/book-guide-mcp)** | Playbooks and tutors your coding agents run locally. Citations from books you own. No API keys for the core loop. | [GitHub](https://github.com/Kayforkind/book-guide-mcp) |
| **[study-guide](https://github.com/Kayforkind/study-guide)** | Exam-guides platform — certification prep with topic units and quizzes. | [GitHub](https://github.com/Kayforkind/study-guide) |
| **[design-health-action](https://github.com/Kayforkind/design-health-action)** | 18 deterministic design-quality checks for HTML as a GitHub Action. No LLM, no API key. | [GitHub](https://github.com/Kayforkind/design-health-action) |

## The guarantees — and the machinery behind them

**"No uploads, no accounts, no telemetry"** is not a policy; it is an architecture. And it is audited, not asserted:

- 🔒 **Private by architecture** — browser tools make zero network calls with your files; the CLI has zero runtime dependencies.
- 📦 **Provenance-signed releases** — npm packages ship with **SLSA provenance** and cosign signatures.
- 🛡️ **OpenSSF Scorecard 7.0** — Token-Permissions 10, Security-Policy 10, SHA-pinned CI, secret-scanning push protection.
- 🔁 **Proofs, not screenshots** — 17 committed design artifacts regenerate **byte-identically** in CI, including six real public-domain government pages (NPS, NASA, NOAA, Census, Federal Register, Smithsonian).
- ✅ **One protected main** — every change lands by PR through 16+ required checks; **116 tests** (68 unit + 20 MCP + 28 e2e) on a 155-file parity corpus.

## Upstream, not drive-bys

We send hard, reviewable fixes back to the tools we build on — [simonw/llm](https://github.com/simonw/llm) (#1613, merged), [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) (#966, #988, merged), [nullorder/agenthub](https://github.com/nullorder/agenthub) (#35, merged), with open work in [simonw/llm](https://github.com/simonw/llm) (#1612) and [pypa/hatch](https://github.com/pypa/hatch) (#2386).

---

<p align="center">
  <em>Local-first is a promise. Ours ships with a paper trail.</em>
</p>
