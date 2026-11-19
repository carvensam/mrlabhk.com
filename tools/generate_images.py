# -*- coding: utf-8 -*-
"""Generate one distinct, professional medical-style SVG image per plan."""
import hashlib
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "assets" / "images"
IMG.mkdir(parents=True, exist_ok=True)

CODES = (
    [f"e{i:02d}" for i in range(1, 7)]
    + [f"g{i:02d}" for i in range(1, 13)]
    + [f"a{i:02d}" for i in range(1, 13)]
    + [f"w{i:02d}" for i in range(1, 13)]
    + [f"c{i:02d}" for i in range(1, 13)]
)

CAT = {
    "e": ("精選體檢", "#0ea5a4", "#0f4c81"),
    "g": ("一般／全身", "#1d9fd8", "#123f77"),
    "a": ("腹腔相關", "#17a2a2", "#0d4b66"),
    "w": ("女性健康", "#c04f8d", "#173f72"),
    "c": ("癌症篩查", "#7b61c9", "#16386e"),
}

PALETTES = [
    ("#0b3d6e", "#0e8f9e", "#62d6e6"),
    ("#0f4c81", "#1490b5", "#8fe3ee"),
    ("#123f77", "#0e9a8c", "#7ce0cc"),
    ("#16386e", "#3f7fd1", "#b6d8ff"),
    ("#0c4a63", "#0f9aa8", "#a5f0e6"),
    ("#1b3a6b", "#2c8fc4", "#a7dcf5"),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def waveform(seed, y, width, amp, freq):
    r = random.Random(seed + 31)
    pts = []
    steps = 34
    for i in range(steps + 1):
        x = i * width / steps
        v = 0.0
        if 8 <= i <= 12:
            v = -amp * 1.15
        elif 12 < i <= 15:
            v = amp * 0.85
        elif 19 <= i <= 22:
            v = -amp * 0.55
        else:
            v = math_sin(i * freq + seed % 7) * amp * 0.14
        pts.append(f"{x:.1f},{y + v:.1f}")
    return " ".join(pts)


def math_sin(x):
    import math
    return math.sin(x)


def icon(kind, cx, cy, color):
    """Return SVG markup for a simple, clean medical icon."""
    if kind == 0:  # medical cross
        return (
            f'<g opacity=".92" stroke="{color}" stroke-width="7" fill="none" stroke-linejoin="round">'
            f'<rect x="{cx-46}" y="{cy-18}" width="92" height="36" rx="9"/>'
            f'<rect x="{cx-18}" y="{cy-46}" width="36" height="92" rx="9"/></g>'
        )
    if kind == 1:  # ultrasound arcs
        s = ""
        for i in range(4):
            r = 26 + i * 17
            s += f'<path d="M {cx-r} {cy+30} A {r} {r} 0 0 1 {cx+r} {cy+30}" fill="none" stroke="{color}" stroke-width="5" opacity="{0.85-i*0.16:.2f}"/>'
        s += f'<circle cx="{cx}" cy="{cy+30}" r="7" fill="{color}"/>'
        return s
    if kind == 2:  # shield
        return (
            f'<path d="M {cx} {cy-58} L {cx+52} {cy-38} L {cx+52} {cy+6} '
            f'Q {cx+52} {cy+48} {cx} {cy+66} Q {cx-52} {cy+48} {cx-52} {cy+6} '
            f'L {cx-52} {cy-38} Z" fill="none" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M {cx-22} {cy} L {cx-6} {cy+17} L {cx+25} {cy-19}" fill="none" stroke="{color}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        )
    if kind == 3:  # DNA helix
        s = ""
        for i in range(5):
            y = cy - 44 + i * 22
            s += f'<line x1="{cx-30}" y1="{y}" x2="{cx+30}" y2="{y}" stroke="{color}" stroke-width="4" opacity=".55"/>'
        s += f'<path d="M {cx-30} {cy-52} C {cx+40} {cy-26}, {cx-40} {cy+26}, {cx+30} {cy+52}" fill="none" stroke="{color}" stroke-width="6"/>'
        s += f'<path d="M {cx+30} {cy-52} C {cx-40} {cy-26}, {cx+40} {cy+26}, {cx-30} {cy+52}" fill="none" stroke="{color}" stroke-width="6" opacity=".65"/>'
        return s
    # stethoscope / heart pulse
    return (
        f'<path d="M {cx-12} {cy+20} C {cx-52} {cy-10}, {cx-28} {cy-58}, {cx} {cy-32} '
        f'C {cx+28} {cy-58}, {cx+52} {cy-10}, {cx+12} {cy+20} L {cx} {cy+34} Z" '
        f'fill="none" stroke="{color}" stroke-width="7" stroke-linejoin="round"/>'
        f'<path d="M {cx-58} {cy+6} L {cx-28} {cy+6} L {cx-16} {cy-12} L {cx} {cy+22} L {cx+16} {cy-12} L {cx+28} {cy+6} L {cx+58} {cy+6}" '
        f'fill="none" stroke="{color}" stroke-width="4" opacity=".8"/>'
    )


def generate(code):
    h = hashlib.sha256(code.encode()).hexdigest()
    seed = int(h[:8], 16)
    r = random.Random(seed)
    prefix = code[0]
    label, accent, deep = CAT[prefix]
    c1, c2, c3 = PALETTES[seed % len(PALETTES)]
    angle = 110 + seed % 90
    icon_kind = {"e": 2, "g": 0, "a": 1, "w": 3, "c": 4}[prefix]
    n_circles = 3 + seed % 4
    amp = 12 + seed % 16
    freq = 0.7 + (seed % 9) * 0.11
    dot_op = 0.10 + (seed % 4) * 0.025
    code_up = code.upper()

    circles = ""
    for i in range(n_circles):
        rad = 120 + i * 62 + (seed % 17)
        circles += (
            f'<circle cx="1010" cy="120" r="{rad}" fill="none" stroke="{c3}" '
            f'stroke-width="2" opacity="{0.10 + i*0.025:.2f}"/>'
        )

    dots = ""
    for row in range(6):
        for col in range(10):
            x = 62 + col * 56 + (row % 2) * 18
            y = 548 + row * 32
            dots += f'<circle cx="{x}" cy="{y}" r="2.6" fill="{c3}" opacity="{dot_op:.2f}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 750" width="1200" height="750">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1" gradientTransform="rotate({angle} .5 .5)">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="58%" stop-color="{c2}"/>
      <stop offset="100%" stop-color="{c3}"/>
    </linearGradient>
    <radialGradient id="glow" cx="30%" cy="28%" r="70%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity=".24"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#041c3a" stop-opacity="0"/>
      <stop offset="100%" stop-color="#041c3a" stop-opacity=".34"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="750" fill="url(#bg)"/>
  <rect width="1200" height="750" fill="url(#glow)"/>
  {circles}
  <path d="M0 620 L1200 620 L1200 750 L0 750 Z" fill="url(#fade)"/>
  {dots}
  <g transform="translate(60 52)">
    <rect x="0" y="0" width="196" height="44" rx="22" fill="#ffffff" fill-opacity=".16" stroke="#ffffff" stroke-opacity=".28"/>
    <circle cx="24" cy="22" r="7" fill="#ffffff" fill-opacity=".9"/>
    <text x="42" y="29" font-family="'Noto Sans TC','Microsoft JhengHei',sans-serif" font-size="18" fill="#ffffff" letter-spacing="1">{esc(label)}</text>
  </g>
  <g transform="translate(598 320)">
    <circle r="118" fill="#ffffff" fill-opacity=".07"/>
    <circle r="118" fill="none" stroke="#ffffff" stroke-opacity=".30" stroke-width="2"/>
    {icon(icon_kind, 0, 0, "#ffffff")}
  </g>
  <polyline points="{waveform(seed, 596, 1200, amp, freq)}" fill="none" stroke="{c3}" stroke-width="3" opacity=".55"/>
  <text x="62" y="700" font-family="'Segoe UI',Arial,sans-serif" font-size="86" font-weight="700" fill="#ffffff" fill-opacity=".13" letter-spacing="6">{code_up}</text>
  <text x="1138" y="704" text-anchor="end" font-family="'Segoe UI',Arial,sans-serif" font-size="20" fill="#ffffff" fill-opacity=".45" letter-spacing="3">MRLAB · HEALTH</text>
</svg>'''

    (IMG / f"{code}.svg").write_text(svg, encoding="utf-8")


def generate_logo():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 64" width="240" height="64">
  <rect width="240" height="64" rx="14" fill="#0b3d6e"/>
  <g transform="translate(32 32)">
    <circle r="21" fill="none" stroke="#62d6e6" stroke-width="3" opacity=".8"/>
    <path d="M-8 0 L-3 0 L0 -8 L4 10 L7 0 L12 0" fill="none" stroke="#ffffff" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
  </g>
  <text x="66" y="28" font-family="'Segoe UI',Arial,sans-serif" font-size="21" font-weight="700" fill="#ffffff" letter-spacing="1">MR LAB</text>
  <text x="66" y="47" font-family="'Noto Sans TC','Microsoft JhengHei',sans-serif" font-size="12" fill="#8fe3ee" letter-spacing="2">化驗所優惠站</text>
</svg>'''
    (IMG / "logo.svg").write_text(svg, encoding="utf-8")


def generate_favicon():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="14" fill="#0b3d6e"/>
  <path d="M12 33 L24 33 L29 20 L35 45 L40 33 L52 33" fill="none" stroke="#62d6e6" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
    (IMG / "favicon.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    for c in CODES:
        generate(c)
    generate_logo()
    generate_favicon()
    print(f"Generated {len(CODES)} plan images + logo + favicon in {IMG.relative_to(ROOT)}")
