#!/usr/bin/env python3
"""Render the 22 November 2026 newspaper front page (entry.png, 1024x1024).

Draws the whole page in code with Pillow: masthead, numbers strip, region
bar, UTC timeline, three leads, twelve pictured cards, dotted world map,
also-on list, DATE CHECK box and sources footer. No network, no photos.
The page is rendered at 2048x2048 and downscaled to 1024x1024 for clean
edges. Same input always gives the same bytes.
"""
import os

from PIL import Image, ImageDraw, ImageFont

SCALE = 2
W = 1024 * SCALE
H = 1024 * SCALE
MARGIN = 48 * SCALE
CW = W - 2 * MARGIN  # content width

PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 30, 36)
NAVY = (31, 58, 95)
TEAL = (15, 107, 92)
AMBER = (196, 110, 0)
OLIVE = (90, 110, 40)
PURPLE = (90, 60, 120)
GREY = (90, 90, 90)
SKY = (168, 205, 225)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
_font_cache = {}


def _font(name, size):
    key = (name, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_DIR + name, size)
    return _font_cache[key]


def serif_b(size):
    return _font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return _font("DejaVuSerif.ttf", size)


def sans_b(size):
    return _font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return _font("DejaVuSans.ttf", size)


def wrap(text, font, max_width):
    """Greedy word wrap; returns the lines that fit inside max_width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def para(draw, x, y, text, font, fill, max_width, max_lines=None, line_h=None):
    """Draw a wrapped paragraph; returns the y below the last line."""
    if line_h is None:
        line_h = int(font.size * 1.28)
    lines = wrap(text, font, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += line_h
    return y


TAG_COLORS = {
    "CONFIRMED": (15, 107, 92),
    "CLAIM": (196, 110, 0),
    "REPORTED": (90, 90, 90),
    "FORECAST": (31, 58, 95),
}


def tag_chip(draw, x_right, y, label):
    """Small coloured certainty chip, right-aligned at x_right."""
    f = sans_b(17)
    tw = int(f.getlength(label)) + 16
    h = 26
    x0 = x_right - tw
    draw.rounded_rectangle([x0, y, x_right, y + h], radius=4,
                           fill=TAG_COLORS.get(label, (90, 90, 90)))
    draw.text((x0 + 8, y + 3), label, font=f, fill=(255, 255, 255))
    return tw


# ------------------------------------------------------------------ content
SUBHEAD = ("COP31 collapses with no deal  ·  186 drones over Ukraine  ·  "
           "Iran's radar claim meets Bahrain's denial")

NUMBERS = [
    ("186", "drones fired at Ukraine overnight"),
    ("161", "downed or suppressed by air defence"),
    ("35%", "electricity goal for 2035, kept"),
    ("720/9", "India's record Test total in NZ"),
    ("50", "Wembanyama points, 19 rebounds"),
    ("98.79%", "Hong Kong turnout, a record"),
    ("4–0", "Liverpool over United"),
]

REGIONS = [
    ("EUROPE", 8, NAVY), ("MIDDLE EAST", 5, RED), ("AMERICAS", 5, TEAL),
    ("ASIA-PACIFIC", 9, AMBER), ("AFRICA", 2, OLIVE), ("OCEANIA", 5, PURPLE),
    ("WORLD", 2, GREY),
]

TIMELINE = [
    ("01:00", "HK polls open"),
    ("04:00", "Las Vegas GP"),
    ("05:30", "Verstappen wins"),
    ("06:00", "COP31 plenary"),
    ("07:06", "M4.9 quake"),
    ("10:00", "HK polls close"),
    ("12:00", "Pope's lunch"),
    ("14:15", "HK count done"),
    ("16:30", "Liverpool kick-off"),
    ("18:28", "Liverpool 4–0"),
    ("18:45", "Alcaraz wins"),
    ("EVENING", "COP31 collapses"),
]

# Pictured stories: (number, scene key, kicker, tag, headline, body, source)
LEADS = [
    (1, "cop31", "ANTALYA, TÜRKIYE · CLIMATE", "CONFIRMED",
     "COP31 collapses with no deal",
     "Two days into overtime, the EU and island states reject a text that never "
     "names fossil fuels. “There is no agreement,” Kurum rules. The longest "
     "COP ends with no pact.",
     "UN News, Reuters"),
    (2, "drones", "KYIV REGION, UKRAINE · WAR", "CONFIRMED",
     "186 drones in the night; a block falls in Dymer",
     "Russia fires 186 drones, 72 of them jet-powered; air defences down 161. One "
     "destroys a five-storey block in Dymer: one killed, three hurt, 14 "
     "unaccounted for.",
     "Ukrainian Air Force via Reuters"),
    (3, "bahrain", "MANAMA, BAHRAIN · IRAN", "CLAIM",
     "Iran claims two US radars hit; Bahrain denies it",
     "The IRGC says it destroyed two Patriot radars at Al-Riffa and Awali. Bahrain "
     "says the target was a civilian site and calls it a violation of sovereignty.",
     "Khaleej Times, Reuters"),
]

CARDS = [
    (4, "hongkong", "HONG KONG · ELECTION", "CONFIRMED",
     "Hong Kong elects its Election Committee",
     "Record 98.79% turnout: 5,640 of 5,709 vote. (HK Govt, SCMP)",
     "HK Govt, SCMP"),
    (5, "cricket", "WELLINGTON · CRICKET", "CONFIRMED",
     "India declare on 720/9, a record in NZ",
     "Rahul 136, Pant 128; NZ 119/2 at stumps. (Cricinfo)",
     "Cricinfo"),
    (6, "f1", "LAS VEGAS · FORMULA 1", "CONFIRMED",
     "Verstappen takes the Las Vegas GP",
     "35 lead changes; Norris 2nd by 0.639s. (Formula1.com)",
     "Formula1.com, FIA"),
    (7, "liverpool", "LIVERPOOL · FOOTBALL", "CONFIRMED",
     "Liverpool rout 10-man United 4–0",
     "Yoro off in 8'; four different scorers. (Reuters)",
     "Reuters"),
    (8, "tennis", "TURIN · TENNIS", "CONFIRMED",
     "Alcaraz wins first ATP Finals title",
     "6–2, 7–6(7) over the world No. 1. (ATP Tour)",
     "ATP Tour"),
    (9, "sparta", "GULF OF FINLAND · SEA", "CONFIRMED",
     "Towing begins for drone-hit Sparta II",
     "Towed out after two days of firefighting. (Reuters)",
     "Reuters"),
    (10, "cikande", "CIKANDE, INDONESIA · FIRE", "CONFIRMED",
     "Candy-factory fire: 3 dead, 36 missing",
     "3 dead, 36 missing; 15 rescued alive. (CNA, AP)",
     "CNA, AP"),
    (11, "manipur", "MANIPUR, INDIA · POISONING", "CONFIRMED",
     "Toxic-liquor toll reaches 17",
     "17 dead, 230 in hospital, 38 on dialysis. (Statesman)",
     "The Statesman, IANS"),
    (12, "bolsonaro", "BRASÍLIA · HEALTH", "CONFIRMED",
     "Bolsonaro stable in ICU",
     "Stable; wife says he walked, pain-free. (Reuters)",
     "Reuters, AFP"),
    (13, "pope", "VATICAN CITY · FAITH", "CONFIRMED",
     "Pope hosts 1,300 poor guests for lunch",
     "Cannelloni and beef stew for 1,300. (Vatican News)",
     "Vatican News"),
    (14, "iranpower", "TEHRAN · ENERGY", "CONFIRMED",
     "Iran begins rolling power cuts",
     "Up to two hours a day, no end date. (Tavanir)",
     "Tavanir via Reuters"),
    (15, "wemby", "SAN ANTONIO · NBA", "CONFIRMED",
     "Wembanyama drops 50 as Spurs roll on",
     "50 pts, 19 reb, 5 blocks — a first. (AP)",
     "AP"),
]


# Also-on items: (region, one-liner) in two columns.
ALSO_LEFT = [
    ("EUROPE", "Belgium: Monday flights grounded 07:00–21:00 (Skeyes)"),
    ("EUROPE", "Russia says it downed 170 Ukrainian drones (Moscow)"),
    ("MIDDLE EAST", "Gaza: drone strike kills one near Deir al-Balah (Wafa)"),
    ("MIDDLE EAST", "Trump seeks a ‘permanent’ Iran deal (Al Jazeera)"),
    ("MIDDLE EAST", "Eisenkot invites Likud to coalition talks (Reuters)"),
    ("AMERICAS", "Peru quake toll: 1 dead, 16 hurt, 150 homes hit (Reuters)"),
    ("AMERICAS", "Washington pauses gun checks in FBI breach probe (AP)"),
    ("ASIA-PACIFIC", "Seoul minister quits over exam AI-cheating chaos (Yonhap)"),
    ("ASIA-PACIFIC", "Nepal PM Shah lands in Delhi; meets Modi Monday (Hindu)"),
    ("ASIA-PACIFIC", "Fukushima roads reopen after 1,500 stranded (Kyodo)"),
]
ALSO_RIGHT = [
    ("ASIA-PACIFIC", "Sonepur Mela opens; Asia’s biggest cattle fair (TOI)"),
    ("ASIA-PACIFIC", "Dutch FM Berendsen in Delhi; meets Jaishankar (Tribune)"),
    ("ASIA-PACIFIC", "M4.9 quake off Sarangani, Philippines (QuakeTrace)"),
    ("AFRICA", "Khartoum drones kill 4, damage UN building (Al Jazeera)"),
    ("AFRICA", "S. Africa: half-mast for Mlambo-Ngcuka (Presidency)"),
    ("OCEANIA", "Ashes: Australia beat England in two days (ANI)"),
    ("OCEANIA", "Cummins keeps Australia’s Test captaincy (Wires)"),
    ("OCEANIA", "Melbourne: 70 years since 1956 Olympics (ABC)"),
    ("OCEANIA", "Marles: US budget office ‘wrong’ on AUKUS (Reuters)"),
    ("WORLD", "Gold holds near $5,353 (Reuters)"),
    ("WORLD", "Bitcoin back above $60,000 (Market data)"),
]

DATE_CHECK = ("Left out — other days: Myanmar verdict (Thu) · 400-drone barrage "
    "(Thu–Fri) · Kryvyi Rih strike (Fri) · Bahrain strikes (Sat) · Bayelsa "
    "boat (Fri) · Peru quake (Fri) · Sparta II hit (Sat) · China bomber "
    "(Sat) · Somalia–UAE (Thu) · Kenya Ebola (11 Nov) · Mlambo-Ngcuka "
    "(Fri) · Cikande fire began (Sat) · FBI breach reported (Fri) · "
    "Estonia / Denmark (15–20 Nov) · Nvidia probe (Fri).")

FOOTER = ("Sources: Reuters, AP, AFP, BBC, UN News, Ukrainian Air Force, Khaleej Times, HK Govt, "
    "SCMP, Cricinfo, Formula1.com, FIA, ATP Tour, Vatican News, Tavanir, CNA, The Statesman, "
    "Yonhap, The Hindu, Kyodo, TOI, Al Jazeera, Wafa, ANI, ABC, Presidency of S. Africa. "
    "Pictures and map: original, drawn in code. Press time 20:45 WAT (19:45 UTC).")
CERTAINTY = ("CERTAINTY:  CONFIRMED = official or 2+ outlets  ·  CLAIM = one side’s account, "
    "labelled as such  ·  FORECAST = still to happen when drawn")

# Map pins: story number -> (longitude, latitude) of the pictured story.
PINS = {
    1: (30.7, 36.9), 2: (30.3, 50.8), 3: (50.6, 26.2), 4: (114.2, 22.3),
    5: (174.8, -41.3), 6: (-115.1, 36.2), 7: (-2.99, 53.4), 8: (7.7, 45.1),
    9: (25.0, 59.8), 10: (106.3, -6.2), 11: (93.9, 24.8), 12: (-47.9, -15.8),
    13: (12.45, 41.9), 14: (51.4, 35.7), 15: (-98.5, 29.4),
}
# Coarse land boxes: (lon_min, lon_max, lat_min, lat_max) for the dotted map.
LAND = [
    (-168, -55, 50, 72), (-125, -67, 25, 49), (-117, -87, 15, 32),
    (-92, -77, 7, 18), (-58, -20, 60, 84),
    (-80, -35, -55, 5), (-70, -35, 5, 12),
    (-11, 40, 36, 70), (-5, 2, 50, 59), (5, 30, 55, 71),
    (-18, 35, 5, 32), (-18, 52, -35, 5), (43, 50, -25, -12),
    (35, 63, 12, 42), (68, 89, 8, 35), (95, 110, 5, 28),
    (75, 135, 20, 53), (40, 180, 50, 75), (95, 141, -10, 6),
    (130, 146, 31, 45), (113, 154, -40, -11), (166, 178, -47, -34),
]


# ------------------------------------------------------------------ scenes
# Every scene draws into the box (x, y, w, h) in render-scale pixels.
# All pictures are original, drawn with Pillow primitives.

def _person(draw, x, y, s, shirt, skin=(232, 190, 150), hair=(40, 30, 22)):
    """Small figure: head, hair cap and shoulders. s = head radius."""
    draw.ellipse([x - s, y - s, x + s, y + s], fill=skin)
    draw.pieslice([x - s, y - s, x + s, y + s], 180, 360, fill=hair)
    draw.rounded_rectangle([x - int(1.5 * s), y + s, x + int(1.5 * s),
                            y + int(3.4 * s)], radius=int(0.6 * s), fill=shirt)


def scene_cop31(draw, x, y, w, h):
    """Negotiators around a table; the draft text crossed out, NO DEAL."""
    draw.rectangle([x, y, x + w, y + h], fill=(38, 74, 66))
    draw.rectangle([x, y, x + w, y + int(h * 0.30)], fill=(52, 96, 84))
    # flags along the top of the hall
    for i, c in enumerate([(176, 30, 36), (31, 58, 95), (196, 110, 0),
                           (15, 107, 92), (90, 60, 120), (26, 26, 26)]):
        fx = x + int(w * (0.06 + i * 0.16))
        draw.rectangle([fx, y + int(h * 0.05), fx + int(w * 0.09),
                        y + int(h * 0.24)], fill=c, outline=(255, 255, 255))
    # long table with five delegates
    draw.rectangle([x + int(w * 0.04), y + int(h * 0.52), x + int(w * 0.96),
                    y + int(h * 0.62)], fill=(120, 84, 50))
    draw.rectangle([x + int(w * 0.04), y + int(h * 0.52), x + int(w * 0.96),
                    y + int(h * 0.56)], fill=(150, 110, 66))
    for i, c in enumerate([(176, 30, 36), (31, 58, 95), (196, 110, 0),
                           (15, 107, 92), (90, 60, 120)]):
        px = x + int(w * (0.13 + i * 0.18))
        _person(draw, px, y + int(h * 0.36), int(h * 0.055), c)
    # rejected document on the table, crossed out in red
    draw.rectangle([x + int(w * 0.38), y + int(h * 0.66), x + int(w * 0.62),
                    y + int(h * 0.92)], fill=(255, 255, 255),
                   outline=(120, 120, 120))
    for j in range(4):
        draw.line([x + int(w * 0.41), y + int(h * (0.71 + j * 0.05)),
                   x + int(w * 0.59), y + int(h * (0.71 + j * 0.05))],
                  fill=(120, 120, 120), width=int(2 * SCALE))
    draw.line([x + int(w * 0.40), y + int(h * 0.68), x + int(w * 0.60),
               y + int(h * 0.90)], fill=RED, width=int(5 * SCALE))
    draw.line([x + int(w * 0.60), y + int(h * 0.68), x + int(w * 0.40),
               y + int(h * 0.90)], fill=RED, width=int(5 * SCALE))
    # gavel beside the document
    gx, gy = x + int(w * 0.72), y + int(h * 0.70)
    draw.rectangle([gx, gy, gx + int(w * 0.16), gy + int(h * 0.07)],
                   fill=(90, 60, 30))
    draw.rectangle([gx + int(w * 0.07), gy + int(h * 0.07), gx + int(w * 0.09),
                    gy + int(h * 0.24)], fill=(120, 84, 50))
    draw.ellipse([gx - int(w * 0.02), gy + int(h * 0.22), gx + int(w * 0.20),
                  gy + int(h * 0.27)], fill=(150, 110, 66))


def scene_drones(draw, x, y, w, h):
    """Night sky over Kyiv: drones, a shelled apartment block, searchlight."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 22, 44))
    for (sx, sy, sr) in [(0.12, 0.15, 3), (0.3, 0.08, 2), (0.5, 0.18, 3),
                         (0.7, 0.1, 2), (0.88, 0.2, 3), (0.42, 0.05, 2),
                         (0.62, 0.26, 2)]:
        draw.ellipse([x + int(w * sx) - sr * SCALE, y + int(h * sy) - sr * SCALE,
                      x + int(w * sx) + sr * SCALE, y + int(h * sy) + sr * SCALE],
                     fill=(255, 255, 220))
    # drones: small X silhouettes with rotor blur and a red light
    for (dx, dy, ds) in [(0.2, 0.28, 0.05), (0.55, 0.18, 0.06),
                         (0.82, 0.32, 0.045)]:
        cx, cy = x + int(w * dx), y + int(h * dy)
        r = int(w * ds)
        draw.line([cx - r, cy - r, cx + r, cy + r], fill=(200, 200, 200),
                  width=int(3 * SCALE))
        draw.line([cx - r, cy + r, cx + r, cy - r], fill=(200, 200, 200),
                  width=int(3 * SCALE))
        draw.ellipse([cx - r // 2, cy - r // 2, cx + r // 2, cy + r // 2],
                     fill=(120, 120, 120))
        draw.ellipse([cx - r - 4, cy - 3, cx - r + 4, cy + 3],
                     fill=(255, 220, 120))
    # apartment block, one section collapsed
    bx, by = x + int(w * 0.08), y + int(h * 0.42)
    bw, bh = int(w * 0.5), int(h * 0.5)
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(96, 88, 80))
    for r in range(5):
        for c in range(4):
            wx = bx + int(bw * (0.08 + c * 0.23))
            wy = by + int(bh * (0.08 + r * 0.18))
            lit = (r + c) % 3 == 0
            draw.rectangle([wx, wy, wx + int(bw * 0.14), wy + int(bh * 0.11)],
                           fill=(255, 214, 120) if lit else (52, 48, 44))
    # collapsed section: jagged dark hole, rubble and fire glow
    draw.polygon([(bx + bw, by), (bx + bw, by + bh), (bx + int(bw * 0.72), by + bh),
                  (bx + int(bw * 0.78), by + int(bh * 0.55)),
                  (bx + int(bw * 0.7), by + int(bh * 0.3))], fill=(30, 26, 24))
    draw.polygon([(bx + int(bw * 0.7), by + bh), (bx + bw, by + bh),
                  (bx + int(bw * 0.86), by + int(bh * 0.8))], fill=(70, 64, 58))
    draw.ellipse([bx + int(bw * 0.55), by + int(bh * 0.55), bx + int(bw * 0.95),
                  by + int(bh * 0.95)], fill=(255, 140, 40))
    draw.ellipse([bx + int(bw * 0.62), by + int(bh * 0.62), bx + int(bw * 0.88),
                  by + int(bh * 0.88)], fill=(255, 220, 90))
    # searchlight beam and a rescue ladder
    draw.polygon([(x + int(w * 0.95), y + h), (x + int(w * 0.72), y + int(h * 0.35)),
                  (x + int(w * 0.8), y + int(h * 0.35))], fill=(255, 244, 180))
    draw.line([x + int(w * 0.68), y + h, x + int(w * 0.78), y + int(h * 0.45)],
              fill=(220, 220, 220), width=int(4 * SCALE))


