#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121 — Saturday 21 November 2026.
All scenes are simple flat shapes drawn with PIL; no downloaded images.
Layout: date banner on top, one large hero panel (Riyadh), two panels
right (COP31, cricket), three panels along the bottom (Akvan, Warsaw, Pope).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (245, 239, 224)
INK = (20, 20, 20)
NAVY = (13, 33, 55)
GOLD = (232, 179, 60)
WHITE = (255, 255, 255)
STRIP = (12, 16, 22)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def fit(text, max_w, size, bold=True):
    """Largest font size <= size that fits max_w."""
    while size > 10:
        f = font(size, bold)
        if d.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(10, bold)


def wrap(text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(x, y, w, h, color):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=color)


def title_strip(x, y, w, h, title, sub, title_size=30, sub_size=20):
    """Dark strip at the bottom of a panel with a bold title + smaller sub."""
    strip_h = h
    d.rectangle([x, y, x + w, y + h], fill=STRIP + (235,))
    tf = font(title_size)
    lines = wrap(title, tf, w - 24)
    # shrink only if the title needs more than two lines
    while len(lines) > 2 and title_size > 14:
        title_size -= 2
        tf = font(title_size)
        lines = wrap(title, tf, w - 24)
    lh = tf.size + 4
    total = len(lines) * lh + (sub_size + 6 if sub else 0)
    ty = y + max(6, (strip_h - total) // 2)
    for ln in lines:
        d.text((x + 12, ty), ln, font=tf, fill=WHITE)
        ty += lh
    if sub:
        sf = fit(sub, w - 24, sub_size, bold=False)
        d.text((x + 12, ty + 2), sub, font=sf, fill=(210, 215, 220))


def starburst(cx, cy, r, color):
    for k in range(8):
        a = math.pi * k / 4
        d.line([cx, cy, cx + r * math.cos(a), cy + r * math.sin(a)],
               fill=color, width=4)
    d.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3], fill=color)


# ---------------------------------------------------------------- banner
d.rectangle([0, 0, W, 116], fill=NAVY)
d.rectangle([0, 116, W, 122], fill=GOLD)
bf = fit("SATURDAY 21 NOVEMBER 2026", W - 48, 58)
d.text(((W - d.textlength("SATURDAY 21 NOVEMBER 2026", font=bf)) / 2, 14),
       "SATURDAY 21 NOVEMBER 2026", font=bf, fill=WHITE)
sf = font(22, bold=False)
sub = "ONE DAY IN ONE IMAGE  ·  WORLD NEWS"
d.text(((W - d.textlength(sub, font=sf)) / 2, 82), sub, font=sf, fill=GOLD)

# ---------------------------------------------------------------- hero: Riyadh
hx, hy, hw, hh = 16, 134, 632, 506
panel(hx, hy, hw, hh, (11, 30, 58))
# sky gradient bands
for i in range(14):
    y0 = hy + i * 26
    t = i / 13
    c = (int(11 + 30 * t), int(30 + 35 * t), int(58 + 45 * t))
    d.rectangle([hx, y0, hx + hw, y0 + 27], fill=c)
# stars
import random
random.seed(21)
for _ in range(60):
    sx = hx + random.randint(8, hw - 8)
    sy = hy + random.randint(8, 200)
    r = random.choice([1, 1, 2])
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 220))
# moon
d.ellipse([hx + hw - 110, hy + 30, hx + hw - 50, hy + 90], fill=(240, 230, 190))
# skyline (back row)
for bx, bw_, bh_ in [(30, 46, 120), (100, 60, 170), (200, 40, 100),
                     (470, 55, 150), (540, 44, 110), (600, 30, 90)]:
    d.rectangle([hx + bx, hy + hh - 150 - bh_, hx + bx + bw_, hy + hh - 60],
                fill=(27, 47, 74))
