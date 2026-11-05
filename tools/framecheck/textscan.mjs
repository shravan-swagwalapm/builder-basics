// Frame-by-frame text-overlap scan of a HyperFrames composition (DOM truth, every frame).
// usage: node tools/framecheck/textscan.mjs <comp/index.html> <out.json> [fps=30]
// For each frame: seek the paused GSAP timeline, collect every visible text run (Range rects of text nodes,
// effective opacity = product up the tree, skip clipped-out runs), and flag any two runs from different text
// nodes whose boxes overlap by > 12% of the smaller one. Also flags text outside the 1080x1920 canvas.
// Why: hf check treats a label + sub-label inside one node as one block, and pixels can't tell text apart
// (a "POLICY PAGE" / "✕ not after travel" collision reached Shravan on 2026-11-06).
import { createRequire } from "node:module";
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
const [file, out, fpsArg] = process.argv.slice(2);
const FPS = Number(fpsArg || 30);
const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ["--allow-file-access-from-files"] });
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
  await page.goto("file://" + path.resolve(file), { waitUntil: "networkidle0", timeout: 90000 });
  await page.evaluate(() => document.fonts.ready);
  const dur = await page.evaluate(() => window.__timelines.main.duration());
  const res = await page.evaluate((dur, FPS) => {
    const tl = window.__timelines.main;
    const nodes = [];
    const tw = document.createTreeWalker(document.getElementById("root"), NodeFilter.SHOW_TEXT);
    while (tw.nextNode()) if (tw.currentNode.nodeValue.trim()) nodes.push(tw.currentNode);
    const opacityOf = (el) => { let o = 1; for (let e = el; e && e.nodeType === 1; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= parseFloat(cs.opacity); } return o; };
    const clippedOut = (el, r) => { for (let e = el.parentElement; e && e.id !== "root"; e = e.parentElement) { const cs = getComputedStyle(e); if (cs.overflow === "hidden" || cs.clipPath !== "none") { const b = e.getBoundingClientRect(); if (r.right <= b.left || r.left >= b.right || r.bottom <= b.top || r.top >= b.bottom) return true; } } return false; };
    const hits = [], off = [];
    const n = Math.floor(dur * FPS);
    for (let f = 0; f <= n; f++) {
      const t = f / FPS;
      tl.seek(t, false);
      const runs = [];
      nodes.forEach((tn, i) => {
        const el = tn.parentElement;
        const op = opacityOf(el);
        if (op < 0.15) return;
        const r = document.createRange(); r.selectNodeContents(tn);
        for (const q of r.getClientRects()) {
          if (q.width < 2 || q.height < 2 || clippedOut(el, q)) continue;
          runs.push({ i, q, text: tn.nodeValue.trim().slice(0, 28) });
          if (q.left < -2 || q.top < -2 || q.right > 1082 || q.bottom > 1922) off.push({ t: +t.toFixed(3), text: tn.nodeValue.trim().slice(0, 28) });
        }
      });
      for (let a = 0; a < runs.length; a++) for (let b = a + 1; b < runs.length; b++) {
        if (runs[a].i === runs[b].i) continue;
        const A = runs[a].q, B = runs[b].q;
        const ix = Math.max(0, Math.min(A.right, B.right) - Math.max(A.left, B.left));
        const iy = Math.max(0, Math.min(A.bottom, B.bottom) - Math.max(A.top, B.top));
        const small = Math.min(A.width * A.height, B.width * B.height);
        if (ix * iy > 0.12 * small) hits.push({ t: +t.toFixed(3), a: runs[a].text, b: runs[b].text });
      }
    }
    return { frames: n + 1, hits, off };
  }, dur, FPS);
  // collapse consecutive frames of the same pair into spans
  const spans = [];
  for (const h of res.hits) {
    const last = spans.find((s) => s.a === h.a && s.b === h.b && Math.abs(s.to - h.t) <= 1.5 / FPS);
    if (last) last.to = h.t; else spans.push({ a: h.a, b: h.b, from: h.t, to: h.t });
  }
  fs.writeFileSync(out, JSON.stringify({ frames: res.frames, overlaps: spans, offCanvas: res.off.slice(0, 50) }, null, 1));
  process.stdout.write(JSON.stringify({ frames: res.frames, overlap_spans: spans.length, off_canvas: res.off.length, first: spans.slice(0, 6) }) + "\n");
  process.exit(spans.length || res.off.length ? 1 : 0);
} finally {
  await browser.close();
}