def scene_bahrain(draw, x, y, w, h):
    """Two radar dishes at night, missile trails, one dish hit."""
    draw.rectangle([x, y, x + w, y + h], fill=(44, 34, 58))
    draw.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(94, 64, 78))
    draw.ellipse([x + int(w * 0.68), y + int(h * 0.06), x + int(w * 0.86),
                  y + int(h * 0.24)], fill=(255, 196, 110))
    # two radar dishes, one tilted
    for (rx, tilt) in [(0.16, -1), (0.58, 1)]:
        cx, cy = x + int(w * rx), y + int(h * 0.62)
        draw.line([cx, cy, cx, cy + int(h * 0.18)], fill=(180, 180, 180),
                  width=int(4 * SCALE))
        draw.arc([cx - int(w * 0.09), cy - int(h * 0.16), cx + int(w * 0.09),
                  cy + int(h * 0.10)], 200 + tilt * 30, 340 + tilt * 30,
                 fill=(220, 220, 220), width=int(5 * SCALE))
        draw.line([cx, cy, cx + tilt * int(w * 0.05), cy - int(h * 0.12)],
                  fill=(220, 220, 220), width=int(3 * SCALE))
    # missile trails arcing across the sky
    draw.arc([x + int(w * 0.05), y - int(h * 0.25), x + int(w * 0.75),
              y + int(h * 0.55)], 300, 360, fill=(255, 255, 255),
             width=int(3 * SCALE))
    draw.arc([x + int(w * 0.3), y - int(h * 0.3), x + int(w * 0.95),
              y + int(h * 0.4)], 300, 355, fill=(255, 220, 120),
             width=int(3 * SCALE))
    # industrial building on fire
    ix, iy = x + int(w * 0.78), y + int(h * 0.66)
    draw.rectangle([ix, iy, ix + int(w * 0.18), iy + int(h * 0.2)],
                   fill=(70, 70, 78))
    draw.polygon([(ix + int(w * 0.03), iy), (ix + int(w * 0.07), iy - int(h * 0.12)),
                  (ix + int(w * 0.11), iy - int(h * 0.05)),
                  (ix + int(w * 0.15), iy - int(h * 0.14)),
                  (ix + int(w * 0.18), iy)], fill=(255, 140, 40))
    draw.polygon([(ix + int(w * 0.06), iy - int(h * 0.04)), (ix + int(w * 0.09),
                  iy - int(h * 0.1)), (ix + int(w * 0.12), iy - int(h * 0.04))],
                 fill=(255, 220, 90))
    draw.rectangle([x, y + int(h * 0.86), x + w, y + h], fill=(30, 26, 34))
    draw.text((x + int(w * 0.05), y + int(h * 0.88)), "CLAIM  vs  DENIAL",
              font=sans_b(int(h * 0.07)), fill=(255, 255, 255))


