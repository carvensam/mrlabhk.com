# -*- coding: utf-8 -*-
"""Parse the supplied 48-plan text file into structured JSON/JS for the site."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "香港體檢計劃資料（共 48 個）.txt"
OUT_JSON = ROOT / "data" / "plans.json"
OUT_JS = ROOT / "data" / "plans.js"

CATEGORY_MAP = {"G": "general", "A": "abdominal", "W": "women", "C": "cancer"}
CATEGORY_LABEL = {
    "general": "一般／全身",
    "abdominal": "腹腔相關",
    "women": "女性",
    "cancer": "癌症相關",
}

FIELD_RE = re.compile(r"^(計劃名稱|體檢中心|ESD Life 標示項目數|ESD Life 網上售價|適用對象及重點（ESD Life 頁面原文）|檢查內容|體檢中心地址、辦公時間及電話（共 \d+ 個地點）|出處|出處網址)：(.*)$")


def clean(s: str) -> str:
    return s.strip()


def parse():
    text = SRC.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    plans = []
    cur = None
    mode = None
    section = None
    location = None

    def flush():
        nonlocal cur
        if cur:
            plans.append(cur)
            cur = None

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()

        m = re.match(r"^【([GAWC]\d{2})】(.+)$", stripped)
        if m:
            flush()
            code = m.group(1)
            cur = {
                "id": code.lower(),
                "code": code,
                "category": CATEGORY_MAP[code[0]],
                "categoryLabel": CATEGORY_LABEL[CATEGORY_MAP[code[0]]],
                "name": clean(m.group(2)),
                "centre": "",
                "itemCount": "",
                "price": "",
                "priceValue": None,
                "audience": [],
                "highlight": "",
                "examSections": [],
                "locations": [],
                "source": "",
                "sourceUrl": "",
                "authorised": False,
                "featured": False,
                "image": f"assets/images/{code.lower()}.svg",
            }
            mode = None
            section = None
            location = None
            continue

        if cur is None:
            continue
        if stripped.startswith("---") or stripped.startswith("===") or stripped.startswith("###"):
            continue

        fm = FIELD_RE.match(stripped)
        if fm:
            key, value = fm.group(1), clean(fm.group(2))
            if key == "計劃名稱":
                cur["name"] = value
            elif key == "體檢中心":
                cur["centre"] = value
            elif key == "ESD Life 標示項目數":
                cur["itemCount"] = value
            elif key == "ESD Life 網上售價":
                cur["price"] = value
                pm = re.search(r"HK\$([\d,]+)", value)
                cur["priceValue"] = int(pm.group(1).replace(",", "")) if pm else None
            elif key.startswith("適用對象及重點"):
                mode = "audience"
                if value:
                    cur["audience"].append(value)
            elif key == "檢查內容":
                mode = "exam"
            elif key.startswith("體檢中心地址"):
                mode = "locations"
            elif key == "出處":
                cur["source"] = value
                mode = None
            elif key == "出處網址":
                cur["sourceUrl"] = value
                mode = None
            continue

        if not stripped:
            continue

        if mode == "audience":
            if stripped.startswith("‧"):
                stripped = stripped.lstrip("‧ ").strip()
            cur["audience"].append(stripped)
            if stripped.startswith("重點檢查項目"):
                pass
            continue

        if mode == "exam":
            if stripped.startswith("■"):
                section = {"title": stripped.lstrip("■ ").strip(), "items": []}
                cur["examSections"].append(section)
            elif stripped.startswith("‧") and section is not None:
                section["items"].append(stripped.lstrip("‧ ").strip())
            continue

        if mode == "locations":
            lm = re.match(r"^\((\d+)\)\s*(.+)$", stripped)
            if lm:
                location = {
                    "name": clean(lm.group(2)),
                    "address": "",
                    "hours": [],
                    "phone": "",
                    "note": "",
                }
                cur["locations"].append(location)
                continue
            if location is None:
                continue
            km = re.match(r"^(地址|辦公時間|電話|備註)：(.*)$", stripped)
            if km:
                k, v = km.group(1), clean(km.group(2))
                if k == "地址":
                    location["address"] = v
                elif k == "辦公時間":
                    location["hours"] = [v] if v else []
                elif k == "電話":
                    location["phone"] = v
                elif k == "備註":
                    location["note"] = v
            elif line.startswith("      ") and location["hours"]:
                # continuation line of office hours
                location["hours"].append(stripped)
            elif line.startswith("      ") and location["note"]:
                location["note"] += " " + stripped
            continue

    flush()

    # Derive a concise highlight from the "重點檢查項目" line(s).
    for p in plans:
        hl = ""
        for i, a in enumerate(p["audience"]):
            if a.startswith("重點檢查項目"):
                parts = []
                for j in range(i + 1, len(p["audience"])):
                    nxt = p["audience"][j]
                    if nxt.startswith("優惠時段條款") or nxt.startswith("重點檢查項目"):
                        break
                    parts.append(nxt)
                    if j + 1 < len(p["audience"]) and p["audience"][j + 1].startswith("優惠時段條款"):
                        break
                hl = "；".join(parts)
                break
        if not hl:
            hl = "；".join(a for a in p["audience"] if not a.startswith("適用於") and not a.startswith("適合"))
        p["highlight"] = hl[:220]

    if len(plans) != 48:
        raise SystemExit(f"Expected 48 plans, got {len(plans)}")

    # Verify no duplicate ids and all have basic data.
    ids = [p["id"] for p in plans]
    assert len(set(ids)) == 48
    for p in plans:
        assert p["centre"] and p["price"] and p["sourceUrl"], p["id"]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(plans, ensure_ascii=False, indent=2), encoding="utf-8")
    js = "/* Auto-generated from 香港體檢計劃資料（共 48 個）.txt — do not edit by hand. */\n" \
         "window.PLANS_DATA = " + json.dumps(plans, ensure_ascii=False, indent=2) + ";\n"
    OUT_JS.write_text(js, encoding="utf-8")
    print(f"Parsed {len(plans)} plans -> {OUT_JSON.relative_to(ROOT)}, {OUT_JS.relative_to(ROOT)}")


if __name__ == "__main__":
    parse()
