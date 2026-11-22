#!/usr/bin/env python3
"""Draw the news-image-20261121 v2 front page with PIL.

Layout (1024 x 1024): masthead + date, one big HERO story (Riyadh) with a
drawn night-skyline scene, then three panels (Mexico, Bahrain, COP31).
All text is wrapped by measured pixel width so nothing overlaps.
Deterministic: the random module is seeded, so re-runs are byte-identical.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap by measured width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, fnt, fill, line_h):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += line_h
    return y


def burst(d, cx, cy, r, fill):
    """An 8-point starburst for a missile interception flash."""
    pts = []
    for i in range(16):
        ang = i * 3.14159265 / 8
        rr = r if i % 2 == 0 else r * 0.38
        pts.append((cx + rr * 1.0 * __import__("math").cos(ang),
                    cy + rr * __import__("math").sin(ang)))
    d.polygon(pts, fill=fill)
    d.ellipse((cx - r * 0.28, cy - r * 0.28, cx + r * 0.28, cy + r * 0.28),
              fill=(255, 240, 180))


def hero_scene(d, x0, y0, x1, y1, rnd):
    """Night sky over the Riyadh skyline: three missile trails meet bursts."""
    # sky gradient, dark navy to steel blue
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0)
        r = int(14 + 26 * t)
        g = int(26 + 42 * t)
        b = int(58 + 62 * t)
        d.line([(x0, yy), (x1, yy)], fill=(r, g, b))
    # stars
    for _ in range(46):
        sx = rnd.randint(x0 + 4, x1 - 4)
        sy = rnd.randint(y0 + 4, y0 + int((y1 - y0) * 0.45))
        d.ellipse((sx, sy, sx + 2, sy + 2), fill=(235, 235, 220))
    # moon
    d.ellipse((x1 - 66, y0 + 14, x1 - 26, y0 + 54), fill=(240, 236, 210))
    # skyline silhouettes (Kingdom Centre tower with its arch, plus blocks)
    base = y1 - 8
    ink = (12, 15, 24)
    towers = [(x0 + 18, 118, 34), (x0 + 60, 88, 30), (x0 + 96, 150, 40),
              (x0 + 142, 104, 30), (x0 + 178, 132, 36), (x0 + 220, 96, 30),
              (x0 + 256, 142, 38), (x0 + 300, 110, 30), (x0 + 336, 84, 32),
              (x0 + 374, 128, 34), (x0 + 414, 96, 30), (x0 + 450, 138, 30)]
    for tx, th, tw in towers:
        d.rectangle((tx, base - th, tx + tw, base), fill=ink)
    # Kingdom Centre arch: two pillars joined by a top bar (rectangular opening)
    ax = x0 + 96
    d.rectangle((ax, base - 168, ax + 12, base), fill=ink)
    d.rectangle((ax + 28, base - 168, ax + 40, base), fill=ink)
    d.rectangle((ax, base - 168, ax + 40, base - 156), fill=ink)
    # lit windows
    for _ in range(70):
        wx = rnd.randint(x0 + 20, x1 - 20)
        wy = rnd.randint(base - 150, base - 14)
        d.rectangle((wx, wy, wx + 3, wy + 4), fill=(250, 205, 90))
    # three missile trails arcing down to interception bursts
    trails = [((x0 + 30, y0 + 6), (x0 + 190, y0 + 78)),
              ((x1 - 40, y0 + 2), (x0 + 300, y0 + 66)),
              ((x0 + 250, y0 + 4), (x0 + 120, y0 + 96))]
    for (sx, sy), (ex, ey) in trails:
        mx, my = (sx + ex) // 2, min(sy, ey) - 14
        pts = []
        for k in range(21):
            t = k / 20
            px = (1 - t) ** 2 * sx + 2 * (1 - t) * t * mx + t * t * ex
            py = (1 - t) ** 2 * sy + 2 * (1 - t) * t * my + t * t * ey
            pts.append((px, py))
        d.line(pts, fill=(255, 214, 120), width=3)
        burst(d, ex, ey, 15, (255, 150, 40))
    d.rectangle((x0, base, x1, y1), fill=(10, 12, 20))


def desert_scene(d, x0, y0, x1, y1, rnd):
    """Sunset desert with a cactus (Mexico panel)."""
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0)
        d.line([(x0, yy), (x1, yy)],
               fill=(int(232 - 60 * t), int(120 - 20 * t), int(40 + 30 * t)))
    d.ellipse((x1 - 92, y0 + 8, x1 - 42, y0 + 58), fill=(255, 214, 130))
    gy = y1 - 16
    d.rectangle((x0, gy, x1, y1), fill=(94, 52, 22))
    # cactus silhouette
    cx = x0 + 52
    d.rounded_rectangle((cx - 7, gy - 52, cx + 7, gy), radius=6, fill=(24, 74, 40))
    d.rounded_rectangle((cx - 26, gy - 38, cx - 12, gy - 26), radius=5, fill=(24, 74, 40))
    d.rectangle((cx - 26, gy - 30, cx - 12, gy - 24), fill=(24, 74, 40))
    d.rounded_rectangle((cx + 12, gy - 44, cx + 26, gy - 32), radius=5, fill=(24, 74, 40))
    d.rectangle((cx + 12, gy - 36, cx + 26, gy - 30), fill=(24, 74, 40))
    d.polygon([(x0 + 190, gy), (x0 + 230, gy - 26), (x0 + 270, gy)],
              fill=(70, 38, 18))


def sea_scene(d, x0, y0, x1, y1, rnd):
    """Gulf sea at dusk with a base silhouette and one interception (Bahrain)."""
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0)
        d.line([(x0, yy), (x1, yy)],
               fill=(int(58 + 30 * t), int(96 + 40 * t), int(150 + 50 * t)))
    d.ellipse((x0 + 18, y0 + 8, x0 + 52, y0 + 42), fill=(255, 226, 150))
    gy = y1 - 22
    # base silhouette: low blocks, a radar dome, a mast
    d.rectangle((x0 + 150, gy - 18, x0 + 260, gy), fill=(28, 34, 44))
    d.rectangle((x0 + 120, gy - 10, x0 + 150, gy), fill=(28, 34, 44))
    d.arc((x0 + 196, gy - 40, x0 + 224, gy - 12), 180, 360, fill=(28, 34, 44))
    d.rectangle((x0 + 208, gy - 40, x0 + 212, gy - 12), fill=(28, 34, 44))
    d.line([(x0 + 262, gy - 26), (x0 + 262, gy)], fill=(28, 34, 44), width=3)
    # missile arc + burst
    pts = []
    for k in range(21):
        t = k / 20
        px = x0 + 40 + t * 150
        py = y0 + 6 + t * t * 46 - t * 10
        pts.append((px, py))
    d.line(pts, fill=(255, 214, 120), width=3)
    burst(d, x0 + 190, y0 + 42, 12, (255, 150, 40))
    # waves
    for wy in (gy + 6, gy + 13):
        for wx in range(x0, x1 - 24, 24):
            d.arc((wx, wy, wx + 24, wy + 10), 0, 180, fill=(210, 225, 240), width=2)
    d.rectangle((x0, gy, x1, gy + 2), fill=(200, 215, 230))


def globe_scene(d, x0, y0, x1, y1, rnd):
    """A globe over a conference-table horizon (COP31 panel)."""
    for yy in range(y0, y1):
        t = (yy - y0) / max(1, y1 - y0)
        d.line([(x0, yy), (x1, yy)],
               fill=(int(214 - 30 * t), int(232 - 20 * t), int(238 - 10 * t)))
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2 + 4, 34
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(42, 109, 176))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(20, 60, 110), width=2)
    # simple land blobs
    d.ellipse((cx - 24, cy - 18, cx - 4, cy + 2), fill=(74, 148, 74))
    d.ellipse((cx + 2, cy + 4, cx + 22, cy + 22), fill=(74, 148, 74))
    d.ellipse((cx + 8, cy - 22, cx + 24, cy - 6), fill=(94, 168, 94))
    d.rectangle((x0, y1 - 12, x1, y1), fill=(120, 90, 60))


def main():
    rnd = random.Random(20261121)
    img = Image.new("RGB", (W, H), (248, 244, 233))
    d = ImageDraw.Draw(img)

    # frame
    d.rectangle((8, 8, W - 9, H - 9), outline=(20, 20, 20), width=5)
    d.rectangle((18, 18, W - 19, H - 19), outline=(20, 20, 20), width=1)

    # ---- masthead ----
    name_f = font(SERIF_B, 74)
    name = "THE WORLD TODAY"
    nw = name_f.getlength(name)
    d.text(((W - nw) / 2, 30), name, font=name_f, fill=(15, 15, 15))
    d.line((44, 122, W - 44, 122), fill=(15, 15, 15), width=2)
    date_f = font(SANS_B, 40)
    date = "SATURDAY 21 NOVEMBER 2026"
    dw = date_f.getlength(date)
    d.text(((W - dw) / 2, 132), date, font=date_f, fill=(15, 15, 15))
    d.line((44, 182, W - 44, 182), fill=(15, 15, 15), width=4)
    d.line((44, 190, W - 44, 190), fill=(15, 15, 15), width=1)

    # ---- HERO: Riyadh ----
    kick_f = font(SANS_B, 30)
    d.text((44, 202), "RIYADH  ·  SAUDI ARABIA", font=kick_f, fill=(163, 22, 33))
    head_f = font(SERIF_B, 64)
    d.text((44, 240), "THREE MISSILES DOWN", font=head_f, fill=(15, 15, 15))
    d.text((44, 318), "OVER RIYADH", font=head_f, fill=(15, 15, 15))
    hero_scene(d, 44, 404, 540, 592, rnd)
    body_f = font(SANS, 32)
    hero_body = ("Saudi defences destroy three Houthi missiles aimed at "
                 "the capital — the second strike on Riyadh in days.")
    blines = wrap(hero_body, body_f, 420)
    draw_lines(d, blines, 560, 404, body_f, (25, 25, 25), 40)

    # ---- divider ----
    d.line((44, 612, W - 44, 612), fill=(15, 15, 15), width=4)
    d.line((44, 620, W - 44, 620), fill=(15, 15, 15), width=1)

    # ---- three panels ----
    panels = [
        ("MEXICO CAPTURES", ["EL CHAPO", "ISIDRO"],
         "FBI most-wanted cartel boss seized in Sinaloa.", desert_scene),
        ("IRAN STRIKES", ["US BASES", "IN BAHRAIN"],
         "Iran claims US bases hit; factory ablaze.", sea_scene),
        ("CLIMATE · ANTALYA", ["COP31", "NO DEAL"],
         "Talks run past deadline; fossil fuels left out.", globe_scene),
    ]
    pkick_f = font(SANS_B, 26)
    phead_f = font(SANS_B, 44)
    pbody_f = font(SANS, 32)
    xs = [44, 362, 680]
    for (kick, head_lines, body, scene_fn), x0 in zip(panels, xs):
        x1 = x0 + 300
        scene_fn(d, x0, 632, x1, 712, rnd)
        d.text((x0, 722), kick, font=pkick_f, fill=(163, 22, 33))
        y = 754
        for hl in head_lines:
            d.text((x0, y), hl, font=phead_f, fill=(15, 15, 15))
            y += 52
        blines = wrap(body, pbody_f, 300)
        draw_lines(d, blines, x0, y + 6, pbody_f, (25, 25, 25), 38)

    img.save(OUT, "PNG", optimize=True)
    print("saved", OUT)


if __name__ == "__main__":
    main()
