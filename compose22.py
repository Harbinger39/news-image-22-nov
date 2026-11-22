#!/usr/bin/env python3
"""Compose the 22 Nov 2026 news image: 'the day as a giant clock'.

A warm, bright editorial-illustration clock face. Ten pictured stories sit in
circular medallions around the dial (sun at 12, moon at 6); the centre holds
the date; a bottom band carries the rest of the day plus a DATE CHECK box
naming the big 21 Nov stories deliberately left out.

Every pictured story was verified live as a 22 Nov 2026 event (see README.md).
All art is drawn in code with PIL primitives; no photos, no network.
Drawn at 2x and downscaled for clean edges. Deterministic output.
"""
import math
from PIL import Image, ImageDraw, ImageFont

S = 2                      # supersample factor
W = H = 1024
OUT = "/home/hatch/workspace/makefun/news22-entry/entry.png"

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONTB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CREAM = (246, 238, 220)
PAPER = (250, 244, 230)
INK = (59, 42, 26)        # dark brown
TERRA = (196, 98, 45)     # terracotta
GOLD = (201, 154, 63)
FACE = (255, 248, 231)
REDBG = (251, 239, 234)
REDB = (163, 59, 46)


def font(path, size):
    return ImageFont.truetype(path, int(size * S))


def fit_font(draw, text, path, start, max_w):
    """Largest bold font size (<= start) that fits max_w (1024-space px)."""
    size = start
    while size > 7:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w * S:
            return f
        size -= 0.5
    return font(path, 7)


class DW:
    """Draw wrapper: all coordinates in 1024-space, scaled by S."""

    def __init__(self, draw):
        self.d = draw

    def _s(self, box):
        if isinstance(box, (list, tuple)):
            return [v * S for v in box]
        return box * S

    def rect(self, box, **kw):
        self.d.rectangle(self._s(box), **kw)

    def ellipse(self, box, **kw):
        self.d.ellipse(self._s(box), **kw)

    def polygon(self, pts, **kw):
        self.d.polygon([(x * S, y * S) for x, y in pts], **kw)

    def line(self, pts, **kw):
        if "width" in kw:
            kw["width"] = int(kw["width"] * S)
        self.d.line([(x * S, y * S) for x, y in pts], **kw)

    def arc(self, box, a0, a1, **kw):
        if "width" in kw:
            kw["width"] = int(kw["width"] * S)
        self.d.arc(self._s(box), a0, a1, **kw)

    def pieslice(self, box, a0, a1, **kw):
        self.d.pieslice(self._s(box), a0, a1, **kw)

    def text(self, xy, s, f, **kw):
        self.d.text((xy[0] * S, xy[1] * S), s, font=f, **kw)

    def text_center(self, x, y, s, f, **kw):
        w = self.d.textlength(s, font=f)
        self.d.text((x * S - w / 2, y * S), s, font=f, **kw)

    def textlength(self, s, f):
        return self.d.textlength(s, font=f) / S


def circle_medallion(size=128):
    """Return (image, draw) for a vignette drawn at 4x, plus its circular mask."""
    m = size * 4
    img = Image.new("RGB", (m, m), (255, 255, 255))
    mask = Image.new("L", (m, m), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([4, 4, m - 4, m - 4], fill=255)
    return img, ImageDraw.Draw(img), mask, m


def add_banner(img, line1, line2):
    """Dark caption banner across the bottom of a vignette image (any scale)."""
    m = img.size[0]
    d = ImageDraw.Draw(img, "RGBA")
    bw = int(m * 0.94)
    bh = int(m * 0.30)
    bx0 = (m - bw) // 2
    by0 = m - bh - int(m * 0.02)
    d.rounded_rectangle([bx0, by0, bx0 + bw, by0 + bh], radius=int(m * 0.05),
                        fill=(59, 42, 26, 235))
    f1 = ImageFont.truetype(FONTB, int(m * 0.055))
    while f1.size > 8 and d.textlength(line1, font=f1) > bw * 0.92:
        f1 = ImageFont.truetype(FONTB, f1.size - 1)
    f2 = ImageFont.truetype(FONT, int(m * 0.048))
    while f2.size > 8 and d.textlength(line2, font=f2) > bw * 0.92:
        f2 = ImageFont.truetype(FONT, f2.size - 1)
    d.text((bx0 + bw / 2, by0 + bh * 0.10), line1, font=f1, fill=(255, 248, 231),
           anchor="ma")
    d.text((bx0 + bw / 2, by0 + bh * 0.56), line2, font=f2, fill=(255, 214, 170),
           anchor="ma")


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W * S, H * S), CREAM)
d = ImageDraw.Draw(img)
w = DW(d)

