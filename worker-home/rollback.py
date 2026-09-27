#!/usr/bin/env python3
"""Rollback: remove the navigatorslab-home routes (navigatorslab.com/ and
navigatorslab.com/apps*) so the catch-all navigatorslab-tools worker serves
everything again (instant)."""
import sys
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
import json, urllib.request

ZONE_ID = "ef65f42da03bceb67d4526c5a297f4e3"
API = "https://api.cloudflare.com/client/v4"
PATTERNS = {"navigatorslab.com/", "navigatorslab.com/apps*"}

def api(method, path):
    req = urllib.request.Request(API + path, method=method)
    add_surrogate_to_request(req, "custom.cloudflare", entry_name="access_token",
                             allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(req, timeout=60) as resp:
        return read_json_response(resp)

routes = api("GET", f"/zones/{ZONE_ID}/workers/routes")["result"]
removed = 0
for r in routes:
    if r.get("pattern") in PATTERNS:
        api("DELETE", f"/zones/{ZONE_ID}/workers/routes/{r['id']}")
        print("removed route", r["id"], r.get("pattern"), "->", r.get("script"))
        removed += 1
if not removed:
    print("no navigatorslab-home routes found; nothing to roll back")