def scene_hongkong(draw, x, y, w, h):
    """Polling booths, a queue of voters and a ballot box marked VOTE."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 238))
    draw.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(31, 58, 95))
    # polling booths
    for i in range(3):
        bx = x + int(w * (0.06 + i * 0.22))
        draw.rectangle([bx, y + int(h * 0.18), bx + int(w * 0.17),
                        y + int(h * 0.62)], fill=(247, 243, 232),
                       outline=(120, 120, 120))
        draw.rectangle([bx, y + int(h * 0.18), bx + int(w * 0.17),
                        y + int(h * 0.26)], fill=(176, 30, 36))
    # queue of voters
    for i, c in enumerate([(176, 30, 36), (31, 58, 95), (15, 107, 92),
                           (196, 110, 0)]):
        _person(draw, x + int(w * (0.72 + (i % 2) * 0.12)),
                y + int(h * (0.30 + (i // 2) * 0.22)), int(h * 0.06), c)
    # ballot box with a paper going in
    bx, by = x + int(w * 0.36), y + int(h * 0.66)
    draw.rectangle([bx, by, bx + int(w * 0.28), by + int(h * 0.26)],
                   fill=(176, 30, 36))
    draw.rectangle([bx + int(w * 0.04), by - int(h * 0.05), bx + int(w * 0.24),
                    by], fill=(120, 20, 24))
    draw.polygon([(bx + int(w * 0.1), by - int(h * 0.22)),
                  (bx + int(w * 0.18), by - int(h * 0.22)),
                  (bx + int(w * 0.2), by - int(h * 0.05)),
                  (bx + int(w * 0.08), by - int(h * 0.05))], fill=(255, 255, 255),
                 outline=(120, 120, 120))
    draw.text((bx + int(w * 0.02), by + int(h * 0.08)), "VOTE",
              font=sans_b(int(h * 0.15)), fill=(255, 255, 255))


def scene_cricket(draw, x, y, w, h):
    """Batsman at the crease, stumps, and a 720/9 scoreboard."""
    draw.rectangle([x, y, x + w, y + h], fill=(96, 158, 82))
    draw.rectangle([x + int(w * 0.42), y, x + int(w * 0.58), y + h],
                   fill=(214, 190, 140))
    draw.rectangle([x, y + int(h * 0.78), x + w, y + h], fill=(70, 128, 60))
    # stumps
    sx, sy = x + int(w * 0.52), y + int(h * 0.30)
    for i in range(3):
        draw.line([sx + i * int(w * 0.015), sy, sx + i * int(w * 0.015),
                   sy + int(h * 0.14)], fill=(240, 220, 160), width=int(3 * SCALE))
    # batsman
    px, py = x + int(w * 0.34), y + int(h * 0.42)
    draw.ellipse([px - int(w * 0.03), py - int(w * 0.03), px + int(w * 0.03),
                  py + int(w * 0.03)], fill=(232, 190, 150))
    draw.line([px, py + int(w * 0.03), px - int(w * 0.02), py + int(h * 0.28)],
              fill=(31, 58, 95), width=int(7 * SCALE))
    draw.line([px, py + int(w * 0.03), px + int(w * 0.05), py + int(h * 0.10)],
              fill=(31, 58, 95), width=int(6 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.28), px - int(w * 0.06),
               py + int(h * 0.42)], fill=(240, 240, 240), width=int(6 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.28), px + int(w * 0.03),
               py + int(h * 0.42)], fill=(240, 240, 240), width=int(6 * SCALE))
    # bat and red ball
    draw.line([px + int(w * 0.05), py + int(h * 0.10), px + int(w * 0.12),
               py + int(h * 0.34)], fill=(180, 140, 80), width=int(6 * SCALE))
    draw.ellipse([x + int(w * 0.66), y + int(h * 0.18), x + int(w * 0.70),
                  y + int(h * 0.22)], fill=(176, 30, 36))
    # scoreboard
    draw.rectangle([x + int(w * 0.62), y + int(h * 0.58), x + int(w * 0.97),
                    y + int(h * 0.92)], fill=(26, 26, 26))
    draw.text((x + int(w * 0.67), y + int(h * 0.66)), "720/9",
              font=serif_b(int(h * 0.19)), fill=(255, 214, 120))


def scene_f1(draw, x, y, w, h):
    """Neon Las Vegas skyline, a race car and a chequered flag."""
    draw.rectangle([x, y, x + w, y + h], fill=(18, 18, 34))
    # neon skyline
    for (bx, bh, c) in [(0.02, 0.30, (255, 80, 160)),
                        (0.14, 0.42, (80, 200, 255)),
                        (0.28, 0.34, (255, 200, 60)),
                        (0.44, 0.48, (160, 90, 255)),
                        (0.60, 0.36, (255, 80, 160)),
                        (0.74, 0.44, (80, 200, 255)),
                        (0.88, 0.30, (255, 200, 60))]:
        draw.rectangle([x + int(w * bx), y + int(h * (0.55 - bh)),
                        x + int(w * (bx + 0.09)), y + int(h * 0.55)], fill=c)
    # track
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(52, 52, 62))
    draw.line([x, y + int(h * 0.72), x + w, y + int(h * 0.72)],
              fill=(255, 255, 255), width=int(2 * SCALE))
    for i in range(6):
        draw.line([x + int(w * (0.05 + i * 0.16)), y + int(h * 0.72),
                   x + int(w * (0.09 + i * 0.16)), y + int(h * 0.72)],
                  fill=(255, 214, 120), width=int(4 * SCALE))
    # race car, low side profile
    cx, cy = x + int(w * 0.30), y + int(h * 0.62)
    draw.polygon([(cx, cy), (cx + int(w * 0.12), cy - int(h * 0.05)),
                  (cx + int(w * 0.34), cy - int(h * 0.05)),
                  (cx + int(w * 0.44), cy), (cx + int(w * 0.40), cy + int(h * 0.04)),
                  (cx, cy + int(h * 0.04))], fill=(176, 30, 36))
    draw.polygon([(cx + int(w * 0.14), cy - int(h * 0.05)),
                  (cx + int(w * 0.18), cy - int(h * 0.12)),
                  (cx + int(w * 0.28), cy - int(h * 0.12)),
                  (cx + int(w * 0.30), cy - int(h * 0.05))], fill=(26, 26, 26))
    for wx in (0.06, 0.36):
        draw.ellipse([cx + int(w * wx), cy - int(h * 0.02),
                      cx + int(w * (wx + 0.07)), cy + int(h * 0.05)],
                     fill=(10, 10, 10), outline=(200, 200, 200))
    # chequered flag
    fx, fy = x + int(w * 0.80), y + int(h * 0.30)
    for r in range(3):
        for c in range(4):
            draw.rectangle([fx + c * int(w * 0.035), fy + r * int(h * 0.05),
                            fx + (c + 1) * int(w * 0.035),
                            fy + (r + 1) * int(h * 0.05)],
                           fill=(26, 26, 26) if (r + c) % 2 == 0 else (255, 255, 255))
    draw.line([fx, fy, fx, fy + int(h * 0.28)], fill=(200, 200, 200),
              width=int(3 * SCALE))


def scene_liverpool(draw, x, y, w, h):
    """Football pitch: a red scorer, a white defender and a 4–0 board."""
    draw.rectangle([x, y, x + w, y + h], fill=(96, 158, 82))
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(70, 128, 60))
    draw.ellipse([x + int(w * 0.05), y + int(h * 0.10), x + int(w * 0.95),
                  y + int(h * 0.62)], outline=(255, 255, 255), width=int(3 * SCALE))
    # goal with net lines
    gx, gy = x + int(w * 0.62), y + int(h * 0.18)
    draw.rectangle([gx, gy, gx + int(w * 0.30), gy + int(h * 0.34)],
                   outline=(255, 255, 255), width=int(4 * SCALE))
    for i in range(4):
        draw.line([gx + int(w * 0.075 * i), gy, gx + int(w * 0.075 * i),
                   gy + int(h * 0.34)], fill=(255, 255, 255), width=int(1 * SCALE))
    # red scorer striking the ball
    px, py = x + int(w * 0.30), y + int(h * 0.40)
    draw.ellipse([px - int(w * 0.035), py - int(w * 0.035), px + int(w * 0.035),
                  py + int(w * 0.035)], fill=(232, 190, 150))
    draw.line([px, py + int(w * 0.035), px - int(w * 0.02), py + int(h * 0.30)],
              fill=(176, 30, 36), width=int(8 * SCALE))
    draw.line([px, py + int(w * 0.035), px + int(w * 0.06), py + int(h * 0.14)],
              fill=(176, 30, 36), width=int(7 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.30), px - int(w * 0.07),
               py + int(h * 0.44)], fill=(255, 255, 255), width=int(6 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.30), px + int(w * 0.04),
               py + int(h * 0.44)], fill=(255, 255, 255), width=int(6 * SCALE))
    # white defender and the ball in the net
    qx, qy = x + int(w * 0.52), y + int(h * 0.46)
    draw.ellipse([qx - int(w * 0.03), qy - int(w * 0.03), qx + int(w * 0.03),
                  qy + int(w * 0.03)], fill=(210, 170, 130))
    draw.line([qx, qy + int(w * 0.03), qx, qy + int(h * 0.26)],
              fill=(240, 240, 240), width=int(7 * SCALE))
    draw.ellipse([gx + int(w * 0.12), gy + int(h * 0.12), gx + int(w * 0.17),
                  gy + int(h * 0.17)], fill=(255, 255, 255), outline=(26, 26, 26))
    # scoreboard
    draw.rectangle([x + int(w * 0.05), y + int(h * 0.68), x + int(w * 0.38),
                    y + int(h * 0.90)], fill=(26, 26, 26))
    draw.text((x + int(w * 0.09), y + int(h * 0.71)), "4–0",
              font=serif_b(int(h * 0.16)), fill=(255, 255, 255))


def scene_tennis(draw, x, y, w, h):
    """Tennis court: a player serving, the net, ball and trophy."""
    draw.rectangle([x, y, x + w, y + h], fill=(58, 92, 158))
    draw.rectangle([x, y + int(h * 0.60), x + w, y + h], fill=(96, 158, 82))
    draw.line([x + int(w * 0.1), y + int(h * 0.60), x + int(w * 0.9),
               y + int(h * 0.60)], fill=(255, 255, 255), width=int(2 * SCALE))
    # net
    draw.rectangle([x + int(w * 0.55), y + int(h * 0.42), x + int(w * 0.57),
                    y + int(h * 0.62)], fill=(240, 240, 240))
    draw.rectangle([x + int(w * 0.30), y + int(h * 0.44), x + int(w * 0.57),
                    y + int(h * 0.50)], outline=(255, 255, 255), width=int(2 * SCALE))
    # player with racket
    px, py = x + int(w * 0.24), y + int(h * 0.30)
    draw.ellipse([px - int(w * 0.035), py - int(w * 0.035), px + int(w * 0.035),
                  py + int(w * 0.035)], fill=(232, 190, 150))
    draw.line([px, py + int(w * 0.035), px - int(w * 0.01), py + int(h * 0.30)],
              fill=(255, 255, 255), width=int(8 * SCALE))
    draw.line([px, py + int(w * 0.035), px + int(w * 0.09), py - int(h * 0.02)],
              fill=(255, 255, 255), width=int(6 * SCALE))
    draw.ellipse([px + int(w * 0.09), py - int(h * 0.10), px + int(w * 0.17),
                  py - int(h * 0.02)], outline=(255, 255, 255), width=int(4 * SCALE))
    draw.line([px - int(w * 0.01), py + int(h * 0.30), px - int(w * 0.06),
               py + int(h * 0.46)], fill=(26, 26, 26), width=int(6 * SCALE))
    draw.line([px - int(w * 0.01), py + int(h * 0.30), px + int(w * 0.05),
               py + int(h * 0.46)], fill=(26, 26, 26), width=int(6 * SCALE))
    # ball and trophy
    draw.ellipse([x + int(w * 0.66), y + int(h * 0.30), x + int(w * 0.70),
                  y + int(h * 0.34)], fill=(220, 255, 80))
    tx, ty = x + int(w * 0.78), y + int(h * 0.62)
    draw.polygon([(tx, ty), (tx + int(w * 0.10), ty), (tx + int(w * 0.08),
                  ty + int(h * 0.12)), (tx + int(w * 0.02), ty + int(h * 0.12))],
                 fill=(255, 214, 120))
    draw.rectangle([tx - int(w * 0.01), ty + int(h * 0.12), tx + int(w * 0.11),
                    ty + int(h * 0.16)], fill=(255, 214, 120))
    draw.rectangle([tx + int(w * 0.02), ty + int(h * 0.16), tx + int(w * 0.08),
                    ty + int(h * 0.19)], fill=(196, 160, 60))


def scene_sparta(draw, x, y, w, h):
    """Cargo ship under tow after a drone hit; rescue boat spraying water."""
    draw.rectangle([x, y, x + w, y + h], fill=(168, 205, 225))
    draw.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(52, 96, 138))
    for i in range(3):
        draw.arc([x + int(w * (0.02 + i * 0.3)), y + int(h * 0.66),
                  x + int(w * (0.22 + i * 0.3)), y + int(h * 0.86)], 180, 360,
                 fill=(220, 235, 245), width=int(3 * SCALE))
    # cargo ship with smoke and a small fire
    sx, sy = x + int(w * 0.10), y + int(h * 0.44)
    draw.polygon([(sx, sy), (sx + int(w * 0.62), sy), (sx + int(w * 0.56),
                  sy + int(h * 0.16)), (sx + int(w * 0.04), sy + int(h * 0.16))],
                 fill=(90, 40, 36))
    draw.rectangle([sx + int(w * 0.06), sy - int(h * 0.10), sx + int(w * 0.16),
                    sy], fill=(200, 200, 200))
    for i, c in enumerate([(176, 30, 36), (31, 58, 95), (196, 110, 0),
                           (15, 107, 92)]):
        draw.rectangle([sx + int(w * (0.20 + i * 0.11)), sy - int(h * 0.09),
                        sx + int(w * (0.29 + i * 0.11)), sy - int(h * 0.01)],
                       fill=c)
    for (ox, oy, r) in [(0.30, 0.22, 0.05), (0.36, 0.14, 0.06),
                        (0.43, 0.08, 0.05)]:
        draw.ellipse([x + int(w * ox) - int(w * r), y + int(h * oy) - int(h * r),
                      x + int(w * ox) + int(w * r), y + int(h * oy) + int(h * r)],
                     fill=(90, 90, 90))
    draw.ellipse([x + int(w * 0.34), y + int(h * 0.30), x + int(w * 0.42),
                  y + int(h * 0.38)], fill=(255, 140, 40))
    # rescue boat spraying water at the hull
    bx, by = x + int(w * 0.74), y + int(h * 0.58)
    draw.polygon([(bx, by), (bx + int(w * 0.18), by), (bx + int(w * 0.15),
                  by + int(h * 0.08)), (bx + int(w * 0.02), by + int(h * 0.08))],
                 fill=(220, 60, 50))
    draw.arc([bx - int(w * 0.30), by - int(h * 0.30), bx + int(w * 0.05),
              by + int(h * 0.05)], 270, 350, fill=(220, 240, 250),
             width=int(5 * SCALE))
    draw.arc([bx - int(w * 0.26), by - int(h * 0.24), bx + int(w * 0.02),
              by + int(h * 0.02)], 280, 350, fill=(200, 230, 245),
             width=int(3 * SCALE))


def scene_cikande(draw, x, y, w, h):
    """Candy factory with sawtooth roof, big flames and a fire crew."""
    draw.rectangle([x, y, x + w, y + h], fill=(52, 44, 40))
    draw.rectangle([x, y, x + w, y + int(h * 0.40)], fill=(120, 100, 92))
    # factory with sawtooth roof
    fx, fy = x + int(w * 0.06), y + int(h * 0.44)
    draw.rectangle([fx, fy, fx + int(w * 0.88), fy + int(h * 0.42)],
                   fill=(150, 140, 128))
    for i in range(4):
        draw.polygon([(fx + int(w * (0.06 + i * 0.22)), fy),
                      (fx + int(w * (0.17 + i * 0.22)), fy - int(h * 0.12)),
                      (fx + int(w * (0.28 + i * 0.22)), fy)], fill=(120, 112, 100))
    for i in range(5):
        draw.rectangle([fx + int(w * (0.10 + i * 0.17)), fy + int(h * 0.10),
                        fx + int(w * (0.20 + i * 0.17)), fy + int(h * 0.28)],
                       fill=(60, 54, 48))
    # big flames with yellow cores, and smoke
    for (flx, flw, flh) in [(0.20, 0.16, 0.34), (0.42, 0.20, 0.44),
                            (0.66, 0.16, 0.36)]:
        draw.polygon([(x + int(w * flx), fy + int(h * 0.05)),
                      (x + int(w * (flx + flw / 2)), fy - int(h * flh)),
                      (x + int(w * (flx + flw)), fy + int(h * 0.05))],
                     fill=(255, 140, 40))
        draw.polygon([(x + int(w * (flx + 0.04)), fy + int(h * 0.05)),
                      (x + int(w * (flx + flw / 2)), fy - int(h * (flh - 0.14))),
                      (x + int(w * (flx + flw - 0.04)), fy + int(h * 0.05))],
                     fill=(255, 220, 90))
    for (ox, oy, r) in [(0.30, 0.10, 0.06), (0.55, 0.06, 0.07),
                        (0.75, 0.12, 0.05)]:
        draw.ellipse([x + int(w * ox) - int(w * r), y + int(h * oy) - int(h * r),
                      x + int(w * ox) + int(w * r), y + int(h * oy) + int(h * r)],
                     fill=(40, 36, 34))
    # fire crew hose line
    draw.line([x + int(w * 0.05), y + int(h * 0.95), x + int(w * 0.30),
               y + int(h * 0.70)], fill=(220, 220, 220), width=int(4 * SCALE))
    _person(draw, x + int(w * 0.08), y + int(h * 0.82), int(h * 0.05),
            (255, 200, 40))


def scene_manipur(draw, x, y, w, h):
    """Hospital ward: a bed, an IV drip and medicine bottles."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 226, 228))
    draw.rectangle([x, y, x + w, y + int(h * 0.30)], fill=(168, 200, 210))
    draw.rectangle([x + int(w * 0.06), y + int(h * 0.06), x + int(w * 0.30),
                    y + int(h * 0.24)], fill=(255, 255, 255),
                   outline=(120, 160, 170))
    draw.line([x + int(w * 0.06), y + int(h * 0.15), x + int(w * 0.30),
               y + int(h * 0.15)], fill=(176, 30, 36), width=int(3 * SCALE))
    # hospital bed with a patient
    bx, by = x + int(w * 0.08), y + int(h * 0.62)
    draw.rectangle([bx, by, bx + int(w * 0.84), by + int(h * 0.08)],
                   fill=(90, 110, 130))
    draw.line([bx + int(w * 0.02), by + int(h * 0.08), bx + int(w * 0.02),
               by + int(h * 0.26)], fill=(90, 110, 130), width=int(4 * SCALE))
    draw.line([bx + int(w * 0.82), by + int(h * 0.08), bx + int(w * 0.82),
               by + int(h * 0.26)], fill=(90, 110, 130), width=int(4 * SCALE))
    draw.ellipse([bx + int(w * 0.06), by - int(h * 0.10), bx + int(w * 0.14),
                  by - int(h * 0.02)], fill=(232, 190, 150))
    draw.rounded_rectangle([bx + int(w * 0.14), by - int(h * 0.06),
                            bx + int(w * 0.70), by + int(h * 0.02)],
                           radius=int(3 * SCALE), fill=(240, 240, 240))
    # IV drip stand and bag
    ix = x + int(w * 0.88)
    draw.line([ix, y + int(h * 0.28), ix, y + int(h * 0.86)],
              fill=(90, 90, 90), width=int(4 * SCALE))
    draw.rounded_rectangle([ix - int(w * 0.035), y + int(h * 0.30),
                            ix + int(w * 0.035), y + int(h * 0.46)],
                           radius=int(4 * SCALE), fill=(220, 235, 220),
                           outline=(120, 160, 120))
    draw.line([ix, y + int(h * 0.46), ix - int(w * 0.10), y + int(h * 0.58)],
              fill=(120, 160, 120), width=int(2 * SCALE))
    # medicine bottles on a table
    for i, c in enumerate([(176, 30, 36), (31, 58, 95), (196, 110, 0)]):
        bxx = x + int(w * (0.40 + i * 0.10))
        draw.rectangle([bxx, y + int(h * 0.78), bxx + int(w * 0.05),
                        y + int(h * 0.92)], fill=c)
        draw.rectangle([bxx + int(w * 0.015), y + int(h * 0.74),
                        bxx + int(w * 0.035), y + int(h * 0.78)],
                       fill=(200, 200, 200))