# faint paper speckle (deterministic)
import random
rnd = random.Random(22112026)
for _ in range(900):
    x = rnd.randint(0, W * S)
    y = rnd.randint(0, H * S)
    d.point((x, y), fill=(232, 220, 196))

# ---------------------------------------------------------------- title
w.text_center(512, 14, "SUNDAY 22 NOVEMBER 2026", font(FONTB, 46), fill=INK)
w.text_center(512, 66, "THE WORLD IN ONE DAY \u2014 TOLD BY THE CLOCK",
              font(FONTB, 19), fill=TERRA)

# ---------------------------------------------------------------- clock
CX, CY = 512, 505
RIM, FACE_R, NUM_R = 272, 252, 212

w.ellipse([CX - RIM, CY - RIM, CX + RIM, CY + RIM], fill=TERRA)
w.ellipse([CX - RIM + 8, CY - RIM + 8, CX + RIM - 8, CY + RIM - 8], fill=GOLD)
w.ellipse([CX - FACE_R, CY - FACE_R, CX + FACE_R, CY + FACE_R], fill=FACE)
# tick marks
for h in range(12):
    a = math.radians(h * 30)
    r0, r1 = NUM_R + 26, NUM_R + 38
    w.line([(CX + r0 * math.sin(a), CY - r0 * math.cos(a)),
            (CX + r1 * math.sin(a), CY - r1 * math.cos(a))],
           fill=INK, width=4)
# numerals
for h in range(1, 13):
    a = math.radians(h * 30)
    x = CX + NUM_R * math.sin(a)
    y = CY - NUM_R * math.cos(a)
    w.text_center(x, y - 17, str(h), font(FONTB, 34), fill=INK)

# hands: hour to 1, minute to 12 (the day as it began, 01:00 WAT)
def hand(angle_deg, length, width, color):
    a = math.radians(angle_deg)
    x = CX + length * math.sin(a)
    y = CY - length * math.cos(a)
    w.line([(CX, CY), (x, y)], fill=color, width=width)
    w.ellipse([x - width / 2, y - width / 2, x + width / 2, y + width / 2], fill=color)

hand(30, 128, 15, INK)     # hour hand -> 1
hand(0, 178, 10, TERRA)    # minute hand -> 12

# centre date medallion
w.ellipse([CX - 96, CY - 96, CX + 96, CY + 96], fill=(255, 246, 219), outline=INK, width=3)
w.text_center(CX, CY - 78, "SUNDAY", font(FONTB, 17), fill=TERRA)
w.text_center(CX, CY - 52, "22", font(FONTB, 66), fill=INK)
w.text_center(CX, CY + 22, "NOVEMBER", font(FONTB, 19), fill=INK)
w.text_center(CX, CY + 50, "2026", font(FONTB, 16), fill=(120, 100, 75))
w.ellipse([CX - 7, CY - 7, CX + 7, CY + 7], fill=INK)

# ---------------------------------------------------------------- vignettes
# Each draws on a 512x512 canvas; circle mask + caption applied by place().

def F(size):
    return ImageFont.truetype(FONT, int(size))


def FB(size):
    return ImageFont.truetype(FONTB, int(size))


