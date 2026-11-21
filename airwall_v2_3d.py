"""
AIRWALL 3D model generator (v2, matches the reference concept images)
Run:  python airwall_v2_3d.py
Output: airwall_v2_3d.html (open in any browser; needs internet once for three.js)

Tabs: System (all three parts together), Outdoor unit, Indoor panel, AQI monitor.
Each part has an Outside view (casing) and an Inside view (components).
Scale: 1 unit = 10 inches, so sizes match the dimensions in the reference.
"""
import json
import math
from pathlib import Path

TITLE = "AIRWALL"
SUBTITLE = "Three-part air quality system · 3D model"
DESIGNER = "Designed by Prabhava Kaushal P"   # <- change this
HALF = 1.5708


def B(s, p, c, e=None, r=None, tex=None):
    d = dict(t="box", s=s, p=p, c=c)
    if e: d["e"] = e
    if r: d["r"] = r
    if tex: d["tex"] = tex
    return d


def C(s, p, c, e=None, r=None):
    d = dict(t="cyl", s=s, p=p, c=c)
    if e: d["e"] = e
    if r: d["r"] = r
    return d


def T(w, h, bg, items):
    return dict(w=w, h=h, bg=bg, items=items)


def txt(s, x, y, f, c, a="left", bold=True):
    return dict(s=s, x=x, y=y, f=f, c=c, a=a, b=bold)


def part(dev, side, id_, name, desc, meshes, ex=0):
    return dict(dev=dev, side=side, id=id_, name=name, desc=desc, meshes=meshes, ex=ex)


BEIGE, DARK = "#dcc7a4", "#2b3440"

MONITOR_FACE = T(512, 512, "#14191f", [
    txt("AIRWALL", 40, 66, 30, "#ffffff"),
    txt("● GOOD", 472, 66, 24, "#5ad17f", "right"),
    txt("AIR QUALITY INDEX", 40, 130, 22, "#9aa5b4", bold=False),
    txt("34", 36, 270, 150, "#6fe39a"),
    txt("PM2.5", 300, 205, 24, "#c9d1dc", bold=False),
    txt("10 µg/m³", 300, 255, 40, "#ffffff"),
    dict(r=[40, 330, 432, 2], c="#2c343e"),
    txt("26°C", 40, 400, 30, "#b9c2cf", bold=False),
    txt("48% RH", 472, 400, 30, "#b9c2cf", "right", False),
])

