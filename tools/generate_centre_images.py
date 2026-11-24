# -*- coding: utf-8 -*-
"""Generate lightweight, local centre thumbnail artwork for the centre list."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]

COLOURS = [
    ("#0e8f86", "#1fb6a8"), ("#1267a3", "#2b9fd6"), ("#2a6f97", "#4aa3c7"),
    ("#177f8c", "#35b3b8"), ("#365f9e", "#5b8fd0"), ("#0f7a6b", "#2fae8c"),
    ("#1d6b8a", "#39a6bd"), ("#3d6b8f", "#6aa2c4"), ("#116b7d", "#2b9fae"),
    ("#2c7a6f", "#54b39a"),
]

ICONS = [
    '<path d="M100 72h22v18h18v22h-18v18h-22v-18H82V90h18z"/>',
    '<path d="M111 128s-24-16-24-34a13 13 0 0 1 24-7 13 13 0 0 1 24 7c0 18-24 34-24 34z"/>',
    '<path d="M100 60v18a22 22 0 0 0 44 0V60M122 100v12a20 20 0 0 0 40 0V96"/><circle cx="100" cy="56" r="5"/><circle cx="162" cy="92" r="5"/>',
    '<rect x="88" y="58" width="68" height="84" rx="10"/><path d="M102 82h40M102 98h40M102 114h26"/>',
    '<circle cx="122" cy="100" r="34"/><circle cx="122" cy="100" r="12"/><path d="M122 56v12M122 132v12M78 100h12M154 100h12"/>',
    '<path d="M94 132V74l28-16 28 16v58M94 132h56M108 92h28M108 108h20"/>',
]

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 180" role="img" aria-label="體檢中心識別圖">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
  <rect width="280" height="180" fill="url(#g)"/>
  <circle cx="242" cy="26" r="58" fill="#fff" opacity=".09"/>
  <circle cx="20" cy="162" r="48" fill="#fff" opacity=".08"/>
  <g fill="none" stroke="#fff" stroke-width="2.4" opacity=".16"><circle cx="44" cy="40" r="6"/><circle cx="70" cy="40" r="6"/><circle cx="96" cy="40" r="6"/><path d="M210 148h18m12 0h18m12 0h10"/></g>
  <g fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round" opacity=".95" transform="translate(18,0)">{icon}</g>
  <g fill="#fff" opacity=".9"><rect x="184" y="112" width="66" height="6" rx="3"/><rect x="184" y="128" width="44" height="6" rx="3" opacity=".6"/></g>
</svg>
"""


def centre_names():
    featured = (ROOT / "data" / "featured.js").read_text(encoding="utf-8")
    f = json.loads(re.search(r"window\.FEATURED_DATA\s*=\s*(\[.*\])\s*;?\s*$", featured, re.S).group(1))
    plans = json.loads((ROOT / "data" / "plans.json").read_text(encoding="utf-8"))
    seen = []
    for item in f + plans:
        if item["centre"] not in seen:
            seen.append(item["centre"])
    ordered = ["香港生物醫學核心化驗所", "醫家健康體檢中心"] + [c for c in seen if c not in ("香港生物醫學核心化驗所", "醫家健康體檢中心")]
    return ordered


out_dir = ROOT / "assets" / "images"
out_dir.mkdir(parents=True, exist_ok=True)
for i, name in enumerate(centre_names()):
    c1, c2 = COLOURS[i % len(COLOURS)]
    icon = ICONS[i % len(ICONS)]
    (out_dir / ("centre-%02d.svg" % (i + 1))).write_text(
        TEMPLATE.format(c1=c1, c2=c2, icon=icon), encoding="utf-8"
    )
print("generated", len(centre_names()), "centre thumbnails")
