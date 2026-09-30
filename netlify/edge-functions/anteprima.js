// Protegge tutto il sito finché è in preparazione.
// Senza il cookie di anteprima si vede solo /in-arrivo/.
// Nel codice ci sono solo hash: la password non è nel repository.
// Per aprire il sito a tutti, cancella questo file (o la cartella netlify/edge-functions).

const PASSWORD_SHA = "c2740447ad8acb3f09c4a2d31dbc93e22854de87030946bf4a63177c19ae172e";
const TOKEN_SHA = "1b87e9ed3bd31a1f6ebfa1d3534591a13a9a59e5e52c20dcb274cdf00d4e5e4e";
const COOKIE = "sa_anteprima";
const LOGIN_PATH = "/__anteprima";
const MAX_AGE = 60 * 60 * 24 * 30;

async function sha256(text) {
  const data = new TextEncoder().encode(text);
  const buf = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(buf), (b) => b.toString(16).padStart(2, "0")).join("");
}

function readCookie(request, name) {
  const header = request.headers.get("cookie") || "";
  for (const part of header.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === name) return v.join("=");
  }
  return null;
}

function redirect(location, extraHeaders = {}) {
  return new Response(null, { status: 303, headers: { location, ...extraHeaders } });
}

export default async (request, context) => {
  const url = new URL(request.url);

  if (url.pathname === LOGIN_PATH) {
    if (request.method !== "POST") return redirect("/in-arrivo/accesso.html");
    const form = await request.formData();
    const password = String(form.get("password") || "");
    if ((await sha256(password)) !== PASSWORD_SHA) {
      return redirect("/in-arrivo/accesso.html?errore=1");
    }
    const token = await sha256(password + ":anteprima");
    return redirect("/", {
      "set-cookie": `${COOKIE}=${token}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
      "cache-control": "no-store",
    });
  }

  const token = readCookie(request, COOKIE);
  if (token && (await sha256(token)) === TOKEN_SHA) {
    const response = await context.next();
    response.headers.set("cache-control", "private, no-store");
    response.headers.set("x-robots-tag", "noindex");
    return response;
  }

  return new URL("/in-arrivo/", request.url);
};

export const config = {
  path: "/*",
  excludedPath: ["/in-arrivo/*", "/css/fonts.css", "/fonts/*", "/img/logo/*"],
};
