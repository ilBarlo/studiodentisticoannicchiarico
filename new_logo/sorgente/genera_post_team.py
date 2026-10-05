"""Post e storia Instagram del team (una card per dottore + una di gruppo).

Nomi, ruoli e specializzazioni vengono letti dalla sezione team di index.html.
Rilancia con:  python3 new_logo/sorgente/genera_post_team.py
"""
import os
import re
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = f"{ROOT}/new_logo/instagram/team"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
os.makedirs(OUT, exist_ok=True)

html = open(f"{ROOT}/index.html", encoding="utf-8").read()
team_html = html[html.index('id="team"'):]
team_html = team_html[:team_html.index("</section>")]
DOTTORI = {}
for nome, ruolo, voci in re.findall(
        r'<h3>(.*?)</h3>\s*<p class="team-role">(.*?)</p>\s*<ul class="chip-list">(.*?)</ul>', team_html, re.S):
    DOTTORI[nome] = dict(nome=nome, ruolo=ruolo, voci=re.findall(r"<li>(.*?)</li>", voci))

CIRO = DOTTORI["Dr. Ciro Annicchiarico"]
ALICE = DOTTORI["Dr.ssa Alice Annicchiarico"]
FOTO = {
    # (file scontornato, quota di altezza da mostrare: sotto sfuma nel blu)
    "ciro": (f"{ROOT}/img/team/dr-ciro-cutout.png", 0.80),
    "alice": (f"{ROOT}/img/team/dr-alice-cutout.png", 0.80),
    "team": (f"{ROOT}/img/team/team-cutout.png", 0.84),
}

POST = dict(w=1080, h=1350, top=56, mark=120, mark_gap=10, scritte=290, after_logo=34,
            eyebrow=22, after_eyebrow=18, photo=600, overlap=30,
            name=56, after_name=12, role=27, after_role=26, pill=21, sig=34, sig_bottom=44)
STORIA = dict(w=1080, h=1920, top=150, mark=150, mark_gap=12, scritte=360, after_logo=54,
              eyebrow=26, after_eyebrow=24, photo=700, overlap=36,
              name=68, after_name=16, role=32, after_role=36, pill=25, sig=40, sig_bottom=250)  # sopra "Invia messaggio"


def pills(voci):
    return "".join(f"<li>{v}</li>" for v in voci)


def page(L, foto, corpo):
    src, quota = FOTO[foto]
    if foto == "team":
        L = dict(L, photo=int(L["photo"] * 1.22))
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8"><style>
@font-face {{ font-family: Plex; src: url(file://{ROOT}/fonts/ibm-plex-sans-latin.woff2); font-weight: 100 700; }}
@font-face {{ font-family: Piazzolla; src: url(file://{ROOT}/fonts/piazzolla-latin.woff2); font-weight: 100 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: {L['w']}px; height: {L['h']}px; overflow: hidden; }}
body {{ position: relative; font-family: Plex, sans-serif; color: #fdfaf5; text-align: center;
  display: flex; flex-direction: column; align-items: center; padding-top: {L['top']}px;
  background: radial-gradient(circle {L['w'] * 0.95}px at 50% {L['h'] * 0.30}px,
    #385978 0%, #355672 18%, #32506c 45%, #2c4862 75%, #28425b 100%); }}
.mark {{ width: {L['mark']}px; }}
.scritte {{ width: {L['scritte']}px; margin-top: {L['mark_gap']}px; }}
.eyebrow {{ margin-top: {L['after_logo']}px; font-size: {L['eyebrow']}px; font-weight: 600; letter-spacing: .28em; color: #7ed6c4; }}
/* scontornata come nell'hero del sito: niente cornice, ombra morbida, base che sfuma */
.foto {{ position: relative; z-index: 0; margin-top: {L['after_eyebrow']}px; height: {L['photo']}px; overflow: visible;
  -webkit-mask-image: linear-gradient(to bottom, #000 76%, transparent 100%); }}
.foto img {{ display: block; height: {L['photo'] / quota}px; filter: drop-shadow(0 24px 30px rgba(8, 20, 32, .45)); }}
.foto-box {{ height: {L['photo']}px; overflow: hidden; padding: 0 60px; }}
.testo {{ position: relative; z-index: 1; margin-top: -{L['overlap']}px; }}
h1 {{ font: 500 {L['name']}px/1.15 Piazzolla, serif; }}
.role {{ margin-top: {L['after_name']}px; font-size: {L['role']}px; color: #d6e2ea; }}
ul {{ list-style: none; margin: {L['after_role']}px auto 0; max-width: 900px; display: flex; flex-wrap: wrap; justify-content: center; gap: 14px; }}
li {{ padding: 10px 24px; border: 2px solid #7ed6c4; border-radius: 999px; font-size: {L['pill']}px; font-weight: 500; }}
.duo {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; width: 980px; margin: 0 auto; }}
.duo h1 {{ font-size: {L['name'] * 0.7}px; }}
.duo .role {{ font-size: {L['role'] * 0.74}px; margin-top: 8px; }}
.claim {{ margin-top: {L['after_role']}px; font: 500 {L['role'] * 1.15}px/1.3 Piazzolla, serif; color: #7ed6c4; }}
.firma {{ position: absolute; left: 0; right: 0; bottom: {L['sig_bottom']}px; height: {L['sig']}px;
  display: flex; justify-content: center; align-items: center; gap: {L['sig'] * 0.55}px; }}
.chip {{ height: 100%; padding: 6px 8px; background: #fff; border-radius: 6px; }}
.chip img {{ height: 100%; display: block; }}
.sep {{ width: 2px; height: {L['sig'] - 8}px; background: #96acbe; }}
.firma .studio {{ height: 100%; }}
</style></head><body>
<img class="mark" src="file://{ROOT}/new_logo/finale/marchio-bianco.png" alt="">
<img class="scritte" src="file://{ROOT}/new_logo/finale/scritte-bianco.png" alt="">
<p class="eyebrow">IL NOSTRO TEAM</p>
<div class="foto"><div class="foto-box"><img src="file://{src}" alt=""></div></div>
<div class="testo">{corpo}</div>
<div class="firma">
  <span class="chip"><img src="file://{ROOT}/new_logo/sorgente/ilbarlo-firma.png" alt=""></span>
  <span class="sep"></span>
  <img class="studio" src="file://{ROOT}/new_logo/finale/logo-orizzontale-bianco.png" alt="">
</div>
</body></html>"""


def singolo(d):
    return f'<h1>{d["nome"]}</h1><p class="role">{d["ruolo"]}</p><ul>{pills(d["voci"])}</ul>'


def gruppo():
    # stesso ordine della foto: Alice a sinistra, Ciro a destra
    duo = "".join(f'<div><h1>{d["nome"]}</h1><p class="role">{d["ruolo"]}</p></div>' for d in (ALICE, CIRO))
    return f'<div class="duo">{duo}</div><p class="claim">Due specialisti, un solo studio.</p>'


CARDS = [
    ("team-dr-ciro", "ciro", singolo(CIRO)),
    ("team-dr-alice", "alice", singolo(ALICE)),
    ("team-studio", "team", gruppo()),
]

for base, foto, corpo in CARDS:
    for prefisso, L in (("post", POST), ("storia", STORIA)):
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
            tmp.write(page(L, foto, corpo))
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={L['w']},{L['h']}", f"--screenshot={OUT}/{prefisso}-{base}.png",
                        "--allow-file-access-from-files", f"file://{tmp.name}"],
                       check=True, capture_output=True)
        os.unlink(tmp.name)
        print("ok", f"{prefisso}-{base}")
