#!/usr/bin/env python3
"""Draw news-image-01: a front page for Friday 13 November 2026.

Everything is drawn with PIL primitives - no photos, no model images - so the
text stays crisp and the icons stay clean at any size. Four panels, each one a
story first reported on 13 November 2026, plus a ticker of three more.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 240, 231)
CARD = (252, 249, 243)
INK = (22, 20, 18)
RED = (170, 34, 40)
GREY = (86, 80, 72)
RULE = (34, 30, 27)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(d, xy, text, f, fill):
    x, y = xy
    tw = d.textlength(text, font=f)
    d.text((x - tw / 2, y), text, font=f, fill=fill)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_grounded(d, x, y, w, h, col):
    """An airliner with a red stop bar and a small cloud behind it."""
    cx, cy = x + w / 2, y + h / 2
    d.ellipse([cx - 96, cy - 74, cx - 26, cy - 18], fill=col)
    d.ellipse([cx - 62, cy - 92, cx + 2, cy - 26], fill=col)
    d.ellipse([cx - 34, cy - 72, cx + 26, cy - 20], fill=col)
    d.rectangle([cx - 92, cy - 46, cx + 20, cy - 22], fill=col)
    # airliner, nose to the right
    body = [(cx - 78, cy + 16), (cx + 46, cy + 2), (cx + 92, cy + 12),
            (cx + 42, cy + 30), (cx - 70, cy + 32)]
    d.polygon(body, fill=col)
    d.polygon([(cx + 10, cy + 6), (cx + 52, cy - 34), (cx + 66, cy - 30),
               (cx + 40, cy + 12)], fill=col)
    d.polygon([(cx - 2, cy + 26), (cx + 18, cy + 62), (cx + 2, cy + 64),
               (cx - 24, cy + 28)], fill=col)
    for i in range(3):
        d.ellipse([cx - 56 + i * 26, cy + 12, cx - 44 + i * 26, cy + 22], fill=PAPER)
    # red ground-stop bar
    d.line([(cx - 92, cy + 56), (cx + 96, cy - 4)], fill=RED, width=13)
    d.line([(cx - 96, cy + 74), (cx + 96, cy + 74)], fill=GREY, width=5)


def icon_ship(d, x, y, w, h, col):
    """A cruise ship listing into the water, a raft of survivors, a helicopter."""
    cx, cy = x + w / 2, y + h / 2
    # listing hull
    hull = [(cx - 96, cy + 4), (cx + 54, cy - 22), (cx + 44, cy + 30),
            (cx - 84, cy + 46)]
    d.polygon(hull, fill=col)
    d.polygon([(cx - 26, cy - 6), (cx + 34, cy - 18), (cx + 30, cy + 6),
               (cx - 22, cy + 12)], fill=PAPER)
    for i in range(3):
        d.rectangle([cx - 18 + i * 18, cy - 6, cx - 6 + i * 18, cy + 4], fill=col)
    # funnel
    d.polygon([(cx - 46, cy - 12), (cx - 30, cy - 16), (cx - 26, cy + 2),
               (cx - 42, cy + 4)], fill=RED)
    # water
    for i in range(3):
        yy = cy + 56 + i * 13
        d.line([(cx - 104 + i * 10, yy), (cx - 14, yy - 8)], fill=GREY, width=5)
        d.line([(cx + 6, yy - 8), (cx + 96 - i * 10, yy)], fill=GREY, width=5)
    # survivors' raft
    d.polygon([(cx + 40, cy + 40), (cx + 96, cy + 40), (cx + 88, cy + 56),
               (cx + 46, cy + 56)], fill=RED)
    for i in range(3):
        d.ellipse([cx + 50 + i * 15, cy + 26, cx + 62 + i * 15, cy + 40], fill=col)
    # helicopter
    d.ellipse([cx - 84, cy - 86, cx - 34, cy - 58], fill=col)
    d.line([(cx - 108, cy - 90), (cx - 10, cy - 90)], fill=col, width=6)
    d.line([(cx - 60, cy - 58), (cx - 60, cy - 40)], fill=col, width=5)
    d.line([(cx - 76, cy - 40), (cx - 44, cy - 40)], fill=col, width=5)


def icon_chip(d, x, y, w, h, col):
    """A processor with a gavel striking it."""
    cx, cy = x + w / 2 - 22, y + h / 2 + 6
    s = 50
    for i in range(4):
        off = -s + 16 + i * 24
        d.line([(cx + off, cy - s - 18), (cx + off, cy - s)], fill=col, width=7)
        d.line([(cx + off, cy + s), (cx + off, cy + s + 18)], fill=col, width=7)
        d.line([(cx - s - 18, cy + off), (cx - s, cy + off)], fill=col, width=7)
        d.line([(cx + s, cy + off), (cx + s + 18, cy + off)], fill=col, width=7)
    d.rectangle([cx - s, cy - s, cx + s, cy + s], outline=col, width=8)
    d.rectangle([cx - 22, cy - 22, cx + 22, cy + 22], fill=col)
    # gavel, upper right
    gx, gy = cx + 92, cy - 62
    d.line([(gx - 44, gy + 44), (gx + 6, gy - 6)], fill=col, width=12)
    d.rectangle([gx - 10, gy - 34, gx + 34, gy - 4], fill=RED)
    d.rectangle([gx - 4, gy - 40, gx + 6, gy + 4], fill=RED)
    d.line([(gx - 30, gy + 52), (gx + 24, gy + 52)], fill=col, width=9)


def icon_talks(d, x, y, w, h, col):
    """Two delegations across a table, a split flag between them."""
    cx, cy = x + w / 2, y + h / 2 + 8
    # table
    d.rectangle([cx - 86, cy + 18, cx + 86, cy + 32], fill=col)
    d.rectangle([cx - 72, cy + 32, cx - 60, cy + 62], fill=col)
    d.rectangle([cx + 60, cy + 32, cx + 72, cy + 62], fill=col)
    # left figure
    d.ellipse([cx - 92, cy - 34, cx - 60, cy - 2], fill=col)
    d.polygon([(cx - 100, cy + 18), (cx - 52, cy + 18), (cx - 58, cy - 12),
               (cx - 94, cy - 12)], fill=col)
    # right figure
    d.ellipse([cx + 60, cy - 34, cx + 92, cy - 2], fill=col)
    d.polygon([(cx + 52, cy + 18), (cx + 100, cy + 18), (cx + 94, cy - 12),
               (cx + 58, cy - 12)], fill=col)
    # split flag above the table
    d.rectangle([cx - 44, cy - 96, cx - 2, cy - 54], fill=col)
    d.rectangle([cx - 2, cy - 96, cx + 40, cy - 54], fill=RED)
    d.line([(cx - 2, cy - 100), (cx - 2, cy - 50)], fill=PAPER, width=5)
    # document on the table
    d.rectangle([cx - 26, cy - 4, cx + 26, cy + 16], fill=PAPER, outline=col, width=3)
    for i in range(3):
        d.line([(cx - 20, cy + 2 + i * 5), (cx + 16, cy + 2 + i * 5)], fill=GREY, width=2)


# ---------------------------------------------------------------- page
def build(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    centered(d, (W / 2, 26), "THE WORLD", font(SERIF_B, 70), INK)
    centered(d, (W / 2, 106), "FRIDAY 13 NOVEMBER 2026", font(SANS_B, 27), RED)
    d.line([(44, 148), (W - 44, 148)], fill=RULE, width=4)
    d.line([(44, 156), (W - 44, 156)], fill=RULE, width=1)

    stories = [
        ("US FLIGHTS GROUNDED", "FAA halts every US departure in the Microsoft outage", icon_grounded),
        ("SHIP SINKS, ALL SAVED", "A tanker hits a New Orleans cruise boat; 32 hurt, all rescued", icon_ship),
        ("NVIDIA: SENATE SUMMONS", "Huang and Lutnick called to testify as the row widens", icon_chip),
        ("PUTIN HARDENS TERMS", "Zelensky meets US envoys as Europe joins the talks", icon_talks),
    ]

    margin, gap, top = 40, 16, 178
    cell_w = (W - 2 * margin - gap) // 2
    ticker_h = 128
    cell_h = (H - top - ticker_h - gap) // 2

    f_head = font(SANS_B, 36)
    f_deck = font(SANS, 21)
    for i, (head, deck, draw_icon) in enumerate(stories):
        col, row = i % 2, i // 2
        x = margin + col * (cell_w + gap)
        y = top + row * (cell_h + gap)
        d.rectangle([x, y, x + cell_w, y + cell_h], fill=CARD, outline=(214, 206, 194))
        icon_h = cell_h - 156
        draw_icon(d, x + 6, y + 4, cell_w - 12, icon_h, INK)
        ty = y + icon_h + 6
        for line in wrap(d, head, f_head, cell_w - 24)[:2]:
            d.text((x + 12, ty), line, font=f_head, fill=INK)
            ty += 40
        for line in wrap(d, deck, f_deck, cell_w - 24)[:2]:
            d.text((x + 12, ty + 2), line, font=f_deck, fill=GREY)
            ty += 25

    ty = H - ticker_h
    d.line([(44, ty), (W - 44, ty)], fill=RULE, width=3)
    d.text((margin, ty + 8), "ALSO ON THE DAY", font=font(SANS_B, 21), fill=RED)
    f_tick = font(SANS, 22)
    lines = [
        "Tanker burns in the Strait of Hormuz after mines strike it",
        "24 killed as a bus and a truck collide in Assam, India",
        "Pope Leo returns to the Peruvian city where he was bishop",
    ]
    yy = ty + 38
    for ln in lines:
        d.text((margin, yy), "\u2022 " + ln, font=f_tick, fill=INK)
        yy += 29

    img.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path} {os.path.getsize(out_path)} bytes {img.size}")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
