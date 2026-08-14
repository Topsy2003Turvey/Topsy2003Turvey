#!/usr/bin/env python3
"""Generate cyberpunk Twilight-style SVG widgets for the GitHub profile README."""

from __future__ import annotations

import base64
import json
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"

W = 850

# Cyberpunk 2077 × Twilight × VS Code
PINK = "#ff2ea6"
PINK_SOFT = "#ffb3ec"
PINK_HOT = "#ff4ecd"
PURPLE = "#bf5fff"
GOLD = "#ff9f43"
CYAN = "#67e8f9"
TEXT = "#ffe6fb"
MUTED = "#c4a0d8"
BG0 = "#120018"
BG1 = "#1a0b24"
BG2 = "#241033"
HEAT = ["#2a1538", "#5c2a78", "#9d4edd", "#e879f9", "#ffd6f5"]


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def write_svg(name: str, body: str) -> None:
    path = ASSETS / name
    path.write_text(body, encoding="utf-8")
    print(f"wrote {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


def svg_open(width: int, height: int) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">'''


def defs_common() -> str:
    return f'''
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22082c"/>
      <stop offset="45%" stop-color="{BG0}"/>
      <stop offset="100%" stop-color="#1a0830"/>
    </linearGradient>
    <linearGradient id="neonStroke" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="50%" stop-color="{PINK}"/>
      <stop offset="100%" stop-color="#7c3aed"/>
    </linearGradient>
    <linearGradient id="barPink" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#c026d3"/>
      <stop offset="100%" stop-color="{PINK}"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="softGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="wave">
      <feTurbulence type="fractalNoise" baseFrequency="0.015 0.04" numOctaves="2" seed="2" result="t">
        <animate attributeName="baseFrequency" values="0.015 0.04;0.03 0.02;0.015 0.04" dur="5s" repeatCount="indefinite"/>
      </feTurbulence>
      <feDisplacementMap in="SourceGraphic" in2="t" scale="7" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
    <clipPath id="cardClip">
      <rect x="4" y="4" width="{W-8}" height="9999" rx="22"/>
    </clipPath>
  </defs>'''


def card_frame(height: int, inner_gold: bool = True) -> str:
    gold = ""
    if inner_gold:
        gold = f'<rect x="12" y="12" width="{W-24}" height="{height-24}" rx="16" fill="none" stroke="{GOLD}" stroke-width="1.2" opacity="0.55"/>'
    return f'''
  <rect x="5" y="5" width="{W-10}" height="{height-10}" rx="22" fill="none" stroke="{PINK}" stroke-width="6" opacity="0.35" filter="url(#glow)"/>
  <rect x="8" y="8" width="{W-16}" height="{height-16}" rx="20" fill="url(#bg)" stroke="url(#neonStroke)" stroke-width="2.5"/>
  {gold}
  <rect x="8" y="-16" width="{W-16}" height="10" fill="{PINK}" opacity="0.07" clip-path="url(#cardClip)">
    <animate attributeName="y" values="-16;{height};-16" dur="5.5s" repeatCount="indefinite"/>
  </rect>'''


def section_label(text: str) -> str:
    return f'<text x="28" y="38" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" font-weight="700" letter-spacing="3">{esc(text)}</text>'


def load_b64(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\x89PNG"):
        mime = "image/png"
    elif raw.startswith(b"\xff\xd8"):
        mime = "image/jpeg"
    elif raw.startswith(b"GIF8"):
        mime = "image/gif"
    elif raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
        mime = "image/webp"
    else:
        mime = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }.get(path.suffix.lower(), "image/jpeg")
    b64 = base64.b64encode(raw).decode("ascii")
    return f"data:{mime};base64,{b64}"


def gen_banner() -> None:
    avatar = load_b64(ASSETS / "avatar.png")
    h = 230
    body = f'''{svg_open(W, h)}
{defs_common()}
  <clipPath id="ava">
    <circle cx="78" cy="115" r="48"/>
  </clipPath>
{card_frame(h)}
  <circle cx="78" cy="115" r="52" fill="none" stroke="{PINK_SOFT}" stroke-width="2.4" filter="url(#glow)">
    <animate attributeName="stroke-opacity" values="0.55;1;0.55" dur="2.4s" repeatCount="indefinite"/>
  </circle>
  <image href="{avatar}" xlink:href="{avatar}" x="30" y="67" width="96" height="96" clip-path="url(#ava)"/>
  <path d="M 148 78 Q 310 58 470 78" fill="none" stroke="{TEXT}" stroke-width="0.7" opacity="0.28"/>
  <text x="148" y="86" fill="{TEXT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">@Topsy2003Turvey</text>
  <text x="148" y="124" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="32" font-weight="800">Stéfan Driaan Turvey</text>
  <text x="148" y="152" fill="{PINK_SOFT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="15">BSc Hons IT · Data Science · Pretoria, ZA</text>
  <g font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="12" font-weight="600" fill="{TEXT}">
    <rect x="148" y="172" width="78" height="26" rx="13" fill="#14081c" stroke="{GOLD}" stroke-width="1.2"/>
    <text x="187" y="190" text-anchor="middle">Python</text>
    <rect x="236" y="172" width="108" height="26" rx="13" fill="#14081c" stroke="{GOLD}" stroke-width="1.2"/>
    <text x="290" y="190" text-anchor="middle">Data Science</text>
    <rect x="354" y="172" width="64" height="26" rx="13" fill="#14081c" stroke="{GOLD}" stroke-width="1.2"/>
    <text x="386" y="190" text-anchor="middle">Java</text>
  </g>
  <text x="792" y="118" text-anchor="end" fill="{PINK}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="52" font-weight="800" filter="url(#softGlow)">44</text>
  <text x="792" y="146" text-anchor="end" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="12" font-weight="700" letter-spacing="2.4">CONTRIBUTIONS</text>
</svg>'''
    write_svg("banner.svg", body)


def _is_cream_background(rgb: tuple[int, int, int]) -> bool:
    r, g, b = (int(c) for c in rgb)
    if min(r, g, b) < 215 or (r + g + b) / 3 < 235:
        return False
    # Hat fur is pink-white (R high, G lower). Real backdrop is cream/neutral.
    if r - g > 8 and b > g - 5:
        return False
    return True


def _background_mask(img) -> list[list[bool]]:
    pixels = img.load()
    w, h = img.size
    seen = [[False] * w for _ in range(h)]
    q: deque[tuple[int, int]] = deque()

    def seed(x: int, y: int) -> None:
        if not seen[y][x] and _is_cream_background(pixels[x, y]):
            seen[y][x] = True
            q.append((x, y))

    for x in range(w):
        seed(x, 0)
        seed(x, h - 1)
        if h > 2:
            seed(x, 1)
            seed(x, h - 2)
    for y in range(h):
        seed(0, y)
        seed(w - 1, y)

    while q:
        x, y = q.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and _is_cream_background(pixels[nx, ny]):
                seen[ny][nx] = True
                q.append((nx, ny))
    return seen


def _punch_backdrop(img):
    """Key out the cream photo backdrop and keep the white hat trim visible."""
    src = img.convert("RGB")
    mask = _background_mask(src)
    pixels = src.load()
    w, h = src.size
    for y in range(h):
        for x in range(w):
            if mask[y][x]:
                pixels[x, y] = (18, 0, 24)
                continue
            r, g, b = pixels[x, y]
            # Keep the Santa hat fur as a bright white-pink band on the dark card.
            if r > 220 and g > 205 and b > 205:
                pixels[x, y] = (255, 244, 250)
    return src


def _blink_frame(img):
    from PIL import ImageDraw

    out = img.copy()
    draw = ImageDraw.Draw(out)
    w, h = out.size
    # Profile eye on the source 184x184 xmas portrait; scale if needed.
    sx, sy = w / 184, h / 184
    cx, cy = 137 * sx, 98 * sy
    rw, rh = 16 * sx, 7 * sy
    lid = (232, 168, 188)
    lash = (52, 28, 38)
    draw.ellipse((cx - rw, cy - rh, cx + rw, cy + rh), fill=lid)
    draw.line((cx - rw + 2, cy + 1, cx + rw - 2, cy + 2), fill=lash, width=max(2, int(3 * sy)))
    return out


def _ascii_lines(img, cols: int, rows: int) -> list[str]:
    from PIL import Image

    img = img.resize((cols, rows), Image.Resampling.LANCZOS)
    chars = " .:-=+*#%@"
    lines = []
    for y in range(rows):
        parts = []
        for x in range(cols):
            r, g, b = img.getpixel((x, y))
            lum = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
            if lum < 0.07:
                parts.append(" ")
                continue
            idx = min(int(lum * (len(chars) - 1)), len(chars) - 1)
            # White hat fur should read as a solid band, not sparse dots.
            if r > 235 and g > 220 and b > 220:
                idx = max(idx, len(chars) - 2)
            ch = chars[idx]
            if ch == " ":
                ch = "."
            parts.append(f'<tspan fill="#{r:02x}{g:02x}{b:02x}">{esc(ch)}</tspan>')
        lines.append("".join(parts))
    return lines


def gen_ascii() -> None:
    from PIL import Image

    src = _punch_backdrop(Image.open(ASSETS / "xmas-girl.gif"))
    cols, rows = 70, 40
    frames = [("open", _ascii_lines(src, cols, rows)), ("blink", _ascii_lines(_blink_frame(src), cols, rows))]
    line_h = 12
    text_y0 = 48
    font_size = 11
    h = text_y0 + rows * line_h + 36

    def frame_xml(name: str, lines: list[str], opacity_values: str, key_times: str) -> str:
        texts = "\n".join(
            f'    <text x="40" y="{text_y0 + i * line_h}" xml:space="preserve" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="{font_size}">{line}</text>'
            for i, line in enumerate(lines)
        )
        return f'''  <g id="ascii-{name}" opacity="{0 if name == "blink" else 1}">
    <animate attributeName="opacity" values="{opacity_values}" keyTimes="{key_times}" dur="3.6s" repeatCount="indefinite"/>
{texts}
  </g>'''

    # Mostly open, then a double-blink like the source GIF.
    open_xml = frame_xml("open", frames[0][1], "1;1;0;1;1;0;1;1", "0;0.78;0.81;0.84;0.88;0.91;0.94;1")
    blink_xml = frame_xml("blink", frames[1][1], "0;0;1;0;0;1;0;0", "0;0.78;0.81;0.84;0.88;0.91;0.94;1")

    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h, inner_gold=False)}
{open_xml}
{blink_xml}
  <text x="{W-28}" y="{h-22}" text-anchor="end" fill="{MUTED}" font-size="10" font-family="Segoe UI, Helvetica, Arial, sans-serif" opacity="0.7">character scan complete</text>
