"""Build static HTML for navigatorslab.com + /apps/<slug>/ into worker-home/public/.

Scrolltide-inspired cinematic design with:
- Dual-host NotebookLM Audio/Video Deep-Dive Overview (/tools/videos/notebooklm-overview.mp4)
- 16:9 per-tool demo videos (/tools/videos/<tid>.mp4) & posters (/tools/shots/<tid>.jpg)
- Concrete Input -> Engine -> Output examples & sample outputs on every card and detail page
- Interactive category filtering & search
- Preserves all 29 verification checks in worker-home/verify.py.
"""
from __future__ import annotations
import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "public"

APPS: list[dict[str, str]] = [
    {
        "slug": "pdf-studio",
        "tid": "pdfstudio",
        "cat": "flagship",
        "cat_label": "Flagship Web App",
        "name": "NavigatorsLab PDF Studio",
        "repo": "NavigatorsLab-PDF-Studio",
        "live": "https://navigatorslab.com/pdf-studio/",
        "summary": "Browser-based PDF workspace for viewing, true in-place text editing, AcroForm filling, page organization, signing, vector redaction, revision diffing, and Tesseract WASM OCR.",
        "how_to_use": "Open the live web app at navigatorslab.com/pdf-studio/ in a modern desktop browser, or clone the repository and run npm install && npm run build.",
        "input_ex": "Scanned-Contract.pdf (12 pages, upside-down page 4, SSNs visible, unsigned)",
        "engine_ex": "Client-side PDF content-stream rewriter + Tesseract WASM OCR + vector redaction + on-device AI",
        "output_ex": "Contract-Edited-Signed.pdf (In-place text edited, OCR layer added, SSNs purged from bytes, signed)",
        "sample_code": "Stream Rewrite: /Contents updated in-place | Redaction: vector paths purged | OCR: searchable text layer ✓",
        "caveat": "Large PDFs and OCR run in-browser and are bounded by available tab memory; scanned-PDF OCR downloads language data on first use.",
    },
    {
        "slug": "tools",
        "tid": "exif",
        "cat": "flagship",
        "cat_label": "Flagship Suite (24 Tools)",
        "name": "NavigatorsLab Tools",
        "repo": "NavigatorsLab-Tools",
        "live": "https://navigatorslab.com/tools/",
        "summary": "Suite of 24 client-side browser utilities and local-first tools covering EXIF stripping, image shrinking, scan cleaning, e-signing, receipt OCR, QR codes, audio trimming, invoices, and text diffing.",
        "how_to_use": "Use any tool directly at navigatorslab.com/tools/ (installable as an offline PWA), or call the stateless MCP server at navigatorslab.com/tools/mcp.",
        "input_ex": "Photos with GPS leaks, 16 MB scans, crumpled receipts, unsigned NDAs, or voice notes",
        "engine_ex": "24 specialized engines (WebAssembly Tesseract, LAME MP3, pdf-lib, pdf.js, WebCrypto SHA-1) under CSP default-src 'none'",
        "output_ex": "Cleaned JPEGs, <=300 KB compressed images, expenses.csv, flattened signed PDFs, MP3 clips, and diffs",
        "sample_code": "CSP: default-src 'none' | 39/39 Playwright E2E checks green | 0 bytes uploaded to any server ✓",
        "caveat": "All processing happens in the local browser tab; clearing site data removes cached offline assets, and Password Breach Checker queries api.pwnedpasswords.com using a 5-character SHA-1 prefix.",
    },
    {
        "slug": "reimagine-it",
        "tid": "reimagine",
        "cat": "flagship",
        "cat_label": "Flagship Web App",
        "name": "reimagine-it",
        "repo": "reimagine-it",
        "live": "https://navigatorslab.com/reimagine/",
        "summary": "Client-side HTML redesign playground that extracts headings, metrics, dates, and palette colors from existing markup and rebuilds the page across 17 layout directions.",
        "how_to_use": "Open navigatorslab.com/reimagine/ to paste HTML or try built-in presets in the browser, or run locally from source with npm install && npm run build.",
        "input_ex": "Dense, unstyled HTML report or documentation page with tables, dates, and metrics",
        "engine_ex": "Pure TypeScript content-extraction AST layout engine + optional Three.js 3D renderer",
        "output_ex": "17 complete redesigned HTML pages (Infographic, Editorial, 3D, Cinematic, Dashboard, Magazine...)",
        "sample_code": "Extracted: 14 metrics, 6 dates, 4 sections -> Rebuilt into 17 visual directions (0 hallucinated words) ✓",
        "caveat": "Output quality depends on semantic structure in the source HTML; heavily obfuscated or canvas-only pages yield sparser extractions.",
    },
    {
        "slug": "design-health-action",
        "tid": "designhealth",
        "cat": "agents",
        "cat_label": "CI & Design Gate",
        "name": "Design Health Action",
        "repo": "design-health-action",
        "live": "",
        "summary": "Deterministic HTML/CSS design-quality checker for GitHub Actions that evaluates 18 rules across typography, palette, motion, content, structure, and performance without an LLM.",
        "how_to_use": "Add uses: Kayforkind/design-health-action@main to a GitHub Actions workflow pointed at your built HTML directory, or run the script locally with Node.js.",
        "input_ex": "Built static HTML files in CI (`path: \"dist/**/*.html\"`)",
        "engine_step": "18 deterministic DOM & CSS static analysis rules (zero API keys, zero LLM calls)",
        "output_ex": "Pass/Fail CI Gate report covering Hierarchy, Contrast, prefers-reduced-motion, :focus-visible & CLS",
        "sample_code": "Rule 01..18 evaluated in 1.2s -> Typography 3/3, Palette 3/3, Motion 3/3, Structure 3/3 -> PASS ✓",
        "caveat": "Evaluates static HTML/CSS heuristics rather than full visual rendering across every browser engine.",
    },
    {
        "slug": "skill-slice",
        "tid": "skillslice",
        "cat": "agents",
        "cat_label": "Agent Skills & CLI",
        "name": "Skill Slice",
        "repo": "skill-slice",
        "live": "https://kayforkind.github.io/skill-slice/",
        "summary": "Catalog and installer pattern for copying individual SKILL.md folders into coding-agent workspaces one skill at a time instead of bulk-installing entire repositories.",
        "how_to_use": "Browse the catalog at kayforkind.github.io/skill-slice/ and copy a single skill folder or run npx skills add with a specific --skill name.",
        "input_ex": "Coding agent needs one specific workflow skill without polluting context with 500 unverified files",
        "engine_ex": "Progressive-disclosure SKILL.md folders with 12 Read-verified chairs documented in WORKS_VERIFIED.md",
        "output_ex": "Single verified skill folder installed cleanly into `.claude/skills/<name>/SKILL.md`",
        "sample_code": "$ npx skills add kazimrmerchant/skill-slice --skill systematic-debugging -> 1 verified skill copied ✓",
        "caveat": "Only the subset listed in docs/WORKS_VERIFIED.md has been Read-verified; skills are procedural prompts, not sandboxed executables.",
    },
    {
        "slug": "liecatchers",
        "tid": "liecatchers",
        "cat": "agents",
        "cat_label": "Agent Verification CLI",
        "name": "liecatchers",
        "repo": "liecatchers",
        "live": "https://navigatorslab.com/tools/detail.html?id=liecatchers",
        "summary": "Post-run verification CLI for coding agents that checks declared commands, git diffs, lockfiles, and file contracts, then writes a machine-readable RECEIPT.json.",
        "how_to_use": "Clone https://github.com/Kayforkind/liecatchers and run uvx --from . liecatcher run inside a target workspace on Windows or POSIX.",
        "input_ex": "Coding agent claims 'All tests pass and PR is ready!' at the end of a turn",
        "engine_ex": "10 workspace sensors inspect command history, git diff paths, lockfile integrity, native binaries & handoffs",
        "output_ex": "Cryptographically signed `RECEIPT.json` (Exit 0 if all 10 sensors pass; Exit 1 with failure evidence if agent lied)",
        "sample_code": "$ uvx --from . liecatcher run -> Sensors 10/10 PASS -> Signed RECEIPT.json emitted ✓",
        "caveat": "Verifies workspace artifacts and command evidence after a run; it does not sandbox or prevent commands while an agent is executing.",
    },
    {
        "slug": "book-guide-mcp",
        "tid": "bookguide",
        "cat": "agents",
        "cat_label": "Local-First MCP Server",
        "name": "Book Guide MCP",
        "repo": "book-guide-mcp",
        "live": "https://navigatorslab.com/tools/detail.html?id=bookguide",
        "summary": "Local-first Python Model Context Protocol (MCP) server over stdio for indexing user-supplied books, citing passages with locators, and running structured study playbooks.",
        "how_to_use": "Install from https://github.com/Kayforkind/book-guide-mcp with Python/uv and register the stdio server command in your MCP client configuration.",
        "input_ex": "Your local folder of technical books (PDF / EPUB / Markdown) + an MCP host (Cursor, Claude, Antigravity)",
        "engine_ex": "Python MCP stdio server progressing from L0 Library indexing to L4 Socratic & Avicenna tutors",
        "output_ex": "Exact chapter/page locator citations and structured engineering playbooks inside your coding agent",
        "sample_code": "mcp://book-guide/cite?book=ddia&topic=consensus -> Chapter 9, p. 324 locator + playbook ✓",
        "caveat": "Requires user-provided book files and a local Python runtime; does not bundle copyrighted books or hosted API endpoints.",
    },
    {
        "slug": "data-insights",
        "tid": "datainsights",
        "cat": "agents",
        "cat_label": "Intelligence Platform",
        "name": "Data Insights",
        "repo": "data-insights",
        "live": "https://navigatorslab.com/tools/detail.html?id=datainsights",
        "summary": "Node.js signal-aggregation workspace that compiles public technology, startup, security, and research feeds into daily 5W1H briefs and weekly synthesis reports.",
        "how_to_use": "Clone https://github.com/Kayforkind/data-insights, run npm install && npm run dev, and open the local web portal on port 3000.",
        "input_ex": "Public RSS/API feeds across technology, security advisories, arXiv preprints, and startup releases",
        "engine_ex": "Node.js signal normalizer, 5W1H daily synthesizer, momentum scorer & JSON API server",
        "output_ex": "Headline river portal, Daily 5W1H report, Weekly executive PDF brief, and agent JSON endpoints",
        "sample_code": "GET /api/briefs/daily -> 5W1H synthesis + source availability history + print-ready weekly PDF ✓",
        "caveat": "Requires local Node.js execution and outbound network access to fetch live public RSS/API feeds.",
    },
    {
        "slug": "iron-axe-legacy",
        "tid": "ironaxe",
        "cat": "flagship",
        "cat_label": "Godot 4 Game",
        "name": "Iron Axe: Legacy",
        "repo": "iron-axe-legacy",
        "live": "https://navigatorslab.com/tools/detail.html?id=ironaxe",
        "summary": "Open-source side-scrolling beat 'em up prototype built in Godot 4 featuring original characters, combo chains, throws, elevation lanes, and particle effects.",
        "how_to_use": "Clone https://github.com/Kayforkind/iron-axe-legacy, open project.godot in Godot Engine 4.3+, and run the main scene.",
        "input_ex": "Keyboard or Gamepad combat inputs in Godot 4.3+ runtime",
        "engine_ex": "GDScript state-machine combat engine with hitstop frames, elevation lanes, throws & team magic",
        "output_ex": "60 FPS arcade beat-'em-up gameplay with 100% original sprites, stages, and MIT-licensed source",
        "sample_code": "State: COMBO_3 -> Hitstop(60ms) -> ScreenShake(4px) -> SpawnHitSpark() ✓",
        "caveat": "Active prototype under development; requires Godot 4.3+ to build or play from source.",
    },
    {
        "slug": "integration-rot",
        "tid": "textdiff",
        "cat": "agents",
        "cat_label": "Developer CLI + MCP",
        "name": "integration-rot",
        "repo": "integration-rot",
        "live": "https://navigatorslab.com/Integrationrot",
        "summary": "Find uses of aging APIs across 76 SDK packages, draft migrations, and verify changes with generated contract tests.",
        "how_to_use": "Open navigatorslab.com/Integrationrot or run the CLI from https://github.com/Kayforkind/integration-rot against your project lockfile and source tree.",
        "input_ex": "Repository package.json / requirements.txt + source tree calling deprecated SDK methods",
        "engine_ex": "AST call-site scanner across 76 SDKs + migration diff drafter + contract test generator",
        "output_ex": "Pinpointed SDK deprecation report, migration patch, and runnable contract test suite",
        "sample_code": "$ npx integration-rot scan . -> 76 SDK catalog checked -> 3 aging endpoints flagged + patch ✓",
        "caveat": "Review generated migrations and test assumptions before merging.",
    },
    {
        "slug": "redact-lint",
        "tid": "pdfstudio",
        "cat": "privacy",
        "cat_label": "Rust CLI + Python + Action",
        "name": "redact-lint",
        "repo": "redact-lint",
        "live": "",
        "summary": "Catch fake PDF redactions before they ship — detects painted-over black rectangles where underlying text streams remain extractable.",
        "how_to_use": "Install from https://github.com/Kayforkind/redact-lint and run redact-lint on any PDF directory or in GitHub Actions CI before publishing.",
        "input_ex": "Legal-Filing.pdf where a black rectangle was drawn over sensitive names instead of purging text bytes",
        "engine_ex": "Rust PDF content-stream & vector bounding-box overlap analyzer",
        "output_ex": "CI exit code 1 with exact page/bounding-box coordinates of extractable text hidden under vector boxes",
        "sample_code": "$ redact-lint filing.pdf -> [FAIL] Page 3: 18 chars extractable under black rect (142,510..310,524) ✓",
        "caveat": "Scans extractable PDF text streams and vector geometry; raster-only image leaks require OCR review.",
    },
    {
        "slug": "api-watch",
        "tid": "datainsights",
        "cat": "agents",
        "cat_label": "Node 20+ CLI",
        "name": "api-watch",
        "repo": "api-watch",
        "live": "",
        "summary": "API response contracts with secret-safe environment references, bounded reads, and CI reports.",
        "how_to_use": "Clone https://github.com/Kayforkind/api-watch and run the CLI against your endpoint contract definitions in CI.",
        "input_ex": "Declarative JSON contract specifying expected HTTP status, headers, latency budget & JSON schema",
        "engine_ex": "Node 20+ bounded response reader + secret-safe env resolver + deterministic schema validator",
        "output_ex": "Zero-leak CI contract verification report with schema drift & latency breakdown",
        "sample_code": "$ npx api-watch verify contracts.json -> 12/12 endpoints match schema (0 secrets logged) ✓",
        "caveat": "Targets are trusted configuration; this is not a public SSRF-safe URL proxy.",
    },
    {
        "slug": "pdf-a11y-check",
        "tid": "pdfpages",
        "cat": "documents",
        "cat_label": "Node 20+ CLI",
        "name": "pdf-a11y-check",
        "repo": "pdf-a11y-check",
        "live": "",
        "summary": "Bounded PDF accessibility pre-flight checks for language, tags, title, figure alternatives, and tab order.",
        "how_to_use": "Run pdf-a11y-check from https://github.com/Kayforkind/pdf-a11y-check on exported PDFs in local builds or CI pipelines.",
        "input_ex": "Public-Report.pdf exported without /Lang, /StructTreeRoot tags, or /Alt text on figures",
        "engine_ex": "Deterministic PDF catalog, structure tree, figure /Alt, and page tab-order inspector",
        "output_ex": "Structured JSON & terminal pre-flight report pinpointing missing accessibility metadata",
        "sample_code": "$ npx pdf-a11y-check report.pdf -> Checks: /Lang, /StructTreeRoot, /Title, Figure /Alt, /Tabs ✓",
        "caveat": "Heuristic pre-flight only — not PDF/UA certification or malware clearance.",
    },
    {
        "slug": "design-gate",
        "tid": "designhealth",
        "cat": "agents",
        "cat_label": "Node 20+ CLI",
        "name": "design-gate",
        "repo": "design-gate",
        "live": "",
        "summary": "Bounded structural checks for generated HTML with escaped reports and configurable CI thresholds.",
        "how_to_use": "Run design-gate from https://github.com/Kayforkind/design-gate against generated HTML files before deployment.",
        "input_ex": "AI-generated or template-built HTML pages awaiting deployment",
        "engine_ex": "Bounded DOM & CSS structural analyzer with escaped HTML reporting and threshold gates",
        "output_ex": "Deterministic score report and CI pass/fail exit code",
        "sample_code": "$ npx design-gate dist/index.html --min-score 90 -> Score 96/100 (PASS) ✓",
        "caveat": "Not an HTML sanitizer or accessibility certification.",
    },
    {
        "slug": "skills-registry",
        "tid": "skillslice",
        "cat": "agents",
        "cat_label": "Node CLI + Static HTML",
        "name": "skills-registry",
        "repo": "skills-registry",
        "live": "",
        "summary": "Build a searchable static index of agent skills with heuristic risk checks and SHA-256 digests.",
        "how_to_use": "Run skills-registry from https://github.com/Kayforkind/skills-registry on a directory of SKILL.md folders to emit a static searchable catalog.",
        "input_ex": "Directory of SKILL.md folders and helper scripts for coding agents",
        "engine_ex": "SHA-256 file hasher + heuristic prompt/shell risk scanner + static HTML catalog builder",
        "output_ex": "Self-contained searchable HTML registry with per-skill SHA-256 digests and risk badges",
        "sample_code": "$ npx skills-registry build ./skills -> Indexed 24 skills with SHA-256 digests & risk flags ✓",
        "caveat": "Risk patterns are heuristics; 'checked' is not safety approval.",
    },
    {
        "slug": "share-safe",
        "tid": "metadata",
        "cat": "privacy",
        "cat_label": "Node 20+ CLI",
        "name": "share-safe",
        "repo": "share-safe",
        "live": "",
        "summary": "Remove selected PDF metadata and actions, prune unreachable payloads, and recheck the saved output.",
        "how_to_use": "Run share-safe from https://github.com/Kayforkind/share-safe on PDFs before external distribution.",
        "input_ex": "Draft.pdf containing /Info author dictionaries, /Metadata XMP streams, and /OpenAction triggers",
        "engine_ex": "PDF dictionary scrubber + unreachable object pruner + post-save re-inspector",
        "output_ex": "Sanitized PDF verified free of /Info, /XMP, /JavaScript, and /OpenAction keys",
        "sample_code": "$ npx share-safe clean draft.pdf out.pdf -> Stripped /Info, /XMP, /OpenAction -> Re-verified 0 leaks ✓",
        "caveat": "Not full anonymization, content redaction, or malware scanning; manually review forms, annotations, visible content and media.",
    },
    {
        "slug": "privacy-plugin",
        "tid": "metadata",
        "cat": "privacy",
        "cat_label": "Claude Code Plugin",
        "name": "navigatorslab-privacy-tools",
        "repo": "privacy-plugin",
        "live": "",
        "summary": "Read-only local PDF parsing, extraction, and search through bundled MCP tools.",
        "how_to_use": "Install from https://github.com/Kayforkind/privacy-plugin into Claude Code or any MCP-compatible client.",
        "input_ex": "Local PDF documents queried inside an MCP-enabled coding agent session",
        "engine_ex": "Read-only local PDF parser, page-range extractor, and regex search MCP server",
        "output_ex": "Structured page text and metadata responses returned over local stdio",
        "sample_code": "mcp://privacy-plugin/pdf_search?path=spec.pdf&q=indentation -> 4 matches with page numbers ✓",
        "caveat": "Extracted text enters the AI client context and may reach its model provider.",
    },
    {
        "slug": "agent-receipts",
        "tid": "liecatchers",
        "cat": "agents",
        "cat_label": "Node 20+ CLI",
        "name": "agent-receipts",
        "repo": "agent-receipts",
        "live": "",
        "summary": "Record bounded check outcomes and root-confined artifact hashes; verify receipts and optional Ed25519 signatures.",
        "how_to_use": "Run agent-receipts from https://github.com/Kayforkind/agent-receipts to emit and verify signed build/test receipts.",
        "input_ex": "Build artifacts and test command exit codes from an automated agent workflow",
        "engine_ex": "Root-confined SHA-256 artifact hasher + Ed25519 receipt signer and offline verifier",
        "output_ex": "Signed JSON receipt verified offline without re-executing untrusted commands",
        "sample_code": "$ npx agent-receipts verify receipt.json --pubkey key.pub -> SHA-256 & Ed25519 signature VALID ✓",
        "caveat": "Signatures show possession of a key, not that checks ran honestly; verification never executes commands.",
    },
    {
        "slug": "health-claims",
        "tid": "textstats",
        "cat": "documents",
        "cat_label": "Node 20+ CLI",
        "name": "sourced-claims",
        "repo": "health-claims",
        "live": "",
        "summary": "Validate sourced-claim data, calendar dates, human review fields, and review freshness; render a safe report template.",
        "how_to_use": "Run sourced-claims from https://github.com/Kayforkind/health-claims on structured claim JSON datasets.",
        "input_ex": "JSON dataset of factual claims, source DOIs/URLs, reviewer sign-offs, and review dates",
        "engine_ex": "Strict calendar-date, freshness-window, citation-link, and human-reviewer schema validator",
        "output_ex": "Escaped HTML audit report flagging stale reviews or missing source citations",
        "sample_code": "$ npx sourced-claims check claims.json -> 42/42 claims within 90-day review window -> Report rendered ✓",
        "caveat": "Not medical advice or scientific evaluation; a passing schema does not establish claim truth.",
    },
    {
        "slug": "photo-privacy-kit",
        "tid": "exif",
        "cat": "privacy",
        "cat_label": "Privacy & Security",
        "name": "Photo Privacy Kit",
        "repo": "NavigatorsLab-Photo-Privacy-Kit",
        "live": "https://navigatorslab.com/tools/exif.html",
        "summary": "In-browser JPEG, PNG, and WebP metadata inspector and stripper that removes EXIF, GPS, XMP, and IPTC segments while verifying pixel integrity via SHA-256.",
        "how_to_use": "Open navigatorslab.com/tools/exif.html, drop or paste an image, review the detected metadata fields, and download the stripped copy.",
        "input_ex": "vacation-photo.jpg (3.4 MB) leaking GPS 41.0082° N, 28.9784° E, iPhone 15 Pro & embedded thumbnail",
        "engine_ex": "Byte-level JPEG APP1/APP13/COM, PNG & WebP segment parser — never decodes or re-encodes pixels",
        "output_ex": "clean-vacation-photo.jpg with 0 EXIF/GPS bytes and SHA-256 proof that decoded pixels are 100% identical",
        "sample_code": "GPS: STRIPPED | APP1: REMOVED | Pixel SHA-256: 9f84c2...e10b (Byte-identical pixels) ✓",
        "caveat": "Strips container metadata segments (EXIF/XMP/IPTC/comments); it does not blur or redact faces, license plates, or text visible inside the image pixels.",
    },
    {
        "slug": "metadata-checker",
        "tid": "metadata",
        "cat": "privacy",
        "cat_label": "Privacy & Security",
        "name": "Metadata & Hidden-Data Checker",
        "repo": "NavigatorsLab-Metadata-Checker",
        "live": "https://navigatorslab.com/tools/metadata.html",
        "summary": "Local file inspector for PDF, DOCX, XLSX, PPTX, ODT, and image files that displays author names, revision counts, editing time, and XMP streams before exporting a cleaned copy.",
        "how_to_use": "Open navigatorslab.com/tools/metadata.html, drop a document or image, inspect the reported fields, and click export to save a cleaned version.",
        "input_ex": "Board-Proposal.docx & Contract.pdf containing hidden Author, Company, 14 revisions & 312m editing time",
        "engine_ex": "pdf-lib Info/XMP parser + OOXML/ODF ZIP central-directory & XML rewriter in the browser tab",
        "output_ex": "Cleaned DOCX/PDF with Author, Company, revision history & XMP streams wiped and re-verified clean",
        "sample_code": "Author: REMOVED | Company: REMOVED | TotalTime: 0 | Re-inspection: 0 hidden fields ✓",
        "caveat": "Cleans standard metadata dictionaries and package properties; tracked changes or comments embedded inside document body text should still be reviewed manually.",
    },
    {
        "slug": "image-shrinker",
        "tid": "shrink",
        "cat": "images",
        "cat_label": "Images & Print",
        "name": "Image Shrinker",
        "repo": "NavigatorsLab-Image-Shrinker",
        "live": "https://navigatorslab.com/tools/shrink.html",
        "summary": "Client-side batch image compressor that binary-searches JPEG, WebP, or AVIF encoder quality to hit a target file-size ceiling such as 300 KB or 2 MB.",
        "how_to_use": "Open navigatorslab.com/tools/shrink.html, drop one or more images, set your target kilobyte or megabyte cap, and download the compressed files or ZIP.",
        "input_ex": "passport-scan.png (16.0 MB, 4000×3000) rejected by a government portal with a strict 300 KB limit",
        "engine_ex": "8-step binary search over HTML5 Canvas JPEG/WebP/AVIF quality + scale fallback + JSZip batch bundler",
        "output_ex": "passport-scan-shrunk.jpg (294 KB — safely under the 300 KB cap on the first try)",
        "sample_code": "Source: 16,777,216 B -> Target: <=300 KB -> Output: 294,112 B (98.2% reduction) ✓",
        "caveat": "AVIF encoding support depends on the host browser's native Canvas encoder implementation.",
    },
    {
        "slug": "scan-cleaner",
        "tid": "scan",
        "cat": "documents",
        "cat_label": "PDF & Documents",
        "name": "Scan & Screenshot Cleaner",
        "repo": "NavigatorsLab-Scan-Cleaner",
        "live": "https://navigatorslab.com/tools/scan.html",
        "summary": "Document photo cleaner that performs deskewing, auto-levels, grayscale/photocopy thresholding, and interactive cropping, then exports a multi-page 300-DPI PDF.",
        "how_to_use": "Open navigatorslab.com/tools/scan.html, drop phone photos of documents, adjust crop or threshold controls, and export as PNG or PDF.",
        "input_ex": "Skewed, shadowed phone photos of a 3-page paper contract taken on a dark desk",
        "engine_ex": "Canvas ±4° deskew search + auto-levels normalization + photocopy threshold + pdf-lib 300-DPI builder",
        "output_ex": "Crisp, straight, high-contrast 3-page 300-DPI PDF ready for printing or archiving",
        "sample_code": "Deskew: -2.8° | Contrast: Photocopy B&W | Output: 2-page 300-DPI PDF (53 KB) ✓",
        "caveat": "Auto-crop and deskew work best when the document edges have clear contrast against the background surface.",
    },
    {
        "slug": "e-sign-pad",
        "tid": "sign",
        "cat": "documents",
        "cat_label": "PDF & Documents",
        "name": "Local E-Sign Pad",
        "repo": "NavigatorsLab-E-Sign-Pad",
        "live": "https://navigatorslab.com/tools/sign.html",
        "summary": "In-browser PDF signer that lets you draw or type a signature, position it on any page with an optional date stamp, and flatten the ink into the PDF.",
        "how_to_use": "Open navigatorslab.com/tools/sign.html, load a PDF, draw or type your signature, click to place it on the page preview, and download the flattened PDF.",
        "input_ex": "Lease-Agreement.pdf requiring a signature and date stamp before midnight",
        "engine_ex": "HTML5 signature pad + pdf.js live placement preview + pdf-lib page resource flattening",
        "output_ex": "Lease-Agreement-signed.pdf with ink and date permanently flattened into page content (0 form fields)",
        "sample_code": "Embedded XObject signature + date caption (2026-11-08) | Editable fields left: 0 ✓",
        "caveat": "Produces a visual signature flattened into page content; it does not attach a cryptographic X.509 certificate or PKI digital signature.",
    },
    {
        "slug": "receipts-to-pdf",
        "tid": "receipts",
        "cat": "money",
        "cat_label": "Money & OCR",
        "name": "Receipts to One PDF",
        "repo": "NavigatorsLab-Receipts-to-PDF",
        "live": "https://navigatorslab.com/tools/receipts.html",
        "summary": "Combines multiple receipt photos into a single chronologically sorted PDF using EXIF capture dates and stamps each page header with its date and filename.",
        "how_to_use": "Open navigatorslab.com/tools/receipts.html, drop a batch of receipt images, reorder or rotate if needed, and export the combined PDF.",
        "input_ex": "Shoebox of 15 unsorted receipt photos from a business trip with staggered capture dates",
        "engine_ex": "EXIF DateTimeOriginal parser + chronological sorter + pdf-lib page header stamper",
        "output_ex": "Single chronologically ordered PDF with every page stamped with capture date and source filename",
        "sample_code": "Sorted 3 receipts by EXIF date -> Stamped headers -> Built 3-page PDF (108 KB) ✓",
        "caveat": "Images without EXIF capture timestamps fall back to the file's last-modified date for sorting.",
    },
    {
        "slug": "receipt-ocr",
        "tid": "ocr",
        "cat": "money",
        "cat_label": "Money & OCR",
        "name": "Receipt OCR to CSV",
        "repo": "NavigatorsLab-Receipt-OCR",
        "live": "https://navigatorslab.com/tools/ocr.html",
        "summary": "Runs self-hosted Tesseract WebAssembly OCR on receipt images in the browser to extract vendor, date, and total lines into an editable table that exports to CSV or TSV.",
        "how_to_use": "Open navigatorslab.com/tools/ocr.html, drop receipt photos, review or edit any low-confidence cells, and export expenses.csv.",
        "input_ex": "Photos of printed grocery, coffee, and hardware store receipts ('GREEN GROCER ... TOTAL $23.98')",
        "engine_ex": "Self-hosted Tesseract WebAssembly engine + vendor/date/total heuristic parser + confidence scorer",
        "output_ex": "Editable expense table exported as `expenses.csv` for Excel, Google Sheets, or QuickBooks",
        "sample_code": "date,vendor,category,currency,total,confidence -> 2026-09-14,GREEN GROCER,Meals,USD,23.98,94% ✓",
        "caveat": "First run downloads ~24 MB of same-origin Tesseract WASM/traineddata (cached afterward); faded thermal ink or crumpled receipts may require manual cell edits.",
    },
]