# Kingdom Centre tower (distinctive arch top), centre-left
tx = hx + 300
d.rectangle([tx, hy + 130, tx + 90, hy + hh - 60], fill=(35, 58, 88))
d.rectangle([tx - 6, hy + 130, tx + 96, hy + 150], fill=(35, 58, 88))
# arch opening cut in sky colour
d.pieslice([tx + 12, hy + 158, tx + 78, hy + 250], 180, 360, fill=(24, 52, 84))
d.rectangle([tx + 12, hy + 205, tx + 78, hy + 250], fill=(24, 52, 84))
# lit windows
for wx in range(tx + 8, tx + 86, 14):
    for wy in range(hy + 260, hy + hh - 70, 26):
        if random.random() < 0.55:
            d.rectangle([wx, wy, wx + 6, wy + 8], fill=(255, 209, 102))
for bx, bw_, bh_ in [(30, 46, 120), (100, 60, 170), (200, 40, 100),
                     (470, 55, 150), (540, 44, 110)]:
    for wx in range(hx + bx + 6, hx + bx + bw_ - 6, 12):
        for wy in range(hy + hh - 150 - bh_ + 10, hy + hh - 70, 22):
            if random.random() < 0.4:
                d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 209, 102))
# ground
d.rectangle([hx, hy + hh - 60, hx + hw, hy + hh], fill=(16, 22, 34))
# incoming missiles: 3 orange streaks descending from top right
for (x0, y0, x1, y1) in [(hx + 560, hy + 20, hx + 470, hy + 150),
                         (hx + 610, hy + 90, hx + 520, hy + 210),
                         (hx + 480, hy + 60, hx + 400, hy + 180)]:
    d.line([x0, y0, x1, y1], fill=(255, 120, 40), width=7)
    d.ellipse([x1 - 9, y1 - 9, x1 + 9, y1 + 9], fill=(255, 170, 60))
# interceptors: 3 white streaks rising from bottom left
for (x0, y0, x1, y1) in [(hx + 60, hy + hh - 70, hx + 300, hy + 220),
                         (hx + 130, hy + hh - 70, hx + 380, hy + 260),
                         (hx + 200, hy + hh - 70, hx + 470, hy + 300)]:
    d.line([x0, y0, x1, y1], fill=(255, 240, 180), width=5)
# interception bursts
starburst(hx + 420, hy + 190, 26, (255, 200, 80))
starburst(hx + 500, hy + 250, 22, (255, 200, 80))
starburst(hx + 330, hy + 260, 18, (255, 220, 120))
# hero title strip
title_strip(hx, hy + hh - 118, hw, 118,
            "RIYADH: 3 HOUTHI MISSILES INTERCEPTED",
            "Saudi defences stop early-morning attack",
            title_size=34, sub_size=21)

# ---------------------------------------------------------------- COP31 (right top)
cx, cy, cw, ch = 664, 134, 344, 244
panel(cx, cy, cw, ch, (14, 124, 107))
# sun rays
for k in range(12):
    a = math.pi * k / 6
    x0 = cx + 172 + 62 * math.cos(a)
    y0 = cy + 92 + 62 * math.sin(a)
    x1 = cx + 172 + 82 * math.cos(a)
    y1 = cy + 92 + 82 * math.sin(a)
    d.line([x0, y0, x1, y1], fill=(255, 220, 120), width=5)
# globe
d.ellipse([cx + 112, cy + 32, cx + 232, cy + 152], fill=(46, 160, 140))
d.ellipse([cx + 128, cy + 48, cx + 168, cy + 82], fill=(123, 201, 111))
d.ellipse([cx + 178, cy + 92, cx + 216, cy + 128], fill=(123, 201, 111))
d.ellipse([cx + 148, cy + 108, cx + 178, cy + 140], fill=(90, 180, 120))
d.arc([cx + 112, cy + 32, cx + 232, cy + 152], 0, 360, fill=(220, 245, 235), width=3)
# leaf
d.pieslice([cx + 252, cy + 84, cx + 324, cy + 156], 270, 360, fill=(140, 220, 90))
d.line([cx + 252, cy + 156, cx + 324, cy + 84], fill=(60, 140, 60), width=5)
title_strip(cx, cy + ch - 92, cw, 92,
            "COP31 TALKS RUN INTO OVERTIME",
            "Draft drops fossil-fuel text",
            title_size=26, sub_size=19)

