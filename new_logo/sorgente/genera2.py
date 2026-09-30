"""Tre proposte rifinite per il logo Studio Dentistico Annicchiarico.

Uso: python3 genera2.py  -> scrive in new_logo/rifiniti/
Testo convertito in tracciati con fontTools (Piazzolla + IBM Plex Sans, gli stessi del sito).
"""
import math, os
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "rifiniti")
FONTS = os.path.join(os.path.dirname(HERE), "..", "fonts")
os.makedirs(OUT, exist_ok=True)

INK = "#0F2A2E"; TEAL = "#4CB0B8"; TEAL_DARK = "#39868D"; TEAL_TEXT = "#256B72"
MINT = "#5FE3B8"; PAPER = "#FFFFFF"; SEA = "#EAF4F3"
TITLE = "Studio Dentistico Annicchiarico"
_cache = {}

def font(name, wght, opsz=None):
    key = (name, wght, opsz)
    if key not in _cache:
        f = TTFont(os.path.join(FONTS, name))
        axes = {"wght": wght}
        if opsz is not None: axes["opsz"] = opsz
        f = instancer.instantiateVariableFont(f, axes)
        _cache[key] = (f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _cache[key]

PLEX = "ibm-plex-sans-latin.woff2"; PIAZ = "piazzolla-latin.woff2"
fmt = lambda v: ("%.2f" % v).rstrip("0").rstrip(".")

def text(fs, s, size, x, y, tracking=0.0, anchor="start"):
    f, gs, cmap, hmtx, upm = fs
    sc = size / upm
    adv = [(cmap[ord(ch)], hmtx[cmap[ord(ch)]][0] * sc) for ch in s]
    tr = tracking * size
    width = sum(a for _, a in adv) + tr * (len(s) - 1)
    if anchor == "middle": x -= width / 2
    elif anchor == "end": x -= width
    pen = SVGPathPen(gs, ntos=fmt); cx = x
    for g, a in adv:
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, cx, y))); cx += a + tr
    return pen.getCommands(), width

def measure(fs, s, size, tracking=0.0):
    return text(fs, s, size, 0, 0, tracking)[1]

def arc_text(fs, s, size, cx, cy, R, tracking=0.0, bottom=False):
    """Testo lungo un arco centrato in alto (o in basso, leggibile) di un cerchio."""
    f, gs, cmap, hmtx, upm = fs
    sc = size / upm
    adv = [(cmap[ord(ch)], hmtx[cmap[ord(ch)]][0] * sc) for ch in s]
    tr = tracking * size
    total = sum(a for _, a in adv) + tr * (len(s) - 1)
    span = total / R
    pen = SVGPathPen(gs, ntos=fmt)
    pos = 0.0
    for g, a in adv:
        mid = pos + a / 2
        if not bottom:
            th = -span / 2 + mid / R
            px, py = cx + R * math.sin(th), cy - R * math.cos(th)
            rot = th
        else:
            th = math.pi + span / 2 - mid / R
            px, py = cx + R * math.sin(th), cy - R * math.cos(th)
            rot = th + math.pi
        t = Transform().translate(px, py).rotate(rot).translate(-a / 2, 0).scale(sc, -sc)
        gs[g].draw(TransformPen(pen, t))
        pos += a + tr
    return pen.getCommands()

# molare in un riquadro 100 x 116, contorni più morbidi del precedente
TOOTH = ("M50 22C45 10 33 4 22 8C9 13 5 30 9 46C12 58 17 66 19 78C21 92 23 106 30 110"
         "C37 114 40 102 42 92C44 82 47 76 50 76C53 76 56 82 58 92C60 102 63 114 70 110"
         "C77 106 79 92 81 78C83 66 88 58 91 46C95 30 91 13 78 8C67 4 55 10 50 22Z")

def tooth(x, y, h, fill=None, stroke=None, sw=0):
    s = h / 116
    a = 'fill="%s"' % fill if fill else 'fill="none"'
    if stroke: a += ' stroke="%s" stroke-width="%.3f" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw / s)
    return '<path transform="translate(%.2f %.2f) scale(%.4f)" d="%s" %s/>' % (x, y, s, TOOTH, a)

