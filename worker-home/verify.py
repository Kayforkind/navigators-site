#!/usr/bin/env python3
"""Post-deploy verification for the navigatorslab-home Netflix-style site."""
import os
import sys
import time
import urllib.request

BASE = os.environ.get("NAV_HOME_BASE", "https://navigatorslab.com")
SLUGS = ["reimagine-it", "integration-rot", "pdf-studio", "tools",
         "book-guide-mcp", "design-health-action", "liecatchers", "data-insights"]

CHECKS = [
    ("homepage serves", f"{BASE}/",
     lambda b, h: "<title>NavigatorLabs — local-first, private-by-default software</title>" in b
                  and "Top 10" in b and "For Builders" in b),
    ("stylesheet serves", f"{BASE}/apps/style.css",
     lambda b, h: ".billboard" in b and ".card" in b),
] + [
    (f"app page {s}", f"{BASE}/apps/{s}/",
     lambda b, h, s=s: f"<title>" in b and "Examples" in b and "More Like This" in b)
    for s in SLUGS
] + [
    ("unknown app 404s", f"{BASE}/apps/nope/",
     lambda b, h: h.startswith("HTTP 404")),
    ("tools hub intact", "https://navigatorslab.com/tools/",
     lambda b, h: "NavigatorsLab Tools" in b),
    ("Integrationrot docs intact", "https://navigatorslab.com/Integrationrot",
     lambda b, h: "integration-rot" in b.lower() or "waitlist" in b.lower()),
    ("pdf-studio route intact", "https://navigatorslab.com/pdf-studio/",
     lambda b, h: h.startswith("HTTP 200")),
    ("reimagine route intact", "https://navigatorslab.com/reimagine/",
     lambda b, h: h.startswith("HTTP 200")),
    ("waitlist API intact", "https://navigatorslab.com/Integrationrot/waitlist/count",
     lambda b, h: '"count"' in b),
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "navhome-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return f"HTTP {resp.status}", resp.read().decode("utf-8", errors="replace")[:80000]
    except Exception as e:
        return f"ERROR {e}", ""

ok = True
for name, url, pred in CHECKS:
    status, body = fetch(url)
    passed = pred(body, status)
    ok = ok and passed
    print(("PASS " if passed else "FAIL ") + name + f"  [{url} -> {status}]")
    time.sleep(1)
sys.exit(0 if ok else 1)