def sun_rays(dr, cx, cy, r, n, color):
    for i in range(n):
        a = math.radians(i * 360 / n)
        x0 = cx + (r + 6) * math.cos(a)
        y0 = cy + (r + 6) * math.sin(a)
        x1 = cx + (r + 26) * math.cos(a)
        y1 = cy + (r + 26) * math.sin(a)
        dr.line([(x0, y0), (x1, y1)], fill=color, width=10)


def cloud(dr, x, y, s, color=(255, 255, 255)):
    dr.ellipse([x, y, x + 70 * s, y + 34 * s], fill=color)
    dr.ellipse([x + 14 * s, y - 16 * s, x + 62 * s, y + 22 * s], fill=color)
    dr.ellipse([x + 40 * s, y - 8 * s, x + 92 * s, y + 30 * s], fill=color)


def v_sun(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(191, 227, 248))
    sun_rays(dr, 256, 240, 78, 12, (255, 205, 60))
    dr.ellipse([178, 162, 334, 318], fill=(255, 214, 64))
    dr.ellipse([205, 190, 307, 292], fill=(255, 232, 130))
    cloud(dr, 40, 380, 1.0)
    cloud(dr, 330, 90, 0.8)
    dr.pieslice([40, 400, 472, 640], 180, 360, fill=(124, 180, 92))


def v_moon(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(30, 42, 74))
    for (x, y, s) in [(70, 80, 1), (420, 70, 1), (380, 180, 0.7), (90, 200, 0.7),
                      (450, 300, 0.8), (60, 330, 0.6), (300, 60, 0.6)]:
        dr.polygon([(x, y - 14 * s), (x + 5 * s, y - 5 * s), (x + 14 * s, y),
                    (x + 5 * s, y + 5 * s), (x, y + 14 * s), (x - 5 * s, y + 5 * s),
                    (x - 14 * s, y), (x - 5 * s, y - 5 * s)], fill=(255, 240, 180))
    dr.ellipse([176, 148, 336, 308], fill=(255, 226, 110))
    dr.ellipse([216, 128, 366, 288], fill=(30, 42, 74))
    cloud(dr, 60, 400, 0.9, color=(90, 110, 150))
    cloud(dr, 300, 420, 0.8, color=(90, 110, 150))


def v_cop31(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(143, 208, 232))
    dr.rectangle([0, 300, 512, 512], fill=(201, 233, 242))
    sun_rays(dr, 420, 70, 26, 8, (255, 214, 64))
    dr.ellipse([394, 44, 446, 96], fill=(255, 214, 64))
    cloud(dr, 30, 60, 0.9)
    cloud(dr, 300, 130, 0.7)
    # globe
    dr.ellipse([106, 120, 406, 420], fill=(46, 127, 194))
    dr.ellipse([150, 160, 260, 250], fill=(62, 155, 79))   # land mass 1
    dr.ellipse([270, 260, 370, 350], fill=(62, 155, 79))   # land mass 2
    dr.ellipse([230, 150, 300, 210], fill=(84, 178, 96))
    dr.ellipse([140, 300, 230, 380], fill=(84, 178, 96))
    # leaf sprout on top of the globe
    dr.polygon([(256, 108), (286, 60), (256, 78), (226, 60)], fill=(62, 155, 79))
    dr.line([(256, 108), (256, 70)], fill=(46, 120, 60), width=8)


