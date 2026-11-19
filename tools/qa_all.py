# -*- coding: utf-8 -*-
"""Final QA: fetch every page and asset from local server, verify HTTP 200 and key content."""
import re
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8123/"
PAGES = ["index.html", "plans.html", "plan-detail.html", "centres.html", "about.html", "partner.html"]
ASSETS = [
    "assets/css/style.css", "assets/js/app.js", "data/featured.js", "data/plans.js",
    "assets/images/logo.svg", "assets/images/favicon.svg",
]
errors = []


def fetch(path):
    try:
        r = urllib.request.urlopen(BASE + path, timeout=10)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()


for p in PAGES:
    status, body = fetch(p)
    ok = status == 200 and len(body) > 100
    print(f"PAGE {p}: status={status} bytes={len(body)} ok={ok}")
    if not ok:
        errors.append(p)

for a in ASSETS:
    status, body = fetch(a)
    ok = status == 200 and len(body) > 0
    print(f"ASSET {a}: status={status} bytes={len(body)} ok={ok}")
    if not ok:
        errors.append(a)

# Check every image referenced in plans.js/featured.js is fetchable
import json
plans = json.load(open("data/plans.json", encoding="utf-8"))
featured_txt = open("data/featured.js", encoding="utf-8").read()
imgs = set(p["image"] for p in plans)
imgs |= set(re.findall(r'image:\s*"(assets/images/[^"]+)"', featured_txt))
img_errors = 0
for img in sorted(imgs):
    status, body = fetch(img)
    if status != 200 or b"<svg" not in body[:200]:
        img_errors += 1
        print(f"IMG FAIL {img}: status={status}")
print(f"IMAGES total={len(imgs)} failures={img_errors}")
if img_errors:
    errors.append("images")

print(f"\nRESULT errors={len(errors)}")
raise SystemExit(1 if errors else 0)