def scene_bolsonaro(draw, x, y, w, h):
    """ICU bed with a heart monitor and an IV bag."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 232, 236))
    draw.rectangle([x, y, x + w, y + int(h * 0.34)], fill=(168, 190, 205))
    # heart monitor with a green trace
    mx, my = x + int(w * 0.60), y + int(h * 0.08)
    draw.rectangle([mx, my, mx + int(w * 0.34), my + int(h * 0.24)],
                   fill=(26, 26, 26))
    draw.line([(mx + int(w * 0.03), my + int(h * 0.12)),
               (mx + int(w * 0.09), my + int(h * 0.12)),
               (mx + int(w * 0.13), my + int(h * 0.05)),
               (mx + int(w * 0.17), my + int(h * 0.19)),
               (mx + int(w * 0.21), my + int(h * 0.12)),
               (mx + int(w * 0.31), my + int(h * 0.12))],
              fill=(80, 220, 120), width=int(3 * SCALE))
    draw.line([mx + int(w * 0.17), my + int(h * 0.24), mx + int(w * 0.17),
               my + int(h * 0.34)], fill=(90, 90, 90), width=int(3 * SCALE))
    # bed with a patient under a blanket
    bx, by = x + int(w * 0.08), y + int(h * 0.60)
    draw.rectangle([bx, by, bx + int(w * 0.80), by + int(h * 0.10)],
                   fill=(120, 130, 140))
    draw.line([bx + int(w * 0.03), by + int(h * 0.10), bx + int(w * 0.03),
               by + int(h * 0.30)], fill=(120, 130, 140), width=int(4 * SCALE))
    draw.line([bx + int(w * 0.77), by + int(h * 0.10), bx + int(w * 0.77),
               by + int(h * 0.30)], fill=(120, 130, 140), width=int(4 * SCALE))
    draw.ellipse([bx + int(w * 0.04), by - int(h * 0.12), bx + int(w * 0.13),
                  by - int(h * 0.03)], fill=(232, 190, 150))
    draw.ellipse([bx + int(w * 0.04), by - int(h * 0.12), bx + int(w * 0.13),
                  by - int(h * 0.07)], fill=(200, 200, 200))
    draw.rounded_rectangle([bx + int(w * 0.13), by - int(h * 0.07),
                            bx + int(w * 0.62), by + int(h * 0.04)],
                           radius=int(3 * SCALE), fill=(31, 58, 95))
    # IV bag
    ix = x + int(w * 0.90)
    draw.line([ix, y + int(h * 0.36), ix, y + int(h * 0.80)],
              fill=(90, 90, 90), width=int(4 * SCALE))
    draw.rounded_rectangle([ix - int(w * 0.035), y + int(h * 0.38),
                            ix + int(w * 0.035), y + int(h * 0.52)],
                           radius=int(4 * SCALE), fill=(240, 240, 220),
                           outline=(150, 150, 120))


def scene_pope(draw, x, y, w, h):
    """Vatican hall: arches, guests at a long table, the Pope in white."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 168, 120))
    draw.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(232, 214, 178))
    # arches
    for i in range(3):
        ax = x + int(w * (0.08 + i * 0.32))
        draw.arc([ax, y + int(h * 0.04), ax + int(w * 0.24), y + int(h * 0.42)],
                 180, 360, fill=(150, 120, 80), width=int(4 * SCALE))
    # long table with guests
    draw.rectangle([x + int(w * 0.04), y + int(h * 0.58), x + int(w * 0.96),
                    y + int(h * 0.68)], fill=(255, 255, 255))
    draw.rectangle([x + int(w * 0.04), y + int(h * 0.68), x + int(w * 0.96),
                    y + int(h * 0.74)], fill=(176, 30, 36))
    for i, c in enumerate([(31, 58, 95), (15, 107, 92), (196, 110, 0),
                           (90, 60, 120), (176, 30, 36), (60, 90, 60)]):
        _person(draw, x + int(w * (0.10 + i * 0.16)), y + int(h * 0.42),
                int(h * 0.05), c)
    # white-robed figure at the centre of the table
    cx, cy = x + int(w * 0.50), y + int(h * 0.34)
    draw.ellipse([cx - int(w * 0.035), cy - int(w * 0.035),
                  cx + int(w * 0.035), cy + int(w * 0.035)],
                 fill=(232, 190, 150))
    draw.polygon([(cx - int(w * 0.05), cy + int(w * 0.03)),
                  (cx + int(w * 0.05), cy + int(w * 0.03)),
                  (cx + int(w * 0.07), cy + int(h * 0.24)),
                  (cx - int(w * 0.07), cy + int(h * 0.24))],
                 fill=(255, 255, 255))
    # plates on the table
    for i in range(6):
        px = x + int(w * (0.10 + i * 0.16))
        draw.ellipse([px - int(w * 0.025), y + int(h * 0.60),
                      px + int(w * 0.025), y + int(h * 0.64)],
                     fill=(240, 240, 240), outline=(180, 180, 180))