assert len(APPS) >= 16, f"Expected at least 16 apps, got {len(APPS)}"

CSS = """:root {
  --bg: #05070d;
  --bg-elev: #0b101c;
  --panel: #0f1626;
  --panel-hi: #141e33;
  --line: rgba(148, 163, 184, 0.16);
  --line-hi: rgba(45, 212, 191, 0.45);
  --fg: #f1f5f9;
  --muted: #94a3b8;
  --dim: #64748b;
  --cyan: #2dd4bf;
  --sky: #38bdf8;
  --indigo: #818cf8;
  --ok: #34d399;
  --warn: #fbbf24;
  --rose: #fb7185;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font: 15.5px/1.6 "Inter", "Segoe UI", system-ui, -apple-system, sans-serif;
  overflow-x: hidden;
}
a { color: var(--sky); text-decoration: none; transition: color 0.15s ease; }
a:hover { color: var(--cyan); }

/* Ambient Aurora Background */
.aurora-bg {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background:
    radial-gradient(900px 420px at 15% -5%, rgba(45, 212, 191, 0.12), transparent 65%),
    radial-gradient(850px 460px at 88% 8%, rgba(56, 189, 248, 0.12), transparent 65%),
    radial-gradient(700px 400px at 50% 95%, rgba(129, 140, 248, 0.08), transparent 65%);
}

/* Top Announcement Bar */
.announce-bar {
  position: relative;
  z-index: 20;
  background: linear-gradient(90deg, rgba(15, 22, 38, 0.95), rgba(20, 30, 51, 0.95));
  border-bottom: 1px solid var(--line);
  padding: 8px 20px;
  text-align: center;
  font-size: 12.5px;
  color: var(--muted);
  letter-spacing: 0.03em;
}
.announce-bar b { color: var(--cyan); font-weight: 600; }
.announce-bar a { color: var(--fg); text-decoration: underline; text-underline-offset: 3px; margin-left: 8px; font-weight: 600; }

/* Sticky Glassmorphic Header */
.site-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  background: rgba(5, 7, 13, 0.82);
  border-bottom: 1px solid var(--line);
}
.site-nav-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.brand-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  font-size: 18px;
  color: var(--fg);
  letter-spacing: -0.02em;
}
.brand-logo .dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--cyan);
  box-shadow: 0 0 12px var(--cyan);
}
.brand-logo span { color: var(--cyan); font-weight: 600; font-size: 13px; padding: 2px 8px; border-radius: 999px; background: rgba(45, 212, 191, 0.12); border: 1px solid rgba(45, 212, 191, 0.3); }
.nav-links {
  display: flex;
  align-items: center;
  gap: 18px;
  flex-wrap: wrap;
  font-size: 13.5px;
}
.nav-links a { color: var(--muted); font-weight: 500; }
.nav-links a:hover { color: var(--fg); }
.nav-links a.cta-pill {
  color: #041019;
  background: linear-gradient(135deg, var(--cyan), var(--sky));
  padding: 7px 15px;
  border-radius: 999px;
  font-weight: 700;
}

.wrap {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

/* Scrolltide Hero */
.hero-sec {
  text-align: center;
  padding: 28px 0 36px;
  max-width: 940px;
  margin: 0 auto;
}
.eyebrow-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  border-radius: 999px;
  background: rgba(45, 212, 191, 0.1);
  border: 1px solid rgba(45, 212, 191, 0.32);
  color: var(--cyan);
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 18px;
}
h1 {
  font-size: clamp(2.2rem, 4.8vw, 3.8rem);
  line-height: 1.08;
  letter-spacing: -0.03em;
  margin: 0 0 18px;
  font-weight: 800;
}
h1 .grad {
  background: linear-gradient(95deg, #2dd4bf 0%, #38bdf8 52%, #818cf8 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.lede {
  color: var(--muted);
  font-size: clamp(1rem, 1.8vw, 1.18rem);
  max-width: 760px;
  margin: 0 auto 26px;
}
.hero-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 28px;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 11px 20px;
  border-radius: 10px;
  border: 1px solid var(--line);
  background: var(--panel);
  color: var(--fg);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.18s ease;
}
.btn:hover {
  border-color: var(--cyan);
  transform: translateY(-1px);
  color: var(--fg);
}
.btn.primary {
  background: linear-gradient(135deg, var(--cyan), var(--sky));
  color: #041019;
  border-color: transparent;
  font-weight: 700;
}
.btn.primary:hover {
  filter: brightness(1.08);
  color: #041019;
}

/* Proof Stat Strip */
.proof-strip {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px;
  margin: 24px 0 42px;
}
.proof-box {
  background: rgba(15, 22, 38, 0.78);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 16px;
  text-align: left;
}
.proof-box b {
  display: block;
  font-size: 20px;
  color: var(--cyan);
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
}
.proof-box span {
  font-size: 12.5px;
  color: var(--muted);
}

/* NotebookLM Video Overview Studio Section */
.nlm-section {
  background: linear-gradient(180deg, rgba(15, 22, 38, 0.92), rgba(11, 16, 28, 0.96));
  border: 1px solid rgba(45, 212, 191, 0.35);
  border-radius: 20px;
  padding: 28px;
  margin-bottom: 48px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.55);
}
.nlm-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}
.nlm-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 5px 12px;
  border-radius: 999px;
  background: rgba(45, 212, 191, 0.14);
  border: 1px solid rgba(45, 212, 191, 0.4);
  color: var(--cyan);
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.nlm-grid {
  display: grid;
  grid-template-columns: 1.55fr 1fr;
  gap: 22px;
  align-items: stretch;
}
.video-frame {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #070a11;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid var(--line);
}
.video-frame video, .video-frame img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  background: #070a11;
}
.nlm-chapters {
  display: flex;
  flex-direction: column;
  gap: 10px;
  justify-content: space-between;
}
.nlm-chap {
  background: rgba(9, 13, 22, 0.85);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 12px 14px;
  cursor: pointer;
  text-align: left;
  color: var(--fg);
  transition: border-color 0.15s, background 0.15s;
}
.nlm-chap:hover {
  border-color: var(--cyan);
  background: rgba(20, 30, 51, 0.9);
}
.nlm-chap .ch-top {
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
  font-family: ui-monospace, Consolas, monospace;
  color: var(--cyan);
  margin-bottom: 4px;
}
.nlm-chap b { display: block; font-size: 14px; margin-bottom: 2px; }
.nlm-chap span { font-size: 12.5px; color: var(--muted); }

/* Filter Bar */
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  margin: 36px 0 22px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--line);
}
.filter-tabs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.ftab {
  background: var(--panel);
  border: 1px solid var(--line);
  color: var(--muted);
  padding: 7px 14px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.ftab:hover, .ftab.active {
  background: var(--cyan);
  color: #041019;
  border-color: var(--cyan);
}
.search-box {
  background: var(--panel);
  border: 1px solid var(--line);
  color: var(--fg);
  padding: 8px 14px;
  border-radius: 10px;
  font-size: 13.5px;
  min-width: 240px;
}

/* Scrolltide Showcase Cards (.grid and .card required by verify.py) */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(370px, 1fr));
  gap: 22px;
}
.card {
  display: flex;
  flex-direction: column;
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
  color: var(--fg);
  text-decoration: none;
  transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
  border-color: var(--line-hi);
  transform: translateY(-3px);
  box-shadow: 0 18px 44px rgba(0, 0, 0, 0.55);
  color: var(--fg);
}
.card-media {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #070a11;
  border-bottom: 1px solid var(--line);
  overflow: hidden;
}
.card-media video, .card-media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
  background: #070a11;
}
.card-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(5, 7, 13, 0.86);
  border: 1px solid rgba(45, 212, 191, 0.4);
  color: var(--cyan);
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 999px;
  backdrop-filter: blur(8px);
}
.card-play-hint {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: rgba(5, 7, 13, 0.85);
  border: 1px solid var(--line);
  color: var(--fg);
  font-size: 11px;
  font-family: ui-monospace, Consolas, monospace;
  padding: 3px 8px;
  border-radius: 6px;
}
.card-body {
  padding: 18px 20px 20px;
  display: flex;
  flex-direction: column;
  flex: 1;
}
.card h2 {
  font-size: 1.18rem;
  margin: 0 0 6px;
  color: var(--fg);
}
.card p {
  margin: 0 0 14px;
  color: var(--muted);
  font-size: 0.92rem;
}

/* Concrete Input -> Output Box inside every card */
.io-box {
  background: rgba(7, 10, 17, 0.85);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 10px 12px;
  margin-bottom: 12px;
  font-size: 12.5px;
}
.io-row {
  display: flex;
  gap: 8px;
  margin: 4px 0;
  align-items: baseline;
}
.io-tag {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 10.5px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  flex-shrink: 0;
}
.io-tag.in { background: rgba(251, 113, 133, 0.16); color: #fda4af; border: 1px solid rgba(251, 113, 133, 0.35); }
.io-tag.out { background: rgba(52, 211, 153, 0.16); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.35); }
.io-text { color: #cbd5e1; line-height: 1.4; }
.io-code {
  margin-top: 6px;
  padding-top: 6px;
  border-top: 1px dashed rgba(148, 163, 184, 0.18);
  font-family: ui-monospace, Consolas, monospace;
  font-size: 11px;
  color: var(--cyan);
  overflow-x: auto;
  white-space: nowrap;
}

.card .caveat {
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid var(--line);
  color: var(--dim);
  font-size: 0.8rem;
}
.card-foot {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  font-weight: 700;
  color: var(--cyan);
}

/* Detail Page Styles (/apps/<slug>/) */
.detail-grid {
  display: grid;
  grid-template-columns: 1.45fr 1fr;
  gap: 26px;
  margin: 24px 0 32px;
}
.panel-box {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 22px;
  margin-bottom: 20px;
}
.panel-box h2 {
  margin: 0 0 12px;
  font-size: 1.15rem;
  color: var(--fg);
}
.step-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin: 20px 0;
}
.step-card {
  background: rgba(9, 13, 22, 0.9);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 16px;
}
.step-card h3 {
  margin: 0 0 8px;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--cyan);
  font-family: ui-monospace, Consolas, monospace;
}
.caveat-box {
  border-left: 3px solid var(--warn);
  padding: 14px 18px;
  background: rgba(251, 191, 36, 0.07);
  border-radius: 0 12px 12px 0;
  margin: 20px 0;
}
.links { display: flex; gap: 12px; flex-wrap: wrap; margin: 20px 0; }
.links a {
  padding: 10px 16px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--panel);
  color: var(--fg);
  font-weight: 600;
}
.links a.primary {
  background: linear-gradient(135deg, var(--cyan), var(--sky));
  color: #041019;
  border-color: transparent;
  font-weight: 700;
}
footer {
  margin-top: 56px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.88rem;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}
@media (max-width: 920px) {
  .nlm-grid, .detail-grid, .step-cards { grid-template-columns: 1fr; }
  .grid { grid-template-columns: 1fr; }
}
"""