def v_f1(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(20, 27, 61))
    for (x, y) in [(50, 60), (120, 40), (300, 50), (430, 90), (200, 30), (470, 180)]:
        dr.ellipse([x, y, x + 6, y + 6], fill=(255, 255, 255))
    # neon strips (the Strip)
    dr.rectangle([0, 96, 512, 116], fill=(255, 46, 136))
    dr.rectangle([0, 116, 512, 122], fill=(255, 210, 63))
    dr.rectangle([0, 380, 512, 392], fill=(255, 210, 63))
    # speed lines
    for y in (240, 270, 300):
        dr.line([(20, y), (180, y)], fill=(255, 255, 255), width=8)
    # race car (side profile, facing right)
    dr.polygon([(90, 300), (130, 268), (300, 262), (380, 278), (420, 300),
                (420, 322), (90, 322)], fill=(225, 6, 0))
    dr.polygon([(300, 262), (330, 236), (380, 236), (400, 262)], fill=(160, 4, 0))
    dr.rectangle([398, 228, 440, 244], fill=(40, 40, 40))   # rear wing
    dr.rectangle([398, 244, 406, 300], fill=(40, 40, 40))
    dr.ellipse([130, 296, 196, 362], fill=(20, 20, 20))     # wheels
    dr.ellipse([318, 296, 384, 362], fill=(20, 20, 20))
    dr.ellipse([152, 318, 174, 340], fill=(180, 180, 180))
    dr.ellipse([340, 318, 362, 340], fill=(180, 180, 180))
    dr.rectangle([150, 268, 290, 282], fill=(200, 230, 255))  # cockpit glass
    dr.rectangle([0, 400, 512, 512], fill=(12, 16, 36))


def v_indnz(img, dr):
    dr.rectangle([0, 0, 512, 300], fill=(191, 227, 240))
    dr.rectangle([0, 300, 512, 512], fill=(76, 154, 63))
    cloud(dr, 40, 60, 0.9)
    cloud(dr, 320, 90, 0.7)
    # scoreboard (top centre, inside the circle)
    dr.rounded_rectangle([150, 22, 362, 66], radius=12, fill=(59, 42, 26))
    dr.text((256, 44), "IND 616/5", font=FB(28), fill=(255, 248, 231), anchor="mm")
    # stumps
    for x in (360, 378, 396):
        dr.rectangle([x, 210, x + 10, 300], fill=(255, 214, 64))
    dr.rectangle([360, 202, 406, 210], fill=(255, 214, 64))
    # batsman (white kit, mid-swing)
    dr.ellipse([128, 120, 172, 164], fill=(222, 184, 150))          # head
    dr.ellipse([128, 120, 172, 150], fill=(40, 40, 40))             # cap
    dr.polygon([(120, 170), (180, 170), (196, 300), (104, 300)], fill=(245, 245, 240))
    dr.polygon([(110, 300), (140, 300), (132, 400), (104, 400)], fill=(245, 245, 240))
    dr.polygon([(160, 300), (190, 300), (200, 400), (170, 400)], fill=(245, 245, 240))
    dr.polygon([(180, 180), (300, 120), (316, 140), (196, 200)], fill=(150, 105, 60))  # bat
    dr.line([(180, 180), (150, 220)], fill=(222, 184, 150), width=18)  # arm
    # red ball flying off the bat
    dr.ellipse([318, 96, 350, 128], fill=(200, 30, 30))
    dr.arc([318, 96, 350, 128], 200, 340, fill=(255, 255, 255), width=4)


def v_sonepur(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(247, 183, 115))
    dr.rectangle([0, 400, 512, 512], fill=(214, 164, 110))
    # bunting
    for i, c in enumerate([(225, 6, 0), (255, 210, 63), (62, 155, 79), (46, 127, 194)] * 6):
        x = 10 + i * 22
        dr.polygon([(x, 20), (x + 20, 20), (x + 10, 48)], fill=c)
    # ferris wheel
    cx, cy, r = 256, 210, 130
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(120, 70, 30), width=10)
    for i in range(8):
        a = math.radians(i * 45)
        dr.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
                fill=(120, 70, 30), width=6)
        gx = cx + r * math.cos(a)
        gy = cy + r * math.sin(a)
        dr.ellipse([gx - 16, gy - 16, gx + 16, gy + 16],
                   fill=[(225, 6, 0), (255, 210, 63), (62, 155, 79), (46, 127, 194)][i % 4])
    dr.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(120, 70, 30))
    dr.line([(cx - 90, 400), (cx, cy)], fill=(120, 70, 30), width=12)
    dr.line([(cx + 90, 400), (cx, cy)], fill=(120, 70, 30), width=12)
    # cattle silhouette at the fair
    dr.ellipse([60, 420, 150, 470], fill=(90, 60, 40))
    dr.ellipse([140, 410, 165, 440], fill=(90, 60, 40))
    dr.polygon([(60, 420), (48, 392), (66, 414)], fill=(90, 60, 40))
    dr.polygon([(150, 418), (164, 392), (166, 420)], fill=(90, 60, 40))
    for x in (75, 100, 125, 145):
        dr.rectangle([x, 465, x + 8, 495], fill=(90, 60, 40))