def svg(w, h, body, bg=None):
    rect = '<rect width="%.0f" height="%.0f" fill="%s"/>' % (w, h, bg) if bg else ""
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" role="img" aria-label="%s">\n'
            '<title>%s</title>\n%s\n%s\n</svg>\n' % (w, h, w, h, TITLE, TITLE, rect, body))

p = lambda d, fill: '<path fill="%s" d="%s"/>' % (fill, d)
def write(name, content):
    open(os.path.join(OUT, name), "w").write(content); print("scritto", name)

# ---------- A. Sigillo C: evoluzione del marchio attuale ----------
def mark_a(ox, oy, size, arc=TEAL, disc=INK, toothc=PAPER):
    sw = size * 0.10
    r = size / 2 - sw / 2
    cx, cy = ox + size / 2, oy + size / 2
    a = math.radians(46)
    x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
    x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
    ri = size * 0.29
    th = ri * 1.3; tw = th * 100 / 116
    return ('<path d="M%.2f %.2fA%.2f %.2f 0 1 0 %.2f %.2f" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round"/>'
            % (x1, y1, r, r, x2, y2, arc, sw)
            + '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, ri, disc)
            + tooth(cx - tw / 2, cy - th / 2, th, fill=toothc))

def a_horizontal(dark=False):
    piaz = font(PIAZ, 500, 72); plex = font(PLEX, 500)
    name_c = PAPER if dark else INK; tag_c = MINT if dark else TEAL_TEXT
    m, pad = 176, 32
    tx = pad + m + 40
    d_tag, w_tag = text(plex, "STUDIO DENTISTICO", 21, tx + 2, pad + 60, tracking=0.32)
    d_name, w_name = text(piaz, "Annicchiarico", 86, tx, pad + 136)
    W = tx + max(w_tag, w_name) + pad; H = m + pad * 2
    body = mark_a(pad, pad, m, TEAL, PAPER if dark else INK, INK if dark else PAPER) + p(d_tag, tag_c) + p(d_name, name_c)
    return svg(W, H, body, bg=INK if dark else None)

def a_vertical():
    piaz = font(PIAZ, 500, 72); plex = font(PLEX, 500)
    m, pad = 200, 36
    w_name = measure(piaz, "Annicchiarico", 74); w_tag = measure(plex, "STUDIO DENTISTICO", 20, 0.34)
    W = max(w_name, w_tag, m) + pad * 2; cx = W / 2
    d_name, _ = text(piaz, "Annicchiarico", 74, cx, pad + m + 92, anchor="middle")
    d_tag, _ = text(plex, "STUDIO DENTISTICO", 20, cx, pad + m + 130, 0.34, "middle")
    H = pad + m + 130 + pad
    return svg(W, H, mark_a(cx - m / 2, pad, m) + p(d_name, INK) + p(d_tag, TEAL_TEXT))

def a_mark():
    return svg(256, 256, mark_a(16, 16, 224))