def scene_iranpower(draw, x, y, w, h):
    """Dark skyline at night: most windows dark, a few lit, a pylon."""
    draw.rectangle([x, y, x + w, y + h], fill=(24, 28, 52))
    draw.ellipse([x + int(w * 0.74), y + int(h * 0.06), x + int(w * 0.88),
                  y + int(h * 0.20)], fill=(240, 230, 200))
    # skyline: most windows dark, a few lit
    for i, (bx, bw, bh) in enumerate([(0.02, 0.12, 0.42), (0.16, 0.10, 0.55),
                                      (0.28, 0.14, 0.38), (0.44, 0.10, 0.50),
                                      (0.56, 0.12, 0.34), (0.70, 0.10, 0.46),
                                      (0.82, 0.14, 0.40)]):
        draw.rectangle([x + int(w * bx), y + int(h * (0.92 - bh)),
                        x + int(w * (bx + bw)), y + int(h * 0.92)],
                       fill=(52, 56, 84))
        for r in range(3):
            for c in range(2):
                lit = (i + r + c) % 4 == 0
                wx = x + int(w * (bx + 0.02 + c * 0.05))
                wy = y + int(h * (0.92 - bh + 0.05 + r * 0.12))
                draw.rectangle([wx, wy, wx + int(w * 0.025), wy + int(h * 0.05)],
                               fill=(255, 214, 120) if lit else (30, 34, 56))
    # power pylon with a sagging line
    px = x + int(w * 0.90)
    draw.polygon([(px - int(w * 0.03), y + int(h * 0.92)),
                  (px + int(w * 0.03), y + int(h * 0.92)),
                  (px + int(w * 0.01), y + int(h * 0.34)),
                  (px - int(w * 0.01), y + int(h * 0.34))], fill=(120, 120, 130))
    draw.line([px - int(w * 0.05), y + int(h * 0.36), px + int(w * 0.05),
               y + int(h * 0.36)], fill=(120, 120, 130), width=int(3 * SCALE))
    draw.arc([x + int(w * 0.30), y + int(h * 0.30), x + int(w * 0.90),
              y + int(h * 0.55)], 20, 160, fill=(180, 180, 190),
             width=int(2 * SCALE))
    draw.rectangle([x, y + int(h * 0.92), x + w, y + h], fill=(16, 18, 36))


