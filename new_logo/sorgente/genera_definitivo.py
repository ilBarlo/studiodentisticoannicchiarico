"""Logo definitivo Studio Dentistico Annicchiarico.
Dente a linea che legge come "A" (radici = gambe, archetto = traversa),
sorriso sotto = "C" ruotata, completo come una mezzaluna.
Uso: python3 genera_definitivo.py -> new_logo/definitivo/
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera2 as g

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "definitivo"); os.makedirs(OUT, exist_ok=True)
PAPER, INK = "#FFFFFF", "#0F2A2E"
PALETTES = {
    "": ("#38878E", "#4AB1B8"),                    # colori del marchio in uso sul sito
    "colori-originali": ("#39A495", "#54EBBB"),    # colori del file originale del cliente
}

# geometria in un riquadro 124 x 178, asse a x = 62
SW = 7.0  # spessore linea del dente: poco più del riferimento

def half(mx):
    """Metà dente (mx = 1 sinistra, -1 destra), tracciato aperto.
    Molare: corona larga con due cuspidi, colletto leggermente stretto,
    radici che si aprono a punta (le gambe della A)."""
    def X(x): return 62 + mx * (x - 62)
    outer = ("M%.1f 128C%.1f 112 %.1f 90 %.1f 72"      # radice: dalla punta al colletto
             "C%.1f 62 %.1f 52 %.1f 40"                 # colletto -> punto più largo della corona
             "C%.1f 26 %.1f 14 %.1f 14"                 # fianco -> cuspide
             "C%.1f 14 %.1f 20 62 26") % (               # cuspide -> solco centrale
        X(30), X(26), X(24), X(28),
        X(29), X(20), X(20),
        X(20), X(28), X(40),
        X(50), X(58))
    inner = "M62 84C%.1f 100 %.1f 116 %.1f 126" % (X(58), X(50), X(42))
    return outer, inner

def tooth_paths(color, sw=SW):
    d = []
    for mx in (1, -1):
        o, i = half(mx); d += [o, i]
    d.append("M44 56Q62 47 80 56")  # traversa della A, nel corpo della corona
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linecap="round" stroke-linejoin="round"/>' % (
        " ".join(d), color, sw)

def smile_path(color):
    """Mezzaluna: C ruotata verso l'alto. Arco esterno più profondo, interno più piatto:
    spessa al centro, affilata alle punte."""
    x1, x2, y, R1, R2 = 2, 122, 136, 64, 78
    return ('<path d="M%d %dA%d %d 0 0 0 %d %dA%d %d 0 0 1 %d %dZ" fill="%s"/>'
            % (x1, y, R1, R1, x2, y, R2, R2, x1, y, color))

MW, MH = 124, 180

def mark(x, y, h, tooth_c, smile_c):
    s = h / MH
    return '<g transform="translate(%.2f %.2f) scale(%.4f)">%s%s</g>' % (x, y, s, smile_path(smile_c), tooth_paths(tooth_c))

def vertical(dark_c, light_c, bg=None, text_c=None, sub_c=None):
    piaz = g.font(g.PIAZ, 500, 36); plex = g.font(g.PLEX, 400)
    text_c = text_c or dark_c; sub_c = sub_c or light_c
    pad, mh = 44, 190
    name = "ANNICCHIARICO"; sub = "STUDIO DENTISTICO"
    w1 = g.measure(piaz, name, 46, 0.16); w2 = g.measure(plex, sub, 19, 0.38)
    W = max(w1, w2) + pad * 2 + 40; cx = W / 2
    mw = mh * MW / MH
    body = mark(cx - mw / 2, pad, mh, dark_c, light_c)
    y1 = pad + mh + 74
    d1, _ = g.text(piaz, name, 46, cx, y1, 0.16, "middle"); body += g.p(d1, text_c)
    d2, _ = g.text(plex, sub, 19, cx, y1 + 44, 0.38, "middle"); body += g.p(d2, sub_c)
    body += '<rect x="%.2f" y="%.2f" width="72" height="1.6" fill="%s"/>' % (cx - 36, y1 + 70, light_c)
    H = y1 + 70 + pad
    return g.svg(W, H, body, bg=bg)

def horizontal(dark_c, light_c, bg=None, text_c=None, sub_c=None):
    piaz = g.font(g.PIAZ, 500, 36); plex = g.font(g.PLEX, 400)
    text_c = text_c or dark_c; sub_c = sub_c or light_c
    pad, mh = 32, 150
    mw = mh * MW / MH
    tx = pad + mw + 40
    d1, w1 = g.text(piaz, "ANNICCHIARICO", 50, tx, pad + 82, 0.14)
    d2, w2 = g.text(plex, "STUDIO DENTISTICO", 20, tx + 2, pad + 118, 0.36)
    W = tx + max(w1, w2) + pad; H = mh + pad * 2
    body = mark(pad, pad, mh, dark_c, light_c) + g.p(d1, text_c) + g.p(d2, sub_c)
    return g.svg(W, H, body, bg=bg)

def mark_only(dark_c, light_c, bg=None):
    return g.svg(256, 256, mark(38, 22, 212, dark_c, light_c), bg=bg)

def oneline(dark_c, light_c):
    piaz = g.font(g.PIAZ, 500, 36); plex = g.font(g.PLEX, 400)
    pad, mh = 18, 72
    mw = mh * MW / MH; tx = pad + mw + 22; base = pad + mh * 0.64
    d1, w1 = g.text(plex, "Studio Dentistico ", 34, tx, base)
    d2, w2 = g.text(piaz, "Annicchiarico", 38, tx + w1, base)
    return g.svg(tx + w1 + w2 + pad, mh + pad * 2, mark(pad, pad, mh, dark_c, light_c) + g.p(d1, light_c) + g.p(d2, dark_c))

RED = "#C62828"

def cross(cx, cy, size, color, arm=0.32):
    a = size * arm; r = size * 0.09
    return ('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="%.2f" fill="%s"/>'
            % (cx - a / 2, cy - size / 2, a, size, r, color, cx - size / 2, cy - a / 2, size, a, r, color))

def insegna(dark_c, light_c, mode, bg=None, text_c=None, sub_c=None):
    """Orizzontale per insegna. mode: 'badge' (quadrato rosso a destra) o 'disco' (disco rosso sul dente)."""
    piaz = g.font(g.PIAZ, 500, 36); plex = g.font(g.PLEX, 400)
    text_c = text_c or dark_c; sub_c = sub_c or light_c
    pad, mh = 40, 190
    mw = mh * MW / MH
    tx = pad + mw + 52
    d1, w1 = g.text(piaz, "ANNICCHIARICO", 64, tx, pad + 104, 0.14)
    d2, w2 = g.text(plex, "STUDIO DENTISTICO", 25, tx + 2, pad + 150, 0.36)
    W = tx + max(w1, w2) + pad
    body = mark(pad, pad, mh, dark_c, light_c) + g.p(d1, text_c) + g.p(d2, sub_c)
    if mode == "badge":
        s = 92; bx = W; W += s + pad
        body += '<rect x="%.2f" y="%.2f" width="%d" height="%d" rx="%.1f" fill="%s"/>' % (bx, pad + (mh - s) / 2, s, s, s * 0.22, RED)
        body += cross(bx + s / 2, pad + mh / 2, s * 0.56, PAPER)
    else:
        sc = mh / MH
        cx, cy = pad + 104 * sc, pad + 26 * sc
        body += '<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (cx, cy, 15 * sc, RED)
        body += cross(cx, cy, 17 * sc, PAPER, arm=0.3)
    return g.svg(W, mh + pad * 2, body, bg=bg)

def write(sub, name, content):
    d = os.path.join(OUT, sub) if sub else OUT
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, name), "w").write(content); print("scritto", os.path.join(sub, name) if sub else name)

if __name__ == "__main__":
    for sub, (dark_c, light_c) in PALETTES.items():
        write(sub, "logo-verticale.svg", vertical(dark_c, light_c))
        write(sub, "logo-orizzontale.svg", horizontal(dark_c, light_c))
        write(sub, "logo-una-riga.svg", oneline(dark_c, light_c))
        write(sub, "marchio.svg", mark_only(dark_c, light_c))
        # negativo su fondo scuro: dente chiaro, sorriso teal, testo bianco
        write(sub, "logo-verticale-negativo.svg", vertical(light_c, light_c, bg=INK, text_c=PAPER, sub_c=light_c))
        write(sub, "logo-orizzontale-negativo.svg", horizontal(light_c, light_c, bg=INK, text_c=PAPER, sub_c=light_c))
        write(sub, "marchio-negativo.svg", mark_only(light_c, light_c, bg=INK))
        # monocromatici
        write(sub, "logo-verticale-mono-nero.svg", vertical(INK, INK))
        write(sub, "logo-orizzontale-mono-nero.svg", horizontal(INK, INK))
        write(sub, "logo-orizzontale-mono-bianco.svg", horizontal(PAPER, PAPER))
        write(sub, "marchio-mono-nero.svg", mark_only(INK, INK))
        if sub == "":
            write("insegna", "insegna-croce-badge-rosso.svg", insegna(dark_c, light_c, "badge"))
            write("insegna", "insegna-croce-badge-rosso-negativo.svg", insegna(light_c, light_c, "badge", bg=INK, text_c=PAPER))
            write("insegna", "insegna-croce-disco-rosso.svg", insegna(dark_c, light_c, "disco"))
            write("insegna", "insegna-croce-disco-rosso-negativo.svg", insegna(light_c, light_c, "disco", bg=INK, text_c=PAPER))
            write("insegna", "insegna-senza-croce.svg", horizontal(dark_c, light_c))
            write("insegna", "insegna-mono-nero.svg", horizontal(INK, INK))
            write("insegna", "insegna-mono-bianco.svg", horizontal(PAPER, PAPER))