PARTS = [
    # ================= OUTDOOR UNIT (18" x 18" x 8") =================
    part("outdoor", "outer", "o_top", "Upper housing", "Dark weather-sealed upper half. It holds the controller and battery and carries the unit ID tag and exhaust louvers.",
         [B([1.8, .9, .8], [0, .45, 0], DARK)]),
    part("outdoor", "outer", "o_low", "Intake housing", "Sand-coloured lower half that takes in outside air through the slotted intake panel.",
         [B([1.8, .9, .8], [0, -.45, 0], BEIGE)]),
    part("outdoor", "outer", "o_tag", "Unit ID tag", "Identifies this outdoor unit (AIR 034) so it pairs with the right indoor panel and monitor.",
         [B([.42, .14, .02], [-.62, .68, .41], "#5fd0e8", tex=T(256, 84, "#5fd0e8", [txt("AIR 034", 128, 56, 36, "#12303a", "center")]))]),
    part("outdoor", "outer", "o_lou", "Exhaust louvers", "Slats that let warm electronics air escape without letting rain in.",
         [B([.5, .025, .02], [.5, .75 - .1 * i, .41], "#8c96a3") for i in range(5)]),
    part("outdoor", "outer", "o_slot", "Intake slots", "Wide horizontal slots where outdoor air is drawn in to be sampled.",
         [B([1.2, .035, .02], [-.15, -.25 - .15 * i, .41], "#8a8478") for i in range(3)]),
    part("outdoor", "outer", "o_lab", "INTAKE label", "Marks the air entry so it is never blocked or covered.",
         [B([.4, .08, .02], [.58, -.75, .41], BEIGE, tex=T(256, 52, BEIGE, [txt("INTAKE", 128, 38, 30, "#6b5f4a", "center")]))]),
    part("outdoor", "outer", "o_duct", "Outlet duct & fins", "Side duct with angled fins that sends conditioned outdoor air toward the indoor panel.",
         [B([.22, .05, .34], [1.02, -.62 + .17 * i, 0], "#7a838f", r=[0, 0, .35]) for i in range(8)] +
         [B([.05, 1.6, .05], [1.16, 0, .2], "#666c75"), B([.05, 1.6, .05], [1.16, 0, -.2], "#666c75")]),
    part("outdoor", "outer", "o_brk", "Wall / pole bracket", "Mounts the unit to an outside wall or pole.",
         [B([1.4, 1.4, .05], [0, 0, -.43], "#6b7686")]),
    part("outdoor", "inner", "o_filt", "Intake dust filter", "Coarse filter behind the intake slots that blocks leaves, insects and debris.",
         [B([1.4, .6, .06], [-.1, -.45, .3], "#a89f8c")]),
    part("outdoor", "inner", "o_fan", "Intake fan", "Pulls a steady stream of outdoor air across the sensors and into the duct.",
         [C([.3, .1], [-.1, -.45, .1], "#3b4452", r=[HALF, 0, 0])] + [B([.5, .06, .03], [-.1, -.45, .16], "#aab4c3", r=[0, 0, i * 1.047]) for i in range(3)]),
    part("outdoor", "inner", "o_pm", "PM2.5 / PM10 sensor", "Counts fine and coarse particles in outdoor air.",
         [B([.3, .25, .15], [-.6, -.45, -.1], "#ffb347")]),
    part("outdoor", "inner", "o_gas", "Gas sensor", "Measures CO₂, NO₂ and other pollutants.",
         [B([.25, .2, .1], [-.2, -.45, -.15], "#4aa3ff")]),
    part("outdoor", "inner", "o_air", "Air duct", "Internal channel that carries sampled air from the fan to the outlet fins.",
         [C([.12, .9], [.5, -.1, 0], "#5b7a9a", r=[0, 0, HALF])]),
    part("outdoor", "inner", "o_mcu", "ESP32 controller", "Reads the sensors and sends readings to the indoor panel and AQI monitor over Wi-Fi.",
         [B([.55, .4, .04], [-.5, .45, -.2], "#1f9d55"), B([.18, .18, .05], [-.5, .45, -.17], "#111")]),
    part("outdoor", "inner", "o_bat", "Battery pack", "18650 cells keep the unit working through power cuts.",
         [B([.6, .3, .2], [.3, .45, -.2], "#2f6bd9")]),
    part("outdoor", "inner", "o_chg", "Power / charge board", "Charges the battery and regulates power for the fan and electronics.",
         [B([.4, .3, .05], [.5, -.45, -.25], "#d94f4f")]),

    # ================= INDOOR PANEL (8" H x 18" W x 1.5" D) =================
    part("indoor", "outer", "i_house", "Panel body", "Slim white panel that sits flat on the wall like a piece of decor.",
         [B([1.8, .8, .15], [0, 0, 0], "#f2f4f7")]),
    part("indoor", "outer", "i_slat", "Air slats", "Long horizontal slots that draw room air in and return it clean, with no visible fan or grille.",
         [B([1.5, .035, .01], [0, .22 - .07 * i, .08], "#9aa3ae") for i in range(8)]),
    part("indoor", "outer", "i_lab", "AIRWALL label", "Brand mark in the top-left corner.",
         [B([.5, .08, .01], [-.6, .32, .08], "#f2f4f7", tex=T(256, 40, "#f2f4f7", [txt("AIRWALL", 8, 30, 26, "#8a93a0")]))]),
    part("indoor", "outer", "i_led", "Airflow indicator", "Cyan light glows when the panel is moving air.",
         [B([.12, .03, .01], [.82, .3, .08], "#4fd3f0", e="#22a6c4")]),
    part("indoor", "outer", "i_brk", "Wall standoffs", "Four spacers hold the panel off the wall so air can flow behind it.",
         [B([.12, .12, .08], [x, y, -.11], "#6b7686") for x in (-.75, .75) for y in (-.25, .25)]),
    part("indoor", "inner", "i_pre", "Pre-filter", "Washable mesh that catches hair, lint and large dust.",
         [B([1.55, .6, .02], [0, 0, .06], "#8a93a0")]),
    part("indoor", "inner", "i_hepa", "HEPA filter", "Pleated filter that traps 99.97% of particles down to 0.3 µm, including PM2.5.",
         [B([1.5, .55, .04], [0, 0, .025], "#f4f4f4")] + [B([.015, .55, .045], [-.7 + .1 * i, 0, .025], "#cfd3d8") for i in range(15)]),
    part("indoor", "inner", "i_carb", "Carbon layer", "Activated charcoal that absorbs odours and VOCs.",
         [B([1.45, .5, .02], [0, 0, -.01], "#2b2f36")]),
    part("indoor", "inner", "i_fan", "Blower fans", "Two slim blowers move air through the filters.",
         [C([.2, .04], [x, 0, -.04], "#3b4452", r=[HALF, 0, 0]) for x in (-.4, .4)]),
    part("indoor", "inner", "i_mcu", "Controller board", "Drives the fans and the airflow light, and pairs with the outdoor unit and monitor.",
         [B([.3, .2, .02], [0, 0, -.065], "#1f9d55")]),
    part("indoor", "inner", "i_sens", "Airflow / PM sensor", "Checks filter clogging and room air.",
         [B([.15, .15, .03], [.75, 0, -.045], "#ffb347")]),

    # ================= AQI MONITOR (8" x 8" x 1.5") =================
    part("monitor", "outer", "m_house", "Casing", "Slim black body, small enough for a desk or wall.",
         [B([.8, .8, .15], [0, 0, 0], "#161b21")]),
    part("monitor", "outer", "m_screen", "AQI screen", "Shows the AQI (34, Good), PM2.5 in µg/m³, temperature and humidity.",
         [B([.72, .72, .01], [0, 0, .08], "#14191f", tex=MONITOR_FACE)]),
    part("monitor", "outer", "m_back", "Mounting plate", "Back plate for wall mounting or a desk stand.",
         [B([.5, .5, .03], [0, 0, -.09], "#6b7686")]),
    part("monitor", "inner", "m_mcu", "ESP32 board", "Receives readings from the indoor and outdoor units and draws the screen.",
         [B([.3, .3, .02], [-.15, .15, -.03], "#1f9d55")]),
    part("monitor", "inner", "m_pm", "PM2.5 sensor", "Measures dust around the monitor.",
         [B([.2, .15, .05], [.2, .2, -.02], "#ffb347")]),
    part("monitor", "inner", "m_dht", "Temp / humidity sensor", "Provides the 26°C and 48% RH readout.",
         [B([.1, .12, .04], [.2, -.05, -.02], "#e8e8e8")]),
    part("monitor", "inner", "m_pwr", "USB-C power board", "Charges the battery.",
         [B([.2, .08, .04], [-.2, -.05, -.03], "#d94f4f")]),
    part("monitor", "inner", "m_bat", "Li-ion battery", "Lets the monitor run without a cable.",
         [B([.5, .2, .04], [0, -.25, -.03], "#2f6bd9")]),
]