def v_dutch(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(234, 243, 248))
    # India flag (left), Netherlands flag (right)
    dr.rectangle([30, 40, 170, 200], outline=(59, 42, 26), width=4)
    dr.rectangle([34, 44, 166, 97], fill=(255, 153, 51))
    dr.rectangle([34, 97, 166, 150], fill=(255, 255, 255))
    dr.rectangle([34, 150, 166, 196], fill=(19, 136, 8))
    dr.ellipse([80, 103, 120, 143], outline=(6, 62, 132), width=5)
    dr.rectangle([342, 40, 482, 200], outline=(59, 42, 26), width=4)
    dr.rectangle([346, 44, 478, 97], fill=(174, 28, 40))
    dr.rectangle([346, 97, 478, 150], fill=(255, 255, 255))
    dr.rectangle([346, 150, 478, 196], fill=(33, 70, 139))
    # two figures shaking hands
    dr.ellipse([196, 210, 244, 258], fill=(222, 184, 150))
    dr.ellipse([268, 210, 316, 258], fill=(222, 184, 150))
    dr.polygon([(180, 270), (260, 270), (268, 420), (172, 420)], fill=(40, 60, 110))
    dr.polygon([(252, 270), (332, 270), (340, 420), (244, 420)], fill=(60, 60, 66))
    dr.polygon([(226, 270), (244, 270), (240, 320), (230, 320)], fill=(255, 153, 51))
    dr.polygon([(276, 270), (294, 270), (290, 320), (280, 320)], fill=(200, 40, 40))
    dr.line([(250, 300), (268, 330)], fill=(222, 184, 150), width=20)
    dr.line([(262, 300), (244, 330)], fill=(222, 184, 150), width=20)
    dr.ellipse([244, 318, 268, 342], fill=(222, 184, 150))


def v_senate(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(207, 227, 242))
    cloud(dr, 30, 60, 0.8)
    cloud(dr, 340, 40, 0.7)
    # Capitol dome
    dr.pieslice([156, 120, 356, 320], 180, 360, fill=(245, 245, 240))
    dr.rectangle([150, 240, 362, 320], fill=(245, 245, 240))
    dr.rectangle([140, 320, 372, 340], fill=(220, 220, 215))
    for x in (170, 210, 250, 290, 330):
        dr.rectangle([x, 320, x + 16, 400], fill=(245, 245, 240))
        dr.rectangle([x - 4, 316, x + 20, 324], fill=(220, 220, 215))
    dr.rectangle([130, 400, 382, 420], fill=(200, 200, 195))
    dr.rectangle([110, 420, 402, 440], fill=(180, 180, 175))
    dr.rectangle([90, 440, 422, 460], fill=(160, 160, 155))
    # flag on top
    dr.line([(256, 120), (256, 70)], fill=(59, 42, 26), width=6)
    dr.polygon([(256, 70), (306, 82), (256, 94)], fill=(178, 34, 52))
    dr.rectangle([0, 460, 512, 512], fill=(124, 180, 92))
    # two podiums with figures (the two rivals), heads above the banner
    dr.ellipse([94, 268, 130, 304], fill=(222, 184, 150))
    dr.polygon([(82, 312), (142, 312), (150, 352), (74, 352)], fill=(40, 60, 110))
    dr.ellipse([382, 268, 418, 304], fill=(222, 184, 150))
    dr.polygon([(370, 312), (430, 312), (438, 352), (362, 352)], fill=(120, 30, 30))


