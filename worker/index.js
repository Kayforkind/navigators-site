/**
 * navigatorslab.com/reimagine/ — serves the reimagine-it docs site (playground
 * + gallery) by proxying the GitHub Pages origin, exactly like /tools/ does.
 *
 * Same-account custom domains need a CNAME via the dashboard, but zone routes
 * on an already-proxied hostname do not — so this worker + two routes put the
 * playground on the main site with zero DNS changes.
 *
 * The origin is the reimagine-it GitHub Pages site. Relative asset paths in
 * the docs HTML (examples/…, tokens/…) resolve against /reimagine/… and hit
 * the same proxy, so the whole 38 MB docs tree works without a rebuild.
 *
 * Deploy: npx wrangler deploy   (from this directory)
 */

// Trailing slash is load-bearing: new URL(path, base) drops the last
// segment of a base without one, which would 404 every request.
const ORIGIN = "https://kayforkind.github.io/reimagine-it";

const SECURITY_HEADERS = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
};

// Only allow proxying to the fixed origin — never open-proxy user paths.
const SAFE_PATH = /^\/[A-Za-z0-9_\-./]*$/;

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/favicon.ico") {
      return new Response(null, { status: 204 });
    }

    if (!SAFE_PATH.test(url.pathname)) {
      return new Response("Not found", { status: 404 });
    }

    // On the zone route the request path carries the mount prefix
    // (/reimagine/...); the origin has no such prefix. Strip it — but only
    // when serving under the custom host, workers.dev keeps bare paths.
    // Case-insensitive: /Reimagine and friends 301 to the canonical path.
    let path = url.pathname;
    if (url.hostname !== "reimagine-lab.kazim-r-merchant.workers.dev") {
      const m = path.match(/^\/reimagine(\/.*)?$/i);
      if (m) {
        const rest = m[1] || "/";
        const canonical = "/reimagine" + rest;
        if (path !== canonical) {
          return Response.redirect(new URL(canonical + url.search, url.origin).toString(), 301);
        }
        path = rest;
      }
    }

    // Manual join: new URL("/x", base) discards the base path entirely,
    // which silently pointed every request at the github.io root.
    const originURL = new URL(ORIGIN + path + url.search);

    // GitHub Pages sends HTML to the canonical root for unknown paths —
    // detect the redirect and surface a clean 404 instead of a wrong page.
    const upstream = await fetch(originURL, {
      redirect: "manual",
      headers: { "User-Agent": "navigatorslab-proxy" },
    });

    if (upstream.status >= 300 && upstream.status < 400) {
      const location = upstream.headers.get("location");
      if (location) {
        const redirectTarget = new URL(location, originURL);
        if (redirectTarget.pathname.startsWith("/reimagine-it/")) {
          redirectTarget.pathname =
            "/reimagine" + redirectTarget.pathname.slice("/reimagine-it".length);
        }
        return Response.redirect(redirectTarget.toString(), upstream.status);
      }
    }

    const headers = new Headers();
    for (const [k, v] of upstream.headers) {
      // Hop-by-hop and origin-specific headers must not pass through.
      if (
        [
          "set-cookie",
          "content-security-policy",
          "content-security-policy-report-only",
          "content-encoding",
          "content-length",
          "transfer-encoding",
          "connection",
          "strict-transport-security",
        ].includes(k.toLowerCase())
      ) {
        continue;
      }
      headers.set(k, v);
    }

    for (const [k, v] of Object.entries(SECURITY_HEADERS)) {
      headers.set(k, v);
    }

    return new Response(upstream.body, {
      status: upstream.status,
      headers,
    });
  },
};
