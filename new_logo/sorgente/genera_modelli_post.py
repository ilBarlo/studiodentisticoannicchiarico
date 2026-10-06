"""Modelli vuoti per i post dello studio: solo il logo, in più colori e formati.
Lo studio li apre in Canva o nell'editor di Instagram e ci aggiunge testi e foto.
Rilancia con:  python3 new_logo/sorgente/genera_modelli_post.py
"""
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = f"{ROOT}/new_logo/instagram/modelli"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# nome, sfondo CSS, logo (bianco o blu), codice colore da comunicare
COLORI = [
    ("01-blu", "radial-gradient(circle 1030px at 50% 30%, #385978 0%, #32506c 45%, #28425b 100%)", "bianco", "#385978"),
    ("02-blu-notte", "radial-gradient(circle 1030px at 50% 30%, #2a4258 0%, #1f3446 55%, #182a39 100%)", "bianco", "#1F3446"),
    ("03-crema", "#fdfaf5", "blu", "#FDFAF5"),
    ("04-bianco", "#ffffff", "blu", "#FFFFFF"),
    ("05-azzurro", "#e7eef5", "blu", "#E7EEF5"),
    ("06-menta", "#dff3ee", "blu", "#DFF3EE"),
]
# formato, larghezza, altezza, distanza del logo dall'alto, larghezza del marchio
FORMATI = [
    ("post", 1080, 1350, 64, 120),
    ("quadrato", 1080, 1080, 56, 110),
    ("storia", 1080, 1920, 160, 140),  # sotto la barra con il nome profilo
]


def page(sfondo, logo, w, h, top, mark):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin: 0; padding: 0; }}
html, body {{ width: {w}px; height: {h}px; overflow: hidden; }}
body {{ background: {sfondo}; display: flex; flex-direction: column; align-items: center; padding-top: {top}px; }}
.mark {{ width: {mark}px; }}
.scritte {{ width: {mark * 2.4}px; margin-top: {mark * 0.08}px; }}
</style></head><body>
<img class="mark" src="file://{ROOT}/new_logo/finale/marchio-{logo}.png" alt="">
<img class="scritte" src="file://{ROOT}/new_logo/finale/scritte-{logo}.png" alt="">
</body></html>"""


shutil.rmtree(OUT, ignore_errors=True)
for fmt, w, h, top, mark in FORMATI:
    os.makedirs(f"{OUT}/{fmt}", exist_ok=True)
    for nome, sfondo, logo, _ in COLORI:
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
            tmp.write(page(sfondo, logo, w, h, top, mark))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                        f"--screenshot={OUT}/{fmt}/{fmt}-{nome}.png", "--allow-file-access-from-files", f"file://{tmp.name}"],
                       check=True, capture_output=True)
        os.unlink(tmp.name)

# loghi sciolti, per chi vuole impaginare da zero
os.makedirs(f"{OUT}/loghi", exist_ok=True)
for f in ("logo-orizzontale-blu.png", "logo-orizzontale-bianco.png", "marchio-blu.png", "marchio-bianco.png",
          "scritte-blu.png", "scritte-bianco.png"):
    shutil.copy(f"{ROOT}/new_logo/finale/{f}", f"{OUT}/loghi/{f}")

righe = "\n".join(f"  {nome[3:]:<12} sfondo {hexc}   logo {logo}" for nome, _, logo, hexc in COLORI)
open(f"{OUT}/LEGGIMI.txt", "w", encoding="utf-8").write(f"""MODELLI POST - STUDIO DENTISTICO ANNICCHIARICO
==============================================
Sfondi vuoti con il logo dello studio, pronti da completare in Canva o su Instagram.

Formati
  post/       1080 x 1350  post verticale del feed (consigliato)
  quadrato/   1080 x 1080  post quadrato
  storia/     1080 x 1920  storie e reel; il logo è sotto la barra del profilo

Colori
{righe}

Colori per testi e dettagli
  Blu del logo     #385978   titoli su sfondi chiari
  Menta            #7ED6C4   piccoli titoli e dettagli su sfondi blu
  Crema            #FDFAF5   testi su sfondi blu
  Caratteri del sito: Piazzolla (titoli) e IBM Plex Sans (testi), entrambi gratuiti su Google Fonts e in Canva.

loghi/  loghi su fondo trasparente, per impaginare da zero.

Come usarli in Canva: Crea un design > Importa file > scegli il modello, poi aggiungi testi e foto sopra.
Nelle storie lasciate libera la parte bassa (circa 250 px): lì Instagram mette "Invia messaggio".
""")

zip_base = f"{ROOT}/new_logo/instagram/modelli-post-studio-annicchiarico"
shutil.make_archive(zip_base, "zip", OUT)
print("ok", zip_base + ".zip")
