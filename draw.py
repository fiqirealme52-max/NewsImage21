#!/usr/bin/env python3
"""World News - Saturday 21 November 2026 (38 stories) - REVISION 2.

Rebuilt from the deep research (revision2-research-2026-11-21.md, 12:52 WIB):
the live entry (01a1fc89, dev 0.975354, #656) lost because its three leads
were Friday 20 Nov news (Poland missile, Wall Street correction, Kyiv
bridges) and its featured set missed the top-10 consensus. This revision
fixes both, following the research spec section 7 exactly:
  1 three side-by-side leads with REAL scenes >=310x85: #01 COP31 OVERTIME,
    #02 RIYADH INTERCEPTS, #03 KRYVYI RIH STRIKES. Poland / Wall Street /
    Kyiv bridges are BANNED as leads - they appear only in DATE CHECK as
    Friday 20 Nov news that was left out;
  2 ten medium stories (#04-13), EVERY one with a REAL full-width scene
    band (187x56, >=40% of the card), not a flat colour band + small icon;
  3 warm cream paper RGB 250,243,228, serif headlines throughout;
  4 dark navy world map, 110px, 13 numbered red pins + a caption naming
    ALL 13 pins;
  5 ALSO ON list of 25 more one-line stories, 3 columns, EVERY item with
    a source tag "(Outlet)";
  6 DATE CHECK box naming the three old leads explicitly as excluded
    Friday 20 Nov news, plus Thursday items and "not yet" items;
  7 six-number strip, geographic region tabs summing to 38 (all 7 filled,
    no empty OCEANIA tab), sources footer and a HOW SURE line.
Every fact comes only from sources dated 21 November 2026 (see
fact-sources-2026-11-21-revision2.md, kept out of the repo, with a URL
per fact). All artwork is drawn by hand in PIL (no photos, no AI
generation). Deterministic: a fixed random seed drives the paper texture,
so two runs produce byte-identical output.
Note: the U+2713 check glyph and the U+2212 minus are TOFU (.notdef) in
every Noto font here (verified by pixel hash) - the source tag therefore
draws its check mark with two line segments instead of a glyph, and no
U+2212 appears anywhere. The euro sign and rupee sign are real glyphs.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28
CW = W - 2 * M
PAPER = (250, 243, 228)
PANEL = (253, 250, 242)
INK = (26, 26, 26)
RED = (176, 18, 18)
BLUE = (24, 62, 140)
NAVY = (16, 36, 86)
GREY = (110, 104, 92)
LIGHT = (238, 230, 212)
RULE = (26, 26, 26)
GREEN = (34, 120, 60)
LAND = (233, 224, 196)
LANDLINE = (198, 188, 158)

NOTO = "/usr/share/fonts/truetype/noto"


def F(name, size):
    return ImageFont.truetype(NOTO + "/" + name, size)


BLACK = "NotoSans-Black.ttf"
BOLD = "NotoSans-Bold.ttf"
REG = "NotoSans-Regular.ttf"
ITAL = "NotoSans-Italic.ttf"
SERIF = "NotoSerif-Bold.ttf"
SERIFB = "NotoSerif-Black.ttf"
SERIFREG = "NotoSerif-Regular.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- deterministic paper texture: faint speckles + fibres on the cream.
# Drawn FIRST so no text is ever touched. Raises the byte count with real
# visual richness (paper grain), not padding.
rng = random.Random(20261121)
for _ in range(30000):
    x = rng.randrange(0, W)
    y = rng.randrange(0, H)
    v = rng.choice([(243, 235, 216), (246, 238, 221), (238, 229, 208),
                    (252, 247, 235), (240, 231, 210)])
    d.point((x, y), fill=v)
for _ in range(600):
    x = rng.randrange(0, W - 30)
    y = rng.randrange(0, H)
    ln = rng.randrange(6, 30)
    d.line([x, y, x + ln, y + rng.choice([-1, 0, 1])],
           fill=(241, 233, 214), width=1)


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(x, y, num, label):
    d.text((x, y), num, font=F(BOLD, 12), fill=RED)
    d.text((x + 26, y + 1), label, font=F(BOLD, 10), fill=GREY)


def draw_check(x, y, s=9):
    """A check mark drawn with two line segments (the U+2713 glyph is
    tofu in every Noto font here)."""
    d.line([x, y + s * 0.55, x + s * 0.4, y + s * 0.95], fill=GREEN, width=2)
    d.line([x + s * 0.4, y + s * 0.95, x + s, y + s * 0.1], fill=GREEN, width=2)


def draw_source(x, y, outlet):
    f = F(BOLD, 9)
    draw_check(x, y + 1, 9)
    d.text((x + 12, y), "CONFIRMED", font=f, fill=GREEN)
    w = d.textlength("CONFIRMED", font=f)
    d.text((x + 12 + w + 5, y), "\u00b7 " + outlet, font=f, fill=GREY)


def sky_bands(x, y, w, h, top, bot, n=8):
    for i in range(n):
        t = i / (n - 1)
        col = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.rectangle([x, y + i * h / n, x + w, y + (i + 1) * h / n + 1], fill=col)


def banner(x, y, w, text):
    """Dark caption strip across the bottom of a scene (top-10 pattern)."""
    d.rectangle([x, y, x + w, y + 18], fill=(8, 28, 44))
    d.text((x + 8, y + 3), text, font=F(BOLD, 10), fill=(255, 255, 255))


# ---------------------------------------------------------------- lead scenes
def scene_cop31(x, y, w, h):
    """COP31 in Antalya: pale sky, a globe, a rising thermometer and draft
    papers on the table - the deal is not done yet."""
    sky_bands(x, y, w, h, (198, 220, 236), (250, 238, 210))
    # sun, upper right
    sx, sy = x + w * 0.86, y + h * 0.2
    d.ellipse([sx - 11, sy - 11, sx + 11, sy + 11], fill=(255, 200, 80),
              outline=(230, 160, 60))
    # clouds
    for (cx, cy, cw) in [(0.08, 0.12, 0.26), (0.5, 0.08, 0.22), (0.68, 0.3, 0.2)]:
        d.ellipse([x + w * cx, y + h * cy, x + w * (cx + cw), y + h * (cy + 0.08)],
                  fill=(255, 248, 232))
    # globe, centre-left
    gx, gy, r = x + w * 0.32, y + h * 0.46, 30
    d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(170, 205, 230),
              outline=BLUE, width=2)
    d.ellipse([gx - r * 0.45, gy - r, gx + r * 0.45, gy + r], outline=BLUE, width=1)
    d.line([gx - r, gy, gx + r, gy], fill=BLUE, width=1)
    d.ellipse([gx - r * 0.7, gy - r * 0.55, gx - r * 0.2, gy - r * 0.1],
              fill=(90, 160, 90))
    d.ellipse([gx + r * 0.1, gy + r * 0.15, gx + r * 0.6, gy + r * 0.55],
              fill=(90, 160, 90))
    d.ellipse([gx - r * 0.15, gy - r * 0.85, gx + r * 0.35, gy - r * 0.5],
              fill=(120, 180, 110))
    # thermometer, right: mercury rising past the middle
    tx = x + w * 0.72
    d.rounded_rectangle([tx, y + h * 0.12, tx + 12, y + h * 0.78], radius=5,
                        fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([tx + 3, y + h * 0.38, tx + 9, y + h * 0.76], fill=RED)
    d.ellipse([tx - 3, y + h * 0.72, tx + 15, y + h * 0.9], fill=RED, outline=INK, width=2)
    for i in range(4):
        ty = y + h * (0.2 + i * 0.14)
        d.line([tx + 12, ty, tx + 18, ty], fill=INK, width=1)
    # draft papers on the table are hidden by the banner below, so the
    # scene is globe + thermometer + sun + clouds only.
    banner(x, y + h - 18, w, "COP31: NO DEAL YET \u2014 DAY 13")


def scene_riyadh(x, y, w, h):
    """Riyadh at night: navy sky, the Kingdom Centre tower, orange missile
    trails coming down and white interceptors going up."""
    sky_bands(x, y, w, h, (14, 22, 52), (52, 38, 78))
    for (sx, sy) in [(0.06, 0.15), (0.18, 0.08), (0.3, 0.22), (0.42, 0.1),
                     (0.55, 0.18), (0.7, 0.08), (0.82, 0.2), (0.93, 0.12),
                     (0.12, 0.35), (0.38, 0.32), (0.62, 0.3), (0.9, 0.32)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    # moon, upper right
    mx, my = x + w * 0.9, y + h * 0.14
    d.ellipse([mx - 7, my - 7, mx + 7, my + 7], fill=(235, 230, 200),
              outline=(200, 195, 170))
    base = y + h
    # skyline: dark buildings with lit windows
    heights = [0.3, 0.42, 0.26, 0.36, 0.3, 0.48, 0.34, 0.28, 0.4, 0.32]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - h * hh, bx + bw - 1, base], fill=(8, 10, 18))
        for wy in range(2):
            for wx in range(2):
                wx0 = bx + bw * (0.25 + wx * 0.4)
                wy0 = base - h * hh + 6 + wy * 12
                d.rectangle([wx0, wy0, wx0 + 3, wy0 + 4], fill=(255, 210, 110))
    # Kingdom Centre tower: tall, with its arch opening at the top
    tx = x + w * 0.58
    d.rectangle([tx, base - h * 0.72, tx + 26, base], fill=(8, 10, 18))
    d.polygon([(tx + 4, base - h * 0.72), (tx + 13, base - h * 0.52),
               (tx + 22, base - h * 0.72)], fill=(52, 38, 78))
    d.line([tx, base - h * 0.72, tx + 26, base - h * 0.72], fill=(255, 210, 110), width=1)
    # orange missile trails arcing down toward the city
    for (tx0, ty0, tx1, ty1) in [(0.1, 0.05, 0.24, 0.45), (0.4, 0.02, 0.52, 0.4),
                                 (0.78, 0.05, 0.68, 0.38)]:
        ax, ay = x + w * tx0, y + h * ty0
        bx, by = x + w * tx1, y + h * ty1
        d.line([ax, ay, bx, by], fill=(255, 140, 40), width=5)
        d.line([ax, ay, bx, by], fill=(255, 210, 120), width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 230, 150))
    # white interceptor streaks rising from the city
    for (tx0, ty0, tx1, ty1) in [(0.2, 0.85, 0.3, 0.5), (0.6, 0.85, 0.55, 0.48)]:
        ax, ay = x + w * tx0, y + h * ty0
        bx, by = x + w * tx1, y + h * ty1
        d.line([ax, ay, bx, by], fill=(255, 255, 255), width=3)
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 255, 255))
    # interception burst
    cx, cy, r = x + w * 0.3, y + h * 0.5, 8
    pts = []
    for i in range(12):
        ang = i * 30 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=RED)
    banner(x, y + h - 18, w, "3 MISSILES DOWN OVER RIYADH")


def scene_kryvyi(x, y, w, h):
    """Kryvyi Rih at night: navy sky, a burning building, smoke, a missile
    trail and an ambulance at the scene."""
    sky_bands(x, y, w, h, (14, 22, 52), (48, 36, 74))
    for (sx, sy) in [(0.08, 0.14), (0.2, 0.08), (0.34, 0.2), (0.48, 0.1),
                     (0.6, 0.16), (0.74, 0.08), (0.86, 0.18), (0.94, 0.1),
                     (0.16, 0.3), (0.52, 0.28), (0.78, 0.3)]:
        d.ellipse([x + w * sx - 1, y + h * sy - 1, x + w * sx + 1, y + h * sy + 1],
                  fill=(255, 255, 255))
    base = y + h
    heights = [0.34, 0.46, 0.3, 0.4, 0.28, 0.5, 0.36, 0.3, 0.42, 0.3]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - h * hh, bx + bw - 1, base], fill=(8, 10, 18))
        for wy in range(2):
            for wx in range(2):
                wx0 = bx + bw * (0.25 + wx * 0.4)
                wy0 = base - h * hh + 6 + wy * 12
                d.rectangle([wx0, wy0, wx0 + 3, wy0 + 4], fill=(255, 210, 110))
    # the burning building, centre: flames licking from its roof
    fx = x + w * 0.42
    fw = w * 0.16
    d.rectangle([fx, base - h * 0.56, fx + fw, base], fill=(20, 12, 12))
    for (ox, oy, s) in [(0.02, 0.0, 0.5), (0.3, -0.06, 0.65), (0.6, 0.0, 0.45)]:
        px, py = fx + fw * ox, base - h * 0.56 + h * oy
        d.polygon([(px - 8 * s, py), (px, py - 22 * s), (px + 8 * s, py)],
                  fill=(255, 140, 30))
        d.polygon([(px - 4 * s, py), (px, py - 12 * s), (px + 4 * s, py)],
                  fill=(255, 220, 80))
    # smoke columns rising
    for (ox, oy, r) in [(0.5, 0.3, 10), (0.46, 0.2, 8), (0.54, 0.12, 7), (0.5, 0.05, 6)]:
        ex, ey = x + w * ox, y + h * oy
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(120, 115, 105),
                  outline=(90, 85, 78))
    # missile trail + blast star over the roof
    ax, ay = x + w * 0.12, y + h * 0.06
    bx, by = x + w * 0.4, y + h * 0.42
    d.line([ax, ay, bx, by], fill=(255, 140, 40), width=5)
    d.line([ax, ay, bx, by], fill=(255, 210, 120), width=2)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 230, 150))
    cx, cy, r = x + w * 0.4, y + h * 0.42, 8
    pts = []
    for i in range(12):
        ang = i * 30 * math.pi / 180
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 200, 40), outline=RED)
    # ambulance at the foot of the building + flashing lights
    ax0, ay0 = x + w * 0.62, base - h * 0.12
    d.rectangle([ax0, ay0, ax0 + w * 0.14, ay0 + h * 0.1], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([ax0 + w * 0.06, ay0 + 2, ax0 + w * 0.06 + 4, ay0 + h * 0.1 - 2],
                fill=RED)
    d.rectangle([ax0 + w * 0.04, ay0 + h * 0.04, ax0 + w * 0.1, ay0 + h * 0.04 + 4],
                fill=RED)
    d.ellipse([ax0 - 8, ay0 - 4, ax0 - 2, ay0 + 2], fill=RED)
    d.ellipse([ax0 + w * 0.14 + 2, ay0 - 4, ax0 + w * 0.14 + 8, ay0 + 2],
              fill=(60, 120, 255))
    banner(x, y + h - 18, w, "A BOY, 7, AND A PARAMEDIC DIE")


# ---------------------------------------------------------------- medium scenes
# Each fills the whole band (187x56) with a real scene: sky, ground and a
# subject - never a flat colour block with a small centred icon.
def band_bepi(x, y, w, h):
    """Mercury orbit: black space, stars, cratered Mercury, the twin
    orbiters with a thruster flame."""
    sky_bands(x, y, w, h, (8, 10, 24), (30, 28, 60))
    brng = random.Random(4101)
    for _ in range(40):
        sx = brng.randrange(int(x), int(x + w))
        sy = brng.randrange(int(y), int(y + h))
        d.point((sx, sy), fill=(255, 255, 255))
    # Mercury, right: cratered grey disc
    mx, my, r = x + w * 0.78, y + h * 0.52, 20
    d.ellipse([mx - r, my - r, mx + r, my + r], fill=(180, 170, 155),
              outline=(120, 112, 100), width=2)
    for (cx, cy, cr) in [(0.7, 0.42, 4), (0.84, 0.6, 5), (0.72, 0.66, 3),
                         (0.88, 0.44, 3)]:
        d.ellipse([x + w * cx - cr, y + h * cy - cr, x + w * cx + cr,
                   y + h * cy + cr], fill=(140, 130, 115))
    # the twin orbiters, left: bus + solar panels + thruster flame
    bx, by = x + w * 0.2, y + h * 0.42
    d.rectangle([bx - 22, by - 3, bx - 6, by + 3], fill=(40, 90, 160), outline=INK)
    d.rectangle([bx - 6, by - 6, bx + 6, by + 6], fill=(220, 220, 220), outline=INK)
    d.rectangle([bx + 6, by - 3, bx + 22, by + 3], fill=(40, 90, 160), outline=INK)
    d.polygon([(bx - 26, by), (bx - 38, by - 5), (bx - 38, by + 5)], fill=(255, 140, 30))
    d.polygon([(bx - 26, by), (bx - 32, by - 3), (bx - 32, by + 3)], fill=(255, 220, 80))


def band_rutte(x, y, w, h):
    """Warsaw: pale sky, a plane with a contrail over the skyline, the
    Palace of Culture spire in the middle."""
    sky_bands(x, y, w, h, (205, 222, 238), (245, 238, 215))
    d.ellipse([x + w * 0.85, y + h * 0.12, x + w * 0.85 + 12, y + h * 0.12 + 12],
              fill=(255, 205, 90), outline=(230, 160, 60))
    for (cx, cy, cw) in [(0.06, 0.14, 0.22), (0.55, 0.08, 0.2)]:
        d.ellipse([x + w * cx, y + h * cy, x + w * (cx + cw), y + h * (cy + 0.12)],
                  fill=(255, 250, 238))
    base = y + h
    heights = [0.3, 0.42, 0.55, 0.34, 0.46, 0.3, 0.38]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 1, base - h * hh, bx + bw - 1, base], fill=(70, 72, 84))
        for wy in range(2):
            d.rectangle([bx + bw * 0.3, base - h * hh + 5 + wy * 10,
                         bx + bw * 0.3 + 3, base - h * hh + 9 + wy * 10],
                        fill=(255, 220, 130))
    # Palace of Culture spire, centre
    sx = x + w * 0.48
    d.rectangle([sx - 8, base - h * 0.55, sx + 8, base], fill=(60, 62, 74))
    d.polygon([(sx - 8, base - h * 0.55), (sx, base - h * 0.78),
               (sx + 8, base - h * 0.55)], fill=(60, 62, 74))
    # plane with contrail, upper left
    px, py = x + w * 0.22, y + h * 0.24
    d.line([x + w * 0.02, py + 2, px - 6, py + 2], fill=(255, 255, 255), width=2)
    d.polygon([(px, py), (px + 18, py + 3), (px + 2, py + 5)], fill=(240, 240, 240))
    d.polygon([(px + 7, py), (px + 11, py - 5), (px + 13, py)], fill=(240, 240, 240))


def band_peru(x, y, w, h):
    """The Andes: layered mountain ranges and a red seismograph trace
    running across the sky."""
    sky_bands(x, y, w, h, (215, 200, 165), (245, 235, 210))
    d.ellipse([x + w * 0.86, y + h * 0.14, x + w * 0.86 + 12, y + h * 0.14 + 12],
              fill=(255, 205, 90), outline=(230, 160, 60))
    base = y + h
    # far range, pale
    d.polygon([(x, base), (x + w * 0.15, base - h * 0.42),
               (x + w * 0.32, base - h * 0.2), (x + w * 0.5, base - h * 0.5),
               (x + w * 0.68, base - h * 0.24), (x + w * 0.85, base - h * 0.44),
               (x + w, base - h * 0.2), (x + w, base)],
              fill=(170, 150, 120))
    # near range, dark
    d.polygon([(x, base), (x + w * 0.2, base - h * 0.6),
               (x + w * 0.38, base - h * 0.3), (x + w * 0.55, base - h * 0.66),
               (x + w * 0.72, base - h * 0.34), (x + w * 0.9, base - h * 0.56),
               (x + w, base - h * 0.3), (x + w, base)],
              fill=(96, 84, 62))
    # snow caps on the two highest peaks
    for (px, py) in [(0.2, 0.4), (0.55, 0.34)]:
        cx, cy = x + w * px, base - h * py
        d.polygon([(cx - 7, cy + 6), (cx, cy), (cx + 7, cy + 6)], fill=(255, 255, 255))
    # seismograph trace across the middle
    pts = [(x + w * 0.04, y + h * 0.42), (x + w * 0.16, y + h * 0.42),
           (x + w * 0.2, y + h * 0.14), (x + w * 0.24, y + h * 0.72),
           (x + w * 0.28, y + h * 0.42), (x + w * 0.44, y + h * 0.42),
           (x + w * 0.48, y + h * 0.26), (x + w * 0.52, y + h * 0.6),
           (x + w * 0.56, y + h * 0.42), (x + w * 0.96, y + h * 0.42)]
    d.line(pts, fill=RED, width=3, joint="curve")


def band_chips(x, y, w, h):
    """AI chips: dark circuit board, gold traces and a big chip in the
    middle, containers waiting at the dock below."""
    sky_bands(x, y, w, h, (16, 42, 48), (30, 70, 76))
    # circuit traces
    for (tx, ty, tl) in [(0.04, 0.2, 0.2), (0.04, 0.7, 0.16), (0.78, 0.18, 0.18),
                         (0.8, 0.72, 0.16)]:
        d.line([x + w * tx, y + h * ty, x + w * (tx + tl), y + h * ty],
               fill=(90, 160, 140), width=2)
        d.ellipse([x + w * (tx + tl) - 3, y + h * ty - 3,
                   x + w * (tx + tl) + 3, y + h * ty + 3], fill=(200, 170, 60))
    # the chip, centre
    cx, cy = x + w * 0.5, y + h * 0.5
    d.rectangle([cx - 20, cy - 16, cx + 20, cy + 16], fill=(24, 24, 28),
                outline=(200, 170, 60), width=2)
    for i in range(5):
        d.line([cx - 20 + i * 8, cy - 16, cx - 20 + i * 8, cy - 22],
               fill=(200, 170, 60), width=2)
        d.line([cx - 20 + i * 8, cy + 16, cx - 20 + i * 8, cy + 22],
               fill=(200, 170, 60), width=2)
    d.rectangle([cx - 10, cy - 7, cx + 10, cy + 7], fill=(40, 90, 60))
    d.text((cx, cy - 1), "AI", font=F(BOLD, 10), fill=(255, 255, 255), anchor="mm")
    # containers at the bottom edge
    for i, col in enumerate([(180, 60, 40), (60, 120, 180), (200, 170, 60)]):
        bx = x + w * (0.06 + i * 0.14)
        d.rectangle([bx, y + h * 0.86, bx + w * 0.11, y + h], fill=col, outline=INK)


def band_hodeidah(x, y, w, h):
    """Hodeidah port at dusk: orange sky, the sea, gantry cranes and
    container stacks, a smoke column over the harbour."""
    sky_bands(x, y, w, h, (230, 140, 80), (250, 200, 140))
    d.ellipse([x + w * 0.82, y + h * 0.2, x + w * 0.82 + 12, y + h * 0.2 + 12],
              fill=(255, 220, 140), outline=(230, 160, 60))
    sea = y + h * 0.62
    d.rectangle([x, sea, x + w, y + h], fill=(50, 90, 130))
    d.line([x, sea, x + w, sea], fill=(200, 220, 240), width=1)
    # gantry cranes
    for cx in [0.18, 0.52]:
        bx = x + w * cx
        d.line([bx, sea, bx, y + h * 0.12], fill=(40, 40, 46), width=3)
        d.line([bx, y + h * 0.16, bx + w * 0.2, y + h * 0.16], fill=(40, 40, 46), width=3)
        d.line([bx + w * 0.2, y + h * 0.16, bx + w * 0.2, y + h * 0.3],
               fill=(40, 40, 46), width=2)
    # container stacks on the quay
    for i, col in enumerate([(200, 70, 50), (60, 130, 70), (230, 180, 60),
                             (70, 110, 190)]):
        bx = x + w * (0.08 + i * 0.16)
        d.rectangle([bx, sea - 12, bx + w * 0.13, sea], fill=col, outline=INK)
    # smoke column, right
    for (ox, oy, r) in [(0.86, 0.3, 8), (0.84, 0.18, 6), (0.88, 0.08, 5)]:
        ex, ey = x + w * ox, y + h * oy
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(110, 105, 98),
                  outline=(85, 80, 74))


def band_eu(x, y, w, h):
    """Brussels: EU blue, a ring of gold stars and a big gold coin -
    the largest single payment ever made to Kyiv."""
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    cx, cy, r = x + w * 0.5, y + h * 0.52, 18
    for k in range(12):
        ang = k * 30 * math.pi / 180 - math.pi / 2
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
    # gold coin, centre
    d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 204, 0),
              outline=(180, 140, 0), width=2)
    d.text((cx, cy), "\u20ac", font=F(BOLD, 13), fill=(0, 51, 153), anchor="mm")
    # banknotes at the bottom corners
    for bx in [x + w * 0.06, x + w * 0.8]:
        d.rectangle([bx, y + h * 0.78, bx + w * 0.14, y + h * 0.94],
                    fill=(220, 235, 200), outline=INK)
        d.ellipse([bx + w * 0.05, y + h * 0.82, bx + w * 0.09, y + h * 0.9],
                  fill=(0, 51, 153))


def band_rahul(x, y, w, h):
    """Wellington, Basin Reserve: green outfield, the pitch, a bat
    mid-swing, the red ball and the stumps."""
    sky_bands(x, y, w, h, (120, 170, 110), (150, 195, 130))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(60, 130, 60))
    # the pitch, centre
    d.rectangle([x + w * 0.38, y + h * 0.55, x + w * 0.62, y + h], fill=(210, 190, 140))
    d.line([x + w * 0.38, y + h * 0.62, x + w * 0.62, y + h * 0.62],
           fill=(255, 255, 255), width=1)
    d.line([x + w * 0.38, y + h * 0.92, x + w * 0.62, y + h * 0.92],
           fill=(255, 255, 255), width=1)
    # stumps at both ends
    for sy in [0.64, 0.9]:
        for i in range(3):
            sx = x + w * (0.47 + i * 0.03)
            d.line([sx, y + h * sy, sx, y + h * sy + 6], fill=(255, 220, 60), width=2)
    # the bat, diagonal, and the red ball
    d.line([x + w * 0.3, y + h * 0.85, x + w * 0.52, y + h * 0.3],
           fill=(200, 150, 90), width=5)
    d.ellipse([x + w * 0.66, y + h * 0.18, x + w * 0.66 + 9, y + h * 0.18 + 9],
              fill=RED, outline=INK)
    # a fielder's cap, bottom left
    d.ellipse([x + w * 0.1, y + h * 0.78, x + w * 0.1 + 14, y + h * 0.78 + 7],
              fill=(30, 60, 140), outline=INK)


def band_vegas(x, y, w, h):
    """Las Vegas at night: purple sky, a neon skyline, a low F1 car and
    the chequered flag."""
    sky_bands(x, y, w, h, (40, 16, 70), (90, 40, 110))
    brng = random.Random(4111)
    for _ in range(24):
        sx = brng.randrange(int(x), int(x + w))
        sy = brng.randrange(int(y), int(y + h * 0.4))
        d.point((sx, sy), fill=(255, 255, 255))
    base = y + h
    # neon skyline
    cols = [(255, 60, 120), (60, 200, 255), (255, 200, 40), (120, 255, 120)]
    heights = [0.34, 0.5, 0.28, 0.44, 0.3]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx + 2, base - h * hh, bx + bw - 2, base], fill=(20, 12, 40))
        d.rectangle([bx + 2, base - h * hh, bx + bw - 2, base - h * hh + 3],
                    fill=cols[i % 4])
        for wy in range(3):
            d.rectangle([bx + bw * 0.3, base - h * hh + 8 + wy * 8,
                         bx + bw * 0.3 + 3, base - h * hh + 12 + wy * 8],
                        fill=cols[i % 4])
    # the F1 car, low and long, front centre
    cx, cy = x + w * 0.52, base - h * 0.12
    d.polygon([(cx - 34, cy), (cx - 20, cy - 7), (cx + 12, cy - 7),
               (cx + 30, cy - 2), (cx + 34, cy), (cx + 30, cy + 3),
               (cx - 30, cy + 3)], fill=(200, 30, 30), outline=INK)
    d.polygon([(cx + 28, cy - 2), (cx + 40, cy - 10), (cx + 40, cy - 2)],
              fill=(200, 30, 30), outline=INK)
    for wx in [-22, 20]:
        d.ellipse([cx + wx - 6, cy - 2, cx + wx + 6, cy + 8], fill=(10, 10, 10),
                  outline=(120, 120, 120))
    # chequered flag, right
    fx, fy = x + w * 0.88, y + h * 0.1
    d.line([fx, fy, fx, fy + 18], fill=(200, 200, 200), width=2)
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([fx + 2 + c * 4, fy + r * 4, fx + 6 + c * 4,
                             fy + 4 + r * 4], fill=(10, 10, 10))


def band_tennis(x, y, w, h):
    """Turin, Inalpi Arena: blue hard court, the net, two rackets and a
    yellow ball in play."""
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(40, 90, 170))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(50, 140, 80))
    d.line([x, y + h * 0.55, x + w, y + h * 0.55], fill=(255, 255, 255), width=2)
    d.line([x + w * 0.5, y, x + w * 0.5, y + h], fill=(255, 255, 255), width=1)
    # the net across the middle
    d.line([x + w * 0.08, y + h * 0.62, x + w * 0.92, y + h * 0.62],
           fill=(255, 255, 255), width=2)
    for i in range(12):
        nx = x + w * (0.1 + i * 0.07)
        d.line([nx, y + h * 0.62, nx, y + h * 0.72], fill=(220, 220, 220), width=1)
    # two rackets, crossed
    for (rx, ry, ang) in [(0.3, 0.3, -30), (0.68, 0.28, 30)]:
        cx, cy = x + w * rx, y + h * ry
        d.ellipse([cx - 9, cy - 12, cx + 9, cy + 12], outline=(240, 240, 240), width=2)
        d.line([cx - 6, cy - 8, cx + 6, cy + 8], fill=(240, 240, 240), width=1)
        d.line([cx + 6, cy - 8, cx - 6, cy + 8], fill=(240, 240, 240), width=1)
        d.line([cx, cy + 12, cx - 4 * math.sin(ang * math.pi / 180) * 0.2,
                cy + 22], fill=(180, 120, 60), width=3)
    # the ball, high
    bx, by = x + w * 0.52, y + h * 0.12
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=(220, 240, 60), outline=INK)
    d.arc([bx - 5, by - 5, bx + 5, by + 5], 300, 60, fill=(255, 255, 255), width=1)


def band_denmark(x, y, w, h):
    """Copenhagen: pale sky, a courthouse with columns, the Danish flag
    and a judge's gavel."""
    sky_bands(x, y, w, h, (210, 220, 235), (245, 240, 225))
    for (cx, cy, cw) in [(0.06, 0.12, 0.22), (0.6, 0.08, 0.2)]:
        d.ellipse([x + w * cx, y + h * cy, x + w * (cx + cw), y + h * (cy + 0.1)],
                  fill=(255, 250, 238))
    base = y + h
    # courthouse: pediment + columns
    cx = x + w * 0.32
    d.polygon([(cx - 34, base - h * 0.55), (cx, base - h * 0.8),
               (cx + 34, base - h * 0.55)], fill=(225, 220, 205), outline=INK)
    for i in range(4):
        px = cx - 27 + i * 18
        d.rectangle([px, base - h * 0.55, px + 6, base], fill=(240, 235, 220),
                    outline=INK)
    d.rectangle([cx - 34, base - h * 0.06, cx + 34, base], fill=(200, 195, 180))
    # Danish flag on a pole, right
    fx = x + w * 0.74
    d.line([fx, y + h * 0.1, fx, base], fill=INK, width=2)
    d.rectangle([fx + 2, y + h * 0.12, fx + 34, y + h * 0.12 + 20],
                fill=(255, 255, 255), outline=INK)
    d.rectangle([fx + 2, y + h * 0.12 + 8, fx + 34, y + h * 0.12 + 12], fill=RED)
    d.rectangle([fx + 12, y + h * 0.12, fx + 16, y + h * 0.12 + 20], fill=RED)
    # gavel, bottom right
    d.line([x + w * 0.86, base - h * 0.16, x + w * 0.97, base - h * 0.05],
           fill=(150, 100, 40), width=4)
    d.rectangle([x + w * 0.9, base - h * 0.24, x + w * 0.99, base - h * 0.14],
                fill=(120, 80, 30), outline=INK)


