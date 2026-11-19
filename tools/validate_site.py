# -*- coding: utf-8 -*-
"""Static validation: pages, asset references, data integrity, WhatsApp links."""
import json
import re
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
    if not p["sourceUrl"].startswith("https://"):
        errors.append(f"{p['id']}: bad sourceUrl")
    if not p["centre"] or not p["name"]:
        errors.append(f"{p['id']}: missing basic data")

# Expected category counts
from collections import Counter
c = Counter(p["category"] for p in plans)
for cat, n in [("general", 12), ("abdominal", 12), ("women", 12), ("cancer", 12)]:
    if c[cat] != n:
        errors.append(f"category {cat}: expected {n}, got {c[cat]}")

# Featured images
for i in range(1, 6):
    f = ROOT / "assets" / "images" / f"e{i:02d}.svg"
    if not f.exists():
        errors.append(f"missing featured image {f.name}")

app = (ROOT / "assets" / "js" / "app.js").read_text(encoding="utf-8")
for needle in ['WA_NUMBER = "85246151993"', "encodeURIComponent", "無授權本平台代為 Booking", "plan-detail.html?id="]:
    if needle not in app:
        errors.append(f"app.js missing expected string: {needle}")

unique_imgs = list((ROOT / "assets" / "images").glob("*.svg"))
if len(unique_imgs) < 55:
    warnings.append(f"only {len(unique_imgs)} svg images found")

print(f"pages={len(pages)} plans={len(plans)} images={len(unique_imgs)}")
print(f"errors={len(errors)} warnings={len(warnings)}")
for e in errors:
    print("ERROR:", e)
for w in warnings:
    print("WARN:", w)
raise SystemExit(1 if errors else 0)
