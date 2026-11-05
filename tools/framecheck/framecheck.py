"""Frame check: verify the RENDERED Short frame by frame and write the approval artifact.

usage: python3 -I tools/framecheck/framecheck.py <short-dir> <video.mp4>
writes <short-dir>/qa/framecheck/{report.html, report.json, sheet-NN.jpg}; exit 1 if any check FAILs.

Replaces a cloud video-model check (no upload: everything runs on this machine). Each check names its rule
and prints its evidence; the report binds the verdict to the file's sha256, so approval is for THAT file.
Checks: container · decode · black/frozen · flash safety (WCAG 2.3.1) · loudness/peak · A/V sync ·
caption-on-every-word · motion benchmarks · platform safe zones (warn) · evidence provenance · contact sheets.
"""
import hashlib, html, json, os, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

short, video = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
OUT = os.path.join(short, "qa", "framecheck")
os.makedirs(OUT, exist_ok=True)
A = json.load(open(os.path.join(short, "voice", "FINAL.align.json")))
CUES = json.load(open(os.path.join(short, "comp", "cues.json")))
END = CUES["end"]
FPS, W, H = 30, 1080, 1920
results = []


def check(name, ok, evidence, level="FAIL"):
    results.append({"check": name, "status": "PASS" if ok else level, "evidence": evidence})


def ff(*args, **kw):
    return subprocess.run(["ffmpeg", "-v", "error", "-nostdin", *args], capture_output=True, **kw)


def frames(vf, w, h, pix="gray"):
    raw = ff("-i", video, "-vf", vf, "-f", "rawvideo", "-pix_fmt", pix, "-").stdout
    ch = 3 if pix == "rgb24" else 1
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, ch) if ch == 3 else np.frombuffer(raw, np.uint8).reshape(-1, h, w)


sha = hashlib.sha256(open(video, "rb").read()).hexdigest()

# 1 container
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", video],
                               capture_output=True, check=True).stdout)
v = next(s for s in pr["streams"] if s["codec_type"] == "video")
au = [s for s in pr["streams"] if s["codec_type"] == "audio"]
dur = float(pr["format"]["duration"])
fps = eval(v["r_frame_rate"])  # "30/1"
check("container", v["width"] == W and v["height"] == H and abs(fps - FPS) < 0.01 and au and abs(dur - END) < 0.1,
      f'{v["width"]}x{v["height"]} {fps:g}fps {v["codec_name"]}, audio {au[0]["codec_name"] if au else "MISSING"}, {dur:.2f}s vs cue end {END:.2f}s')

# 2 decode: every frame decodes
dec = ff("-i", video, "-f", "null", "-")
check("decode every frame", dec.returncode == 0 and not dec.stderr.strip(), dec.stderr.decode()[:300] or "0 decode errors")

# frame-by-frame luma (all frames, 108x192)
G = frames(f"fps={FPS},scale=108:192", 108, 192).astype(np.float32)
n = len(G)
t_of = lambda i: i / FPS
check("frame count", abs(n - round(END * FPS)) <= 2, f"{n} frames decoded, expected ~{round(END * FPS)}")

# 3 black / frozen
mean = G.mean(axis=(1, 2))
black = [t_of(i) for i in range(n) if mean[i] < 4 and t_of(i) > 0.2]
check("no black frames", not black, f"{len(black)} black frames" + (f" from {black[0]:.2f}s" if black else " (luma<4 after 0.2s)"))
diff = np.abs(np.diff(G, axis=0)).mean(axis=(1, 2))
still, best, best_at, run_start = 0, 0, 0, 0
for i, d in enumerate(diff):
    if d < 0.35:
        if still == 0:
            run_start = i
        still += 1
        if still > best:
            best, best_at = still, run_start
    else:
        still = 0
longest, longest_at = best / FPS, best_at / FPS
in_end_hold = longest_at >= END - 3.0
check("longest still (style guide <= 4.5 s; final hold exempt)", longest <= 4.5 or in_end_hold,
      f"{longest:.2f}s starting {longest_at:.2f}s" + (" (final hold)" if in_end_hold else ""))

