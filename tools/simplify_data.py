# -*- coding: utf-8 -*-
"""Turn plan data into a plain offers list and correct E Plus contact details."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
DROP_FIELDS = {
    "source", "sourceUrl", "sourceCheckedAt", "dataNote", "validityNote",
    "hoursSourceUrl", "hoursCheckedAt",
}

REPLACE = [
    ("男女計劃按貼文所列部位有不同超聲波項目", "男女計劃的超聲波部位不同"),
    ("DR70 癌症風險指標（來源貼文用語；不是確診檢查）", "DR70 癌症風險指標"),
    ("其他檢查類別（按貼文整理）", "其他檢查類別"),
    ("大便隱血（貼文列作腸癌評估）", "大便隱血"),
    ("貼文列出的期間限定加送（需確認）", "期間限定加送"),
    ("貼文以長者及銀髮族為對象", "適合長者及銀髮族"),
    ("HPV：23種，包括14種高危型（依貼文）", "HPV：23種，包括14種高危型"),
    ("海報列出的癌症名稱不是逐種確診測試。", ""),
    ("n.a.（來源頁面未列出此地點的辦公時間）", "辦公時間請查詢"),
    ("電話 6235 0198（頁面註明可經 WhatsApp 查詢／預約）", "電話 6235 0198"),
    ("（2026-11-19 所見，僅供參考）", ""),
]

EPLUS_ADDRESSES = {
    "尖沙咀": "九龍尖沙咀加拿分道18號恒生尖沙咀大廈7樓704室",
    "佐敦": "九龍佐敦彌敦道301-309號嘉賓商業大廈9樓911室",
    "中環": "香港中環德輔道中21-23號歐陸貿易中心17樓1701室",
    "荃灣": "新界荃灣青山公路荃灣段264-298號南豐中心12樓1211室",
}
EPLUS_HOURS = [
    "星期一至星期日及公眾假期 09:00–17:30",
    "午膳時間 13:00–14:00",
    "聖誕及農曆新年休息",
]


def clean_text(value):
    if not isinstance(value, str):
        return value
    for old, new in REPLACE:
        value = value.replace(old, new)
    # Remove any remaining parenthetical provenance/disclaimer notes.
    value = re.sub(
        r"（[^）]*(?:貼文|海報|來源|出處|公開|會員|頁面|僅供|參考|核對|整理|為準|註明|確認|原價|標示)[^）]*）",
        "",
        value,
    )
    return re.sub(r"\s{2,}", " ", value).strip()


def clean_object(obj):
    if isinstance(obj, dict):
        return {k: clean_object(v) for k, v in obj.items() if k not in DROP_FIELDS}
    if isinstance(obj, list):
        return [clean_object(v) for v in obj]
    return clean_text(obj)


def load_js(path, var):
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\." + var + r"\s*=\s*(\[.*\])\s*;?\s*$", text, re.S)
    if not match:
        raise SystemExit("cannot parse " + str(path))
    return json.loads(match.group(1))


def save_js(path, var, data):
    path.write_text(
        "/* 體檢優惠資料 */\nwindow." + var + " = " +
        json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8",
    )


plans_path = ROOT / "data" / "plans.json"
plans = json.loads(plans_path.read_text(encoding="utf-8"))
featured_path = ROOT / "data" / "featured.js"
featured = load_js(featured_path, "FEATURED_DATA")

for item in plans + featured:
    if isinstance(item.get("price"), str):
        match = re.match(r"(HK\$[\d,]+)", item["price"])
        if match:
            item["price"] = match.group(1)

for item in featured:
    if item.get("id") == "e06":
        for loc in item.get("locations", []):
            name = loc.get("name", "")
            if name in EPLUS_ADDRESSES:
                loc["address"] = EPLUS_ADDRESSES[name]
            loc["hours"] = list(EPLUS_HOURS)
            loc["phone"] = "6661 8628"
            loc.pop("note", None)

plans = clean_object(plans)
featured = clean_object(featured)

plans_path.write_text(json.dumps(plans, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
save_js(ROOT / "data" / "plans.js", "PLANS_DATA", plans)
save_js(featured_path, "FEATURED_DATA", featured)

print("simplified", len(plans), "plans and", len(featured), "featured offers")