# ================= REALISTIC INSIDE PARTS =================
# Replaces the simple inner blocks above with detailed models.
# ex = how far (units of 10 in) a part slides forward/back in the Inside view, so every layer is visible.
PARTS = [p for p in PARTS if p["side"] != "inner"]
SIL, GOLD = "#cfd5dd", "#d4af37"


def M(t, s, p, c, **k):
    d = dict(t=t, s=s, p=p, c=c)
    d.update(k)
    return d


def fan(cx, cy, cz, rad, n=7, col="#4a5568"):
    ms = [M("box", [rad * 2.3, rad * 2.3, .01], [cx, cy, cz - .012], "#1b2028", m=.4, g=.6),
          M("tor", [rad * 1.02, rad * .07], [cx, cy, cz], "#2a303a", m=.5, g=.4),
          M("cyl", [rad * .24, rad * .3], [cx, cy, cz], SIL, r=[HALF, 0, 0], m=.6, g=.3)]
    for i in range(n):
        a = i * 6.2832 / n
        ms.append(M("box", [rad * .72, rad * .22, .006], [cx + math.cos(a) * rad * .55, cy + math.sin(a) * rad * .55, cz],
                    col, r=[.5, 0, a], m=.3, g=.5))
    return ms


def pcb(cx, cy, cz, w, h, col="#1f9d55"):
    ms = [M("box", [w, h, .012], [cx, cy, cz], col, m=.2, g=.45)]
    for i in range(3):
        ms.append(M("box", [w * .22, h * .18, .01], [cx - w * .28 + i * w * .28, cy + h * .15, cz + .011], "#14171c", m=.3, g=.5))
    for i in range(8):
        ms.append(M("box", [w * .05, h * .06, .004], [cx - w * .4 + i * w * .115, cy - h * .32, cz + .008], GOLD, m=.6, g=.3))
    ms.append(M("cyl", [w * .035, .02], [cx + w * .32, cy - h * .05, cz + .016], SIL, r=[HALF, 0, 0], m=.6, g=.3))
    return ms


