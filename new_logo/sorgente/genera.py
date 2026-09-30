"""Genera le varianti del logo Studio Dentistico Annicchiarico.

Uso: python3 genera.py  (scrive gli SVG nella cartella new_logo/)
Il testo è convertito in tracciati: gli SVG non dipendono da font installati.
Font: IBM Plex Sans e Piazzolla (licenza SIL OFL), gli stessi del sito.
"""

import math
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
FONTS = os.path.join(OUT, "..", "fonts")

TEAL = "#4CB0B8"
TEAL_DARK = "#39868D"
TEAL_DEEP = "#17393C"
TEAL_TEXT = "#2B6A70"
NAVY = "#1D3557"
MINT = "#6CC5B0"
MINT_DARK = "#2F8F7C"
WHITE = "#FFFFFF"

_cache = {}


def font(name, wght, opsz=None):
    key = (name, wght, opsz)
    if key not in _cache:
        f = TTFont(os.path.join(FONTS, name))
        axes = {"wght": wght}
        if opsz is not None:
            axes["opsz"] = opsz
        f = instancer.instantiateVariableFont(f, axes)
        _cache[key] = (f, f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)
    return _cache[key]


PLEX = "ibm-plex-sans-latin.woff2"
PIAZ = "piazzolla-latin.woff2"


def text(fontspec, s, size, x, y, tracking=0.0, anchor="start"):
    """Restituisce (path_d, larghezza). y è la baseline. tracking in em."""
    f, gs, cmap, hmtx, upm = fontspec
    scale = size / upm
    advances = []
    for ch in s:
        g = cmap[ord(ch)]
        advances.append((g, hmtx[g][0] * scale))
    track = tracking * size
    width = sum(a for _, a in advances) + track * (len(s) - 1)
    if anchor == "middle":
        x -= width / 2
    elif anchor == "end":
        x -= width
    pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
    cx = x
    for g, adv in advances:
        tp = TransformPen(pen, (scale, 0, 0, -scale, cx, y))
        gs[g].draw(tp)
        cx += adv + track
    return pen.getCommands(), width


def measure(fontspec, s, size, tracking=0.0):
    return text(fontspec, s, size, 0, 0, tracking)[1]


# Molare in un riquadro 100 x 112: due cuspidi, due radici.
TOOTH = (
    "M50 14C42 4 28 2 18 8C6 16 4 34 8 50C11 62 16 70 18 82"
    "C20 96 22 108 30 110C38 112 40 100 42 90C44 80 46 74 50 74"
    "C54 74 56 80 58 90C60 100 62 112 70 110C78 108 80 96 82 82"
    "C84 70 89 62 92 50C96 34 94 16 82 8C72 2 58 4 50 14Z"
)


def tooth(x, y, h, fill=None, stroke=None, sw=0):
    """Dente con angolo in alto a sinistra (x, y) e altezza h."""
    s = h / 112
    attrs = []
    if fill:
        attrs.append('fill="%s"' % fill)
    else:
        attrs.append('fill="none"')
    if stroke:
        attrs.append(
            'stroke="%s" stroke-width="%.3f" stroke-linejoin="round"'
            % (stroke, sw / s)
        )
    return '<path transform="translate(%.2f %.2f) scale(%.4f)" d="%s" %s/>' % (
        x, y, s, TOOTH, " ".join(attrs))


def sparkle(cx, cy, r, fill):
    k = r * 0.22
    return (
        '<path fill="%s" d="M%.2f %.2fQ%.2f %.2f %.2f %.2fQ%.2f %.2f %.2f %.2f'
        'Q%.2f %.2f %.2f %.2fQ%.2f %.2f %.2f %.2fZ"/>'
        % (fill,
           cx, cy - r, cx + k, cy - k, cx + r, cy,
           cx + k, cy + k, cx, cy + r,
           cx - k, cy + k, cx - r, cy,
           cx - k, cy - k, cx, cy - r)
    )


