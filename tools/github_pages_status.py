# -*- coding: utf-8 -*-
"""Query and update GitHub Pages configuration for the site repo."""
import json
import sys
from urllib.error import HTTPError

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
from github_setup import api, get_credential, REPO, DOMAIN  # noqa: E402

user, token = get_credential()
login = user if user != "oauth" else "carvensam"
base = "/repos/" + login + "/" + REPO + "/pages"

status, pages = api("GET", base, token)
print("pages_get=" + str(status))
print(json.dumps({k: pages.get(k) for k in ("cname", "https_enforced", "public", "build_type", "status", "url", "html_url")}, ensure_ascii=False))

status, upd = api("PUT", base, token, {"cname": DOMAIN, "https_enforced": True})
print("pages_put=" + str(status))
if status >= 400:
    print(json.dumps(upd, ensure_ascii=False)[:800])
else:
    print(json.dumps({k: upd.get(k) for k in ("cname", "https_enforced", "public", "build_type", "status")}, ensure_ascii=False))
