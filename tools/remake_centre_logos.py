# -*- coding: utf-8 -*-
"""Rebuild centre identity thumbnails from confirmed sources.

Reads tools/logo_sources.json. Each entry must provide an exact centre name and
either an official logo URL (kind="logo"), a checked-in local asset
(kind="file"), or a neutral wordmark instruction (kind="wordmark"). Every output
is a 640x240 PNG that fits the whole image.

Requires requests, Pillow and resvg-py.
"""
import io
import json
import sys
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "tools" / "logo_sources.json"
OUT = ROOT / "assets" / "images"

CANVAS = (640, 240)
PAD = 16
CONTENT = (CANVAS[0] - PAD * 2, CANVAS[1] - PAD * 2)
BG = (234, 243, 248, 255)
BORDER = (210, 230, 238, 255)
INK = (10, 62, 92, 255)
ACCENT = (10, 158, 152, 255)
FONT_Candidates = [
    Path(r"C:\Windows\Fonts\msyhbd.ttc"),
    Path(r"C:\Windows\Fonts\msyh.ttc"),
    Path(r"C:\Windows\Fonts\simhei.ttf"),
]


def font(size):
    for p in FONT_Candidates:
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default()


def as_rgba(raw, label):
    if b"<svg" in raw[:2048].lower():
        try:
            from resvg_py import svg_to_bytes

            raw = svg_to_bytes(svg_string=raw.decode("utf-8", "ignore"), width=1200)
        except Exception as exc:
            raise RuntimeError("SVG source could not be rendered: %s (%s)" % (label, exc)) from exc
    with Image.open(io.BytesIO(raw)) as im:
        out = im.convert("RGBA")
    out.load()
    if max(out.size) < 80:
        raise RuntimeError("source too small: %s (%s)" % (label, out.size))
    return out


def get_logo(url):
    from urllib.parse import urlparse

    parts = urlparse(url)
    referer = "%s://%s/" % (parts.scheme or "https", parts.netloc)
    resp = requests.get(
        url,
        timeout=25,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
            "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": referer,
        },
    )
    resp.raise_for_status()
    return as_rgba(resp.content, url)


def load_logo(path):
    return as_rgba(path.read_bytes(), str(path))


def content_box(im):
    w, h = im.size
    alpha = im.getchannel("A")
    if alpha.getextrema()[0] < 250:
        box = alpha.getbbox()
        if box and box != (0, 0, w, h):
            return box
    bg = im.getpixel((0, 0))[:3]
    mask = Image.new("L", im.size, 0)
    src, dst = im.load(), mask.load()
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y][:3]
            if max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2])) > 18:
                dst[x, y] = 255
    return mask.getbbox() or (0, 0, w, h)


def trim(im):
    box = content_box(im)
    if not box or box == (0, 0, im.width, im.height):
        return im
    pad = 4
    box = (
        max(0, box[0] - pad),
        max(0, box[1] - pad),
        min(im.width, box[2] + pad),
        min(im.height, box[3] + pad),
    )
    return im.crop(box)


def fit(im):
    scale = min(CONTENT[0] / im.width, CONTENT[1] / im.height)
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(size, Image.LANCZOS)


def wrap(text, fnt, max_width, draw):
    lines = []
    current = ""
    for ch in text:
        candidate = current + ch
        if current and draw.textlength(candidate, font=fnt) > max_width:
            lines.append(current)
            current = ch
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def wordmark(text):
    size = 46
    while size >= 28:
        fnt = font(size)
        probe = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        lines = wrap(text, fnt, CONTENT[0] - 40, probe)
        if len(lines) <= 2:
            break
        size -= 2
    else:
        fnt = font(28)
        lines = wrap(text, fnt, CONTENT[0] - 20, probe)
    line_h = int(size * 1.28)
    total_h = line_h * len(lines)
    im = Image.new("RGBA", (CANVAS[0], total_h + 34), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.rounded_rectangle((im.width // 2 - 30, 0, im.width // 2 + 30, 6), radius=3, fill=ACCENT)
    y = 22
    for line in lines:
        width = draw.textlength(line, font=fnt)
        draw.text(((im.width - width) / 2, y), line, font=fnt, fill=INK)
        y += line_h
    return im


def finish(art):
    art = fit(trim(art))
    canvas = Image.new("RGBA", CANVAS, BG)
    x = (CANVAS[0] - art.width) // 2
    y = (CANVAS[1] - art.height) // 2
    canvas.paste(art, (x, y), art)
    ImageDraw.Draw(canvas).rectangle(
        (x, y, x + art.width - 1, y + art.height - 1), outline=BORDER, width=1
    )
    return canvas


def main():
    entries = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    used = set()
    mapping = {"1": "assets/images/centre-01.png"}
    finish(load_logo(OUT / "logo-mrlab.png")).save(OUT / "centre-01.png", "PNG", optimize=True)
    print("OK 01 香港生物醫學核心化驗所 <- assets/images/logo-mrlab.png")
    for entry in entries:
        idx = int(entry["index"])
        if idx in used:
            raise SystemExit("duplicate index in manifest: %d" % idx)
        used.add(idx)
        name = entry["name"]
        kind = entry.get("kind")
        if kind == "logo":
            urls = entry.get("urls") or [entry["url"]]
            art, source = None, ""
            errors = []
            for url in urls:
                try:
                    art = get_logo(url)
                    source = url
                    break
                except Exception as exc:
                    errors.append("%s: %s" % (url, exc))
            if art is None:
                raise SystemExit("logo fetch failed for %d: %s" % (idx, "; ".join(errors)))
        elif kind == "file":
            path = ROOT / entry["path"]
            art = load_logo(path)
            source = entry["path"]
        elif kind == "wordmark":
            art = wordmark(name)
            source = "wordmark:" + name
        else:
            raise SystemExit("bad kind for index %d" % idx)
        target = OUT / ("centre-%02d.png" % idx)
        finish(art).save(target, "PNG", optimize=True)
        mapping[str(idx)] = "assets/images/" + target.name
        print("OK %02d %s <- %s" % (idx, name, source))
    missing = [i for i in range(2, 32) if i not in used]
    if missing:
        raise SystemExit("manifest missing indexes: %s" % missing)

    (ROOT / "data" / "centre-images.js").write_text(
        "/* 體檢中心識別圖 */\nwindow.CENTRE_IMAGES = "
        + json.dumps(mapping, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    print("updated", len(mapping), "centre image references")


if __name__ == "__main__":
    main()