def c_arc(cx, cy, r, sw, color, gap_deg=48):
    a = math.radians(gap_deg)
    x1, y1 = cx + r * math.cos(a), cy - r * math.sin(a)
    x2, y2 = cx + r * math.cos(a), cy + r * math.sin(a)
    return (
        '<path d="M%.2f %.2fA%.2f %.2f 0 1 0 %.2f %.2f" fill="none" stroke="%s" '
        'stroke-width="%.2f" stroke-linecap="round"/>' % (x1, y1, r, r, x2, y2, color, sw)
    )


def svg(w, h, body, title, bg=None):
    rect = '<rect width="%.0f" height="%.0f" fill="%s"/>' % (w, h, bg) if bg else ""
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %.0f %.0f" width="%.0f" height="%.0f" '
        'role="img" aria-label="%s">\n<title>%s</title>\n%s\n%s\n</svg>\n'
        % (w, h, w, h, title, title, rect, body)
    )


def p(d, fill):
    return '<path fill="%s" d="%s"/>' % (fill, d)


def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content)
    print("scritto", name)


TITLE = "Studio Dentistico Annicchiarico"


# ---------- 01 C e dente: evoluzione del logo attuale ----------
def mark_c(ox, oy, size, arc, inner, toothc):
    """Marchio C + cerchio + dente. size = diametro esterno."""
    sw = size * 0.12
    r = size / 2 - sw / 2
    cx, cy = ox + size / 2, oy + size / 2
    ri = size * 0.30
    th = ri * 1.35
    tw = th * 100 / 112
    return (
        c_arc(cx, cy, r, sw, arc)
        + '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, ri, inner)
        + tooth(cx - tw / 2, cy - th / 2 - th * 0.02, th, fill=toothc)
    )


def v01(dark=False):
    plex_l, plex_m = font(PLEX, 300), font(PLEX, 500)
    txt = WHITE if dark else TEAL_DEEP
    sub = TEAL if dark else TEAL_TEXT
    m = 200
    pad = 30
    tx = pad + m + 44
    d1, w1 = text(plex_m, "ANNICCHIARICO", 64, tx, pad + 118, tracking=0.06)
    d2, w2 = text(plex_l, "STUDIO DENTISTICO", 30, tx, pad + 62, tracking=0.28)
    W = tx + max(w1, w2) + pad
    H = m + pad * 2
    body = (mark_c(pad, pad, m, TEAL, TEAL_DARK if not dark else TEAL, WHITE if not dark else TEAL_DEEP)
            + p(d2, sub) + p(d1, txt)
            + '<rect x="%.2f" y="%.2f" width="56" height="3" fill="%s"/>' % (tx, pad + 148, TEAL))
    return svg(W, H, body, TITLE, bg=TEAL_DEEP if dark else None)


def v01_vertical():
    plex_l, plex_m = font(PLEX, 300), font(PLEX, 500)
    m = 220
    pad = 30
    w1 = measure(plex_m, "ANNICCHIARICO", 58, 0.06)
    w2 = measure(plex_l, "STUDIO DENTISTICO", 26, 0.3)
    W = max(w1, w2, m) + pad * 2
    cx = W / 2
    d2, _ = text(plex_l, "STUDIO DENTISTICO", 26, cx, pad + m + 64, 0.3, "middle")
    d1, _ = text(plex_m, "ANNICCHIARICO", 58, cx, pad + m + 128, 0.06, "middle")
    H = pad + m + 128 + pad + 6
    body = mark_c(cx - m / 2, pad, m, TEAL, TEAL_DARK, WHITE) + p(d2, TEAL_TEXT) + p(d1, TEAL_DEEP)
    return svg(W, H, body, TITLE)


def v01_mark():
    m, pad = 240, 16
    return svg(m + pad * 2, m + pad * 2, mark_c(pad, pad, m, TEAL, TEAL_DARK, WHITE), TITLE)