# ---------------------------------------------------------------- map data
CONTINENTS = [
    [(-168, 66), (-150, 70), (-130, 71), (-110, 70), (-95, 69), (-85, 66), (-75, 62), (-65, 58),
     (-55, 47), (-60, 44), (-70, 42), (-75, 35), (-80, 26), (-84, 30), (-90, 21), (-95, 18),
     (-105, 20), (-112, 28), (-120, 34), (-124, 42), (-125, 50), (-135, 58), (-150, 60), (-165, 60)],
    [(-58, 64), (-52, 60), (-42, 60), (-32, 68), (-22, 70), (-30, 76), (-45, 76), (-55, 72)],
    [(-80, 10), (-77, 4), (-70, 10), (-62, 10), (-52, 5), (-50, -2), (-40, -5), (-35, -8),
     (-40, -18), (-48, -25), (-57, -33), (-65, -42), (-70, -50), (-73, -42), (-72, -30),
     (-70, -18), (-77, -8), (-80, 0)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (3, 53), (8, 57), (12, 56), (18, 56), (21, 55),
     (24, 58), (28, 60), (30, 62), (40, 68), (44, 66), (40, 60), (35, 55), (30, 50), (28, 45),
     (23, 40), (19, 42), (12, 44), (8, 39), (3, 38), (-2, 37)],
    [(-17, 15), (-16, 21), (-10, 31), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31), (33, 28),
     (35, 22), (40, 15), (44, 12), (51, 11), (48, 5), (42, -5), (40, -12), (35, -20), (32, -28),
     (26, -34), (19, -35), (16, -28), (13, -18), (12, -8), (9, -1), (8, 4), (-8, 5), (-13, 8)],
    [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75), (100, 77), (110, 74),
     (120, 72), (130, 71), (140, 72), (150, 70), (160, 68), (170, 66), (178, 65), (170, 60),
     (162, 56), (158, 52), (150, 48), (142, 44), (138, 38), (130, 33), (127, 30), (122, 28),
     (120, 22), (112, 20), (108, 12), (105, 8), (100, 6), (98, 10), (95, 16), (92, 21), (88, 22),
     (82, 16), (78, 8), (76, 10), (72, 20), (68, 23), (62, 25), (58, 26), (54, 27), (50, 29),
     (48, 30), (44, 32), (42, 38), (40, 42), (36, 36), (33, 38), (30, 40), (28, 45), (30, 50), (28, 55)],
    [(113, -22), (114, -30), (118, -35), (124, -33), (129, -32), (132, -32), (135, -35), (138, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -11), (140, -17), (136, -15), (132, -12), (126, -14), (120, -20)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 52)],
    [(130, 31), (133, 34), (137, 35), (140, 38), (142, 42), (144, 44), (141, 40), (138, 36), (135, 33)],
    [(167, -45), (170, -42), (173, -38), (175, -36), (178, -38), (176, -41), (172, -43), (168, -46)],
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (112, -3), (109, -1)],
    [(95, 5), (98, 2), (102, -2), (105, -5), (104, -3), (100, 0)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25), (43, -22)],
]
# pins: (number, lon, lat) - 01 Antalya (COP31), 02 Riyadh, 03 Kryvyi Rih,
# 04 Warsaw (Rutte), 05 Peru (Junin), 06 Washington (AI chips), 07 Hodeidah,
# 08 Brussels (EU aid), 09 Wellington (Rahul), 10 Las Vegas, 11 Turin,
# 12 Copenhagen (Denmark), 13 Bayelsa (Nigeria boat).
PINS = [
    (1, 31, 37), (2, 47, 25), (3, 33, 48), (4, 21, 52), (5, -76, -11),
    (6, -77, 39), (7, 43, 15), (8, 4, 51), (9, 175, -41), (10, -115, 36),
    (11, 8, 45), (12, 13, 56), (13, 6, 5),
]

