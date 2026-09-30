"""Varianti per insegna del logo A (Sigillo C) con croce sanitaria nei colori del marchio.
Uso: python3 genera_insegna.py -> new_logo/insegna/
"""
import os, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera2 as g

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "insegna")
os.makedirs(OUT, exist_ok=True)
INK, TEAL, TEAL_DARK, MINT, PAPER = g.INK, g.TEAL, g.TEAL_DARK, g.MINT, g.PAPER
RED = "#C62828"  # rosso del dettaglio: croce bianca su fondo rosso, non croce rossa su bianco

def cross(cx, cy, size, color, arm=0.34, r=None):
    """Croce piena a bracci uguali, angoli arrotondati."""
    a = size * arm; r = size * 0.09 if r is None else r
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>'
            % (cx - a / 2, cy - size / 2, a, size, r, color, cx - size / 2, cy - a / 2, size, a, r, color))

def cross_badge(x, y, s, bg, fg):
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>' % (x, y, s, s, s * 0.22, bg)
            + cross(x + s / 2, y + s / 2, s * 0.58, fg, arm=0.32))

def mark_cross(ox, oy, size, arc, disc, toothc, crossc):
    """Marchio A con la croce nell'apertura della C, a destra."""
    body = g.mark_a(ox, oy, size, arc, disc, toothc)
    sw = size * 0.10
    cx = ox + size - sw / 2 - size * 0.02
    cy = oy + size / 2
    body += cross(cx, cy, size * 0.20, crossc, arm=0.32)
    return body

def mark_cross_red(ox, oy, size, arc, disc, toothc, crossc):
    """Marchio A con disco rosso e croce bianca nell'apertura della C."""
    body = g.mark_a(ox, oy, size, arc, disc, toothc)
    sw = size * 0.10
    cx = ox + size - sw / 2 - size * 0.01
    cy = oy + size / 2
    body += '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, size * 0.145, RED)
    body += cross(cx, cy, size * 0.165, PAPER, arm=0.3)
    return body

def lockup(mark_fn, dark=False, mono=None, badge=False, red_badge=False):
    """Orizzontale per insegna: marchio (con croce) + nome. mono = colore unico."""
    piaz = g.font(g.PIAZ, 500, 72); plex = g.font(g.PLEX, 500)
    if mono:
        name_c = tag_c = arc = disc = crossc = mono; toothc = PAPER if mono != PAPER else INK
        bg = None
    elif dark:
        name_c, tag_c, arc, disc, toothc, crossc, bg = PAPER, MINT, TEAL, PAPER, INK, MINT, INK
    else:
        name_c, tag_c, arc, disc, toothc, crossc, bg = INK, g.TEAL_TEXT, TEAL, INK, PAPER, TEAL_DARK, None
    m, pad = 200, 40
    extra = m * 0.22 if mark_fn in (mark_cross, mark_cross_red) else 0
    tx = pad + m + extra + 48
    d_tag, w_tag = g.text(plex, "STUDIO DENTISTICO", 26, tx + 2, pad + 70, tracking=0.32)
    d_name, w_name = g.text(piaz, "Annicchiarico", 104, tx, pad + 158)
    W = tx + max(w_tag, w_name) + pad
    body = mark_fn(pad, pad, m, arc, disc, toothc, crossc) if mark_fn in (mark_cross, mark_cross_red) else g.mark_a(pad, pad, m, arc, disc, toothc)
    body += g.p(d_tag, tag_c) + g.p(d_name, name_c)
    if badge:
        s = 88
        bx = W; W += s + pad
        bbg, bfg = (mono, toothc) if mono else ((RED, PAPER) if red_badge else ((MINT, INK) if dark else (TEAL, PAPER)))
        body += cross_badge(bx, pad + (m - s) / 2, s, bbg, bfg)
    H = m + pad * 2
    return g.svg(W, H, body, bg=bg)

def mark_only(dark=False, mono=None, fn=None):
    fn = fn or mark_cross
    if mono: arc = disc = crossc = mono; toothc = PAPER if mono != PAPER else INK; bg = None
    elif dark: arc, disc, toothc, crossc, bg = TEAL, PAPER, INK, MINT, INK
    else: arc, disc, toothc, crossc, bg = TEAL, INK, PAPER, TEAL_DARK, None
    size = 240; W = 320; H = 300
    return g.svg(W, H, fn(30, 30, size, arc, disc, toothc, crossc), bg=bg)

def w(name, content):
    open(os.path.join(OUT, name), "w").write(content); print("scritto", name)

# 1. croce nella C
w("insegna-1-croce-nella-c.svg", lockup(mark_cross))
w("insegna-1-croce-nella-c-negativo.svg", lockup(mark_cross, dark=True))
w("insegna-1-croce-nella-c-mono-nero.svg", lockup(mark_cross, mono=INK))
w("insegna-1-croce-nella-c-mono-bianco.svg", lockup(mark_cross, mono=PAPER))
w("insegna-1-marchio.svg", mark_only())
w("insegna-1-marchio-negativo.svg", mark_only(dark=True))
w("insegna-1-marchio-mono-nero.svg", mark_only(mono=INK))
# 2. croce a badge, separata, a destra del nome
w("insegna-2-croce-badge.svg", lockup(g.mark_a, badge=True))
w("insegna-2-croce-badge-negativo.svg", lockup(g.mark_a, dark=True, badge=True))
w("insegna-2-croce-badge-mono-nero.svg", lockup(g.mark_a, mono=INK, badge=True))
w("insegna-2-croce-badge-mono-bianco.svg", lockup(g.mark_a, mono=PAPER, badge=True))
# 4. dettaglio rosso: croce bianca su disco rosso nella C, o badge rosso
w("insegna-4-rosso-nella-c.svg", lockup(mark_cross_red))
w("insegna-4-rosso-nella-c-negativo.svg", lockup(mark_cross_red, dark=True))
w("insegna-4-rosso-marchio.svg", mark_only(fn=mark_cross_red))
w("insegna-4-rosso-marchio-negativo.svg", mark_only(dark=True, fn=mark_cross_red))
w("insegna-5-rosso-badge.svg", lockup(g.mark_a, badge=True, red_badge=True))
w("insegna-5-rosso-badge-negativo.svg", lockup(g.mark_a, dark=True, badge=True, red_badge=True))
# 3. entrambe: croce nella C e badge, per insegne lunghe
w("insegna-3-croce-doppia.svg", lockup(mark_cross, badge=True))
w("insegna-3-croce-doppia-negativo.svg", lockup(mark_cross, dark=True, badge=True))