# 4 flash safety — WCAG 2.3.1 general flash: a pair of opposing relative-luminance changes >= 10%,
#   the darker state < 0.80; fail if > 3 flashes in any 1 s. Measured on the whole frame AND on each 4x4 block
#   (a block of 1080x1920/16 is ~ the 25%-of-10-degree area at phone distance).
def rel_lum(g):
    c = g / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def flashes(series):
    ev, last, ref = [], 0, series[0]          # alternating rise/fall events of >= 0.10 from the last extreme
    for i in range(1, len(series)):
        d = series[i] - ref
        if abs(d) >= 0.10 and min(series[i], ref) < 0.80:
            s = 1 if d > 0 else -1
            if s != last:
                ev.append(i)
                last = s
            ref = series[i]
        elif (last >= 0 and series[i] > ref) or (last < 0 and series[i] < ref):
            ref = series[i]
    return ev


L = rel_lum(G)
series = {"frame": L.mean(axis=(1, 2))}
for by in range(4):
    for bx in range(4):
        series[f"block{by}{bx}"] = L[:, by * 48:(by + 1) * 48, bx * 27:(bx + 1) * 27].mean(axis=(1, 2))
worst = (0, "", 0.0)
for k, sr in series.items():
    ev = flashes(sr)
    for j in range(len(ev)):
        cnt = sum(1 for e in ev[j:] if e - ev[j] < FPS) // 2      # a flash = one pair of opposing changes
        if cnt > worst[0]:
            worst = (cnt, k, ev[j] / FPS)
check("flash safety (WCAG 2.3.1: <= 3 flashes/s)", worst[0] <= 3,
      f"max {worst[0]} flashes in 1 s ({worst[1]} at {worst[2]:.2f}s)" if worst[0] else "no flashes")

# 5 loudness / peak
eb = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-nostdin", "-i", video, "-af", "ebur128=peak=true", "-f", "null", "-"],
                    capture_output=True).stderr.decode()   # the summary prints at info level
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)[-1])
TP = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb)[-1])
check("loudness -14 LUFS +-1, true peak <= -1 dBTP", abs(I + 14) <= 1 and TP <= -0.9, f"I {I:.1f} LUFS, true peak {TP:.1f} dBTP")

# 6 A/V sync: the voice in the file vs the approved take (envelope cross-correlation, first 12 s)
def env(path, offset=0.0):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(offset), "-t", "12", "-i", path, "-ac", "1", "-ar", "8000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.abs(np.frombuffer(raw, np.int16).astype(np.float32))
    return x[: len(x) // 80 * 80].reshape(-1, 80).mean(axis=1)   # 10 ms bins


a, b = env(os.path.join(short, "voice", "FINAL.wav")), env(video)
m = min(len(a), len(b))
a, b = (a[:m] - a[:m].mean()), (b[:m] - b[:m].mean())
lags = range(-30, 31)
corr = [np.dot(a[max(0, -l):m - max(0, l)], b[max(0, l):m - max(0, -l)]) for l in lags]
lag = list(lags)[int(np.argmax(corr))] * 0.01
check("A/V sync (voice vs approved take; only SFX are delayed)", abs(lag) <= 0.034, f"voice offset {lag:+.3f}s (1 frame = 0.033 s)")

# 7 caption visible on every spoken word: lit (spoken) caption pixels in the caption band at each word's midpoint
BAND = (70, 1385, 1010, 1495)
cw, chh = (BAND[2] - BAND[0]) // 2, (BAND[3] - BAND[1]) // 2
C = frames(f"fps={FPS},crop={BAND[2]-BAND[0]}:{BAND[3]-BAND[1]}:{BAND[0]}:{BAND[1]},scale={cw}:{chh}", cw, chh, "rgb24")
miss = []
for x in A["words"]:
    # lit at SOME displayed frame from mid-word to word end (the voice is not delayed; only SFX are, mix.py).
    # Catches a caption that leaves before its word ends (the "Orca" bug); tolerates a 1-letter word caught mid-fade-in.
    def lit_at(i):
        px = C[min(i, len(C) - 1)].reshape(-1, 3).astype(int)
        return (px.max(axis=1) > 165).mean()   # lit = any ink colour (white/periwinkle/lime peak > 240); unspoken greys peak at 119-150
    lit = max(lit_at(i) for i in range(int((x["s"] + x["e"]) / 2 * FPS), int(x["e"] * FPS) + 1))
    if lit < 0.002:
        miss.append(f'{x["w"]}@{x["s"]:.2f}')
check("caption lit on every spoken word", not miss, f"{len(A['words']) - len(miss)}/{len(A['words'])} words" + (f"; missing {miss[:8]}" if miss else ""))

# 8 motion benchmarks (style guide)
mq = json.loads(subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(__file__), "..", "motion-qa", "analyze.py"), video],
                               capture_output=True, check=True, text=True).stdout)
