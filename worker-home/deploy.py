#!/usr/bin/env python3
"""Build + deploy the navigatorslab-home worker (Netflix-style site).

Worker serves:  /                 -> homepage
                /apps/style.css   -> shared stylesheet
                /apps/<slug>/     -> 8 dedicated app pages
Zone routes `navigatorslab.com/` and `navigatorslab.com/apps*` point here;
everything else keeps serving via navigatorslab-tools (untouched).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response  # noqa: E402

ROOT = Path(__file__).resolve().parent
ACCOUNT_ID = "56faf9a57ad29af2d943fdedfb5ecda9"
ZONE_ID = "ef65f42da03bceb67d4526c5a297f4e3"
SCRIPT_NAME = os.environ.get("NAV_HOME_WORKER", "navigatorslab-home")
API = "https://api.cloudflare.com/client/v4"
ROUTES = ["navigatorslab.com/", "navigatorslab.com/apps*"]
SKIP_ROUTES = os.environ.get("NAV_HOME_SKIP_ROUTES") == "1"


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
    subprocess.run([sys.executable, str(ROOT / "build_site.py")], check=True, cwd=ROOT)
    script = (ROOT / "dist" / "worker.js").read_bytes()
    print(f"built worker: {len(script)} bytes")
    return script


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


def ensure_routes():
    status, result = api("GET", f"/zones/{ZONE_ID}/workers/routes")
    existing = {(r.get("pattern"), r.get("script")) for r in (result or {}).get("result") or []}
    for pattern in ROUTES:
        if (pattern, SCRIPT_NAME) in existing:
            print("route already present:", pattern)
            continue
        status, result = api("POST", f"/zones/{ZONE_ID}/workers/routes",
                             json.dumps({"pattern": pattern, "script": SCRIPT_NAME}).encode(),
                             "application/json")
        print("route create", pattern, ":", status, "success:", (result or {}).get("success"))
        if not (result or {}).get("success"):
            print(json.dumps((result or {}).get("errors"), indent=1)[:1500])
            raise SystemExit(1)


def main() -> None:
    # --target staging deploys to the staging worker and never touches routes.
    # Anything else deploys to the production worker and ensures its routes.
    target = "staging" if "--target" in sys.argv and "staging" in sys.argv else "production"
    global SCRIPT_NAME
    if target == "staging":
        SCRIPT_NAME = "navigatorslab-home-staging"
        os.environ["NAV_HOME_SKIP_ROUTES"] = "1"
    print(f"target: {target} -> worker {SCRIPT_NAME}")
    script = build()
    deploy_worker(script)
    if not SKIP_ROUTES and os.environ.get("NAV_HOME_SKIP_ROUTES") != "1":
        ensure_routes()


if __name__ == "__main__":
    main()