def v_ashes(img, dr):
    dr.rectangle([0, 0, 512, 300], fill=(255, 233, 168))
    dr.rectangle([0, 300, 512, 512], fill=(62, 142, 65))
    sun_rays(dr, 430, 70, 24, 8, (255, 205, 60))
    dr.ellipse([406, 46, 454, 94], fill=(255, 214, 64))
    # scoreboard (top centre, inside the circle)
    dr.rounded_rectangle([150, 22, 362, 66], radius=12, fill=(59, 42, 26))
    dr.text((256, 44), "AUS 205/2", font=FB(28), fill=(255, 248, 231), anchor="mm")
    # stumps, upright
    for x in (330, 352, 374):
        dr.rectangle([x, 210, x + 10, 300], fill=(255, 214, 64))
    dr.rectangle([330, 202, 384, 210], fill=(255, 214, 64))
    # big bat, ball
    dr.polygon([(120, 340), (200, 180), (240, 196), (170, 360)], fill=(150, 105, 60))
    dr.polygon([(200, 180), (230, 150), (258, 166), (240, 196)], fill=(120, 80, 45))
    dr.ellipse([270, 120, 306, 156], fill=(200, 30, 30))
    dr.arc([270, 120, 306, 156], 200, 340, fill=(255, 255, 255), width=4)
    # the Ashes urn (small, on the pitch)
    dr.polygon([(60, 400), (100, 400), (94, 440), (66, 440)], fill=(200, 170, 120))
    dr.ellipse([58, 388, 102, 404], fill=(200, 170, 120))


def v_forest(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(191, 232, 201))
    sun_rays(dr, 80, 70, 24, 8, (255, 214, 64))
    dr.ellipse([56, 46, 104, 94], fill=(255, 214, 64))
    cloud(dr, 330, 60, 0.8)
    # three pines
    for (x, s) in [(110, 1.0), (256, 1.25), (400, 0.9)]:
        h = 150 * s
        dr.rectangle([x - 12 * s, 400, x + 12 * s, 460], fill=(120, 70, 30))
        for k in range(3):
            y0 = 400 - h + k * h / 3
            wdt = (90 - k * 22) * s
            dr.polygon([(x - wdt, y0 + h / 3), (x + wdt, y0 + h / 3),
                        (x, y0 - 10)], fill=(34, 120, 60) if k % 2 else (46, 140, 74))
    dr.rectangle([0, 460, 512, 512], fill=(124, 180, 92))
    dr.polygon([(226, 460), (286, 460), (320, 512), (192, 512)], fill=(214, 184, 140))


def v_airindia(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(168, 216, 240))
    cloud(dr, 40, 70, 0.9)
    cloud(dr, 320, 50, 0.7)
    cloud(dr, 180, 150, 0.6)
    # runway
    dr.rectangle([0, 420, 512, 512], fill=(120, 120, 125))
    for x in range(20, 500, 60):
        dr.rectangle([x, 460, x + 34, 470], fill=(255, 255, 255))
    # plane (white, red-orange tail)
    dr.ellipse([60, 250, 452, 320], fill=(255, 255, 255))
    dr.polygon([(400, 250), (452, 210), (470, 210), (452, 290)], fill=(200, 40, 40))
    dr.polygon([(440, 250), (452, 210), (470, 210), (470, 250)], fill=(255, 120, 40))
    dr.polygon([(200, 300), (280, 360), (330, 360), (280, 300)], fill=(220, 220, 225))
    dr.polygon([(90, 270), (40, 300), (60, 310), (110, 290)], fill=(220, 220, 225))
    for x in range(120, 380, 28):
        dr.ellipse([x, 272, x + 12, 284], fill=(40, 80, 130))
    # JEDDAH sign with red X
    dr.rounded_rectangle([150, 330, 362, 392], radius=10, fill=(59, 42, 26))
    dr.text((256, 361), "JEDDAH", font=FB(34), fill=(255, 248, 231), anchor="mm")
    dr.line([(160, 340), (352, 382)], fill=(225, 30, 30), width=10)
    dr.line([(352, 340), (160, 382)], fill=(225, 30, 30), width=10)


