#!/usr/bin/env python3
"""Rollback: remove the navigatorslab.com/ exact route so the catch-all
navigatorslab-tools worker serves / again (instant)."""
import sys
sys.path.insert(0, "/opt/hatch/skills/skill-creator/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
import json, urllib.request

ZONE_ID = "ef65f42da03bceb67d4526c5a297f4e3"
API = "https://api.cloudflare.com/client/v4"

def api(method, path):
    req = urllib.request.Request(API + path, method=method)
    add_surrogate_to_request(req, "custom.cloudflare", entry_name="access_token",
                             allowed_hosts=["api.cloudflare.com"])
    with urllib.request.urlopen(req, timeout=60) as resp:
        return read_json_response(resp)

routes = api("GET", f"/zones/{ZONE_ID}/workers/routes")["result"]
for r in routes:
    if r.get("pattern") == "navigatorslab.com/":
        api("DELETE", f"/zones/{ZONE_ID}/workers/routes/{r['id']}")
        print("removed route", r["id"], "->", r.get("script"))
        break
else:
    print("no navigatorslab.com/ route found; nothing to roll back")