</svg>'''
    write_svg("ascii-portrait.svg", body)


def gen_name() -> None:
    letters = list("STEFAN TURVEY")
    h = 240
    start_x = 86
    gap = 52
    layers = [
        (4, 4, "#4a0d3a", 0.9),
        (2.5, 2.5, "#9d174d", 0.95),
        (1.2, 1.2, PINK, 1.0),
        (0, 0, TEXT, 1.0),
    ]
    glyphs = []
    for i, ch in enumerate(letters):
        x = start_x + i * gap
        if ch == " ":
            continue
        copies = []
        for dx, dy, color, op in layers:
            copies.append(
                f'<text x="{dx}" y="{dy}" fill="{color}" opacity="{op}" font-family="Arial Black, Impact, Segoe UI, sans-serif" font-size="54" font-weight="900">{ch}</text>'
            )
        glyphs.append(
            f'''  <g transform="translate({x},130)">
    <animateTransform attributeName="transform" type="translate" values="{x},118; {x},142; {x},118" dur="2.8s" begin="{i * 0.09:.2f}s" repeatCount="indefinite"/>
    {''.join(copies)}
  </g>'''
        )
    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h)}
  {section_label("HOLOGRAM ID")}
  <g filter="url(#wave)">
{''.join(glyphs)}
  </g>
  <text x="425" y="208" text-anchor="middle" fill="{PINK_SOFT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13" letter-spacing="6">STEFAN TURVEY</text>
</svg>'''
    write_svg("name-wave.svg", body)