def esp(cx, cy, cz, w, h):
    ms = [M("box", [w, h, .012], [cx, cy, cz], "#15181f", m=.2, g=.4),
          M("box", [w * .5, h * .28, .014], [cx - w * .12, cy + h * .2, cz + .012], SIL, m=.6, g=.35),
          M("box", [w * .22, h * .2, .01], [cx - w * .05, cy - h * .15, cz + .011], "#2b2f38", m=.3, g=.5),
          M("box", [w * .2, h * .12, .014], [cx + w * .05, cy - h * .5, cz + .01], SIL, m=.6, g=.3)]
    for i in range(4):
        ms.append(M("box", [w * .2, .008, .004], [cx + w * .32, cy + h * .42 - i * h * .07, cz + .008], GOLD, m=.6, g=.3))
    for sd in (-1, 1):
        ms.append(M("box", [.012, h * .92, .012], [cx + sd * w * .46, cy, cz + .011], "#0c0d10", g=.6))
        for i in range(10):
            ms.append(M("box", [.007, .007, .006], [cx + sd * w * .46, cy - h * .4 + i * h * .088, cz + .018], GOLD, m=.6, g=.3))
    return ms


def cells(cx, cy, cz, n, length):
    ms = [M("box", [length + .04, n * .09 + .02, .08], [cx, cy, cz - .01], "#1b1e24", g=.6)]
    for i in range(n):
        y = cy + (i - (n - 1) / 2) * .09
        ms.append(M("cyl", [.04, length], [cx, y, cz], "#2f6bd9", r=[0, 0, HALF], m=.3, g=.4))
        ms.append(M("cyl", [.018, .02], [cx + length / 2 + .01, y, cz], SIL, r=[0, 0, HALF], m=.6, g=.3))
        ms.append(M("cyl", [.041, length * .3], [cx - length * .15, y, cz], "#f2f2f2", r=[0, 0, HALF], g=.7))
    return ms


def frame(cx, cy, cz, w, h, d, col="#cfd6de"):
    return [M("box", [w, .03, d + .006], [cx, cy + h / 2, cz], col, m=.4, g=.5),
            M("box", [w, .03, d + .006], [cx, cy - h / 2, cz], col, m=.4, g=.5),
            M("box", [.03, h, d + .006], [cx - w / 2, cy, cz], col, m=.4, g=.5),
            M("box", [.03, h, d + .006], [cx + w / 2, cy, cz], col, m=.4, g=.5)]


def hepa_f(cx, cy, cz, w, h, d):
    ms = frame(cx, cy, cz, w, h, d)
    for i in range(18):
        ms.append(M("box", [.012, h - .04, d], [cx - w / 2 + .05 + i * (w - .1) / 17, cy, cz], "#f7f6f1",
                    r=[0, .5 if i % 2 else -.5, 0], g=.95))
    return ms


def mesh_f(cx, cy, cz, w, h):
    ms = frame(cx, cy, cz, w, h, .02, "#8a93a0")
    for i in range(1, 9):
        ms.append(M("box", [w, .004, .006], [cx, cy - h / 2 + i * h / 9, cz], "#b8c0cc", m=.5, g=.4))
    for i in range(1, 24):
        ms.append(M("box", [.004, h, .006], [cx - w / 2 + i * w / 24, cy, cz], "#b8c0cc", m=.5, g=.4))
    return ms


def honey(cx, cy, cz, w, h):
    ms = [M("box", [w, h, .018], [cx, cy, cz], "#14171c", g=.9)]
    rad = min(w / 30, h / 12)
    for i in range(14):
        for j in range(5):
            ms.append(M("cyl", [rad, .022], [cx - w / 2 + .06 + i * (w - .12) / 13, cy - h / 2 + .06 + j * (h - .12) / 4, cz],
                        "#2f343d" if (i + j) % 2 else "#222730", r=[HALF, 0, 0], g=.9))
    return ms


