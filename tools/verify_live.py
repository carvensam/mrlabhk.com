# -*- coding: utf-8 -*-
"""Verify the live site: public copy, contact details, images and HTTPS."""
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://www.mrlabhk.com/"
CB = str(int(time.time()))
PAGES = ["index.html", "plans.html", "plan-detail.html", "centres.html", "about.html", "partner.html"]
PUBLIC_FILES = PAGES + [
    "assets/js/app.js", "data/plans.js", "data/plans.json", "data/featured.js",
    "README.md", "GODADDY_DNS_SETUP.md",
]
BANNED = [
    "ESD" + chr(32) + "Life", "esd" + "life", "生活" + "易",
    "來" + "源", "出" + "處", "貼" + "文", "海" + "報", "會" + "員",
    "公" + "開", "僅" + "供", "參" + "考", "核" + "對", "整" + "理",
    "為" + "準", "頁" + "面", "原" + "價", "標" + "示", "LUAHK",
]


def fetch(path):
    url = BASE + path + ("&" if "?" in path else "?") + "v=" + CB
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
    try:
        response = urllib.request.urlopen(req, timeout=25)
        return response.status, response.headers.get("Content-Type", ""), response.read()
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
texts = {}
for rel in PUBLIC_FILES:
    status, _, body = fetch(rel)
    text = body.decode("utf-8", "ignore")
    texts[rel] = text
    hits = [term for term in BANNED if term in text]
    ok = status == 200 and len(body) > 100 and not hits
    print(f"FILE {rel}: status={status} bytes={len(body)} clean={ok} hits={hits[:3]}")
    if not ok:
        errors.append("file " + rel)

source_txt = urllib.parse.quote("香港體檢計劃資料（共 48 個）.txt")
status, _, _ = fetch(source_txt)
print(f"SOURCE TXT: status={status} removed={status == 404}")
if status != 404:
    errors.append("source txt still public")

featured_text = texts.get("data/featured.js", "")
if "6661 8628" not in featured_text:
    errors.append("live E06 phone missing")
for place in ["尖沙咀", "佐敦", "中環", "荃灣"]:
    if place not in featured_text:
        errors.append(f"live E06 place missing: {place}")

plans = json.loads(Path("data/plans.json").read_text(encoding="utf-8"))
images = [p["image"] for p in plans]
images += re.findall(r'"image"\s*:\s*"(assets/images/[^"]+)"', featured_text)
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
