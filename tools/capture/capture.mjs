// Evidence capture: photograph the REAL source pages a Short cites, and record where each quoted phrase sits.
//
// usage: node tools/capture/capture.mjs <short-dir> [--dump] [--only id,id]
//   reads  <short-dir>/evidence/shots.json   [{id, url, expect, phrases:[...], mode:"mobile"|"desktop", dark:true}]
//          a shot whose url ends in .pdf is rendered with pdftoppm and located with pdftotext -bbox
//   writes <short-dir>/evidence/<id>.png + evidence/manifest.json (phrase rects in image pixels)
//   --dump also writes evidence/src/<id>.txt (page text) so phrases can be copied verbatim
//
// Guards (all fail loud, exit 1):
//   identity  — page title/body (or PDF text) must contain `expect`: a 200 from the wrong page is not evidence
//   secrets   — every key-shaped string is masked before the photo, then the DOM is re-scanned: must be 0
//   phrases   — every phrase must be found and visible; a missing quote means the dossier and page disagree
// Privacy: fresh incognito context, no cookies, logged out; consent banners are hidden, never accepted.
import { createRequire } from "node:module";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const require = createRequire(path.join(ROOT, "engine/package.json"));
const puppeteer = require("puppeteer-core");
const CHROME = process.env.CHROME_PATH || (() => {   // the headless shell HyperFrames installed (any version), or set CHROME_PATH
  const base = path.join(process.env.HOME, ".cache/puppeteer/chrome-headless-shell");
  for (const v of (fs.existsSync(base) ? fs.readdirSync(base).sort().reverse() : [])) {
    for (const p of ["chrome-headless-shell-mac-arm64/chrome-headless-shell", "chrome-headless-shell-mac-x64/chrome-headless-shell", "chrome-headless-shell-linux64/chrome-headless-shell"]) {
      if (fs.existsSync(path.join(base, v, p))) return path.join(base, v, p);
    }
  }
  throw new Error("no headless Chrome found: run `npx puppeteer browsers install chrome-headless-shell` in engine/ or set CHROME_PATH");
})();

const SECRET_RES = [
  "sk-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}", "sk_(?:live|test)_[A-Za-z0-9]{10,}", "AKIA[0-9A-Z]{16}",
  "gh[pousr]_[A-Za-z0-9]{30,}", "AIza[0-9A-Za-z_-]{35}", "xai-[A-Za-z0-9]{20,}", "glpat-[A-Za-z0-9_-]{20,}",
];
const MODES = {
  mobile: { width: 430, height: 932, deviceScaleFactor: 3, isMobile: true, hasTouch: true, clipH: 1100 },
  desktop: { width: 1280, height: 900, deviceScaleFactor: 2, isMobile: false, hasTouch: false, clipH: 900 },
};
const MOBILE_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1";

const say = (m) => process.stdout.write(m + "\n");
const die = (m) => { process.stderr.write("CAPTURE FAIL: " + m + "\n"); process.exit(1); };
const args = process.argv.slice(2);
const shortDir = path.resolve(args[0] || die("usage: capture.mjs <short-dir> [--dump] [--only a,b]"));
const DUMP = args.includes("--dump");
const ONLY = args.includes("--only") ? args[args.indexOf("--only") + 1].split(",") : null;
const EV = path.join(shortDir, "evidence");
const shots = JSON.parse(fs.readFileSync(path.join(EV, "shots.json"), "utf8")).filter((s) => !ONLY || ONLY.includes(s.id));
fs.mkdirSync(path.join(EV, "src"), { recursive: true });
const manifestPath = path.join(EV, "manifest.json");
const manifest = fs.existsSync(manifestPath) ? JSON.parse(fs.readFileSync(manifestPath, "utf8")) : {};
const sha = (f) => createHash("sha256").update(fs.readFileSync(f)).digest("hex").slice(0, 16);
const norm = (s) => s.replace(/[\u2018\u2019]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/\s+/g, " ").trim().toLowerCase();