def sensor(cx, cy, cz, w, h, d, col="#ffb347"):
    return [M("box", [w, h, d], [cx, cy, cz], "#20242b", m=.3, g=.5),
            M("box", [w * .8, h * .8, .004], [cx, cy, cz + d / 2 + .002], SIL, m=.6, g=.35),
            M("box", [w * .5, h * .25, .004], [cx, cy + h * .15, cz + d / 2 + .005], col, g=.6),
            M("cyl", [w * .1, h * .3], [cx - w * .22, cy + h * .55, cz], "#0d0f12", g=.6),
            M("cyl", [w * .1, h * .3], [cx + w * .22, cy + h * .55, cz], "#0d0f12", g=.6)]


PARTS += [
    # ---- outdoor ----
    part("outdoor", "inner", "o_filt", "Intake dust filter", "Coarse mesh behind the intake slots that blocks leaves, insects and debris.", mesh_f(-.1, -.45, .3, 1.4, .6), .35),
    part("outdoor", "inner", "o_fan", "Intake fan", "Seven-blade fan that pulls a steady stream of outdoor air across the sensors and into the duct.", fan(-.1, -.45, .1, .3), .15),
    part("outdoor", "inner", "o_pm", "PM2.5 / PM10 sensor", "Laser particle counter in a metal-lidded housing with twin air tubes.", sensor(-.6, -.45, -.1, .3, .25, .15), -.05),
    part("outdoor", "inner", "o_gas", "Gas sensor", "Measures CO₂, NO₂ and other pollutants through a metal mesh cap.",
         sensor(-.2, -.45, -.15, .25, .2, .1, "#4aa3ff") + [M("cyl", [.07, .06], [-.2, -.45, -.07], SIL, r=[HALF, 0, 0], m=.6, g=.35)], -.05),
    part("outdoor", "inner", "o_air", "Air duct", "Ribbed channel that carries sampled air from the fan to the outlet fins.",
         [M("cyl", [.12, .9], [.5, -.1, 0], "#5b7a9a", r=[0, 0, HALF], m=.3, g=.4)] +
         [M("tor", [.125, .012], [.1 + i * .2, -.1, 0], "#9db4cc", r=[0, HALF, 0], m=.5, g=.4) for i in range(5)], 0),
    part("outdoor", "inner", "o_mcu", "ESP32 controller", "Dual-core Wi-Fi board with metal shield, antenna trace and gold header pins.", esp(-.5, .45, -.2, .55, .4), -.25),
    part("outdoor", "inner", "o_bat", "Battery pack", "Three 18650 lithium cells in a holder, so the unit keeps running in a power cut.", cells(.3, .45, -.2, 3, .55), -.25),
    part("outdoor", "inner", "o_chg", "Power / charge board", "Charges the battery and regulates power for the fan and electronics.", pcb(.5, -.45, -.25, .4, .3, "#b02e2e"), -.3),
    # ---- indoor ----
    part("indoor", "inner", "i_pre", "Pre-filter", "Fine washable mesh that catches hair, lint and large dust.", mesh_f(0, 0, .06, 1.55, .6), .9),
    part("indoor", "inner", "i_hepa", "HEPA filter", "Pleated glass-fibre filter that traps 99.97% of particles down to 0.3 µm, including PM2.5.", hepa_f(0, 0, .025, 1.5, .55, .04), .55),
    part("indoor", "inner", "i_carb", "Carbon layer", "Honeycomb of activated charcoal that absorbs odours and VOCs.", honey(0, 0, -.01, 1.45, .5), .2),
    part("indoor", "inner", "i_fan", "Blower fans", "Two seven-blade fans move air through the filters and back into the room.", fan(-.4, 0, -.04, .2) + fan(.4, 0, -.04, .2), -.2),
    part("indoor", "inner", "i_mcu", "ESP32 controller", "Drives the fans and the airflow light, and pairs with the outdoor unit and monitor.", esp(0, 0, -.065, .3, .2), -.5),
    part("indoor", "inner", "i_sens", "Airflow / PM sensor", "Checks filter clogging and room air quality.", sensor(.75, 0, -.045, .15, .15, .03), -.5),
    # ---- monitor ----
    part("monitor", "inner", "m_mcu", "ESP32 board", "Receives readings from the indoor and outdoor units and draws the screen.", esp(-.15, .15, -.03, .3, .3), -.1),
    part("monitor", "inner", "m_pm", "PM2.5 sensor", "Measures dust around the monitor.", sensor(.2, .2, -.02, .2, .15, .05), .12),
    part("monitor", "inner", "m_dht", "Temp / humidity sensor", "Provides the 26°C and 48% RH readout.",
         [M("box", [.1, .12, .04], [.2, -.05, -.02], "#e8e8e8", g=.6)] +
         [M("box", [.012, .012, .004], [.17 + i * .03, -.02 - j * .03, .001], "#2a2d33", g=.8) for i in range(3) for j in range(3)], .06),
    part("monitor", "inner", "m_pwr", "USB-C power board", "Charges the battery.",
         pcb(-.2, -.05, -.03, .2, .08, "#b02e2e") + [M("box", [.07, .03, .02], [-.2, -.1, -.03], SIL, m=.6, g=.3)], -.18),
    part("monitor", "inner", "m_bat", "Li-ion battery", "Flat lithium-polymer pouch with protection board and wires.",
         [M("box", [.5, .2, .04], [0, -.25, -.03], "#2f6bd9", m=.2, g=.4), M("box", [.3, .08, .004], [0, -.25, -.008], "#f2f2f2", g=.7),
          M("box", [.4, .004, .004], [0, -.15, -.03], "#d33", g=.6), M("box", [.4, .004, .004], [0, -.145, -.03], "#111", g=.6)], -.1),
]

