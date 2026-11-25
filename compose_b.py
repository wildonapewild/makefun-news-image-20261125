#!/usr/bin/env python3
"""THE TWO SHORES TIMES - variant B. Deep purple + copper, Layout B.
Fixes over A: wrapped two-line headlines, clean date band, two-column
briefs, spread map pins, decks sized to fit. Lead trio pool #3/#6/#2.
13 full-scene cards + 24 numbered briefs = 37 stories, 9 regions."""
from PIL import Image, ImageDraw, ImageFont
import os, math

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
txt(512, 28, "THE TWO SHORES TIMES", PF_K(50), fill=PURPLE, anchor="ma")
txt(20, 34, "Vol. 25-XI - No. 25", AR(10), fill=FAINT)
txt(1004, 34, "ONE DAY - ONE PAGE", AR_B(10), fill=FAINT, anchor="ra")
rect(0, 84, W, 86, fill=COPPER)
rect(0, 122, W, 124, fill=COPPER)
txt(512, 103, "TUESDAY 25 NOVEMBER 2026", PF_B(25), fill=INK, anchor="ma")

# ---------- numbers strip (8) ----------
nums = [("700,000+", "RUSSIAN DEAD #6"), ("3", "TANKERS - IRAN SAYS #2"),
        ("50", "BOEING 737-8 JETS #10"), ("5-1", "MADRID v PSV #11"),
        ("12", "CORAL SPECIES BACK #13"), ("23", "INJURED, COLOMBIA #8"),
        ("7", "KILLED IN GAZA #4"), ("+31.5%", "NVIDIA MON CLOSE #36")]
y0 = 132
for i, (big, small) in enumerate(nums):
    x = 8 + i * 127
    rect(x, y0, x + 121, y0 + 38, fill=CARD, outline=COPPER, w=1)
    txt(x + 60, y0 + 12, big, AR_B(16), fill=PURPLE, anchor="ma")
    txt(x + 60, y0 + 29, small, AR(7.5), fill=FAINT, anchor="ma")