def gen_stats() -> None:
    h = 280
    stats = [
        ("0", "Stars", 0.08),
        ("44", "Contributions", 0.86),
        ("1", "Repos", 0.18),
        ("7", "Followers", 0.42),
    ]
    col_w = 190
    x0 = 42
    blocks = []
    for i, (val, label, pct) in enumerate(stats):
        x = x0 + i * col_w
        bw = 150
        fw = int(bw * pct)
        blocks.append(
            f'''  <g transform="translate({x},122)">
    <text x="0" y="38" fill="{PINK}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="36" font-weight="800" filter="url(#glow)">{val}</text>
    <text x="0" y="76" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13">{label}</text>
    <rect x="0" y="92" width="{bw}" height="8" rx="4" fill="#2a1538"/>
    <rect x="0" y="92" width="0" height="8" rx="4" fill="url(#barPink)">
      <animate attributeName="width" from="0" to="{fw}" dur="1.4s" begin="{0.2 + i * 0.18}s" fill="freeze"/>
    </rect>
  </g>'''
        )
    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h, inner_gold=False)}
  {section_label("ANIMATED STATS")}
  <text x="28" y="64" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="700">Profile Signal</text>
  <text x="28" y="88" fill="{MUTED}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13">Live GitHub stats · Twilight / Pretoria</text>
{''.join(blocks)}
</svg>'''
    write_svg("stats.svg", body)


def gen_stack() -> None:
    h = 268
    langs = [
        ("Python", "42%", 0.42, PINK),
        ("Java", "24%", 0.24, PURPLE),
        ("Terraform", "18%", 0.18, GOLD),
        ("Azure", "12%", 0.12, CYAN),
        ("SQL", "4%", 0.04, PINK_SOFT),
    ]
    rows = []
    for i, (name, pct, frac, color) in enumerate(langs):
        y = 108 + i * 28
        bw = 520
        fw = int(bw * frac)
        rows.append(
            f'''  <circle cx="40" cy="{y}" r="5" fill="{color}" filter="url(#glow)"/>
  <text x="56" y="{y+4}" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="14">{name}</text>
  <text x="210" y="{y+4}" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">{pct}</text>
  <rect x="270" y="{y-7}" width="{bw}" height="10" rx="5" fill="#2a1538"/>
  <rect x="270" y="{y-7}" width="0" height="10" rx="5" fill="{color}">
    <animate attributeName="width" from="0" to="{fw}" dur="1.5s" begin="{0.15 + i * 0.16}s" fill="freeze"/>
  </rect>'''
        )
    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h, inner_gold=False)}
  {section_label("ANIMATED STACK")}
  <text x="28" y="62" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="700">Language Stack</text>
  <text x="28" y="84" fill="{MUTED}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="13">Focus-weighted technologies · Data Science Honours</text>
{''.join(rows)}
</svg>'''
    write_svg("stack.svg", body)


