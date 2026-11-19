# -*- coding: utf-8 -*-
"""Verify the deployed site: pages, data files and every plan image."""
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE = "https://www.mrlabhk.com/"
CB = str(int(time.time()))
PAGES = ["index.html", "plans.html", "plan-detail.html", "centres.html", "about.html", "partner.html"]


def fetch(path):
    url = BASE + path + ("&" if "?" in path else "?") + "v=" + CB
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    try:
        r = urllib.request.urlopen(req, timeout=25)
        return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, "", b""
    except Exception as e:
        return 0, str(e), b""


def is_image(body):
    return (
        b"<svg" in body[:200]
        or body.startswith(b"\x89PNG")
        or body.startswith(b"\xff\xd8\xff")
        or b"WEBP" in body[:16]
    )


errors = []
for page in PAGES:
    status, _, body = fetch(page)
    ok = status == 200 and len(body) > 100
    print(f"PAGE {page}: status={status} bytes={len(body)} ok={ok}")
    if not ok:
        errors.append("page " + page)

for data_file in ("data/plans.js", "data/featured.js"):
    status, _, body = fetch(data_file)
    text = body.decode("utf-8", "ignore")
    ok = status == 200 and len(body) > 100 and "assets/images/e01.svg" not in text
    print(f"DATA {data_file}: status={status} bytes={len(body)} ok={ok}")
    if not ok:
        errors.append("data " + data_file)

plans = json.loads(Path("data/plans.json").read_text(encoding="utf-8"))
featured = Path("data/featured.js").read_text(encoding="utf-8")
images = [p["image"] for p in plans]
images += re.findall(r'"image"\s*:\s*"(assets/images/[^"]+)"', featured)
images = sorted(set(images))

image_failures = []
for image in images:
    status, ctype, body = fetch(image)
    if not (status == 200 and is_image(body)):
        image_failures.append((image, status, ctype, len(body)))
print(f"IMAGES total={len(images)} failures={len(image_failures)}")
for failure in image_failures[:10]:
    print("IMG FAIL", failure)

try:
    ssl.get_server_certificate(("www.mrlabhk.com", 443))
    ssl_ok = True
except Exception:
    ssl_ok = False
print(f"SSL ok={ssl_ok}")
print(f"RESULT errors={len(errors)} image_failures={len(image_failures)} ssl_ok={ssl_ok}")
raise SystemExit(1 if errors or image_failures or not ssl_ok else 0)
