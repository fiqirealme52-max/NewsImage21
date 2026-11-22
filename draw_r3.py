#!/usr/bin/env python3
"""World News - Saturday 21 November 2026 (35 stories) - REVISION 3.

First-authored build for round 3 (news-image-20261121). Built from
revision3-spec-2026-11-22.md + revision3-build-checks-2026-11-22.md
(briefs 27/28/29 replaced, new region strip) + revision3-research-2026-11-22.md
(top-10 winner patterns). Replaces the round-2 live entry (01a1fcdc,
dev 0.979552, #1198) with the #1-style package: COP31 + Bahrain + Peru
leads, THE DAY IN UTC timeline, six verified numbers, LIGHT map with
numbered pins, DATE CHECK in the winners' shape.

Layout zones (must sum to 1024; every zone's content is measured to fit):
  masthead 100 | timeline 34 | 6-number strip 84 | region strip 32 |
  leads 270 | mediums 250 | map+briefs 170 | DATE CHECK 84 = 1024.

Facts: only from sources dated 21 Nov 2026 (see revision3-research).
Banned claims (spec §11) appear nowhere: no "128 nations back", no
"5 missiles on Saturday", no "42 injured Kryvyi Rih", no Bitcoin
"-3.9%", no "Flight 767", no "Friday 19 November", no reversed
EU-Indonesia percentages, no "0.99981". All artwork is hand-drawn in
PIL (no photos, no AI generation). Deterministic: fixed seed, so two
runs produce byte-identical output.

Glyph notes (verified by pixel hash in round 2): U+2713 check and
U+2212 minus are TOFU in the Noto fonts here - checks are drawn with
line segments and every minus is an ASCII hyphen. U+25C6 diamonds are
drawn as polygons. En/em dashes, middots and accented letters are real.
"""
import hashlib
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
DARKRED = (140, 12, 12)
BLUE = (24, 62, 140)
NAVY = (16, 36, 86)
GREY = (110, 104, 92)
LIGHT = (238, 230, 212)
RULE = (26, 26, 26)
GREEN = (34, 120, 60)
SEALIGHT = (244, 241, 232)
LAND = (227, 213, 172)
LANDLINE = (201, 191, 158)
SEAGRID = (216, 205, 178)

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

# --- deterministic paper texture (drawn first, never touches text).
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


def fit_lines(text, font, max_w, max_lines, what):
    """Wrap text; fail loudly if it does not fit (never silently clip)."""
    lines = wrap(text, font, max_w)
    assert len(lines) <= max_lines, (
        f"{what}: {len(lines)} lines > {max_lines}: {lines}")
    return lines


def draw_check(x, y, s=9, color=GREEN, width=2):
    """Check mark from two line segments (U+2713 glyph is tofu)."""
    d.line([x, y + s * 0.55, x + s * 0.4, y + s * 0.95], fill=color, width=width)
    d.line([x + s * 0.4, y + s * 0.95, x + s, y + s * 0.1], fill=color, width=width)


def draw_diamond(cx, cy, r, color):
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)],
              fill=color)


def starburst(cx, cy, r, color, inner=(255, 220, 90)):
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - r * 0.4, cy - r * 0.4, cx + r * 0.4, cy + r * 0.4],
              fill=inner)


def fit_size(text, sizes, max_w, what):
    """Largest font size from `sizes` (list of (name, px)) fitting max_w."""
    for name, px in sizes:
        f = F(name, px)
        if d.textlength(text, font=f) <= max_w:
            return f, px
    raise AssertionError(f"{what}: does not fit at smallest size: {text!r}")