def gen_heatmap() -> None:
    data = json.loads((ASSETS / "contributions.json").read_text())
    weeks: list[list[int | None]] = []
    week: list[int | None] = []
    for _date, level in data:
        week.append(int(level))
        if len(week) == 7:
            weeks.append(week)
            week = []
    if week:
        while len(week) < 7:
            week.append(None)
        weeks.append(week)

    cell, gap = 11, 3
    step = cell + gap
    gx, gy = 48, 108
    grid_w = len(weeks) * step
    grid_h = 7 * step
    ship_y = gy + grid_h + 42
    h = ship_y + 52

    cells = []
    for wi, week in enumerate(weeks):
        x = gx + wi * step
        begin = (wi / max(len(weeks) - 1, 1)) * 3.0
        for di, level in enumerate(week):
            if level is None:
                continue
            y = gy + di * step
            fill = HEAT[level]
            if level:
                cells.append(
                    f'''  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}">
    <animate attributeName="fill" values="{fill};{PINK};#ffffff;{fill};{fill}" keyTimes="0;0.04;0.07;0.12;1" dur="6s" begin="{begin:.2f}s" repeatCount="indefinite"/>
  </rect>'''
                )
            else:
                cells.append(
                    f'  <rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{fill}"/>'
                )

    months = [
        ("Aug", 0),
        ("Sep", 4),
        ("Oct", 8),
        ("Nov", 12),
        ("Dec", 17),
        ("Jan", 21),
        ("Feb", 25),
        ("Mar", 29),
        ("Apr", 34),
        ("May", 38),
        ("Jun", 43),
        ("Jul", 47),
        ("Aug", 51),
    ]
    month_xml = []
    for label, col in months:
        if col < len(weeks):
            month_xml.append(
                f'<text x="{gx + col * step}" y="{gy - 10}" fill="{MUTED}" font-size="10" font-family="Segoe UI, Helvetica, Arial, sans-serif">{label}</text>'
            )

    legend = []
    for i, c in enumerate(HEAT):
        legend.append(
            f'<rect x="{W - 168 + i * 16}" y="56" width="12" height="12" rx="2" fill="{c}"/>'
        )

    laser_group = []
    for i, delay in enumerate((0, 0.35, 0.7, 1.05)):
        laser_group.append(
            f'''    <rect x="-1.2" y="0" width="2.4" height="18" rx="1" fill="{CYAN}" opacity="0">
      <animate attributeName="y" values="0;-{grid_h + 50};0" dur="1.4s" begin="{delay}s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.05;0.55;0.7;1" dur="1.4s" begin="{delay}s" repeatCount="indefinite"/>
    </rect>'''
        )

    x_left = gx
    x_right = gx + grid_w - 12
    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h, inner_gold=False)}
  {section_label("ANIMATED HEATMAP")}
  <text x="28" y="62" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="20" font-weight="700">Contribution Activity</text>
  <text x="28" y="82" fill="{MUTED}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="12">44 contributions in the last year</text>
  <text x="{W-196}" y="66" fill="{MUTED}" font-size="11" font-family="Segoe UI, Helvetica, Arial, sans-serif">Less</text>
  {''.join(legend)}
  <text x="{W-28}" y="66" text-anchor="end" fill="{MUTED}" font-size="11" font-family="Segoe UI, Helvetica, Arial, sans-serif">More</text>
  <rect x="{gx}" y="{gy}" width="{cell}" height="{grid_h}" rx="2" fill="{PINK}" opacity="0.18">
    <animate attributeName="x" values="{gx};{gx + grid_w - cell};{gx}" dur="6s" repeatCount="indefinite"/>
  </rect>
  {''.join(month_xml)}
{''.join(cells)}
  <g>
    <animateTransform attributeName="transform" type="translate" values="{x_left},{ship_y}; {x_right},{ship_y}; {x_left},{ship_y}" dur="6s" repeatCount="indefinite"/>
    {''.join(laser_group)}
    <polygon points="0,-16 -11,10 0,4 11,10" fill="{PINK}" filter="url(#glow)"/>
    <polygon points="0,-10 -6,6 0,2 6,6" fill="{TEXT}"/>
    <rect x="-1.5" y="-24" width="3" height="10" rx="1" fill="{CYAN}"/>
    <polygon points="-5,10 -8,16 0,12 8,16 5,10" fill="{GOLD}" opacity="0.9">
      <animate attributeName="opacity" values="0.35;1;0.35" dur="0.18s" repeatCount="indefinite"/>
    </polygon>
  </g>