# ---------------------------------------------------------------- cricket (right bottom)
kx, ky, kw, kh = 664, 394, 344, 246
panel(kx, ky, kw, kh, (46, 125, 50))
# stands
d.rectangle([kx, ky, kx + kw, ky + 46], fill=(30, 90, 40))
for sx in range(kx + 10, kx + kw - 10, 18):
    d.ellipse([sx, ky + 14, sx + 10, ky + 24], fill=(255, 220, 150))
# pitch
d.polygon([(kx + 120, ky + 60), (kx + 224, ky + 60),
           (kx + 260, ky + 150), (kx + 84, ky + 150)], fill=(217, 192, 138))
# stumps
for sxx in (kx + 158, kx + 168, kx + 178):
    d.line([sxx, ky + 128, sxx, ky + 150], fill=(255, 220, 120), width=4)
# batsman (simple silhouette)
d.ellipse([kx + 196, ky + 62, kx + 218, ky + 84], fill=(20, 30, 60))  # head
d.line([kx + 207, ky + 84, kx + 200, ky + 128], fill=(20, 30, 60), width=12)  # body
d.line([kx + 200, ky + 128, kx + 188, ky + 148], fill=(20, 30, 60), width=8)  # leg
d.line([kx + 200, ky + 128, kx + 214, ky + 148], fill=(20, 30, 60), width=8)  # leg
d.line([kx + 207, ky + 96, kx + 232, ky + 118], fill=(20, 30, 60), width=8)  # arm+bat
d.rectangle([kx + 228, ky + 112, kx + 244, ky + 138], fill=(200, 160, 90))  # bat
# ball with motion lines
d.ellipse([kx + 262, ky + 78, kx + 276, ky + 92], fill=(200, 40, 40))
d.line([kx + 240, ky + 74, kx + 256, ky + 80], fill=(255, 255, 255), width=3)
d.line([kx + 244, ky + 96, kx + 258, ky + 100], fill=(255, 255, 255), width=3)
# scoreboard
d.rounded_rectangle([kx + 14, ky + 66, kx + 108, ky + 108], radius=6,
                    fill=(10, 20, 14))
sbf = font(26)
d.text((kx + 22, ky + 72), "IND 255/1", font=sbf, fill=(255, 230, 120))
title_strip(kx, ky + kh - 92, kw, 92,
            "RAHUL'S CENTURY LIFTS INDIA",
            "Day 3 vs New Zealand",
            title_size=26, sub_size=19)

# ---------------------------------------------------------------- bottom row
by, bh = 656, 316

# --- Akvan cyclone
ax, aw = 16, 320
panel(ax, by, aw, bh, (19, 78, 94))
# spiral: concentric arcs
spx, spy = ax + 160, by + 105
for r in (18, 36, 54, 72):
    d.arc([spx - r, spy - r, spx + r, spy + r], 20, 320,
          fill=(234, 246, 246), width=7)
d.ellipse([spx - 12, spy - 12, spx + 12, spy + 12], fill=(255, 255, 255))
# rain
for rx in range(ax + 10, ax + aw - 10, 26):
    d.line([rx, by + 30, rx - 10, by + 52], fill=(180, 220, 235), width=3)
# sea + coast
d.rectangle([ax, by + 190, ax + aw, by + bh], fill=(27, 110, 138))
d.polygon([(ax, by + 190), (ax + 130, by + 190), (ax + 90, by + 240),
           (ax, by + 240)], fill=(222, 196, 130))