# ---------------------------------------------------------------- (1) masthead: 0-100
# Black kicker bar, giant serif date, italic 3-story subline, rules.
d.rectangle([0, 0, W, 18], fill=INK)
d.text((M, 4), "THE WORLD IN ONE DAY", font=F(BOLD, 10), fill=(255, 255, 255))
rbar = "35 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
d.text((W - M, 4), rbar, font=F(BOLD, 10), fill=(255, 255, 255), anchor="ra")
d.text((W // 2, 20), "Saturday 21 November 2026", font=F(SERIFB, 52),
       fill=INK, anchor="ma")
d.text((W // 2, 78), "Iran hits Bahrain bases  \u00b7  a deep quake shakes Peru  \u00b7  "
       "COP31 runs into overtime", font=F(ITAL, 14), fill=INK, anchor="ma")
d.line([M, 96, W - M, 96], fill=RED, width=3)
d.line([M, 99, W - M, 99], fill=RULE, width=1)

# ---------------------------------------------------------------- (2) timeline: 100-134
TIMELINE = [
    ("00:09", "Peru quake M6.7"),
    ("02:00", "Sinaloa raid, Guasave"),
    ("05:00", "Tanker hit off Khasab"),
    ("05:50", "2nd tanker hit, 17 nm E"),
    ("09:42", "Banda Sea M6.8"),
    ("15:16", "Bitcoin over $60,000"),
    ("18:24", "BepiColombo burn"),
]
d.rectangle([M, 100, M + 92, 134], fill=INK)
d.text((M + 46, 105), "THE DAY", font=F(BOLD, 11), fill=(255, 255, 255), anchor="ma")
d.text((M + 46, 118), "IN UTC", font=F(BOLD, 11), fill=(255, 255, 255), anchor="ma")
tl_x0, tl_x1 = M + 100, W - M
slot_w = (tl_x1 - tl_x0) / 7
d.line([tl_x0, 129, tl_x1, 129], fill=(150, 142, 124), width=1)
for i, (tm, lab) in enumerate(TIMELINE):
    cx = tl_x0 + slot_w * (i + 0.5)
    d.text((cx, 101), tm, font=F(BOLD, 10), fill=RED, anchor="ma")
    d.text((cx, 113), lab, font=F(REG, 9), fill=INK, anchor="ma")
    if tm == "15:16":
        draw_diamond(cx, 129, 4, RED)  # Bitcoin re-cross: diamond, not dot
    else:
        d.ellipse([cx - 3, 126, cx + 3, 132], fill=BLUE)

# ---------------------------------------------------------------- (3) six-number strip: 134-218
NUMBERS = [
    ("6.7", "Peru quake magnitude (USGS)"),
    ("3", "missiles down over Riyadh (coalition)"),
    ("2", "tankers hit off Khasab (UKMTO)"),
    ("146", "safe after the Davao landing (CAAP)"),
    ("124*", "K L Rahul's score at tea (India 344/2)"),
    ("90.4%", "Indonesian lines duty-free into the EU (IEU-CEPA)"),
]
cell_w = CW / 6
for i, (num, label) in enumerate(NUMBERS):
    cx = M + cell_w * (i + 0.5)
    d.text((cx, 138), num, font=F(SERIFB, 38), fill=INK, anchor="ma")
    lab = fit_lines(label, F(BOLD, 11), cell_w - 14, 2, f"strip {num}")
    for j, ln in enumerate(lab):
        d.text((cx, 182 + j * 13), ln, font=F(BOLD, 11), fill=GREY, anchor="ma")
    if i:
        d.line([M + cell_w * i, 142, M + cell_w * i, 210],
               fill=(200, 192, 172), width=1)
d.line([M, 217, W - M, 217], fill=RULE, width=1)

# ---------------------------------------------------------------- (4) region strip: 218-250
# EUROPE 8 · MIDDLE EAST 6 · AMERICAS 5 · ASIA 9 · OCEANIA 3 · AFRICA 1 ·
# GLOBAL 3 = 35 (recomputed from the final story list, memo 22 Nov).
REGIONS = [
    ("EUROPE", 8, (31, 78, 156)),
    ("MIDDLE EAST", 6, (163, 22, 22)),
    ("AMERICAS", 5, (14, 124, 123)),
    ("ASIA", 9, (46, 125, 50)),
    ("OCEANIA", 3, (106, 76, 147)),
    ("AFRICA", 1, (192, 86, 33)),
    ("GLOBAL", 3, (90, 90, 90)),
]
assert sum(c for _, c, _ in REGIONS) == 35, "region strip must sum to 35"
tab_w = (CW - 6 * 6) // 7
for i, (name, cnt, col) in enumerate(REGIONS):
    tx = M + i * (tab_w + 6)
    tw = tab_w + (CW - 6 * 6 - 7 * tab_w if i == 6 else 0)
    d.rounded_rectangle([tx, 222, tx + tw, 246], radius=4, fill=col)
    lab = f"{name}  {cnt}"
    f, _ = fit_size(lab, [(BOLD, 12), (BOLD, 11)], tw - 8, f"region {name}")
    d.text((tx + tw // 2, 228), lab, font=f, fill=(255, 255, 255), anchor="ma")

# ---------------------------------------------------------------- lead scenes (314 x 148 each)
def scene_cop31(x, y, w, h):
    """Globe + 1.5C thermometer + DAY 13 clock + draft with FOSSIL FUELS
    struck through. Pale mint sky."""
    d.rectangle([x, y, x + w, y + h], fill=(216, 234, 222))
    # globe, left
    gx, gy, gr = x + 78, y + 66, 46
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(46, 111, 176),
              outline=(20, 60, 110), width=2)
    d.ellipse([gx - 26, gy - 30, gx + 2, gy - 6], fill=(62, 155, 79))
    d.ellipse([gx - 6, gy + 2, gx + 30, gy + 28], fill=(62, 155, 79))
    d.ellipse([gx + 12, gy - 34, gx + 34, gy - 14], fill=(62, 155, 79))
    d.arc([gx - gr + 6, gy - 18, gx + gr - 10, gy + 10], 200, 330,
          fill=(255, 255, 255), width=3)
    d.arc([gx - gr + 10, gy + 8, gx + gr - 6, gy + 30], 200, 340,
          fill=(255, 255, 255), width=3)
    # thermometer, centre-right
    tx = x + 168
    d.rectangle([tx, y + 18, tx + 16, y + 108], fill=(255, 255, 255),
                outline=INK, width=2)
    d.rectangle([tx + 2, y + 62, tx + 14, y + 106], fill=(200, 30, 30))
    d.ellipse([tx - 6, y + 100, tx + 22, y + 132], fill=(200, 30, 30),
              outline=INK, width=2)
    for k in range(5):
        yy = y + 30 + k * 18
        d.line([tx + 16, yy, tx + 22, yy], fill=INK, width=2)
    d.text((tx + 26, y + 20), "1.5\u00b0C", font=F(BLACK, 20), fill=RED)
    d.text((tx + 26, y + 44), "LIMIT", font=F(BOLD, 9), fill=GREY)
    # clock DAY 13, top right
    cx, cy, cr = x + 282, y + 34, 20
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([cx, cy, cx, cy - 13], fill=INK, width=2)
    d.line([cx, cy, cx + 9, cy + 5], fill=INK, width=2)
    d.text((cx, cy + 24), "DAY 13", font=F(BLACK, 11), fill=RED, anchor="ma")
    # draft document, bottom right, FOSSIL FUELS struck through
    dx, dy = x + 178, y + 96
    d.rectangle([dx, dy, dx + 128, dy + 46], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((dx + 6, dy + 3), "DRAFT 2 \u00b7 80 ARTICLES", font=F(BOLD, 8),
           fill=GREY)
    for k in range(2):
        d.line([dx + 6, dy + 17 + k * 6, dx + 122, dy + 17 + k * 6],
               fill=(180, 175, 160), width=2)
    d.text((dx + 6, dy + 28), "FOSSIL FUELS", font=F(BLACK, 11), fill=RED)
    d.line([dx + 4, dy + 34, dx + 92, dy + 34], fill=RED, width=2)


def scene_bahrain(x, y, w, h):
    """Stylised Gulf map: tan land, pale-blue sea, Bahrain island, two
    blast markers on the bases, two tankers burning off Khasab."""
    d.rectangle([x, y, x + w, y + h], fill=(127, 168, 201))
    # land: Iran top, Arabia bottom-left, Oman bottom-right
    d.polygon([(x, y), (x + w, y), (x + w, y + 34), (x + 210, y + 52),
               (x + 120, y + 40), (x, y + 46)], fill=(232, 217, 176))
    d.polygon([(x, y + h), (x, y + 96), (x + 90, y + 84), (x + 150, y + 104),
               (x + 130, y + h)], fill=(232, 217, 176))
    d.polygon([(x + w, y + h), (x + w, y + 100), (x + 262, y + 104),
               (x + 252, y + h)], fill=(232, 217, 176))
    d.text((x + 12, y + 6), "IRAN", font=F(BLACK, 12), fill=(90, 70, 40))
    d.text((x + 16, y + 118), "SAUDI ARABIA", font=F(BOLD, 9),
           fill=(120, 100, 60))
    d.text((x + 280, y + 132), "OMAN", font=F(BOLD, 9), fill=(120, 100, 60),
           anchor="ma")
    # Bahrain island (kept visible: blasts sit on its edges, not its centre)
    bx, by = x + 150, y + 66
    d.ellipse([bx - 14, by - 10, bx + 14, by + 10], fill=(232, 217, 176),
              outline=(120, 100, 60), width=1)
    d.text((bx, by - 26), "BAHRAIN", font=F(BLACK, 11), fill=INK, anchor="ma")
    # two blast markers on the bases, at the island's edges
    starburst(bx - 14, by + 2, 8, (230, 90, 20))
    starburst(bx + 14, by + 6, 7, (230, 90, 20))
    d.text((bx, by + 22), "2 AIR BASES HIT", font=F(BLACK, 9), fill=DARKRED,
           anchor="ma")
    # Strait of Hormuz label
    d.text((x + 236, y + 52), "HORMUZ", font=F(BOLD, 9), fill=(255, 255, 255),
           anchor="ma")
    # two tankers off Khasab, burning - both in the blue sea, clear of land
    for tx, ty in [(x + 200, y + 100), (x + 238, y + 112)]:
        d.rectangle([tx - 16, ty - 5, tx + 16, ty + 5], fill=(40, 40, 40))
        d.rectangle([tx + 6, ty - 11, tx + 14, ty - 5], fill=(240, 240, 240))
        starburst(tx - 8, ty - 12, 8, (240, 110, 20))
        d.line([tx - 4, ty - 22, tx - 2, ty - 30], fill=(120, 120, 120),
               width=3)
        d.line([tx + 2, ty - 24, tx + 6, ty - 32], fill=(150, 150, 150),
               width=3)
    d.text((x + 222, y + 130), "2 TANKERS HIT", font=F(BLACK, 9),
           fill=DARKRED, anchor="ma")


def scene_peru(x, y, w, h):
    """Seismograph trace over mountains + earth cross-section with the
    108 km hypocentre, Lima houses at the surface."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 228, 205))
    # seismograph trace across the sky
    pts = [(x + 6, y + 26)]
    import random as _r
    srng = _r.Random(20261121)
    px = x + 6
    while px < x + w - 8:
        step = srng.choice([6, 8, 10])
        amp = srng.choice([2, 4, 6, 22, 30, 14, 5, 3])
        px += step
        pts.append((px, y + 26 + srng.choice([-1, 1]) * amp))
    pts.append((x + w - 6, y + 26))
    d.line(pts, fill=(200, 30, 30), width=2, joint="curve")
    # mountains
    d.polygon([(x, y + 74), (x + 60, y + 34), (x + 110, y + 74)],
              fill=(120, 90, 60))
    d.polygon([(x + 90, y + 74), (x + 170, y + 28), (x + 240, y + 74)],
              fill=(96, 72, 48))
    d.polygon([(x + 150, y + 44), (x + 170, y + 28), (x + 190, y + 44)],
              fill=(250, 250, 250))
    # ground line + earth strata
    d.line([x, y + 74, x + w, y + 74], fill=INK, width=2)
    for k, col in enumerate([(210, 190, 150), (190, 165, 120), (170, 140, 95)]):
        d.rectangle([x, y + 76 + k * 24, x + w, y + 98 + k * 24], fill=col)
    # dashed depth line to the hypocentre
    hx, hy = x + 200, y + 128
    for k in range(0, 52, 6):
        d.line([hx, y + 76 + k, hx, y + 80 + k], fill=RED, width=2)
    starburst(hx, hy, 9, (200, 30, 30))
    d.text((hx + 14, hy - 6), "108 KM", font=F(BLACK, 11), fill=RED)
    d.text((hx + 14, hy + 6), "DEEP", font=F(BOLD, 8), fill=GREY)
    # Lima houses at the surface, left
    for hx0 in (x + 14, x + 40, x + 64):
        d.rectangle([hx0, y + 58, hx0 + 20, y + 74], fill=(255, 250, 240),
                    outline=INK, width=1)
        d.polygon([(hx0 - 2, y + 58), (hx0 + 10, y + 48), (hx0 + 22, y + 58)],
                  fill=(176, 60, 40))
    # "LIMA" label: sits in the sky, top left, on a backing patch that
    # knocks out the seismograph trace (it used to sit inside the earth
    # strata, below the ground line - as if Lima were buried).
    d.rectangle([x + 6, y + 4, x + 42, y + 16], fill=(238, 228, 205))
    d.text((x + 8, y + 6), "LIMA", font=F(BOLD, 9), fill=INK)


# ---------------------------------------------------------------- leads: 250-520
LEADS = [
    {"num": "1", "place": "ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
     "tag": "NO DEAL \u00b7 DAY 13", "status": "CONFIRMED",
     "headline": "COP31 climate talks run into overtime",
     "sub": "Talks miss their Friday deadline; a draft with no mention of "
            "fossil fuels splits nearly 200 countries.",
     "source": "Reuters, AFP", "scene": scene_cop31},
    {"num": "2", "place": "BAHRAIN \u00b7 HORMUZ \u00b7 IRAN WAR",
     "tag": "2 BASES \u00b7 2 TANKERS HIT", "status": "CONFIRMED",
     "headline": "Iran strikes Bahrain bases; tankers hit off Oman",
     "sub": "IRGC says it hit US radar at two bases; Bahrain says a "
            "civilian plant burned; two tankers struck off Khasab.",
     "source": "Al Jazeera, Xinhua, UKMTO", "scene": scene_bahrain},
    {"num": "3", "place": "JUN\u00cdN, PERU \u00b7 EARTHQUAKE",
     "tag": "00:09 UTC \u00b7 108 KM DEEP", "status": "OFFICIAL",
     "headline": "Deep 6.7 earthquake shakes central Peru",
     "sub": "Centred near Carhuamayo and felt in Lima; no deaths, no "
            "tsunami risk. USGS 108 km deep; IGP 129 km.",
     "source": "USGS, IGP", "scene": scene_peru},
]
lead_w = 314
lead_xs = [M, M + lead_w + 13, M + 2 * (lead_w + 13)]
LY = 250
for j, lead in enumerate(LEADS):
    x0 = lead_xs[j]
    lead["scene"](x0, LY, lead_w, 148)
    d.rectangle([x0, LY, x0 + lead_w, LY + 148], outline=INK, width=1)
    # red tag bar under the scene
    d.rectangle([x0, LY + 148, x0 + lead_w, LY + 164], fill=RED)
    d.text((x0 + 8, LY + 151), lead["tag"], font=F(BLACK, 11),
           fill=(255, 255, 255))
    # number + place + status line
    ny = LY + 168
    d.text((x0, ny), lead["num"], font=F(BLACK, 12), fill=RED)
    d.text((x0 + 16, ny + 1), lead["place"], font=F(BOLD, 10), fill=GREY)
    st = lead["status"]
    sw = d.textlength(st, font=F(BOLD, 10))
    draw_check(x0 + lead_w - sw - 16, ny + 2, 9)
    d.text((x0 + lead_w - sw, ny + 1), st, font=F(BOLD, 10), fill=GREEN)
    # headline, max 2 lines, serif bold
    hf = F(SERIFB, 22)
    hl = wrap(lead["headline"], hf, lead_w)
    if len(hl) > 2:
        hf = F(SERIFB, 20)
        hl = fit_lines(lead["headline"], hf, lead_w, 2,
                       f"lead {lead['num']} headline")
    for i, ln in enumerate(hl):
        d.text((x0, LY + 180 + i * 26), ln, font=hf, fill=INK)
    # sub, max 2 lines
    sub = fit_lines(lead["sub"], F(REG, 11), lead_w, 2,
                    f"lead {lead['num']} sub")
    for i, ln in enumerate(sub):
        d.text((x0, LY + 232 + i * 13), ln, font=F(REG, 11), fill=INK)
    # source line
    d.text((x0, LY + 258), lead["source"], font=F(ITAL, 10), fill=GREY)
    if j:
        d.line([x0 - 7, LY + 2, x0 - 7, LY + 268], fill=(210, 200, 180),
               width=1)
d.line([M, 519, W - M, 519], fill=RULE, width=1)

# ---------------------------------------------------------------- medium scenes (186 x 58 each)
# Each draws only the picture; the red tag (top-left) and the black source
# strip (bottom 11 px) are added by the grid code below.
def scene_saudi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 28, 64))
    # night skyline
    for bx, bw, bh in [(0, 26, 22), (30, 18, 30), (52, 30, 18), (86, 22, 34),
                       (112, 26, 20), (142, 20, 28), (166, 20, 16)]:
        d.rectangle([x + bx, y + h - 11 - bh, x + bx + bw, y + h - 11],
                    fill=(8, 14, 34))
        for wy in range(y + h - 11 - bh + 4, y + h - 13, 7):
            d.point((x + bx + 6, wy), fill=(255, 220, 120))
            d.point((x + bx + bw - 6, wy), fill=(255, 220, 120))
    # three missile trails + bursts
    for mx, my, ex, ey in [(20, 48, 52, 14), (80, 50, 118, 18),
                           (140, 48, 168, 12)]:
        d.line([(x + mx, y + my), (x + (mx + ex) // 2, y + (my + ey) // 2 - 8),
                (x + ex, y + ey)], fill=(255, 200, 90), width=2)
        starburst(x + ex, y + ey, 7, (240, 110, 20))
        d.ellipse([x + mx - 2, y + my - 2, x + mx + 2, y + my + 2],
                  fill=(255, 240, 180))


def scene_sinaloa(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 32, 58))
    # road with perspective lines
    d.polygon([(x, y + h - 11), (x + w, y + h - 11), (x + w, y + 34),
               (x, y + 34)], fill=(48, 48, 52))
    d.line([x + 40, y + h - 11, x + 80, y + 34], fill=(220, 200, 80), width=2)
    d.line([x + w - 40, y + h - 11, x + 110, y + 34], fill=(220, 200, 80),
           width=2)
    # houses
    for hx in (8, 130):
        d.rectangle([x + hx, y + 22, x + hx + 34, y + 34], fill=(70, 60, 50))
        d.polygon([(x + hx - 2, y + 22), (x + hx + 17, y + 12),
                   (x + hx + 36, y + 22)], fill=(120, 40, 30))
    # helicopter with searchlight cone
    hx, hy = x + 118, y + 16
    d.ellipse([hx - 16, hy - 5, hx + 16, hy + 5], fill=(10, 10, 12))
    d.line([hx - 22, hy - 8, hx + 22, hy - 8], fill=(10, 10, 12), width=2)
    d.line([hx + 14, hy - 4, hx + 26, hy - 10], fill=(10, 10, 12), width=2)
    d.polygon([(hx - 3, hy + 4), (hx + 3, hy + 4), (hx + 16, y + 34),
               (hx - 10, y + 34)], fill=(255, 240, 160))
    # two soldiers
    for sx in (58, 74):
        d.ellipse([x + sx, y + 36, x + sx + 6, y + 42], fill=(20, 20, 22))
        d.rectangle([x + sx - 1, y + 42, x + sx + 7, y + 52],
                    fill=(30, 60, 30))


def scene_euindo(x, y, w, h):
    # EU flag left, Indonesia flag right, signed document centre-bottom
    d.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
    # 12 stars on a tight circle (was a wide flat ellipse: read as random
    # scattered dots, and the document overlapped the rightmost stars)
    for k in range(12):
        ang = 2 * math.pi * k / 12 - math.pi / 2
        sx = x + 44 + 18 * math.cos(ang)
        sy = y + 24 + 10 * math.sin(ang)
        draw_diamond(sx, sy, 3, (255, 204, 0))
    d.rectangle([x + 96, y, x + w, y + 24], fill=(215, 30, 30))
    d.rectangle([x + 96, y + 24, x + w, y + h - 11], fill=(255, 255, 255))
    d.rectangle([x + 68, y + 30, x + 130, y + h - 11], fill=(255, 255, 255),
                outline=INK, width=1)
    d.text((x + 74, y + 32), "IEU-CEPA", font=F(BLACK, 9), fill=INK)
    for k in range(2):
        d.line([x + 74, y + 44 + k * 5, x + 124, y + 44 + k * 5],
               fill=(180, 175, 160), width=2)
    d.line([x + 74, y + 52, x + 102, y + 50], fill=(24, 62, 140), width=2)
    d.ellipse([x + 112, y + 46, x + 122, y + 56], fill=(176, 18, 18))


def scene_robot(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 216, 235))
    # UN flag, left
    d.rectangle([x + 12, y + 10, x + 56, y + 36], fill=(90, 140, 200))
    d.ellipse([x + 28, y + 16, x + 40, y + 30], fill=(255, 255, 255))
    d.line([x + 12, y + 36, x + 12, y + h - 11], fill=INK, width=2)
    # robot, right
    rx, ry = x + 118, y + 14
    d.line([rx, ry, rx, ry - 6], fill=INK, width=2)
    d.ellipse([rx - 2, ry - 9, rx + 2, ry - 5], fill=RED)
    d.rounded_rectangle([rx - 16, ry, rx + 16, ry + 16], radius=4,
                        fill=(230, 230, 235), outline=INK, width=1)
    d.ellipse([rx - 9, ry + 6, rx - 3, ry + 12], fill=INK)
    d.ellipse([rx + 3, ry + 6, rx + 9, ry + 12], fill=INK)
    d.rounded_rectangle([rx - 20, ry + 18, rx + 20, ry + 34], radius=4,
                        fill=(200, 205, 215), outline=INK, width=1)
    d.rectangle([rx - 8, ry + 24, rx + 8, ry + 28], fill=(176, 18, 18))
    d.line([rx - 20, ry + 22, rx - 30, ry + 30], fill=INK, width=3)
    d.line([rx + 20, ry + 22, rx + 30, ry + 30], fill=INK, width=3)
    d.text((x + 96, y + 40), "2028", font=F(BLACK, 12), fill=NAVY)


def scene_davao(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 205, 235))
    d.ellipse([x + 12, y + 8, x + 44, y + 18], fill=(255, 255, 255))
    d.ellipse([x + 130, y + 4, x + 160, y + 12], fill=(255, 255, 255))
    # runway
    d.rectangle([x, y + h - 18, x + w, y + h - 11], fill=(90, 90, 95))
    # aircraft
    ax, ay = x + 30, y + 26
    d.rounded_rectangle([ax, ay, ax + 120, ay + 14], radius=7,
                        fill=(255, 255, 255), outline=INK, width=1)
    d.polygon([(ax + 108, ay), (ax + 128, ay - 12), (ax + 136, ay - 12),
               (ax + 122, ay)], fill=(200, 30, 30))
    d.polygon([(ax + 52, ay + 12), (ax + 78, ay + 12), (ax + 66, ay + 20),
               (ax + 48, ay + 20)], fill=(200, 30, 30))
    for wx in range(ax + 12, ax + 100, 12):
        d.rectangle([wx, ay + 4, wx + 6, ay + 8], fill=(60, 120, 180))
    d.text((ax + 4, ay + 1), "PX19", font=F(BOLD, 8), fill=INK)
    # evacuation slide from the door
    d.polygon([(ax + 88, ay + 12), (ax + 94, ay + 12), (ax + 118, y + h - 18),
               (ax + 106, y + h - 18)], fill=(255, 210, 40),
              outline=(180, 140, 0))


def scene_bitcoin(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    for gx in range(x, x + w, 24):
        d.line([gx, y, gx, y + h - 11], fill=(235, 235, 235), width=1)
    for gy in range(y, y + h - 11, 12):
        d.line([x, gy, x + w, gy], fill=(235, 235, 235), width=1)
    pts = [(x + 8, y + 12), (x + 40, y + 16), (x + 70, y + 14),
           (x + 100, y + 26), (x + 130, y + 38), (x + 160, y + 44)]
    d.line(pts, fill=(200, 30, 30), width=3, joint="curve")
    d.ellipse([x + 152, y + 36, x + 168, y + 52], fill=(200, 30, 30))
    # gold coin
    cx, cy, cr = x + 34, y + 32, 13
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(247, 147, 26),
              outline=(180, 100, 0), width=2)
    d.text((cx, cy), "B", font=F(BLACK, 14), fill=(255, 255, 255), anchor="mm")
    d.text((x + 8, y + h - 26), "$55,789", font=F(BLACK, 13), fill=RED)
    d.text((x + 82, y + h - 25), "-9.9%", font=F(BOLD, 10), fill=RED)


def scene_vegas(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 38))
    # track
    d.rectangle([x, y + 30, x + w, y + h - 11], fill=(60, 60, 68))
    d.line([x, y + 30, x + w, y + 30], fill=(255, 255, 255), width=1)
    d.line([x, y + 42, x + w, y + 42], fill=(255, 220, 0), width=1)
    # F1 car
    cx, cy = x + 78, y + 34
    d.polygon([(cx - 52, cy + 6), (cx - 40, cy - 4), (cx + 20, cy - 6),
               (cx + 48, cy + 2), (cx + 44, cy + 6)], fill=(200, 20, 20))
    d.polygon([(cx - 52, cy + 6), (cx - 58, cy + 2), (cx - 58, cy - 6),
               (cx - 50, cy - 6)], fill=(120, 10, 10))
    d.ellipse([cx - 34, cy + 2, cx - 18, cy + 14], fill=(10, 10, 10),
              outline=(120, 120, 120), width=1)
    d.ellipse([cx + 18, cy + 2, cx + 34, cy + 14], fill=(10, 10, 10),
              outline=(120, 120, 120), width=1)
    d.text((cx - 8, cy - 4), "63", font=F(BLACK, 9), fill=(255, 255, 255))
    # checkered flag, right
    fx, fy = x + 158, y + 8
    for r in range(3):
        for c in range(4):
            col = INK if (r + c) % 2 == 0 else (255, 255, 255)
            d.rectangle([fx + c * 5, fy + r * 5, fx + c * 5 + 5, fy + r * 5 + 5],
                        fill=col, outline=INK, width=1)
    d.line([fx, fy, fx, fy + 22], fill=INK, width=2)
    # neon skyline hint
    for bx, bh, col in [(8, 12, (255, 80, 160)), (24, 18, (80, 200, 255)),
                        (44, 10, (255, 200, 60))]:
        d.rectangle([x + bx, y + 30 - bh, x + bx + 12, y + 30], fill=col)


def scene_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 120))
    d.rectangle([x, y + h - 22, x + w, y + h - 11], fill=(110, 160, 95))
    # pitch
    d.rectangle([x + 60, y + 16, x + 130, y + h - 11], fill=(214, 190, 140))
    # stumps
    for sx in (150, 156, 162):
        d.line([x + sx, y + 20, x + sx, y + 32], fill=(255, 220, 60), width=2)
    d.line([x + 150, y + 20, x + 162, y + 20], fill=(255, 220, 60), width=2)
    # batsman: white kit, red helmet, thick bat raised (v1's figure read
    # as a pawn: thin 4 px bat, no helmet, head the same colour as the kit)
    bx, by = x + 100, y + 22
    d.ellipse([bx - 6, by - 13, bx + 6, by - 1], fill=(210, 170, 130))
    d.pieslice([bx - 6, by - 14, bx + 6, by - 2], 180, 360, fill=(200, 30, 30))
    d.rectangle([bx - 7, by - 1, bx + 7, by + 15], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([bx - 7, by + 15, bx - 1, by + 27], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([bx + 1, by + 15, bx + 7, by + 27], fill=(255, 255, 255),
                outline=INK, width=1)
    d.line([bx + 5, by, bx + 18, by - 18], fill=(140, 100, 60), width=6)
    d.line([bx + 5, by, bx + 18, by - 18], fill=(200, 160, 100), width=2)
    d.ellipse([x + 132, y + 8, x + 138, y + 14], fill=(200, 30, 30))
    # scoreboard hint
    d.rectangle([x + 8, y + 8, x + 44, y + 22], fill=INK)
    d.text((x + 26, y + 11), "124*", font=F(BOLD, 9), fill=(255, 255, 255),
           anchor="ma")


def scene_kryvyi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 44))
    # buildings
    for bx, bw, bh in [(6, 30, 20), (40, 24, 28), (68, 34, 16), (106, 26, 24),
                       (136, 30, 18), (168, 18, 14)]:
        d.rectangle([x + bx, y + h - 11 - bh, x + bx + bw, y + h - 11],
                    fill=(10, 12, 24))
        for wy in range(y + h - 9 - bh, y + h - 13, 6):
            d.point((x + bx + 5, wy), fill=(255, 220, 120))
    # fire + smoke on the restaurant building
    fx = x + 52
    for k, (fw, fh) in enumerate([(16, 18), (10, 12), (6, 8)]):
        d.polygon([(fx - fw // 2, y + h - 11 - 26), (fx, y + h - 11 - 26 - fh),
                   (fx + fw // 2, y + h - 11 - 26)],
                  fill=[(240, 110, 20), (250, 180, 40), (255, 230, 120)][k])
    d.ellipse([fx - 4, y + 6, fx + 4, y + 12], fill=(120, 120, 120))
    d.ellipse([fx + 2, y + 2, fx + 12, y + 10], fill=(150, 150, 150))
    # ambulance, right
    ax, ay = x + 128, y + h - 26
    d.rectangle([ax, ay, ax + 44, ay + 13], fill=(255, 255, 255), outline=INK,
                width=1)
    d.rectangle([ax + 16, ay + 3, ax + 22, ay + 10], fill=RED)
    d.rectangle([ax + 18, ay + 5, ax + 20, ay + 8], fill=(255, 255, 255))
    d.ellipse([ax + 6, ay + 11, ax + 12, ay + 17], fill=INK)
    d.ellipse([ax + 32, ay + 11, ax + 38, ay + 17], fill=INK)


def scene_space(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 26))
    for sx, sy in [(12, 8), (40, 16), (70, 6), (100, 12), (150, 8),
                   (170, 20), (30, 30), (120, 26), (60, 40), (160, 40)]:
        d.point((x + sx, y + sy), fill=(255, 255, 255))
    # Mercury, right
    mx, my, mr = x + 138, y + 28, 20
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(190, 130, 80),
              outline=(140, 90, 50), width=1)
    for cx, cy, cr in [(mx - 8, my - 6, 3), (mx + 6, my + 2, 4),
                       (mx - 2, my + 10, 2), (mx + 10, my - 10, 2)]:
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(150, 95, 55))
    # spacecraft with solar panels, left, thruster flame
    sx, sy = x + 56, y + 26
    d.rectangle([sx - 8, sy - 6, sx + 8, sy + 6], fill=(200, 200, 210),
                outline=INK, width=1)
    d.rectangle([sx - 34, sy - 4, sx - 10, sy + 4], fill=(40, 90, 180),
                outline=INK, width=1)
    d.rectangle([sx + 10, sy - 4, sx + 34, sy + 4], fill=(40, 90, 180),
                outline=INK, width=1)
    d.polygon([(sx - 8, sy), (sx - 20, sy - 4), (sx - 20, sy + 4)],
              fill=(240, 140, 30))


# ---------------------------------------------------------------- mediums: 520-770
MEDIUM = [
    ("4", "Three Houthi missiles shot down over Riyadh",
     "Three missiles down before dawn; two more fell over Jizan Friday evening.",
     "3 SHOT DOWN", "Reuters, AFP", scene_saudi),
    ("5", "Mexico captures 'El Chapo Isidro'; 11 die",
     "FBI top-10 fugitive seized in Guasave; 7 gunmen and 4 soldiers killed.",
     "11 DEAD", "Reuters, AP", scene_sinaloa),
    ("6", "EU and Indonesia sign trade pact after a decade",
     "Signed in Brussels; 98.5% EU lines, 90.4% Indonesian lines duty-free.",
     "90.4% DUTY-FREE", "Reuters, European Commission", scene_euindo),
    ("7", "UN talks set a 2-year path on killer robots",
     "States agree a 2-year path to an instrument by 2028; binding undecided.",
     "2028 AIM", "AP", scene_robot),
    ("8", "Jet lands safely after engine-fire alert",
     "Air Niugini PX19 diverts to Davao; all 146 aboard safe.",
     "146 SAFE", "CAAP, AP", scene_davao),
    ("9", "Bitcoin sinks to $55,789 - lowest since Sep 2024",
     "Down 9.9% to $55,789 at 05:56 UTC, then back over $60,000 by evening.",
     "-9.9%", "CoinGecko, Investing.com", scene_bitcoin),
    ("10", "Russell fastest in final Las Vegas practice",
     "1:34.041 in the dry final session; Antonelli penalised, Verstappen on pole.",
     "1:34.041", "Formula 1", scene_vegas),
    ("11", "Rahul hits a century against New Zealand",
     "124 not out at tea, India 344 for 2, replying to 368; he finished on 136.",
     "124*", "AFP, ICC", scene_cricket),
    ("12", "Russian strikes kill 2 in Kryvyi Rih; ~60 hurt",
     "A boy of 7 and a paramedic die as missiles hit a restaurant, then rescuers.",
     "~60 HURT", "AP", scene_kryvyi),
    ("13", "BepiColombo reaches Mercury",
     "Thrusters fire at 19:24 CET; ESA confirms orbit capture the same day.",
     "19:24 CET", "ESA", scene_space),
]
med_w = [186, 186, 185, 186, 185]
med_x = [M]
for wd in med_w[:-1]:
    med_x.append(med_x[-1] + wd + 10)
MY0 = 520
for idx, (num, headline, sub, tag, source, scene) in enumerate(MEDIUM):
    r, c = divmod(idx, 5)
    x0 = med_x[c]
    y0 = MY0 + r * 125
    # scene band, 58 px, with red tag top-left and black source strip bottom
    scene(x0, y0, med_w[c], 58)
    d.rectangle([x0, y0, x0 + med_w[c], y0 + 58], outline=INK, width=1)
    tag_f = F(BLACK, 9)
    tw = d.textlength(tag, font=tag_f) + 10
    d.rectangle([x0, y0, x0 + tw, y0 + 12], fill=RED)
    d.text((x0 + 5, y0 + 2), tag, font=tag_f, fill=(255, 255, 255))
    d.rectangle([x0, y0 + 47, x0 + med_w[c], y0 + 58], fill=INK)
    d.text((x0 + 4, y0 + 49), source, font=F(REG, 8), fill=(255, 255, 255))
    # headline, max 2 lines, serif bold
    hf = F(SERIFB, 14)
    hl = wrap(headline, hf, med_w[c])
    if len(hl) > 2:
        hf = F(SERIFB, 13)
        hl = fit_lines(headline, hf, med_w[c], 2, f"medium {num} headline")
    for i, ln in enumerate(hl):
        d.text((x0, y0 + 61 + i * 17), ln, font=hf, fill=INK)
    # sub, max 2 lines (font 10, fall back to 9)
    sf = F(REG, 10)
    sl = wrap(sub, sf, med_w[c])
    if len(sl) > 2:
        sf = F(REG, 9)
        sl = fit_lines(sub, sf, med_w[c], 2, f"medium {num} sub")
    for i, ln in enumerate(sl):
        d.text((x0, y0 + 61 + len(hl) * 17 + 2 + i * 12), ln, font=sf,
               fill=INK)
    if c:
        d.line([x0 - 5, y0 + 2, x0 - 5, y0 + 120], fill=(210, 200, 180),
               width=1)
    if r:
        d.line([x0, y0 - 5, x0 + med_w[c], y0 - 5], fill=(210, 200, 180),
               width=1)
d.line([M, 769, W - M, 769], fill=RULE, width=1)

# ---------------------------------------------------------------- map + briefs: 770-940
# Light map (winners' style): pale sea, tan continents, red numbered pins.
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
# pins: (number, lon, lat, nudge) - 9 (Bitcoin, world market) and 13
# (BepiColombo, space) live only in the caption, never on the map.
# Brussels/Geneva truly overlap at this scale (4 px apart), so their
# numbered circles are offset with a leader line from a dot at the true
# position - the honest cartographic fix, instead of nudging a pin onto
# the wrong country (v1 put Brussels over the UK). Other nudges <= 10 px
# keep every pin on the right landmass.
PINS = [
    (1, 30.7, 36.9, (0, -4)), (2, 50.6, 26.2, (10, -6)),
    (3, -75.9, -11.2, (0, 0)), (4, 46.7, 24.6, (0, 0)),
    (5, -108.5, 25.6, (-8, 8)), (6, 4.35, 50.85, (-14, -12)),
    (7, 6.14, 46.2, (-14, 12)), (8, 125.6, 7.07, (0, 0)),
    (10, -115.1, 36.2, (0, -4)), (11, 174.8, -41.3, (-10, 0)),
    (12, 33.4, 47.9, (8, -4)),
]
LEADER_PINS = {6, 7}
MAP_X0, MAP_X1, MAP_Y0, MAP_Y1 = M, 463, 788, 926
MAP_W, MAP_H = MAP_X1 - MAP_X0, MAP_Y1 - MAP_Y0
d.text((M, 770), "WHERE IT HAPPENED", font=F(BOLD, 12), fill=INK)
d.text((475, 770), "ALSO ON SATURDAY \u2014 22 MORE STORIES", font=F(BOLD, 12),
       fill=INK)
d.rectangle([MAP_X0, MAP_Y0, MAP_X1, MAP_Y1], fill=SEALIGHT, outline=INK,
            width=1)
for gx in range(-150, 181, 30):
    xg = MAP_X0 + (gx + 180) / 360 * MAP_W
    d.line([xg, MAP_Y0, xg, MAP_Y1], fill=SEAGRID, width=1)
for gy in [-60, -30, 0, 30, 60]:
    yg = MAP_Y0 + (75 - gy) / 135 * MAP_H
    d.line([MAP_X0, yg, MAP_X1, yg], fill=SEAGRID, width=1)


def mpx(lon, lat):
    return (MAP_X0 + (lon + 180) / 360 * MAP_W,
            MAP_Y0 + (75 - lat) / 135 * MAP_H)


for poly in CONTINENTS:
    d.polygon([mpx(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LANDLINE)
mlab = F(BOLD, 8)
# ARCTIC dropped: at this scale its label sat on northern land, and pin 6
# covered it in v1 ("6CTIC"). PACIFIC moved off pin 10 (v1: "PAC" + pin).
for (tx, ty, word) in [(0.24, 0.82, "ATLANTIC"), (0.68, 0.88, "INDIAN"),
                       (0.07, 0.68, "PACIFIC")]:
    d.text((MAP_X0 + MAP_W * tx, MAP_Y0 + MAP_H * ty), word, font=mlab,
           fill=(150, 140, 115), anchor="mm")
for num, lon, lat, (dx, dy) in PINS:
    cx, cy = mpx(lon, lat)
    if num in LEADER_PINS:
        # true position: small dot + leader line to the offset number
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
        d.line([cx, cy, cx + dx, cy + dy], fill=RED, width=1)
    cx, cy = cx + dx, cy + dy
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=F(BOLD, 8), fill=(255, 255, 255),
           anchor="mm")
d.text((M, 929), "Pins mark stories 1\u201313. No. 9 is a world market; "
       "No. 13 is in space: Mercury.", font=F(REG, 9), fill=GREY)

BRIEFS = [
    ("14", "Basra: power-station fire kills 4, 35 hurt (Reuters)"),
    ("15", "Gaza: drone strike kills 3 in food-aid van (Reuters)"),
    ("16", "Hormuz: Iran says it downed a US MQ-9 drone (IRIB)"),
    ("17", "Tehran: uranium stock stays in the country (Reuters)"),
    ("18", "Paris: 82,500 march over living costs (Reuters)"),
    ("19", "Taipei: curbs on short-selling after -17.5% week (FSC)"),
    ("20", "Washington: Trump vows 'tremendous' data-centre tax (WSJ)"),
    ("21", "Beijing: China tells Japan to 'correct' Taiwan words (MFA)"),
    ("22", "Canberra: Australia and China agree AI talks (ABC)"),
    ("23", "Kyiv: Zelensky \u2014 Crimea bridge 'will not stay' (NBC)"),
    ("24", "Warsaw: Rutte \u2014 NATO will defend 'every inch' (Reuters)"),
    ("25", "London: England beat All Blacks 37\u201312 (Reuters)"),
    ("26", "Bayelsa: at least 24 dead in boat capsize (NEMA)"),
    ("27", "E. India: rain alerts as Akvan moves inland (IMD)"),
    ("28", "Lahore: Rizwan, Masood out of Pakistan contracts (SuperSport)"),
    ("29", "Dublin: Ireland beat South Africa 20\u201317 (Reuters)"),
    ("30", "Vancouver: defence rests in youth climate case (AFP)"),
    ("31", "Pyongyang: Kim tours factories after Trump trip (KCNA)"),
    ("32", "Bangkok: six-point plan on arsenic in two rivers (Nation)"),
    ("33", "New Delhi: Pakistan minister joins SCO forum (Dawn)"),
    ("34", "Sejong: freight train derails, none hurt (Korea Herald)"),
    ("35", "Melbourne: Cummins keeps Australian captaincy (ABC)"),
]
assert len(BRIEFS) == 22, "briefs must be 22 (stories 14-35)"
brief_cols = [(475, 255), (740, 255)]
for i, (num, text) in enumerate(BRIEFS):
    col = 0 if i < 11 else 1
    row = i % 11
    bx, bw = brief_cols[col]
    by = 786 + row * 12
    d.text((bx, by), num, font=F(BOLD, 10), fill=RED)
    nw = d.textlength(num, font=F(BOLD, 10)) + 4
    f, px = fit_size(text, [(REG, 10), (REG, 9), (REG, 8)], bw - nw,
                     f"brief {num}")
    d.text((bx + nw, by + (10 - px) // 2), text, font=f, fill=INK)

# ---------------------------------------------------------------- DATE CHECK: 940-1024
DATE_CHECK = ("Left out as Friday 20 November's news: Poland missile \u00b7 "
              "Kyiv bridges hit \u00b7 Wall Street correction \u00b7 Akvan "
              "landfall \u00b7 UK\u2013EU deal signed \u00b7 Denmark expels "
              "Russian attach\u00e9 \u00b7 Jizan missiles (Fri eve). Older: "
              "ICJ Myanmar ruling (Thu 19 Nov) \u00b7 Shenzhen summit. "
              "Not yet: COP31 final text (Sun 06:00 GMT) \u00b7 Las Vegas GP "
              "race (Sun 04:00 UTC) \u00b7 Liverpool v Man Utd (Sun).")
assert len(DATE_CHECK) <= 380, f"DATE CHECK {len(DATE_CHECK)} chars > 380"
FOOTER = ("Every story happened, or was first reported, on Saturday "
          "21 November 2026 \u00b7 HOW WE CHECKED: CONFIRMED = 2+ outlets "
          "\u00b7 OFFICIAL = on the record \u00b7 REPORTED = one outlet "
          "\u00b7 CLAIM = one side's account")
d.rectangle([M, 940, W - M, 1024], fill=PANEL, outline=RED, width=2)
d.text((M + 12, 945), "DATE CHECK", font=F(BLACK, 12), fill=RED)
dc_lines = fit_lines(DATE_CHECK, F(REG, 12), CW - 24, 3, "DATE CHECK")
for i, ln in enumerate(dc_lines):
    d.text((M + 12, 961 + i * 14), ln, font=F(REG, 12), fill=INK)
d.line([M + 12, 1006, W - M - 12, 1006], fill=(200, 192, 172), width=1)
ff, _ = fit_size(FOOTER, [(BOLD, 10), (REG, 9), (REG, 8)], CW - 24,
                 "DATE CHECK footer")
d.text((M + 12, 1010), FOOTER, font=ff, fill=GREY)

# ---------------------------------------------------------------- save + self-checks
img.save("entry.png", optimize=True)
import os
n_bytes = os.path.getsize("entry.png")
digest = hashlib.sha256(open("entry.png", "rb").read()).hexdigest()
print(f"entry.png: {n_bytes} bytes, 1024x1024, sha256 {digest}")
print(f"DATE CHECK: {len(DATE_CHECK)} chars, {len(dc_lines)} lines")
print(f"regions sum: {sum(c for _, c, _ in REGIONS)} (35 stories: "
      f"3 leads + 10 mediums + 22 briefs)")
print("zones: 100+34+84+32+270+250+170+84 = "
      f"{100+34+84+32+270+250+170+84}")
assert n_bytes <= 1024 * 1024, "entry.png over the 1 MiB limit"