</svg>'''
    write_svg("heatmap.svg", body)


def gen_whoami() -> None:
    h = 168
    body = f'''{svg_open(W, h)}
{defs_common()}
{card_frame(h, inner_gold=False)}
  {section_label("WHOAMI")}
  <text x="28" y="64" fill="{CYAN}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">topsy2003turvey@night-city:~$ whoami</text>
  <text x="28" y="92" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="16">Studying for a Bachelor of Science Honours in IT Specializing in Data Science</text>
  <text x="28" y="118" fill="{PINK_SOFT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="13">location: South Africa  ·  timezone: UTC+02  ·  status: Focusing</text>
  <text x="28" y="142" fill="{MUTED}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="12">Butler: Goeiedag, Meneer! Mag u 'n produktiewe sessie hê.</text>
</svg>'''
    write_svg("whoami.svg", body)


def gen_link_button(filename: str, label: str, sub: str) -> None:
    bw, bh = 200, 56
    body = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{bw}" height="{bh}" viewBox="0 0 {bw} {bh}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#22082c"/>
      <stop offset="100%" stop-color="#120018"/>
    </linearGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect x="2" y="2" width="{bw-4}" height="{bh-4}" rx="14" fill="url(#bg)" stroke="{PINK}" stroke-width="2" filter="url(#glow)"/>
  <text x="{bw/2}" y="26" text-anchor="middle" fill="{TEXT}" font-family="Segoe UI, Helvetica, Arial, sans-serif" font-size="15" font-weight="700">{esc(label)}</text>
  <text x="{bw/2}" y="44" text-anchor="middle" fill="{PINK_SOFT}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="10">{esc(sub)}</text>
</svg>'''
    write_svg(filename, body)


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    gen_banner()
    gen_ascii()
    gen_name()
    gen_stats()
    gen_stack()
    gen_heatmap()
    gen_whoami()
    gen_link_button("link-github.svg", "GitHub", "@Topsy2003Turvey")
    gen_link_button("link-linkedin.svg", "LinkedIn", "stéfan-turvey")
    gen_link_button("link-stackoverflow.svg", "Stack Overflow", "71 reputation")
    gen_link_button("link-discord.svg", "Discord", "open profile")
    print("done")


if __name__ == "__main__":
    main()
