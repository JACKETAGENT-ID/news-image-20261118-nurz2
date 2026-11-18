#!/usr/bin/env python3
"""Draw 'APEC Dawn' — one editorial image summing up Wednesday 18 November 2026.

Original PIL illustration, no external assets. Output: entry.png, 1024x1024.
Layout: date banner on top, dawn skyline of Shenzhen with three flags and a
negotiation table (APEC summit), four captioned mini-scenes below, ticker line.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def flag_china(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.30
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.18), (0.68, 0.32), (0.68, 0.52), (0.55, 0.66)]:
        px, py = x + w * sx, y + h * sy
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 222, 0))


def flag_usa(d, x, y, w, h):
    for i in range(13):
        d.rectangle([x, y + i * h / 13, x + w, y + (i + 1) * h / 13],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + h * 7 / 13], fill=(60, 59, 110))
    for r in range(4):
        for c in range(5):
            px = x + 8 + c * (w * 0.4 - 14) / 4
            py = y + 6 + r * (h * 7 / 13 - 12) / 3
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 255, 255))


def flag_russia(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def draw_flag(d, kind, x, y, w=74, h=48):
    d.line([(x, y - 118), (x, y)], fill=(40, 40, 40), width=4)
    d.ellipse([x - 4, y - 124, x + 4, y - 116], fill=(255, 200, 60))
    if kind == "china":
        flag_china(d, x + 2, y - 118, w, h)
    elif kind == "usa":
        flag_usa(d, x + 2, y - 118, w, h)
    else:
        flag_russia(d, x + 2, y - 118, w, h)


def skyline(d, base_y):
    """Shenzhen dawn skyline silhouettes with lit windows."""
    towers = [
        (0, 300, 70, 210), (70, 260, 60, 250), (130, 330, 56, 180),
        (186, 210, 64, 300), (250, 290, 58, 220), (308, 240, 62, 270),
        (370, 320, 54, 190), (424, 180, 66, 330), (490, 280, 58, 230),
        (548, 230, 60, 280), (608, 310, 56, 200), (664, 200, 64, 310),
        (728, 270, 58, 240), (786, 330, 54, 180), (840, 250, 62, 260),
        (902, 300, 60, 210), (962, 340, 62, 170),
    ]
    for x, top, w, _h in towers:
        d.rectangle([x, top, x + w, base_y], fill=(38, 32, 66))
        # antenna on the two tallest
        if top <= 210:
            d.line([(x + w // 2, top), (x + w // 2, top - 34)], fill=(38, 32, 66), width=3)
            d.ellipse([x + w // 2 - 3, top - 40, x + w // 2 + 3, top - 34], fill=(255, 90, 60))
    # lit windows
    import random
    rnd = random.Random(1811)
    for x, top, w, _h in towers:
        for _ in range(26):
            wx = x + 6 + rnd.randrange(0, max(1, w - 12))
            wy = top + 10 + rnd.randrange(0, max(1, base_y - top - 16))
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 196, 90))


def table_scene(d, y0, y1):
    """Negotiation table silhouette in the foreground."""
    d.rectangle([0, y0, W, y1], fill=(24, 20, 48))
    # table
    d.ellipse([180, y0 + 26, 844, y0 + 78], fill=(58, 44, 96))
    d.rectangle([200, y0 + 52, 824, y0 + 66], fill=(58, 44, 96))
    # chairs + seated silhouettes
    for cx in (260, 400, 540, 680, 790):
        d.ellipse([cx - 26, y0 - 26, cx + 26, y0 + 26], fill=(14, 12, 30))
        d.rectangle([cx - 30, y0 + 18, cx + 30, y0 + 44], fill=(14, 12, 30))
    # flags on the table
    for fx, col in [(330, (222, 41, 16)), (512, (60, 59, 110)), (694, (213, 0, 50))]:
        d.rectangle([fx - 14, y0 + 2, fx + 14, y0 + 18], fill=col)
        d.line([(fx, y0 + 2), (fx, y0 - 16)], fill=(200, 200, 200), width=2)
    d.text((512, y0 + 84), "APEC LEADERS MEET IN SHENZHEN",
           font=font(SANS_B, 20), fill=(255, 214, 130), anchor="mt")


def panel_drone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(23, 58, 86))
    d.rectangle([x, y + h - 42, x + w, y + h], fill=(16, 110, 140))
    for i in range(3):
        d.arc([x + 14 + i * 74, y + h - 46, x + 66 + i * 74, y + h - 14],
              180, 360, fill=(255, 255, 255), width=3)
    cx, cy = x + w // 2, y + 58
    d.rectangle([cx - 26, cy - 10, cx + 26, cy + 10], fill=(200, 200, 205))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 200, 60))
    for dx in (-34, 34):
        d.line([(cx + dx - 22, cy - 16), (cx + dx + 22, cy - 16)], fill=(255, 255, 255), width=3)
        d.ellipse([cx + dx - 6, cy - 20, cx + dx + 6, cy - 8], fill=(180, 180, 180))
    d.line([(cx - 26, cy), (cx - 40, cy - 12)], fill=(200, 200, 200), width=3)
    d.line([(cx + 26, cy), (cx + 40, cy - 12)], fill=(200, 200, 200), width=3)


def panel_chip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 84, 52))
    cx, cy = x + w // 2, y + 62
    for i in range(5):
        off = -40 + i * 20
        d.line([(cx + off, y + 18), (cx + off, y + 32)], fill=(255, 214, 90), width=4)
        d.line([(cx + off, y + 92), (cx + off, y + 106)], fill=(255, 214, 90), width=4)
        d.line([(x + 18, cy + off), (x + 32, cy + off)], fill=(255, 214, 90), width=4)
        d.line([(x + w - 32, cy + off), (x + w - 18, cy + off)], fill=(255, 214, 90), width=4)
    d.rectangle([cx - 44, cy - 44, cx + 44, cy + 44], fill=(20, 20, 24), outline=(255, 214, 90), width=3)
    d.rectangle([cx - 26, cy - 26, cx + 26, cy + 26], fill=(60, 180, 120))
    d.text((cx, cy), "AI", font=font(SANS_B, 26), fill=(255, 255, 255), anchor="mm")


def panel_dove(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 84, 58))
    cx, cy = x + w // 2, y + 62
    d.ellipse([cx - 52, cy - 22, cx + 52, cy + 22], fill=(245, 245, 240))
    d.ellipse([cx + 34, cy - 34, cx + 66, cy - 6], fill=(245, 245, 240))
    d.polygon([(cx + 58, cy - 26), (cx + 84, cy - 30), (cx + 62, cy - 12)], fill=(255, 180, 60))
    d.ellipse([cx + 52, cy - 30, cx + 58, cy - 24], fill=(20, 20, 20))
    d.arc([cx - 34, cy - 34, cx + 26, cy + 6], 200, 340, fill=(180, 180, 170), width=4)
    d.line([(cx - 52, cy + 14), (cx - 78, cy + 30)], fill=(245, 245, 240), width=10)
    d.line([(cx - 52, cy + 14), (cx - 72, cy + 38)], fill=(245, 245, 240), width=8)
    # olive branch
    d.line([(cx - 70, cy + 44), (cx - 20, cy + 30)], fill=(90, 140, 60), width=3)
    for ox in (-64, -52, -40, -28):
        d.ellipse([ox - 5, cy + 38, ox + 5, cy + 46], fill=(110, 170, 70))


def panel_voyager(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 34))
    import random
    rnd = random.Random(1977)
    for _ in range(28):
        sx = x + rnd.randrange(6, w - 6)
        sy = y + rnd.randrange(6, h - 6)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    cx, cy = x + w // 2, y + 58
    d.line([(x + 12, y + h - 14), (cx, cy)], fill=(120, 200, 255), width=2)
    d.polygon([(cx - 8, cy - 8), (cx + 30, cy - 26), (cx + 30, cy + 10), (cx - 8, cy + 8)],
              fill=(220, 220, 220))
    d.ellipse([cx + 22, cy - 30, cx + 44, cy - 8], fill=(255, 255, 255), outline=(180, 180, 180))
    d.line([(cx - 8, cy), (cx - 44, cy + 18)], fill=(200, 200, 200), width=4)
    d.ellipse([cx + 60, cy - 52, cx + 92, cy - 20], fill=(255, 200, 80))
    d.text((x + w - 8, y + 116), "1 LIGHT-DAY", font=font(SANS_B, 12),
           fill=(255, 214, 130), anchor="rb")


def build():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # --- date banner ---
    d.rectangle([0, 0, W, 118], fill=(16, 20, 52))
    d.rectangle([0, 118, W, 124], fill=(255, 180, 60))
    d.text((512, 26), "WEDNESDAY  18  NOVEMBER  2026",
           font=font(SERIF_B, 46), fill=(255, 255, 255), anchor="mt")
    d.text((512, 84), "THE WORLD IN ONE DAY  •  SUMMIT, CHIPS, DRONES AND A SPACECRAFT",
           font=font(SANS_B, 19), fill=(255, 200, 90), anchor="mt")

    # --- dawn sky hero ---
    vgrad(d, (0, 124, W, 560), (255, 166, 88), (122, 62, 150))
    # sun
    d.ellipse([452, 210, 572, 330], fill=(255, 226, 130))
    d.ellipse([472, 230, 552, 310], fill=(255, 240, 180))
    # clouds
    for cx, cy, cw in [(140, 190, 150), (700, 170, 170), (830, 250, 130)]:
        d.ellipse([cx, cy, cx + cw, cy + 26], fill=(255, 205, 170))
        d.ellipse([cx + 30, cy - 12, cx + cw - 20, cy + 18], fill=(255, 220, 190))
    skyline(d, 560)
    # three flags above the skyline
    draw_flag(d, "china", 300, 372)
    draw_flag(d, "usa", 512, 356)
    draw_flag(d, "russia", 724, 372)
    # headline band across the skyline so the text reads cleanly
    d.rectangle([0, 384, W, 472], fill=(22, 18, 46))
    d.rectangle([0, 384, W, 388], fill=(255, 180, 60))
    d.rectangle([0, 468, W, 472], fill=(255, 180, 60))
    d.text((512, 396), "APEC OPENS IN SHENZHEN",
           font=font(SERIF_B, 30), fill=(255, 255, 255), anchor="mt")
    d.text((512, 434), "Trump in Manila for Quad talks  •  Xi meets Canada's Carney",
           font=font(SANS, 19), fill=(255, 235, 200), anchor="mt")

    # --- negotiation table ---
    table_scene(d, 560, 668)

    # --- four mini-scenes ---
    panels = [
        ("GULF DRONES", "Bahrain all-clear after overnight threat; Kuwait intercepts drones.",
         panel_drone),
        ("NVIDIA $115.84BN", "Quarterly revenue doubles; board rejects Huang return; Trump backs him.",
         panel_chip),
        ("GAZA CEASEFIRE", "Board of Peace warns truce may collapse; WFP: one hot meal every two days.",
         panel_dove),
        ("VOYAGER 1", "NASA probe nears one light-day from Earth — a first for a human object.",
         panel_voyager),
    ]
    px, py, pw, ph, gap = 12, 680, 244, 252, 8
    for i, (title, body, painter) in enumerate(panels):
        x = px + i * (pw + gap)
        d.rectangle([x, py, x + pw, py + ph], outline=(30, 30, 60), width=2)
        painter(d, x, py, pw, 124)
        d.rectangle([x, py + 124, x + pw, py + ph], fill=(250, 248, 240))
        d.text((x + 10, py + 132), title, font=font(SANS_B, 17), fill=(16, 20, 52))
        lines = wrap(d, body, font(SANS, 15), pw - 20)
        yy = py + 156
        for ln in lines[:4]:
            d.text((x + 10, yy), ln, font=font(SANS, 15), fill=(40, 40, 50))
            yy += 19

    # --- ticker of the rest of the day ---
    d.rectangle([0, 944, W, H], fill=(16, 20, 52))
    d.text((512, 954), "ALSO: Dhoni retires from IPL  •  Cyclone Akvan strengthens in the Bay of Bengal",
           font=font(SANS_B, 17), fill=(255, 255, 255), anchor="mt")
    d.text((512, 980), "Latvia approves a new government  •  UN: 372 civilians killed in Ukraine in October",
           font=font(SANS, 16), fill=(200, 205, 230), anchor="mt")

    img.save(OUT, optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
