#!/usr/bin/env node
/**
 * Claim gate — this site may only publish numbers that are currently true.
 *
 * The landing page and the one-pager make countable claims (stars, downloads,
 * Scorecard, tests, releases, merged PRs, corpus size, diversity, ...). Those
 * numbers drift the moment someone pushes to reimagine-it, so "and keep them
 * true" is only honest if a machine re-measures them.
 *
 * This gate reads the published numbers out of the copy, measures each one
 * from its real source, and fails when the two disagree:
 *
 *   stars          → api.github.com/repos/Kayforkind/reimagine-it
 *   npm dl / week  → api.npmjs.org/downloads/point/last-week/reimagine-it
 *   Scorecard      → api.securityscorecards.dev (OpenSSF)
 *   releases/3 mo  → GitHub releases, published within the last 92 days
 *   merged PRs     → GitHub search (is:pr is:merged)
 *   tests          → `npm test` in reimagine-it, summed from its own report
 *   168-file corpus, 19 rules, 17 artifacts
 *                  → parsed from that same test run (the guards that own them)
 *   96.8% / 17.9%  → node scripts/benchmark-tokens.js (real measurement)
 *   17 directions  → reimagine-it's src/generate.js TOKENS
 *   15 utilities   → NavigatorsLab-Tools/public/tools.json
 *   6 gov proofs   → examples/public-sources/* in reimagine-it
 *
 * Usage:
 *   node scripts/verify-claims.cjs              # gate (exit 1 on any drift)
 *   node scripts/verify-claims.cjs --fix        # rewrite the copy to reality
 *   node scripts/verify-claims.cjs --no-network # skip API claims (offline)
 *
 * Claims that cannot be measured from a machine are listed under "not gated"
 * with the reason — they are never silently ignored.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const ROOT = path.resolve(__dirname, '..');
const FIX = process.argv.includes('--fix');
const OFFLINE = process.argv.includes('--no-network');
const REPO_SLUG = 'Kayforkind/reimagine-it';
const PKG = 'reimagine-it';
const RELEASE_WINDOW_DAYS = 92; // "releases / 3 mo"

const PROBLEMS = [];
const FIXES = [];
const SKIPPED = [];
const NUM_WORDS = {
  one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8,
  nine: 9, ten: 10, eleven: 11, twelve: 12, thirteen: 13, fourteen: 14,
  fifteen: 15, sixteen: 16, seventeen: 17, eighteen: 18, nineteen: 19,
  twenty: 20,
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ── the reimagine-it working copy (the source of most numbers) ──────────────

function locateReimagine() {
  const candidates = [
    process.env.REIMAGINE_DIR,
    path.resolve(ROOT, '..', 'reimagine-it'), // local sibling clone
    path.resolve(ROOT, '.cache', 'reimagine-it'),
  ].filter(Boolean);
  for (const dir of candidates) {
    if (fs.existsSync(path.join(dir, 'scripts', 'test.js'))) return dir;
  }
  const dest = path.resolve(ROOT, '.cache', 'reimagine-it');
  console.log(`· cloning ${REPO_SLUG} → .cache/reimagine-it (shallow, main)…`);
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  const clone = spawnSync(
    'git',
    ['clone', '--depth', '1', '--quiet', `https://github.com/${REPO_SLUG}.git`, dest],
    { stdio: 'inherit' }
  );
  if (clone.status !== 0) {
    die(`could not clone ${REPO_SLUG} — the numbers cannot be measured without it`);
  }
  return dest;
}

function die(msg) {
  console.error(`\nFAIL: ${msg}`);
  process.exit(1);
}

function run(cmd, args, cwd) {
  const r = spawnSync(cmd, args, { cwd, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
  return { code: r.status, out: `${r.stdout || ''}${r.stderr || ''}` };
}

function gitOutput(args, cwd) {
  const r = spawnSync('git', args, { cwd, encoding: 'utf8' });
  return r.status === 0 ? r.stdout.trim() : '';
}

// ── live sources ───────────────────────────────────────────────────────────

async function api(url) {
  const headers = {
    'user-agent': 'navigators-site-claim-gate',
    accept: 'application/vnd.github+json',
  };
  if (process.env.GITHUB_TOKEN) headers.authorization = `Bearer ${process.env.GITHUB_TOKEN}`;
  let lastErr;
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const res = await fetch(url, { headers, signal: AbortSignal.timeout(20000) });
      if (!res.ok) throw new Error(`HTTP ${res.status} ${res.statusText}`);
      return await res.json();
    } catch (e) {
      lastErr = e;
      if (attempt < 3) await sleep(attempt * 1500);
    }
  }
  throw new Error(`${url} → ${lastErr.message}`);
}

async function measureApis() {
  const out = {};
  const jobs = [
    ['repo', `https://api.github.com/repos/${REPO_SLUG}`],
    ['releases', `https://api.github.com/repos/${REPO_SLUG}/releases?per_page=100`],
    [
      'search',
      `https://api.github.com/search/issues?q=${encodeURIComponent(
        `repo:${REPO_SLUG} is:pr is:merged`
      )}&per_page=1`,
    ],
    ['score', `https://api.securityscorecards.dev/projects/github.com/${REPO_SLUG}`],
    ['npm', `https://api.npmjs.org/downloads/point/last-week/${PKG}`],
  ];
  for (const [key, url] of jobs) {
    try {
      out[key] = await api(url);
    } catch (e) {
      out[key] = { __error: e.message };
    }
  }
  return out;
}

async function toolsCatalog() {
  const local = path.resolve(ROOT, '..', 'NavigatorsLab-Tools', 'public', 'tools.json');
  if (fs.existsSync(local)) {
    return { list: JSON.parse(fs.readFileSync(local, 'utf8')), from: 'sibling clone' };
  }
  const url = 'https://raw.githubusercontent.com/Kayforkind/NavigatorsLab-Tools/main/public/tools.json';
  const res = await fetch(url, { signal: AbortSignal.timeout(20000) });
  if (!res.ok) throw new Error(`${url} → HTTP ${res.status}`);
  return { list: await res.json(), from: 'raw.githubusercontent.com' };
}

// ── gather every measurement once ──────────────────────────────────────────

async function measure() {
  const REPO = locateReimagine();
  const head = gitOutput(['rev-parse', '--short', 'HEAD'], REPO);
  const branch = gitOutput(['rev-parse', '--abbrev-ref', 'HEAD'], REPO);
  if (branch && branch !== 'main') {
    console.log(
      `· note: measuring ${REPO} at ${branch}@${head} — CI measures main, so a\n` +
        `  branch-local number is not a published number.`
    );
  }

  const pkg = JSON.parse(fs.readFileSync(path.join(REPO, 'package.json'), 'utf8'));

  if (!fs.existsSync(path.join(REPO, 'node_modules', 'fast-check'))) {
    die(
      `reimagine-it has no devDependencies installed — its own suite needs\n` +
        `  fast-check (extractor property tests). Run:\n\n` +
        `    cd ${REPO} && npm ci --ignore-scripts --no-audit --no-fund\n\n` +
        `  without it the reported test count would be lower than the published one.`
    );
  }

  const test = run(process.execPath, ['scripts/test.js'], REPO);
  const testOut = test.out;
  if (test.code !== 0 || !/ALL TESTS PASSED/.test(testOut)) {
    die(
      `reimagine-it's own suite failed here, so its numbers cannot be trusted.\n` +
        `  Fix that first: cd ${REPO} && npm test\n\n` +
        testOut.split('\n').slice(-25).join('\n')
    );
  }

  // 160 tests = the sum of every section that reports a pass count.
  const sectionCounts = [...testOut.matchAll(/^\s*(\d+) passed, 0 failed\s*$/gm)].map((m) =>
    Number(m[1])
  );
  const tests = sectionCounts.reduce((a, b) => a + b, 0);

  // The parity line is the corpus + rule registry (the guard that owns them).
  const parity = testOut.match(/Design Health parity — (\d+) HTML files, (\d+) rules/);
  if (!parity) {
    die(
      `the "Design Health parity — N HTML files, M rules" line is missing from the\n` +
        `  test output. That line is the source of truth for the corpus size and the\n` +
        `  rule count, and it only prints when python is available (npm test skips the\n` +
        `  audit parity + gold smoke demo without it). Install python, or set up the\n` +
        `  same two interpreters reimagine-it's own gate uses.`
    );
  }
  const [corpusFiles, rulesFromRun] = [Number(parity[1]), Number(parity[2])];

  // Independent cross-check: the rule registry as written in audit.py.
  const auditPy = fs.readFileSync(path.join(REPO, 'scripts', 'audit.py'), 'utf8');
  const rulesInRegistry = new Set(
    [...auditPy.matchAll(/"code": "([A-Z]{3,4}-\d{2})"/g)].map((m) => m[1])
  ).size;
  if (rulesInRegistry && rulesInRegistry !== rulesFromRun) {
    PROBLEMS.push({
      label: 'rule registry',
      detail: `the parity guard ran ${rulesFromRun} rules but scripts/audit.py registers ${rulesInRegistry}`,
      source: true,
    });
  }

  const repro = testOut.match(/reproduction guard OK — (\d+) artifacts regenerate byte-identically/);
  if (!repro) die('the reproduction guard did not report an artifact count in the test output');
  const artifacts = Number(repro[1]);

  const bench = run(process.execPath, ['scripts/benchmark-tokens.js'], REPO);
  const benchLine = bench.out.match(
    /rows=(\d+) size-diversity=([\d.]+)% class-diversity=([\d.]+)%/
  );
  if (!benchLine) die('scripts/benchmark-tokens.js did not print its diversity summary line');
  const [, benchRows, sizeDiversity, classDiversity] = benchLine;
  const usabilityRows = [...benchOut(bench.out)].map((m) => m[1]);
  const allPerfect = usabilityRows.length > 0 && usabilityRows.every((u) => u === '100/100');

  const { TOKENS } = require(path.join(REPO, 'src', 'generate.js'));
  const directions = TOKENS.length;

  const govPages = fs
    .readdirSync(path.join(REPO, 'examples', 'public-sources'), { withFileTypes: true })
    .filter((d) => d.isDirectory()).length;

  // tools.json: the browser utilities are the entries with a pretty URL slug
  // published as a per-tool mirror repo (PDF Studio and the CLI are their own
  // products, and they carry no `pretty`).
  let utilities = null;
  let utilitiesFrom = '';
  try {
    const { list, from } = await toolsCatalog();
    utilitiesFrom = from;
    utilities = list.filter(
      (t) => t.pretty && /^Kayforkind\/NavigatorsLab-/.test(String(t.repo || '').replace('https://github.com/', ''))
    ).length;
    const fleet = path.resolve(ROOT, '..');
    if (fs.existsSync(fleet)) {
      const mirrors = fs
        .readdirSync(fleet, { withFileTypes: true })
        .filter(
          (d) =>
            d.isDirectory() &&
            /^NavigatorsLab-/.test(d.name) &&
            !['NavigatorsLab-Tools', 'NavigatorsLab-PDF-Studio'].includes(d.name)
        ).length;
      if (mirrors && mirrors !== utilities) {
        PROBLEMS.push({
          label: 'utilities',
          detail: `tools.json implies ${utilities} browser utilities but the fleet has ${mirrors} tool mirrors`,
          source: true,
        });
      }
    }
  } catch (e) {
    PROBLEMS.push({ label: 'utilities', detail: `could not read the Tools catalog (${e.message})`, source: true });
  }

  let apis = {};
  if (OFFLINE) {
    SKIPPED.push('stars, npm downloads, Scorecard, releases, merged PRs (--no-network)');
  } else {
    apis = await measureApis();
  }

  const num = (key, read) => {
    if (OFFLINE) return null;
    const payload = apis[key];
    if (!payload || payload.__error) {
      PROBLEMS.push({
        label: key,
        detail: `live source unreachable: ${payload ? payload.__error : 'not fetched'}`,
        source: true,
      });
      return null;
    }
    const value = read(payload);
    if (value === undefined || value === null || Number.isNaN(value)) {
      PROBLEMS.push({ label: key, detail: 'live source answered in an unexpected shape', source: true });
      return null;
    }
    return String(value);
  };

  const stars = num('repo', (r) => r.stargazers_count);
  const npmWeekly = num('npm', (d) => d.downloads);
  const score = num('score', (s) => Number(s.score).toFixed(1));
  const mergedPRs = num('search', (s) => s.total_count);
  const releases = num('releases', (list) =>
    list.filter((r) => Date.now() - Date.parse(r.published_at || r.created_at) <= RELEASE_WINDOW_DAYS * 864e5).length
  );

  // The month/year behind "**v2.15.0 (Sep 2026)**" comes from the release itself.
  let releaseMonth = null;
  if (!OFFLINE && apis.releases && !apis.releases.__error) {
    const tag = apis.releases.find(
      (r) => String(r.tag_name || '').replace(/^v/, '') === pkg.version
    );
    if (tag) {
      const d = new Date(tag.published_at);
      releaseMonth = `${d.toLocaleString('en-US', { month: 'short', timeZone: 'UTC' })} ${d.getUTCFullYear()}`;
    } else {
      PROBLEMS.push({ label: 'release month', detail: `no release tag matches v${pkg.version}`, source: true });
    }
  }

  return {
    REPO,
    head,
    version: pkg.version,
    deps: Object.keys(pkg.dependencies || {}).length,
    tests,
    sectionCount: sectionCounts.length,
    corpusFiles,
    rulesFromRun,
    artifacts,
    benchRows: Number(benchRows),
    sizeDiversity,
    classDiversity,
    allPerfect,
    directions,
    govPages,
    utilities,
    utilitiesFrom,
    stars,
    npmWeekly,
    score,
    mergedPRs,
    releases,
    releaseMonth,
  };
}

function* benchOut(out) {
  for (const m of out.matchAll(/usability=([\d/]+)/g)) yield m;
}

// ── the published claims: value + every place the copy states it ────────────

function claims(m) {
  const k = (v) => (v === null || v === undefined ? '·unmeasured·' : String(v));
  return [
    {
      label: 'reimagine-it stars',
      value: k(m.stars),
      api: true,
      band: [40, 500000],
      how: `${REPO_SLUG}.stargazers_count`,
      sites: [
        { file: 'index.html', re: /⭐ (\d+) · v/ },
        { file: 'index.html', re: /<b>(\d+)★<\/b><span>reimagine-it<\/span>/ },
        { file: 'one-pager.html', re: /<b>(\d+)★<\/b><span>reimagine-it<\/span>/ },
        { file: 'one-pager.html', re: /★ (\d+)<\/span>/ },
        { file: 'NOMINATIONS.md', re: /(\d+) GitHub/ },
        { file: 'NOMINATIONS.md', re: /(\d+)★, zero dependencies/ },
      ],
    },
    {
      label: 'npm downloads / week',
      value: k(m.npmWeekly),
      api: true,
      band: [1, 100000000],
      how: `npm last-week point for ${PKG}`,
      sites: [
        { file: 'index.html', re: /<b>(\d+)<\/b><span>npm dl \/ week<\/span>/ },
        { file: 'index.html', re: /(\d+) downloads\/wk/ },
        { file: 'one-pager.html', re: /<b>(\d+)<\/b><span>npm dl \/ week<\/span>/ },
        { file: 'NOMINATIONS.md', re: /(\d+) npm downloads\/week/ },
      ],
    },
    {
      label: 'OpenSSF Scorecard',
      value: k(m.score),
      api: true,
      band: [0, 10],
      how: 'api.securityscorecards.dev project score',
      sites: [
        { file: 'index.html', re: /<b>([\d.]+)<\/b><span>OpenSSF Scorecard<\/span>/ },
        { file: 'index.html', re: /OpenSSF Scorecard <code>([\d.]+)<\/code>/ },
        { file: 'one-pager.html', re: /<b>([\d.]+)<\/b><span>OpenSSF Scorecard<\/span>/ },
        { file: 'one-pager.html', re: /OpenSSF Scorecard <code>([\d.]+)<\/code>/ },
        { file: 'ORG-README.md', re: /OpenSSF Scorecard ([\d.]+)\*\*/ },
        { file: 'NOMINATIONS.md', re: /Scorecard (?:of )?([\d.]+)/ },
      ],
    },
    {
      label: 'tests in CI',
      value: k(m.tests),
      band: [1, 100000],
      how: `sum of the ${m.sectionCount} reporting sections in reimagine-it npm test`,
      sites: [
        { file: 'index.html', re: /<b>(\d+)<\/b><span>tests in CI<\/span>/ },
        { file: 'index.html', re: /— (\d+) tests,/ },
        { file: 'one-pager.html', re: /<b>(\d+)<\/b><span>tests in CI<\/span>/ },
        { file: 'one-pager.html', re: /<code>(\d+) tests<\/code> over a/ },
        { file: 'ORG-README.md', re: /\*\*(\d+) tests\*\*/ },
        { file: 'NOMINATIONS.md', re: /(\d+) tests/ },
      ],
    },
    {
      label: 'releases in the last 3 months',
      value: k(m.releases),
      api: true,
      band: [1, 10000],
      how: `GitHub releases published within ${RELEASE_WINDOW_DAYS} days`,
      sites: [
        { file: 'one-pager.html', re: /<b>(\d+)<\/b><span>releases \/ 3 mo<\/span>/ },
        { file: 'NOMINATIONS.md', re: /(\d+) releases/ },
      ],
    },
    {
      label: 'merged PRs',
      value: k(m.mergedPRs),
      api: true,
      band: [1, 1000000],
      how: 'GitHub search is:pr is:merged',
      sites: [
        { file: 'index.html', re: /(\d+) merged PRs/ },
        { file: 'one-pager.html', re: /<b>(\d+)<\/b><span>merged PRs<\/span>/ },
      ],
    },
    {
      label: 'reimagine-it version',
      value: m.version,
      how: 'reimagine-it/package.json',
      sites: [
        { file: 'index.html', re: /v(\d+\.\d+\.\d+) · \d+ downloads\/wk/ },
        { file: 'one-pager.html', re: /v(\d+\.\d+\.\d+) · CLI/ },
        { file: 'NOMINATIONS.md', re: /v(\d+\.\d+\.\d+) \(\w{3} \d{4}\)/ },
      ],
    },
    {
      label: 'version release month',
      value: k(m.releaseMonth),
      api: true,
      how: `published_at of the ${m.version} release`,
      sites: [{ file: 'NOMINATIONS.md', re: /v\d+\.\d+\.\d+ \((\w{3} \d{4})\)/ }],
    },
    {
      label: 'parity corpus files',
      value: k(m.corpusFiles),
      band: [1, 100000],
      how: 'the audit-parity guard in npm test',
      sites: [
        { file: 'one-pager.html', re: /(\d+)-file parity corpus/ },
        { file: 'ORG-README.md', re: /(\d+)-file parity corpus/ },
      ],
    },
    {
      label: 'audit rules',
      value: k(m.rulesFromRun),
      band: [1, 500],
      how: 'the audit-parity guard + scripts/audit.py registry',
      sites: [
        { file: 'index.html', re: /(\d+)-rule deterministic audit/ },
        { file: 'one-pager.html', re: /(\d+)-rule audit/ },
        { file: 'NOMINATIONS.md', re: /(\d+)-rule audit/ },
        { file: 'NOMINATIONS.md', re: /(\d+) rules,/ },
      ],
    },
    {
      label: 'committed artifacts',
      value: k(m.artifacts),
      band: [1, 10000],
      how: 'the reproduction guard in npm test',
      sites: [
        { file: 'index.html', re: /(\d+) committed design artifacts/ },
        { file: 'one-pager.html', re: /<code>(\d+) committed artifacts<\/code>/ },
        { file: 'NOMINATIONS.md', re: /(\d+) committed artifacts/ },
        { file: 'NOMINATIONS.md', re: /(\d+) artifacts regenerate/ },
      ],
    },
    {
      label: 'design directions',
      value: k(m.directions),
      band: [1, 500],
      how: 'reimagine-it src/generate.js TOKENS',
      sites: [
        { file: 'index.html', re: /(\d+) design directions/ },
        { file: 'one-pager.html', re: /(\d+) design directions/ },
        { file: 'one-pager.html', re: /all (\d+) design tokens/ },
        { file: 'ORG-README.md', re: /(\d+) directions,/ },
        { file: 'NOMINATIONS.md', re: /(\d+) design directions/ },
        { file: 'NOMINATIONS.md', re: /one of (\d+) directions/ },
        { file: 'NOMINATIONS.md', re: /(\d+) directions \(/ },
      ],
    },
    {
      label: 'class-set difference',
      value: m.classDiversity,
      band: [0, 100],
      how: 'benchmark-tokens.js class-diversity',
      sites: [
        { file: 'one-pager.html', re: /([\d.]+)% mean class-set difference/ },
        { file: 'NOMINATIONS.md', re: /([\d.]+)% mean class-set difference/ },
      ],
    },
    {
      label: 'size difference',
      value: m.sizeDiversity,
      band: [0, 100],
      how: 'benchmark-tokens.js size-diversity',
      sites: [{ file: 'one-pager.html', re: /\(([\d.]+)% size difference\)/ }],
    },
    {
      label: 'government-page proofs',
      value: k(m.govPages),
      band: [1, 100],
      how: 'examples/public-sources/* in reimagine-it',
      sites: [
        { file: 'index.html', re: /<b>(\d+)<\/b><span>gov-page proofs<\/span>/ },
        {
          file: 'index.html',
          re: /\b(\w+) real public-domain government pages/,
          word: true,
        },
        {
          file: 'one-pager.html',
          re: /\b(\w+) real public-domain government pages/,
          word: true,
        },
        {
          file: 'ORG-README.md',
          re: /\b(\w+) real public-domain government pages/,
          word: true,
        },
      ],
    },
    {
      label: 'browser utilities',
      value: k(m.utilities),
      band: [1, 500],
      how: `Tools catalog entries with a pretty slug (${m.utilitiesFrom || 'unavailable'})`,
      sites: [
        { file: 'one-pager.html', re: /<span class="v">(\d+) utilities<\/span>/ },
        { file: 'index.html', re: /(\d+) private browser tools/ },
      ],
    },
    {
      label: 'benchmark rows = directions × 4 sources',
      value: k(m.directions * 4),
      kind: 'assert',
      how: 'benchmark-tokens.js row count',
      sites: [
        {
          file: 'one-pager.html',
          re: /Benchmark: 100\/100 on all \d+ design tokens × 4 sources/,
          // presence-only: the row count below is the real check
        },
      ],
      extra: () =>
        m.benchRows === m.directions * 4 && m.allPerfect
          ? null
          : `benchmark printed ${m.benchRows} rows (expected ${m.directions * 4}) and ${
              m.allPerfect ? 'every row is 100/100' : 'not every row is usability=100/100'
            }`,
    },
    {
      label: 'zero runtime dependencies',
      value: 'zero',
      kind: 'assert',
      how: 'reimagine-it package.json dependencies',
      sites: [
        { file: 'index.html', re: /zero runtime dependencies/ },
        { file: 'NOMINATIONS.md', re: /\bzero dependencies\b/ },
      ],
      extra: () => (m.deps === 0 ? null : `package.json declares ${m.deps} runtime dependencies`),
    },
  ];
}