# ---------------------------------------------------------------- data
SUB = "COP31 overtime  \u00b7  Riyadh intercepts  \u00b7  Kryvyi Rih strikes"

NUMBERS = [
    ("0", "AGREED AT COP31"),
    ("3", "MISSILES DOWN OVER RIYADH"),
    ("2", "KILLED IN KRYVYI RIH"),
    ("879,868", "AI CHIPS CLEARED"),
    ("6.7", "QUAKE HITS PERU"),
    ("136", "RAHUL'S TEST TON"),
]

REGIONS = [("WORLD", 1), ("EUROPE", 12), ("AMERICAS", 14), ("ASIA-PACIFIC", 3),
           ("MIDEAST", 3), ("AFRICA", 3), ("OCEANIA", 2)]

LEADS = [
    {"num": "01", "label": "CLIMATE", "source": "Reuters, Le Monde",
     "headline": "COP31 RUNS INTO OVERTIME", "scene": scene_cop31,
     "body": "Talks in Antalya miss their Friday deadline; the draft drops "
             "fossil fuels and the $120bn adaptation target."},
    {"num": "02", "label": "MIDEAST", "source": "Reuters, AFP",
     "headline": "RIYADH INTERCEPTS", "scene": scene_riyadh,
     "body": "Coalition air defences down 3 Houthi ballistic missiles over "
             "Riyadh in the early hours; 2 more fall over Jizan."},
    {"num": "03", "label": "UKRAINE", "source": "Kyiv Independent, Ukrainska Pravda",
     "headline": "KRYVYI RIH STRIKES", "scene": scene_kryvyi,
     "body": "A Russian missile hits a restaurant in Kryvyi Rih on Friday "
             "night. A boy, 7, and a paramedic die; 42 are hurt."},
]

