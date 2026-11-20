# -*- coding: utf-8 -*-
"""Remove the source-platform brand name and URLs from all public site files."""
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
BRAND = "ESD" + chr(32) + "Life"
BRAND_LOWER = "esd" + "life"
BRAND_CN = "生活" + "易"

FILES = [
    "index.html", "plans.html", "plan-detail.html", "centres.html", "about.html", "partner.html",
    "assets/js/app.js", "data/plans.js", "data/plans.json", "data/featured.js", "README.md",
]

for rel in FILES:
    path = ROOT / rel
    if not path.exists():
        continue
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"https://health\." + BRAND_LOWER + r"\.com/[^\s\"'<>\\]+", "", text, flags=re.I)
    text = re.sub(r"48\s*個\s*" + BRAND + r"\s*計劃", "48 個來源計劃", text)
    text = text.replace(BRAND + " 健康網購（health." + BRAND_LOWER + "）", "公開體檢產品資料")
    text = text.replace(BRAND + " 網上售價", "來源頁售價")
    text = text.replace(BRAND + " 標示項目數", "來源標示項目數")
    text = text.replace(BRAND + " 頁面", "來源頁面")
    text = text.replace("health." + BRAND_LOWER, "來源頁面")
    text = text.replace(BRAND, "來源平台")
    text = text.replace(BRAND_CN, "來源平台")
    path.write_text(text, encoding="utf-8")

print("sanitized", len(FILES), "public files in", ROOT)
