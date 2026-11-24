# -*- coding: utf-8 -*-
"""Try to source centre images online; fall back to local generated thumbnails."""
import json
import mimetypes
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images"


def get(url, binary=False, timeout=12):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; site-builder)"})
    data = urllib.request.urlopen(req, timeout=timeout).read()
    return data if binary else data.decode("utf-8", "ignore")


def text_of(html):
    for pat in [
        r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"',
        r'<meta[^>]+content="([^"]+)"[^>]+property="og:image"',
        r'<meta[^>]+name="twitter:image"[^>]+content="([^"]+)"',
        r'<link[^>]+rel="apple-touch-icon"[^>]+href="([^"]+)"',
    ]:
        m = re.search(pat, html, re.I)
        if m:
            return m.group(1).replace("&amp;", "&")
    return ""


def absolute(base, url):
    return urllib.parse.urljoin(base, url)


def image_ext(data, ctype, url):
    head = data[:16]
    if b"<svg" in head or "svg" in ctype:
        return "svg"
    if head.startswith(b"\x89PNG"):
        return "png"
    if head.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if b"WEBP" in head:
        return "webp"
    guess = mimetypes.guess_extension(ctype.split(";")[0].strip())
    if guess in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
        return "jpg" if guess == ".jpeg" else guess.lstrip(".")
    return ""


def centre_names():
    featured = (ROOT / "data" / "featured.js").read_text(encoding="utf-8")
    f = json.loads(re.search(r"window\.FEATURED_DATA\s*=\s*(\[.*\])\s*;?\s*$", featured, re.S).group(1))
    plans = json.loads((ROOT / "data" / "plans.json").read_text(encoding="utf-8"))
    seen = []
    for item in f + plans:
        if item["centre"] not in seen:
            seen.append(item["centre"])
    return ["香港生物醫學核心化驗所", "醫家健康體檢中心"] + [c for c in seen if c not in ("香港生物醫學核心化驗所", "醫家健康體檢中心")]


mapping = {"2": "assets/images/centre-02.png"}  # 醫家健康體檢中心官方網站圖片
names = centre_names()
for idx in range(3, len(names) + 1):
    name = names[idx - 1]
    got = False
    try:
        q = urllib.parse.quote(name + " 香港 中心")
        rss = get("https://www.bing.com/search?format=rss&q=" + q)
        links = [re.sub(r"&amp;", "&", x) for x in re.findall(r"<link>([^<]+)</link>", rss)]
        links = [x for x in links if "bing.com" not in x][:3]
        for link in links:
            try:
                html = get(link)
                img = text_of(html)
                if not img:
                    continue
                img = absolute(link, img)
                data = get(img, binary=True)
                req = urllib.request.Request(img, headers={"User-Agent": "Mozilla/5.0"}, method="HEAD")
                try:
                    ctype = urllib.request.urlopen(req, timeout=8).headers.get("Content-Type", "")
                except Exception:
                    ctype = ""
                ext = image_ext(data, ctype, img)
                if not ext or len(data) > 3_000_000 or len(data) < 600:
                    continue
                fname = "centre-%02d.%s" % (idx, ext)
                (OUT / fname).write_bytes(data)
                mapping[str(idx)] = "assets/images/" + fname
                print("OK", idx, name, fname, len(data))
                got = True
                break
            except Exception as e:
                continue
    except Exception:
        pass
    if not got:
        print("FALLBACK", idx, name)

print("sourced", len(mapping), "of", len(names) - 1)
(ROOT / "data" / "centre-images.js").write_text(
    "/* 體檢中心識別圖 */\nwindow.CENTRE_IMAGES = " + json.dumps(mapping, ensure_ascii=False, indent=2) + ";\n",
    encoding="utf-8",
)
app = ROOT / "assets" / "js" / "app.js"
text = app.read_text(encoding="utf-8")
old = "var CENTRE_IMAGES = window.CENTRE_IMAGES || {};"
new = "var CENTRE_IMAGES = " + json.dumps(mapping, ensure_ascii=False) + ";"
if old in text:
    app.write_text(text.replace(old, new), encoding="utf-8")
    print("patched app.js")
