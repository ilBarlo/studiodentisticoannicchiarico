"""Post e storia per il lancio del sito: "arriva domani" e "è online".
Stesso stile del primo post "sito in arrivo", con la firma "Sito web realizzato da" e il logo ilbarlo.
Rilancia con:  python3 new_logo/sorgente/genera_post_lancio.py
"""
import os
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = f"{ROOT}/new_logo/instagram/lancio"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DOMINIO = "studiodentisticoannicchiarico.it"
os.makedirs(OUT, exist_ok=True)

POST = dict(w=1080, h=1350, top=70, mark=170, scritte=380, after_logo=56, eyebrow=22, title=78, sub=27,
            phone=300, chip=200, credit_bottom=64)
STORIA = dict(w=1080, h=1920, top=230, mark=220, scritte=480, after_logo=80, eyebrow=26, title=96, sub=32,
              phone=380, chip=230, credit_bottom=300)  # sopra la barra "Invia messaggio"

VERSIONI = {
    "domani": dict(
        eyebrow="MANCA SOLO UN GIORNO",
        title="Il nostro sito<br>arriva domani.",
        sub="Trattamenti, team e prenotazioni online,<br>tutto in un unico posto.",
        extra=f'<p class="dominio"><span>Da domani su</span>{DOMINIO}</p>',
    ),
    "online": dict(
        eyebrow="ORA ONLINE",
        title="Il nostro sito<br>è online.",
        sub="Scopri trattamenti e team,<br>e prenota la tua prima visita.",
        extra="phone",
    ),
}


# la versione con il telefono ha più contenuto: logo e titolo più compatti
COMPATTO = {
    "post": dict(top=48, mark=118, scritte=270, after_logo=34, title=66, sub=25, phone=250, credit_bottom=44),
    "storia": dict(top=170, mark=160, scritte=360, after_logo=50, title=86, sub=30, phone=340, credit_bottom=280),
}


def page(L, v):
    if v["extra"] == "phone":
        extra = (f'<div class="phone"><img src="file://{ROOT}/new_logo/sorgente/schermata-sito-mobile.png" alt=""></div>'
                 f'<p class="dominio solo">{DOMINIO}</p>')
    else:
        extra = v["extra"]
    p = L["phone"]
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Plex; src: url(file://{ROOT}/fonts/ibm-plex-sans-latin.woff2); font-weight: 100 700; }}
@font-face {{ font-family: Piazzolla; src: url(file://{ROOT}/fonts/piazzolla-latin.woff2); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {L['w']}px; height: {L['h']}px; overflow: hidden; }}
body {{ position: relative; font-family: Plex, sans-serif; color: #fdfaf5; text-align: center;
  display: flex; flex-direction: column; align-items: center; padding-top: {L['top']}px;
  background: radial-gradient(circle {L['w'] * 0.95}px at 50% {L['h'] * 0.34}px,
    #385978 0%, #355672 18%, #32506c 45%, #2c4862 75%, #28425b 100%); }}
.mark {{ width: {L['mark']}px; }}
.scritte {{ width: {L['scritte']}px; margin-top: {L['mark'] * 0.08}px; }}
.eyebrow {{ margin-top: {L['after_logo']}px; font-size: {L['eyebrow']}px; font-weight: 600; letter-spacing: .3em; color: #7ed6c4; }}
h1 {{ margin-top: {L['eyebrow'] * 0.9}px; font: 500 {L['title']}px/1.08 Piazzolla, serif; letter-spacing: -.01em; }}
.sub {{ margin-top: {L['sub'] * 0.9}px; font-size: {L['sub']}px; line-height: 1.45; color: #d6e2ea; }}
.dominio {{ margin-top: {L['sub'] * 1.6}px; padding: {L['sub'] * 0.55}px {L['sub'] * 1.2}px; border: 2px solid #7ed6c4; border-radius: 999px;
  font-size: {L['sub'] * 1.02}px; font-weight: 500; color: #fdfaf5; }}
.dominio span {{ display: block; font-size: {L['sub'] * 0.62}px; font-weight: 600; letter-spacing: .2em; text-transform: uppercase; color: #7ed6c4; margin-bottom: 4px; }}
.dominio.solo {{ margin-top: {L['sub'] * 1.1}px; border: 0; padding: 0; color: #7ed6c4; }}
/* telefono con la home del sito: cornice scura, angoli arrotondati, ombra */
.phone {{ margin-top: {L['sub'] * 1.3}px; width: {p}px; height: {p * 1.62}px; padding: {p * 0.035}px; border-radius: {p * 0.16}px;
  background: #0d1a24; box-shadow: 0 30px 60px rgba(5, 14, 22, .5), inset 0 0 0 2px rgba(255, 255, 255, .08); overflow: hidden; }}
.phone img {{ width: 100%; height: 100%; object-fit: cover; object-position: top; border-radius: {p * 0.13}px; display: block;
  -webkit-mask-image: linear-gradient(to bottom, #000 82%, transparent 100%); }}
.credit {{ margin-top: auto; margin-bottom: {L['credit_bottom']}px; padding-top: 24px; display: flex; flex-direction: column; align-items: center; gap: 12px; }}
.credit p {{ font-size: {L['sub'] * 0.82}px; color: #b4c6d4; }}
.chip {{ width: {L['chip']}px; padding: 12px 18px; background: #fff; border-radius: 12px; }}
.chip img {{ width: 100%; display: block; }}
</style></head><body>
<img class="mark" src="file://{ROOT}/new_logo/finale/marchio-bianco.png" alt="">
<img class="scritte" src="file://{ROOT}/new_logo/finale/scritte-bianco.png" alt="">
<p class="eyebrow">{v['eyebrow']}</p>
<h1>{v['title']}</h1>
<p class="sub">{v['sub']}</p>
{extra}
<div class="credit">
  <p>Sito web realizzato da</p>
  <span class="chip"><img src="file://{ROOT}/new_logo/sorgente/ilbarlo-firma.png" alt="ilbarlo"></span>
</div>
</body></html>"""


for nome, v in VERSIONI.items():
    for prefisso, L in (("post", POST), ("storia", STORIA)):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
            tmp.write(page(dict(L, **COMPATTO[prefisso]) if v["extra"] == "phone" else L, v))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={L['w']},{L['h']}", f"--screenshot={OUT}/{prefisso}-sito-{nome}.png",
                        "--allow-file-access-from-files", f"file://{tmp.name}"], check=True, capture_output=True)
        os.unlink(tmp.name)
        print("ok", f"{prefisso}-sito-{nome}")