# ---------- B. Monolinea: dente a contorno, nome in serif ----------
def mark_b(x, y, h, stroke=INK, dot=MINT):
    tw = h * 100 / 116
    s = h / 116
    return (tooth(x, y, h, stroke=stroke, sw=h * 0.075)
            + '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (x + 66 * s, y + 34 * s, 6.5 * s, dot))

def b_horizontal(dark=False):
    piaz = font(PIAZ, 500, 72); plex = font(PLEX, 500)
    name_c = PAPER if dark else INK; tag_c = MINT if dark else TEAL_TEXT
    th, pad = 168, 34
    tw = th * 100 / 116
    tx = pad + tw + 44
    d_name, w_name = text(piaz, "Annicchiarico", 92, tx, pad + 104)
    d_tag, w_tag = text(plex, "STUDIO DENTISTICO", 21, tx + 3, pad + 148, tracking=0.34)
    W = tx + max(w_name, w_tag) + pad; H = th + pad * 2
    body = mark_b(pad, pad + 2, th, PAPER if dark else INK, MINT) + p(d_name, name_c) + p(d_tag, tag_c)
    return svg(W, H, body, bg=INK if dark else None)

def b_oneline():
    piaz = font(PIAZ, 500, 36); plex = font(PLEX, 400)
    th, pad = 84, 22
    tw = th * 100 / 116
    tx = pad + tw + 26; base = pad + th * 0.66
    d1, w1 = text(plex, "Studio Dentistico ", 40, tx, base)
    d2, w2 = text(piaz, "Annicchiarico", 46, tx + w1, base)
    W = tx + w1 + w2 + pad; H = th + pad * 2
    return svg(W, H, mark_b(pad, pad, th) + p(d1, TEAL_TEXT) + p(d2, INK))

def b_mark():
    return svg(256, 256, '<rect width="256" height="256" rx="60" fill="%s"/>' % INK + mark_b(60, 48, 160, PAPER, MINT))

# ---------- C. Sigillo rotondo: testo ad arco, dente al centro ----------
def seal(cx, cy, R, ink=INK, accent=MINT, paper=None):
    plex = font(PLEX, 500)
    out = '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (cx, cy, R, ink, R * 0.028)
    out += '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="none" stroke="%s" stroke-width="%.2f"/>' % (cx, cy, R * 0.70, ink, R * 0.012)
    size = R * 0.135
    out += p(arc_text(plex, "STUDIO DENTISTICO", size, cx, cy, R * 0.84, tracking=0.3), ink)
    out += p(arc_text(plex, "GROTTAGLIE", size, cx, cy, R * 0.84, tracking=0.3, bottom=True), ink)
    for sx in (-1, 1):
        out += '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx + sx * R * 0.845, cy, R * 0.032, accent)
    th = R * 0.78; tw = th * 100 / 116
    out += tooth(cx - tw / 2, cy - th / 2 + R * 0.01, th, fill=ink)
    return out

def c_horizontal(dark=False):
    piaz = font(PIAZ, 500, 72); plex = font(PLEX, 500)
    ink = PAPER if dark else INK; tag_c = MINT if dark else TEAL_TEXT
    R, pad = 100, 32
    tx = pad + 2 * R + 44
    d_name, w_name = text(piaz, "Annicchiarico", 86, tx, pad + 112)
    d_tag, w_tag = text(plex, "STUDIO DENTISTICO", 21, tx + 3, pad + 154, tracking=0.34)
    W = tx + max(w_name, w_tag) + pad; H = 2 * R + pad * 2
    body = seal(pad + R, pad + R, R, ink, MINT) + p(d_name, ink) + p(d_tag, tag_c)
    return svg(W, H, body, bg=INK if dark else None)

def c_mark():
    return svg(256, 256, seal(128, 128, 116))

def c_vertical():
    piaz = font(PIAZ, 500, 72)
    R, pad = 110, 36
    w_name = measure(piaz, "Annicchiarico", 72)
    W = max(w_name, 2 * R) + pad * 2; cx = W / 2
    d_name, _ = text(piaz, "Annicchiarico", 72, cx, pad + 2 * R + 84, anchor="middle")
    H = pad + 2 * R + 84 + pad
    return svg(W, H, seal(cx, pad + R, R) + p(d_name, INK))

if __name__ == "__main__":
    write("A-sigillo-c-orizzontale.svg", a_horizontal())
    write("A-sigillo-c-negativo.svg", a_horizontal(dark=True))
    write("A-sigillo-c-verticale.svg", a_vertical())
    write("A-sigillo-c-marchio.svg", a_mark())
    write("B-monolinea-orizzontale.svg", b_horizontal())
    write("B-monolinea-negativo.svg", b_horizontal(dark=True))
    write("B-monolinea-una-riga.svg", b_oneline())
    write("B-monolinea-icona.svg", b_mark())
    write("C-sigillo-rotondo-orizzontale.svg", c_horizontal())
    write("C-sigillo-rotondo-negativo.svg", c_horizontal(dark=True))
    write("C-sigillo-rotondo-verticale.svg", c_vertical())
    write("C-sigillo-rotondo-marchio.svg", c_mark())
