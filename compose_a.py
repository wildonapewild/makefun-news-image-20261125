#!/usr/bin/env python3
"""THE TWO SHORES TIMES - variant A. Deep purple + copper, Layout B.
Lead trio: #3 Iraq (wide hero), #6 700k count, #2 Hormuz claim.
13 full-scene cards + 24 numbered briefs = 37 stories, 9 regions."""
from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
FD = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
def F(name, size):
    return ImageFont.truetype(FD + name, size)
PF_B = lambda s: F("PlayfairDisplay-Bold.ttf", s)
PF_K = lambda s: F("PlayfairDisplay-Black.ttf", s)
AR = lambda s: F("Archivo.ttf", s)
AR_B = lambda s: F("Archivo-Bold.ttf", s)

PAPER = (247, 240, 225); INK = (43, 16, 63); PURPLE = (59, 24, 92)
COPPER = (181, 106, 50); COPPER_L = (224, 164, 110); FAINT = (120, 105, 130)
CARD = (252, 248, 238); LINE = (43, 16, 63)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def rect(x0, y0, x1, y1, fill=None, outline=None, w=1):
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=outline, width=w)
def txt(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)
def wrap(s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = wd
    if cur: lines.append(cur)
    return lines

REGION_COLORS = {
    "EUROPE": (70, 110, 180), "MIDDLE EAST": (181, 106, 50), "AFRICA": (46, 139, 87),
    "AMERICAS": (178, 60, 60), "ASIA": (200, 150, 40), "SOUTH ASIA": (220, 110, 160),
    "ASIA-PACIFIC": (90, 170, 190), "OCEANIA": (60, 160, 140), "WORLD": (110, 90, 170),
}

# ---------- header ----------
rect(0, 0, W, 24, fill=PURPLE)
txt(512, 12, "37 DATED STORIES  -  9 REGIONS  -  EVERY CARD SOURCED AND CHECKED", AR_B(13), fill=(255, 240, 210), anchor="ma")
txt(512, 30, "THE TWO SHORES TIMES", PF_K(52), fill=PURPLE, anchor="ma")
rect(0, 88, W, 90, fill=COPPER); rect(0, 130, W, 132, fill=COPPER)
txt(512, 110, "TUESDAY 25 NOVEMBER 2026", PF_B(30), fill=INK, anchor="ma")
txt(880, 96, "ONE DAY - ONE PAGE", AR_B(10), fill=FAINT)
txt(20, 96, "Vol. 25-XI - No. 25", AR(10), fill=FAINT)

# ---------- numbers strip (8) ----------
nums = [("700,000+", "RUSSIAN DEAD #6"), ("3", "TANKERS - IRAN SAYS #2"),
        ("50", "BOEING 737-8 JETS #10"), ("5-1", "MADRID v PSV #11"),
        ("12", "CORAL SPECIES BACK #13"), ("23", "INJURED, COLOMBIA #8"),
        ("7", "KILLED IN GAZA #4"), ("+31.5%", "NVIDIA MON CLOSE #36")]
y0 = 138
for i, (big, small) in enumerate(nums):
    x = 8 + i * 127
    rect(x, y0, x + 121, y0 + 40, fill=CARD, outline=COPPER, w=1)
    txt(x + 60, y0 + 13, big, AR_B(17), fill=PURPLE, anchor="ma")
    txt(x + 60, y0 + 31, small, AR(7.5), fill=FAINT, anchor="ma")

# ---------- region strip (9) ----------
regs = ["EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "ASIA", "SOUTH ASIA", "ASIA-PACIFIC", "OCEANIA", "WORLD"]
y0 = 182
for i, r in enumerate(regs):
    x = 8 + i * 113
    rect(x, y0, x + 107, y0 + 20, fill=REGION_COLORS[r])
    txt(x + 53, y0 + 10, r, AR_B(9), fill=(255, 255, 255), anchor="ma")

# ---------- timeline (6) ----------
tl = [("OVERNIGHT", "AWACS to Poland #1"), ("DAWN", "Hormuz claim #2"),
      ("MORNING", "Oilfields order #3"), ("MIDDAY", "Gaza strikes #4"),
      ("AFTERNOON", "PCE due today #33"), ("EVENING", "Storms target travel #37")]
y0 = 206
for i, (t, s) in enumerate(tl):
    x = 8 + i * 169
    rect(x, y0, x + 163, y0 + 26, fill=(238, 228, 205), outline=LINE, w=1)
    txt(x + 6, y0 + 4, t, AR_B(9), fill=COPPER)
    txt(x + 6, y0 + 15, s, AR(9), fill=INK)

# ---------- scene helpers ----------
def scene_oilfield(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(214, 178, 130))
    d.polygon([(x, y + h), (x + w * .4, y + h * .35), (x + w, y + h)], fill=(160, 110, 70))
    for px in (0.18, 0.55, 0.82):
        bx = x + w * px
        d.line([bx, y + h, bx, y + h * .45], fill=(60, 40, 30), width=4)
        d.line([bx, y + h * .45, bx + 26, y + h * .3], fill=(60, 40, 30), width=4)
        d.line([bx + 26, y + h * .3, bx + 26, y + h * .55], fill=(60, 40, 30), width=3)
    d.ellipse([x + w - 52, y + 8, x + w - 14, y + 46], fill=(240, 200, 90))
def scene_count(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(90, 84, 110))
    for r in range(3):
        for c in range(7):
            cx, cy = x + 14 + c * (w - 20) // 6, y + 14 + r * (h - 24) // 2
            d.line([cx, cy - 7, cx, cy + 7], fill=(235, 230, 215), width=3)
            d.line([cx - 5, cy - 3, cx + 5, cy - 3], fill=(235, 230, 215), width=3)
    txt(x + w // 2, y + h - 4, "700,000+", PF_B(20), fill=(255, 220, 150), anchor="ms")
def scene_tanker(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(70, 130, 170))
    rect(x, y + h * .55, x + w, y + h, fill=(40, 90, 140))
    hx, hy = x + w * .18, y + h * .48
    d.polygon([(hx, hy), (hx + w * .6, hy), (hx + w * .5, hy + 16), (hx + 12, hy + 16)], fill=(50, 50, 60))
    rect(hx + 20, hy - 14, hx + w * .5, hy, fill=(200, 90, 50))
    rect(hx + w * .52, hy - 22, hx + w * .58, hy, fill=(230, 230, 220))
    for mx in (0.08, 0.88):
        cx = x + w * mx; cy = y + h * .78
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(30, 30, 40))
        for a in range(8):
            import math
            d.line([cx, cy, cx + 12 * math.cos(a), cy + 12 * math.sin(a)], fill=(30, 30, 40), width=2)
def scene_jets(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(150, 180, 215))
    for jx, jy, s in ((.2, .35, 1.0), (.55, .55, .8), (.78, .25, .65)):
        bx, by = x + w * jx, y + h * jy
        d.polygon([(bx, by), (bx + 34 * s, by + 6 * s), (bx + 8 * s, by + 10 * s)], fill=(70, 80, 100))
        d.polygon([(bx + 4 * s, by), (bx - 8 * s, by - 8 * s), (bx + 10 * s, by + 2 * s)], fill=(90, 100, 120))
    rect(x, y + h - 12, x + w, y + h, fill=(90, 130, 80))
def scene_drone(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(196, 170, 140))
    for bx in (0.1, 0.45, 0.75):
        rect(x + w * bx, y + h * .45, x + w * bx + w * .18, y + h, fill=(120, 100, 85))
    cx, cy = x + w * .5, y + h * .25
    d.ellipse([cx - 22, cy - 6, cx + 22, cy + 6], fill=(40, 40, 48))
    for dx in (-30, 30):
        d.ellipse([cx + dx - 8, cy - 14, cx + dx + 8, cy - 2], outline=(40, 40, 48), width=2)
def scene_plane(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(140, 185, 225))
    d.polygon([(x + w * .15, y + h * .55), (x + w * .85, y + h * .4), (x + w * .8, y + h * .55), (x + w * .2, y + h * .68)], fill=(240, 240, 245))
    d.polygon([(x + w * .42, y + h * .5), (x + w * .55, y + h * .2), (x + w * .65, y + h * .48)], fill=(200, 205, 215))
    txt(x + w // 2, y + h - 6, "50 x 737-8", AR_B(11), fill=(30, 60, 110), anchor="ms")
def scene_coral(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(40, 130, 160))
    for cx, col in ((.25, (240, 130, 110)), (.55, (250, 170, 90)), (.8, (230, 110, 150))):
        bx = x + w * cx
        for a in (-.5, 0, .5):
            import math
            d.line([bx, y + h, bx + 22 * math.sin(a + .4), y + h * .45], fill=col, width=5)
            d.line([bx, y + h * .7, bx + 16 * math.sin(a - .5), y + h * .3], fill=col, width=4)
    rect(x, y + h - 10, x + w, y + h, fill=(220, 200, 150))
def scene_drought(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(235, 205, 130))
    d.ellipse([x + w - 44, y + 6, x + w - 8, y + 42], fill=(245, 170, 40))
    for px in (0.2, 0.5, 0.8):
        bx = x + w * px
        d.line([bx, y + h, bx, y + h * .4], fill=(90, 70, 40), width=4)
        d.polygon([(bx, y + h * .4), (bx - 16, y + h * .22), (bx + 4, y + h * .3)], fill=(80, 140, 70))
    d.line([x + 6, y + h - 8, x + w - 6, y + h - 14], fill=(150, 110, 60), width=3)
def scene_flag(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(60, 130, 80))
    d.polygon([(x, y + h), (x + w * .5, y + h * .3), (x + w, y + h)], fill=(40, 100, 60))
    rect(x + w * .42, y + h * .25, x + w * .46, y + h, fill=(80, 60, 40))
    d.polygon([(x + w * .46, y + h * .25), (x + w * .75, y + h * .33), (x + w * .46, y + h * .42)], fill=(240, 200, 60))
def scene_car(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(170, 160, 150))
    rect(x + w * .2, y + h * .5, x + w * .75, y + h * .78, fill=(150, 60, 50))
    rect(x + w * .32, y + h * .32, x + w * .62, y + h * .52, fill=(120, 50, 45))
    for wx in (.3, .65):
        d.ellipse([x + w * wx - 9, y + h * .72, x + w * wx + 9, y + h * .72 + 18], fill=(30, 30, 30))
    for sx in (.15, .85):
        d.polygon([(x + w * sx, y + h * .2), (x + w * sx + 8, y + h * .38), (x + w * sx - 8, y + h * .38)], fill=(245, 190, 60))
def scene_alliance(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(250, 225, 190))
    d.ellipse([x + w * .32, y + h * .38, x + w * .46, y + h * .6], fill=(150, 100, 70))
    d.ellipse([x + w * .56, y + h * .38, x + w * .7, y + h * .6], fill=(110, 80, 55))
    d.arc([x + w * .25, y + h * .25, x + w * .78, y + h * .85], 300, 60, fill=(181, 106, 50), width=4)
def scene_resign(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(215, 190, 170))
    rect(x + w * .15, y + h * .3, x + w * .85, y + h, fill=(170, 140, 120))
    rect(x + w * .42, y + h * .12, x + w * .58, y + h * .3, fill=(120, 60, 60))
    rect(x + w * .3, y + h * .55, x + w * .7, y + h * .68, fill=(250, 248, 240))
def scene_chip(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(35, 60, 45))
    d.rectangle([x + w * .3, y + h * .25, x + w * .7, y + h * .75], fill=(60, 160, 100), outline=(220, 255, 220), width=2)
    for i in range(4):
        d.line([x + w * (.34 + i * .1), y + h * .25, x + w * (.34 + i * .1), y + h * .12], fill=(220, 255, 220), width=2)
        d.line([x + w * (.34 + i * .1), y + h * .75, x + w * (.34 + i * .1), y + h * .88], fill=(220, 255, 220), width=2)
    txt(x + w // 2, y + h - 4, "+31.5%", AR_B(12), fill=(180, 255, 190), anchor="ms")

SCENES = {1: scene_jets, 2: scene_tanker, 3: scene_oilfield, 4: scene_drone, 6: scene_count,
          8: scene_car, 10: scene_plane, 13: scene_coral, 14: scene_drought, 18: scene_flag,
          23: scene_alliance, 25: scene_resign, 36: scene_chip}

def card(x, y, w, h, num, region, place, head, deck, src, cert, chip, big=False):
    rect(x, y, x + w, y + h, fill=CARD, outline=LINE, w=2 if big else 1)
    sh = int(h * (0.42 if big else 0.36))
    SCENES[num](x + 3, y + 3, w - 6, sh)
    cy = y + sh + 8
    txt(x + 7, cy, f"{num}. {head}", AR_B(15 if big else 11), fill=PURPLE)
    cy += 20 if big else 15
    for ln in wrap(deck, AR(11 if big else 8.5), w - 14)[:3 if big else 2]:
        txt(x + 7, cy, ln, AR(11 if big else 8.5), fill=INK); cy += 14 if big else 11
    txt(x + 7, y + h - 24, f"{region} - {place}", AR_B(8), fill=REGION_COLORS.get(region, INK))
    txt(x + 7, y + h - 13, f"{src} - {cert}", AR(7.5), fill=FAINT)
    cw = d.textlength(chip, font=AR_B(8)) + 10
    rect(x + w - cw - 6, y + h - 25, x + w - 6, y + h - 6, fill=COPPER)
    txt(x + w - cw, y + h - 16, chip, AR_B(8), fill=(255, 255, 255), anchor="la")

# ---------- lead trio (Layout B: hero left, stack right) ----------
card(8, 238, 500, 232, 3, "MIDDLE EAST", "Iraq",
     "Baghdad orders Kurdish oilfields seized",
     "PM Ali al-Zaidi directs federal units to seize oilfields and crossings in Kurdish-run regions. President Barzani: Kurdistan 'will not submit to unconstitutional decisions.'",
     "Starlit / wires", "REPORTED", "OILFIELDS ORDER")
card(516, 238, 500, 112, 6, "WORLD", "Ukraine",
     "700,000 Russian dead, new count finds",
     "New analysis finds more than 700,000 Russian soldiers killed in the nearly five-year war on Ukraine.",
     "RFE/RL", "REPORTED", "700,000+ KILLED")
card(516, 358, 500, 112, 2, "MIDDLE EAST", "Strait of Hormuz",
     "Iran says 3 tankers hit by mines",
     "IRGC Navy claims three oil tankers were hit by naval mines in the Strait of Hormuz; shipping concerns rise.",
     "Iranian claim via wires", "CLAIMED", "3 TANKERS HIT - IRAN SAYS")

# ---------- grid 10 (5 x 2) ----------
grid = [
    (1, "EUROPE", "Poland", "NATO sends early-warning jets to Poland",
     "NATO plans AWACS deployment in Poland after Russian missiles landed in Poland; Chancellor Merz vows complete support.", "Wire reports", "REPORTED", "AWACS TO POLAND"),
    (4, "MIDDLE EAST", "Gaza", "Drone strikes kill Hamas security chief",
     "Israeli drone strikes killed a senior Hamas security official, three policemen and three siblings, one a child.", "Al Jazeera", "REPORTED", "7 KILLED IN STRIKES"),
    (10, "ASIA", "China", "Xiamen Airlines orders 50 Boeing jets",
     "Xiamen Airlines, a China Southern unit, agreed to acquire 50 Boeing 737-8 jets.", "Wires", "REPORTED", "50 JETS ORDERED"),
    (13, "OCEANIA", "Australia", "12 coral species brought back",
     "Great Barrier Reef genetic analysis resurrects 12 Acropora coral species; reef diversity wider than known.", "Science wires", "REPORTED", "12 SPECIES BACK"),
    (36, "WORLD", "Nvidia", "Nvidia's $1 trillion Monday",
     "MONDAY CLOSE: shares +31.5%, nearly $1 trillion of market value clawed back as Jensen Huang was reinstated as CEO, +$34 billion in a day (Forbes).", "Forbes via wires", "REPORTED", "+31.5% MONDAY"),
    (8, "AMERICAS", "Colombia", "Car bomb injures at least 23",
     "A car bomb in Colombia injured at least 23 people.", "Wires", "REPORTED", "23 INJURED"),
    (14, "OCEANIA", "Fiji", "Fiji declares disaster in dry spell",
     "Fijian government declares a nationwide disaster amid an El Nino dry spell.", "Wires", "REPORTED", "DISASTER DECLARED"),
    (18, "AFRICA", "Senegal", "Senegal's AFCON title restored",
     "CAS ruling gives Senegal its 2025 Africa Cup of Nations title back.", "Wires", "REPORTED", "TITLE RESTORED"),
    (23, "SOUTH ASIA", "Punjab", "Old allies reunite in Punjab",
     "BJP and Shiromani Akali Dal announce an alliance for the 2027 Punjab elections, ending a six-year split.", "Indian wires", "REPORTED", "ALLIANCE AGAIN"),
    (25, "ASIA-PACIFIC", "Indonesia", "Indonesia's vice-president resigns",
     "Indonesia's Vice-President resigns amid political strain.", "Starlit", "REPORTED", "VP RESIGNS"),
]
gy = 478
for i, g in enumerate(grid):
    gx = 8 + (i % 5) * 203
    yy = gy + (i // 5) * 168
    card(gx, yy, 197, 160, *g)

# ---------- bottom: map + date check + also on ----------
by = 822
rect(8, by, 300, 968, fill=(238, 230, 210), outline=LINE, w=1)
txt(16, by + 6, "WHERE IT HAPPENED - MAP PINS = CARD NUMBERS", AR_B(9), fill=PURPLE)
pins = [(1, 60, 60), (3, 120, 78), (2, 105, 92), (4, 128, 95), (6, 70, 52), (8, 30, 105),
        (10, 225, 70), (13, 255, 118), (14, 272, 105), (18, 95, 108), (23, 175, 82),
        (25, 232, 92), (36, 38, 62)]
for n, px, py in pins:
    cx, cy = 8 + px, by + 22 + py
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=COPPER, outline=INK)
    txt(cx, cy, str(n), AR_B(8), fill=(255, 255, 255), anchor="ma")
for i in range(14):
    d.point([(20 + i * 19, by + 40 + (i % 3) * 30)], fill=FAINT)
txt(16, 950, "Dotted world sketch - pins mark story places.", AR(7.5), fill=FAINT)

rect(308, by, 500, 968, fill=(250, 240, 240), outline=LINE, w=1)
txt(316, by + 6, "DATE CHECK - NOT TODAY'S NEWS", AR_B(10), fill=(160, 40, 40))
dc = ["Merkury mission report - 23 Nov, not today", "COP31 summit close - earlier this month",
      "Liverpool 4-0 friendly - last week", "GTA VI launch hype - no release today",
      "Sunday market close - 23 Nov prices"]
cy = by + 26
for s in dc:
    for ln in wrap("X " + s, AR(9), 184):
        txt(316, cy, ln, AR(9), fill=INK); cy += 12
    cy += 3

rect(508, by, 1016, 968, fill=CARD, outline=LINE, w=1)
txt(516, by + 6, "ALSO ON THIS PAGE - BRIEFS 14-37", AR_B(10), fill=PURPLE)
briefs = [
    "5 EU unveils new Russia sanctions - Brussels",
    "7 First German Lynx KF41 IFVs arrive - Ukraine, 5 Lynx",
    "9 Gunmen hold dozens in Cartagena supermarket",
    "11 Madrid rout PSV 5-1: Bellingham stunner, Mbappe brace",
    "12 England beat Australia by 8 wickets, chase 185, T20I; Fraser-McGurk 27 off 13",
    "15 Iran pharmacies run dry - medicine shortage (DW)",
    "16 Iran braces for winter gas shortages; rationing from 22 Nov",
    "17 Britain sanctions Houthi leaders - London",
    "19 Rebels pull back after clashes - DR Congo",
    "20 Emir suspended after allegation - Nigeria",
    "21 Sudan RSF commander defects",
    "22 Cameroon separatist in Norway court - war crimes",
    "24 Bangladesh opens China office in Guangzhou",
    "26 Solomon Islands eye Australia treaty switch",
    "27 North Korea touts China ties - Pyongyang",
    "28 Denmark court upholds ghetto evictions law",
    "29 Sarkozy headed for Libya-case trial - Paris",
    "30 Black Sea clash at the UN over shipping attacks",
    "31 Shortwave school returns for Afghan girls (RFE/RL)",
    "32 Asteroid eclipse: Dimorphos shadows Didymos",
    "33 PCE inflation report due today - no figure yet, scheduled",
    "34 US targets 7 firms over chips, one Alibaba-owned",
    "35 Decoy army: Moscow buys inflatable decoys from China",
    "37 Storms target Thanksgiving travel on both US coasts",
]
cy = by + 24
for b in briefs:
    for ln in wrap(b, AR(8), 492):
        txt(516, cy, ln, AR(8), fill=INK); cy += 10.5
    cy += 0.5

rect(0, 974, W, 1024, fill=PURPLE)
txt(512, 986, "Sources: RFE/RL - Starlit Daily - DW - Al Jazeera - Jagran - Forbes via wires - science wires - wire roundups", AR(10), fill=(255, 240, 210), anchor="ma")
txt(512, 1002, "Original drawings - flat layered scenes drawn for this page. Claims labelled as claims (Hormuz: Iran says). PCE due today, no figure invented.", AR(10), fill=COPPER_L, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_a.png")
img.save(out)
print(out, os.path.getsize(out))