def render_home() -> str:
    cards = []
    for a in APPS:
        slug = a["slug"]
        tid = a["tid"]
        name = html.escape(a["name"])
        summary = html.escape(a["summary"])
        caveat = html.escape(a["caveat"])
        cat = html.escape(a["cat"])
        cat_label = html.escape(a["cat_label"])
        in_ex = html.escape(a["input_ex"])
        out_ex = html.escape(a["output_ex"])
        scode = html.escape(a["sample_code"])
        cards.append(
            f'      <a class="card" href="/apps/{slug}/" data-cat="{cat}" data-search="{name.lower()} {summary.lower()} {cat_label.lower()}">\n'
            f'        <div class="card-media">\n'
            f'          <video src="/tools/videos/{tid}.mp4" poster="/tools/shots/{tid}.jpg" muted loop playsinline preload="none" data-aspect="horizontal"></video>\n'
            f'          <span class="card-badge">{cat_label}</span>\n'
            f'          <span class="card-play-hint">▶ 16:9 Demo &amp; Output</span>\n'
            f'        </div>\n'
            f'        <div class="card-body">\n'
            f'          <h2>{name}</h2>\n'
            f'          <p>{summary}</p>\n'
            f'          <div class="io-box">\n'
            f'            <div class="io-row"><span class="io-tag in">INPUT</span><span class="io-text">{in_ex}</span></div>\n'
            f'            <div class="io-row"><span class="io-tag out">OUTPUT</span><span class="io-text">{out_ex}</span></div>\n'
            f'            <div class="io-code">{scode}</div>\n'
            f'          </div>\n'
            f'          <div class="caveat">Caveat: {caveat}</div>\n'
            f'          <div class="card-foot"><span>Watch video walkthrough &amp; examples</span><span>→</span></div>\n'
            f'        </div>\n'
            f'      </a>'
        )
    cards_html = "\n".join(cards)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NavigatorLabs Product library</title>
  <meta name="description" content="NavigatorLabs open-source product library: 16 apps across browser tools, PDF editing, HTML redesign, MCP servers, and developer utilities — with interactive video demos and concrete input-to-output examples.">
  <link rel="stylesheet" href="/apps/style.css">