# ---------- 02 Dente a linea con scintilla, serif ----------
def v02():
    piaz = font(PIAZ, 500, 30)
    plex = font(PLEX, 500)
    pad = 30
    th = 170
    tw = th * 100 / 112
    body = tooth(pad + 4, pad + 14, th, stroke=TEAL, sw=9)
    body += sparkle(pad + tw + 2, pad + 18, 20, TEAL_DARK)
    tx = pad + tw + 52
    d1, w1 = text(piaz, "Annicchiarico", 92, tx, pad + 128)
    d2, w2 = text(plex, "STUDIO DENTISTICO", 25, tx + 4, pad + 58, tracking=0.34)
    W = tx + max(w1, w2) + pad
    H = th + pad * 2 + 20
    body += p(d2, TEAL_TEXT) + p(d1, TEAL_DEEP)
    body += '<rect x="%.2f" y="%.2f" width="%.2f" height="2" fill="%s"/>' % (tx + 4, pad + 162, w1 - 4, TEAL)
    return svg(W, H, body, TITLE)


# ---------- 03 Monogramma: dente con la A ----------
def v03():
    piaz_b = font(PIAZ, 600, 30)
    piaz = font(PIAZ, 450, 30)
    plex = font(PLEX, 400)
    pad = 30
    th = 190
    tw = th * 100 / 112
    tx0, ty0 = pad, pad
    body = tooth(tx0, ty0, th, fill=TEAL_DEEP)
    da, _ = text(piaz_b, "A", 96, tx0 + tw / 2, ty0 + th * 0.56, anchor="middle")
    body += p(da, WHITE)
    body += '<circle cx="%.2f" cy="%.2f" r="7" fill="%s"/>' % (tx0 + tw * 0.76, ty0 + th * 0.2, TEAL)
    x = tx0 + tw + 44
    body += '<rect x="%.2f" y="%.2f" width="2" height="%.2f" fill="%s"/>' % (x, pad + 24, th - 48, TEAL)
    tx = x + 40
    d1, w1 = text(piaz, "Annicchiarico", 84, tx, pad + 124)
    d2, w2 = text(plex, "STUDIO DENTISTICO", 24, tx + 3, pad + 62, tracking=0.36)
    W = tx + max(w1, w2) + pad
    H = th + pad * 2
    body += p(d2, TEAL_TEXT) + p(d1, TEAL_DEEP)
    return svg(W, H, body, TITLE)


# ---------- 04 Sorriso: badge circolare, impaginazione verticale ----------
def badge_smile(cx, cy, r, bg, fg):
    th = r * 1.02
    tw = th * 100 / 112
    out = '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, r, bg)
    out += tooth(cx - tw / 2, cy - th * 0.62, th, fill=fg)
    sr = r * 0.62
    a = math.radians(32)
    y0 = cy + r * 0.22
    x1, y1 = cx - sr * math.sin(a), y0 + sr * (1 - math.cos(a)) * 0
    out += (
        '<path d="M%.2f %.2fQ%.2f %.2f %.2f %.2f" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round"/>'
        % (cx - r * 0.5, cy + r * 0.52, cx, cy + r * 0.84, cx + r * 0.5, cy + r * 0.52, fg, r * 0.07)
    )
    return out


def v04():
    plex_m = font(PLEX, 600)
    plex_l = font(PLEX, 400)
    pad = 34
    r = 110
    w1 = measure(plex_m, "ANNICCHIARICO", 54, 0.1)
    w2 = measure(plex_l, "STUDIO DENTISTICO", 24, 0.42)
    W = max(w1, w2, r * 2) + pad * 2
    cx = W / 2
    body = badge_smile(cx, pad + r, r, TEAL, WHITE)
    d1, _ = text(plex_m, "ANNICCHIARICO", 54, cx, pad + 2 * r + 86, 0.1, "middle")
    d2, _ = text(plex_l, "STUDIO DENTISTICO", 24, cx, pad + 2 * r + 132, 0.42, "middle")
    H = pad + 2 * r + 132 + pad
    body += p(d1, TEAL_DEEP) + p(d2, TEAL_TEXT)
    return svg(W, H, body, TITLE)