title_strip(ax, by + bh - 92, aw, 92,
            "CYCLONE AKVAN WEAKENS",
            "Deep depression over Odisha",
            title_size=26, sub_size=19)

# --- Warsaw / NATO
wx, ww = 352, 320
panel(wx, by, ww, bh, (220, 233, 245))
# NATO compass star on blue disc
d.ellipse([wx + 100, by + 14, wx + 220, by + 134], fill=(31, 78, 121))
star = [(wx + 160, by + 26), (wx + 172, by + 62), (wx + 208, by + 74),
        (wx + 172, by + 86), (wx + 160, by + 122), (wx + 148, by + 86),
        (wx + 112, by + 74), (wx + 148, by + 62)]
d.polygon(star, fill=(255, 255, 255))
d.ellipse([wx + 152, by + 66, wx + 168, by + 82], fill=(31, 78, 121))
# skyline with spire (Palace of Culture style)
d.rectangle([wx + 20, by + 150, wx + 300, by + 224], fill=(90, 110, 130))
d.rectangle([wx + 140, by + 110, wx + 180, by + 224], fill=(70, 90, 110))
d.polygon([(wx + 140, by + 110), (wx + 180, by + 110), (wx + 160, by + 66)],
          fill=(70, 90, 110))
d.line([wx + 160, by + 66, wx + 160, by + 44], fill=(70, 90, 110), width=4)
for wxx in range(wx + 30, wx + 300, 22):
    for wyy in range(by + 160, by + 220, 20):
        d.rectangle([wxx, wyy, wxx + 8, wyy + 10], fill=(255, 220, 120))
# Polish flag stripe
d.rectangle([wx + 20, by + 196, wx + 60, by + 208], fill=(255, 255, 255))
d.rectangle([wx + 20, by + 208, wx + 60, by + 220], fill=(220, 40, 60))
title_strip(wx, by + bh - 92, ww, 92,
            "NATO CHIEF HEADS TO WARSAW",
            "After missiles fell in Poland",
            title_size=26, sub_size=19)

# --- Pope / Vatican
px, pw = 688, 320
panel(px, by, pw, bh, (243, 227, 179))
# St Peter's dome
d.rectangle([px + 30, by + 150, px + 290, by + 224], fill=(184, 155, 94))
d.pieslice([px + 110, by + 60, px + 210, by + 170], 180, 360, fill=(122, 139, 153))
d.rectangle([px + 152, by + 44, px + 168, by + 70], fill=(122, 139, 153))
d.ellipse([px + 156, by + 36, px + 164, by + 46], fill=(232, 179, 60))
# columns
for colx in range(px + 44, px + 290, 26):
    d.rectangle([colx, by + 164, colx + 12, by + 224], fill=(120, 100, 70))
# crowd: rows of heads
for row, yy in enumerate((by + 196, by + 210)):
    for cxx in range(px + 16 + row * 8, px + pw - 16, 20):
        d.ellipse([cxx, yy, cxx + 12, yy + 12],
                  fill=(40, 60, 90) if row == 0 else (120, 60, 60))
# Vatican flag colours
d.rectangle([px + 20, by + 14, px + 44, by + 30], fill=(255, 215, 0))
d.rectangle([px + 44, by + 14, px + 68, by + 30], fill=(255, 255, 255))
title_strip(px, by + bh - 92, pw, 92,
            "POPE LEO MEETS 6,000 YOUTH",
            "World Youth Day in the Vatican",
            title_size=26, sub_size=19)

# ---------------------------------------------------------------- footer
ff = font(20, bold=False)
foot = "21 NOVEMBER 2026  ·  SIX STORIES, ONE DAY"
d.text(((W - d.textlength(foot, font=ff)) / 2, 986), foot, font=ff, fill=(90, 80, 60))

img.save("entry.png", optimize=True)
print("saved entry.png")
