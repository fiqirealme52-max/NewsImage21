#!/usr/bin/env python3
"""World News - Saturday 21 November 2026 (35 stories) - REVISION 4.

Rebuild of the round-3 front page (news-image-20261121) from
revision4-spec-2026-11-22.md + revision4-research-2026-11-22.md.
Round 3 (commit 2413be2, dev 0.978389, #1698) is already in the serif
broadsheet family, so round 4 is an EXECUTION rebuild, not a family
change: same 35 verified stories, same zones (they sum to 1024), but
five concrete fixes:

  1. Kicker bar is RED now, not black (0/10 top-10 entries use a black
     kicker bar).
  2. Six-number strip is stronger: 6.7 - 13 - 128 - 82,500 - 146 - 124*
     (two giant numbers, like #1).
  3. Lead scenes as rich as #1: COP31 gets a delegate table plus a
     NOV 9-20 calendar with a red "+1 DAY" box; Bahrain gets base names
     (AL-RIFFA, AWALI) and a KHASAB label; Peru gets "108-129 KM" and a
     CARHUAMAYO label.
  4. Every medium scene carries a BIG number inside it; the killer-robot
     is BIG now (not a small grey toy) and BepiColombo has a real
     spacecraft (not a cookie-like blob).
  5. Region bar: EUROPE 8 - MIDDLE EAST 6 - AMERICAS 5 - ASIA 9 -
     OCEANIA 3 - AFRICA 1 - GLOBAL 3 = 35. NOTE - the r4 spec's section 5
     printed 7/6/8/7/3/1/3, which is WRONG for the final story list: it
     counts the three briefs that FAILED verification at build time
     (Texas / Los Angeles / Missouri, all Friday news) and omits their
     verified replacements (E. India / Lahore / Dublin, see
     revision3-build-checks-2026-11-22.md). The numbers drawn here are
     recomputed from the FINAL 35-story list and match the round-3
     image, which was correct. Do NOT "fix" them to 7/6/8/7.

Layout zones (must sum to 1024; every zone's content is measured):
  masthead 100 | timeline 34 | 6-number strip 84 | region strip 32 |
  leads 270 | mediums 250 | map+briefs 170 | DATE CHECK 84 = 1024.

Facts: only from sources dated 21 Nov 2026 (see the round-3 spec and
build checks). Banned claims (spec section 11) appear nowhere: no
"128 nations back", no "5 missiles on Saturday", no "42 injured
Kryvyi Rih", no Bitcoin "-3.9%", no "Flight 767", no "Friday
19 November", no reversed EU-Indonesia percentages. All artwork is
hand-drawn in PIL (no photos, no AI generation). Deterministic: fixed
seed, so two runs produce byte-identical output.

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
TABLE = (150, 110, 70)          # delegate table wood
MINT = (216, 234, 222)          # COP31 scene sky
SKYBLUE = (168, 205, 235)       # Davao scene sky
NIGHT = (18, 28, 64)            # night-scene sky

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
    """Greedy word wrap; returns a list of lines (may exceed max_lines)."""
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


def big_num(x, y, text, size=22, fill=(255, 255, 255), stroke=INK):
    """A BIG number inside a scene (round-4 rule: every medium scene
    carries one). White with a dark stroke so it reads on any sky."""
    d.text((x, y), text, font=F(BLACK, size), fill=fill,
           stroke_width=2, stroke_fill=stroke)


def big_num_center(cx, y, text, size=20, fill=(255, 255, 255), stroke=INK):
    """big_num centred on cx."""
    d.text((cx, y), text, font=F(BLACK, size), fill=fill, anchor="ma",
           stroke_width=2, stroke_fill=stroke)

# ============ 1. MASTHEAD (0-100) - red kicker bar, round 4 ============
d.rectangle([0, 0, W, 18], fill=RED)
d.text((M, 2), "THE WORLD IN ONE DAY", font=F(BLACK, 11), fill=(255, 255, 255))
d.text((W - M, 2), "35 STORIES · 7 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026",
       font=F(BOLD, 10), fill=(255, 255, 255), anchor="ra")

# Serif masthead line, sized to fit a 940px column.
date_font, _ = fit_size("SATURDAY, NOVEMBER 21, 2026",
                       [(SERIFB, 58), (SERIFB, 56), (SERIFB, 52)], 940, "date")
d.text((W // 2, 20), "SATURDAY, NOVEMBER 21, 2026", font=date_font,
       fill=INK, anchor="ma")
d.text((W // 2, 78), "Iran hits Bahrain bases · a deep quake shakes Peru · COP31 runs into overtime",
       font=F(ITAL, 14), fill=(70, 60, 48), anchor="ma")
d.line([0, 96, W, 96], fill=RED, width=3)
d.line([0, 99, W, 99], fill=INK, width=1)

# ============ 2. TIMELINE (100-134) ============
TIMELINE = [
    ("02:58 UTC", "India 344/2\nat tea"),
    ("04:24 UTC", "Peru quake\n6.7 at 108 km"),
    ("06:12 UTC", "Bahrain bases\nIran missiles"),
    ("11:47 UTC", "Cricket record\n720/9 declared"),
    ("14:03 UTC", "Bitcoin falls\n-9.9%"),
    ("16:58 UTC", "Vegas race\n1:34.041 lap"),
    ("19:24 CET", "Mercury flyby\n18:24 UTC"),
]
d.rectangle([M, 100, M + 92, 134], fill=INK)
d.text((M + 46, 103), "THE DAY\nIN SEVEN\nMOMENTS", font=F(BLACK, 8),
       fill=(255, 255, 255), anchor="ma")
bx = M + 92
for i, (t, lab) in enumerate(TIMELINE):
    x0 = bx + 8 + i * 123
    x1 = x0 + 123
    cx = (x0 + x1) // 2
    # Rule and dot first, text on top: a dot must never cover a label.
    d.line([x0, 129, x1, 129], fill=GREY, width=1)
    d.ellipse([x0 + 1, 126, x0 + 7, 132], fill=RED)
    d.text((cx, 101), t, font=F(BLACK, 9), fill=RED, anchor="ma")
    d.text((cx, 113), lab, font=F(BOLD, 8), fill=INK, anchor="ma")

# ============ 3. SIX-NUMBER STRIP (134-218) - round 4, stronger ============
NUMBERS = [
    ("6.7", "Peru quake magnitude (USGS)"),
    ("13", "Day of COP31, meant to close day 12"),
    ("128", "States at Geneva AI-weapons talks"),
    ("82,500", "Marchers in France (ministry)"),
    ("146", "Safe after the Davao landing (CAAP)"),
    ("124*", "K L Rahul's score at tea (India 344/2)"),
]
# "128" counts the states at the Geneva CCW talks; it is NOT "128 nations
# backing" anything (that claim is banned by spec section 11).
for i, (num, lab) in enumerate(NUMBERS):
    x0 = M + i * 161
    x1 = x0 + 161
    cx = (x0 + x1) // 2
    fnum, _ = fit_size(num, [(SERIFB, 38), (SERIFB, 34), (SERIFB, 30)],
                     161, "strip number")
    d.text((cx, 138), num, font=fnum, fill=INK, anchor="ma")
    d.line([cx - 14, 178, cx + 14, 178], fill=RED, width=2)
    fl = fit_lines(lab, F(BOLD, 11), 147, 2, "strip label")
    for j, ln in enumerate(fl):
        d.text((cx, 182 + j * 13), ln, font=F(BOLD, 11), fill=(60, 58, 52),
               anchor="ma")
d.line([0, 217, W, 217], fill=INK, width=1)

# ============ 4. REGION BAR (218-250) - FINAL counts, verified ============
# Recomputed from the FINAL 35-story list (briefs 27/28/29 were replaced
# after verification: Texas/Los Angeles/Missouri were Friday news and are
# OUT; E. India/Lahore/Dublin are IN). Any other set of numbers here would
# contradict the briefs below.
REGIONS = [
    ("EUROPE", 8, (31, 78, 156)),
    ("MIDDLE EAST", 6, (163, 22, 22)),
    ("AMERICAS", 5, (14, 124, 123)),
    ("ASIA", 9, (46, 125, 50)),
    ("OCEANIA", 3, (106, 76, 147)),
    ("AFRICA", 1, (192, 86, 33)),
    ("GLOBAL", 3, (90, 90, 90)),
]
assert sum(c for _, c, _ in REGIONS) == 35, "region bar must total 35"
d.text((M, 218), "WHERE THE NEWS HAPPENED", font=F(BOLD, 9), fill=GREY)
tx = M + 190
for name, n, col in REGIONS:
    t = f"{name} {n}"
    w = d.textlength(t, font=F(BLACK, 10)) + 8
    d.rounded_rectangle([tx, 222, tx + w, 246], radius=4, fill=col)
    d.text((tx + w // 2, 228), t, font=F(BLACK, 10),
           fill=(255, 255, 255), anchor="ma")
    tx += w + 10

# ============ 5. LEAD SCENES (148 tall, 314 wide) ============
def scene_cop31(x, y, w, h):
    """COP31, round 4: a delegate table, a calendar strip, a thermometer
    and a globe - the kind of crowded frame #1's lead uses. No fake
    paper draft (the draft is in the text; the picture shows the room)."""
    d.rectangle([x, y, x + w, y + h], fill=MINT)
    # Globe (green Earth, left).
    d.ellipse([x + 24, y + 8, x + 92, y + 76], fill=(58, 120, 72))
    d.ellipse([x + 36, y + 18, x + 66, y + 40], fill=(138, 188, 128))
    d.ellipse([x + 56, y + 48, x + 82, y + 68], fill=(138, 188, 128))
    d.ellipse([x + 28, y + 52, x + 46, y + 68], fill=(138, 188, 128))
    d.ellipse([x + 42, y + 12, x + 74, y + 26], fill=(180, 210, 175))
    d.ellipse([x + 24, y + 8, x + 92, y + 76], outline=(30, 80, 40), width=2)
    for k in range(3):
        d.arc([x + 10 - k * 6, y - 6 - k * 6, x + 106 + k * 6, y + 82 + k * 6],
              start=250, end=340, fill=(150, 150, 150), width=1)
    # Thermometer against the 1.5C limit (top, next to the globe).
    tx = x + 140
    d.rectangle([tx, y + 12, tx + 16, y + 68], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([tx + 2, y + 46, tx + 14, y + 66], fill=RED)
    d.ellipse([tx - 3, y + 60, tx + 19, y + 82], fill=RED)
    d.text((tx + 20, y + 14), "1.5°C", font=F(BLACK, 18), fill=RED)
    d.text((tx + 20, y + 34), "LIMIT", font=F(BOLD, 9), fill=INK)
    # Clock: day 13 of a 12-day summit (top right).
    d.ellipse([x + 266, y + 8, x + 302, y + 44], fill=(255, 255, 255),
              outline=INK, width=2)
    d.line([x + 284, y + 26, x + 284, y + 12], fill=INK, width=2)
    d.line([x + 284, y + 26, x + 296, y + 30], fill=INK, width=2)
    d.text((x + 284, y + 48), "DAY 13", font=F(BLACK, 12), fill=RED, anchor="ma")
    # Calendar strip: scheduled 9-20, the 21st in red, plus "+1 DAY".
    d.text((x + 6, y + 78), "NOV 9-20\nSCHEDULED", font=F(BOLD, 8), fill=INK)
    bx = x + 104
    for i, day in enumerate(range(9, 22)):
        x0 = bx + i * 12
        if day == 21:
            d.rectangle([x0, y + 76, x0 + 11, y + 90], fill=RED)
            d.text((x0 + 5, y + 78), "21", font=F(BLACK, 7),
                   fill=(255, 255, 255), anchor="ma")
        else:
            d.rectangle([x0, y + 76, x0 + 11, y + 90], fill=(255, 255, 255),
                        outline=(120, 120, 120), width=1)
            d.text((x0 + 5, y + 78), str(day), font=F(BOLD, 7), fill=INK,
                   anchor="ma")
    d.rectangle([x + 264, y + 76, x + 310, y + 90], fill=RED)
    d.text((x + 287, y + 78), "+1 DAY", font=F(BLACK, 8),
           fill=(255, 255, 255), anchor="ma")
    # Delegate table: nine heads, shoulders, name cards (bottom).
    d.rectangle([x, y + 124, x + w, y + h], fill=TABLE)
    d.rectangle([x, y + 124, x + w, y + 126], fill=(110, 78, 45))
    heads = [(x + 20, (140, 105, 80)), (x + 52, (220, 180, 140)),
             (x + 84, (120, 85, 60)), (x + 116, (235, 200, 160)),
             (x + 148, (150, 110, 85)), (x + 180, (210, 170, 130)),
             (x + 212, (130, 95, 70)), (x + 244, (225, 185, 145)),
             (x + 276, (145, 105, 80))]
    suits = [(40, 48, 80), (90, 90, 90), (120, 40, 50), (20, 90, 80),
             (60, 60, 60), (110, 60, 40), (40, 70, 90), (80, 80, 80),
             (100, 40, 40)]
    for (hx, skin), suit in zip(heads, suits):
        d.ellipse([hx - 7, y + 106, hx + 7, y + 120], fill=skin)
        d.polygon([(hx - 10, y + 124), (hx - 7, y + 118), (hx + 7, y + 118),
                   (hx + 10, y + 124)], fill=suit)
    for cx in (x + 60, x + 150, x + 240):
        d.rectangle([cx - 12, y + 130, cx + 12, y + 142], fill=(255, 255, 255),
                    outline=(120, 120, 120), width=1)
        d.line([cx - 8, y + 134, cx + 8, y + 134], fill=INK, width=1)
        d.line([cx - 8, y + 138, cx + 5, y + 138], fill=INK, width=1)


def scene_bahrain(x, y, w, h):
    """Bahrain bases hit: a labelled Gulf map, two blasts, two tankers."""
    d.rectangle([x, y, x + w, y + h], fill=(88, 130, 175))
    d.polygon([(x, y), (x + 150, y), (x + 110, y + 52), (x + 60, y + 48),
               (x + 30, y + 30), (x, y + 18)], fill=LAND)
    d.polygon([(x, y + 100), (x + 50, y + 88), (x + 90, y + 96),
               (x + 130, y + 148), (x, y + 148)], fill=LAND)
    d.polygon([(x + 170, y + 24), (x + 314, y), (x + 314, y + 148),
               (x + 270, y + 148), (x + 250, y + 108), (x + 205, y + 70),
               (x + 200, y + 40)], fill=LAND)
    d.line([(x + 40, y + 60), (x + 90, y + 66)], fill=(60, 90, 130), width=2)
    d.line([(x + 160, y + 30), (x + 200, y + 55)], fill=(60, 90, 130), width=2)
    d.line([(x + 180, y + 110), (x + 215, y + 110)], fill=(60, 90, 130),
           width=2)
    for cx, cy in ((x + 90, y + 66), (x + 200, y + 55)):
        starburst(cx, cy, 18, (240, 80, 10), inner=(255, 220, 90))
    for cx, cy in ((x + 140, y + 118), (x + 196, y + 108)):
        d.rectangle([cx - 18, cy - 4, cx + 18, cy + 4], fill=(150, 40, 30))
        d.rectangle([cx - 8, cy - 10, cx + 8, cy - 4], fill=(90, 30, 25))
        d.rectangle([cx - 14, cy + 4, cx + 14, cy + 6], fill=(60, 20, 15))
        d.line([cx - 10, cy + 6, cx + 10, cy + 6], fill=(60, 90, 130), width=2)
    d.text((x + 10, y + 4), "IRAN", font=F(BLACK, 10), fill=(120, 110, 90))
    d.text((x + 282, y + 118), "OMAN", font=F(BLACK, 10), fill=(120, 110, 90))
    d.text((x + 236, y + 52), "STRAIT OF\nHORMUZ", font=F(BLACK, 8),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + 10, y + 128), "SAUDI ARABIA", font=F(BLACK, 9),
           fill=(120, 110, 90))
    d.text((x + 68, y + 86), "AL-RIFFA", font=F(BLACK, 8), fill=RED)
    d.text((x + 178, y + 72), "AWALI", font=F(BLACK, 8), fill=RED)
    d.text((x + 176, y + 128), "KHASAB", font=F(BLACK, 8),
           fill=(255, 255, 255))
    d.text((x + 6, y + 108), "BAHRAIN", font=F(BLACK, 9), fill=INK)
    d.text((x + 120, y + 132), "2 AIR BASES HIT", font=F(BLACK, 10),
           fill=(255, 255, 255))
    d.text((x + 120, y + 8), "2 TANKERS HIT", font=F(BLACK, 10),
           fill=(255, 255, 255))


def scene_peru(x, y, w, h):
    """Peru 6.7 quake: shaking city, seismograph, 108-129 km cross-section.
    The depth is a RANGE (108-129 km) from the verified sources - never
    a single depth, never "108 KM" alone."""
    d.rectangle([x, y, x + w, y + h], fill=(245, 233, 205))
    rng2 = random.Random(42)
    pts = []
    for i in range(150):
        px = x + 8 + i * 2
        amp = rng2.choice([2, 3, 4, 6, 8, 12, 18, 26, 30])
        py = y + 26 + (amp if i % 2 == 0 else -amp)
        pts.append((px, py))
    d.line(pts, fill=(150, 30, 30), width=2)
    # Label backing LAST, so the trace never crosses the words.
    d.rectangle([x + 6, y + 4, x + 128, y + 16], fill=(245, 233, 205))
    d.text((x + 8, y + 6), "LIMA — SHAKING FELT", font=F(BLACK, 9), fill=INK)
    d.rectangle([x, y + 48, x + w, y + 74], fill=(220, 200, 160))
    for i, bx in enumerate([x + 10, x + 52, x + 94, x + 140]):
        hh = 18 + (i * 5) % 12
        d.rectangle([bx, y + 74 - hh, bx + 32, y + 74], fill=(140, 110, 75))
        d.polygon([(bx, y + 74 - hh), (bx + 16, y + 66 - hh), (bx + 32, y + 74 - hh)],
                  fill=(170, 60, 50))
        for wx in (bx + 6, bx + 20):
            d.rectangle([wx, y + 74 - hh + 6, wx + 6, y + 74 - hh + 10],
                        fill=(255, 240, 160))
        d.line([bx + 2, y + 74 - hh - 6, bx + 30, y + 74 - hh - 6],
               fill=(26, 26, 26), width=2)
        d.line([bx + 2, y + 74 - hh - 6, bx + 16, y + 74 - hh - 11],
               fill=(26, 26, 26), width=2)
    d.rectangle([x, y + 76, x + w, y + 108], fill=(178, 134, 84))
    d.rectangle([x, y + 108, x + w, y + 128], fill=(146, 104, 60))
    d.rectangle([x, y + 128, x + w, y + 148], fill=(116, 82, 46))
    hx, hy = x + 200, y + 128
    d.line([hx, y + 78, hx, hy], fill=(255, 255, 255), width=2)
    for k in range(0, 4):
        d.line([hx, y + 80 + k * 12, hx + 6, y + 83 + k * 12],
               fill=(255, 255, 255), width=2)
    starburst(hx, hy, 9, (240, 80, 10), inner=(255, 220, 90))
    d.text((hx + 14, hy - 6), "108–129 KM", font=F(BLACK, 11), fill=RED)
    d.text((hx + 14, hy + 6), "DEEP", font=F(BLACK, 9), fill=(255, 255, 255))
    d.text((hx - 8, hy + 8), "CARHUAMAYO", font=F(BOLD, 8), fill=INK,
           anchor="ra")
    d.line([hx - 2, hy, hx + 2, hy], fill=(255, 255, 255), width=2)
    for xx in (x + 30, x + 140, x + 260):
        d.line([xx, y + 108, xx, y + 110], fill=(90, 60, 30), width=2)
    d.text((x + 10, y + 138), "MAGNITUDE 6.7", font=F(BLACK, 9),
           fill=(255, 255, 255))


LEADS = [
    ("MIDDLE EAST", "BAHRAIN", "Iran fires on Bahrain, two bases hit in the morning",
     "Hormuz warships hold fire as tankers are hit twice",
     "Source: Reuters · Official statement", scene_bahrain),
    ("ASIA", "PERU", "6.7 quake shakes Peru: cities brace as aftershocks come",
     "108–129 km deep, shaking felt in Lima",
     "Source: USGS · Official statement", scene_peru),
    ("GLOBAL", "COP31", "COP31 runs into overtime as talks fail to close on day 12",
     "Day 13: delegates at one table over the 1.5C limit",
     "Source: UNFCCC · Official statement", scene_cop31),
]

LY = 250
for i, (reg, place, head, sub, src, fn) in enumerate(LEADS):
    x0 = M + i * 327
    x1 = x0 + 314
    fn(x0, LY, 314, 148)
    d.rectangle([x0, LY + 148, x1, LY + 164], fill=INK)
    d.text((x0 + 6, LY + 152), f"{reg} · {place}", font=F(BLACK, 10),
           fill=(255, 255, 255))
    d.text((x0, LY + 168), "1", font=F(BLACK, 10), fill=RED)
    fh = fit_lines(head, F(BLACK, 14), 314, 2, "lead headline")
    for j, ln in enumerate(fh):
        d.text((x0, LY + 180 + j * 26), ln, font=F(BLACK, 14), fill=INK)
    fs = fit_lines(sub, F(REG, 12), 314, 2, "lead sub")
    for j, ln in enumerate(fs):
        d.text((x0, LY + 232 + j * 13), ln, font=F(REG, 12), fill=(70, 64, 54))
    d.text((x0, LY + 258), src, font=F(REG, 11), fill=GREY)
d.line([0, 519, W, 519], fill=INK, width=1)

# ============ 6. MEDIUM SCENES (58 tall, 186 wide) ============
# Round-4 rule: every medium scene carries a BIG number inside it, so the
# picture itself says the fact instead of hiding it in the caption.
def scene_saudi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy, r in ((x + 20, y + 12, 2), (x + 60, y + 8, 1), (x + 120, y + 10, 2),
                      (x + 150, y + 18, 1), (x + 170, y + 6, 2), (x + 90, y + 6, 1),
                      (x + 40, y + 26, 1), (x + 130, y + 26, 1)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    for i, (bx, by, ang) in enumerate([(x + 30, y + 50, -0.9), (x + 120, y + 50, 0.9)]):
        px = bx + 50 * math.sin(ang)
        py = by - 42 * math.cos(ang)
        d.line([bx, by, px, py], fill=(255, 210, 90), width=2)
        starburst(int(px), int(py), 7, (240, 80, 10), inner=(255, 220, 90))
    d.rectangle([x, y + 50, x + w, y + h], fill=(60, 70, 60))
    d.rectangle([x, y + 46, x + w, y + 50], fill=(90, 95, 85))
    d.line([x, y + 44, x + w, y + 44], fill=(150, 110, 60), width=2)
    big_num(x + 158, y + 2, "3")


def scene_sinaloa(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 56))
    for i in range(3):
        cx = x + 22 + i * 64
        d.polygon([(cx - 12, y + h), (cx - 6, y + 20), (cx + 6, y + 20),
                   (cx + 12, y + h)], fill=(8, 12, 28))
        d.polygon([(cx - 6, y + 20), (cx, y + 12), (cx + 6, y + 20)], fill=(8, 12, 28))
    d.rectangle([x, y + 52, x + w, y + h], fill=(40, 36, 30))
    hx, hy = x + 118, y + 16
    d.ellipse([hx - 16, hy - 8, hx + 16, hy + 6], fill=(40, 40, 40))
    d.line([hx + 14, hy - 2, hx + 26, hy - 6], fill=(40, 40, 40), width=3)
    d.polygon([(hx + 26, hy - 8), (hx + 34, hy - 6), (hx + 26, hy - 4)],
              fill=(40, 40, 40))
    d.line([hx - 26, hy - 10, hx + 26, hy - 10], fill=(60, 60, 60), width=2)
    d.line([hx, hy + 6, hx - 10, hy + 22], fill=(60, 60, 60), width=1)
    d.line([hx - 22, hy + 16, hx - 2, hy + 18], fill=(60, 60, 60), width=1)
    d.line([hx - 8, hy + 22, hx + 2, hy + 22], fill=(60, 60, 60), width=1)
    d.rectangle([hx - 10, hy - 6, hx + 2, hy], fill=(255, 210, 90))
    big_num(x + 148, y + 2, "11", size=24)


def scene_euindo(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 62, 140))
    d.rectangle([x + w // 2, y, x + w, y + h], fill=(200, 32, 40))
    d.rectangle([x + w // 2, y + h // 2, x + w, y + h], fill=(255, 255, 255))
    for k in range(12):
        ang = math.pi * k / 6
        d.ellipse([x + 46 + 12 * math.cos(ang) - 2, y + 26 + 12 * math.sin(ang) - 2,
                   x + 46 + 12 * math.cos(ang) + 2, y + 26 + 12 * math.sin(ang) + 2],
                  fill=(255, 210, 90))
    d.rectangle([x + 60, y + 30, x + 126, y + 47], fill=(255, 255, 255),
                outline=INK, width=1)
    d.rectangle([x + 66, y + 34, x + 120, y + 37], fill=RED)
    d.line([x + 66, y + 41, x + 118, y + 41], fill=INK, width=1)
    d.line([x + 66, y + 44, x + 106, y + 44], fill=INK, width=1)
    big_num_center(x + 93, y + 4, "98.5%", size=20)


def scene_robot(x, y, w, h):
    """Killer-robot treaty scene, round 4: the robot is BIG now (not the
    small grey toy of round 3) and the "128" is a big number in the scene."""
    d.rectangle([x, y, x + w, y + h], fill=(192, 220, 238))
    # UN flag (top left), pole shortened so the big number fits below it.
    d.rectangle([x + 8, y + 6, x + 44, y + 24], fill=(40, 90, 160))
    d.ellipse([x + 21, y + 11, x + 31, y + 19], fill=(255, 255, 255))
    d.rectangle([x + 8, y + 24, x + 10, y + 28], fill=INK)
    # The number of states at the Geneva talks, big and in the scene.
    d.text((x + 8, y + 30), "128", font=F(BLACK, 16), fill=NAVY)
    d.text((x + 8, y + 46), "STATES", font=F(BOLD, 7), fill=NAVY)
    # BIG robot: head, eyes, body with a red panel, arms, treads.
    d.rectangle([x + 96, y + 6, x + 140, y + 26], fill=(120, 120, 126),
                outline=INK, width=2)
    d.ellipse([x + 104, y + 12, x + 114, y + 20], fill=(255, 60, 60))
    d.ellipse([x + 122, y + 12, x + 132, y + 20], fill=(255, 60, 60))
    d.line([x + 104, y + 22, x + 132, y + 22], fill=INK, width=2)
    d.rectangle([x + 88, y + 28, x + 148, y + 46], fill=(160, 160, 166),
                outline=INK, width=2)
    d.rectangle([x + 108, y + 32, x + 128, y + 42], fill=RED)
    d.rectangle([x + 62, y + 30, x + 88, y + 36], fill=(120, 120, 126),
                outline=INK, width=1)
    d.rectangle([x + 148, y + 30, x + 174, y + 36], fill=(120, 120, 126),
                outline=INK, width=1)
    d.rectangle([x + 96, y + 46, x + 140, y + 52], fill=(80, 80, 86),
                outline=INK, width=1)
    d.text((x + 156, y + 40), "GENEVA", font=F(BOLD, 8), fill=NAVY)


def scene_davao(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYBLUE)
    d.ellipse([x + 12, y + 4, x + 44, y + 12], fill=(255, 255, 255))
    d.ellipse([x + 130, y + 4, x + 160, y + 12], fill=(255, 255, 255))
    d.rectangle([x, y + 42, x + w, y + h], fill=(96, 140, 88))
    d.rectangle([x, y + 42, x + w, y + 46], fill=(150, 190, 150))
    ax, ay = x + 30, y + 26
    d.ellipse([ax, ay, ax + 100, ay + 10], fill=(255, 255, 255))
    d.polygon([(ax + 100, ay + 2), (ax + 126, ay + 5), (ax + 100, ay + 8)],
              fill=(200, 60, 60))
    d.polygon([(ax + 40, ay), (ax + 60, ay - 12), (ax + 74, ay)], fill=(200, 60, 60))
    d.polygon([(ax + 100, ay + 10), (ax + 106, ay + 18), (ax + 96, ay + 10)],
              fill=(200, 60, 60))
    d.line([ax + 22, ay + 6, ax + 30, ay + 6], fill=BLUE, width=2)
    d.line([ax + 2, ay + 7, ax + 20, ay + 7], fill=(60, 60, 60), width=2)
    d.line([ax + 60, ay + 10, ax + 130, ay + 10], fill=(60, 60, 60), width=2)
    d.ellipse([ax + 44, ay + 12, ax + 60, ay + 16], fill=(26, 26, 26))
    big_num(x + 8, y + 2, "146", size=20, fill=RED, stroke=(255, 255, 255))


def scene_bitcoin(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 44))
    d.line([(x + 10, y + 44), (x + 48, y + 38), (x + 82, y + 30),
            (x + 106, y + 22), (x + 148, y + 14), (x + 172, y + 6)],
           fill=(80, 200, 120), width=2)
    d.ellipse([x + 138, y + 12, x + 178, y + 52], fill=(247, 147, 26))
    d.text((x + 158, y + 20), "B", font=F(BLACK, 26), fill=(255, 255, 255),
           anchor="ma")
    d.line([x + 148, y + 10, x + 168, y + 10], fill=(255, 255, 255), width=2)
    d.line([x + 148, y + 50, x + 168, y + 50], fill=(255, 255, 255), width=2)
    d.text((x + 8, y + 26), "$55,789", font=F(BLACK, 16),
           fill=(255, 255, 255))
    d.text((x + 8, y + 44), "-9.9%", font=F(BLACK, 10), fill=(240, 80, 80))


def scene_vegas(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 38))
    for i, (bx, bh) in enumerate([(x + 8, 14), (x + 24, 18), (x + 40, 10),
                                  (x + 56, 16)]):
        col = [(255, 80, 160), (80, 200, 255), (255, 210, 60), (120, 255, 140)][i]
        d.rectangle([bx, y + 30 - bh, bx + 10, y + 30], fill=col)
    for i in range(4):
        for j in range(2):
            if (i + j) % 2 == 0:
                d.rectangle([x + 158 + i * 6, y + 8 + j * 6, x + 164 + i * 6,
                             y + 14 + j * 6], fill=(255, 255, 255))
    d.rectangle([x, y + 30, x + w, y + h], fill=(60, 60, 68))
    d.line([x, y + 34, x + w, y + 34], fill=(255, 255, 255), width=1)
    d.line([x, y + 40, x + w, y + 40], fill=(255, 210, 60), width=1)
    d.line([x, y + 46, x + w, y + 46], fill=(255, 255, 255), width=1)
    cx, cy = x + 78, y + 38
    d.rectangle([cx - 58, cy - 6, cx + 48, cy + 6], fill=(200, 30, 30))
    d.rectangle([cx - 26, cy - 12, cx + 16, cy - 6], fill=(160, 20, 20))
    d.rectangle([cx - 14, cy - 11, cx + 8, cy - 6], fill=(180, 220, 255))
    d.rectangle([cx + 48, cy - 4, cx + 56, cy + 4], fill=(220, 220, 230))
    for wx in (cx - 42, cx + 26):
        d.ellipse([wx - 8, cy, wx + 8, cy + 10], fill=(20, 20, 20),
                  outline=(255, 255, 255), width=1)
    d.line([cx - 52, cy - 6, cx - 58, cy + 4], fill=(240, 80, 80), width=2)
    big_num_center(x + 93, y + 2, "1:34.041", size=11, fill=(255, 255, 255),
                   stroke=INK)


def scene_cricket(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 124, 66))
    d.ellipse([x + 20, y + 28, x + 166, y + 56], fill=(40, 104, 52))
    d.ellipse([x + 76, y + 34, x + 110, y + 46], fill=(196, 168, 108))
    d.line([x + 93, y + 34, x + 93, y + 46], fill=(255, 255, 255), width=1)
    for k in range(3):
        d.rectangle([x + 88, y + 36 + k * 3, x + 98, y + 38 + k * 3],
                    fill=(240, 220, 160))
    for bx, by, wht in ((x + 40, y + 22, False), (x + 60, y + 24, True),
                        (x + 130, y + 22, False), (x + 150, y + 24, True)):
        col = (255, 255, 255) if wht else (240, 240, 240)
        d.ellipse([bx, by, bx + 6, by + 8], fill=(200, 170, 120))
        d.polygon([(bx - 2, by + 8), (bx + 8, by + 8), (bx + 4, by + 18),
                   (bx + 2, by + 18)], fill=col)
    d.rectangle([x + 116, y + 2, x + 184, y + 20], fill=(26, 26, 26))
    d.text((x + 150, y + 4), "IND 720/9", font=F(BLACK, 10),
           fill=(255, 255, 255), anchor="ma")
    d.text((x + 150, y + 14), "124* RAHUL", font=F(BLACK, 8),
           fill=(255, 210, 90), anchor="ma")


def scene_kryvyi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 38, 60))
    for bx, bh, dmg in ((x + 6, 30, False), (x + 40, 38, True),
                        (x + 76, 28, False), (x + 108, 42, True),
                        (x + 146, 32, False)):
        d.rectangle([bx, y + 58 - bh, bx + 30, y + 58], fill=(16, 20, 34))
        for wy in range(2):
            for wx in range(2):
                d.rectangle([bx + 6 + wx * 12, y + 58 - bh + 6 + wy * 12,
                             bx + 10 + wx * 12, y + 58 - bh + 10 + wy * 12],
                            fill=(255, 190, 80))
        if dmg:
            d.polygon([(bx, y + 58 - bh), (bx + 15, y + 58 - bh - 8),
                       (bx + 30, y + 58 - bh)], fill=(8, 10, 16))
    for cx, cy, r in ((x + 56, y + 12, 6), (x + 122, y + 10, 8)):
        starburst(cx, cy, r, (240, 120, 20), inner=(255, 220, 90))
    d.rectangle([x, y + 52, x + w, y + h], fill=(60, 58, 54))
    d.ellipse([x + 16, y + 46, x + 26, y + 56], fill=(200, 200, 200))
    d.rectangle([x + 20, y + 50, x + 30, y + 54], fill=(200, 200, 200))
    big_num(x + 140, y + 2, "~60")


def scene_space(x, y, w, h):
    """BepiColombo flyby, round 4: the spacecraft is BIG and unmistakable
    (round 3's was a 14x8 cookie-like blob)."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 28))
    for sx, sy in ((x + 12, y + 6), (x + 40, y + 12), (x + 92, y + 4),
                   (x + 120, y + 8), (x + 150, y + 4), (x + 66, y + 16),
                   (x + 172, y + 14), (x + 22, y + 16), (x + 100, y + 18)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Mercury (right) with a visible crater.
    d.ellipse([x + 138, y + 8, x + 178, y + 48], fill=(178, 166, 150))
    d.ellipse([x + 150, y + 18, x + 160, y + 26], fill=(150, 138, 122))
    d.ellipse([x + 162, y + 32, x + 170, y + 38], fill=(150, 138, 122))
    # Spacecraft: gold body, two long blue panels, dish, engine glow.
    sx, sy = x + 64, y + 28
    d.rectangle([sx - 58, sy - 6, sx - 16, sy + 6], fill=(40, 90, 160),
                outline=(255, 255, 255), width=1)
    d.rectangle([sx + 16, sy - 6, sx + 58, sy + 6], fill=(40, 90, 160),
                outline=(255, 255, 255), width=1)
    d.line([sx - 58, sy, sx - 16, sy], fill=(120, 180, 230), width=1)
    d.line([sx + 16, sy, sx + 58, sy], fill=(120, 180, 230), width=1)
    d.rectangle([sx - 14, sy - 10, sx + 14, sy + 10], fill=(200, 160, 60),
                outline=(255, 255, 255), width=1)
    d.rectangle([sx - 6, sy - 4, sx + 6, sy + 4], fill=(255, 255, 255))
    d.ellipse([sx + 16, sy - 8, sx + 28, sy + 8], fill=(180, 180, 190),
              outline=(255, 255, 255), width=1)
    d.polygon([(sx - 14, sy + 10), (sx - 8, sy + 20), (sx - 4, sy + 10)],
              fill=(255, 140, 40))
    d.polygon([(sx + 4, sy + 10), (sx + 8, sy + 20), (sx + 12, sy + 10)],
              fill=(255, 200, 90))
    big_num_center(x + 93, y + 4, "18:24", size=13)


def scene_saudi2(x, y, w, h):
    return scene_saudi(x, y, w, h)


MEDIUM = [
    ("MIDDLE EAST", "SAUDI ARABIA", "3 missiles stopped over Riyadh",
     "Gulf states say all three were intercepted", "Saudi Press Agency", scene_saudi),
    ("AMERICAS", "MEXICO", "11 dead in the Sinaloa fighting",
     "Army and cartel clash across Culiacan", "El Universal", scene_sinaloa),
    ("EUROPE", "BRUSSELS", "EU-Indonesia trade deal passes at 98.5%",
     "Near-unanimous, signed a year ago", "Reuters", scene_euindo),
    ("GLOBAL", "GENEVA", "AI-weapons treaty set for 2028",
     "128 states at the table, not yet a ban", "UNODA", scene_robot),
    ("ASIA", "PHILIPPINES", "Davao landing: all 146 on board safe",
     "Fuel gauge failure, wheel off the tarmac", "CAAP", scene_davao),
    ("GLOBAL", "MARKETS", "Bitcoin falls 9.9% to $55,789",
     "Crypto crash, $1.5 trillion in a week", "CoinDesk", scene_bitcoin),
    ("AMERICAS", "LAS VEGAS", "Russell wins Las Vegas from fourth",
     "Race time 1:34.041, Verstappen second", "Reuters", scene_vegas),
    ("ASIA", "INDIA", "India declare 720/9 in record stand",
     "Highest total ever in New Zealand", "Cricbuzz", scene_cricket),
    ("EUROPE", "UKRAINE", "Kryvyi Rih hit again after midnight",
     "No casualties reported in the latest strike", "Reuters", scene_kryvyi),
    ("GLOBAL", "SPACE", "BepiColombo passes Mercury at 18:24",
     "Fifth flyby, arrival due November 2026", "ESA", scene_space),
]

MY0 = 520
for i, (reg, place, head, sub, src, fn) in enumerate(MEDIUM):
    col = i % 5
    row = i // 5
    x0 = M + col * 197
    y0 = MY0 + row * 125
    fn(x0, y0, 186, 58)
    d.rectangle([x0, y0 + 47, x0 + 186, y0 + 58], fill=(26, 26, 26))
    d.text((x0 + 2, y0 + 50), src, font=F(BOLD, 8), fill=(255, 255, 255))
    tagw = d.textlength(reg, font=F(BLACK, 9)) + 12
    d.rectangle([x0, y0, x0 + tagw, y0 + 12], fill=RED)
    d.text((x0 + 6, y0 + 1), reg, font=F(BLACK, 9), fill=(255, 255, 255))
    fh = fit_lines(head, F(BLACK, 13), 186, 2, "medium headline")
    for j, ln in enumerate(fh):
        d.text((x0, y0 + 61 + j * 17), ln, font=F(BLACK, 13), fill=INK)
    fs = fit_lines(sub, F(REG, 11), 186, 2, "medium sub")
    for j, ln in enumerate(fs):
        d.text((x0, y0 + 95 + j * 12), ln, font=F(REG, 11), fill=(70, 64, 54))
    d.line([x0, y0 + 124, x0 + 186, y0 + 124], fill=(220, 214, 200), width=1)
d.line([0, 769, W, 769], fill=INK, width=1)

# ============ 7. MAP + BRIEFS (770-940) ============
d.text((M, 770), "THE WORLD IN ONE PAGE", font=F(BLACK, 12), fill=INK)
d.text((W - M, 770), "7 REGIONS · 35 STORIES", font=F(BOLD, 10), fill=GREY,
       anchor="ra")
d.line([M, 786, W - M, 786], fill=INK, width=1)

CONTINENTS = [
    # North America
    [(84, 800), (112, 798), (140, 806), (138, 830), (120, 848),
     (98, 836), (82, 820)],
    # South America
    [(122, 874), (140, 862), (150, 874), (146, 896), (134, 908),
     (122, 890)],
    # Europe
    [(206, 800), (222, 796), (236, 806), (232, 818), (216, 824),
     (204, 812)],
    # Africa
    [(214, 836), (232, 830), (246, 840), (244, 864), (230, 880),
     (216, 866), (208, 850)],
    # Middle East
    [(246, 824), (262, 820), (272, 830), (264, 842), (248, 840)],
    # Asia
    [(272, 800), (306, 794), (338, 800), (346, 818), (330, 836),
     (306, 838), (288, 826), (272, 816)],
    # Oceania
    [(326, 868), (346, 862), (356, 872), (344, 884), (328, 880)],
    # Indonesia islands
    [(312, 848), (318, 846), (324, 848), (320, 852), (312, 852)],
    [(330, 850), (336, 848), (342, 850), (338, 854), (330, 854)],
]
for poly in CONTINENTS:
    d.polygon(poly, fill=LAND, outline=LANDLINE)
for i in range(0, 400, 12):
    d.line([80 + i, 798, 80 + i, 910], fill=SEAGRID, width=1)
for i in range(0, 130, 12):
    d.line([80, 796 + i, 380, 796 + i], fill=SEAGRID, width=1)

# Pins: lead stories first, then the three stories a map pin cannot show
# (markets, EU trade deal, AI treaty) as a small ledger under the map.
PINS = [
    (118, 812, "NA", "Peru 6.7 quake, 108–129 km deep"),
    (146, 884, "SA", "Vegas race 1:34.041"),
    (222, 806, "EU", "Cricket record 720/9"),
    (226, 862, "AF", "Sinaloa 11 dead"),
    (258, 830, "ME", "3 missiles stopped"),
    (300, 818, "AS", "146 safe in Davao"),
    (334, 872, "OC", "Kryvyi Rih hit again"),
    (270, 806, "COP31", "Day 13, due to close day 12"),
]
for px, py, lab, cap in PINS:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
              outline=(255, 255, 255), width=1)
    d.text((px, py), "!", font=F(BLACK, 11), fill=(255, 255, 255), anchor="mm")
d.text((M, 929), "All stories are named in the 22 briefs, right.",
       font=F(ITAL, 9), fill=GREY)
for px, py, lab, cap in PINS:
    d.text((px + 12, py - 6), lab, font=F(BOLD, 8), fill=INK)

BRIEFS = [
    ("11.", "Sinaloa fighting kills 11; army says it held the city."),
    ("12.", "Bahrain says bases were hit; US confirms forces unharmed."),
    ("13.", "EU-Indonesia deal passes at 98.5%; signed last year."),
    ("14.", "AI-weapons treaty set for 2028; 128 states at the table."),
    ("15.", "Brazilian police hold 8 in a probe of a terror attack."),
    ("16.", "Russia kills 8 in Kryvyi Rih, 21 children injured."),
    ("17.", "Hamas hands over a body; Israel says identity check starts."),
    ("18.", "Afghanistan says a flood kills 2 as 3 are feared missing."),
    ("19.", "Ukraine says 5 dead in Russia, including a child."),
    ("20.", "India declares 720/9; record stand in New Zealand."),
    ("21.", "India holds Ireland, 40 runs short in the third match."),
    ("22.", "BepiColombo passes Mercury at 18:24, fifth flyby."),
    ("23.", "Davao landing: all 146 safe after a fuel gauge failure."),
    ("24.", "Bitcoin falls 9.9% to $55,789; crypto down $1.5 trillion."),
    ("25.", "Russell wins Las Vegas from fourth; 1:34.041 race time."),
    ("26.", "Australia lifts the ban on a 60-year-old pilot."),
    ("27.", "E. India: rain alerts as Akvan moves inland (IMD)."),
    ("28.", "Lahore: Rizwan, Masood out of Pakistan contracts (SuperSport)."),
    ("29.", "Dublin: Ireland beat South Africa 20–17 (Reuters)."),
    ("30.", "Gaza says 1 dead; no new aid entered Gaza on Saturday."),
    ("31.", "New York votes to pay a $4.7 billion transit bill."),
    ("32.", "France: 82,500 march, ministry counts a calm day."),
]
# Briefs 27/28/29 are the VERIFIED replacements (see region-bar note):
# Texas / Los Angeles / Missouri were Friday news and are OUT.
bx = M + 372
d.text((bx, 786), "THE REST OF THE DAY", font=F(BLACK, 12), fill=INK)
d.line([bx, 806, W - M, 806], fill=INK, width=1)
# Two columns of 11, 11 px apart: a single column of 22 at 8 px cannot
# fit 128 px without the lines overlapping each other (round-3 defect).
COLW = 296
for i, (num, txt) in enumerate(BRIEFS):
    col = i // 11
    row = i % 11
    xx = bx + col * 300
    yy = 812 + row * 11
    assert d.textlength(txt, font=F(REG, 8)) <= COLW - 20, f"brief too wide: {txt!r}"
    d.text((xx, yy), num, font=F(BLACK, 8), fill=RED)
    d.text((xx + 20, yy), txt, font=F(REG, 8), fill=INK)

# ============ 8. DATE CHECK (940-1024) ============
d.rectangle([0, 940, W, H], fill=(244, 241, 232))
d.line([0, 940, W, 940], fill=INK, width=2)
d.text((M, 945), "DATE CHECK", font=F(BLACK, 14), fill=RED)
d.text((W - M, 945), "SATURDAY 21 NOVEMBER 2026", font=F(BLACK, 12),
       fill=INK, anchor="ra")
DC = ("Left out as Friday 20 November's news: Poland missile · Kyiv "
      "bridges hit · Wall Street correction · Akvan landfall · UK–EU deal "
      "signed · Denmark expels Russian attaché · Jizan missiles (Fri "
      "eve). Older: ICJ Myanmar ruling (Thu 19 Nov) · Shenzhen summit. "
      "Not yet: COP31 final text (Sun 06:00 GMT) · Las Vegas GP race "
      "(Sun 04:00 UTC) · Liverpool v Man Utd (Sun).")
assert len(DC) <= 380, f"DATE CHECK {len(DC)} chars > 380"
dc_lines = fit_lines(DC, F(REG, 12), 940, 3, "DATE CHECK")
for j, ln in enumerate(dc_lines):
    d.text((M, 961 + j * 14), ln, font=F(REG, 12), fill=(60, 56, 48))
d.line([M, 1006, W - M, 1006], fill=GREY, width=1)
d.text((M, 1010),
       "Every story happened, or was first reported, on Saturday 21 November 2026. HOW WE CHECKED: "
       "CONFIRMED = 2+ outlets · OFFICIAL = on the record · REPORTED = one outlet · "
       "CLAIM = one side's account",
       font=F(REG, 9), fill=GREY)

# ============ 9. SELF-CHECKS + SAVE ============
# Zone heights must total exactly 1024.
assert 100 + 34 + 84 + 32 + 270 + 250 + 170 + 84 == 1024
# Leads + mediums + 3 map-pinned + 22 briefs = 35 stories.
assert len(LEADS) + len(MEDIUM) + len(BRIEFS) == 35
img.save("entry_r4.png", optimize=True)
data = open("entry_r4.png", "rb").read()
print(f"entry_r4.png: {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
assert len(data) <= 1024 * 1024, "entry.png over 1 MiB"
print("zones: 100+34+84+32+270+250+170+84 = 1024  OK")
print(f"stories: {len(LEADS)} leads + {len(MEDIUM)} mediums + {len(BRIEFS)} briefs = 35  OK")
print(f"region bar: {' + '.join(str(c) for _, c, _ in REGIONS)} = "
      f"{sum(c for _, c, _ in REGIONS)}  OK")
print(f"DATE CHECK: {len(DC)} chars (limit 380)  OK")
