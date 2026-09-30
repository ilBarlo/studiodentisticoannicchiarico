"""Varianti del logo definitivo con denti più anatomici.

Genera marchio e logo orizzontale in:
new_logo/definitivo/varianti-dente-realistiche/
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import genera2 as g

ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, "new_logo", "definitivo", "varianti-dente-realistiche")
os.makedirs(OUT, exist_ok=True)

DARK = "#39A495"
LIGHT = "#54EBBB"
WHITE = "#FFFFFF"
MW, MH = 124, 180
SW = 6.5


def line_path(d, width=SW):
    return (
        '<path d="%s" fill="none" stroke="%s" stroke-width="%.2f" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    ) % (d, DARK, width)


def smile():
    return (
        '<path d="M2 136A64 64 0 0 0 122 136'
        'A78 78 0 0 1 2 136Z" fill="%s"/>'
    ) % LIGHT


# Molare superiore: corona larga, due cuspidi e radici separate.
MOLARE_LARGO = (
    "M25 78C21 65 18 46 23 31"
    "C28 16 42 12 53 20C58 23 60 27 62 31"
    "C65 26 68 21 74 18C86 13 99 20 103 34"
    "C107 49 102 66 99 79"
    "C96 93 95 110 91 122C88 131 82 132 77 124"
    "C71 114 69 96 64 90C62 87 60 87 58 90"
    "C53 97 51 114 46 124C41 132 35 131 32 122"
    "C28 110 28 93 25 78Z"
    " M38 51C47 44 55 46 62 52C69 46 77 44 86 51"
)

# Molare compatto: profilo più pulito, solco centrale e biforcazione leggibile.
MOLARE_COMPATTO = (
    "M24 73C20 57 20 38 28 25"
    "C35 14 48 13 57 23L62 30L67 23"
    "C76 13 89 14 96 25C104 38 104 57 100 73"
    "C97 87 96 108 91 122C88 131 82 132 77 124"
    "C72 115 70 98 65 89C63 85 61 85 59 89"
    "C54 98 52 115 47 124C42 132 36 131 33 122"
    "C28 108 27 87 24 73Z"
    " M39 49C47 44 54 46 62 52C70 46 77 44 85 49"
    " M62 84C61 75 61 66 62 57"
)

# Premolare: corona più stretta, due cuspidi e radici lunghe.
PREMOLARE = (
    "M32 69C29 56 28 39 34 27"
    "C39 17 48 14 56 21C59 24 61 28 62 34"
    "C64 28 66 24 70 21C78 14 87 17 92 27"
    "C98 39 97 56 94 69"
    "C91 85 90 106 86 122C84 130 78 132 74 124"
    "C69 114 67 96 63 88C62 86 61 86 60 88"
    "C56 96 54 114 50 124C46 132 40 130 38 122"
    "C34 106 35 85 32 69Z"
    " M43 48C50 43 56 46 62 52C68 46 74 43 81 48"
)

# Doppia radice: corona molare piena e separazione radicolare anatomica.
DOPPIA_RADICE = (
    "M23 67C20 53 20 35 29 24"
    "C37 14 49 15 57 24L62 31L67 24"
    "C75 15 87 14 95 24C104 35 104 53 101 67"
    "C98 79 91 88 88 99L83 123"
    "C81 132 74 132 71 123L64 96"
    "C63 92 61 92 60 96L53 123"
    "C50 132 43 132 41 123L36 99"
    "C33 88 26 79 23 67Z"
    " M35 48C44 42 53 45 62 52C71 45 80 42 89 48"
    " M62 58C61 68 61 80 62 91"
)

# Profilo pieno: il più immediato a dimensioni piccole.
SILHOUETTE = (
    "M23 68C19 52 20 34 29 23"
    "C37 13 49 14 57 23L62 30L67 23"
    "C75 14 87 13 95 23C104 34 105 52 101 68"
    "C98 83 95 105 91 121C88 132 81 133 76 123"
    "C71 113 69 96 64 89C62 86 60 86 58 89"
    "C53 96 51 113 46 123C41 133 34 132 31 121"
    "C27 105 26 83 23 68Z"
)

VARIANTS = [
    ("01-molare-largo", MOLARE_LARGO, False),
    ("02-molare-compatto", MOLARE_COMPATTO, False),
    ("03-premolare", PREMOLARE, False),
    ("04-doppia-radice", DOPPIA_RADICE, False),
    ("05-silhouette-piena", SILHOUETTE, True),
]


def symbol(path_d, filled=False):
    tooth = (
        '<path d="%s" fill="%s"/>'
        % (path_d, DARK)
        if filled
        else line_path(path_d)
    )
    return smile() + tooth


def mark(path_d, filled, x, y, h):
    scale = h / MH
    return (
        '<g transform="translate(%.2f %.2f) scale(%.4f)">%s</g>'
        % (x, y, scale, symbol(path_d, filled))
    )


def horizontal(path_d, filled):
    piaz = g.font(g.PIAZ, 500, 36)
    plex = g.font(g.PLEX, 400)
    pad, mh = 32, 150
    mw = mh * MW / MH
    tx = pad + mw + 40
    d1, w1 = g.text(piaz, "ANNICCHIARICO", 50, tx, pad + 82, 0.14)
    d2, w2 = g.text(plex, "STUDIO DENTISTICO", 20, tx + 2, pad + 118, 0.36)
    width = tx + max(w1, w2) + pad
    body = mark(path_d, filled, pad, pad, mh)
    body += g.p(d1, DARK) + g.p(d2, LIGHT)
    return g.svg(width, mh + pad * 2, body)


def mark_only(path_d, filled):
    return g.svg(256, 256, mark(path_d, filled, 38, 22, 212))


if __name__ == "__main__":
    for name, path_d, filled in VARIANTS:
        with open(os.path.join(OUT, name + "-orizzontale.svg"), "w") as f:
            f.write(horizontal(path_d, filled))
        with open(os.path.join(OUT, name + "-marchio.svg"), "w") as f:
            f.write(mark_only(path_d, filled))
        print("scritto", name)
