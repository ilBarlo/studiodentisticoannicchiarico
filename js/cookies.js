/* ============================================================
   Consenso cookie e contenuti di terze parti

   Come si usa quando aggiungi qualcosa di esterno:

   1. Metti THIRD_PARTY a true qui sotto. Da quel momento il
      banner compare a chi non ha ancora scelto.

   2. Uno script esterno (statistiche, pixel) va scritto così,
      con type="text/plain": il browser non lo esegue, ci pensa
      questo file dopo il consenso.
        <script type="text/plain" data-consent data-src="https://..."></script>

   3. Un iframe esterno (mappa Google, video) va scritto così:
        <iframe data-consent-src="https://..." title="..."></iframe>
      Finché il consenso manca, al suo posto compare un riquadro
      con un pulsante per caricarlo.

   Senza niente di esterno il banner non compare, ed è corretto:
   le linee guida del Garante non vogliono banner inutili.
   ============================================================ */

(function () {
  // true solo quando il sito carica davvero qualcosa di terze parti
  var THIRD_PARTY = true;

  var KEY = "ca-consenso";
  var bar = null;

  function stored() {
    try {
      return localStorage.getItem(KEY);
    } catch (e) {
      return null;
    }
  }

  function store(value) {
    try {
      localStorage.setItem(KEY, value);
    } catch (e) {
      /* navigazione privata o storage negato: la scelta vale per questa visita */
    }
  }

  function granted() {
    return stored() === "tutti";
  }

  /* ---- attivazione dei contenuti esterni ---- */

  function runScripts() {
    document.querySelectorAll("script[type='text/plain'][data-consent]").forEach(function (node) {
      var live = document.createElement("script");
      if (node.dataset.src) live.src = node.dataset.src;
      else live.textContent = node.textContent;
      live.async = true;
      node.parentNode.replaceChild(live, node);
    });
  }

  function paintFrames() {
    document.querySelectorAll("iframe[data-consent-src]").forEach(function (frame) {
      var holder = frame.parentElement;
      if (!holder) return;

      var block = holder.querySelector(".consent-block");
      if (!block) {
        block = document.createElement("div");
        block.className = "consent-block";
        block.innerHTML =
          "<p>Questo contenuto è ospitato da un servizio esterno, che può " +
          "registrare il tuo indirizzo IP.</p>" +
          '<button type="button" class="btn btn-ghost">Carica il contenuto</button>';
        holder.appendChild(block);
      }
      if (!block.dataset.bound) {
        block.dataset.bound = "1";
        block.querySelector("button").addEventListener("click", function () {
          accept();
        });
      }

      if (granted()) {
        if (!frame.getAttribute("src")) frame.src = frame.dataset.consentSrc;
        frame.hidden = false;
        block.hidden = true;
      } else {
        frame.removeAttribute("src");
        frame.hidden = true;
        block.hidden = false;
      }
    });
  }

  /* ---- banner ---- */

  function build() {
    var node = document.createElement("div");
    node.className = "cookie-bar";
    node.setAttribute("role", "dialog");
    node.setAttribute("aria-modal", "false");
    node.setAttribute("aria-label", "Scelte sui cookie");
    node.hidden = true;
    node.innerHTML =
      "<h2>Cookie</h2>" +
      '<p class="cookie-text">La mappa dello studio è di Google e si carica solo se la autorizzi. ' +
      "Non profiliamo e non facciamo pubblicità: salviamo solo la tua scelta.</p>" +
      '<div class="cookie-actions">' +
      '<button type="button" class="btn btn-primary" data-act="tutti">Accetta tutto</button>' +
      '<button type="button" class="btn btn-ghost" data-act="necessari">Solo necessari</button>' +
      '<a class="cookie-more" href="privacy.html">Leggi l\'informativa privacy e cookie</a>' +
      "</div>";

    document.body.appendChild(node);

    node.querySelectorAll("button[data-act]").forEach(function (button) {
      button.addEventListener("click", function () {
        var prima = stored();
        var adesso = button.dataset.act;
        store(adesso);

        // uno script di terze parti già avviato non si ferma togliendogli
        // il tag: se il consenso viene revocato serve ripartire da zero
        if (prima === "tutti" && adesso !== "tutti") {
          location.reload();
          return;
        }

        apply();
        hide();
      });
    });

    return node;
  }

  function show() {
    if (!bar) bar = build();
    bar.hidden = false;
    var first = bar.querySelector("button");
    if (first) first.focus();
  }

  function hide() {
    if (bar) bar.hidden = true;
  }

  function accept() {
    store("tutti");
    apply();
    hide();
  }

  function apply() {
    paintFrames();
    if (granted()) runScripts();
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && bar && !bar.hidden && stored()) hide();
  });

  document.addEventListener("DOMContentLoaded", function () {
    apply();

    // il banner serve solo se c'è qualcosa da autorizzare
    if (THIRD_PARTY && !stored()) show();

    document.querySelectorAll(".cookie-prefs").forEach(function (button) {
      button.addEventListener("click", function () {
        show();
      });
    });
  });

  // utile se in futuro vuoi decidere via codice
  window.consensoCookie = {
    consente: granted,
    apri: show,
    accetta: accept
  };
})();
