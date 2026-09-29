const header = document.querySelector(".site-header");

/* ---------------------------------------------------------------
   Menù mobile
   --------------------------------------------------------------- */

(function () {
  const toggle = document.querySelector(".nav-toggle");
  if (!header || !toggle) return;

  let lockY = 0;

  function setOpen(isOpen) {
    header.classList.toggle("nav-open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    toggle.setAttribute("aria-label", isOpen ? "Chiudi menù" : "Menù");
    if (isOpen) {
      lockY = window.scrollY || window.pageYOffset || 0;
      document.body.style.position = "fixed";
      document.body.style.top = `-${lockY}px`;
      document.body.style.left = "0";
      document.body.style.right = "0";
      document.body.style.width = "100%";
      document.documentElement.classList.add("nav-lock");
    } else {
      document.documentElement.classList.remove("nav-lock");
      document.body.style.position = "";
      document.body.style.top = "";
      document.body.style.left = "";
      document.body.style.right = "";
      document.body.style.width = "";
      window.scrollTo(0, lockY);
    }
  }

  toggle.addEventListener("click", (event) => {
    event.preventDefault();
    event.stopPropagation();
    setOpen(!header.classList.contains("nav-open"));
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && header.classList.contains("nav-open")) {
      setOpen(false);
      toggle.focus();
    }
  });

  header.querySelectorAll(".nav-list a, .nav-meta a, .brand").forEach((link) => {
    link.addEventListener("click", () => {
      if (header.classList.contains("nav-open")) setOpen(false);
    });
  });

  // la soglia segue il breakpoint dell'overlay in style.css
  window.addEventListener("resize", () => {
    if (window.matchMedia("(min-width: 861px)").matches && header.classList.contains("nav-open")) {
      setOpen(false);
    }
  });
})();

/* ---------------------------------------------------------------
   Ombra dell'header: compare solo quando c'è pagina sopra
   --------------------------------------------------------------- */

(function () {
  if (!header) return;

  let queued = false;

  function sync() {
    header.classList.toggle("is-scrolled", window.scrollY > 4);
    queued = false;
  }

  window.addEventListener(
    "scroll",
    () => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(sync);
    },
    { passive: true }
  );

  sync();
})();

/* ---------------------------------------------------------------
   Sezione in lettura evidenziata nella nav
   --------------------------------------------------------------- */

(function () {
  if (!header || !("IntersectionObserver" in window)) return;

  const links = Array.from(header.querySelectorAll('.nav-list a[href^="#"]'));
  const watched = links
    .map((link) => ({ link, section: document.querySelector(link.getAttribute("href")) }))
    .filter((entry) => entry.section);

  if (!watched.length) return;

  const visible = new Set();

  function sync() {
    // fra le sezioni in campo vince la prima nell'ordine del documento
    const current = watched.find((entry) => visible.has(entry.section));
    watched.forEach(({ link }) => {
      if (current && link === current.link) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      });
      sync();
    },
    { rootMargin: "-25% 0px -60% 0px" }
  );

  watched.forEach(({ section }) => observer.observe(section));
})();

/* ---------------------------------------------------------------
   Comparsa allo scroll: una volta sola, quando il blocco è entrato
   per un buon tratto. Con motion ridotto tutto è visibile subito.
   --------------------------------------------------------------- */

(function () {
  const targets = document.querySelectorAll("[data-reveal], [data-reveal-group]");
  if (!targets.length) return;

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (!("IntersectionObserver" in window) || reduceMotion) {
    targets.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { rootMargin: "0px 0px -12% 0px", threshold: 0.05 }
  );

  targets.forEach((el) => observer.observe(el));
})();

/* ---------------------------------------------------------------
   Barra mobile: sparisce quando il modulo di contatto è già in vista,
   perché lì il pulsante c'è già
   --------------------------------------------------------------- */

(function () {
  const bar = document.querySelector(".mobile-bar");
  const contact = document.getElementById("contatti");
  if (!bar || !contact || !("IntersectionObserver" in window)) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => bar.classList.toggle("is-hidden", entry.isIntersecting));
    },
    { rootMargin: "0px 0px -40% 0px", threshold: 0.05 }
  );
  observer.observe(contact);
})();

/* ---------------------------------------------------------------
   Galleria: lightbox con <dialog>
   --------------------------------------------------------------- */

(function () {
  const dialog = document.querySelector(".lightbox");
  const buttons = document.querySelectorAll(".gallery-open");
  if (!dialog || !buttons.length || typeof dialog.showModal !== "function") return;

  const img = dialog.querySelector("img");
  const caption = dialog.querySelector("figcaption");
  const close = dialog.querySelector(".lightbox-close");
  let opener = null;

  function open(button) {
    opener = button;
    img.src = button.dataset.full;
    img.alt = button.querySelector("img")?.alt || "";
    caption.textContent = button.dataset.caption || "";
    document.documentElement.classList.add("lightbox-open");
    dialog.showModal();
  }

  buttons.forEach((button) => button.addEventListener("click", () => open(button)));

  close.addEventListener("click", () => dialog.close());

  // clic sullo sfondo: fuori dalla figura si chiude
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  dialog.addEventListener("close", () => {
    document.documentElement.classList.remove("lightbox-open");
    img.removeAttribute("src");
    if (opener) opener.focus();
  });
})();

/* ---------------------------------------------------------------
   Modulo: errori chiari accanto al campo, invio una volta sola.
   Il POST resta gestito da Netlify Forms e porta a grazie.html.
   --------------------------------------------------------------- */

(function () {
  const form = document.querySelector(".contact-form");
  if (!form) return;

  const fields = Array.from(form.querySelectorAll(".field")).filter((field) =>
    field.querySelector("input[required], textarea[required], input[type='email']")
  );

  function control(field) {
    return field.querySelector("input, textarea");
  }

  function check(field) {
    const input = control(field);
    let valid = true;

    if (input.type === "checkbox") valid = input.checked;
    else if (input.required) valid = input.value.trim().length > 0;

    if (valid && input.type === "email" && input.value.trim()) {
      valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
    }
    if (valid && input.type === "tel" && input.value.trim()) {
      valid = input.value.replace(/\D/g, "").length >= 6;
    }

    field.classList.toggle("is-invalid", !valid);
    const error = field.querySelector(".field-error");
    if (error) {
      input.setAttribute("aria-invalid", valid ? "false" : "true");
      if (!valid) input.setAttribute("aria-describedby", error.id);
      else input.removeAttribute("aria-describedby");
    }
    return valid;
  }

  fields.forEach((field) => {
    const input = control(field);
    input.addEventListener("blur", () => {
      if (input.value || input.type === "checkbox") check(field);
    });
    input.addEventListener("input", () => {
      if (field.classList.contains("is-invalid")) check(field);
    });
    input.addEventListener("change", () => {
      if (field.classList.contains("is-invalid")) check(field);
    });
  });

  form.addEventListener("submit", (event) => {
    const results = fields.map((field) => check(field));
    const firstInvalid = fields[results.indexOf(false)];

    if (firstInvalid) {
      event.preventDefault();
      control(firstInvalid).focus();
      return;
    }

    const button = form.querySelector("button[type='submit']");
    if (button) {
      button.disabled = true;
      button.textContent = "Invio in corso…";
    }
  });
})();
