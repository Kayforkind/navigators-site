#!/usr/bin/env python3
"""Post-deploy verification for the navigatorslab-home landing page."""
import sys
import urllib.request

CHECKS = [
    ("root serves new landing",
     "https://navigatorslab.com/",
     lambda b, h: "<title>NavigatorLabs — local-first, private-by-default software</title>" in b
                  and "and proves it." in b),
    ("root is NOT the old SPA",
     "https://navigatorslab.com/",
     lambda b, h: "NavigatorsLab Tools — 23 free tools" not in b.split("</title>")[0]),
    ("tools hub intact",
     "https://navigatorslab.com/tools/",
     lambda b, h: "NavigatorsLab Tools" in b),
    ("Integrationrot docs intact",
     "https://navigatorslab.com/Integrationrot",
     lambda b, h: "integration-rot" in b.lower() or "waitlist" in b.lower()),
    ("pdf-studio route intact",
     "https://navigatorslab.com/pdf-studio/",
     lambda b, h: h.startswith("HTTP 200")),
    ("waitlist API intact",
     "https://navigatorslab.com/Integrationrot/waitlist/count",
     lambda b, h: '"count"' in b),
]

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "navhome-verify/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return f"HTTP {resp.status}", resp.read().decode("utf-8", errors="replace")[:60000]
    except Exception as e:
        return f"ERROR {e}", ""

ok = True
for name, url, pred in CHECKS:
    status, body = fetch(url)
    passed = pred(body, status)
    ok = ok and passed
    print(("PASS " if passed else "FAIL ") + name + f"  [{url} -> {status}]")
sys.exit(0 if ok else 1)