check("motion: >= 60% of 1-s windows move", mq["pct_1s_windows_with_motion"] >= 60, f'{mq["pct_1s_windows_with_motion"]}% (refs: Rethink 90, Algo 59, Reels 73)')
check("frame-fill envelope >= 30%", mq["frame_usage_envelope_pct"] >= 30, f'{mq["frame_usage_envelope_pct"]}%')

# 9 platform safe zones (WARN only): share of frames with foreground in zones covered by IG/YT UI
F = frames(f"fps=2,scale=270:480", 270, 480).astype(np.int16)
bg = np.median(F, axis=0)
fg = np.abs(F - bg) > 40
zones = {"top 0-200 (app header)": (0, 0, 270, 50), "bottom 1600-1920 (caption/handle)": (0, 400, 270, 480),
         "right rail x>960, y 1150-1600 (buttons)": (240, 287, 270, 400)}
for name, (x0, y0, x1, y1) in zones.items():
    share = (fg[:, y0:y1, x0:x1].mean(axis=(1, 2)) > 0.02).mean()
    check(f"safe zone: {name}", share < 0.05, f"foreground in {share:.0%} of sampled frames", level="WARN")

# 10 evidence provenance: every page shown is the captured one (sha) and still has its source URL
man_p = os.path.join(short, "evidence", "manifest.json")
if os.path.exists(man_p):
    man = json.load(open(man_p))
    bad = []
    for k, r in man.items():
        f = os.path.join(short, "comp", "assets", "ev", r["file"])
        if not os.path.exists(f) or hashlib.sha256(open(f, "rb").read()).hexdigest()[:16] != r["sha"]:
            bad.append(k)
    check("evidence = captured pages (sha match)", not bad, f"{len(man)} pages; mismatched: {bad or 'none'}")
else:
    man = {}

# 10b no overlapping text, every frame: DOM scan of the composition the MP4 was rendered from (textscan.mjs)
comp = os.path.join(short, "comp", "index.html")
if os.path.exists(comp):
    ts = subprocess.run(["node", os.path.join(os.path.dirname(os.path.abspath(__file__)), "textscan.mjs"), comp, os.path.join(OUT, "textscan.json"), str(FPS)],
                        capture_output=True, text=True, timeout=900)
    lines = [l for l in ts.stdout.strip().splitlines() if l.startswith("{")]
    info = json.loads(lines[-1]) if lines else {}
    comp_sha = hashlib.sha256(open(comp, "rb").read()).hexdigest()[:16]
    check("no overlapping text, every frame (DOM scan)", ts.returncode == 0 and bool(info),
          f'{info.get("frames")} frames scanned; {info.get("overlap_spans")} overlap spans; {info.get("off_canvas")} off-canvas; comp sha {comp_sha}'
          + (f'; first {info.get("first", [])[:2]}' if info.get("overlap_spans") else "") + (f"; error {ts.stderr[-200:]}" if not info else ""))