// ── not gated, on purpose ──────────────────────────────────────────────────

const NOT_GATED = [
  ['16+ required checks', 'required status checks live in branch protection, which needs admin on the repo; the automation token is a collaborator (admin=false). Confirmed by hand 2026-09-25.'],
  ['18 deterministic design checks', 'owned by Kayforkind/design-health-action, a different repo; its own description states 18.'],
  ['ten sensors', 'owned by Kayforkind/liecatchers; its own description states "ten sensors, one RECEIPT.json".'],
  ['five agent hosts', 'the host list lives in reimagine-it docs, not in a machine-readable form.'],
  ['"the first 185" stargazers (NOMINATIONS.md)', 'historical: it means the first 185 people who starred, so it must not track the current count.'],
  ['"I spent 3 months building" (NOMINATIONS.md)', 'historical effort statement.'],
];

// ── the sweep ─────────────────────────────────────────────────────────────

function lineOf(text, index) {
  return text.slice(0, index).split('\n').length;
}

function sweep(all) {
  let sitesChecked = 0;
  for (const claim of all) {
    if (claim.value === '·unmeasured·') continue; // already reported as a source problem
    const bandFail =
      claim.band && !OFFLINE && (Number(claim.value) < claim.band[0] || Number(claim.value) > claim.band[1]);
    if (bandFail) {
      PROBLEMS.push({
        label: claim.label,
        detail: `measured ${claim.value} via ${claim.how}, which is outside the plausible range ${JSON.stringify(
          claim.band
        )} — the source is probably broken, so nothing was compared or rewritten`,
        source: true,
      });
      continue;
    }

    if (claim.extra) {
      const problem = claim.extra();
      if (problem) PROBLEMS.push({ label: claim.label, detail: problem, source: true });
    }

    for (const site of claim.sites) {
      const file = path.join(ROOT, site.file);
      const text = fs.readFileSync(file, 'utf8');
      const matches = [...text.matchAll(new RegExp(site.re.source, site.re.flags + 'g'))];
      if (!matches.length) {
        PROBLEMS.push({
          label: claim.label,
          detail: `${site.file}: the claim is no longer in the copy (pattern ${site.re}) — if that is deliberate, drop it from this gate`,
        });
        continue;
      }
      for (const match of matches) {
        sitesChecked++;
        const line = lineOf(text, match.index);
        if (claim.kind === 'assert') continue; // presence is the whole check
        const stated = site.word ? String(NUM_WORDS[match[1].toLowerCase()]) : match[1];
        if (stated === claim.value) continue;
        PROBLEMS.push({
          label: claim.label,
          detail: `${site.file}:${line} says "${match[0]}", reality is ${claim.value} (${claim.how})`,
          fix: {
            file: site.file,
            start: match.index + match[0].indexOf(match[1]),
            end: match.index + match[0].indexOf(match[1]) + match[1].length,
            text: site.word ? wordOf(Number(claim.value)) : claim.value,
          },
        });
      }
    }
  }
  return sitesChecked;
}

