"""Post e storia Instagram "I nostri servizi".

Servizi, descrizioni e icone vengono letti da index.html: se cambia il sito,
basta rilanciare  python3 new_logo/sorgente/genera_post_servizi.py
L'impaginazione è HTML resa da Chrome headless, così testo e icone restano nitidi.
"""
import os
import re
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = f"{ROOT}/new_logo/instagram/servizi"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)

html = open(f"{ROOT}/index.html", encoding="utf-8").read()
cards = re.findall(r'<li class="treatment-card">.*?(<svg.*?</svg>).*?<h3>(.*?)</h3>\s*<p>(.*?)</p>', html, re.S)
assert cards, "nessun trattamento trovato in index.html"

POST = dict(w=1080, h=1350, top=56, mark=110, mark_gap=8, scritte=260, after_logo=34,
            eyebrow=21, after_eyebrow=14, title=56, after_title=12, sub=24, after_sub=30,
            icon=34, font=27, gap_x=44, gap_y=15, after_grid=36,
            cta=36, after_cta=12, cta_sub=22, sig=34, sig_bottom=44)
STORIA = dict(w=1080, h=1920, top=150, mark=140, mark_gap=12, scritte=330, after_logo=50,
              eyebrow=25, after_eyebrow=20, title=66, after_title=16, sub=28, after_sub=54,
              icon=38, font=30, gap_x=44, gap_y=24, after_grid=60,
              cta=44, after_cta=16, cta_sub=26, sig=40, sig_bottom=250)  # sopra "Invia messaggio"


def page(L):
    items = "".join(
        f'<div class="t"><span class="num">{i:02d}</span><span class="i">{svg}</span>'
        # trattino non divisibile: "laser-terapia" non va a capo a metà
        f'<div><p class="n">{t}</p><p class="d">{d.replace("-", "&#8209;")}</p></div></div>'
        for i, (svg, t, d) in enumerate(cards, 1))
    f = L["font"]
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Plex; src: url(file://{ROOT}/fonts/ibm-plex-sans-latin.woff2); font-weight: 100 700; }}
@font-face {{ font-family: Piazzolla; src: url(file://{ROOT}/fonts/piazzolla-latin.woff2); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {L['w']}px; height: {L['h']}px; overflow: hidden; }}
body {{ position: relative; font-family: Plex, sans-serif; color: #fdfaf5; text-align: center;
  /* blu del logo con una luce morbida in alto, come post e storia precedenti */
  background: radial-gradient(circle {L['w'] * 0.95}px at 50% {L['h'] * 0.26}px,
    #385978 0%, #355672 18%, #32506c 45%, #2c4862 75%, #28425b 100%); }}
.top {{ padding-top: {L['top']}px; display: flex; flex-direction: column; align-items: center; }}
.mark {{ width: {L['mark']}px; }}
.scritte {{ width: {L['scritte']}px; margin-top: {L['mark_gap']}px; }}
.eyebrow {{ margin-top: {L['after_logo']}px; font-size: {L['eyebrow']}px; font-weight: 600; letter-spacing: .28em; color: #7ed6c4; }}
h1 {{ margin-top: {L['after_eyebrow']}px; font: 500 {L['title']}px/1.15 Piazzolla, serif; }}
.sub {{ margin-top: {L['after_title']}px; font-size: {L['sub']}px; color: #d6e2ea; }}
.g {{ width: 940px; margin: {L['after_sub']}px auto 0; display: grid; grid-template-columns: 1fr 1fr; column-gap: {L['gap_x']}px;
  border-top: 1px solid rgba(253, 250, 245, .22); text-align: left; }}
.t {{ display: grid; grid-template-columns: auto auto 1fr; align-items: start; column-gap: {L['icon'] * 0.32}px;
  padding: {L['gap_y']}px 0; border-bottom: 1px solid rgba(253, 250, 245, .22); }}
.num {{ font-size: {f * 0.62}px; line-height: 1; font-weight: 500; letter-spacing: .08em; color: #7ed6c4; padding-top: {f * 0.36}px; }}
.i {{ width: {L['icon']}px; height: {L['icon']}px; color: #7ed6c4; }}
.i svg {{ width: 100%; height: 100%; fill: none; stroke: currentColor; stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }}
.n {{ font: 500 {f}px/1.15 Piazzolla, serif; }}
.d {{ margin-top: {f * 0.28}px; font-size: {f * 0.6}px; line-height: 1.4; color: rgba(214, 226, 234, .82); }}
.cta {{ margin-top: {L['after_grid']}px; font: 500 {L['cta']}px/1.15 Piazzolla, serif; }}
.cta-sub {{ margin-top: {L['after_cta']}px; font-size: {L['cta_sub']}px; font-weight: 500; color: #7ed6c4; word-spacing: .1em; }}
.firma {{ position: absolute; left: 0; right: 0; bottom: {L['sig_bottom']}px; height: {L['sig']}px;
  display: flex; justify-content: center; align-items: center; gap: {L['sig'] * 0.55}px; }}
.chip {{ height: 100%; padding: 6px 8px; background: #fff; border-radius: 6px; }}
.chip img {{ height: 100%; display: block; }}
.sep {{ width: 2px; height: {L['sig'] - 8}px; background: #96acbe; }}
.firma .studio {{ height: 100%; }}
</style></head><body>
<div class="top">
  <img class="mark" src="file://{ROOT}/new_logo/finale/marchio-bianco.png" alt="">
  <img class="scritte" src="file://{ROOT}/new_logo/finale/scritte-bianco.png" alt="">
  <p class="eyebrow">I NOSTRI SERVIZI</p>
  <h1>Di cosa ci occupiamo</h1>
  <p class="sub">Dalla chirurgia alla prevenzione, sotto lo stesso tetto.</p>
</div>
<div class="g">{items}</div>
<p class="cta">Prenota una prima visita</p>
<p class="cta-sub">339 109 2569 &nbsp;·&nbsp; 099 566 8098 &nbsp;·&nbsp; Grottaglie (TA)</p>
<div class="firma">
  <span class="chip"><img src="file://{ROOT}/new_logo/sorgente/ilbarlo-firma.png" alt=""></span>
  <span class="sep"></span>
  <img class="studio" src="file://{ROOT}/new_logo/finale/logo-orizzontale-bianco.png" alt="">
</div>
</body></html>"""


for name, L in (("post-servizi", POST), ("storia-servizi", STORIA)):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(page(L))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    f"--window-size={L['w']},{L['h']}", f"--screenshot={OUT}/{name}.png",
                    "--allow-file-access-from-files", f"file://{tmp.name}"],
                   check=True, capture_output=True)
    os.unlink(tmp.name)
    print("ok", name)