</head>
<body>
  <div class="aurora-bg"></div>
  <div class="announce-bar">
    <b>✦ LOCAL-FIRST SOFTWARE STUDIO</b> · 16 Repositories · 24 Browser &amp; Agent Tools · Concrete Input → Output Video Proofs
    <a href="https://navigatorslab.com/tools/">Explore all 24 browser tools →</a>
  </div>
  <header class="site-nav">
    <div class="site-nav-inner">
      <a class="brand-logo" href="/"><span class="dot"></span> NavigatorLabs <span>LOCAL-FIRST</span></a>
      <nav class="nav-links" aria-label="Primary Navigation">
        <a href="#overview">🎙️ NotebookLM Video Overview</a>
        <a href="#catalog">16-App Library</a>
        <a href="https://navigatorslab.com/pdf-studio/">PDF Studio</a>
        <a href="https://navigatorslab.com/tools/">24 Browser Tools</a>
        <a href="https://navigatorslab.com/reimagine/">Reimagine</a>
        <a href="https://github.com/Kayforkind">GitHub</a>
        <a class="cta-pill" href="https://navigatorslab.com/tools/">Launch Tools Suite →</a>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <section class="hero-sec">
      <div class="eyebrow-pill">NavigatorLabs Product library · 16 apps &amp; 24 local-first tools</div>
      <h1>Software that stays on your machine.<br><span class="grad">With real examples, video demos &amp; verified outputs.</span></h1>
      <p class="lede">
        Every tool in the NavigatorLabs library processes your files locally in your browser tab or local CLI — backed by automated browser E2E checks, concrete input-to-output examples, and zero server uploads.
      </p>
      <div class="hero-actions">
        <a class="btn primary" href="#overview">▶ Watch NotebookLM Deep Dive</a>
        <a class="btn" href="https://navigatorslab.com/tools/">🧭 Open 24 Browser Tools</a>
        <a class="btn" href="https://navigatorslab.com/pdf-studio/">📜 Launch PDF Studio</a>
        <a class="btn" href="https://navigatorslab.com/reimagine/">🎨 Launch Reimagine</a>
      </div>

      <div class="proof-strip">
        <div class="proof-box"><b>16 apps</b><span>Dedicated repositories with video demos, examples &amp; caveats</span></div>
        <div class="proof-box"><b>24 tools</b><span>In-browser utilities, flagships, MCP servers &amp; CI gates</span></div>
        <div class="proof-box"><b>0 uploads</b><span>Enforced by Content-Security-Policy default-src 'none'</span></div>
        <div class="proof-box"><b>39 / 39 E2E</b><span>Real browser Playwright assertions on every output file</span></div>
      </div>
    </section>

    <section id="overview" class="nlm-section" aria-label="NotebookLM Audio and Video Overview">
      <div class="nlm-header">
        <div>
          <span class="nlm-badge">🎙️ NotebookLM Deep-Dive Video Overview</span>
          <h2 style="margin:8px 0 4px;font-size:1.5rem">How Every NavigatorLabs Tool Works — Input to Output</h2>
          <p style="margin:0;color:var(--muted);font-size:0.95rem">Two-host walkthrough covering the local-first CSP architecture, PDF Studio, Reimagine, the 16 browser utilities, and the AI Agent MCP suite.</p>
        </div>
        <a class="btn" href="/tools/videos/notebooklm-overview.mp4" download>⬇ Download MP4 Overview</a>
      </div>
      <div class="nlm-grid">
        <div class="video-frame">
          <video id="nlmVideo" controls playsinline preload="metadata" poster="/tools/shots/notebooklm-overview.jpg" data-aspect="horizontal">
            <source src="/tools/videos/notebooklm-overview.mp4" type="video/mp4">
          </video>
        </div>
        <div class="nlm-chapters">
          <button type="button" class="nlm-chap" data-seek="0">
            <div class="ch-top"><span>CHAPTER 01</span><span>00:00</span></div>
            <b>The Local-First Security Thesis</b>
            <span>Why CSP default-src 'none' beats privacy policies &amp; how 5-char HIBP k-anonymity works.</span>
          </button>
          <button type="button" class="nlm-chap" data-seek="31">
            <div class="ch-top"><span>CHAPTER 02</span><span>00:31</span></div>
            <b>Flagship Suites: PDF Studio &amp; Reimagine</b>
            <span>In-place PDF content stream editing, Tesseract WASM OCR, and 17-direction HTML redesign.</span>
          </button>
          <button type="button" class="nlm-chap" data-seek="64">
            <div class="ch-top"><span>CHAPTER 03</span><span>01:04</span></div>
            <b>Concrete Input → Output Walkthroughs</b>
            <span>Byte-identical EXIF stripping, 16 MB → 294 KB binary search, Receipt OCR to CSV &amp; E-Sign.</span>
          </button>
          <button type="button" class="nlm-chap" data-seek="98">
            <div class="ch-top"><span>CHAPTER 04</span><span>01:38</span></div>
            <b>AI Agents, MCP Server &amp; liecatchers</b>
            <span>Stateless /tools/mcp endpoint, Skill Slice verified folders, and 10-sensor RECEIPT.json proofs.</span>
          </button>
        </div>
      </div>
    </section>

    <section id="catalog" aria-label="Applications Catalog">
      <div class="filter-bar">
        <div class="filter-tabs" role="tablist">
          <button type="button" class="ftab active" data-filter="all">All 16 Apps</button>
          <button type="button" class="ftab" data-filter="flagship">Flagship Apps</button>
          <button type="button" class="ftab" data-filter="privacy">Privacy &amp; Security</button>
          <button type="button" class="ftab" data-filter="documents">PDF &amp; Documents</button>
          <button type="button" class="ftab" data-filter="money">Money &amp; OCR</button>
          <button type="button" class="ftab" data-filter="images">Images &amp; Print</button>
          <button type="button" class="ftab" data-filter="agents">Agents, MCP &amp; CI</button>
        </div>
        <input type="search" id="appSearch" class="search-box" placeholder="Search 16 apps, inputs or outputs…" aria-label="Search applications">
      </div>

      <div class="grid" id="appGrid">
{cards_html}
      </div>
    </section>

    <footer>
      <span>NavigatorLabs · Open-source, local-first software studio (<a href="https://github.com/Kayforkind">github.com/Kayforkind</a>)</span>
      <span><a href="https://navigatorslab.com/tools/">24 Browser Tools</a> · <a href="https://navigatorslab.com/pdf-studio/">PDF Studio</a> · <a href="https://navigatorslab.com/reimagine/">Reimagine</a> · <a href="https://navigatorslab.com/tools/status.html">Live Verification Status</a></span>
    </footer>
  </main>

  <script>
    (function () {{
      // Hover / focus video preview playback on cards
      document.querySelectorAll('.card').forEach(function (card) {{
        var vid = card.querySelector('video');
        if (!vid) return;
        card.addEventListener('mouseenter', function () {{ vid.play().catch(function(){{}}); }});
        card.addEventListener('mouseleave', function () {{ vid.pause(); }});
        card.addEventListener('focus', function () {{ vid.play().catch(function(){{}}); }});
        card.addEventListener('blur', function () {{ vid.pause(); }});
      }});
      // Chapter jump buttons for NotebookLM video
      var nlm = document.getElementById('nlmVideo');
      document.querySelectorAll('.nlm-chap').forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          if (!nlm) return;
          nlm.currentTime = Number(btn.getAttribute('data-seek') || 0);
          nlm.play().catch(function(){{}});
        }});
      }});
      // Category filter + search
      var tabs = document.querySelectorAll('.ftab');
      var search = document.getElementById('appSearch');
      var cards = document.querySelectorAll('#appGrid .card');
      var activeCat = 'all';
      function applyFilter() {{
        var q = (search ? search.value : '').toLowerCase().trim();
        cards.forEach(function (c) {{
          var catMatch = (activeCat === 'all') || (c.getAttribute('data-cat') === activeCat);
          var qMatch = !q || (c.getAttribute('data-search') || '').indexOf(q) !== -1;
          c.style.display = (catMatch && qMatch) ? '' : 'none';
        }});
      }}
      tabs.forEach(function (t) {{
        t.addEventListener('click', function () {{
          tabs.forEach(function (x) {{ x.classList.remove('active'); }});
          t.classList.add('active');
          activeCat = t.getAttribute('data-filter') || 'all';
          applyFilter();
        }});
      }});
      if (search) search.addEventListener('input', applyFilter);
    }})();
  </script>
