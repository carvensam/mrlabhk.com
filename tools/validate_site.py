# -*- coding: utf-8 -*-
"""Static validation: pages, assets, data integrity and plain-language copy."""
import json
import re
import struct
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

PAGES = ["index.html", "plans.html", "plan-detail.html", "centres.html", "items.html", "about.html", "partner.html"]
DROP_FIELDS = {"source", "sourceUrl", "sourceCheckedAt", "dataNote", "validityNote",
               "hoursSourceUrl", "hoursCheckedAt"}

BANNED = [
    "ESD" + chr(32) + "Life", "esd" + "life", "生活" + "易",
    "來" + "源", "出" + "處", "貼" + "文", "海" + "報", "會" + "員",
    "公" + "開", "僅" + "供", "參" + "考", "核" + "對", "整" + "理",
    "為" + "準", "頁" + "面", "原" + "價", "標" + "示", "LUAHK",
]


def load_js(path, var):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\." + var + r"\s*=\s*(\{.*\}|\[.*\])\s*;?\s*$", text, re.S)
    if not match:
        raise SystemExit("cannot parse " + str(path))
    return json.loads(match.group(1))


for page in PAGES:
    path = ROOT / page
    if not path.exists():
        errors.append(f"missing page: {page}")
        continue
    html = path.read_text(encoding="utf-8")
    for ref in re.findall(r'(?:src|href)="([^"#:]+)"', html):
        if ref.startswith(("http", "//", "mailto")):
            continue
        ref = ref.split("?")[0]
        if not (ROOT / ref).exists():
            errors.append(f"{page}: missing referenced file {ref}")

plans = json.loads((ROOT / "data" / "plans.json").read_text(encoding="utf-8"))
featured = load_js(ROOT / "data" / "featured.js", "FEATURED_DATA")
codes = [p["id"] for p in plans]
if len(codes) != len(set(codes)):
    errors.append("duplicate plan ids")

for item in plans + featured:
    extra = DROP_FIELDS.intersection(item)
    if extra:
        errors.append(f"{item.get('id')}: leftover fields {sorted(extra)}")
    if not item.get("centre") or not item.get("name"):
        errors.append(f"{item.get('id')}: missing basic data")

counts = Counter(p["category"] for p in plans)
for category, expected in [("general", 12), ("abdominal", 12), ("women", 12), ("cancer", 12)]:
    if counts[category] != expected:
        errors.append(f"category {category}: expected {expected}, got {counts[category]}")

featured_ids = sorted(p["id"] for p in featured)
if featured_ids != [f"e{i:02d}" for i in range(1, 6)]:
    errors.append(f"featured ids: expected e01-e05, got {featured_ids}")

images = [p["image"] for p in plans + featured]
if len(images) != 53:
    errors.append(f"expected 53 image references, got {len(images)}")
if len(set(images)) != len(images):
    errors.append(f"duplicate image references: {[x for x, n in Counter(images).items() if n > 1]}")
for rel in images:
    if not (ROOT / rel).exists():
        errors.append(f"missing image: {rel}")

for idx in range(1, 32):
    thumb = ROOT / "assets" / "images" / ("centre-%02d.png" % idx)
    if not thumb.exists():
        errors.append("missing centre thumbnail: %s" % thumb.name)
        continue
    header = thumb.read_bytes()[:24]
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        errors.append("bad centre thumbnail format: %s" % thumb.name)
        continue
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (640, 240):
        errors.append("centre thumbnail size %s: %dx%d" % (thumb.name, width, height))

centre_map = load_js(ROOT / "data" / "centre-images.js", "CENTRE_IMAGES")
for idx in range(1, 32):
    ref = "assets/images/centre-%02d.png" % idx
    if centre_map.get(str(idx)) != ref:
        errors.append("centre image mapping for %d: %r" % (idx, centre_map.get(str(idx))))

app = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")
for needle in ['WA_NUMBER = "85246151993"', "encodeURIComponent",
               "無授權本平台代為 Booking", "plan-detail.html?id="]:
    if needle not in app:
        errors.append(f"app.js missing expected string: {needle}")

public_files = PAGES + [
    "assets/js/app.js", "data/plans.js", "data/plans.json", "data/featured.js", "data/items.js",
    "README.md", "GODADDY_DNS_SETUP.md",
]
for rel in public_files:
    text = (ROOT / rel).read_text(encoding="utf-8")
    for term in BANNED:
        if term in text:
            errors.append(f"{rel}: contains unwanted wording {term!r}")

print(f"pages={len(PAGES)} plans={len(plans)} featured={len(featured)} images={len(set(images))}")
print(f"errors={len(errors)} warnings={len(warnings)}")
for e in errors:
    print("ERROR:", e)
for w in warnings:
    print("WARN:", w)
raise SystemExit(1 if errors else 0)
