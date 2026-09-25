/* Extracts every http(s) link from the repo's HTML/MD files and HEAD-checks
 * it. Exit 1 on any 404 — this is the gate that would have caught the
 * study-guide card pointing at a non-existent repo (fixed 2026-09-24).
 * Run: node scripts/check-links.cjs   (skips list in SKIP) */
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '..');
const SKIP = new Set([
  // Templates/placeholders in paste-ready copy, not live pages.
  'https://example.com',
  'https://your-host.example',
  'https://navigators.com/', // documented as NOT ours; kept only in the warning text
]);

function walk(dir, out = []) {
  for (const f of fs.readdirSync(dir)) {
    if (f === '.git' || f === 'node_modules') continue;
    const fp = path.join(dir, f);
    if (fs.statSync(fp).isDirectory()) walk(fp, out);
    else if (/\.(html|md)$/.test(f)) out.push(fp);
  }
  return out;
}

const files = walk(ROOT);
const links = new Map(); // url -> first file that references it
const LINK_RE = /https?:\/\/[^\s"'<>`)\]…]+/g;
for (const f of files) {
  const text = fs.readFileSync(f, 'utf8');
  for (const m of text.matchAll(LINK_RE)) {
    const url = m[0].replace(/[.,;]+$/, '');
    if (!SKIP.has(url)) {
      if (!links.has(url)) links.set(url, path.relative(ROOT, f));
    }
  }
}

(async () => {
  const bad = [];
  let checked = 0;
  for (const [url, from] of links) {
    try {
      const res = await fetch(url, { method: 'HEAD', redirect: 'follow', signal: AbortSignal.timeout(15000) });
      // Some hosts reject HEAD; only treat definitive client errors as dead.
      if (res.status === 404 || res.status === 410) {
        let retry = await fetch(url, { method: 'GET', signal: AbortSignal.timeout(15000) }).then((r) => r.status).catch(() => res.status);
        if (retry === 404 || retry === 410) { bad.push(`404 ${url}  (referenced in ${from})`); }
      }
      checked++;
    } catch (e) {
      console.warn(`warn: could not reach ${url} (${e.message}) — from ${from}`);
    }
  }
  console.log(`\nchecked ${checked} unique external links across ${files.length} files`);
  if (bad.length) {
    console.error('\nDEAD LINKS:');
    for (const b of bad) console.error('  ' + b);
    process.exit(1);
  }
  console.log('all links resolve (404 class gated)');
})();
