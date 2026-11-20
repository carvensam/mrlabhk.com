# -*- coding: utf-8 -*-
"""Static validation: pages, asset references, data integrity, WhatsApp links."""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

pages = ["index.html", "plans.html", "plan-detail.html", "centres.html", "about.html", "partner.html"]
for page in pages:
    p = ROOT / page
    if not p.exists():
        errors.append(f"missing page: {page}")
        continue
    html = p.read_text(encoding="utf-8")
    for ref in re.findall(r'(?:src|href)="([^"#:]+)"', html):
        if ref.startswith(("http", "//", "mailto")):
            continue
        ref = ref.split("?")[0]
        if not (ROOT / ref).exists():
            errors.append(f"{page}: missing referenced file {ref}")

plans = json.loads((ROOT / "data" / "plans.json").read_text(encoding="utf-8"))
featured_js = (ROOT / "data" / "featured.js").read_text(encoding="utf-8")
codes = [p["id"] for p in plans]
if len(codes) != len(set(codes)):
    errors.append("duplicate plan ids")
for p in plans:
    img = ROOT / p["image"]
    if not img.exists():
        errors.append(f"{p['id']}: missing image {p['image']}")
    if p.get("sourceUrl") and not p["sourceUrl"].startswith("https://"):
        errors.append(f"{p['id']}: bad sourceUrl")
    if not p["centre"] or not p["name"]:
        errors.append(f"{p['id']}: missing basic data")

c = Counter(p["category"] for p in plans)
for cat, n in [("general", 12), ("abdominal", 12), ("women", 12), ("cancer", 12)]:
    if c[cat] != n:
        errors.append(f"category {cat}: expected {n}, got {c[cat]}")

featured_ids = re.findall(r'"id"\s*:\s*"(e0[1-6])"', featured_js)
if sorted(featured_ids) != [f"e{i:02d}" for i in range(1, 7)]:
    errors.append(f"featured ids: expected e01-e06, got {sorted(featured_ids)}")

plan_imgs = [p["image"] for p in plans]
featured_imgs = re.findall(r'"image"\s*:\s*"(assets/images/[^"]+)"', featured_js)
all_imgs = plan_imgs + featured_imgs
if len(all_imgs) != 54:
    errors.append(f"expected 54 image references, got {len(all_imgs)}")
if len(set(all_imgs)) != len(all_imgs):
    dupes = [x for x, n in Counter(all_imgs).items() if n > 1]
    errors.append(f"duplicate image references: {dupes}")
for rel in all_imgs:
    if not (ROOT / rel).exists():
        errors.append(f"missing image: {rel}")

app = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")
for needle in ['WA_NUMBER = "85246151993"', "encodeURIComponent", "無授權本平台代為 Booking", "plan-detail.html?id="]:
    if needle not in app:
        errors.append(f"app.js missing expected string: {needle}")

public_files = pages + [
    "assets/js/app.js", "data/plans.js", "data/plans.json", "data/featured.js", "README.md",
]
BRAND = "ESD" + chr(32) + "Life"
forbidden = re.compile(BRAND + r"|esd" + r"life|生活" + "易", re.I)
for rel in public_files:
    text = (ROOT / rel).read_text(encoding="utf-8")
    if forbidden.search(text):
        errors.append(f"{rel}: contains forbidden source-platform name")

print(f"pages={len(pages)} plans={len(plans)} images={len(set(all_imgs))}")
print(f"errors={len(errors)} warnings={len(warnings)}")
for e in errors:
    print("ERROR:", e)
for w in warnings:
    print("WARN:", w)
raise SystemExit(1 if errors else 0)