def v_icmr(img, dr):
    dr.rectangle([0, 0, 512, 512], fill=(232, 244, 248))
    # bench
    dr.rectangle([0, 380, 512, 512], fill=(180, 190, 195))
    dr.rectangle([0, 380, 512, 396], fill=(140, 150, 155))
    # test tubes
    for i, (x, c) in enumerate([(60, (46, 127, 194)), (130, (62, 155, 79)),
                                (200, (230, 120, 30))]):
        dr.rounded_rectangle([x, 240, x + 44, 390], radius=12, fill=(255, 255, 255),
                             outline=(120, 130, 135), width=4)
        dr.rectangle([x + 6, 300, x + 38, 384], fill=c)
    # microscope
    dr.polygon([(300, 390), (430, 390), (420, 360), (310, 360)], fill=(70, 80, 90))
    dr.line([(365, 360), (365, 200)], fill=(70, 80, 90), width=22)
    dr.line([(365, 200), (440, 150)], fill=(70, 80, 90), width=18)
    dr.ellipse([430, 130, 470, 170], fill=(120, 140, 150))
    dr.ellipse([440, 140, 460, 160], fill=(40, 80, 130))
    dr.polygon([(330, 360), (400, 360), (390, 300), (340, 300)], fill=(100, 110, 120))
    # flask with green liquid
    dr.polygon([(300, 330), (330, 330), (330, 300), (318, 300), (318, 330)],
               fill=(255, 255, 255))
    dr.polygon([(300, 330), (290, 390), (340, 390), (330, 330)], fill=(255, 255, 255),
               outline=(120, 130, 135))
    dr.polygon([(296, 360), (334, 360), (340, 390), (290, 390)], fill=(62, 155, 79))


VIGNETTES = [
    # (hour position, draw fn, line1, line2)
    (1, v_cop31, "COP31 DEAL", "Final text near"),
    (2, v_f1, "VEGAS GP", "Verstappen on pole"),
    (3, v_indnz, "PANT'S TON", "India 616/5"),
    (4, v_sonepur, "SONEPUR MELA", "Opens in Bihar"),
    (5, v_dutch, "DUTCH FM", "Arrives in Delhi"),
    (7, v_senate, "SENATE SHOWDOWN", "Schumer v Van Hollen"),
    (8, v_ashes, "ASHES WIN", "Head 123, 2 days"),
    (9, v_forest, "FOREST PLAN", "William: 10,000 insured"),
    (10, v_airindia, "JEDDAH OFF", "Air India to 24 Nov"),
    (11, v_icmr, "ICMR MILESTONE", "100 tech transfers"),
]


def place(hour, fn, line1, line2):
    a = math.radians(hour * 30)
    ring = 348
    cx = int(CX + ring * math.sin(a))
    cy = int(CY - ring * math.cos(a))
    # connector from clock rim to medallion
    w.line([(CX + 276 * math.sin(a), CY - 276 * math.cos(a)),
            (cx - 66 * math.sin(a), cy + 66 * math.cos(a))],
           fill=GOLD, width=3)
    img_v, dr_v, mask, m = circle_medallion(128)
    fn(img_v, dr_v)
    add_banner(img_v, line1, line2)
    small = img_v.resize((128 * S, 128 * S), Image.LANCZOS)
    small_mask = mask.resize((128 * S, 128 * S), Image.LANCZOS)
    img.paste(small, ((cx - 64) * S, (cy - 64) * S), small_mask)
    d.ellipse([(cx - 64) * S, (cy - 64) * S, (cx + 64) * S, (cy + 64) * S],
              outline=(255, 255, 255), width=3 * S)


