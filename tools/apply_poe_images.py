# -*- coding: utf-8 -*-
"""Download POE-generated images, optimise them and switch plan data to PNG."""
import hashlib
import json
import re
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "tools" / "poe_images.json"
IDS = (
    [f"e{i:02d}" for i in range(1, 7)]
    + [f"{prefix}{i:02d}" for prefix in "gawc" for i in range(1, 13)]
)

mapping = json.loads(MAPPING.read_text(encoding="utf-8"))
missing = [i for i in IDS if not mapping.get(i)]
if missing:
    raise SystemExit("missing image URLs: " + ", ".join(missing))

image_dir = ROOT / "assets" / "images"
image_dir.mkdir(parents=True, exist_ok=True)
hashes = {}
for plan_id in IDS:
    url = mapping[plan_id]
    raw = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit(f"{plan_id}: not a PNG ({len(raw)} bytes)")
    image = Image.open(BytesIO(raw)).convert("RGB")
    image = image.resize((1200, 750), Image.LANCZOS)
    out = image_dir / f"{plan_id}.png"
    out = out.with_suffix(".webp")
    image.save(out, "WEBP", quality=84, method=6)
    digest = hashlib.md5(out.read_bytes()).hexdigest()
    hashes.setdefault(digest, []).append(plan_id)

duplicates = [v for v in hashes.values() if len(v) > 1]
if duplicates:
    raise SystemExit("duplicate generated images: " + repr(duplicates))

for filename in ("data/plans.json", "data/plans.js", "data/featured.js"):
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    for plan_id in IDS:
        text = text.replace(f"assets/images/{plan_id}.svg", f"assets/images/{plan_id}.webp")
    path.write_text(text, encoding="utf-8")

validator = ROOT / "tools" / "validate_site.py"
text = validator.read_text(encoding="utf-8")
text = text.replace('f"e{i:02d}.svg"', 'f"e{i:02d}.webp"')
text = text.replace('glob("*.svg")', 'glob("*.webp")')
text = text.replace("{len(unique_imgs)} svg images found", "{len(unique_imgs)} webp images found")
text = text.replace("if len(unique_imgs) < 55:", "if len(unique_imgs) < 54:")
validator.write_text(text, encoding="utf-8")

print(f"downloaded={len(IDS)} unique={len(hashes)}")