</body>
</html>
"""


def render_detail(a: dict[str, str]) -> str:
    name = html.escape(a["name"])
    summary = html.escape(a["summary"])
    how = html.escape(a["how_to_use"])
    caveat = html.escape(a["caveat"])
    tid = a["tid"]
    cat_label = html.escape(a["cat_label"])
    in_ex = html.escape(a["input_ex"])
    eng_ex = html.escape(a.get("engine_ex", a.get("engine_step", "Local execution engine")))
    out_ex = html.escape(a["output_ex"])
    scode = html.escape(a["sample_code"])
    repo_url = f"https://github.com/Kayforkind/{a['repo']}"
    live_btn = (
        f'<a class="primary" href="{html.escape(a["live"])}">Launch Live App →</a>'
        if a["live"]
        else ""
    )

    other_links = []
    for o in APPS:
        if o["slug"] != a["slug"]:
            other_links.append(f'<a class="btn" style="padding:6px 12px;font-size:12.5px" href="/apps/{o["slug"]}/">{html.escape(o["name"])}</a>')
    others_html = "\n        ".join(other_links)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{name} — NavigatorLabs</title>
  <meta name="description" content="{summary}">
  <link rel="stylesheet" href="/apps/style.css">
</head>
<body>
  <div class="aurora-bg"></div>
  <header class="site-nav">
    <div class="site-nav-inner">
      <a class="brand-logo" href="/"><span class="dot"></span> NavigatorLabs <span>PRODUCT DETAIL</span></a>
      <nav class="nav-links">
        <a href="/">← All 16 apps</a>
        <a href="/#overview">🎙️ NotebookLM Overview</a>
        <a href="https://navigatorslab.com/tools/">24 Browser Tools</a>
        <a href="{repo_url}">GitHub Repo</a>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <div class="eyebrow-pill">{cat_label} · Verified Local-First</div>
    <h1>{name}</h1>
    <p class="lede" style="margin:0 0 20px;text-align:left;max-width:880px">{summary}</p>

    <div class="links">
      {live_btn}
      <a href="{repo_url}">Source repository ({html.escape(a['repo'])})</a>
      <a href="/tools/detail.html?id={tid}">Interactive Tool Spec &amp; Deep-Links</a>
    </div>

    <div class="detail-grid">
      <div>
        <div class="panel-box" style="padding:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding:0 6px">
            <b style="font-size:13px;color:var(--cyan);font-family:ui-monospace,Consolas,monospace">▶ LIVE WORKFLOW DEMO VIDEO (16:9)</b>
            <span style="font-size:12px;color:var(--muted)">Input → On-Device Engine → Verified Output</span>
          </div>
          <div class="video-frame">
            <video controls autoplay muted loop playsinline preload="metadata" poster="/tools/shots/{tid}.jpg" data-aspect="horizontal">
              <source src="/tools/videos/{tid}.mp4" type="video/mp4">
            </video>
          </div>
        </div>

        <div class="panel-box" style="padding:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding:0 6px">
            <b style="font-size:13px;color:var(--sky);font-family:ui-monospace,Consolas,monospace">📸 HIGH-RESOLUTION OUTPUT &amp; UI PREVIEW</b>
            <a href="/tools/shots/{tid}.jpg" target="_blank" style="font-size:12px">Open full image ↗</a>
          </div>
          <div class="video-frame">
            <img src="/tools/shots/{tid}.jpg" alt="{name} screenshot and output breakdown" loading="lazy">
          </div>
        </div>
      </div>

      <div>
        <div class="panel-box">
          <h2>Concrete Example: Input → Output</h2>
          <div class="step-cards" style="grid-template-columns:1fr;gap:12px;margin:12px 0">
            <div class="step-card">
              <h3>1 · Raw Input</h3>
              <p style="margin:0;color:var(--fg);font-size:14px">{in_ex}</p>
            </div>
            <div class="step-card">
              <h3>2 · On-Device Engine</h3>
              <p style="margin:0;color:var(--fg);font-size:14px">{eng_ex}</p>
            </div>
            <div class="step-card">
              <h3>3 · Verified Output Artifact</h3>
              <p style="margin:0;color:#6ee7b7;font-size:14px">{out_ex}</p>
            </div>
          </div>
          <div style="background:#070a11;border:1px solid var(--line);border-radius:10px;padding:12px;font-family:ui-monospace,Consolas,monospace;font-size:12px;color:var(--cyan);overflow-x:auto">
            {scode}
          </div>
        </div>

        <div class="panel-box">
          <h2>How to use it</h2>
          <p style="margin:0;color:var(--muted)">{how}</p>
        </div>

        <div class="caveat-box">
          <h2>Important caveat</h2>
          <p style="margin:0;color:var(--fg)">{caveat}</p>
        </div>
      </div>
    </div>

    <div class="panel-box">
      <h2>Explore all 16 NavigatorLabs apps</h2>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:12px">
        {others_html}
      </div>
    </div>

    <footer>
      <a href="/">← Back to all 16 apps</a>
      <a href="{repo_url}">{repo_url}</a>
    </footer>
  </main>
</body>
</html>
"""