# sun at 12, moon at 6 (decorative day/night markers)
for hour, fn, l1, l2 in [(12, v_sun, "THE DAY", "Begins"), (6, v_moon, "THE DAY", "Ends")]:
    a = math.radians(hour * 30)
    ring = 348
    cx = int(CX + ring * math.sin(a))
    cy = int(CY - ring * math.cos(a))
    w.line([(CX + 276 * math.sin(a), CY - 276 * math.cos(a)),
            (cx - 66 * math.sin(a), cy + 66 * math.cos(a))],
           fill=GOLD, width=3)
    img_v, dr_v, mask, m = circle_medallion(128)
    fn(img_v, dr_v)
    add_banner(img_v, l1, l2)
    small = img_v.resize((128 * S, 128 * S), Image.LANCZOS)
    small_mask = mask.resize((128 * S, 128 * S), Image.LANCZOS)
    img.paste(small, ((cx - 64) * S, (cy - 64) * S), small_mask)
    d.ellipse([(cx - 64) * S, (cy - 64) * S, (cx + 64) * S, (cy + 64) * S],
              outline=(255, 255, 255), width=3 * S)

for hour, fn, l1, l2 in VIGNETTES:
    place(hour, fn, l1, l2)

# ---------------------------------------------------------------- bottom band
w.line([(0, 922), (1024, 922)], fill=GOLD, width=3)

# ALSO TODAY (left)
w.text((24, 930), "ALSO TODAY", font(FONTB, 15), fill=TERRA)
also = [
    "\u2022 Cummins keeps Australia's Test captaincy \u2014 Cricket Australia",
    "\u2022 Victoria votes Sat 28 Nov; early voting centres shut today",
    "\u2022 COP31 approval session 06:00 GMT; F1 Las Vegas race 04:00 UTC",
]
for i, line in enumerate(also):
    w.text((24, 952 + i * 18), line, font(FONT, 14), fill=INK)
w.text((24, 1006),
       "Sources: AP \u00b7 Reuters \u00b7 AFP \u00b7 ANI \u00b7 NDTV \u00b7 Arab News \u00b7 Times of India",
       font(FONT, 11), fill=(120, 100, 75))

# DATE CHECK box (right) — big 21 Nov stories deliberately left out
d.rectangle([655 * S, 926 * S, 1004 * S, 1020 * S], fill=REDBG,
            outline=REDB, width=2 * S)
w.text((668, 932), "DATE CHECK \u2014 LEFT OUT ON PURPOSE", font(FONTB, 12), fill=REDB)
check = ("Not 22 Nov: ICJ Myanmar verdict (19 Nov) \u2022 Peru quake (21 Nov) \u2022 "
         "Houthi missiles on Riyadh (21 Nov) \u2022 Trump card-rate vow (21 Nov) \u2022 "
         "Iran strikes on Bahrain (21 Nov) \u2022 French protests (21 Nov) \u2022 "
         "Brazil storm (20 Nov) \u2022 WFP outlook (20 Nov)")
# wrap to fit 322px at 10.5px
words, lines, cur = check.split(" "), [], ""
f10 = font(FONT, 10.5)
for wd in words:
    trial = (cur + " " + wd).strip()
    if d.textlength(trial, font=f10) <= 322 * S:
        cur = trial
    else:
        lines.append(cur)
        cur = wd
lines.append(cur)
for i, line in enumerate(lines):
    w.text((668, 950 + i * 12), line, f10, fill=(90, 50, 40))

# ---------------------------------------------------------------- save
out = img.resize((W, H), Image.LANCZOS)
out.save(OUT, optimize=True)
print("saved", OUT, out.size)
