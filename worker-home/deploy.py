#!/usr/bin/env python3
"""Build + deploy the navigatorslab-home worker.

Serves the new NavigatorLabs landing page at the exact root path `/`.
Zone route `navigatorslab.com/` (exact) is more specific than the existing
`navigatorslab.com/*` catch-all, so everything else keeps flowing to
navigatorslab-tools untouched. Zero changes to the existing worker.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response  # noqa: E402

ROOT = Path(__file__).resolve().parent
ACCOUNT_ID = "56faf9a57ad29af2d943fdedfb5ecda9"
ZONE_ID = "ef65f42da03bceb67d4526c5a297f4e3"
SCRIPT_NAME = "navigatorslab-home"
API = "https://api.cloudflare.com/client/v4"

WORKER_TEMPLATE = """/* navigatorslab-home — NavigatorLabs landing page at the exact root `/`.
 * Zone route `navigatorslab.com/` beats the `navigatorslab.com/*` catch-all
 * for the root path only; every other path keeps serving via
 * navigatorslab-tools (tools SPA, pdf-studio, Integrationrot docs, MCP).
 * Single static HTML, zero external fetches, zero JavaScript (CSP has no
 * 'unsafe-inline' for scripts — all animation is CSS).
 */
addEventListener("fetch", (event) => {
  event.respondWith(handle(event.request));
});

const HEADERS = {
  "content-type": "text/html; charset=utf-8",
  "content-security-policy": "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; font-src 'self' data:; worker-src 'self' blob:; child-src 'self' blob:; frame-ancestors 'none'; base-uri 'none'; form-action 'none'",
  "x-content-type-options": "nosniff",
  "x-frame-options": "DENY",
  "referrer-policy": "no-referrer",
  "cross-origin-opener-policy": "same-origin",
  "cross-origin-resource-policy": "same-origin",
  "permissions-policy": "camera=(), microphone=(), geolocation=(), payment=(), usb=()",
  "strict-transport-security": "max-age=31536000; includeSubDomains",
  "cache-control": "public, max-age=600",
};

async function handle(req) {
  const url = new URL(req.url);
  if (url.pathname === "/") {
    return new Response(HTML, { status: 200, headers: HEADERS });
  }
  return new Response("not found", { status: 404, headers: HEADERS });
}

const HTML = __HTML__;
"""


def api(method: str, path: str, body: bytes | None = None, ctype: str | None = None):
    req = urllib.request.Request(API + path, data=body, method=method)
    if ctype:
        req.add_header("Content-Type", ctype)
    add_surrogate_to_request(req, "custom.cloudflare", entry_name="access_token",
                             allowed_hosts=["api.cloudflare.com"])
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')[:1500]}")


def build() -> bytes:
    html = (ROOT / "landing-new.html").read_text(encoding="utf-8")
    assert "`" not in html and "${" not in html, "HTML not template-literal safe"
    worker = WORKER_TEMPLATE.replace("__HTML__", "`" + html + "`")
    assert "__HTML__" not in worker
    return worker.encode("utf-8")


def deploy_worker(script: bytes):
    metadata = {
        "body_part": "script",
        "compatibility_date": "2026-09-01",
        "usage_model": "standard",
        "bindings": [],
    }
    boundary = "----navhome7f3a2b1c9d"
    head = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="metadata"\r\n'
        "Content-Type: application/json\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="script"; filename="worker.js"\r\n'
        "Content-Type: application/javascript\r\n\r\n"
    ).encode()
    body = head + script + f"\r\n--{boundary}--\r\n".encode()
    status, result = api("PUT", f"/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}",
                         body, f"multipart/form-data; boundary={boundary}")
    print("worker deploy:", status, "success:", (result or {}).get("success"))
    if not (result or {}).get("success"):
        print(json.dumps((result or {}).get("errors"), indent=1)[:1500])
        raise SystemExit(1)


def ensure_route():
    status, result = api("GET", f"/zones/{ZONE_ID}/workers/routes")
    routes = (result or {}).get("result") or []
    for r in routes:
        if r.get("pattern") == "navigatorslab.com/" and r.get("script") == SCRIPT_NAME:
            print("route already present:", r["id"])
            return r["id"]
    status, result = api("POST", f"/zones/{ZONE_ID}/workers/routes",
                         json.dumps({"pattern": "navigatorslab.com/", "script": SCRIPT_NAME}).encode(),
                         "application/json")
    print("route create:", status, "success:", (result or {}).get("success"))
    if not (result or {}).get("success"):
        print(json.dumps((result or {}).get("errors"), indent=1)[:1500])
        raise SystemExit(1)
    return (result.get("result") or {}).get("id")


def main() -> None:
    script = build()
    print(f"built worker: {len(script)} bytes")
    deploy_worker(script)
    rid = ensure_route()
    print("route id:", rid)


if __name__ == "__main__":
    main()