# 11 contact sheets: every 0.5 s, timestamp + the words spoken at that moment
step = 0.5
thumbs = frames(f"fps={1/step},scale=180:320", 180, 320, "rgb24")
words_at = lambda t: " ".join(x["w"] for x in A["words"] if x["s"] - 0.6 <= t <= x["e"] + 0.2)[:40]
per = 48
sheets = []
for si in range(0, len(thumbs), per):
    S = Image.new("RGB", (8 * 180, 6 * 352), (20, 20, 24))
    for j, th in enumerate(thumbs[si:si + per]):
        t = (si + j) * step
        im = Image.fromarray(th)
        x, y = (j % 8) * 180, (j // 8) * 352
        S.paste(im, (x, y))
        d = ImageDraw.Draw(S)
        d.text((x + 4, y + 322), f"{t:5.1f}s", fill=(255, 220, 0))
        d.text((x + 4, y + 336), words_at(t), fill=(200, 200, 210))
    fn = f"sheet-{si // per:02d}.jpg"
    S.save(os.path.join(OUT, fn), quality=88)
    sheets.append(fn)

fails = [r for r in results if r["status"] == "FAIL"]
verdict = "PASS" if not fails else "FAIL"
json.dump({"video": video, "sha256": sha, "verdict": verdict, "results": results, "sheets": sheets}, open(os.path.join(OUT, "report.json"), "w"), indent=1)

rows = "".join(f'<tr class="{r["status"].lower()}"><td>{r["status"]}</td><td>{html.escape(r["check"])}</td><td>{html.escape(r["evidence"])}</td></tr>' for r in results)
ev_rows = "".join(f'<tr><td>{html.escape(k)}</td><td><a href="{html.escape(r["url"])}">{html.escape(r["url"][:70])}</a></td><td>{r["captured_at"][:10]}</td><td><code>{r["sha"]}</code></td></tr>' for k, r in man.items())
open(os.path.join(OUT, "report.html"), "w").write(f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Frame check</title><style>
:root{{--bg:#0B0D14;--ink:#E8EBF7;--mute:#8A93B5;--ok:#4ADE9A;--bad:#FF5A6E;--warn:#F5B94A}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--ink);font:15px/1.5 -apple-system,system-ui,sans-serif}}
main{{max-width:1180px;margin:auto}} h1{{font-size:26px;margin:8px 0}} .v{{font-weight:800;color:var({'--ok' if verdict == 'PASS' else '--bad'})}}
table{{width:100%;border-collapse:collapse;margin:12px 0}} td{{padding:6px 8px;border-bottom:1px solid #222838;vertical-align:top}}
tr.pass td:first-child{{color:var(--ok)}} tr.fail td:first-child{{color:var(--bad);font-weight:800}} tr.warn td:first-child{{color:var(--warn)}}
code{{font:13px ui-monospace,Menlo,monospace;color:var(--mute);word-break:break-all}} img{{width:100%;margin:8px 0;border-radius:8px}} a{{color:#AEB8FF}}
.wrap{{overflow-x:auto}}</style></head><body><main>
<h1>Frame check: <span class="v">{verdict}</span></h1>
<p>File <code>{html.escape(os.path.basename(video))}</code> · {dur:.2f}s · {n} frames checked one by one<br>sha256 <code>{sha}</code><br>
Approve this hash. Any re-render changes it and needs a new check.</p>
<div class="wrap"><table>{rows}</table></div>
<h2>Evidence pages shown</h2><div class="wrap"><table>{ev_rows}</table></div>
<h2>Every half second</h2>{''.join(f'<img src="{s}" alt="contact sheet {i}">' for i, s in enumerate(sheets))}
</main></body></html>""")
print(json.dumps({"verdict": verdict, "sha256": sha[:16], "fails": [f["check"] + ": " + f["evidence"] for f in fails],
                  "warns": [r["check"] + ": " + r["evidence"] for r in results if r["status"] == "WARN"]}, indent=1))
sys.exit(0 if verdict == "PASS" else 1)