// ---------------- web pages ----------------
async function captureWeb(browser, s) {
  const m = MODES[s.mode || "mobile"];
  const ctx = await browser.createBrowserContext();   // incognito: no cookies, logged out
  const page = await ctx.newPage();
  if (m.isMobile) await page.setUserAgent(MOBILE_UA);
  // viewport == photo: rects are measured in the exact layout that is photographed (a banner once moved text between the two)
  await page.setViewport({ width: m.width, height: m.clipH, deviceScaleFactor: m.deviceScaleFactor, isMobile: m.isMobile, hasTouch: m.hasTouch });
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: s.dark === false ? "light" : "dark" }]);
  const resp = await page.goto(s.url, { waitUntil: "networkidle2", timeout: 60000 });
  if (!resp || resp.status() >= 400) die(`${s.id}: HTTP ${resp && resp.status()} for ${s.url}`);
  // plain-text files (raw LICENSE): wrap lines as desktop Chrome's text viewer does, and give them a phone viewport —
  // with no <meta viewport>, mobile emulation lays them out 980 px wide and zooms out. Applied before any measuring,
  // then a settle wait: the viewport change lands a frame later, and measuring earlier scrolled the quote off the photo.
  if (await page.evaluate(() => document.contentType === "text/plain")) {
    await page.evaluate(() => {
      for (const pre of document.querySelectorAll("pre")) pre.style.cssText += ";white-space:pre-wrap;overflow-wrap:anywhere";
      document.head.insertAdjacentHTML("beforeend", '<meta name="viewport" content="width=device-width,initial-scale=1">');
    });
    await new Promise((r) => setTimeout(r, 400));
  }
  await page.evaluate(() => document.fonts.ready);
  const title = await page.title();
  const body = await page.evaluate(() => document.body.innerText);
  if (!norm(title + " " + body).includes(norm(s.expect))) die(`${s.id}: identity check failed — "${s.expect}" not in title/body (title: "${title}")`);
  if (DUMP) fs.writeFileSync(path.join(EV, "src", s.id + ".txt"), title + "\n\n" + body);

  const prep = await page.evaluate((SECRET_RES, REDACT) => {
    // overlays: every fixed element (banners, chat bubbles, headers) is removed, never clicked; sticky stays in place
    for (const el of document.querySelectorAll("*")) {
      const cs = getComputedStyle(el);
      if (cs.position === "fixed") el.style.setProperty("display", "none", "important");
      else if (cs.position === "sticky") el.style.setProperty("position", "relative", "important");
    }
    const textNodes = () => {
      // no filter callback: Chrome throws "callback is no longer runnable" for ANY TreeWalker callback on a
      // text/plain document (raw LICENSE files; probed 2026-11-06), so script/style text is skipped in the loop instead
      const out = [], tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (tw.nextNode()) if (!/^(SCRIPT|STYLE|NOSCRIPT|TEMPLATE)$/.test(tw.currentNode.parentElement?.tagName || "")) out.push(tw.currentNode);
      return out;
    };
    const secretRe = new RegExp(SECRET_RES.join("|"), "g");
    let masked = 0;
    for (const n of textNodes()) {
      const v = n.nodeValue.replace(secretRe, (k) => { masked++; return k.slice(0, 4) + "•".repeat(Math.min(k.length - 4, 12)); });
      if (v !== n.nodeValue) n.nodeValue = v;
    }
    for (const el of document.querySelectorAll("input,textarea")) {
      if (new RegExp(SECRET_RES.join("|")).test(el.value)) { el.value = "••••••••"; masked++; }
    }
    // redact private people's names (shots.json "redact"): black bars, then re-scan must find 0
    let redacted = 0, nameRe = null;
    if (REDACT.length) {
      nameRe = new RegExp("\\b(?:" + REDACT.map((n) => n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|") + ")\\b", "gi");
      for (const n of textNodes()) {
        const v = n.nodeValue.replace(nameRe, (k) => { redacted++; return "█".repeat(Math.max(4, k.length)); });
        if (v !== n.nodeValue) n.nodeValue = v;
      }
    }
    const nameLeft = REDACT.length ? (document.body.innerText.match(nameRe) || []).length : 0;
    const leftover = (document.body.innerText.match(secretRe) || []).length;
    // phrase locator, kept on window so it runs again after the scroll; returns viewport rects + occlusion verdict
    window.__locate = (phrases) => {
      const nodes = textNodes();
      let all = "";
      const starts = [];
      for (const n of nodes) { starts.push(all.length); all += n.nodeValue; }
      const esc = (p) => p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&").replace(/\s+/g, "\\s+").replace(/['\u2019]/g, "['\u2019]").replace(/["\u201C\u201D]/g, "[\"\u201C\u201D]");
      const at = (i) => { let k = starts.length - 1; while (starts[k] > i) k--; return [nodes[k], i - starts[k]]; };
      return phrases.map((p) => {
        const re = new RegExp(esc(p), "gi");
        let mm;
        while ((mm = re.exec(all))) {
          const r = document.createRange();
          const [a, ao] = at(mm.index), [b, bo] = at(mm.index + mm[0].length - 1);
          r.setStart(a, ao); r.setEnd(b, bo + 1);
          const qs = [...r.getClientRects()].filter((q) => q.width > 2 && q.height > 2);
          if (!qs.length || !qs.every((q) => q.left >= 0 && q.right <= innerWidth + 1)) continue;   // hidden carousel / off-canvas copy
          const host = (r.commonAncestorContainer.nodeType === 1 ? r.commonAncestorContainer : r.commonAncestorContainer.parentElement);
          const covered = qs.filter((q) => {
            const cx = q.left + q.width / 2, cy = q.top + q.height / 2;
            if (cy < 0 || cy > innerHeight) return false;   // judged after the scroll, when it is in view
            const el = document.elementFromPoint(cx, cy);
            return !(el && (host.contains(el) || el.contains(host)));
          }).length;
          (window.__hosts = window.__hosts || {})[p] = host;   // kept so an inner-scrolling page can bring it into view
          return { text: p, rects: qs.map((q) => [q.left, q.top, q.width, q.height]), covered, scrollY };
        }
        return { text: p, rects: null };
      });
    };
    return { masked, leftover, redacted, nameLeft, pageH: document.documentElement.scrollHeight };
  }, SECRET_RES, s.redact || []);
  if (prep.nameLeft) die(`${s.id}: ${prep.nameLeft} redacted name(s) still visible`);
  if (prep.leftover) die(`${s.id}: ${prep.leftover} key-shaped strings still visible after masking`);

  // pass 1: where is the first phrase on the page -> scroll so it sits at the reading point
  const pre = await page.evaluate((ph) => window.__locate(ph), s.phrases);
  const miss = pre.filter((f) => !f.rects).map((f) => f.text);
  if (miss.length) die(`${s.id}: phrase(s) not found/visible: ${JSON.stringify(miss)} (run with --dump and copy verbatim)`);
  const fr = pre[0].rects, sy = pre[0].scrollY;
  const cy = sy + (Math.min(...fr.map((q) => q[1])) + Math.max(...fr.map((q) => q[1] + q[3]))) / 2;
  const y0 = Math.max(0, Math.min(Math.round(cy - m.clipH * 0.42), prep.pageH - m.clipH));
  await page.evaluate((y, ph) => {
    scrollTo(0, y);
    // judge the QUOTE's own rects, not its host: a host taller than the viewport (a raw LICENSE's single <pre>) always
    // looked off-screen, so it was re-centred and the quote scrolled out of the photo (probed 2026-11-06)
    const R = window.__locate([ph])[0].rects;
    const off = !R || Math.min(...R.map((q) => q[1])) < 0 || Math.max(...R.map((q) => q[1] + q[3])) > innerHeight;
    if (off) window.__hosts[ph].scrollIntoView({ block: "center" });   // page scrolls inside a panel, not the window
  }, y0, s.phrases[0]);
  await new Promise((r) => setTimeout(r, 900));       // lazy images settle
  // pass 2: measure in the layout we photograph; occlusion guard = the pixel at each highlight centre belongs to the quote
  const found = await page.evaluate((ph) => window.__locate(ph), s.phrases);
  for (const f of found) {
    if (!f.rects) die(`${s.id}: phrase "${f.text}" vanished after scrolling`);
    if (f.covered) die(`${s.id}: phrase "${f.text}" is covered by another element in ${f.covered} place(s)`);
  }
  const file = path.join(EV, s.id + ".png");
  await page.screenshot({ path: file });               // the viewport IS the photo
  await ctx.close();
  const k = m.deviceScaleFactor;
  return {
    id: s.id, url: s.url, title, kind: "web", mode: s.mode || "mobile", file: s.id + ".png",
    w: m.width * k, h: m.clipH * k, masked: prep.masked, redacted: prep.redacted, captured_at: new Date().toISOString(), sha: sha(file),
    phrases: found.map((f) => ({ text: f.text, rects: f.rects.map(([x, y, w, h]) => [x * k, y * k, w * k, h * k].map(Math.round)) })),
  };
}

// ---------------- PDFs (pdftotext -bbox + pdftoppm) ----------------
function capturePdf(s) {
  const pdf = path.join(EV, "src", s.id + ".pdf");
  if (!fs.existsSync(pdf)) execFileSync("curl", ["-sSfL", "--max-time", "90", "-o", pdf, s.url]);
  const bbox = path.join(EV, "src", s.id + ".bbox.html");
  execFileSync("pdftotext", ["-bbox", pdf, bbox]);
  const xml = fs.readFileSync(bbox, "utf8");
  const unent = (t) => t.replace(/&amp;/g, "&").replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">");
  const pages = [...xml.matchAll(/<page width="([\d.]+)" height="([\d.]+)">([\s\S]*?)<\/page>/g)].map((p, i) => ({
    n: i + 1, W: +p[1], H: +p[2],
    words: [...p[3].matchAll(/<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)<\/word>/g)]
      .map((w) => ({ x0: +w[1], y0: +w[2], x1: +w[3], y1: +w[4], t: norm(unent(w[5])) })),
  }));
  const fullText = pages.map((p) => p.words.map((w) => w.t).join(" ")).join(" ");
  if (!fullText.includes(norm(s.expect))) die(`${s.id}: identity check failed — "${s.expect}" not in PDF text`);
  if (DUMP) fs.writeFileSync(path.join(EV, "src", s.id + ".txt"), pages.map((p) => `--- page ${p.n}\n` + p.words.map((w) => w.t).join(" ")).join("\n"));
  const strip = (t) => t.replace(/^["'(]+|[".,;:)']+$/g, "");
  const locate = (phrase) => {
    const want = norm(phrase).split(" ").map(strip);
    for (const p of pages) for (let i = 0; i + want.length <= p.words.length; i++) {
      if (want.every((t, j) => strip(p.words[i + j].t) === t)) return { page: p, ws: p.words.slice(i, i + want.length) };
    }
    return null;
  };
  const hits = s.phrases.map((ph) => ({ ph, hit: locate(ph) }));
  const miss = hits.filter((h) => !h.hit).map((h) => h.ph);
  if (miss.length) die(`${s.id}: phrase(s) not found in PDF: ${JSON.stringify(miss)} (run with --dump)`);
  const pg = hits[0].hit.page;
  if (hits.some((h) => h.hit.page !== pg)) die(`${s.id}: all phrases of one shot must sit on one PDF page`);
  const DPI = 220, k = DPI / 72;
  const outBase = path.join(EV, "src", s.id + "-p");
  execFileSync("pdftoppm", ["-r", String(DPI), "-f", String(pg.n), "-l", String(pg.n), "-png", "-singlefile", pdf, outBase]);
  const file = path.join(EV, s.id + ".png");
  fs.renameSync(outBase + ".png", file);
  const lineRects = (ws) => {   // one rect per text line of the phrase
    const lines = [];
    for (const w of ws) {
      const L = lines.find((l) => Math.abs(l.y0 - w.y0) < 3);
      if (L) { L.x1 = Math.max(L.x1, w.x1); L.y1 = Math.max(L.y1, w.y1); } else lines.push({ ...w });
    }
    return lines.map((l) => [l.x0 * k, l.y0 * k, (l.x1 - l.x0) * k, (l.y1 - l.y0) * k].map(Math.round));
  };
  return {
    id: s.id, url: s.url, title: s.expect, kind: "pdf", page: pg.n, file: s.id + ".png",
    w: Math.round(pg.W * k), h: Math.round(pg.H * k), masked: 0, captured_at: new Date().toISOString(), sha: sha(file),
    phrases: hits.map((h) => ({ text: h.ph, rects: lineRects(h.hit.ws) })),
  };
}

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--no-first-run", "--hide-scrollbars"] });
try {
  for (const s of shots) {
    const rec = s.url.toLowerCase().split("?")[0].endsWith(".pdf") ? capturePdf(s) : await captureWeb(browser, s);
    // in-photo guard: a phrase "found" outside the pixels (hidden carousel copy, off-canvas menu) is not evidence
    for (const ph of rec.phrases) for (const [x, y, w, h] of ph.rects) {
      if (x < 0 || y < 0 || x + w > rec.w + 2 || y + h > rec.h + 2) die(`${s.id}: phrase "${ph.text}" rect [${x},${y},${w},${h}] lies outside the ${rec.w}x${rec.h} photo`);
    }
    manifest[s.id] = rec;
    say(`ok ${s.id}: ${rec.w}x${rec.h} masked=${rec.masked} phrases=${rec.phrases.length} sha=${rec.sha}`);
  }
} finally {
  await browser.close();
}
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 1));