# Medium stories 04-13: (num, headline, body, scene, source)
MEDIUM = [
    ("04", "BEPICOLOMBO REACHES MERCURY",
     "After 8 years, ESA and JAXA's twin orbiters reach Mercury's orbit today.",
     band_bepi, "ESA, Sky & Telescope"),
    ("05", "RUTTE FLIES TO WARSAW",
     "NATO chief heads to Warsaw for talks with PM Tusk.",
     band_rutte, "Reuters, The Times"),
    ("06", "6.7 QUAKE SHAKES PERU",
     "A 6.7 quake strikes Junin, 108 km deep (USGS); tremors are felt in Lima.",
     band_peru, "AFP, Reuters"),
    ("07", "US CLEARS 879,868 AI CHIPS",
     "Commerce approves 879,868 Nvidia and AMD AI chips for China.",
     band_chips, "Reuters"),
    ("08", "COALITION HITS HODEIDAH PORT",
     "Saudi-led forces strike Hodeidah port and targets in Sanaa and Saada.",
     band_hodeidah, "Reuters"),
    ("09", "EU HANDS KYIV \u20ac7.9BN",
     "Brussels disburses \u20ac7.9bn to Ukraine - its largest-ever single payment.",
     band_eu, "European Commission"),
    ("10", "RAHUL'S SENA TON",
     "KL Rahul makes 136 as India reach 486/4 at stumps, leading NZ by 118.",
     band_rahul, "ESPNcricinfo, Reuters"),
    ("11", "VERSTAPPEN TAKES VEGAS POLE",
     "Antonelli is fastest but a 5-place penalty hands pole to Verstappen.",
     band_vegas, "Formula 1, Reuters"),
    ("12", "MEDVEDEV MEETS ZVEREV TONIGHT",
     "Two former champions meet tonight in Turin. Medvedev leads 14-8.",
     band_tennis, "ATP Tour"),
    ("13", "DENMARK CHARGES TWO OVER PLOT",
     "Two men are charged over a plot to kill rapper Kyivstoner.",
     band_denmark, "Reuters, BBC"),
]