function wordOf(n) {
  const hit = Object.entries(NUM_WORDS).find(([, v]) => v === n);
  return hit ? hit[0] : String(n);
}

// ── report / fix ───────────────────────────────────────────────────────────

function applyFixes(fixable) {
  const byFile = new Map();
  for (const f of fixable) {
    if (!byFile.has(f.file)) byFile.set(f.file, []);
    byFile.get(f.file).push(f);
  }
  let count = 0;
  for (const [file, list] of byFile) {
    const abs = path.join(ROOT, file);
    let text = fs.readFileSync(abs, 'utf8');
    for (const f of list.sort((a, b) => b.start - a.start)) {
      text = text.slice(0, f.start) + f.text + text.slice(f.end);
      count++;
    }
    fs.writeFileSync(abs, text);
  }
  return count;
}

(async () => {
  const m = await measure();
  const all = claims(m);
  const sitesChecked = sweep(all);

  const fixable = PROBLEMS.filter((p) => p.fix);
  const sourceProblems = PROBLEMS.filter((p) => p.source && !p.fix);
  const copyProblems = PROBLEMS.filter((p) => !p.source && !p.fix);

  console.log(
    `\nmeasured against ${REPO_SLUG}@${m.head} + live APIs + the Tools catalog` +
      ` (only HTML/MD copy is checked here)`
  );
  console.log(`claims gated: ${all.length} · copy sites checked: ${sitesChecked}`);
  for (const s of SKIPPED) console.log(`· skipped: ${s}`);

  if (FIX && fixable.length) {
    const n = applyFixes(fixable.map((p) => p.fix));
    console.log(`\n--fix: rewrote ${n} published number(s) to the measured values.`);
    for (const p of fixable) console.log(`  ${p.detail}`);
    console.log('\nRe-run without --fix to confirm, then commit the copy.');
  } else if (fixable.length) {
    console.log(`\nDRIFT (${fixable.length}) — the copy disagrees with reality:`);
    for (const p of fixable) console.log(`  ${p.label}: ${p.detail}`);
    console.log('  → run `node scripts/verify-claims.cjs --fix` to rewrite them, or fix the source.');
  }

  if (sourceProblems.length) {
    console.log(`\nBLOCKED (${sourceProblems.length}) — a source of truth could not be read:`);
    for (const p of sourceProblems) console.log(`  ${p.label}: ${p.detail}`);
  }
  if (copyProblems.length) {
    console.log(`\nCOPY (${copyProblems.length}) — a claim went missing or was reworded:`);
    for (const p of copyProblems) console.log(`  ${p.label}: ${p.detail}`);
  }

  console.log('\nnot gated (see the list in this file for why):');
  for (const [text, why] of NOT_GATED) {
    console.log(`  · ${text}\n      ${why}`);
  }
  console.log('  → these are hand-verified; re-check them when the copy changes.');

  if (process.env.GITHUB_ACTIONS && PROBLEMS.length) {
    for (const p of PROBLEMS) {
      console.log(`::error title=Claim gate (${p.label})::${p.detail.replace(/\n/g, ' ')}`);
    }
  }

  if (!PROBLEMS.length) {
    console.log('\nCLAIM GATE OK — every published number matches its source of truth.');
    process.exit(0);
  }
  if (FIX && !sourceProblems.length && !copyProblems.length) {
    console.log(
      `\nCLAIM GATE OK (after --fix) — ${fixable.length} number(s) rewritten to the measured\n` +
        `values. Only the numbers changed; review the diff, then commit the copy.`
    );
    process.exit(0);
  }
  console.log('\nCLAIM GATE FAILED.');
  process.exit(1);
})().catch((e) => {
  console.error(`\nFAIL: ${e.stack || e.message}`);
  process.exit(1);
});