def scene_wemby(draw, x, y, w, h):
    """Basketball court: a tall player dunking, hoop and a 50 board."""
    draw.rectangle([x, y, x + w, y + h], fill=(196, 158, 110))
    draw.rectangle([x, y + int(h * 0.66), x + w, y + h], fill=(150, 110, 70))
    draw.ellipse([x + int(w * 0.08), y + int(h * 0.70), x + int(w * 0.92),
                  y + int(h * 0.86)], outline=(255, 255, 255), width=int(3 * SCALE))
    # backboard and hoop
    bx, by = x + int(w * 0.72), y + int(h * 0.10)
    draw.rectangle([bx, by, bx + int(w * 0.20), by + int(h * 0.20)],
                   fill=(255, 255, 255), outline=(176, 30, 36))
    draw.ellipse([bx + int(w * 0.05), by + int(h * 0.22), bx + int(w * 0.15),
                  by + int(h * 0.28)], outline=(220, 80, 40), width=int(4 * SCALE))
    draw.line([bx + int(w * 0.10), by + int(h * 0.20), bx + int(w * 0.10),
               by + int(h * 0.22)], fill=(120, 120, 120), width=int(3 * SCALE))
    # tall player dunking: long body, one arm up to the rim
    px, py = x + int(w * 0.42), y + int(h * 0.28)
    draw.ellipse([px - int(w * 0.035), py - int(w * 0.035), px + int(w * 0.035),
                  py + int(w * 0.035)], fill=(232, 190, 150))
    draw.line([px, py + int(w * 0.035), px - int(w * 0.02), py + int(h * 0.34)],
              fill=(26, 26, 26), width=int(9 * SCALE))
    draw.line([px, py + int(w * 0.035), px + int(w * 0.16), py - int(h * 0.02)],
              fill=(26, 26, 26), width=int(7 * SCALE))
    draw.line([px, py + int(w * 0.035), px - int(w * 0.08), py + int(h * 0.12)],
              fill=(26, 26, 26), width=int(7 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.34), px - int(w * 0.07),
               py + int(h * 0.52)], fill=(240, 240, 240), width=int(7 * SCALE))
    draw.line([px - int(w * 0.02), py + int(h * 0.34), px + int(w * 0.05),
               py + int(h * 0.52)], fill=(240, 240, 240), width=int(7 * SCALE))
    # ball at the rim
    draw.ellipse([bx + int(w * 0.06), by + int(h * 0.16), bx + int(w * 0.14),
                  by + int(h * 0.24)], fill=(220, 110, 40))
    # scoreboard reading 50
    draw.rectangle([x + int(w * 0.04), y + int(h * 0.64), x + int(w * 0.24),
                    y + int(h * 0.90)], fill=(26, 26, 26))
    draw.text((x + int(w * 0.08), y + int(h * 0.67)), "50",
              font=serif_b(int(h * 0.22)), fill=(255, 214, 120))