DEVICES = [
    dict(id="system", name="System", dist=9.5,
         intro="The three parts work together: the outdoor unit samples outside air, the indoor panel cleans room air, and the AQI monitor shows both."),
    dict(id="outdoor", name="Outdoor unit", dist=6.2,
         intro="18″ H × 18″ W × 8″ D. Samples outside air and sends it through the side duct toward the indoor panel."),
    dict(id="indoor", name="Indoor panel", dist=5.2,
         intro="8″ H × 18″ W × 1.5″ D. Slim wall panel that filters room air through slats."),
    dict(id="monitor", name="AQI monitor", dist=3.2,
         intro="8″ H × 8″ W × 1.5″ D. Digital display of AQI, PM2.5, temperature and humidity."),
]

# where each device sits in the System tab (units of 10 in)
SYS_POS = dict(outdoor=[-1.5, 0, 0], indoor=[1.3, .75, 0], monitor=[.9, -.65, 0])

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__ – 3D Model</title>
<style>
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#071426;color:#e8eefc;font-family:system-ui,Segoe UI,sans-serif;overflow:hidden}
canvas{position:fixed;inset:0;width:100%;height:100%;display:block}
.head{position:fixed;top:20px;left:28px;pointer-events:none}
.head h1{margin:0;font-size:30px}.head p{margin:4px 0 0;color:#b9c6e4}
.hint{position:fixed;top:24px;right:28px;text-align:right;color:#b9c6e4;font-size:14px;pointer-events:none}
.panel{position:fixed;right:20px;top:90px;bottom:90px;width:330px;background:#0d1d38ee;border:1px solid #28406e;border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:10px}
.tabs{display:flex;gap:6px}
button{font:inherit;color:#e8eefc;background:#0d1d38;border:1px solid #28406e;border-radius:8px;padding:9px 12px;cursor:pointer}
button:hover{border-color:#5b8cff}button:focus-visible{outline:2px solid #fff}
button.on{background:#2f6bff;border-color:#2f6bff}
.tabs button{flex:1;padding:9px 2px;font-size:13px}
#list{overflow:auto;flex:1}
#list h3{margin:10px 4px 4px;font-size:14px;color:#9db4ee}
#list button{display:block;width:100%;text-align:left;border:0;background:none;padding:7px 10px}
#list button.on{background:#2f6bff33}
#info{border-top:1px solid #28406e;padding-top:10px;font-size:14px;line-height:1.45;min-height:92px}
#info b{display:block;font-size:15px;margin-bottom:2px}
.bar{position:fixed;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.grp{display:flex;gap:4px;padding:6px;background:#0d1d38ee;border:1px solid #28406e;border-radius:12px}
.grp button{border:0}
@media(max-width:800px){.panel{top:auto;height:42%;bottom:70px;left:10px;right:10px;width:auto}.hint{display:none}}
</style></head><body>
<canvas id="c"></canvas>
<div class="head"><h1>__TITLE__</h1><p>__SUBTITLE__</p><p>__DESIGNER__</p></div>
<div class="hint">Drag to rotate · scroll to zoom<br>Click a part to learn about it</div>
<div class="panel">
  <div class="tabs" id="devtabs"></div>
  <div class="tabs" id="modetabs"><button data-m="outside" class="on">Outside</button><button data-m="inside">Inside</button></div>
  <div id="list"></div>
  <div id="info"></div>
</div>
<div class="bar">
  <div class="grp" id="views"><button data-v="0,0">Front</button><button data-v="1.571,0">Right</button><button data-v="3.142,0">Back</button><button data-v="-1.571,0">Left</button><button data-v="0,1.4">Top</button></div>
  <div class="grp"><button id="rot" class="on">Auto-rotate</button><button id="zi">+</button><button id="zo">−</button></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
const P=__PARTS__, D=__DEVICES__, SP=__SYSPOS__;
const cv=document.getElementById('c');
const R=new THREE.WebGLRenderer({canvas:cv,antialias:true});R.setPixelRatio(devicePixelRatio);
const S=new THREE.Scene();const cam=new THREE.PerspectiveCamera(40,1,.1,60);
S.add(new THREE.HemisphereLight(0xffffff,0x223355,.95));
const dl=new THREE.DirectionalLight(0xffffff,.9);dl.position.set(3,4,5);S.add(dl);
const dl2=new THREE.DirectionalLight(0x9db4ff,.6);dl2.position.set(-4,2,-3);S.add(dl2);
const root=new THREE.Group();S.add(root);
function tex(t){const k=document.createElement('canvas');k.width=t.w;k.height=t.h;const x=k.getContext('2d');
  x.fillStyle=t.bg;x.fillRect(0,0,t.w,t.h);
  t.items.forEach(i=>{if(i.r){x.fillStyle=i.c;x.fillRect(...i.r);return}
    x.font=(i.b?'bold ':'')+i.f+'px sans-serif';x.fillStyle=i.c;x.textAlign=i.a;x.fillText(i.s,i.x,i.y)});
  const tt=new THREE.CanvasTexture(k);tt.anisotropy=8;return tt}
const devG={};['outdoor','indoor','monitor'].forEach(d=>{devG[d]=new THREE.Group();root.add(devG[d])});
const objs=[];
P.forEach(p=>{
  const g=new THREE.Group();g.userData=p;
  p.meshes.forEach(m=>{
    const geo=m.t=='box'?new THREE.BoxGeometry(...m.s):m.t=='tor'?new THREE.TorusGeometry(m.s[0],m.s[1],12,40):new THREE.CylinderGeometry(m.s[0],m.s[0],m.s[1],28);
    const mat=new THREE.MeshStandardMaterial({color:m.tex?'#ffffff':m.c,transparent:true,roughness:m.g??.55,metalness:m.m??.1});
    if(m.tex)mat.map=tex(m.tex);
    mat.emissive=new THREE.Color(m.e||'#000');mat.userData.e=m.e||'#000';
    const me=new THREE.Mesh(geo,mat);me.position.set(...m.p);if(m.r)me.rotation.set(...m.r);g.add(me);
  });
  devG[p.dev].add(g);objs.push(g);
});
let dev='system',mode='outside',sel=null,yaw=.5,pit=.15,dist=9.5,auto=true;
const info=document.getElementById('info');
function applyMode(){
  const sys=dev=='system';
  objs.forEach(g=>{
    const p=g.userData,o=p.side=='outer';
    g.visible=sys?o:(p.dev==dev&&(mode=='inside'||o));
    const op=(!sys&&mode=='inside'&&o)?.08:1;
    g.traverse(n=>{if(n.material){n.material.opacity=op;n.material.depthWrite=op==1;}});
  });
  for(const d in devG)devG[d].position.set(...(sys?SP[d]:[0,0,0]));
  document.getElementById('modetabs').style.display=sys?'none':'flex';
  document.querySelectorAll('[data-m]').forEach(b=>b.classList.toggle('on',b.dataset.m==mode));
  document.querySelectorAll('[data-d]').forEach(b=>b.classList.toggle('on',b.dataset.d==dev));
  buildList();
}
function addBtn(L,p){const b=document.createElement('button');b.textContent=p.name;b.dataset.id=p.id;
  b.className=sel==p.id?'on':'';b.onclick=()=>select(p.id);L.appendChild(b)}
function heading(L,t){const h=document.createElement('h3');h.textContent=t;L.appendChild(h)}
function buildList(){
  const L=document.getElementById('list');L.innerHTML='';
  if(dev=='system'){D.filter(d=>d.id!='system').forEach(d=>{heading(L,d.name);P.filter(p=>p.dev==d.id&&p.side=='outer').forEach(p=>addBtn(L,p))});return}
  heading(L,mode=='outside'?'Outer parts':'Inner parts');
  P.filter(p=>p.dev==dev&&(mode=='inside'?p.side=='inner':p.side=='outer')).forEach(p=>addBtn(L,p));
}
function clearSel(){sel=null;objs.forEach(g=>g.traverse(n=>{if(n.material)n.material.emissive.set(n.material.userData.e)}))}
function intro(){const d=D.find(x=>x.id==dev);info.innerHTML='<b>'+d.name+'</b>'+d.intro}
function select(id){
  sel=id;const p=P.find(x=>x.id==id);
  objs.forEach(g=>g.traverse(n=>{if(n.material)n.material.emissive.set(g.userData.id==id?'#ffffff':n.material.userData.e)}));
  info.innerHTML='<b>'+p.name+'</b>'+p.desc;
  document.querySelectorAll('#list button').forEach(b=>b.classList.toggle('on',b.dataset.id==id));
}
const dt=document.getElementById('devtabs');
D.forEach(d=>{const b=document.createElement('button');b.textContent=d.name;b.dataset.d=d.id;
  b.onclick=()=>{dev=d.id;dist=d.dist*(mode=='inside'?.75:1);clearSel();applyMode();intro()};dt.appendChild(b)});
document.querySelectorAll('[data-m]').forEach(b=>b.onclick=()=>{mode=b.dataset.m;dist=D.find(x=>x.id==dev).dist*(mode=='inside'&&dev!='system'?.75:1);clearSel();applyMode();intro()});
document.querySelectorAll('#views button').forEach(b=>b.onclick=()=>{const[v,w]=b.dataset.v.split(',').map(Number);yaw=v;pit=w;auto=false;rot.classList.remove('on');});
const rot=document.getElementById('rot');
rot.onclick=()=>{auto=!auto;rot.classList.toggle('on',auto)};
zi.onclick=()=>dist=Math.max(1.5,dist*.8);zo.onclick=()=>dist=Math.min(18,dist*1.25);
let down=null,moved=0;
cv.onpointerdown=e=>{down=[e.clientX,e.clientY];moved=0;cv.setPointerCapture(e.pointerId)};
cv.onpointermove=e=>{if(!down)return;const dx=e.clientX-down[0],dy=e.clientY-down[1];moved+=Math.abs(dx)+Math.abs(dy);
  yaw-=dx*.008;pit=Math.max(-1.4,Math.min(1.4,pit+dy*.006));down=[e.clientX,e.clientY];auto=false;rot.classList.remove('on')};
cv.onpointerup=e=>{down=null;if(moved<5){
  const rc=new THREE.Raycaster();rc.setFromCamera(new THREE.Vector2(e.clientX/innerWidth*2-1,-(e.clientY/innerHeight)*2+1),cam);
  const hit=rc.intersectObjects(objs.filter(g=>g.visible),true).find(h=>h.object.material.opacity>.5);
  if(hit){let g=hit.object;while(!g.userData.id)g=g.parent;select(g.userData.id);}
}};
cv.addEventListener('wheel',e=>{e.preventDefault();dist=Math.max(1.5,Math.min(18,dist*(1+e.deltaY*.001)))},{passive:false});
function size(){R.setSize(innerWidth,innerHeight);cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix()}
addEventListener('resize',size);size();
(function loop(){
  requestAnimationFrame(loop);
  if(auto)yaw+=.004;
  objs.forEach(g=>{const t=(dev!='system'&&mode=='inside')?g.userData.ex||0:0;g.position.z+=(t-g.position.z)*.1});
  cam.position.set(dist*Math.sin(yaw)*Math.cos(pit),dist*Math.sin(pit),dist*Math.cos(yaw)*Math.cos(pit));
  cam.lookAt(0,0,0);R.render(S,cam);
})();
applyMode();intro();
</script></body></html>"""

html = (TEMPLATE.replace("__PARTS__", json.dumps(PARTS)).replace("__DEVICES__", json.dumps(DEVICES))
        .replace("__SYSPOS__", json.dumps(SYS_POS))
        .replace("__TITLE__", TITLE).replace("__SUBTITLE__", SUBTITLE).replace("__DESIGNER__", DESIGNER))
out = Path(__file__).with_name("airwall_v2_3d.html")
out.write_text(html, encoding="utf-8")
print("Created", out)
