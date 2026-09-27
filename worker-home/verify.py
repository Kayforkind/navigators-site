#!/usr/bin/env python3
"""Post-deploy verification for the navigatorslab-home Netflix-style site."""
import http.client
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("NAV_HOME_BASE", "https://navigatorslab.com")
SLUGS = ["reimagine-it", "integration-rot", "pdf-studio", "tools",
         "book-guide-mcp", "design-health-action", "liecatchers", "data-insights"]

HOME_TITLE = "<title>NavigatorLabs — local-first, private-by-default software</title>"


def fetch(url, retries=2):
    """Return (status_str, headers_dict, body). Handles HTTPError bodies and
    retries once on IncompleteRead (partial responses)."""
    req = urllib.request.Request(url, headers={"User-Agent": "navhome-verify/1.0"})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", errors="replace")[:120000]
                return f"HTTP {resp.status}", dict(resp.headers), body
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode("utf-8", errors="replace")[:120000]
            except Exception:
                body = ""
            return f"HTTP {e.code}", dict(e.headers or {}), body
        except http.client.IncompleteRead as e:
            if attempt < retries:
                time.sleep(2)
                continue
            body = e.partial.decode("utf-8", errors="replace")[:120000]
            return "PARTIAL", {}, body
        except (http.client.RemoteDisconnected, urllib.error.URLError) as e:
            if attempt < retries:
                time.sleep(3)
                continue
            return f"ERROR {type(e).__name__}: {e}", {}, ""
        except Exception as e:
            return f"ERROR {type(e).__name__}: {e}", {}, ""
    return "ERROR retries exhausted", {}, ""


def lh(h):
    return {k.lower(): v for k, v in h.items()}


def home_worker(h):
    return lh(h).get("x-served-by", "") == "navigatorslab-home"


CHECKS = [
    ("homepage title", f"{BASE}/",
     lambda b, h: HOME_TITLE in b),
    ("homepage served by home worker", f"{BASE}/",
     lambda b, h: home_worker(h)),
    ("homepage Originals grid + billboard", f"{BASE}/",
     lambda b, h: "Originals</h2>" in b and "billboard" in b),
    ("homepage links all 8 apps", f"{BASE}/",
     lambda b, h: all(f"/apps/{s}/" in b for s in SLUGS)),
    ("homepage has no ranking copy", f"{BASE}/",
     lambda b, h: "Top 10" not in b and "For Builders" not in b),
    ("stylesheet serves", f"{BASE}/apps/style.css",
     lambda b, h: ".billboard" in b and ".card" in b),
    ("sw.js kill-switch serves", f"{BASE}/sw.js",
     lambda b, h: home_worker(h) and "registration.unregister()" in b
                  and "javascript" in lh(h).get("content-type", "")),
] + [
    (f"app page {s}", f"{BASE}/apps/{s}/",
     lambda b, h, s=s: "<title>" in b and "Examples" in b
                       and "More Like This" in b and home_worker(h))
    for s in SLUGS
] + [
    ("unknown app 404s", f"{BASE}/apps/nope/",
     lambda b, h, s: s.startswith("HTTP 404")),
    ("tools hub intact (not home worker)", "https://navigatorslab.com/tools/",
     lambda b, h: "NavigatorsLab Tools" in b
                  and lh(h).get("x-served-by", "") != "navigatorslab-home"),
    ("tools sw.js intact (Workbox)", "https://navigatorslab.com/tools/sw.js",
     lambda b, h: "workbox" in b.lower() or "precache" in b.lower()),
    ("Integrationrot docs intact", "https://navigatorslab.com/Integrationrot",
     lambda b, h: "integration-rot" in b.lower() or "waitlist" in b.lower()),
    ("pdf-studio route intact", "https://navigatorslab.com/pdf-studio/",
     lambda b, h, s: s.startswith("HTTP 200")),
    ("reimagine route intact", "https://navigatorslab.com/reimagine/",
     lambda b, h, s: s.startswith("HTTP 200")),
    ("waitlist API intact", "https://navigatorslab.com/Integrationrot/waitlist/count",
     lambda b, h: '"count"' in b),
    ("mcp untouched (no route; still tools-worker 404)", "https://navigatorslab.com/mcp",
     lambda b, h, s: s.startswith("HTTP 404")
                     and lh(h).get("x-served-by", "") != "navigatorslab-home"),
]

ok = True
for name, url, pred in CHECKS:
    status, headers, body = fetch(url)
    try:
        passed = bool(pred(body, headers, status))
    except TypeError:
        # legacy 2-arg predicates
        passed = bool(pred(body, headers))
    except Exception as e:
        passed = False
        print(f"  (predicate error: {e})")
    ok = ok and passed
    print(("PASS " if passed else "FAIL ") + name + f"  [{url} -> {status}]")
    time.sleep(1)
sys.exit(0 if ok else 1)