# Build inline Worker script that serves the generated pages directly
HEADERS_HTML = {
    "content-type": "text/html; charset=utf-8",
    "cache-control": "public, max-age=60, must-revalidate",
    "x-content-type-options": "nosniff",
    "x-frame-options": "DENY",
    "referrer-policy": "strict-origin-when-cross-origin",
    "content-security-policy": (
        "default-src 'none'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: blob:; "
        "media-src 'self' data: blob:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'none'"
    ),
    "x-served-by": "navigatorslab-home",
}
HEADERS_CSS = {
    "content-type": "text/css; charset=utf-8",
    "cache-control": "public, max-age=300, must-revalidate",
    "x-content-type-options": "nosniff",
    "x-served-by": "navigatorslab-home",
}


def main() -> None:
    if OUT.exists():
        for p in sorted(OUT.rglob("*"), reverse=True):
            if p.is_file():
                p.unlink()
            elif p.is_dir():
                p.rmdir()
    (OUT / "apps").mkdir(parents=True, exist_ok=True)

    home_html = render_home()
    (OUT / "index.html").write_text(home_html, encoding="utf-8")
    (OUT / "apps" / "style.css").write_text(CSS, encoding="utf-8")

    # Also keep repo-root index.html in sync so GitHub Pages / check-links.cjs sees the upgraded page

    routes: dict[str, str] = {
        "/": home_html,
        "/index.html": home_html,
    }
    for a in APPS:
        d = OUT / "apps" / a["slug"]
        d.mkdir(parents=True, exist_ok=True)
        html_doc = render_detail(a)
        (d / "index.html").write_text(html_doc, encoding="utf-8")
        # Also write to repo-root /apps/<slug>/index.html for check-links.cjs
        routes[f"/apps/{a['slug']}"] = html_doc
        routes[f"/apps/{a['slug']}/"] = html_doc
        routes[f"/apps/{a['slug']}/index.html"] = html_doc

    sw_kill = (
        "self.addEventListener('install',function(e){self.skipWaiting()});"
        "self.addEventListener('activate',function(e){e.waitUntil((async function(){"
        "try{var k=await caches.keys();await Promise.all(k.map(function(x){return caches.delete(x)}))}catch(e){}"
        "try{await self.registration.unregister()}catch(e){}"
        "try{var cs=await self.clients.matchAll({includeUncontrolled:true});"
        "for(var i=0;i<cs.length;i++){try{cs[i].navigate(cs[i].url)}catch(e){}}}catch(e){}"
        "})())});"
    )
    headers_sw = {
        "content-type": "text/javascript; charset=utf-8",
        "x-served-by": "navigatorslab-home",
        "cache-control": "no-store",
    }

    worker_js = (
        "// Generated by build_site.py — do not edit by hand.\n"
        'addEventListener("fetch", function (event) { event.respondWith(handle(event.request)); });\n'
        f"const ROUTES = {json.dumps(routes, ensure_ascii=False)};\n"
        f"const CSS = {json.dumps(CSS, ensure_ascii=False)};\n"
        f"const SW_KILL = {json.dumps(sw_kill)};\n"
        f"const H_HTML = {json.dumps(HEADERS_HTML)};\n"
        f"const H_CSS = {json.dumps(HEADERS_CSS)};\n"
        f"const H_SW = {json.dumps(headers_sw)};\n"
        """function handle(request) {
  const url = new URL(request.url);
  const p = url.pathname;
  if (p === "/apps/__diag__") {
    const hd = {};
    request.headers.forEach(function (v, k) { hd[k] = v; });
    return new Response(JSON.stringify({
      worker: "navigatorslab-home",
      products: 16,
      url: url.toString(),
      host: url.host,
      ray: hd["cf-ray"] || null
    }), {
      status: 200,
      headers: { "content-type": "application/json", "x-served-by": "navigatorslab-home", "cache-control": "no-store" }
    });
  }
  if (p === "/apps/style.css") {
    return new Response(CSS, { status: 200, headers: H_CSS });
  }
  if (p === "/sw.js") {
    return new Response(SW_KILL, { status: 200, headers: H_SW });
  }
  if (p === "/apps" || p === "/apps/" || p === "/apps/index.html") {
    return Response.redirect(url.origin + "/", 302);
  }
  if (Object.prototype.hasOwnProperty.call(ROUTES, p)) {
    if (p.startsWith("/apps/") && !p.endsWith("/") && !p.endsWith(".html")) {
      return Response.redirect(url.origin + p + "/", 301);
    }
    return new Response(ROUTES[p], { status: 200, headers: H_HTML });
  }
  return new Response("Not found", { status: 404, headers: H_HTML });
}
"""
    )
    (HERE / "worker.js").write_text(worker_js, encoding="utf-8")
    (HERE / "dist").mkdir(parents=True, exist_ok=True)
    (HERE / "dist" / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"Built {len(APPS)} app pages + home into {OUT} and dist/worker.js ({len(worker_js):,} bytes)")


if __name__ == "__main__":
    main()
