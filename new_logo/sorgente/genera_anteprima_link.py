"""Immagine di anteprima quando si condivide il link (WhatsApp, Facebook, LinkedIn): 1200x630.
Rilancia con:  python3 new_logo/sorgente/genera_anteprima_link.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PNG = f"{ROOT}/new_logo/sorgente/_anteprima.png"

page = f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Plex; src: url(file://{ROOT}/fonts/ibm-plex-sans-latin.woff2); font-weight: 100 700; }}
@font-face {{ font-family: Piazzolla; src: url(file://{ROOT}/fonts/piazzolla-latin.woff2); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1200px; height: 630px; overflow: hidden; }}
body {{ position: relative; font-family: Plex, sans-serif; color: #fdfaf5;
  background: radial-gradient(circle 900px at 72% 40%, #385978 0%, #32506c 45%, #28425b 100%); }}
.testo {{ position: absolute; left: 72px; top: 0; bottom: 0; width: 500px; display: flex; flex-direction: column; justify-content: center; }}
.logo {{ width: 340px; }}
h1 {{ margin-top: 40px; font: 500 48px/1.12 Piazzolla, serif; }}
p {{ margin-top: 18px; font-size: 21px; line-height: 1.45; color: #d6e2ea; }}
.luogo {{ margin-top: 26px; font-size: 20px; font-weight: 600; letter-spacing: .2em; color: #7ed6c4; }}
/* foto più alta del riquadro: le figure poggiano sul bordo in basso, tagliate in vita */
.foto {{ position: absolute; right: -10px; bottom: -170px; height: 760px; filter: drop-shadow(0 24px 30px rgba(8, 20, 32, .45)); }}
</style></head><body>
<div class="testo">
  <img class="logo" src="file://{ROOT}/new_logo/finale/logo-orizzontale-bianco.png" alt="">
  <h1>Il tuo piano di trattamento, previsualizzato e condiviso con te in tempo reale.</h1>
  <p>Chirurgia e implantologia, parodontologia, ortodonzia Invisalign e cure per i bambini.</p>
  <p class="luogo">GROTTAGLIE (TA)</p>
</div>
<img class="foto" src="file://{ROOT}/img/team/team-cutout.png" alt="">
</body></html>"""

with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
    tmp.write(page)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                f"--screenshot={PNG}", "--allow-file-access-from-files", f"file://{tmp.name}"], check=True, capture_output=True)
os.unlink(tmp.name)
# JPEG leggero: WhatsApp scarta le anteprime troppo pesanti
subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "84", PNG, "--out", f"{ROOT}/img/anteprima-link.jpg"],
               check=True, capture_output=True)
os.unlink(PNG)
print("ok img/anteprima-link.jpg")