def v04_mark():
    r, pad = 120, 12
    return svg(2 * (r + pad), 2 * (r + pad), badge_smile(r + pad, r + pad, r, TEAL, WHITE), TITLE)


# ---------- 05 Blu e menta: tile arrotondato ----------
def tile(x, y, s):
    th = s * 0.66
    tw = th * 100 / 112
    out = '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>' % (x, y, s, s, s * 0.24, NAVY)
    tx, ty = x + (s - tw) / 2, y + (s - th) / 2 + s * 0.02
    out += tooth(tx, ty, th, fill=MINT)
    k = th / 112
    out += (
        '<path d="M%.2f %.2fC%.2f %.2f %.2f %.2f %.2f %.2f" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round"/>'
        % (tx + 22 * k, ty + 40 * k, tx + 20 * k, ty + 26 * k, tx + 26 * k, ty + 18 * k, tx + 36 * k, ty + 17 * k,
           WHITE, 7 * k)
    )
    return out


def v05():
    plex_b = font(PLEX, 600)
    plex = font(PLEX, 400)
    pad = 30
    s = 190
    body = tile(pad, pad, s)
    tx = pad + s + 44
    d1, w1 = text(plex_b, "Annicchiarico", 86, tx, pad + 132, tracking=-0.01)
    d2, w2 = text(plex, "Studio Dentistico", 38, tx + 2, pad + 64, tracking=0.02)
    W = tx + max(w1, w2) + pad
    H = s + pad * 2
    body += p(d2, MINT_DARK) + p(d1, NAVY)
    return svg(W, H, body, TITLE)


def v05_mark():
    s, pad = 256, 0
    return svg(s, s, tile(0, 0, s), TITLE)


# ---------- 06 Una riga, dente bicolore: per header e insegne strette ----------
TOOTH_LEFT = (
    "M50 14C42 4 28 2 18 8C6 16 4 34 8 50C11 62 16 70 18 82"
    "C20 96 22 108 30 110C38 112 40 100 42 90C44 80 46 74 50 74Z"
)


def tooth_split(x, y, h, left, right):
    s = h / 112
    return (
        '<g transform="translate(%.2f %.2f) scale(%.4f)"><path d="%s" fill="%s"/>'
        '<path d="%s" fill="%s" transform="translate(100 0) scale(-1 1)"/></g>'
        % (x, y, s, TOOTH_LEFT, left, TOOTH_LEFT, right)
    )


def v06():
    plex_l = font(PLEX, 300)
    plex_m = font(PLEX, 600)
    pad = 24
    th = 96
    tw = th * 100 / 112
    body = tooth_split(pad, pad, th, TEAL, TEAL_DARK)
    tx = pad + tw + 30
    base = pad + th / 2 + 16
    d1, w1 = text(plex_l, "Studio Dentistico ", 46, tx, base)
    d2, w2 = text(plex_m, "Annicchiarico", 46, tx + w1, base)
    W = tx + w1 + w2 + pad
    H = th + pad * 2
    body += p(d1, TEAL_TEXT) + p(d2, TEAL_DEEP)
    return svg(W, H, body, TITLE)


if __name__ == "__main__":
    write("01-c-dente-orizzontale.svg", v01())
    write("01-c-dente-orizzontale-negativo.svg", v01(dark=True))
    write("01-c-dente-verticale.svg", v01_vertical())
    write("01-c-dente-marchio.svg", v01_mark())
    write("02-dente-linea.svg", v02())
    write("03-monogramma-a.svg", v03())
    write("04-sorriso-verticale.svg", v04())
    write("04-sorriso-marchio.svg", v04_mark())
    write("05-blu-menta.svg", v05())
    write("05-blu-menta-icona.svg", v05_mark())
    write("06-una-riga.svg", v06())