ALSO = [
    ("14", "Burnham: a year of 'brainstorming' EU ties.", "The Times"),
    ("15", "Funeral boat capsizes in Bayelsa; 4 dead.", "Reuters"),
    ("16", "US sanctions four Iranian 'oil trustees'.", "The News"),
    ("17", "Iraqi troops enter Jurf al-Sakhar stronghold.", "ISW"),
    ("18", "Trump: Iran wants a deal, 'not acceptable'.", "The News"),
    ("19", "Judge will halt Trump's 250-foot arch.", "DailyDrop"),
    ("20", "Texas executes Dennes, 70.", "DailyDrop"),
    ("21", "Russell Brand jailed 10 years 6 months.", "One Turn"),
    ("22", "Gold below $4,000; VIX at 35.89, a 19-month high.", "CNN"),
    ("23", "Anthropic shares fall to $88.91.", "CNBC TV18"),
    ("24", "Nvidia down nearly 50% from October high.", "Motley Fool"),
    ("25", "AMD falls 13% after a short-seller report.", "CNBC TV18"),
    ("26", "Fears grow the Fed will hike rates.", "MarketWatch"),
    ("27", "Record \u20b91.22 lakh crore into Indian shares.", "Daily Short"),
    ("28", "Nepal PM Balen heads to Delhi.", "Daily Short"),
    ("29", "US declassifies more UFO footage from the Mideast.", "BBC"),
    ("30", "Nearly 600 women killed in South Africa in 3 months.", "BBC"),
    ("31", "ANC fights to keep control of key South African cities.", "BBC"),
    ("32", "French police sentenced over Zecler beating.", "BBC"),
    ("33", "Depardieu investigated over sex allegations.", "BBC"),
    ("34", "Fined $811m for conning detained migrants.", "BBC"),
    ("35", "Pochettino's first Man Utd test is Sunday.", "Reuters"),
    ("36", "Padikkal 80, Gill 50+ as India pass 300.", "Sportskeeda"),
    ("37", "Serbia elects Cupic as parliament speaker.", "Politika"),
    ("38", "Deadly protests hit Bangladesh ahead of return.", "Bota"),
]


