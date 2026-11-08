"""Build static HTML for navigatorslab.com + /apps/<slug>/ into worker-home/public/.

Includes:
- Narrated Live-UI Step-by-Step Usage Tutorial Videos (/tools/videos/<tid>.mp4) with spoken voiceover
- Master Hands-On Usage Guide Video (/tools/videos/notebooklm-overview.mp4) with 9 interactive tool chapters
- Comprehensive 4-Step User Manuals, UI Controls Reference & Pro Tips on every /apps/<slug>/ page
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

GUIDE_DATA: dict[str, dict] = {
  "exif": {
    "videoDuration": "43s",
    "guideSteps": [
      {
        "title": "Step 1: Load Your Photo (Drag & Drop or Ctrl+V)",
        "ui": "Dropzone (#dz) or Clipboard Paste",
        "narration": "To use Photo Privacy Kit, open exif.html and drag any JPEG, PNG, or WebP photo onto the dropzone, or press Control V to paste a screenshot.",
        "guide": "Open Photo Privacy Kit and drag one or more JPEG, PNG, or WebP images onto the main dropzone (`#dz`), click to browse your device, or press `Ctrl+V` (`Cmd+V` on Mac) to paste directly from your clipboard.",
        "result": "The file loads immediately into browser memory with zero network activity."
      },
      {
        "title": "Step 2: Inspect the Live Metadata & GPS Leak Report",
        "ui": "Leak Report Table (#list)",
        "narration": "Second, review the automatic inspection report. Any embedded GPS coordinates, camera serial numbers, timestamps, and hidden preview thumbnails are flagged in red.",
        "guide": "Read the per-file inspection row under `#list`. Red warning badges highlight high-risk leaks such as exact GPS latitude/longitude coordinates, device make/model, capture timestamps, and embedded EXIF thumbnails.",
        "result": "Every detected EXIF, XMP, IPTC, and comment segment is listed byte-by-byte."
      },
      {
        "title": "Step 3: Strip Metadata & Toggle SHA-256 Pixel Proof",
        "ui": "Strip Button (#strip) & SHA-256 Toggle",
        "narration": "Third, click Show SHA-256 Fingerprints if you want cryptographic pixel verification, then click Strip Metadata and Download All.",
        "guide": "Optionally toggle **Show SHA-256 fingerprints** to display the decoded RGBA pixel hash before and after cleaning. Click **Strip metadata & download all (`#strip`)** (or **Download as .zip** for batches).",
        "result": "The segment parser strips APP1/APP13/XMP/COM markers without re-encoding your pixels."
      },
      {
        "title": "Step 4: Verify GPS CLEAR & Save Cleaned Image",
        "ui": "Verified Output Row (GPS CLEAR)",
        "narration": "Finally, confirm the green GPS Clear badge and matching pixel SHA-256 hash. Your cleaned photo downloads directly to your device with zero quality loss.",
        "guide": "Verify that the status badge turns green (**GPS CLEAR — 0 metadata segments**) and that the before/after decoded pixel SHA-256 hashes match 100%.",
        "result": "Cleaned `.clean.jpg` / `.png` / `.webp` saved locally with zero generation loss."
      }
    ],
    "guideControls": [
      {
        "name": "Dropzone (`#dz`) / `Ctrl+V`",
        "desc": "Accepts single or batch `.jpg`, `.jpeg`, `.png`, and `.webp` files via drag-and-drop, file picker, or clipboard paste."
      },
      {
        "name": "Strip metadata & download all (`#strip`)",
        "desc": "Removes EXIF, GPS, XMP, IPTC, and comment segments from every loaded file and downloads cleaned copies."
      },
      {
        "name": "Download as .zip (`#zip`)",
        "desc": "Bundles all cleaned images into a single local `.zip` archive when processing multiple photos."
      },
      {
        "name": "Show SHA-256 fingerprints (`#shaToggle`)",
        "desc": "Computes the SHA-256 digest of the decoded pixel buffer before and after stripping to prove zero pixel alteration."
      }
    ],
    "guideProTips": [
      "Press `Ctrl+V` right after taking a system screenshot to strip OS color-profile and timestamp chunks before sharing on Slack, Discord, or GitHub issues.",
      "Because Photo Privacy Kit strips container markers at the byte level without re-compressing JPEG blocks, your photo never suffers JPEG generation loss.",
      "Drop a cleaned `.clean.jpg` file back into the dropzone at any time to confirm it reports `0 metadata segments`."
    ],
    "guideSpecs": "Formats: JPEG, PNG, WebP · Processing: 100% Client-Side Byte Parser · Network: `connect-src 'none'` (0 uploads)"
  },
  "breachcheck": {
    "videoDuration": "38s",
    "guideSteps": [
      {
        "title": "Step 1: Type a Password to Test (Zero Keystrokes Sent)",
        "ui": "Password Input (#pwInput)",
        "narration": "To check if a password has appeared in known data breaches without ever transmitting your password, open breachcheck.html and type the password into the input box.",
        "guide": "Type or paste the password you want to audit into `#pwInput`. Nothing leaves your browser while you type.",
        "result": "Local entropy and offline crack-time estimates update in your tab."
      },
      {
        "title": "Step 2: Click Check Breach Database to Hash Locally via WebCrypto",
        "ui": "Check Button (#btnCheck)",
        "narration": "Second, click Check Breach Database. Your browser computes the SHA-1 hash locally using WebCrypto and sends only the first five hex characters to Have I Been Pwned.",
        "guide": "Click **Check (`#btnCheck`)**. The browser computes the 40-character uppercase SHA-1 digest via `crypto.subtle.digest('SHA-1')` and requests `https://api.pwnedpasswords.com/range/<5-CHAR-PREFIX>`.",
        "result": "The remaining 35 characters of your password hash never leave your device."
      },
      {
        "title": "Step 3: Read the Breach Exposure Count & Crack-Time Verdict",
        "ui": "Verdict Banner (#verdict)",
        "narration": "Third, read the verdict banner. The browser compares the returned hash suffixes locally in your tab and reports the exact number of breaches found.",
        "guide": "Read `#verdict` to see whether your password matched any of the ~500 suffixes in that k-anonymity bucket, along with the total breach occurrence count.",
        "result": "Immediate red alert if breached, or green confirmation if 0 matches found."
      },
      {
        "title": "Step 4: Verify the 5-Character k-Anonymity Network Proof",
        "ui": "k-Anonymity Proof Box (#hashProof)",
        "narration": "Finally, inspect the Hash Proof box below to see the exact five-character prefix that was sent versus the thirty-five-character suffix kept private on your machine.",
        "guide": "Inspect `#hashProof`, which splits your SHA-1 hash visually into the **5-char prefix sent over HTTPS** and the **35-char suffix checked locally**.",
        "result": "Mathematical k-anonymity verification you can confirm in Browser DevTools Network tab."
      }
    ],
    "guideControls": [
      {
        "name": "Password Input (`#pwInput`)",
        "desc": "Local password field (never transmitted; zero network requests until you click Check)."
      },
      {
        "name": "Check Button (`#btnCheck`)",
        "desc": "Triggers local WebCrypto SHA-1 hashing and the 5-char HIBP range query."
      },
      {
        "name": "Verdict Banner (`#verdict`)",
        "desc": "Displays exact breach exposure count and local entropy crack-time estimate."
      },
      {
        "name": "Hash Proof (`#hashProof`)",
        "desc": "Displays the 5-char SHA-1 prefix vs. 35-char private suffix."
      }
    ],
    "guideProTips": [
      "Open Browser DevTools (`F12` → **Network** tab) while clicking Check: you will see a single `GET https://api.pwnedpasswords.com/range/XXXXX` request containing only 5 hex characters.",
      "Even if a password reports `Not found in breaches`, check the local entropy readout—short dictionary words with numbers are still vulnerable to offline GPU cracking.",
      "Use a unique 16+ character passphrase or password-manager-generated string for every critical account."
    ],
    "guideSpecs": "Protocol: HIBP k-Anonymity Range API (`5-char SHA-1 prefix`) · Crypto: Native `SubtleCrypto` (`SHA-1`) + Local Entropy Scorer"
  },
  "metadata": {
    "videoDuration": "41s",
    "guideSteps": [
      {
        "title": "Step 1: Drop Documents or Images Into the Inspector",
        "ui": "Universal Dropzone (#dz)",
        "narration": "To inspect and clean hidden document data, open metadata.html and drop any PDF, Word DOCX, Excel XLSX, PowerPoint, OpenDocument, or image file onto the dropzone.",
        "guide": "Drag and drop any `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.odt`, `.ods`, `.odp`, `.jpg`, `.png`, or `.webp` file onto the inspector dropzone (`#dz`).",
        "result": "The engine parses container dictionaries and ZIP XML streams locally."
      },
      {
        "title": "Step 2: Review Author Names, Company & Revision History",
        "ui": "Metadata Findings Panel (#list)",
        "narration": "Second, examine the extracted metadata table. You will see hidden author names, company fields, revision counts, total editing minutes, software versions, and GPS tags.",
        "guide": "Review each file card in `#list`. The inspector surfaces PDF `/Info` and `/Metadata` XMP keys, Office `docProps/core.xml` and `app.xml` fields (Creator, LastModifiedBy, Company, Revision count, TotalTime), and image EXIF tags.",
        "result": "All hidden identity and revision fields are highlighted clearly on screen."
      },
      {
        "title": "Step 3: Click Clean & Download All",
        "ui": "Clean All Button (#stripAll)",
        "narration": "Third, click Clean and Download All to rewrite the document container in your browser, wiping author identities, company tags, and XMP streams.",
        "guide": "Click **Clean & download all (`#stripAll`)** (or the per-file **Clean & download** button) to scrub `/Info` dictionaries, XMP packets, and OOXML/ODF `core.xml`/`app.xml` properties.",
        "result": "A sanitized copy of your PDF, Office document, or image is rebuilt in memory."
      },
      {
        "title": "Step 4: Re-Drop to Verify Zero Hidden Fields",
        "ui": "Cleaned Output Verification",
        "narration": "Finally, save the cleaned file and drop it back into the inspector to verify that Author, Company, and editing time are completely gone.",
        "guide": "Save the exported `.clean.pdf` or `.clean.docx` file and drop it back into `#dz` to confirm all identity and revision fields now read empty.",
        "result": "Document is safe to send to clients, opposing counsel, or public portals."
      }
    ],
    "guideControls": [
      {
        "name": "File Dropzone (`#dz`)",
        "desc": "Accepts PDF, DOCX, XLSX, PPTX, ODT, ODS, ODP, JPEG, PNG, and WebP files."
      },
      {
        "name": "Clean & download all (`#stripAll`)",
        "desc": "Rewrites metadata dictionaries across all loaded files and triggers local download."
      },
      {
        "name": "Per-File Field Table",
        "desc": "Displays exact key/value pairs found inside `/Info`, XMP, `docProps/core.xml`, and `docProps/app.xml`."
      }
    ],
    "guideProTips": [
      "Always run Word (`.docx`) and PDF proposals through Metadata Checker before sending to clients—Word records cumulative editing minutes (`TotalTime`) and previous authors by default.",
      "After cleaning metadata properties, remember to also check visible document body text for comments or tracked changes.",
      "Combine with `share-safe` CLI in CI pipelines if you publish PDFs automatically from a repository."
    ],
    "guideSpecs": "Formats: PDF, DOCX, XLSX, PPTX, ODT/ODS/ODP, JPEG, PNG, WebP · Engine: pdf-lib + OOXML/ODF ZIP rewriter"
  },
  "shrink": {
    "videoDuration": "36s",
    "guideSteps": [
      {
        "title": "Step 1: Drop One or More Large Images",
        "ui": "Batch Dropzone (#dz)",
        "narration": "To compress images to an exact file-size limit, open shrink.html and drop your high-resolution PNG, JPEG, or WebP photos onto the dropzone.",
        "guide": "Drop one or more large images (for example, a 16 MB camera photo or high-DPI scan) onto `#dz`, or click to select a batch from your computer.",
        "result": "Each image's original dimensions and byte size are listed."
      },
      {
        "title": "Step 2: Pick Output Format & Enter Target Kilobyte Cap",
        "ui": "Format (#fmt) & Target Size (#targetKB)",
        "narration": "Second, choose JPEG, WebP, or AVIF from the format menu and type your strict size ceiling into Target KB—for example, 300 kilobytes for a government portal.",
        "guide": "Select your output format (`JPEG`, `WebP`, or `AVIF`) in `#fmt` and type your maximum allowed file size in kilobytes into `#targetKB` (e.g., `300` for a 300 KB portal limit, or `1024` for 1 MB).",
        "result": "Target byte ceiling and encoder format are locked in (also deep-linkable via `?format=webp&targetKB=300`)."
      },
      {
        "title": "Step 3: Click Shrink & Download to Binary-Search Quality",
        "ui": "Shrink Button (#go)",
        "narration": "Third, click Shrink and Download. The browser runs an eight-step binary search over encoder quality and resolution to land right under your cap.",
        "guide": "Click **Shrink & download (`#go`)**. The engine binary-searches Canvas encoder quality (and gently steps down dimensions only if required) until the encoded output lands at or below your target KB.",
        "result": "Highest possible visual quality that fits strictly beneath your byte cap."
      },
      {
        "title": "Step 4: Save Individual Images or a Batch ZIP",
        "ui": "Output List (#list) & ZIP Download",
        "narration": "Finally, review the before and after file sizes in the results list and download your compressed image or batch ZIP.",
        "guide": "Check the percentage reduction and exact final kilobyte count on each row in `#list`, then save individual files or click **Download all as .zip**.",
        "result": "Every output file is guaranteed to pass strict upload size limits on the first try."
      }
    ],
    "guideControls": [
      {
        "name": "Target KB (`#targetKB`)",
        "desc": "Exact maximum file size in kilobytes (e.g., `200`, `300`, `500`, `2000`)."
      },
      {
        "name": "Output Format (`#fmt`)",
        "desc": "Choose `image/jpeg` (universal compatibility), `image/webp` (smaller at same quality), or `image/avif`."
      },
      {
        "name": "Max Dimension Cap (`#maxDim`)",
        "desc": "Optional maximum width/height in pixels before quality binary search begins."
      },
      {
        "name": "URL Deep-Link Params",
        "desc": "Pre-fill settings via `?format=webp&targetKB=300`."
      }
    ],
    "guideProTips": [
      "For visa, passport, and government portals that require JPEG under 240 KB or 300 KB, select `JPEG` and set Target KB to `235` or `295` for a safety margin.",
      "For web publishing and blog hero images, choose `WebP` with a `150` KB target to cut page weight by 85–95% without visible blur.",
      "Batch-drop 20+ product photos at once—Image Shrinker processes them sequentially in your tab and exports one `.zip`."
    ],
    "guideSpecs": "Formats: PNG, JPEG, WebP, AVIF · Algorithm: 8-step binary search over encoder quality + scale fallback"
  },
  "scan": {
    "videoDuration": "33s",
    "guideSteps": [
      {
        "title": "Step 1: Drop Phone Photos of Paper Documents",
        "ui": "Document Dropzone (#dz)",
        "narration": "To turn phone photos of paper into a clean scanned PDF, open scan.html and drop one or more document photos onto the dropzone.",
        "guide": "Drop phone camera photos of contracts, forms, book pages, or whiteboards onto `#dz`. Multiple photos become pages of a multi-page document.",
        "result": "Page thumbnails appear in `#thumbs` and the first page loads into the interactive canvas (`#cv`)."
      },
      {
        "title": "Step 2: Crop Margins & Auto-Deskew Tilted Pages",
        "ui": "Crop Mode (#cropMode) & Canvas (#cv)",
        "narration": "Second, click Crop Mode and drag a rectangle over the document page to trim desk clutter, then click Apply Crop and Auto-Deskew.",
        "guide": "Click **Crop mode (`#cropMode`)**, drag a bounding rectangle across the document on `#cv`, and click **Apply crop (`#applyCropBtn`)**. Use deskew controls to straighten tilted camera angles.",
        "result": "Background desk surfaces and perspective tilt are removed cleanly."
      },
      {
        "title": "Step 3: Apply Grayscale, Auto-Levels & Contrast Boost",
        "ui": "Enhancement Controls (#gray, #contrast, #applyEnh)",
        "narration": "Third, check Grayscale, raise the Contrast slider to remove uneven room shadows, and click Apply Enhancements.",
        "guide": "Check **Grayscale (`#gray`)**, adjust the **Contrast (`#contrast`)** or photocopy threshold slider to bleach gray paper shadows to pure white while sharpening dark ink, and click **Apply (`#applyEnh`)**.",
        "result": "Dim, shadowed phone photos transform into crisp, high-contrast black-and-white scans."
      },
      {
        "title": "Step 4: Export as a Multi-Page 300-DPI PDF or PNG",
        "ui": "Export 300-DPI PDF Button (#pdf)",
        "narration": "Finally, step through any additional pages with Next Page, then click Export 300-DPI PDF to download a print-ready multi-page PDF.",
        "guide": "Use **Next page (`#next`)** to review additional pages, then click **Export 300-DPI PDF (`#pdf`)** (or **Export PNG** for single images).",
        "result": "A clean, properly sized 300-DPI multi-page PDF downloads locally."
      }
    ],
    "guideControls": [
      {
        "name": "Crop Mode (`#cropMode` + `#applyCropBtn`)",
        "desc": "Interactive drag-rectangle crop directly on the live page preview canvas (`#cv`)."
      },
      {
        "name": "Grayscale (`#gray`) & Contrast (`#contrast`)",
        "desc": "Converts color phone photos to crisp monochrome document scans and removes lighting shadows."
      },
      {
        "name": "Apply Enhancements (`#applyEnh`)",
        "desc": "Commits deskew, auto-levels, grayscale, and contrast adjustments to the active page."
      },
      {
        "name": "Export 300-DPI PDF (`#pdf`)",
        "desc": "Packs all cleaned pages into a single 300-DPI PDF via `pdf-lib`."
      }
    ],
    "guideProTips": [
      "Shoot paper documents against a darker desk or table surface so the page edges are easy to align and crop.",
      "Set Contrast between `35` and `50` with Grayscale enabled to replicate a laser-printer photocopy look.",
      "After exporting your cleaned PDF, you can open it directly in **Local E-Sign Pad (`sign.html`)** to sign and date it."
    ],
    "guideSpecs": "Input: JPEG, PNG, WebP · Output: Multi-page 300-DPI PDF or PNG · Processing: HTML5 Canvas + pdf-lib"
  },
  "sign": {
    "videoDuration": "38s",
    "guideSteps": [
      {
        "title": "Step 1: Draw or Type Your Signature on the Ink Pad",
        "ui": "Signature Pad Canvas (#pad)",
        "narration": "To sign a PDF locally without DocuSign or cloud uploads, open sign.html and draw your signature on the pad using your mouse, trackpad, or stylus.",
        "guide": "Draw your signature smoothly on the `#pad` canvas using a mouse, finger, or stylus (or switch to the **Type** tab to generate a calligraphic signature from your typed name).",
        "result": "High-resolution transparent ink strokes are captured locally."
      },
      {
        "title": "Step 2: Lock Signature & Drop Your PDF Document",
        "ui": "Use Signature (#useSig) & PDF Dropzone (#dz)",
        "narration": "Second, click Use This Signature to lock your ink, then drag your PDF contract or form onto the PDF dropzone below.",
        "guide": "Click **Use this signature (`#useSig`)**, then drop the `.pdf` file you need to sign onto `#dz`. Select the target page number from the page dropdown (`#pageSel`).",
        "result": "The selected PDF page renders live on the preview canvas (`#cv`)."
      },
      {
        "title": "Step 3: Enable Date Stamp & Click Page to Place Signature",
        "ui": "Stamp Date (#addDate) & Page Canvas (#cv)",
        "narration": "Third, check Stamp Date if you want today's ISO date printed beneath your signature, then click the exact spot on the PDF page preview where your signature belongs.",
        "guide": "Check **Stamp today's date (`#addDate`)** and adjust the signature size slider if needed. Click directly on the signature line on the PDF preview canvas (`#cv`) to position your ink.",
        "result": "Your signature and date stamp appear at the exact coordinates you clicked."
      },
      {
        "title": "Step 4: Flatten & Download Signed PDF",
        "ui": "Flatten & Download Button (#stamp)",
        "narration": "Finally, click Flatten and Download Signed PDF. Your signature and date are permanently baked into the PDF page stream with zero editable overlays left behind.",
        "guide": "Click **Flatten & download signed PDF (`#stamp`)**. `pdf-lib` embeds the signature XObject and date text directly into the page content stream.",
        "result": "Signed, flattened `.pdf` saved to your machine—nothing ever left your browser."
      }
    ],
    "guideControls": [
      {
        "name": "Signature Pad (`#pad`) & Clear (`#clearPad`)",
        "desc": "Pressure-aware pointer canvas supporting mouse, touch, and pen/stylus input."
      },
      {
        "name": "Use this signature (`#useSig`)",
        "desc": "Captures the drawn ink as a transparent PNG ready for placement on any PDF page."
      },
      {
        "name": "Page Selector (`#pageSel`) & Stamp Date (`#addDate`)",
        "desc": "Switch between pages of a multi-page PDF and optionally append the current date below the signature."
      },
      {
        "name": "Flatten & download (`#stamp`)",
        "desc": "Bakes the signature and date into the PDF page content stream and downloads the signed PDF."
      }
    ],
    "guideProTips": [
      "On a laptop trackpad, draw slightly larger across the full width of `#pad`, then use the scale control to size it down neatly onto narrow signature lines.",
      "Need to sign on multiple pages (e.g., initialing Page 1 and signing Page 4)? Place and stamp Page 1, then drop the resulting PDF to sign Page 4.",
      "Because the ink is flattened into the page stream rather than added as a floating annotation, recipients cannot accidentally drag or delete your signature."
    ],
    "guideSpecs": "Input: Any standard PDF · Output: Flattened signed PDF · Note: Visual ink signature (not PKI/X.509 hardware certificate)"
  },
  "receipts": {
    "videoDuration": "36s",
    "guideSteps": [
      {
        "title": "Step 1: Drop a Batch of Receipt Photos",
        "ui": "Receipt Dropzone (#dz)",
        "narration": "To combine a shoebox of receipt photos into one organized expense PDF, open receipts.html and drop all your receipt images onto the dropzone.",
        "guide": "Select or drag a batch of receipt photos (`.jpg`, `.png`, `.webp`) onto `#dz`.",
        "result": "All receipts load into the workspace and EXIF timestamps are parsed automatically."
      },
      {
        "title": "Step 2: Automatic Chronological Sorting by Capture Date",
        "ui": "Sorted Receipt List (#list)",
        "narration": "Second, notice how the tool automatically sorts every receipt chronologically using its EXIF capture date, falling back to file modification date when needed.",
        "guide": "Inspect the ordered list in `#list`. Receipts are sorted oldest-to-newest by their EXIF `DateTimeOriginal` tag so your expense packet follows your trip timeline.",
        "result": "Receipts are ordered chronologically without manual renaming."
      },
      {
        "title": "Step 3: Rotate Sideways Receipts or Reorder Rows",
        "ui": "Row Controls in #list",
        "narration": "Third, review each row in the list. You can rotate any sideways phone photo or adjust the order before building the document.",
        "guide": "Use the per-row controls in `#list` to rotate sideways photos 90° or remove duplicate shots before exporting.",
        "result": "Every receipt is upright and properly sequenced."
      },
      {
        "title": "Step 4: Build One Stamped Multi-Page Expense PDF",
        "ui": "Build Stamped PDF Button (#pdf)",
        "narration": "Finally, click Build Stamped PDF. Every page is generated with a clean header showing the receipt index, capture date, and original filename.",
        "guide": "Click **Build 1 stamped PDF (`#pdf`)**. `pdf-lib` lays out one receipt per page with a top audit header (`#1 · YYYY-MM-DD · filename.jpg`).",
        "result": "A single, accountant-ready expense report PDF downloads to your device."
      }
    ],
    "guideControls": [
      {
        "name": "Batch Dropzone (`#dz`)",
        "desc": "Accepts dozens of JPEG, PNG, or WebP receipt photos in one drop."
      },
      {
        "name": "Chronological List (`#list`)",
        "desc": "Displays each receipt's detected EXIF date, dimensions, and page order."
      },
      {
        "name": "Build 1 stamped PDF (`#pdf`)",
        "desc": "Generates a single multi-page PDF with audit headers stamped at the top of every page."
      }
    ],
    "guideProTips": [
      "Take receipt photos with your phone camera (which embeds `DateTimeOriginal`) so multi-day business trip receipts sort themselves automatically.",
      "Pair this tool with **Receipt OCR to CSV (`ocr.html`)**: use `receipts.html` for the visual PDF attachment and `ocr.html` for the spreadsheet line items.",
      "All EXIF GPS coordinates from the original receipt photos are left out of the newly built PDF pages."
    ],
    "guideSpecs": "Input: JPEG, PNG, WebP batches · Output: Chronologically sorted, header-stamped multi-page PDF"
  },
  "ocr": {
    "videoDuration": "43s",
    "guideSteps": [
      {
        "title": "Step 1: Drop Receipt Photos Into the Local OCR Dropzone",
        "ui": "OCR Dropzone (#dz)",
        "narration": "To extract receipt dates, vendors, and totals into a spreadsheet without uploading financial data, open ocr.html and drop your receipt images onto the dropzone.",
        "guide": "Open `ocr.html` and drop one or more receipt images (`.jpg`, `.png`, `.webp`) onto `#dz`.",
        "result": "The self-hosted Tesseract WebAssembly OCR engine initializes from the same origin."
      },
      {
        "title": "Step 2: Watch On-Device Tesseract WASM Extract Text",
        "ui": "OCR Status Indicator (#stat)",
        "narration": "Second, watch the status bar as the self-hosted Tesseract WebAssembly engine recognizes the text on your CPU and parses the merchant name, date, currency, and total.",
        "guide": "Monitor `#stat` while Tesseract WASM scans each receipt image and runs heuristic parsers for merchant header lines, calendar dates, currency symbols, and `TOTAL` amounts.",
        "result": "Structured expense rows populate the results table with an OCR confidence score."
      },
      {
        "title": "Step 3: Review & Edit Any Low-Confidence Cells Inline",
        "ui": "Editable Results Table (#tbl)",
        "narration": "Third, inspect the extracted expense table. Any cell with low OCR confidence is highlighted so you can click directly inside the table to edit the merchant, category, or amount.",
        "guide": "Review `#tbl` inside `#resultsPanel`. Click any Date, Merchant, Category, Amount, or Currency cell to make inline corrections if thermal ink was faded.",
        "result": "100% verified structured expense rows ready for accounting import."
      },
      {
        "title": "Step 4: Export to CSV or TSV for Excel & QuickBooks",
        "ui": "Export CSV Button (#csv)",
        "narration": "Finally, click Export CSV or Copy TSV to bring your structured expense table straight into Excel, Google Sheets, or QuickBooks.",
        "guide": "Click **Export CSV (`#csv`)** to download `expenses.csv` (with columns `date,merchant,category,amount,currency,file,ocr_confidence`) or copy TSV to paste directly into a spreadsheet.",
        "result": "Clean `expenses.csv` file saved locally with zero cloud OCR API fees."
      }
    ],
    "guideControls": [
      {
        "name": "Receipt Dropzone (`#dz`)",
        "desc": "Accepts single or batch receipt photos in JPEG, PNG, or WebP format."
      },
      {
        "name": "Editable Expense Table (`#tbl`)",
        "desc": "Inline-editable cells for Date, Merchant, Category, Amount, and Currency with per-row OCR confidence."
      },
      {
        "name": "Export CSV (`#csv`)",
        "desc": "Downloads RFC-4180 compliant `expenses.csv` ready for Excel, Numbers, Google Sheets, or QuickBooks."
      }
    ],
    "guideProTips": [
      "If a receipt photo is skewed or has dark shadows, run it through **Scan & Screenshot Cleaner (`scan.html`)** with Grayscale + Contrast first to boost OCR accuracy above 95%.",
      "The ~24 MB Tesseract language model is fetched once from `navigatorslab.com` and cached by the PWA Service Worker for full offline use afterward.",
      "Always glance at rows where `ocr_confidence` is below 80%—crumpled thermal paper often blurs decimal points."
    ],
    "guideSpecs": "Engine: Self-hosted Tesseract.js WASM (`tess/` + `tessdata/`) · Output: `expenses.csv` (`date,merchant,category,amount,currency,file,ocr_confidence`)"
  },
  "qr": {
    "videoDuration": "38s",
    "guideSteps": [
      {
        "title": "Step 1: Type Text/URL or Pick Wi-Fi, vCard, or Email Preset",
        "ui": "Payload Input (#qrText) & Presets (#preWifi)",
        "narration": "To generate or decode QR codes offline, open qr.html and type a URL into the payload box, or click one of the preset buttons like Wi-Fi, vCard, or Email.",
        "guide": "Enter any URL or text into `#qrText`, or click a structured preset button (**Wi-Fi `#preWifi`**, **vCard**, **Email**, **SMS**) to open its dedicated fields.",
        "result": "Structured payload fields appear (and special characters like `;` and `\\` in Wi-Fi passwords are escaped automatically)."
      },
      {
        "title": "Step 2: Apply Preset & Tune Error Correction (L / M / Q / H)",
        "ui": "Wi-Fi Builder (#wifiMake) & Error Correction (#ec)",
        "narration": "Second, fill in your Wi-Fi network name and password, click Apply Wi-Fi Preset, and choose your error correction level and foreground or background colors.",
        "guide": "Fill the preset fields (e.g., SSID `#wifiS` and Password `#wifiP`), click **Apply (`#wifiMake`)**, select Error Correction (`L`, `M`, `Q`, or `H`), and click **Generate QR (`#qrMake`)**.",
        "result": "Crisp QR matrix renders immediately with module count and error-correction metadata (`#qrMeta`)."
      },
      {
        "title": "Step 3: Export Crisp Vector SVG or High-DPI PNG",
        "ui": "Export PNG (#qrPng) & SVG (#qrSvg)",
        "narration": "Third, click Download PNG for screens or Download SVG for infinite-resolution print signage without any tracking redirect URLs.",
        "guide": "Click **Download PNG (`#qrPng`)** for digital use or **Download SVG (`#qrSvg`)** for vector print layout in Illustrator, Figma, or InDesign.",
        "result": "Direct-payload PNG or vector SVG saved locally (never expires, zero bit.ly/redirect middlemen)."
      },
      {
        "title": "Step 4: Switch to Decode Tab to Read Any QR Image Locally",
        "ui": "Decode Tab (#tabRead) & QR Dropzone (#qrDz)",
        "narration": "Finally, click the Decode QR tab and drop or paste any screenshot containing a QR code to inspect its exact raw payload before visiting the link.",
        "guide": "Click **Decode QR (`#tabRead`)** and drop an image or paste a screenshot (`Ctrl+V`) onto `#qrDz`. `jsQR` decodes the raw payload string into `#qrData`.",
        "result": "Inspect suspicious QR codes safely without opening untrusted URLs on your phone."
      }
    ],
    "guideControls": [
      {
        "name": "Payload Box (`#qrText`) & Generate (`#qrMake`)",
        "desc": "Encodes any text, URL, or preset string into a QR matrix."
      },
      {
        "name": "Presets (`#preWifi`, vCard, Email)",
        "desc": "Builds standards-compliant `WIFI:T:WPA;...` and `BEGIN:VCARD` payloads with RFC escaping."
      },
      {
        "name": "Export PNG (`#qrPng`) & SVG (`#qrSvg`)",
        "desc": "Saves high-resolution raster PNG or true vector SVG files."
      },
      {
        "name": "Decode Tab (`#tabRead` + `#qrDz`)",
        "desc": "Decodes QR images locally via bundled `jsQR` without a camera or network request."
      }
    ],
    "guideProTips": [
      "Always choose **SVG** when sending a QR code to a print shop for flyers, business cards, or banners so the module edges stay razor-sharp at any size.",
      "Use Error Correction level **Q (25%)** or **H (30%)** for printed stickers outdoors so the code still scans even if scratched or smudged.",
      "You can deep-link directly to a generated QR code via URL parameters: `qr.html?text=https://navigatorslab.com&ec=H`."
    ],
    "guideSpecs": "Engines: `qrcode-generator` + `jsQR` (100% bundled) · Exports: PNG, Vector SVG · Deep-Link: `?text=...&ec=M`"
  },
  "audio": {
    "videoDuration": "40s",
    "guideSteps": [
      {
        "title": "Step 1: Drop a Voice Note, Podcast Clip, or Song",
        "ui": "Audio Dropzone (#dz)",
        "narration": "To trim an audio file or convert it to MP3 in your browser, open audio.html and drop any WAV, MP3, M4A, AAC, or OGG file onto the dropzone.",
        "guide": "Drag and drop an audio file (`.wav`, `.mp3`, `.m4a`, `.aac`, `.ogg`, `.flac`) onto `#dz`.",
        "result": "Web Audio API decodes the audio buffer locally and renders the full waveform canvas (`#wave`)."
      },
      {
        "title": "Step 2: Inspect the Waveform & Select Start / End Times",
        "ui": "Waveform Canvas (#wave) & Time Inputs (#t0, #t1)",
        "narration": "Second, drag the selection handles directly on the waveform canvas—or type exact start and end seconds into the Start and End boxes—to isolate your clip.",
        "guide": "Drag the left and right trim handles on `#wave` or type millisecond-accurate timestamps into **Start (`#t0`)** and **End (`#t1`)**. Click **Preview selection** to listen to the cut.",
        "result": "Exact sample boundaries are locked in with live duration readout."
      },
      {
        "title": "Step 3: Add Smooth Fade-In / Fade-Out & Pick WAV or MP3",
        "ui": "Fade Controls & Format Selector (#fmt)",
        "narration": "Third, add an optional fade-in or fade-out envelope so the cut doesn't click, and choose lossless WAV or compressed MP3 from the format selector.",
        "guide": "Configure fade-in/fade-out durations and select `wav` (uncompressed 16-bit PCM) or `mp3` (encoded via self-hosted `lamejs`) in `#fmt`.",
        "result": "Envelope and encoder settings are ready for local rendering."
      },
      {
        "title": "Step 4: Click Export Trimmed Audio",
        "ui": "Export Button (#exp)",
        "narration": "Finally, click Export Trimmed Audio. Your browser slices the sample buffer and downloads the finished WAV or MP3 file immediately.",
        "guide": "Click **Export (`#exp`)**. The browser slices the PCM buffer, applies fade envelopes, encodes to WAV or MP3 via `lamejs`, and downloads the file.",
        "result": "Sample-accurate `.wav` or `.mp3` clip saved locally in under a second."
      }
    ],
    "guideControls": [
      {
        "name": "Waveform Canvas (`#wave`)",
        "desc": "Interactive peak visualization for dragging trim start and end handles."
      },
      {
        "name": "Start (`#t0`) & End (`#t1`) Inputs",
        "desc": "Numeric inputs (in seconds) for exact sample-accurate trimming."
      },
      {
        "name": "Output Format (`#fmt`)",
        "desc": "Switch between 16-bit PCM `.wav` and self-hosted LAME `.mp3` encoding."
      },
      {
        "name": "Export Button (`#exp`)",
        "desc": "Renders and downloads the trimmed audio clip."
      }
    ],
    "guideProTips": [
      "Apply a `0.05s` to `0.15s` fade-in and fade-out when cutting spoken voice notes to eliminate zero-crossing pops at the start and end of the clip.",
      "Choose `WAV` when exporting clips for video editors (Premiere, DaVinci Resolve, CapCut) and `MP3` when sharing voice notes over email or chat.",
      "Because decoding and LAME MP3 encoding happen entirely in your tab, confidential interview recordings never touch a cloud transcription server."
    ],
    "guideSpecs": "Input: WAV, MP3, M4A, OGG, FLAC · Output: 16-bit PCM WAV or LAME MP3 (`lamejs/` self-hosted)"
  },
  "invoice": {
    "videoDuration": "36s",
    "guideSteps": [
      {
        "title": "Step 1: Enter Business Info, Client Details & Currency",
        "ui": "Header Fields (#biz, #client, #docNo)",
        "narration": "To create a clean vector PDF invoice or quote without signing up for billing software, open invoice.html and fill in your business name, client name, and invoice number.",
        "guide": "Enter your company/freelancer details in `#biz`, client billing address in `#client`, document number in `#docNo` (e.g., `INV-2026-042`), and pick your currency symbol.",
        "result": "Header details populate the live invoice workspace."
      },
      {
        "title": "Step 2: Add Line Items, Quantities & Hourly/Unit Rates",
        "ui": "Line Items Table (#items)",
        "narration": "Second, fill in your line items table with descriptions, hours or quantities, and unit rates. Click Add Row for additional deliverables.",
        "guide": "In `#items`, type each deliverable description (`.d`), quantity/hours (`.q`), and rate (`.r`). Click **+ Add line item** to append more rows.",
        "result": "Each row subtotal calculates automatically as you type."
      },
      {
        "title": "Step 3: Configure Tax Percentage, Discounts & Payment Notes",
        "ui": "Tax (#tax) & Live Total (#total)",
        "narration": "Third, enter your tax percentage or discount and add payment instructions or bank details. The grand total updates live on screen.",
        "guide": "Set your tax percentage in `#tax` (and any discount or payment terms/notes). Verify the calculated subtotal, tax amount, and grand total in `#total`.",
        "result": "Exact subtotal, tax, and grand total verified before export."
      },
      {
        "title": "Step 4: Download Vector PDF Invoice",
        "ui": "Download PDF Button (#pdf)",
        "narration": "Finally, click Download PDF. pdf-lib generates a crisp, print-ready vector PDF invoice directly in your browser tab.",
        "guide": "Click **Download PDF (`#pdf`)** to generate a crisp vector PDF via `pdf-lib` (typically ~4 KB, searchable text, razor-sharp at any zoom).",
        "result": "Professional `INV-xxxx.pdf` downloaded locally with zero watermarks or platform fees."
      }
    ],
    "guideControls": [
      {
        "name": "Sender (`#biz`) & Client (`#client`)",
        "desc": "Multi-line business contact, tax ID, and client billing details."
      },
      {
        "name": "Document Number (`#docNo`) & Currency",
        "desc": "Invoice or quote identifier and currency formatting."
      },
      {
        "name": "Line Items Table (`#items`) & Tax (`#tax`)",
        "desc": "Dynamic rows for description, quantity, and unit price with automatic tax/discount math."
      },
      {
        "name": "Download PDF (`#pdf`)",
        "desc": "Generates a clean vector PDF document via `pdf-lib`."
      }
    ],
    "guideProTips": [
      "Unlike screenshot-based HTML-to-PDF tools, Invoice Generator draws real vector text streams with `pdf-lib`, so your client's accounting software can copy/paste the invoice number and total cleanly.",
      "Include your wire/ACH or payment link in the Notes box at the bottom so clients have everything on one page.",
      "Need to sign the quote before sending? Drop the exported invoice PDF straight into **Local E-Sign Pad (`sign.html`)**."
    ],
    "guideSpecs": "Output: True vector PDF (`pdf-lib`) · Math: Automatic line-item subtotal, discount, and tax calculation"
  },
  "rename": {
    "videoDuration": "33s",
    "guideSteps": [
      {
        "title": "Step 1: Drop a Batch of Photos or Files to Rename",
        "ui": "Batch Dropzone (#dz)",
        "narration": "To batch-rename messy camera photos or project files by capture date, open rename.html and drop your files onto the dropzone.",
        "guide": "Drag and drop a batch of photos or documents (`IMG_4821.JPG`, `DSC0092.JPG`, etc.) onto `#dz`.",
        "result": "Files load and EXIF `DateTimeOriginal` timestamps (or file modified dates) are extracted."
      },
      {
        "title": "Step 2: Choose Naming Pattern & Custom Slug",
        "ui": "Slug Source (#slugSrc) & Custom Slug (#slugText)",
        "narration": "Second, select Fixed Slug or Original Name from the pattern menu and type your descriptive project slug—such as site-inspection or home-depot.",
        "guide": "Select the naming rule in `#slugSrc` (e.g., `fixed` custom slug or cleaned original filename), type your label into `#slugText` (e.g., `site-inspection`), and configure sequence padding.",
        "result": "Pattern rule (`YYYY-MM-DD-<slug>-01.ext`) is configured."
      },
      {
        "title": "Step 3: Click Preview New Names to Inspect Mapping",
        "ui": "Apply Preview (#apply) & Mapping List (#list)",
        "narration": "Third, click Apply and Preview. Every row shows the original filename alongside the new ISO-dated filename so you can catch any collisions before saving.",
        "guide": "Click **Apply (`#apply`)** and inspect the `Old Name → New Name` preview table in `#list`.",
        "result": "Deterministic, collision-free filenames previewed side-by-side."
      },
      {
        "title": "Step 4: Download All Renamed Files as One ZIP",
        "ui": "Download ZIP Button (#zip)",
        "narration": "Finally, click Download ZIP to save all your renamed files in a single archive without touching your originals.",
        "guide": "Click **Download ZIP (`#zip`)** to package all renamed files into a single local `.zip` archive via `JSZip`.",
        "result": "Cleanly named archive downloaded while original files remain untouched."
      }
    ],
    "guideControls": [
      {
        "name": "Batch Dropzone (`#dz`)",
        "desc": "Accepts any number of images or documents for batch renaming."
      },
      {
        "name": "Slug Mode (`#slugSrc`) & Text (`#slugText`)",
        "desc": "Combines EXIF/file dates (`YYYY-MM-DD`) with a custom project slug and sequence numbers."
      },
      {
        "name": "Apply Preview (`#apply`)",
        "desc": "Updates the live `Old → New` filename table (`#list`)."
      },
      {
        "name": "Download ZIP (`#zip`)",
        "desc": "Bundles all renamed files into one `.zip` archive."
      }
    ],
    "guideProTips": [
      "Combining photos from two different cameras (e.g., an iPhone and a Sony mirrorless)? Batch Rename sorts and names them by EXIF capture date so both cameras' shots interleave in true chronological order.",
      "Use lowercase hyphenated slugs (`2026-11-08-client-workshop-01.jpg`) for web assets and S3/Cloudflare R2 uploads so URLs never contain `%20` spaces.",
      "Your original files on disk are never overwritten—the renamed copies are delivered cleanly inside the downloaded `.zip`."
    ],
    "guideSpecs": "Date Parsing: EXIF `DateTimeOriginal` + Last-Modified fallback · Output: Client-side `.zip` bundle (`JSZip`)"
  },
  "printprep": {
    "videoDuration": "40s",
    "guideSteps": [
      {
        "title": "Step 1: Drop Your Image, Flyer, or Artwork",
        "ui": "Print Dropzone (#dz)",
        "narration": "To prepare an image or flyer for a commercial print shop with exact bleed and crop marks, open printprep.html and drop your artwork onto the dropzone.",
        "guide": "Drop your high-resolution image or design (`.jpg`, `.png`, `.webp`) onto `#dz`.",
        "result": "Source pixel dimensions and aspect ratio are inspected."
      },
      {
        "title": "Step 2: Pick Physical Trim Size & Bleed Margin",
        "ui": "Trim Size (#size) & Bleed Input (#bleed)",
        "narration": "Second, choose your physical print size—such as 4 by 6 inches, 5 by 7, Letter, or A4—and enter your print shop's bleed margin, typically 0.125 inches.",
        "guide": "Select the target physical sheet size in `#size` (`4x6`, `5x7`, `8x10`, `Letter`, `A4`) and set the bleed margin in inches in `#bleed` (standard commercial bleed is `0.125` in / 3 mm).",
        "result": "Target physical dimensions (`4.25 × 6.25 in` with bleed) and 300-DPI pixel targets (`1275 × 1875 px`) are calculated."
      },
      {
        "title": "Step 3: Click Prepare Print Sheet & Check DPI Verdict",
        "ui": "Prepare Button (#prep) & Preview (#list)",
        "narration": "Third, click Prepare Print Sheet. The tool computes your effective DPI at that physical size, warns you if resolution is below 300 DPI, and renders trim marks.",
        "guide": "Click **Prepare (`#prep`)**. Inspect the generated proof in `#list` showing the effective DPI calculation, bleed extension area, and corner crop/trim marks.",
        "result": "Visual print proof and DPI quality verdict displayed on screen."
      },
      {
        "title": "Step 4: Export Print-Ready PDF at Exact Physical MediaBox",
        "ui": "Export PDF Button (#pdf)",
        "narration": "Finally, click Export Print-Ready PDF to save a PDF whose MediaBox matches the exact physical inch dimensions required by your printer.",
        "guide": "Click **Export PDF (`#pdf`)** to generate a PDF with exact PostScript point dimensions (`72 pt = 1 inch`, e.g., `306 × 450 pt` for `4.25 × 6.25 in`) and corner trim marks.",
        "result": "Print-shop-ready PDF saved locally."
      }
    ],
    "guideControls": [
      {
        "name": "Physical Size (`#size`)",
        "desc": "Presets for `4x6`, `5x7`, `8x10`, `Letter` (`8.5×11 in`), and `A4`."
      },
      {
        "name": "Bleed Margin (`#bleed`)",
        "desc": "Bleed margin in inches added to all four edges (default `0.125` in)."
      },
      {
        "name": "Prepare (`#prep`) & DPI Readout",
        "desc": "Renders the sheet preview with corner crop marks and reports effective DPI."
      },
      {
        "name": "Export PDF (`#pdf`)",
        "desc": "Builds a PDF with exact physical `MediaBox` dimensions via `pdf-lib`."
      }
    ],
    "guideProTips": [
      "Most commercial print shops (FedEx Office, VistaPrint, local offset printers) require a `0.125 inch` (`3 mm`) bleed so white slivers don't appear when the guillotine blade trims the stack.",
      "Check the **DPI effective** readout before printing: `300+ DPI` is sharp for handheld postcards/photos; `150–200 DPI` is acceptable for wall posters viewed from 3+ feet away.",
      "Open the exported PDF in Adobe Acrobat or PDF Studio to verify the page size in inches matches `Trim Size + (2 × Bleed)`."
    ],
    "guideSpecs": "Sizes: 4×6, 5×7, 8×10, Letter, A4 · Bleed: Configurable (default 0.125 in) · Output: 300-DPI PDF with trim marks"
  },
  "pdfpages": {
    "videoDuration": "38s",
    "guideSteps": [
      {
        "title": "Step 1: Drop One or More PDFs to Load Page Thumbnails",
        "ui": "PDF Dropzone (#dz)",
        "narration": "To reorder, rotate, delete, or merge PDF pages in your browser, open pdfpages.html and drop one or more PDF files onto the dropzone.",
        "guide": "Drag one or more `.pdf` files onto `#dz`. Dropping multiple PDFs appends all of their pages into one unified thumbnail grid.",
        "result": "`pdf.js` renders a live visual thumbnail card (`.pp-cell`) for every page."
      },
      {
        "title": "Step 2: Drag Thumbnails to Reorder, Rotate 90°, or Delete",
        "ui": "Thumbnail Grid (#pages)",
        "narration": "Second, drag any page thumbnail to change its order, click the rotate icon to fix a sideways scan, or click the X button on a card to delete an unwanted page.",
        "guide": "In `#pages`, drag and drop `.pp-cell` cards to reorder them, click **↻** on a card to rotate that page 90°, or click **× (`.pp-x`)** to remove a page.",
        "result": "Page sequence and orientations update visually in real time."
      },
      {
        "title": "Step 3: Select Specific Pages or Insert Blank Separator Pages",
        "ui": "Page Checkboxes & Insert Blank (#blank)",
        "narration": "Third, use the checkboxes on each thumbnail to select a subset of pages, or click Insert Blank Page to add a separator sheet.",
        "guide": "Toggle the checkbox on individual `.pp-cell` cards to pick specific pages for extraction, or click **Insert blank (`#blank`)** to add a clean separator page.",
        "result": "Custom page selection or blank separator pages added to the layout."
      },
      {
        "title": "Step 4: Rebuild Full PDF or Extract Selected Pages",
        "ui": "Rebuild (#rebuild) & Extract (#extract)",
        "narration": "Finally, click Rebuild PDF to export the complete rearranged document, or click Extract Selected to save only your checked pages as a new PDF.",
        "guide": "Click **Rebuild PDF (`#rebuild`)** to download the full reordered/merged document, or **Extract selected (`#extract`)** to export only the checked pages.",
        "result": "Lossless vector page copy built via `pdf-lib` and downloaded locally."
      }
    ],
    "guideControls": [
      {
        "name": "Thumbnail Grid (`#pages` / `.pp-cell`)",
        "desc": "Drag-and-drop visual cards for every page across one or more loaded PDFs."
      },
      {
        "name": "Per-Page Rotate (`↻`) & Delete (`.pp-x`)",
        "desc": "Rotate individual pages in 90° increments or delete unwanted cover/blank pages."
      },
      {
        "name": "Insert Blank (`#blank`)",
        "desc": "Inserts a blank separator page into the document sequence."
      },
      {
        "name": "Rebuild (`#rebuild`) & Extract (`#extract`)",
        "desc": "Exports either the entire modified deck or only the checked pages as a new PDF."
      }
    ],
    "guideProTips": [
      "To merge two or three separate PDFs into one packet, simply drop all of them onto `#dz` one after another, drag the thumbnails into order, and click **Rebuild PDF**.",
      "Because `pdf-lib` copies page dictionary nodes directly without rasterizing, vector text and embedded fonts stay 100% sharp and searchable.",
      "Need deeper in-place text editing, redaction, or OCR on those pages? Open **PDF Studio (`/pdf-studio/`)**."
    ],
    "guideSpecs": "Engine: `pdf.js` (thumbnails) + `pdf-lib` (lossless page-tree rebuild) · Operations: Merge, Split, Extract, Rotate, Reorder, Delete"
  },
  "textdiff": {
    "videoDuration": "32s",
    "guideSteps": [
      {
        "title": "Step 1: Paste Original Text (Version A) Into the Left Pane",
        "ui": "Original Text Editor (#textA)",
        "narration": "To compare two versions of a contract, config file, or article locally, open textdiff.html and paste the original text into the Version A box on the left.",
        "guide": "Paste or type the baseline version of your contract clause, code snippet, or prose into `#textA`.",
        "result": "Original text is loaded in local browser memory."
      },
      {
        "title": "Step 2: Paste Revised Text (Version B) Into the Right Pane",
        "ui": "Revised Text Editor (#textB)",
        "narration": "Second, paste the revised text into the Version B box on the right.",
        "guide": "Paste the updated or redlined text into `#textB`.",
        "result": "Both versions are ready for Longest Common Subsequence (LCS) comparison."
      },
      {
        "title": "Step 3: Click Compare Texts to Inspect Word-Level Highlights",
        "ui": "Compare Button (#btnDiff) & Diff Output (#diffOut)",
        "narration": "Third, click Compare Texts. The diff viewer highlights exact word-level additions in green and deletions in red, so you immediately spot changed numbers or dates.",
        "guide": "Click **Compare (`#btnDiff`)**. Inspect `#diffSummary` (added/removed line counts and similarity percentage) and `#diffOut`, where intra-line word changes are highlighted in green (`.w-add`) and red (`.w-del`).",
        "result": "Subtle single-word edits (like `30 days` → `45 days`) stand out immediately."
      },
      {
        "title": "Step 4: Export Standard Unified .diff Patch File",
        "ui": "Download .diff Button (#btnDl)",
        "narration": "Finally, click Download .diff to save a standard unified diff file that you can attach to a pull request, audit log, or email.",
        "guide": "Click **Download .diff (`#btnDl`)** to save a standard unified diff file with `-` and `+` hunks.",
        "result": "Standard `.diff` patch file downloaded locally."
      }
    ],
    "guideControls": [
      {
        "name": "Version A (`#textA`) & Version B (`#textB`)",
        "desc": "Side-by-side text areas for original and revised text."
      },
      {
        "name": "Compare (`#btnDiff`)",
        "desc": "Runs the deterministic LCS diff algorithm with intra-line word highlighting."
      },
      {
        "name": "Diff Summary (`#diffSummary`) & Output (`#diffOut`)",
        "desc": "Shows similarity score, added/removed counts, and color-coded word diffs."
      },
      {
        "name": "Download .diff (`#btnDl`)",
        "desc": "Exports a standard unified `.diff` text file."
      }
    ],
    "guideProTips": [
      "Use Text Diff before signing a counter-party's 'clean final PDF' of an NDA or MSA: copy the text from your draft into `#textA` and the text from their PDF into `#textB` to catch silent edits.",
      "AI agents can also call this exact diff engine deterministically via `POST https://navigatorslab.com/tools/mcp` (`text_diff` tool).",
      "You can pre-populate inputs via URL parameters (`textdiff.html?a=...&b=...`)."
    ],
    "guideSpecs": "Algorithm: Longest Common Subsequence (LCS) + Intra-line Word Token Diff · Export: Unified `.diff` · MCP: `text_diff`"
  },
  "reimagine": {
    "videoDuration": "44s",
    "guideSteps": [
      {
        "title": "Step 1: Open Reimagine Playground & Paste HTML or Pick a Preset",
        "ui": "Reimagine Workspace (navigatorslab.com/reimagine/)",
        "narration": "To redesign any web page from its own content without hallucinating a single fact, open navigatorslab.com/reimagine/ and paste your HTML or pick a built-in preset.",
        "guide": "Open `https://navigatorslab.com/reimagine/` and paste raw HTML markup, drop an `.html` file, or click one of the built-in presets (SaaS, Documentation, Report, Portfolio).",
        "result": "Source HTML is parsed into a structured content AST in your browser."
      },
      {
        "title": "Step 2: Deterministic Extraction of Headings, Metrics & Dates",
        "ui": "Content Extraction Inspector",
        "narration": "Second, inspect the extracted facts panel. Reimagine deterministically pulls out every heading, metric, date, table, link, and brand color with zero LLM guesswork.",
        "guide": "Review the extracted content inventory: headings, numeric KPIs/metrics, calendar dates, lists, tables, and source palette tokens are preserved verbatim.",
        "result": "100% factual fidelity guaranteed—no numbers or dates are ever invented or altered."
      },
      {
        "title": "Step 3: Switch Across 17 Visual Layout Directions",
        "ui": "17 Direction Switcher (Editorial, Infographic, 3D, Dashboard...)",
        "narration": "Third, click through the seventeen deterministic design directions—including Editorial, Infographic, Three.js 3D, Swiss Grid, Brutalist, and Executive Dashboard.",
        "guide": "Click any of the **17 layout direction pills** (Editorial, Infographic, 3D Interactive, Swiss Grid, Terminal, Magazine, Dashboard, etc.) to rebuild the page live.",
        "result": "Instant full-page visual transformation using your exact source content."
      },
      {
        "title": "Step 4: Export Self-Contained HTML or Run the CLI / MCP Server",
        "ui": "Export HTML Button & CLI (`npx reimagine-it`)",
        "narration": "Finally, click Export HTML to download a single self-contained file, or run npx reimagine-it audit and generate directly in your terminal or coding agent.",
        "guide": "Click **Export HTML** to save the redesigned page, or use the CLI (`npx reimagine-it page.html --direction infographic`) and MCP server in your repo.",
        "result": "Production-ready, self-contained HTML audited across 18 design-health checks."
      }
    ],
    "guideControls": [
      {
        "name": "HTML Input / Preset Selector",
        "desc": "Paste raw HTML markup or load sample presets in the browser playground."
      },
      {
        "name": "17 Deterministic Layout Directions",
        "desc": "Switch instantly between Editorial, Infographic, 3D (Three.js), Dashboard, Swiss Grid, and 12 more."
      },
      {
        "name": "Fact-Preserving AST Extractor",
        "desc": "Locks all source numbers, dates, quotes, and links so nothing is hallucinated."
      },
      {
        "name": "CLI & MCP Server (`Kayforkind/reimagine-it`)",
        "desc": "Run `reimagine-it audit` or `reimagine-it build` from Node.js or any MCP agent."
      }
    ],
    "guideProTips": [
      "Use `reimagine-it audit index.html` in CI to score any web page across typography, contrast, layout rhythm, and content preservation.",
      "Try the **Infographic** direction on dense quarterly reports or READMEs that contain lots of statistics and milestone dates.",
      "All exported HTML pages are self-contained with zero external runtime dependencies."
    ],
    "guideSpecs": "Live App: `navigatorslab.com/reimagine/` · Repo: `Kayforkind/reimagine-it` (213★) · Directions: 17 deterministic layouts"
  },
  "textstats": {
    "videoDuration": "36s",
    "guideSteps": [
      {
        "title": "Step 1: Paste Your Draft, Article, or Script Into the Editor",
        "ui": "Full-Width Text Editor (#textInput)",
        "narration": "To analyze readability, speaking time, and sentence rhythm locally, open textstats.html and paste your draft into the full-width editor box.",
        "guide": "Paste or type your essay, documentation page, video script, or speech into `#textInput` (or pass `?text=...` / `?url=data:...` in the URL).",
        "result": "All metrics compute instantaneously on every keystroke."
      },
      {
        "title": "Step 2: Read Live Word Count, Reading Time & Flesch Grade",
        "ui": "Metric Cards Grid (#cards)",
        "narration": "Second, check the eleven live metric cards showing exact word count, character count, reading time at 225 words per minute, speaking time, and Flesch Reading Ease.",
        "guide": "Review `#cards` for Words, Characters (with/without spaces), Sentences, Paragraphs, Reading Time (`225 wpm`), Speaking Time (`140 wpm`), Average Sentence Length, and Flesch Reading Ease (`0–100` + US Grade Level).",
        "result": "Instant readability and length verification."
      },
      {
        "title": "Step 3: Audit Top Keyword Density & Overused Terms",
        "ui": "Keyword Frequency Panel (#keywords)",
        "narration": "Third, inspect the Keyword Density table on the left, which filters out common stop-words to reveal your most repeated terms and their exact percentage.",
        "guide": "Examine `#keywords` to see the top content words ranked by count and density percentage (with common English stop-words excluded).",
        "result": "Spot repetitive phrasing or verify SEO topic coverage immediately."
      },
      {
        "title": "Step 4: Balance Your Pacing with the Sentence-Rhythm Histogram",
        "ui": "Sentence-Rhythm Histogram (#rhythm)",
        "narration": "Finally, use the Sentence-Rhythm Histogram on the right to see the word-length bar chart of every sentence and break up walls of long clauses.",
        "guide": "Inspect `#rhythm`, which plots a bar for each sentence's word count so you can spot monotonous runs or overly dense 40-word sentences.",
        "result": "Polished, well-paced prose with verified readability."
      }
    ],
    "guideControls": [
      {
        "name": "Text Editor (`#textInput`)",
        "desc": "Full-width live textarea that recalculates metrics on every keystroke."
      },
      {
        "name": "11 Stat Cards (`#cards`)",
        "desc": "Words, characters, sentences, paragraphs, reading/speaking time, and Flesch score."
      },
      {
        "name": "Keyword Density (`#keywords`)",
        "desc": "Stop-word-filtered top terms with occurrence counts and percentages."
      },
      {
        "name": "Sentence Rhythm (`#rhythm`)",
        "desc": "Visual bar chart of sentence lengths across your document."
      }
    ],
    "guideProTips": [
      "Aim for a **Flesch Reading Ease between 60 and 75** (8th–9th grade level) for technical blog posts and product landing pages so readers scan effortlessly.",
      "Recording a YouTube Short or presentation? Check the **Speaking Time (`140 wpm`)** card to verify your script fits inside 60 seconds before recording.",
      "AI agents can invoke this analyzer over MCP (`POST /tools/mcp` -> `text_stats`) or via URL deep-link (`textstats.html?text=...`)."
    ],
    "guideSpecs": "Metrics: 11 Readability & Count Cards + Stop-Word Keyword Density + Sentence Histogram · MCP: `text_stats`"
  },
  "pdfstudio": {
    "videoDuration": "44s",
    "guideSteps": [
      {
        "title": "Step 1: Open PDF Studio & Load Any PDF Document",
        "ui": "PDF Studio Workspace (navigatorslab.com/pdf-studio/)",
        "narration": "To edit, redact, sign, or OCR a PDF in your browser, open navigatorslab.com/pdf-studio/ and drop your PDF file—or click Open Sample PDF to test immediately.",
        "guide": "Navigate to `https://navigatorslab.com/pdf-studio/` and drop a `.pdf` file into the workspace, or load the built-in sample PDF.",
        "result": "Multi-page canvas, thumbnail sidebar, and tool ribbons initialize 100% client-side."
      },
      {
        "title": "Step 2: Select In-Place Text Edit, AcroForm, Sign, or Redact",
        "ui": "Top Mode Toolbar (Edit Text / Redact / Sign / OCR)",
        "narration": "Second, pick your tool from the top workspace bar: click Edit Text to rewrite existing PDF content streams in place, fill AcroForm fields, or select Vector Redaction.",
        "guide": "Choose a mode from the top toolbar: **Edit Text** (modifies PDF `/Contents` text operators in-place), **Forms** (fills AcroForms), **Redact** (purges underlying text/vector bytes), **Sign**, or **OCR**.",
        "result": "Interactive editing handles appear directly over the PDF page elements."
      },
      {
        "title": "Step 3: Run Tesseract WASM OCR or Compare Document Revisions",
        "ui": "OCR & Diff Panels",
        "narration": "Third, for scanned documents, run on-device Tesseract OCR to add a searchable text layer, or use Revision Diff to compare two versions of a contract side by side.",
        "guide": "Click **OCR** to run self-hosted Tesseract WASM across scanned pages, or open **Compare / Diff** to highlight text and visual differences between two PDF revisions.",
        "result": "Searchable text layers and revision diffs are computed locally in your browser tab."
      },
      {
        "title": "Step 4: Export Your Edited, Redacted, or Signed PDF",
        "ui": "Export / Save PDF Button",
        "narration": "Finally, click Export PDF to save your modified document locally—backed by 184 automated unit tests and zero cloud uploads.",
        "guide": "Click **Export / Download PDF** in the top-right corner to serialize the updated PDF structure tree and download the finished file.",
        "result": "Production-grade edited PDF saved locally with 0 bytes sent to any server."
      }
    ],
    "guideControls": [
      {
        "name": "In-Place Content-Stream Text Editor",
        "desc": "Edits existing text runs directly inside PDF `/Contents` streams instead of pasting white boxes over text."
      },
      {
        "name": "True Byte-Purging Vector Redaction",
        "desc": "Removes redacted text operators and vector paths from the underlying PDF stream so they cannot be copy-pasted."
      },
      {
        "name": "On-Device Tesseract WASM OCR",
        "desc": "Converts raster page scans into selectable, searchable PDF text layers locally."
      },
      {
        "name": "AcroForm Filler, Signer & Revision Diff",
        "desc": "Fills interactive PDF forms, places ink signatures, and compares two PDF files side-by-side."
      }
    ],
    "guideProTips": [
      "Unlike basic PDF annotators that merely draw a black rectangle over sensitive text, PDF Studio's Redact mode purges the underlying characters from the PDF content stream.",
      "Pair PDF Studio with the **`redact-lint`** CLI in CI to verify that no PDF in your organization ships with fake painted-over redactions.",
      "Always keep a backup of your original unredacted PDF before exporting a permanently redacted copy."
    ],
    "guideSpecs": "Live App: `navigatorslab.com/pdf-studio/` · Repo: `Kayforkind/NavigatorsLab-PDF-Studio` · Tests: 184/184 Vitest"
  },
  "designhealth": {
    "videoDuration": "39s",
    "guideSteps": [
      {
        "title": "Step 1: Add Design Health Action to Your GitHub Workflow",
        "ui": "GitHub Actions YAML (uses: Kayforkind/design-health-action@main)",
        "narration": "To enforce deterministic design quality in pull requests, open the Design Health Action guide and add uses Kayforkind/design-health-action@main to your GitHub workflow.",
        "guide": "Add `uses: Kayforkind/design-health-action@main` to `.github/workflows/design-health.yml` and point `path:` at your built HTML directory (e.g., `dist/**/*.html`).",
        "result": "Runs in ~1 second in CI with zero LLM calls and zero API keys."
      },
      {
        "title": "Step 2: Configure Target HTML Glob & Minimum Score Threshold",
        "ui": "Workflow Inputs (path, min-score)",
        "narration": "Second, set your target HTML path pattern and minimum passing threshold across the six design pillars: typography, palette, motion, content, structure, and performance.",
        "guide": "Configure `path: 'dist/**/*.html'` and optional threshold gates so regressions in contrast, heading hierarchy, or layout stability fail the PR check.",
        "result": "Deterministic 18-rule rubric locked for every pull request."
      },
      {
        "title": "Step 3: Evaluate 18 Deterministic DOM & CSS Rules",
        "ui": "18-Rule Static Analyzer",
        "narration": "Third, on every push, the action checks eighteen rules including focus-visible states, prefers-reduced-motion media queries, image aspect ratios, and line lengths.",
        "guide": "The analyzer parses HTML/CSS statically to verify 18 checks: heading scale, 45–75ch measure, `:focus-visible`, `prefers-reduced-motion`, explicit media dimensions (CLS), and semantic landmarks.",
        "result": "Per-rule pass/warn/fail table generated automatically."
      },
      {
        "title": "Step 4: Review PR Check Summary & Fix Flagged Selectors",
        "ui": "GitHub Actions Step Summary & Exit Code",
        "narration": "Finally, read the markdown report posted directly to your GitHub Actions summary and fix any flagged elements before merging.",
        "guide": "Inspect the GitHub Step Summary table showing exact file names and failing rule IDs (`T1..T3`, `P1..P3`, `M1..M3`, `C1..C3`, `S1..S3`, `F1..F3`).",
        "result": "Every shipped web page meets baseline accessibility, motion, and typographic quality."
      }
    ],
    "guideControls": [
      {
        "name": "`uses: Kayforkind/design-health-action@main`",
        "desc": "Drop-in GitHub Action step requiring zero secrets or external API tokens."
      },
      {
        "name": "6 Quality Pillars (18 Rules)",
        "desc": "Typography (3), Palette (3), Motion (3), Content (3), Structure (3), Performance (3)."
      },
      {
        "name": "Local Node CLI Runner",
        "desc": "Can also be executed locally with Node.js before committing."
      }
    ],
    "guideProTips": [
      "Pair `design-health-action` with `design-gate` CLI to enforce structural HTML checks both locally in pre-commit hooks and in GitHub Actions.",
      "Always include a `@media (prefers-reduced-motion: reduce)` rule in your CSS—Rule M2 checks for this explicitly.",
      "Set explicit `width` and `height` (or CSS `aspect-ratio`) on all `<img>` and `<video>` elements to pass the Cumulative Layout Shift (CLS) check."
    ],
    "guideSpecs": "Repo: `Kayforkind/design-health-action` · Runtime: Node 20+ / GitHub Actions · Rules: 18 deterministic checks"
  },
  "skillslice": {
    "videoDuration": "37s",
    "guideSteps": [
      {
        "title": "Step 1: Browse the Skill Slice Catalog for Your Task",
        "ui": "Skill Slice Catalog & WORKS_VERIFIED.md",
        "narration": "To add a single verified workflow skill to your coding agent without bloating its context window, open the Skill Slice catalog and pick the exact skill you need.",
        "guide": "Browse `https://kayforkind.github.io/skill-slice/` or check `docs/WORKS_VERIFIED.md` in `Kayforkind/skill-slice` to pick the single `SKILL.md` that matches your task.",
        "result": "Avoids dumping 50+ unrelated skills into your agent's system prompt."
      },
      {
        "title": "Step 2: Copy One SKILL.md Folder or Run npx skills add --skill",
        "ui": "Single-Skill Installer Command",
        "narration": "Second, run npx skills add with the dash-dash-skill flag—or copy just that one folder into your workspace's dot-claude/skills directory.",
        "guide": "Run `npx skills add kazimrmerchant/skill-slice --skill <skill-name>` or copy `skills/<skill-name>/SKILL.md` into `.claude/skills/<skill-name>/`.",
        "result": "Only the single targeted skill is mounted in your workspace."
      },
      {
        "title": "Step 3: Progressive Disclosure (Index First, Full Skill on Demand)",
        "ui": "SKILL.md Frontmatter & Trigger Rules",
        "narration": "Third, your coding agent reads only the compact YAML frontmatter until your prompt matches that skill's domain, keeping token usage lean and focused.",
        "guide": "The agent indexes the 2-line YAML description at startup and loads the full `SKILL.md` body and `references/` only when triggered by your task.",
        "result": "90%+ reduction in idle context-window token overhead."
      },
      {
        "title": "Step 4: Audit Installed Skills with skills-registry",
        "ui": "SHA-256 Digest & Heuristic Verification",
        "narration": "Finally, verify your installed skill folders against WORKS_VERIFIED.md or build a local SHA-256 index using skills-registry.",
        "guide": "Check `docs/WORKS_VERIFIED.md` for Read-verified chairs or run `npx skills-registry` to generate SHA-256 digests of every skill in your repo.",
        "result": "Clean, auditable agent skill setup."
      }
    ],
    "guideControls": [
      {
        "name": "`npx skills add ... --skill <name>`",
        "desc": "Installs a single named skill folder rather than the entire repository."
      },
      {
        "name": "`docs/WORKS_VERIFIED.md`",
        "desc": "Lists the 12 core skills that have passed full Read-verification."
      },
      {
        "name": "`skills/<name>/SKILL.md`",
        "desc": "Self-contained procedural workflow instructions with YAML frontmatter."
      }
    ],
    "guideProTips": [
      "Install 1 to 3 skills per project workspace at most—fewer active skills produce sharper tool selection and lower token costs.",
      "Keep heavy reference tables in `skills/<name>/references/` so they are only read when specifically needed.",
      "Use `Kayforkind/skills-registry` to scan third-party `SKILL.md` files for prompt-injection or risky shell patterns before adopting them."
    ],
    "guideSpecs": "Repo: `Kayforkind/skill-slice` · Catalog: `kayforkind.github.io/skill-slice/` · Verified Core: 12 Read-verified chairs"
  },
  "liecatchers": {
    "videoDuration": "37s",
    "guideSteps": [
      {
        "title": "Step 1: Install or Run liecatchers via uvx After an Agent Turn",
        "ui": "CLI Command (uvx --from . liecatcher run)",
        "narration": "To verify whether a coding agent actually ran the tests and file edits it claimed, clone Kayforkind/liecatchers and run uvx liecatcher run inside your repo.",
        "guide": "Clone `https://github.com/Kayforkind/liecatchers` and run `uvx --from . liecatcher run` against the target project directory after an AI coding session.",
        "result": "Ten independent workspace sensors initialize across git, lockfiles, and artifacts."
      },
      {
        "title": "Step 2: Run All 10 Workspace Sensors Against Git & File Contracts",
        "ui": "10 Sensor Checks (Git Diff, Lockfiles, Binaries, Commands)",
        "narration": "Second, liecatchers executes ten sensors—checking git diff paths, lockfile consistency, declared command exit codes, truncation markers, and native binary tampering.",
        "guide": "The 10 sensors inspect: (1) declared command evidence, (2) git status/diff alignment, (3) lockfile drift, (4) placeholder/TODO truncation, (5) empty/zero-byte files, and (6–10) artifact & contract invariants.",
        "result": "Every discrepancy between the agent's claim and disk state is flagged."
      },
      {
        "title": "Step 3: Inspect the Emitted RECEIPT.json Evidence File",
        "ui": "RECEIPT.json Output",
        "narration": "Third, inspect the generated RECEIPT.json file, which records the exact SHA-256 hashes, sensor verdicts, and timestamps for every check.",
        "guide": "Open `RECEIPT.json` to review the per-sensor pass/fail breakdown, artifact SHA-256 digests, and execution metadata.",
        "result": "Machine-readable audit trail of what actually happened in the workspace."
      },
      {
        "title": "Step 4: Gate CI / PR Merges on Exit Code 0",
        "ui": "CI Gate & Signature Verification",
        "narration": "Finally, enforce exit code zero in your CI pipeline or pre-merge hook so unverified agent completion claims are caught automatically.",
        "guide": "Use `liecatcher run`'s exit code (`0` = all sensors pass, `1` = sensor failure) in CI or pair with `agent-receipts` for offline Ed25519 signature verification.",
        "result": "Zero 'trust me, tests passed' hallucinations slip into `main`."
      }
    ],
    "guideControls": [
      {
        "name": "`uvx --from . liecatcher run`",
        "desc": "Executes the 10-sensor post-run verification suite on Windows or POSIX."
      },
      {
        "name": "10 Workspace Sensors",
        "desc": "Checks git diffs, lockfiles, truncation markers, command logs, and file contracts."
      },
      {
        "name": "`RECEIPT.json`",
        "desc": "Structured JSON receipt containing sensor verdicts and artifact hashes."
      }
    ],
    "guideProTips": [
      "Run `liecatcher run` right before creating a pull request from an autonomous coding agent branch.",
      "Combine `liecatchers` with `Kayforkind/agent-receipts` when you need Ed25519 cryptographic signing of build/test receipts.",
      "Works on both Windows PowerShell and Linux/macOS shells."
    ],
    "guideSpecs": "Repo: `Kayforkind/liecatchers` · Runtime: Python 3.11+ / `uvx` · Output: `RECEIPT.json` + Exit Code Gate"
  },
  "bookguide": {
    "videoDuration": "37s",
    "guideSteps": [
      {
        "title": "Step 1: Install Book Guide MCP & Point at Your Local Books Folder",
        "ui": "MCP Server Config (book-guide-mcp)",
        "narration": "To turn your own technical books into cited agent playbooks, install Kayforkind/book-guide-mcp with uv and register the stdio server in your MCP client.",
        "guide": "Clone `https://github.com/Kayforkind/book-guide-mcp`, install via `uv sync`, and add the `book-guide-mcp` stdio command to your Claude Desktop, Cursor, or Antigravity MCP config.",
        "result": "Your coding agent gains local-first book indexing and citation tools."
      },
      {
        "title": "Step 2: Index Your User-Supplied PDF / EPUB / Markdown Books (L0–L1)",
        "ui": "L0 Library Indexer & Passage Locator",
        "narration": "Second, point the indexer at your local folder of textbooks or architecture guides. It builds chapter and section locators locally without uploading copyrighted text.",
        "guide": "Call the L0 library indexing tool on your local directory of books. The server builds a local searchable index with chapter, section, and page locators.",
        "result": "Fast local passage retrieval with exact source citations."
      },
      {
        "title": "Step 3: Generate Cited Engineering Playbooks & Checklists (L2–L3)",
        "ui": "Playbook & Checklist Generator",
        "narration": "Third, ask your agent to synthesize a step-by-step engineering playbook or review checklist from a specific chapter, complete with exact page citations.",
        "guide": "Invoke the L2/L3 playbook tools to turn a book chapter (e.g., distributed consensus or API design) into an actionable checklist where every rule cites its exact chapter/page locator.",
        "result": "Grounded engineering playbooks backed by real textbook citations."
      },
      {
        "title": "Step 4: Run Interactive Socratic or Avicenna Study Tutors (L4)",
        "ui": "L4 Socratic & Avicenna Tutor Modes",
        "narration": "Finally, use the L4 Socratic or Avicenna tutor modes to test your understanding through guided questions anchored to the text.",
        "guide": "Start an L4 tutor session (`01-socratic-tutor` or `02-avicenna-framework`) to walk through complex chapters interactively with cited feedback.",
        "result": "Deep technical mastery grounded in your own local library."
      }
    ],
    "guideControls": [
      {
        "name": "L0–L1 Library Index & Search",
        "desc": "Indexes local user-provided books and retrieves passages with exact chapter/page locators."
      },
      {
        "name": "L2–L3 Playbook & Checklist Builder",
        "desc": "Transforms chapters into cited engineering checklists and decision trees."
      },
      {
        "name": "L4 Socratic & Avicenna Tutors",
        "desc": "Interactive guided study modes over MCP stdio."
      }
    ],
    "guideProTips": [
      "Use Book Guide MCP during code reviews by indexing your team's architecture books and asking the agent to audit a PR against specific cited chapters.",
      "All indexing runs locally on your machine—no copyrighted book files are bundled in the repo or uploaded to third-party servers.",
      "See `docs/examples/01-socratic-tutor.md` and `02-avicenna-framework.md` in the repository for ready-to-run prompts."
    ],
    "guideSpecs": "Repo: `Kayforkind/book-guide-mcp` · Protocol: Model Context Protocol (MCP stdio) · Runtime: Python / `uv`"
  },
  "datainsights": {
    "videoDuration": "38s",
    "guideSteps": [
      {
        "title": "Step 1: Clone Data Insights & Start the Local Node Server",
        "ui": "Terminal (npm install && npm run dev)",
        "narration": "To run your own technology and security intelligence portal, clone Kayforkind/data-insights, run npm install and npm run dev, and open localhost port 3000.",
        "guide": "Clone `https://github.com/Kayforkind/data-insights`, run `npm install && npm run dev`, and open the local web portal (or visit the live edge deployment).",
        "result": "The signal aggregation engine and web portal start locally."
      },
      {
        "title": "Step 2: Ingest & Normalize Public Tech, Security & Research Feeds",
        "ui": "Feed Normalizer & Momentum Scorer",
        "narration": "Second, the collector fetches public RSS and API feeds across technology, security advisories, and research preprints, deduplicating stories and scoring topic momentum.",
        "guide": "Trigger feed ingestion or let the scheduled collector normalize headlines across tech news, CVE advisories, arXiv papers, and startup launches.",
        "result": "Deduplicated signal river with source-health telemetry."
      },
      {
        "title": "Step 3: Read the Daily 5W1H Brief & Topic Momentum Charts",
        "ui": "Daily 5W1H Brief View",
        "narration": "Third, open the Daily 5W1H Brief view to read structured Who, What, When, Where, Why, and How syntheses for the top stories of the day.",
        "guide": "Switch to the **Daily 5W1H Brief** tab to review structured executive summaries (`Who / What / When / Where / Why / How`) and rising keyword velocity.",
        "result": "High-signal daily briefing without algorithmic social feed noise."
      },
      {
        "title": "Step 4: Export Print-Ready Weekly PDF Briefs or Query the JSON API",
        "ui": "Weekly PDF Export & /api/briefs JSON Endpoints",
        "narration": "Finally, export the Weekly Synthesis report as a print-ready PDF, or query the local JSON endpoints directly from your AI agents.",
        "guide": "Click **Export Weekly PDF** for a clean executive briefing document, or query `/api/briefs/daily` from your scripts and agents.",
        "result": "Self-hosted intelligence pipeline with PDF and JSON outputs."
      }
    ],
    "guideControls": [
      {
        "name": "Signal River Portal",
        "desc": "Real-time categorized stream of tech, security, and research items."
      },
      {
        "name": "Daily 5W1H Synthesizer",
        "desc": "Structures complex news events into Who, What, When, Where, Why, and How."
      },
      {
        "name": "Weekly Executive Report & JSON API",
        "desc": "Print-formatted weekly synthesis and machine-readable REST endpoints."
      }
    ],
    "guideProTips": [
      "Customize the feed list in the configuration to track your specific industry vertical, competitor changelogs, or security advisories.",
      "Use the built-in source availability monitor to spot broken or rate-limited RSS feeds automatically.",
      "Agents can poll the JSON endpoints to include daily industry context in morning briefings."
    ],
    "guideSpecs": "Repo: `Kayforkind/data-insights` · Runtime: Node.js · Outputs: Web Portal, 5W1H Daily Brief, Weekly PDF, JSON API"
  },
  "ironaxe": {
    "videoDuration": "41s",
    "guideSteps": [
      {
        "title": "Step 1: Clone Iron Axe: Legacy & Open in Godot Engine 4.3+",
        "ui": "Godot 4 Project Manager (project.godot)",
        "narration": "To play or modify Iron Axe Legacy, clone Kayforkind/iron-axe-legacy, open project.godot in Godot Engine 4.3 or newer, and press F5 to launch the game.",
        "guide": "Clone `https://github.com/Kayforkind/iron-axe-legacy`, open `project.godot` in **Godot Engine 4.3+**, and press `F5` (Run Project).",
        "result": "The 60 FPS 2.5D side-scrolling beat-'em-up prototype launches immediately."
      },
      {
        "title": "Step 2: Pick Your Fighter & Master Elevation-Lane Movement",
        "ui": "Character Select & 2.5D Depth Lanes",
        "narration": "Second, choose from the four original heroes—such as Kaelen Ironhand or Seraphina Vance—and move across the 2.5D depth lanes using WASD or a gamepad.",
        "guide": "Select one of the 4 original characters (Kaelen, Seraphina, Brann, Nyx) and navigate the 2.5D combat arena with keyboard (`WASD` / Arrow keys) or gamepad.",
        "result": "Responsive 2.5D lane positioning and elevation jumping."
      },
      {
        "title": "Step 3: Execute Light/Heavy Combo Chains, Grabs & Throws",
        "ui": "Combat State Machine (Attack, Grab, Throw, Magic)",
        "narration": "Third, chain light and heavy attacks into multi-hit combos, grab stunned enemies to throw them across the stage, and trigger screen-clearing team magic.",
        "guide": "Use Attack, Jump-Attack, Dash-Attack, Grab/Throw, and Special Magic inputs. Notice the crisp hitstop frames, damage popups, and camera shake on heavy hits.",
        "result": "Arcade-authentic Golden Axe / Streets of Rage style combat feel."
      },
      {
        "title": "Step 4: Customize GDScript Combat Tunables & Export Builds",
        "ui": "GDScript State Machine & Godot Export",
        "narration": "Finally, inspect the modular GDScript state machines and hitbox resources in the editor to add new enemies, stages, or export a desktop or WebGL build.",
        "guide": "Open the `scripts/` and `scenes/` folders in Godot to tune hitboxes, knockback curves, enemy AI waves, or export to Windows, Linux, macOS, or Web.",
        "result": "100% original, MIT-licensed Godot 4 beat-'em-up codebase."
      }
    ],
    "guideControls": [
      {
        "name": "Movement (`WASD` / D-Pad / Left Stick)",
        "desc": "8-way movement across 2.5D depth lanes and elevation platforms."
      },
      {
        "name": "Combat Actions (Attack, Jump, Dash, Grab, Magic)",
        "desc": "Full state-machine combo trees, grapple throws, and elemental magic."
      },
      {
        "name": "Godot 4.3+ Editor (`project.godot`)",
        "desc": "Clean GDScript architecture with zero proprietary asset dependencies."
      }
    ],
    "guideProTips": [
      "Use vertical lane movement (`Up`/`Down`) to avoid linear enemy charges before counter-attacking with a dash-strike.",
      "All sprites, lore, and GDScript combat controllers are 100% original and MIT-licensed—ideal as a starter template for your own 2.5D action game.",
      "Adjust hitstop duration and screen-shake intensity in the combat controller script to tune game-feel."
    ],
    "guideSpecs": "Repo: `Kayforkind/iron-axe-legacy` · Engine: Godot 4.3+ (GDScript) · License: MIT (100% original IP)"
  }
}

MASTER_CHAPTERS: list[dict] = [
  {
    "tid": "exif",
    "name": "Photo Privacy Kit",
    "start": 0,
    "tagline": "Strip GPS, camera model and timestamps before posting"
  },
  {
    "tid": "shrink",
    "name": "Image Shrinker",
    "start": 43,
    "tagline": "Hit “max 2 MB” portal limits without TinyPNG"
  },
  {
    "tid": "scan",
    "name": "Scan & Screenshot Cleaner",
    "start": 79,
    "tagline": "Phone photos of documents → clean, straight PDFs"
  },
  {
    "tid": "sign",
    "name": "Local E-Sign Pad",
    "start": 112,
    "tagline": "Sign this lease tonight — not DocuSign"
  },
  {
    "tid": "ocr",
    "name": "Receipt OCR → CSV",
    "start": 150,
    "tagline": "Read totals off receipt photos, export for expenses"
  },
  {
    "tid": "qr",
    "name": "QR Studio",
    "start": 193,
    "tagline": "Generate QR codes and decode QR images — no site sees them"
  },
  {
    "tid": "invoice",
    "name": "Invoice / Quote Generator",
    "start": 231,
    "tagline": "One-person shops: hours in, clean PDF out"
  },
  {
    "tid": "pdfstudio",
    "name": "PDF Studio",
    "start": 267,
    "tagline": "Edit the text inside your PDF — private, free, open source"
  },
  {
    "tid": "reimagine",
    "name": "Reimagine",
    "start": 311,
    "tagline": "Redesign any HTML page from its own content"
  }
]

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
  gap: 8px;
  max-height: 430px;
  overflow-y: auto;
  padding-right: 4px;
}
.nlm-chap {
  background: rgba(9, 13, 22, 0.85);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px 14px;
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
  font-size: 11px;
  font-family: ui-monospace, Consolas, monospace;
  color: var(--cyan);
  margin-bottom: 3px;
}
.nlm-chap b { display: block; font-size: 13.5px; margin-bottom: 2px; }
.nlm-chap span { font-size: 12px; color: var(--muted); }
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
  background: rgba(5, 7, 13, 0.88);
  border: 1px solid rgba(45, 212, 191, 0.4);
  color: var(--cyan);
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
  margin: 0 0 12px;
  color: var(--muted);
  font-size: 0.92rem;
}
.card-steps-pill {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 12px;
}
.card-steps-pill span {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 10.5px;
  background: rgba(45, 212, 191, 0.08);
  border: 1px solid rgba(45, 212, 191, 0.25);
  color: #cbd5e1;
  padding: 2px 7px;
  border-radius: 5px;
}
.card-steps-pill span b { color: var(--cyan); }
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
.manual-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-top: 14px;
}
.manual-step {
  background: rgba(7, 10, 18, 0.92);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 16px 18px;
}
.manual-step-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
.manual-badge {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 11px;
  font-weight: 700;
  color: #041019;
  background: var(--cyan);
  padding: 2px 8px;
  border-radius: 6px;
}
.manual-ui {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 11px;
  color: var(--cyan);
  background: rgba(45, 212, 191, 0.1);
  border: 1px solid rgba(45, 212, 191, 0.3);
  padding: 2px 8px;
  border-radius: 6px;
}
.manual-step h3 {
  margin: 0 0 6px;
  font-size: 15px;
  color: var(--fg);
}
.manual-step p {
  margin: 0 0 10px;
  font-size: 13.5px;
  color: #cbd5e1;
}
.manual-res {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 11.5px;
  color: var(--ok);
  padding-top: 8px;
  border-top: 1px dashed var(--line);
}
.ctrl-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
}
.ctrl-table th, .ctrl-table td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
.ctrl-table th {
  font-family: ui-monospace, Consolas, monospace;
  font-size: 11px;
  text-transform: uppercase;
  color: var(--muted);
}
.ctrl-table code {
  font-family: ui-monospace, Consolas, monospace;
  color: var(--cyan);
  background: rgba(45, 212, 191, 0.1);
  padding: 2px 6px;
  border-radius: 5px;
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
  .nlm-grid, .detail-grid, .step-cards, .manual-grid { grid-template-columns: 1fr; }
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
        g = GUIDE_DATA.get(tid, {})
        dur = html.escape(g.get("videoDuration", "30s"))
        gsteps = g.get("guideSteps", [])
        step_pills = []
        for idx, st in enumerate(gsteps[:4], 1):
            short_t = html.escape(st.get("title", f"Step {idx}").split("&")[0].strip()[:26])
            step_pills.append(f"<span><b>{idx}.</b> {short_t}</span>")
        pills_html = "".join(step_pills)

        cards.append(
            f'      <a class="card" href="/apps/{slug}/" data-cat="{cat}" data-search="{name.lower()} {summary.lower()} {cat_label.lower()}">\n'
            f'        <div class="card-media">\n'
            f'          <video src="/tools/videos/{tid}.mp4" poster="/tools/shots/{tid}.jpg" muted loop playsinline preload="none" data-aspect="horizontal"></video>\n'
            f'          <span class="card-badge">{cat_label}</span>\n'
            f'          <span class="card-play-hint">🔊 {dur} Narrated Guide</span>\n'
            f'        </div>\n'
            f'        <div class="card-body">\n'
            f'          <h2>{name}</h2>\n'
            f'          <p>{summary}</p>\n'
            f'          <div class="card-steps-pill">{pills_html}</div>\n'
            f'          <div class="io-box">\n'
            f'            <div class="io-row"><span class="io-tag in">INPUT</span><span class="io-text">{in_ex}</span></div>\n'
            f'            <div class="io-row"><span class="io-tag out">OUTPUT</span><span class="io-text">{out_ex}</span></div>\n'
            f'            <div class="io-code">{scode}</div>\n'
            f'          </div>\n'
            f'          <div class="caveat">Caveat: {caveat}</div>\n'
            f'          <div class="card-foot"><span>Open Narrated Video &amp; 4-Step User Guide</span><span>→</span></div>\n'
            f'        </div>\n'
            f'      </a>'
        )
    cards_html = "\n".join(cards)

    chap_btns = []
    for idx, ch in enumerate(MASTER_CHAPTERS, 1):
        sec = int(ch["start"])
        mm = sec // 60
        ss = sec % 60
        tstr = f"{mm:02d}:{ss:02d}"
        chap_btns.append(
            f'          <button type="button" class="nlm-chap" data-seek="{sec}">\n'
            f'            <div class="ch-top"><span>TOOL {idx:02d} · LIVE WALKTHROUGH</span><span>{tstr}</span></div>\n'
            f'            <b>{html.escape(ch["name"])} — 4-Step Usage Guide</b>\n'
            f'            <span>{html.escape(ch["tagline"])}</span>\n'
            f'          </button>'
        )
    chap_html = "\n".join(chap_btns)

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>NavigatorLabs Product library</title>
  <meta name="description" content="NavigatorLabs open-source product library: 16 apps across browser tools, PDF editing, HTML redesign, MCP servers, and developer utilities — with narrated step-by-step usage videos and complete user guides.">
  <link rel="stylesheet" href="/apps/style.css">
</head>
<body>
  <div class="aurora-bg"></div>
  <div class="announce-bar">
    <b>✦ LOCAL-FIRST SOFTWARE STUDIO</b> · 16 Repositories · 24 Browser &amp; Agent Tools · Narrated Live-UI Step-by-Step Usage Guides
    <a href="https://navigatorslab.com/tools/">Explore all 24 browser tools &amp; guides →</a>
  </div>
  <header class="site-nav">
    <div class="site-nav-inner">
      <a class="brand-logo" href="/"><span class="dot"></span> NavigatorLabs <span>LOCAL-FIRST</span></a>
      <nav class="nav-links" aria-label="Primary Navigation">
        <a href="#overview">🎬 Hands-On Video Guide</a>
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
      <h1>Software that stays on your machine.<br><span class="grad">With narrated usage tutorials &amp; step-by-step user guides.</span></h1>
      <p class="lede">
        Every tool in the NavigatorLabs library processes your files locally in your browser tab or local CLI — complete with spoken step-by-step screen walkthroughs, UI control references, and verified output examples.
      </p>
      <div class="hero-actions">
        <a class="btn primary" href="#overview">▶ Watch Hands-On Usage Guide</a>
        <a class="btn" href="https://navigatorslab.com/tools/">🧭 Open 24 Browser Tools &amp; Guides</a>
        <a class="btn" href="https://navigatorslab.com/pdf-studio/">📜 Launch PDF Studio</a>
        <a class="btn" href="https://navigatorslab.com/reimagine/">🎨 Launch Reimagine</a>
      </div>

      <div class="proof-strip">
        <div class="proof-box"><b>16 apps</b><span>Dedicated repositories with narrated tutorials &amp; user guides</span></div>
        <div class="proof-box"><b>24 tools</b><span>In-browser utilities, flagships, MCP servers &amp; CI gates</span></div>
        <div class="proof-box"><b>0 uploads</b><span>Enforced by Content-Security-Policy default-src 'none'</span></div>
        <div class="proof-box"><b>39 / 39 E2E</b><span>Real browser Playwright assertions on every output file</span></div>
      </div>
    </section>

    <section id="overview" class="nlm-section" aria-label="Hands-On Narrated Video Usage Guide">
      <div class="nlm-header">
        <div>
          <span class="nlm-badge">🎬 Narrated Live-UI Step-by-Step Usage Guide</span>
          <h2 style="margin:8px 0 4px;font-size:1.5rem">Watch How to Use Every Core App — Step by Step in the Live Browser UI</h2>
          <p style="margin:0;color:var(--muted);font-size:0.95rem">Full spoken walkthrough showing real files dropped in, UI controls configured, and verified outputs saved across 9 flagship &amp; core apps. Click any chapter on the right to jump straight to that tool.</p>
        </div>
        <a class="btn" href="/tools/videos/notebooklm-overview.mp4" download>⬇ Download Full Guide MP4</a>
      </div>
      <div class="nlm-grid">
        <div class="video-frame">
          <video id="nlmVideo" controls playsinline preload="metadata" poster="/tools/shots/notebooklm-overview.jpg" data-aspect="horizontal">
            <source src="/tools/videos/notebooklm-overview.mp4" type="video/mp4">
          </video>
        </div>
        <div class="nlm-chapters">
{chap_html}
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
        <input type="search" id="appSearch" class="search-box" placeholder="Search 16 apps, guides, inputs or outputs…" aria-label="Search applications">
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
      document.querySelectorAll('.card').forEach(function (card) {{
        var vid = card.querySelector('video');
        if (!vid) return;
        card.addEventListener('mouseenter', function () {{ vid.play().catch(function(){{}}); }});
        card.addEventListener('mouseleave', function () {{ vid.pause(); }});
        card.addEventListener('focus', function () {{ vid.play().catch(function(){{}}); }});
        card.addEventListener('blur', function () {{ vid.pause(); }});
      }});
      var nlm = document.getElementById('nlmVideo');
      document.querySelectorAll('.nlm-chap').forEach(function (btn) {{
        btn.addEventListener('click', function () {{
          if (!nlm) return;
          nlm.currentTime = Number(btn.getAttribute('data-seek') || 0);
          nlm.play().catch(function(){{}});
        }});
      }});
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

    g = GUIDE_DATA.get(tid, {})
    dur = html.escape(g.get("videoDuration", "30s"))
    gsteps = g.get("guideSteps", [])
    gctrls = g.get("guideControls", [])
    gtips = g.get("guideProTips", [])

    manual_cards = []
    for idx, st in enumerate(gsteps, 1):
        st_t = html.escape(st.get("title", f"Step {idx}"))
        st_ui = html.escape(st.get("uiTarget", "Browser UI"))
        st_in = html.escape(st.get("instruction", ""))
        st_rs = html.escape(st.get("result", ""))
        manual_cards.append(
            f'        <div class="manual-step">\n'
            f'          <div class="manual-step-head"><span class="manual-badge">STEP 0{idx}</span><span class="manual-ui">UI Target: {st_ui}</span></div>\n'
            f'          <h3>{st_t}</h3>\n'
            f'          <p>{st_in}</p>\n'
            f'          <div class="manual-res">✓ Expected Result: {st_rs}</div>\n'
            f'        </div>'
        )
    manual_html = "\n".join(manual_cards)

    ctrl_rows = []
    for c in gctrls:
        ctrl_rows.append(
            f'          <tr><td><code>{html.escape(c.get("control",""))}</code></td><td>{html.escape(c.get("purpose",""))}</td></tr>'
        )
    ctrl_html = "\n".join(ctrl_rows)

    tip_rows = []
    for tip in gtips:
        tip_rows.append(f'          <li style="margin:6px 0;color:#cbd5e1">{html.escape(tip)}</li>')
    tip_html = "\n".join(tip_rows)

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
  <title>{name} — Step-by-Step User Guide &amp; Video Tutorial — NavigatorLabs</title>
  <meta name="description" content="{summary}">
  <link rel="stylesheet" href="/apps/style.css">
</head>
<body>
  <div class="aurora-bg"></div>
  <header class="site-nav">
    <div class="site-nav-inner">
      <a class="brand-logo" href="/"><span class="dot"></span> NavigatorLabs <span>USER GUIDE &amp; DEMO</span></a>
      <nav class="nav-links">
        <a href="/">← All 16 apps</a>
        <a href="#user-guide">📖 4-Step User Guide</a>
        <a href="/#overview">🎬 Master Video Guide</a>
        <a href="https://navigatorslab.com/tools/">24 Browser Tools</a>
        <a href="{repo_url}">GitHub Repo</a>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <div class="eyebrow-pill">{cat_label} · Narrated Video Tutorial &amp; Complete User Guide</div>
    <h1>{name}</h1>
    <p class="lede" style="margin:0 0 20px;text-align:left;max-width:880px">{summary}</p>

    <div class="links">
      {live_btn}
      <a href="#user-guide">📖 Read 4-Step User Guide</a>
      <a href="{repo_url}">Source repository ({html.escape(a['repo'])})</a>
      <a href="/tools/detail.html?id={tid}">Interactive Tool Spec &amp; Deep-Links</a>
    </div>

    <div class="detail-grid">
      <div>
        <div class="panel-box" style="padding:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding:0 6px;flex-wrap:wrap;gap:6px">
            <b style="font-size:13px;color:var(--cyan);font-family:ui-monospace,Consolas,monospace">🔊 NARRATED STEP-BY-STEP USAGE TUTORIAL ({dur})</b>
            <span style="font-size:12px;color:var(--muted)">Click Play for spoken commentary &amp; live UI walkthrough</span>
          </div>
          <div class="video-frame">
            <video controls playsinline preload="metadata" poster="/tools/shots/{tid}.jpg" data-aspect="horizontal">
              <source src="/tools/videos/{tid}.mp4" type="video/mp4">
            </video>
          </div>
        </div>

        <div class="panel-box" style="padding:14px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;padding:0 6px">
            <b style="font-size:13px;color:var(--sky);font-family:ui-monospace,Consolas,monospace">📸 ANNOTATED UI CONTROL CALLOUT PREVIEW</b>
            <a href="/tools/shots/{tid}.jpg" target="_blank" style="font-size:12px">Open full image ↗</a>
          </div>
          <div class="video-frame">
            <img src="/tools/shots/{tid}.jpg" alt="{name} annotated UI screenshot and step callout" loading="lazy">
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

    <div id="user-guide" class="panel-box">
      <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:8px">
        <h2>📖 Step-by-Step User Guide: How to Use {name}</h2>
        <span style="font-family:ui-monospace,Consolas,monospace;font-size:12px;color:var(--cyan)">4-Step Operational Walkthrough</span>
      </div>
      <div class="manual-grid">
{manual_html}
      </div>
    </div>

    <div class="detail-grid" style="margin-top:20px">
      <div class="panel-box" style="margin-bottom:0">
        <h2>🎛️ UI Controls, Shortcuts &amp; Parameters Reference</h2>
        <table class="ctrl-table">
          <thead><tr><th>Control / Parameter</th><th>How It Works</th></tr></thead>
          <tbody>
{ctrl_html}
          </tbody>
        </table>
      </div>
      <div class="panel-box" style="margin-bottom:0">
        <h2>💡 Pro Tips &amp; Real-World Workflows</h2>
        <ul style="margin:8px 0 0;padding-left:20px;line-height:1.65">
{tip_html}
        </ul>
      </div>
    </div>

    <div class="panel-box" style="margin-top:20px">
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