SCENES = {
    "cop31": scene_cop31, "drones": scene_drones, "bahrain": scene_bahrain,
    "hongkong": scene_hongkong, "cricket": scene_cricket, "f1": scene_f1,
    "liverpool": scene_liverpool, "tennis": scene_tennis, "sparta": scene_sparta,
    "cikande": scene_cikande, "manipur": scene_manipur,
    "bolsonaro": scene_bolsonaro, "pope": scene_pope,
    "iranpower": scene_iranpower, "wemby": scene_wemby,
}


# ------------------------------------------------------------------ layout

def draw_topbar(draw):
    draw.rectangle([0, 0, W, 56], fill=NAVY)
    draw.text((MARGIN, 11), "THE WORLD IN ONE DAY", font=sans_b(34),
              fill=(255, 255, 255))
    right = "36 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    f = sans(27)
    draw.text((W - MARGIN - f.getlength(right), 14), right, font=f,
              fill=(220, 225, 235))


def draw_masthead(draw):
    title = "Sunday 22 November 2026"
    size = 132
    while serif_b(size).getlength(title) > CW and size > 60:
        size -= 2
    tf = serif_b(size)
    draw.text(((W - tf.getlength(title)) / 2, 66), title, font=tf, fill=INK)
    sf = sans_b(33)
    sub = SUBHEAD
    while sf.getlength(sub) > CW and sf.size > 24:
        sf = sans_b(sf.size - 1)
    draw.text(((W - sf.getlength(sub)) / 2, 196), sub, font=sf, fill=RED)
    draw.line([MARGIN, 238, W - MARGIN, 238], fill=INK, width=3)


def draw_numbers(draw):
    y0, y1 = 250, 348
    n = len(NUMBERS)
    bw = (CW - (n - 1) * 8) // n
    for i, (num, lab) in enumerate(NUMBERS):
        x0 = MARGIN + i * (bw + 8)
        draw.rectangle([x0, y0, x0 + bw, y1], outline=(180, 170, 150), width=2)
        nf = serif_b(56)
        draw.text((x0 + (bw - nf.getlength(num)) / 2, y0 + 4), num, font=nf,
                  fill=RED)
        lf = sans(21)
        lines = wrap(lab, lf, bw - 12)
        ly = y0 + 62
        for ln in lines[:2]:
            draw.text((x0 + (bw - lf.getlength(ln)) / 2, ly), ln, font=lf,
                      fill=INK)
            ly += 24


def draw_regions(draw):
    y0, y1 = 360, 400
    total = sum(c for _, c, _ in REGIONS)
    x = MARGIN
    for name, count, color in REGIONS:
        wseg = int(CW * count / total)
        if name == "WORLD":
            wseg = W - MARGIN - x
        draw.rectangle([x, y0, x + wseg, y1], fill=color)
        f = sans_b(20)
        txt = "%s %d" % (name, count)
        draw.text((x + (wseg - f.getlength(txt)) / 2, y0 + 9), txt, font=f,
                  fill=(255, 255, 255))
        x += wseg


def draw_timeline(draw):
    y0, y1 = 412, 496
    draw.rectangle([MARGIN, y0, W - MARGIN, y1], fill=NAVY)
    lf = sans_b(22)
    label = "THE DAY IN UTC"
    draw.text((MARGIN + 14, y0 + 10), label, font=lf, fill=(255, 214, 120))
    entries = TIMELINE
    half = (len(entries) + 1) // 2
    label_w = lf.getlength(label) + 30
    for row, part in enumerate([entries[:half], entries[half:]]):
        x = MARGIN + 14 + (label_w if row == 0 else 0)
        y = y0 + 8 + row * 40
        tf = sans_b(22)
        bf = sans(22)
        for t, txt in part:
            draw.text((x, y), t, font=tf, fill=(255, 120, 110))
            x += tf.getlength(t) + 8
            draw.text((x, y), txt, font=bf, fill=(255, 255, 255))
            x += bf.getlength(txt) + 8
            draw.text((x, y), "·", font=bf, fill=(180, 190, 205))
            x += bf.getlength("·") + 8