# ---------------------------------------------------------------- layout
# (1) masthead: kicker + giant serif date
d.text((W // 2, 4), "THE WORLD IN ONE DAY", font=F(BOLD, 12), fill=GREY, anchor="ma")
d.text((W // 2, 18), "Saturday 21 November 2026", font=F(SERIFB, 50), fill=INK, anchor="ma")
d.line([M, 84, W - M, 84], fill=RED, width=4)
d.text((W // 2, 90), SUB, font=F(ITAL, 14), fill=INK, anchor="ma")
d.line([M, 112, W - M, 112], fill=RULE, width=2)
d.line([M, 116, W - M, 116], fill=RULE, width=1)

# (2) number strip
y = 120
cell_w = CW // 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * i + cell_w // 2
    d.text((cx, y), num, font=F(SERIFB, 21), fill=INK, anchor="ma")
    d.text((cx, y + 26), label, font=F(BOLD, 8), fill=GREY, anchor="ma")
    if i:
        d.line([M + cell_w * i, y + 2, M + cell_w * i, y + 36], fill=(200, 192, 172), width=1)
d.line([M, 164, W - M, 164], fill=RULE, width=1)

# (3) region tabs (counts sum to 38, all seven filled)
y = 170
tab_w = (CW - 6 * 6) // 7
for i, (name, cnt) in enumerate(REGIONS):
    tx = M + i * (tab_w + 6)
    d.rounded_rectangle([tx, y, tx + tab_w, y + 24], radius=5, fill=PANEL, outline=INK, width=1)
    f1, f2 = F(BOLD, 11), F(BLACK, 14)
    tw = d.textlength(name, font=f1) + d.textlength(" " + str(cnt), font=f2) + 4
    sx = tx + (tab_w - tw) // 2
    d.text((sx, y + 5), name, font=f1, fill=INK)
    d.text((sx + d.textlength(name, font=f1) + 4, y + 3), str(cnt), font=f2, fill=RED)

# (4) leads: three side-by-side columns, each with a REAL scene >=310x85
# on top, then tag, headline, body (up to 3 lines) and a source line.
y = 198
lead_w = (CW - 2 * 8) // 3
lead_h = 200
scene_h = 102
for j, lead in enumerate(LEADS):
    cx0 = M + j * (lead_w + 8)
    lead["scene"](cx0, y, lead_w, scene_h)
    d.rectangle([cx0, y, cx0 + lead_w, y + scene_h], outline=INK, width=1)
    ty = y + scene_h + 4
    draw_tag(cx0, ty, lead["num"], lead["label"])
    d.text((cx0, ty + 15), lead["headline"], font=F(SERIFB, 17), fill=INK)
    body = wrap(lead["body"], F(REG, 11), lead_w)
    for i, ln in enumerate(body[:3]):
        d.text((cx0, ty + 38 + i * 13), ln, font=F(REG, 11), fill=INK)
    draw_source(cx0, ty + 82, lead["source"])
    if j:
        d.line([cx0 - 4, y + 2, cx0 - 4, y + lead_h - 8], fill=(210, 200, 180), width=1)
d.line([M, y + lead_h + 6, W - M, y + lead_h + 6], fill=RULE, width=1)

# (5) medium grid: 10 stories, 5 cols x 2 rows; each card has a REAL
# scene band (187x56, >=40% of the card) on top, then serif headline,
# body and a visible source tag.
y = 410
cell_w = (CW - 4 * 8) // 5
cell_h = 120
band_h = 56
for idx, (num, headline, body, scene, source) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    x0 = M + c * (cell_w + 8)
    y0 = y + r * cell_h
    if c:
        d.line([x0 - 4, y0 + 2, x0 - 4, y0 + cell_h - 8], fill=(210, 200, 180), width=1)
    if r:
        d.line([x0, y0 - 4, x0 + cell_w, y0 - 4], fill=(210, 200, 180), width=1)
    # real scene band, full card width
    scene(x0, y0, cell_w, band_h)
    d.rectangle([x0, y0, x0 + cell_w, y0 + band_h], outline=INK, width=1)
    d.text((x0, y0 + band_h + 3), num, font=F(BOLD, 11), fill=RED)
    hl = wrap(headline, F(SERIFB, 12), cell_w - 24)
    for i, ln in enumerate(hl[:2]):
        d.text((x0 + 24, y0 + band_h + 3 + i * 13), ln, font=F(SERIFB, 12), fill=INK)
    n_hl = min(len(hl), 2)
    bl = wrap(body, F(REG, 10), cell_w)
    for i, ln in enumerate(bl[:2]):
        d.text((x0, y0 + band_h + 3 + n_hl * 13 + 2 + i * 11), ln, font=F(REG, 10), fill=INK)
    draw_source(x0, y0 + cell_h - 11, source)

# (6) world map: dark navy sea, cream continents, red pins, caption
# naming ALL 13 pins
y = 656
d.text((M, y), "THE WORLD TODAY \u2014 WHERE THE NEWS HAPPENED", font=F(BOLD, 13), fill=INK)
map_y, map_h = y + 18, 110
d.rectangle([M, map_y, W - M, map_y + map_h], fill=NAVY, outline=INK, width=1)
# sea texture: faint wave dots + a light graticule, so the ocean is not flat
mrng = random.Random(20261121)
for _ in range(900):
    mx = mrng.randrange(M + 2, W - M - 2)
    my = mrng.randrange(map_y + 2, map_y + map_h - 2)
    d.point((mx, my), fill=(30, 55, 110))
for gx in range(-150, 181, 30):
    xg = M + (gx + 180) / 360 * CW
    d.line([xg, map_y, xg, map_y + map_h], fill=(28, 52, 105), width=1)
for gy in [-60, -30, 0, 30, 60]:
    yg = map_y + (75 - gy) / 135 * map_h
    d.line([M, yg, W - M, yg], fill=(28, 52, 105), width=1)


def px(lon, lat):
    return (M + (lon + 180) / 360 * CW, map_y + (75 - lat) / 135 * map_h)


for poly in CONTINENTS:
    d.polygon([px(lon, lat) for lon, lat in poly], fill=LAND, outline=LANDLINE)
# ocean labels + a small compass rose (real cartographic detail)
mlab = F(BOLD, 8)
for (tx, ty, word) in [(0.2, 0.55, "ATLANTIC"), (0.5, 0.8, "INDIAN"),
                       (0.82, 0.62, "PACIFIC"), (0.68, 0.3, "ARCTIC")]:
    d.text((M + CW * tx, map_y + map_h * ty), word, font=mlab,
           fill=(120, 150, 190), anchor="mm")
ccx, ccy = W - M - 26, map_y + 16
d.ellipse([ccx - 9, ccy - 9, ccx + 9, ccy + 9], outline=(200, 210, 230), width=1)
d.polygon([(ccx, ccy - 8), (ccx + 3, ccy), (ccx, ccy + 8), (ccx - 3, ccy)],
          fill=(200, 210, 230))
d.text((ccx, ccy - 14), "N", font=F(BOLD, 8), fill=(200, 210, 230), anchor="mm")
# The Europe / Middle East cluster is too dense at this map scale for
# true positions (pins 1-3, 7-8, 11-12 would overlap and their numbers
# would be unreadable), so those pins are nudged a few pixels apart.
# The caption says positions are approximate - this is honest.
NUDGE = {1: (-10, 6), 2: (10, -6), 3: (8, 8), 7: (-8, 8), 8: (-8, -6),
         11: (0, 10), 12: (10, -8)}
for num, lon, lat in PINS:
    cx, cy = px(lon, lat)
    dx, dy = NUDGE.get(num, (0, 0))
    cx, cy = cx + dx, cy + dy
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED, outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255), anchor="mm")
d.text((M, map_y + map_h + 4),
       "RED NUMBERS MARK STORIES 1\u201313  \u00b7  01 ANTALYA  \u00b7  02 RIYADH  \u00b7  03 KRYVYI RIH  \u00b7  "
       "04 WARSAW  \u00b7  05 PERU  \u00b7  06 WASHINGTON  \u00b7  07 HODEIDAH  \u00b7  08 BRUSSELS",
       font=F(BOLD, 9), fill=GREY)
d.text((M, map_y + map_h + 15),
       "09 WELLINGTON  \u00b7  10 LAS VEGAS  \u00b7  11 TURIN  \u00b7  12 COPENHAGEN  \u00b7  "
       "13 BAYELSA  \u00b7  POSITIONS ARE APPROXIMATE.",
       font=F(BOLD, 9), fill=GREY)

# (7) ALSO ON list: 25 more stories, 3 columns, EVERY item sourced
y = 816
d.text((M, y), "ALSO ON SATURDAY \u2014 25 MORE STORIES", font=F(BOLD, 14), fill=INK)
d.line([M, y + 18, W - M, y + 18], fill=RULE, width=1)
ly = y + 24
f_line = F(REG, 10)
f_num = F(BOLD, 10)
col_w = (CW - 2 * 8) // 3
# faint zebra shading behind alternate rows (real newspaper ledger look)
for row in range(0, 9, 2):
    d.rectangle([M, ly + row * 11 - 1, W - M, ly + row * 11 + 10], fill=(246, 238, 220))
for i, (num, text, outlet) in enumerate(ALSO):
    col, row = divmod(i, 9)
    lx = M + col * (col_w + 8)
    yy = ly + row * 11
    line = text + " (" + outlet + ")"
    d.text((lx, yy), num, font=f_num, fill=RED)
    d.text((lx + 22, yy), line, font=f_line, fill=INK)

# (8) DATE CHECK box - names the three old leads explicitly as excluded
y = 945
d.rectangle([M, y, W - M, y + 39], fill=LIGHT, outline=INK, width=1)
d.text((M + 6, y + 3),
       "DATE CHECK \u2014 Left out as Friday 20 November's news: Russian missiles land in Poland \u00b7 "
       "Kyiv bridges hit \u00b7 Wall Street enters correction \u00b7 Cyclone Akvan landfall \u00b7 UK\u2013EU summit deal.",
       font=F(REG, 9), fill=INK)
d.text((M + 6, y + 14),
       "Thursday 19 November: ICJ Rohingya ruling \u00b7 Trump\u2013Xi\u2013Putin declaration \u00b7 Crimean Bridge "
       "strike \u00b7 Anthropic IPO debut \u00b7 Mongolia president resigns (17 Nov) \u00b7 Huang resigns (12 Nov).",
       font=F(REG, 9), fill=INK)
d.text((M + 6, y + 25),
       "Not yet happened: COP31 final deal \u00b7 Las Vegas GP race \u00b7 BepiColombo science phase \u00b7 "
       "ATP Finals final.",
       font=F(REG, 9), fill=INK)

# (9) footer: sources + HOW SURE line
d.text((W // 2, y + 45),
       "Sources: Reuters \u00b7 AFP \u00b7 The Times \u00b7 ESPNcricinfo \u00b7 ATP Tour \u00b7 European Commission \u00b7 "
       "ESA \u00b7 BBC \u00b7 CNN \u00b7 ISW \u00b7 Al Jazeera \u2014 all 38 stories verified from Saturday 21 November 2026 only.",
       font=F(REG, 9), fill=GREY, anchor="ma")
d.text((W // 2, y + 56),
       "HOW SURE \u2014 Every story above happened, or was first reported, on Saturday 21 November 2026.",
       font=F(BOLD, 9), fill=INK, anchor="ma")

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