# ---------- region strip (9) ----------
regs = ["EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "ASIA", "SOUTH ASIA", "ASIA-PACIFIC", "OCEANIA", "WORLD"]
y0 = 174
for i, r in enumerate(regs):
    x = 8 + i * 113
    rect(x, y0, x + 107, y0 + 19, fill=REGION_COLORS[r])
    txt(x + 53, y0 + 9, r, AR_B(9), fill=(255, 255, 255), anchor="ma")

# ---------- timeline (6) ----------
tl = [("OVERNIGHT", "AWACS to Poland #1"), ("DAWN", "Hormuz claim #2"),
      ("MORNING", "Oilfields order #3"), ("MIDDAY", "Gaza strikes #4"),
      ("AFTERNOON", "PCE due today #33"), ("EVENING", "Storms target travel #37")]
y0 = 197
for i, (t, s) in enumerate(tl):
    x = 8 + i * 169
    rect(x, y0, x + 163, y0 + 25, fill=(238, 228, 205), outline=LINE, w=1)
    txt(x + 6, y0 + 4, t, AR_B(9), fill=COPPER)
    txt(x + 6, y0 + 14, s, AR(9), fill=INK)

# ---------- scenes ----------
def scene_oilfield(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(214, 178, 130))
    d.polygon([(x, y + h), (x + w * .4, y + h * .35), (x + w, y + h)], fill=(160, 110, 70))
    d.ellipse([x + w - 50, y + 6, x + w - 16, y + 40], fill=(240, 200, 90))
    for px in (0.15, 0.5, 0.8):
        bx = x + w * px
        d.line([bx, y + h, bx, y + h * .45], fill=(60, 40, 30), width=4)
        d.line([bx, y + h * .45, bx + 24, y + h * .3], fill=(60, 40, 30), width=4)
        d.line([bx + 24, y + h * .3, bx + 24, y + h * .55], fill=(60, 40, 30), width=3)
    rect(x + 8, y + h - 20, x + 120, y + h - 6, fill=(90, 55, 35))
    txt(x + 12, y + h - 13, "KURDISH FIELDS", AR_B(9), fill=(255, 235, 200), anchor="la")
def scene_count(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(90, 84, 110))
    for r in range(2):
        for c in range(8):
            cx, cy = x + 16 + c * (w - 30) // 7, y + 13 + r * (h - 40) // 1
            d.line([cx, cy - 6, cx, cy + 6], fill=(235, 230, 215), width=3)
            d.line([cx - 4, cy - 2, cx + 4, cy - 2], fill=(235, 230, 215), width=3)
    rect(x, y + h - 24, x + w, y + h, fill=(60, 55, 80))
    txt(x + w // 2, y + h - 12, "700,000+ DEAD - NEW ANALYSIS", AR_B(11), fill=(255, 220, 150), anchor="ma")
def scene_tanker(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(70, 130, 170))
    rect(x, y + h * .55, x + w, y + h, fill=(40, 90, 140))
    hx, hy = x + w * .2, y + h * .46
    d.polygon([(hx, hy), (hx + w * .58, hy), (hx + w * .48, hy + 15), (hx + 12, hy + 15)], fill=(50, 50, 60))
    rect(hx + 18, hy - 13, hx + w * .48, hy, fill=(200, 90, 50))
    rect(hx + w * .5, hy - 20, hx + w * .56, hy, fill=(230, 230, 220))
    for mx in (0.07, 0.9):
        cx, cy = x + w * mx, y + h * .8
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(30, 30, 40))
        for a in range(8):
            d.line([cx, cy, cx + 11 * math.cos(a * .785), cy + 11 * math.sin(a * .785)], fill=(30, 30, 40), width=2)
    txt(x + 8, y + 6, "STRAIT OF HORMUZ", AR_B(9), fill=(255, 255, 255))
def scene_jets(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(150, 180, 215))
    for jx, jy, s in ((.18, .3, 1.0), (.5, .55, .8), (.75, .22, .65)):
        bx, by = x + w * jx, y + h * jy
        d.polygon([(bx, by), (bx + 32 * s, by + 6 * s), (bx + 8 * s, by + 10 * s)], fill=(70, 80, 100))
        d.polygon([(bx + 4 * s, by), (bx - 8 * s, by - 8 * s), (bx + 10 * s, by + 2 * s)], fill=(90, 100, 120))
    rect(x, y + h - 10, x + w, y + h, fill=(90, 130, 80))
def scene_drone(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(196, 170, 140))
    for bx in (0.08, 0.42, 0.74):
        rect(x + w * bx, y + h * .48, x + w * bx + w * .18, y + h, fill=(120, 100, 85))
    cx, cy = x + w * .5, y + h * .24
    d.ellipse([cx - 20, cy - 5, cx + 20, cy + 5], fill=(40, 40, 48))
    for dx in (-28, 28):
        d.ellipse([cx + dx - 7, cy - 12, cx + dx + 7, cy - 1], outline=(40, 40, 48), width=2)
def scene_plane(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(140, 185, 225))
    d.polygon([(x + w * .14, y + h * .52), (x + w * .86, y + h * .36), (x + w * .8, y + h * .52), (x + w * .2, y + h * .64)], fill=(240, 240, 245))
    d.polygon([(x + w * .42, y + h * .47), (x + w * .55, y + h * .16), (x + w * .65, y + h * .45)], fill=(200, 205, 215))
    txt(x + w // 2, y + h - 5, "50 x 737-8", AR_B(10), fill=(30, 60, 110), anchor="ms")
def scene_coral(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(40, 130, 160))
    for cx, col in ((.22, (240, 130, 110)), (.52, (250, 170, 90)), (.8, (230, 110, 150))):
        bx = x + w * cx
        for a in (-.5, 0, .5):
            d.line([bx, y + h, bx + 20 * math.sin(a + .4), y + h * .45], fill=col, width=5)
            d.line([bx, y + h * .7, bx + 15 * math.sin(a - .5), y + h * .3], fill=col, width=4)
    rect(x, y + h - 9, x + w, y + h, fill=(220, 200, 150))
def scene_drought(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(235, 205, 130))
    d.ellipse([x + w - 40, y + 5, x + w - 8, y + 37], fill=(245, 170, 40))
    for px in (0.18, 0.48, 0.78):
        bx = x + w * px
        d.line([bx, y + h, bx, y + h * .42], fill=(90, 70, 40), width=4)
        d.polygon([(bx, y + h * .42), (bx - 14, y + h * .24), (bx + 4, y + h * .32)], fill=(80, 140, 70))
    d.line([x + 6, y + h - 7, x + w - 6, y + h - 12], fill=(150, 110, 60), width=3)
def scene_flag(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(60, 130, 80))
    d.polygon([(x, y + h), (x + w * .5, y + h * .3), (x + w, y + h)], fill=(40, 100, 60))
    rect(x + w * .42, y + h * .25, x + w * .46, y + h, fill=(80, 60, 40))
    d.polygon([(x + w * .46, y + h * .25), (x + w * .74, y + h * .33), (x + w * .46, y + h * .42)], fill=(240, 200, 60))
def scene_car(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(170, 160, 150))
    rect(x + w * .2, y + h * .48, x + w * .75, y + h * .76, fill=(150, 60, 50))
    rect(x + w * .32, y + h * .3, x + w * .62, y + h * .5, fill=(120, 50, 45))
    for wx in (.3, .65):
        d.ellipse([x + w * wx - 8, y + h * .7, x + w * wx + 8, y + h * .7 + 16], fill=(30, 30, 30))
    for sx in (.14, .84):
        d.polygon([(x + w * sx, y + h * .16), (x + w * sx + 7, y + h * .34), (x + w * sx - 7, y + h * .34)], fill=(245, 190, 60))
def scene_alliance(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(250, 225, 190))
    d.ellipse([x + w * .3, y + h * .34, x + w * .44, y + h * .58], fill=(150, 100, 70))
    d.ellipse([x + w * .56, y + h * .34, x + w * .7, y + h * .58], fill=(110, 80, 55))
    d.arc([x + w * .22, y + h * .2, x + w * .8, y + h * .85], 300, 60, fill=COPPER, width=4)
def scene_resign(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(215, 190, 170))
    rect(x + w * .14, y + h * .3, x + w * .86, y + h, fill=(170, 140, 120))
    rect(x + w * .42, y + h * .1, x + w * .58, y + h * .3, fill=(120, 60, 60))
    rect(x + w * .3, y + h * .52, x + w * .7, y + h * .65, fill=(250, 248, 240))
def scene_chip(x, y, w, h):
    rect(x, y, x + w, y + h, fill=(35, 60, 45))
    d.rectangle([x + w * .32, y + h * .18, x + w * .68, y + h * .62], fill=(60, 160, 100), outline=(220, 255, 220), width=2)
    for i in range(4):
        px = x + w * (.36 + i * .09)
        d.line([px, y + h * .18, px, y + h * .06], fill=(220, 255, 220), width=2)
        d.line([px, y + h * .62, px, y + h * .74], fill=(220, 255, 220), width=2)
    txt(x + w // 2, y + h - 3, "+31.5% MONDAY", AR_B(10), fill=(180, 255, 190), anchor="ms")

SCENES = {1: scene_jets, 2: scene_tanker, 3: scene_oilfield, 4: scene_drone, 6: scene_count,
          8: scene_car, 10: scene_plane, 13: scene_coral, 14: scene_drought, 18: scene_flag,
          23: scene_alliance, 25: scene_resign, 36: scene_chip}

def card(x, y, w, h, num, region, place, head, deck, src, cert, chip, big=False):
    rect(x, y, x + w, y + h, fill=CARD, outline=LINE, w=2 if big else 1)
    sh = int(h * (0.40 if big else 0.34))
    SCENES[num](x + 3, y + 3, w - 6, sh)
    hf = AR_B(15 if big else 10.5)
    cy = y + sh + 7
    for ln in wrap(f"{num}. {head}", hf, w - 12)[:2]:
        txt(x + 6, cy, ln, hf, fill=PURPLE); cy += 18 if big else 13
    df = AR(11 if big else 8.5)
    for ln in wrap(deck, df, w - 12)[:3 if big else 2]:
        txt(x + 6, cy, ln, df, fill=INK); cy += 14 if big else 11
    txt(x + 6, y + h - 23, f"{region} - {place}", AR_B(8), fill=REGION_COLORS.get(region, INK))
    txt(x + 6, y + h - 12, f"{src} - {cert}", AR(7.5), fill=FAINT)
    cw = d.textlength(chip, font=AR_B(8)) + 10
    rect(x + w - cw - 5, y + h - 24, x + w - 5, y + h - 5, fill=COPPER)
    txt(x + w - cw, y + h - 15, chip, AR_B(8), fill=(255, 255, 255))

# ---------- lead trio ----------
card(8, 228, 500, 236, 3, "MIDDLE EAST", "Iraq",
     "Baghdad orders Kurdish oilfields seized",
     "PM Ali al-Zaidi directs federal units to seize oilfields and crossings in Kurdish-run regions. President Barzani: Kurdistan 'will not submit to unconstitutional decisions.'",
     "Starlit / wires", "REPORTED", "OILFIELDS ORDER", big=True)
card(516, 228, 500, 114, 6, "WORLD", "Ukraine",
     "700,000 Russian dead, new count finds",
     "New analysis finds more than 700,000 Russian soldiers killed in the nearly five-year war on Ukraine.",
     "RFE/RL", "REPORTED", "700,000+ KILLED")
card(516, 350, 500, 114, 2, "MIDDLE EAST", "Strait of Hormuz",
     "Iran says 3 tankers hit by mines",
     "IRGC Navy claims three oil tankers were hit by naval mines in the Strait of Hormuz; shipping concerns rise.",
     "Iranian claim via wires", "CLAIMED", "3 TANKERS - IRAN SAYS")

# ---------- grid 10 ----------
grid = [
    (1, "EUROPE", "Poland", "NATO sends early-warning jets to Poland",
     "AWACS deployment planned after Russian missiles landed in Poland; Merz vows complete support.", "Wire reports", "REPORTED", "AWACS TO POLAND"),
    (4, "MIDDLE EAST", "Gaza", "Drone strikes kill Hamas security chief",
     "Strikes killed a senior Hamas official, three policemen and three siblings, one a child.", "Al Jazeera", "REPORTED", "7 KILLED"),
    (10, "ASIA", "China", "Xiamen Airlines orders 50 Boeing jets",
     "China Southern unit agreed to acquire 50 Boeing 737-8 jets.", "Wires", "REPORTED", "50 JETS"),
    (13, "OCEANIA", "Australia", "12 coral species brought back",
     "GBR genetic analysis resurrects 12 Acropora species; diversity wider than known.", "Science wires", "REPORTED", "12 BACK"),
    (36, "WORLD", "Nvidia", "Nvidia's $1 trillion Monday",
     "MONDAY CLOSE: +31.5%, nearly $1tn clawed back; Huang reinstated as CEO.", "Forbes via wires", "REPORTED", "+31.5% MON"),
    (8, "AMERICAS", "Colombia", "Car bomb injures at least 23",
     "A car bomb in Colombia injured at least 23 people.", "Wires", "REPORTED", "23 INJURED"),
    (14, "OCEANIA", "Fiji", "Fiji declares disaster in dry spell",
     "Nationwide disaster declared amid an El Nino dry spell.", "Wires", "REPORTED", "DISASTER"),
    (18, "AFRICA", "Senegal", "Senegal's AFCON title restored",
     "CAS ruling gives Senegal its 2025 Africa Cup title back.", "Wires", "REPORTED", "TITLE BACK"),
    (23, "SOUTH ASIA", "Punjab", "Old allies reunite in Punjab",
     "BJP and Akali Dal ally for 2027 Punjab polls, ending a six-year split.", "Indian wires", "REPORTED", "ALLIANCE"),
    (25, "ASIA-PACIFIC", "Indonesia", "Indonesia's vice-president resigns",
     "The Vice-President resigns amid political strain.", "Starlit", "REPORTED", "VP RESIGNS"),
]
gy = 472
for i, g in enumerate(grid):
    gx = 8 + (i % 5) * 203
    yy = gy + (i // 5) * 170
    card(gx, yy, 197, 162, *g)

# ---------- bottom ----------
by = 820
rect(8, by, 300, 970, fill=(238, 230, 210), outline=LINE, w=1)
txt(14, by + 5, "WHERE IT HAPPENED - PINS = CARD NUMBERS", AR_B(8.5), fill=PURPLE)
pins = [(36, 26, 30), (8, 40, 78), (1, 118, 26), (6, 132, 20), (3, 158, 44), (2, 148, 56),
        (4, 168, 58), (18, 128, 82), (23, 196, 48), (10, 232, 40), (25, 244, 62),
        (13, 262, 96), (14, 276, 84)]
for n, px, py in pins:
    cx, cy = 8 + px, by + 18 + py
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=COPPER, outline=INK)
    txt(cx, cy - 1, str(n), AR_B(7.5), fill=(255, 255, 255), anchor="ma")
txt(14, by + 138, "Dotted sketch - pins mark story places, not to scale.", AR(7.5), fill=FAINT)

rect(308, by, 500, 970, fill=(250, 240, 240), outline=LINE, w=1)
txt(314, by + 5, "DATE CHECK - NOT TODAY", AR_B(9), fill=(160, 40, 40))
dc = ["Merkury report - 23 Nov", "COP31 close - earlier", "Liverpool 4-0 - last week",
      "GTA VI launch - no release today", "Sunday close - 23 Nov prices"]
cy = by + 24
for s in dc:
    for ln in wrap("X " + s, AR(8.5), 178):
        txt(314, cy, ln, AR(8.5), fill=INK); cy += 11
    cy += 4

rect(508, by, 1016, 970, fill=CARD, outline=LINE, w=1)
txt(514, by + 5, "ALSO ON THIS PAGE - BRIEFS 14-37 (24 MORE STORIES)", AR_B(9), fill=PURPLE)
briefs_l = [
    "5 EU unveils new Russia sanctions",
    "7 First Lynx KF41 IFVs arrive, Ukraine",
    "9 Dozens held in Cartagena supermarket",
    "11 Madrid 5-1 PSV: Bellingham, Mbappe brace",
    "12 England by 8 wickets, T20I, Fraser-McGurk 27",
    "15 Iran pharmacies run dry (DW)",
    "16 Iran winter gas shortages loom",
    "17 Britain sanctions Houthis' leaders",
    "19 Rebels pull back in DR Congo",
    "20 Emir suspended in Nigeria",
    "21 Sudan RSF commander defects",
    "22 Cameroon separatist in Norway court",
]
briefs_r = [
    "24 Bangladesh opens Guangzhou office",
    "26 Solomon Islands eye Australia treaty",
    "27 North Korea touts China ties",
    "28 Denmark upholds ghetto evictions law",
    "29 Sarkozy faces Libya-case trial",
    "30 Black Sea clash at the UN",
    "31 Shortwave school for Afghan girls",
    "32 Dimorphos shadows Didymos",
    "33 PCE report due today - no figure yet",
    "34 US targets 7 firms, one Alibaba-owned",
    "35 Moscow buys inflatable decoys",
    "37 Thanksgiving storms, both coasts",
]
for col, colx in ((briefs_l, 514), (briefs_r, 764)):
    cy = by + 22
    for b in col:
        for ln in wrap(b, AR(7.5), 242):
            txt(colx, cy, ln, AR(7.5), fill=INK); cy += 9.5
        cy += 1

rect(0, 976, W, 1024, fill=PURPLE)
txt(512, 988, "Sources: RFE/RL - Starlit Daily - DW - Al Jazeera - Jagran - Forbes via wires - science wires - wire roundups", AR(10), fill=(255, 240, 210), anchor="ma")
txt(512, 1004, "Original drawings - flat layered scenes drawn for this page. Claims labelled as claims (Hormuz: Iran says). PCE due today, no figure invented.", AR(10), fill=COPPER_L, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry_b.png")
img.save(out)
print(out, os.path.getsize(out))