def draw_leads(draw):
    y_pic, pic_h = 512, 220
    colw = (CW - 2 * 24) // 3
    for i, (num, scene, kicker, tag, head, body, src) in enumerate(LEADS):
        x0 = MARGIN + i * (colw + 24)
        SCENES[scene](draw, x0, y_pic, colw, pic_h)
        draw.rectangle([x0, y_pic, x0 + colw, y_pic + pic_h],
                       outline=(120, 120, 120), width=2)
        # number badge on the picture, tag chip top-right
        bx, by = x0 + 8, y_pic + 8
        draw.ellipse([bx, by, bx + 34, by + 34], fill=RED)
        nf = sans_b(22)
        draw.text((bx + 17 - nf.getlength(str(num)) / 2, by + 5), str(num),
                  font=nf, fill=(255, 255, 255))
        tag_chip(draw, x0 + colw - 8, y_pic + 8, tag)
        y = y_pic + pic_h + 10
        kf = sans_b(26)
        draw.text((x0, y), "%d  %s" % (num, kicker), font=kf, fill=RED)
        y += 34
        y = para(draw, x0, y, head, serif_b(46), INK, colw, max_lines=2, line_h=54)
        y += 4
        y = para(draw, x0, y, body, serif(26), INK, colw, max_lines=4, line_h=32)
        y += 6
        sf = sans(20)
        draw.text((x0, y), "(%s)" % src, font=sf, fill=(110, 110, 110))


def draw_cards(draw):
    y0 = 1058
    row_h = 258
    gap = 16
    colw = (CW - 5 * 16) // 6
    pic_h = 108
    for r in range(2):
        y = y0 + r * (row_h + gap)
        for c in range(6):
            num, scene, kicker, tag, head, body, src = CARDS[r * 6 + c]
            x0 = MARGIN + c * (colw + 16)
            SCENES[scene](draw, x0, y, colw, pic_h)
            draw.rectangle([x0, y, x0 + colw, y + pic_h],
                           outline=(120, 120, 120), width=2)
            bx, by = x0 + 6, y + 6
            draw.ellipse([bx, by, bx + 28, by + 28], fill=RED)
            nf = sans_b(18)
            draw.text((bx + 14 - nf.getlength(str(num)) / 2, by + 4), str(num),
                      font=nf, fill=(255, 255, 255))
            tag_chip(draw, x0 + colw - 6, y + 6, tag)
            yy = y + pic_h + 8
            tf = sans_b(16)
            draw.text((x0, yy), kicker, font=tf, fill=RED)
            yy += 22
            yy = para(draw, x0, yy, head, serif_b(28), INK, colw, max_lines=2,
                      line_h=32)
            yy += 2
            para(draw, x0, yy, body, serif(20), INK, colw, max_lines=3, line_h=25)


def draw_map(draw, x0, y0, w, h):
    tf = sans_b(26)
    draw.text((x0, y0), "WHERE IT HAPPENED", font=tf, fill=INK)
    sf = sans(20)
    draw.text((x0 + tf.getlength("WHERE IT HAPPENED") + 12, y0 + 4),
              "pins match story numbers", font=sf, fill=(110, 110, 110))
    my = y0 + 36
    mh = h - 36
    draw.rectangle([x0, my, x0 + w, my + mh], fill=(226, 234, 240),
                   outline=(180, 190, 200), width=2)
    # dotted land
    for lon in range(-180, 181, 4):
        for lat in range(-60, 76, 4):
            if any(lo0 <= lon <= lo1 and la0 <= lat <= la1
                   for lo0, lo1, la0, la1 in LAND):
                px = x0 + (lon + 180) / 360 * w
                py = my + (75 - lat) / 135 * mh
                draw.ellipse([px - 3, py - 3, px + 3, py + 3],
                             fill=(120, 140, 120))
    offsets = {1: (-16, 34), 2: (-2, -22), 3: (26, 2), 5: (-22, 0), 7: (-24, -6),
               8: (-30, 8), 9: (20, -10), 13: (30, 10), 14: (-6, -20),
               15: (10, 10)}
    for n, (lon, lat) in PINS.items():
        px = x0 + (lon + 180) / 360 * w
        py = my + (75 - lat) / 135 * mh
        ox, oy = offsets.get(n, (0, 0))
        cx, cy = px + ox, py + oy
        if (ox, oy) != (0, 0):
            draw.line([px, py, cx, cy], fill=RED, width=2)
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
        draw.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED,
                     outline=(255, 255, 255), width=2)
        nf = sans_b(17)
        draw.text((cx - nf.getlength(str(n)) / 2, cy - 9), str(n), font=nf,
                  fill=(255, 255, 255))


def draw_also_on(draw, x0, y0, w, h):
    tf = sans_b(26)
    draw.text((x0, y0), "ALSO ON SUNDAY 22 NOVEMBER", font=tf, fill=INK)
    sf = sans(20)
    draw.text((x0 + tf.getlength("ALSO ON SUNDAY 22 NOVEMBER") + 12, y0 + 4),
              "— 21 more stories", font=sf, fill=(110, 110, 110))
    colw = (w - 20) // 2
    y = y0 + 36
    region_color = dict((n, c) for n, _, c in REGIONS)
    region_code = {"EUROPE": "EU", "MIDDLE EAST": "ME", "AMERICAS": "AM",
                   "ASIA-PACIFIC": "AP", "AFRICA": "AF", "OCEANIA": "OC",
                   "WORLD": "WO"}
    for ci, items in enumerate([ALSO_LEFT, ALSO_RIGHT]):
        cx = x0 + ci * (colw + 20)
        yy = y
        for name, it in items:
            color = region_color[name]
            draw.ellipse([cx, yy + 3, cx + 13, yy + 16], fill=color)
            bf = sans_b(16)
            code = region_code[name]
            draw.text((cx + 19, yy + 1), code, font=bf, fill=color)
            tf2 = sans(17)
            draw.text((cx + 19 + bf.getlength(code) + 8, yy), it, font=tf2,
                      fill=INK)
            yy += 22


def draw_datecheck(draw):
    y0, y1 = 1900, 1992
    draw.rectangle([MARGIN, y0, W - MARGIN, y1], outline=RED, width=3)
    lf = sans_b(20)
    draw.rectangle([MARGIN, y0, MARGIN + 150, y0 + 28], fill=RED)
    draw.text((MARGIN + 12, y0 + 3), "DATE CHECK", font=lf,
              fill=(255, 255, 255))
    tf = sans(19)
    lines = wrap(DATE_CHECK, tf, CW - 170)
    ly = y0 + 32
    for ln in lines[:3]:
        draw.text((MARGIN + 12, ly), ln, font=tf, fill=INK)
        ly += 22


def draw_footer(draw):
    ff = sans(16)
    lines = wrap(FOOTER, ff, CW)
    ly = 1994
    for ln in lines[:2]:
        draw.text((MARGIN, ly), ln, font=ff, fill=(110, 110, 110))
        ly += 18
    cf = sans_b(14)
    draw.text((MARGIN, ly + 2), CERTAINTY, font=cf, fill=(110, 110, 110))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw)
    draw_masthead(draw)
    draw_numbers(draw)
    draw_regions(draw)
    draw_timeline(draw)
    draw_leads(draw)
    draw_cards(draw)
    draw_map(draw, MARGIN, 1606, 604, 290)
    draw_also_on(draw, MARGIN + 628, 1606, CW - 628, 290)
    draw_datecheck(draw)
    draw_footer(draw)
    out = img.resize((1024, 1024), Image.LANCZOS)
    here = os.path.dirname(os.path.abspath(__file__))
    out.save(os.path.join(here, "entry.png"), optimize=True)
    print("saved entry.png",
          os.path.getsize(os.path.join(here, "entry.png")))


if __name__ == "__main__":
    build()
