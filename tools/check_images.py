# -*- coding: utf-8 -*-
"""Check that every referenced plan image exists and is byte-unique."""
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
plans = json.loads((ROOT / "data" / "plans.json").read_text(encoding="utf-8"))
featured = (ROOT / "data" / "featured.js").read_text(encoding="utf-8")
refs = [p["image"] for p in plans]
refs += re.findall(r'"image"\s*:\s*"(assets/images/[^"]+)"', featured)

by_hash = defaultdict(list)
missing = []
for ref in refs:
    path = ROOT / ref
    if not path.exists():
        missing.append(ref)
        continue
    by_hash[hashlib.md5(path.read_bytes()).hexdigest()].append(ref)

duplicates = [v for v in by_hash.values() if len(v) > 1]
print(f"refs={len(refs)} unique_files={len(by_hash)} missing={len(missing)} duplicate_groups={len(duplicates)}")
for group in duplicates:
    print("DUPLICATE", group)
for ref in missing:
    print("MISSING", ref)
raise SystemExit(1 if missing or duplicates else 0)
