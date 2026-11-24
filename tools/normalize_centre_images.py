# -*- coding: utf-8 -*-
"""Legacy thumbnail normaliser.

Superseded by remake_centre_logos.py, which uses confirmed identity sources.
Kept only for reference.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

CANVAS = (640, 240)
PAD = 16
CONTENT = (CANVAS[0] - PAD * 2, CANVAS[1] - PAD * 2)
BG = (234, 243, 248, 255)
BORDER = (210, 230, 238, 255)


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


def crop_content(im):
    box = content_box(im)
    if box and box != (0, 0, im.width, im.height):
        pad = 4
        box = (
            max(0, box[0] - pad),
            max(0, box[1] - pad),
            min(im.width, box[2] + pad),
            min(im.height, box[3] + pad),
        )
        return im.crop(box)
    return im


def fit(im):
    scale = min(CONTENT[0] / im.width, CONTENT[1] / im.height)
    size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    return im.resize(size, Image.LANCZOS)


def placeholder():
    im = Image.new("RGBA", CANVAS, BG)
    draw = ImageDraw.Draw(im)
    for x in range(CANVAS[0]):
        t = x / CANVAS[0]
        color = (
            round(6 + (10 - 6) * t),
            round(43 + (158 - 43) * t),
            round(77 + (152 - 77) * t),
            255,
        )
        draw.line((x, 0, x, CANVAS[1]), fill=color)
    draw.ellipse((520, -50, 660, 90), fill=(255, 255, 255, 22))
    draw.ellipse((-40, 170, 90, 300), fill=(255, 255, 255, 18))
    draw.ellipse((60, 92, 128, 160), fill=(255, 255, 255, 235))
    draw.line(
        [(76, 126), (86, 126), (92, 112), (102, 142), (110, 126), (122, 126)],
        fill=(10, 158, 152, 255),
        width=5,
        joint="curve",
    )
    draw.rounded_rectangle((180, 108, 430, 120), radius=6, fill=(255, 255, 255, 220))
    draw.rounded_rectangle((180, 134, 360, 144), radius=5, fill=(255, 255, 255, 140))
    return im


def normalise(source):
    with Image.open(source) as raw:
        im = raw.convert("RGBA")
    im.load()
    im = crop_content(im)
    im = fit(im)
    canvas = Image.new("RGBA", CANVAS, BG)
    x = (CANVAS[0] - im.width) // 2
    y = (CANVAS[1] - im.height) // 2
    canvas.paste(im, (x, y), im)
    ImageDraw.Draw(canvas).rectangle((x, y, x + im.width - 1, y + im.height - 1), outline=BORDER, width=1)
    return canvas


def main():
    roots = [Path(p).resolve() for p in sys.argv[1:]] or [Path(__file__).resolve().parents[1]]
    for root in roots:
        out_dir = root / "assets" / "images"
        out_dir.mkdir(parents=True, exist_ok=True)
        for idx in range(1, 32):
            name = "centre-%02d.png" % idx
            target = out_dir / name
            source = None
            if idx == 1:
                source = out_dir / "logo-mrlab.png"
            else:
                for ext in ("png", "jpg", "jpeg", "webp"):
                    candidate = out_dir / ("centre-%02d.%s" % (idx, ext))
                    if candidate.exists():
                        source = candidate
                        break
            try:
                image = normalise(source) if source and source.exists() else placeholder()
            except Exception as exc:
                print("WARN", name, "using placeholder:", exc)
                image = placeholder()
            image.save(target, "PNG", optimize=True)
            print("OK", name, "from", source.name if source else "placeholder")


if __name__ == "__main__":
    main()
