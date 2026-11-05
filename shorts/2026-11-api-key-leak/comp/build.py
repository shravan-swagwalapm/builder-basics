"""Build index.html for the API-key Short from the FINAL voice alignment.

usage: python3 -I build.py   (run inside comp/)
All beat times come from ../voice/FINAL.align.json, so a new voice take re-times the whole film.
"""
import html, json, os, re, shutil

A = json.load(open("../voice/FINAL.align.json"))
W, L = A["words"], A["lines"]
END = L[-1][1] + 2.0  # last line holds >= 2 s (HyperFrames motion.md)


def w(token, after=0.0):
    """Start time of the first word matching token at/after `after`."""
    t = token.lower()
    for x in W:
        if x["s"] >= after - 0.01 and re.sub(r"[^a-z0-9.%']", "", x["w"].lower()).startswith(t):
            return x["s"]
    raise SystemExit(f"anchor word not found: {token!r} after {after}")


def ln(i):  # 1-based line start
    return L[i - 1][0]


# ---------------- captions: 2–4 word groups, keyword accent ----------------
KEY = {"2023", "orca", "two", "minutes", "28.65", "million", "81%", "searchable", "scanners", "deleting", "history",
       "forks", "caches", "toyota", "five", "push", "protection", "openai", "anthropic", "gemini", "env", "gitignore",
       "first", "rotate", "later", "head", "start"}
groups, cur = [], []
for x in W:
    if cur and len(" ".join(y["w"] for y in cur + [x])) > 26:   # break BEFORE the word that would wrap (frame check caught 32-char groups)
        groups.append(cur); cur = []
    cur.append(x)
    end_punct = x["w"][-1] in ".,:?!"
    if len(cur) >= 5 or (end_punct and len(cur) >= 3) or (end_punct and x["w"][-1] in ".?!"):   # one line max (safe zone), longer holds
        groups.append(cur); cur = []
if cur:
    groups.append(cur)

cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    spans = []
    for wi, x in enumerate(g):
        word = html.escape(x["w"])
        k = re.sub(r"[^a-z0-9.%]", "", x["w"].lower()).rstrip(".")
        cls = "kw" if k in KEY else ""
        spans.append(f'<span id="c{gi}_{wi}" class="cw {cls}">{word}</span>')
        spoken = "#7C8CFF" if cls == "kw" else "#F4F6FF"   # karaoke: grey until spoken, then stays lit
        cap_js.append(f'tl.set("#c{gi}_{wi}",{{color:"{spoken}"}},{x["s"]:.3f});')
    start = lambda k: max(groups[k][0]["s"] - 0.12, groups[k - 1][-1]["e"] + 0.06) if k else groups[0][0]["s"] - 0.12
    s = start(gi)                                  # early only into silence: never over a word still being spoken
    nxt = start(gi + 1) if gi + 1 < len(groups) else END
    e = min(g[-1]["e"] + 0.31, nxt)                # hard-kill at the next group; last word stays lit to its end
    cap_html.append(f'<div id="cg{gi}" class="capg">{" ".join(spans)}</div>')
    cap_js.append(f'tl.fromTo("#cg{gi}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.18,ease:"power3.out"}},{max(s,0):.3f});'
                  f'tl.to("#cg{gi}",{{opacity:0,duration:0.06,ease:"none"}},{e-0.06:.3f});')

# ---------------- counters as authored frame rows (deterministic under seek) ----------------
def rows(el, t0, dur, values):
    out = []
    n = len(values)
    for i, v in enumerate(values):
        out.append(f'tl.set("{el}",{{textContent:{json.dumps(v)}}},{t0 + dur * i / max(n - 1, 1):.3f});')
    return "".join(out)


def ease_out(p):
    return 1 - (1 - p) ** 3


timer_vals =[f"{(v:=int(round(120 * ease_out(i / 29))))//60}:{v%60:02d}" for i in range(30)]
year_vals = [str(2017 + round(5 * i / 14)) for i in range(15)]
emails_vals = [f"up to {int(296019 * ease_out(i / 23)):,} emails" for i in range(24)]   # dossier: "up to", no misuse confirmed

T = {
    "orca": w("orca"), "pushed": w("pushed"), "two": ln(2), "rare": ln(3), "n2865": w("28.65"), "p81": w("81%"),
    "because": ln(5), "searchable": w("searchable"), "scanners": w("scanners"), "shaped": w("shaped"),
    "deleting": w("deleting"), "still": ln(7), "history": w("history"), "forks": w("forks"), "caches": w("caches"),
    "toyota": ln(8), "five": w("five", ln(8)), "pp": ln(9), "pp_word": w("push", ln(9)), "default": ln(10),
    "openai": w("openai"), "anthropic": w("anthropic"), "switch": w("switch"), "gemini": w("gemini"),
    "rule": ln(12), "env": w("env"), "gitignore": w("gitignore"), "first": w("first", ln(12)),
    "leaks": ln(13), "rotate": w("rotate"), "clean": w("clean"), "cb": ln(14), "head": w("head"), "end": END,
}
# v4: opening flash of real source pages, then three proof cards placed only where a viewer might doubt the claim
T["open"] = 1.25                                                     # flash stack ends, scene builds in
T["ev_orca"], T["ev_orca_out"] = T["two"] + 1.25, T["rare"] + 0.55     # after the 0:00 -> 2:00 timer lands
T["ev_gg"] = w("leaked", T["n2865"]) - 0.35                           # "...and leaked AI keys grew 81%"
T["ev_toy"], T["ev_toy_out"] = T["toyota"] + 0.1, w("exposed", T["toyota"]) + 0.3
js_T = json.dumps({k: round(v, 3) for k, v in T.items()})
COUNTERS = (rows("#timer", T["two"], 1.0, timer_vals) +
            rows("#year", T["ev_toy_out"] + 0.2, T["five"] - T["ev_toy_out"] - 0.2, year_vals) +
            rows("#emails", T["five"] - 0.3, 0.6, emails_vals))

# ---------------- sound cues from the same anchors as the picture ----------------
LIB = "../../../audio-library/"
G = {"pop": 0.45, "whoosh": 0.4, "tick": 0.25, "sweep": 0.35, "alert": 0.4, "riser": 0.35, "impact": 0.55, "click": 0.5}
def s(name, t):
    return [LIB + name + ".mp3", round(t, 3), G[name.split("-")[0]]]
FLASH_T = [0.0, 0.2, 0.4, 0.6, 0.8]                                  # opening stack: one real page per hit
SFXCUES = [s(("click-1", "tick-1")[i % 2], t) for i, t in enumerate(FLASH_T)] + [s("whoosh-2", T["open"] - 0.1)] + [
    s("whoosh-1", T["ev_orca"]), s("pop-2", T["ev_orca"] + 0.8), s("whoosh-1", T["ev_gg"]), s("whoosh-1", T["ev_toy"]),
    s("pop-1", T["orca"]), s("whoosh-1", T["pushed"]), s("pop-2", T["pushed"] + 0.6),
    s("whoosh-2", T["two"]), s("tick-1", T["two"]), s("alert-1", T["two"] + 1.1),
    s("whoosh-1", T["rare"]), s("tick-1", T["n2865"] - 0.15), s("pop-1", T["p81"]),
    s("whoosh-2", T["because"]), s("sweep-1", T["searchable"]), s("pop-2", T["searchable"] + 0.2),
    s("click-1", T["deleting"] + 0.6), s("pop-1", T["history"]), s("pop-2", T["forks"]), s("pop-1", T["caches"]),
    s("whoosh-2", T["toyota"]), s("tick-1", T["toyota"] + 0.5), s("pop-2", T["five"] + 0.1),
    s("riser-1", T["pp_word"] - 1.6), s("impact-1", T["pp_word"]),
    s("pop-1", T["openai"] + 0.75), s("pop-2", T["anthropic"] + 0.75), s("pop-1", T["switch"]),
    s("alert-1", T["gemini"] + 0.4), s("whoosh-2", T["rule"]),
    s("pop-1", T["env"] - 0.1), s("pop-2", T["gitignore"]), s("whoosh-2", T["gitignore"] + 0.3), s("click-1", T["first"] + 0.5),
    s("pop-1", T["rotate"]), s("pop-2", T["clean"]), s("whoosh-1", T["cb"]), s("whoosh-2", T["head"]),
]
json.dump({"bed": LIB + "bed-calm-70s.mp3", "bed_gain": 0.14, "end": round(END, 3), "sfx": SFXCUES},
          open("cues.json", "w"), indent=1)

# ---------------- Rethink-look generators (v2) ----------------
def typed(sel, text, t0, cps=30):
    """Terminal typing as authored frame rows (seek-safe)."""
    return "".join(f'tl.set("{sel}",{{textContent:{json.dumps(text[:i])}}},{t0 + i / cps:.3f});'
                   for i in range(len(text) + 1))


TYPED = (
    typed("#tl1", "git add .", T["open"] + 0.15, 26) +
    typed("#tl2", 'git commit -m "ship it"', T["open"] + 0.6, 30) +
    typed("#tl3", 'git push origin main', T["pushed"] - 0.1, 26) +
    typed("#tl4", 'git reset --hard HEAD~1', T["deleting"] - 0.05, 30) +
    typed("#tl4b", 'git push --force', T["deleting"] + 0.75, 30) +
    typed("#tr1", 'echo ".env" >> .gitignore', T["env"] - 0.6, 30) +
    typed("#trA", 'git add .', T["gitignore"] + 0.4, 26) +
    typed("#tr2", 'git commit -m "first commit"', T["first"] - 0.6, 34)
)

COLS, ROWS, GAP = 17, 11, 46          # dot matrix (homage to "this is you.")
HOT = (12, 4)                         # the dot that turns out to be your key
dots = []
for r in range(ROWS):
    for c in range(COLS):
        hot = ' id="hotdot"' if (c, r) == HOT else ""
        dots.append(f'<circle{hot} cx="{23 + c * GAP}" cy="{23 + r * GAP}" r="6.5" />')
DOTS = f'<svg id="matrix" viewBox="0 0 {COLS * GAP} {ROWS * GAP}" width="{COLS * GAP}" height="{ROWS * GAP}">{"".join(dots)}</svg>'

PREFIXES = ["sk_live_", "sk-proj-", "sk-ant-", "AKIA", "ghp_", "AIza", "xai-", "sk_test_", "glpat-", "SG."]
chips = []
for i in range(84):  # deterministic: no RNG
    p = PREFIXES[(i * 7) % len(PREFIXES)]
    chips.append(f'<span class="kchip"><i></i>{p}{"•" * (6 + (i * 5) % 7)}</span>')
PLANE = f'<div id="plane">{"".join(chips)}</div>'

# ---------------- slot-roll numeral (reference: per-digit roll) ----------------
SLOT_TXT, slot_html, slot_js = "28.65M", [], []
for i, ch in enumerate(SLOT_TXT):
    if ch.isdigit():
        strip = "".join(f'<span class="d">{d % 10}</span>' for d in range(20 + int(ch) + 1))   # two full turns, then the value
        slot_html.append(f'<span class="col"><div id="sd{i}" data-layout-ignore>{strip}</div></span>')   # off-value digits sit clipped by .col; checker cannot see clips
        slot_js.append(f'tl.fromTo("#sd{i}",{{y:0}},{{y:"-{20 + int(ch)}em",duration:{1.1 + 0.12 * i:.2f},ease:"power4.out",immediateRender:true}},{T["n2865"] - 0.1 + 0.05 * i:.3f});')
    else:
        slot_html.append(f'<span class="col"><span class="d">{ch}</span></span>')
SLOT_HTML, SLOT_JS = "".join(slot_html), "".join(slot_js)

# ---------------- evidence cards from tools/capture (real pages, phrase rects in image px) ----------------
MAN = json.load(open("../evidence/manifest.json"))
os.makedirs("assets/ev", exist_ok=True)
for r in MAN.values():
    shutil.copyfile(f"../evidence/{r['file']}", f"assets/ev/{r['file']}")
BAR = {"orca": ("orca.security", "AWS KEY · 2023"), "gitguardian": ("blog.gitguardian.com", "MAR 2026"),
       "ghdelete": ("docs.github.com", ""), "toyota": ("global.toyota", "OCT 2022"), "pushprot": ("docs.github.com", "")}
WW, WH = 940, 660


def frame(r, idx, s):
    """Image offset that puts the phrase union at the reading point, clamped so the page always covers the window."""
    R = [q for i in idx for q in r["phrases"][i]["rects"]]
    x0, y0 = min(q[0] for q in R), min(q[1] for q in R)
    x1, y1 = max(q[0] + q[2] for q in R), max(q[1] + q[3] for q in R)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    def fit(c, win, size, at):
        return (win - size * s) / 2 if size * s < win else min(0, max(win - size * s, at - c * s))
    return fit(cx, WW, r["w"], WW / 2), fit(cy, WH, r["h"], WH * 0.45), x1 - x0


ev_html, ev_js = [], []
def card(cid, sid, idx, t_in, t_out=None, hl=None, rot=0.0, flash=False):
    r = MAN[sid]
    s0 = WW / r["w"]
    pw = frame(r, idx, s0)[2]
    s1 = max(s0 * 1.12, min(0.8 * WW / pw, 1.5)) if not flash else max(s0, min(0.6 * WW / pw, 1.1))
    pad = 7 / s1
    hls = []
    for i in idx:
        for k, (x, y, w_, h_) in enumerate(r["phrases"][i]["rects"]):
            hid = f"{cid}_h{i}{k}"
            hls.append((hid, w_))
            ev_html_hl = (f'<div class="hl" id="{hid}" style="left:{x - pad:.0f}px;top:{y - pad:.0f}px;'
                          f'width:{w_ + 2 * pad:.0f}px;height:{h_ + 2 * pad:.0f}px;border-radius:{6 / s1:.1f}px"></div>')
            hls[-1] = (hid, w_, ev_html_hl)
    dom, tag = BAR[sid]
    ev_html.append(f'<div class="evcard" id="{cid}" style="transform:rotate({rot}deg)"><div class="evbar"><i style="left:24px"></i><i style="left:44px"></i>'
                   f'<i style="left:64px"></i><span>{dom}</span><b>{tag}</b></div><div class="evwin"><div class="evin" id="{cid}_in" '
                   f'style="width:{r["w"]}px;height:{r["h"]}px"><img src="assets/ev/{r["file"]}" width="{r["w"]}" height="{r["h"]}" alt="">'
                   f'{"".join(h[2] for h in hls)}</div></div></div>')
    if flash:   # a hit: pops in over the stack, highlight already on
        x, y, _ = frame(r, idx, s1)
        ev_js.append(f'gsap.set("#{cid}_in",{{x:{x:.1f},y:{y:.1f},scale:{s1:.4f}}});' + "".join(f'gsap.set("#{h[0]}",{{scaleX:1}});' for h in hls))
        ev_js.append(f'tl.fromTo("#{cid}",{{opacity:0,scale:1.14,rotation:{rot * 2.2:.1f}}},{{opacity:1,scale:1,rotation:{rot},duration:0.16,ease:"power3.out",immediateRender:{str(t_in == 0).lower()}}},{t_in:.3f});')
        ev_js.append(f'tl.fromTo("#flashov",{{opacity:0.34}},{{opacity:0,duration:0.14,ease:"power2.out",immediateRender:{str(t_in == 0).lower()}}},{t_in:.3f});')
        return
    xa, ya, _ = frame(r, idx, s0)
    xb, yb, _ = frame(r, idx, s1)
    xc, yc, _ = frame(r, idx, s1 * 1.04)
    zoom = 0.8
    ev_js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:60,scale:0.94,filter:"blur(10px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:0.45,ease:"expo.out",immediateRender:false}},{t_in:.3f});')
    ev_js.append(f'tl.fromTo("#{cid}_in",{{x:{xa:.1f},y:{ya:.1f},scale:{s0:.4f}}},{{x:{xb:.1f},y:{yb:.1f},scale:{s1:.4f},duration:{zoom},ease:"power3.inOut",immediateRender:true}},{t_in + 0.1:.3f});')
    ev_js.append(f'tl.to("#{cid}_in",{{x:{xc:.1f},y:{yc:.1f},scale:{s1 * 1.04:.4f},duration:{t_out - t_in - 0.1 - zoom:.3f},ease:"none"}},{t_in + 0.1 + zoom:.3f});')   # slow read-drift
    h0, h1 = hl                                                       # marker wipes at speaking pace
    tot, t = sum(h[1] for h in hls), h0
    for hid, w_, _ in hls:
        d = (h1 - h0) * w_ / tot
        ev_js.append(f'tl.fromTo("#{hid}",{{scaleX:0}},{{scaleX:1,duration:{d:.3f},ease:"none",immediateRender:false}},{t:.3f});')
        t += d
    ev_js.append(f'tl.to("#{cid}",{{opacity:0,scale:1.04,filter:"blur(10px)",duration:0.22,ease:"power3.in"}},{t_out - 0.22:.3f});')


for i, (sid, rot) in enumerate([("orca", -3), ("gitguardian", 2.5), ("ghdelete", -1.5), ("toyota", 3), ("pushprot", 0)]):
    card(f"evf{i}", sid, [0], FLASH_T[i], rot=rot, flash=True)
for i in range(len(FLASH_T) - 1):   # hard cut: the old page leaves as the next hits (flash overlay hides the swap) (no text hidden under a card)
    ev_js.append(f'tl.set("#evf{i}",{{opacity:0}},{FLASH_T[i + 1]:.3f});')
ev_js.append(f'tl.to(".evf",{{opacity:0,y:-40,scale:0.92,filter:"blur(10px)",duration:0.25,ease:"power3.in",stagger:0.03}},{T["open"] - 0.3:.3f});')
card("ev_orca", "orca", [0], T["ev_orca"], T["ev_orca_out"], hl=(T["ev_orca"] + 0.85, T["ev_orca"] + 1.45))
card("ev_gg", "gitguardian", [0], T["ev_gg"], T["because"] - 0.02, hl=(w("leaked", T["n2865"]), T["p81"] + 0.45))
card("ev_toy", "toyota", [0], T["ev_toy"], T["ev_toy_out"], hl=(w("a", T["toyota"]), w("exposed", T["toyota"])))
EVIDENCE = "".join(ev_html).replace('class="evcard" id="evf', 'class="evcard evf" id="evf')

tmpl = open("index.html.tmpl").read()
out = (tmpl.replace("/*__T__*/", f"const T={js_T};")
           .replace("/*__CAPTIONS_JS__*/", "".join(cap_js))
           .replace("/*__COUNTERS_JS__*/", COUNTERS)
           .replace("<!--__CAPTIONS__-->", "\n".join(cap_html))
           .replace("/*__TYPED_JS__*/", TYPED)
           .replace("<!--__DOTS__-->", DOTS)
           .replace("<!--__PLANE__-->", PLANE)
           .replace("<!--__SECRETS__-->", SLOT_HTML)
           .replace("/*__SLOT_JS__*/", SLOT_JS)
           .replace("<!--__EVIDENCE__-->", EVIDENCE)
           .replace("/*__EVIDENCE_JS__*/", "".join(ev_js))
           .replace("__END__", f"{END:.2f}"))
assert "__" not in re.sub(r"window\.__\w+|__hyperframes", "", out), "unfilled placeholder left in template"

# ---- text-budget guard (Shravan 2026-11-05: no heavy text; no header/series/section text) ----
for banned in ('id="hdr"', 'id="sect"', 'BUILDER BASICS', 'AI SECURITY'):
    assert banned not in out, f"text budget: banned top-text element is back: {banned}"
LABEL = re.compile(r'<div class="evbar">(.*?)</div><div class="evwin">|<div class="(?:chip|lbl|hd)"[^>]*>(.*?)</div>|<div id="hottag">(.*?)</div>|<small>(.*?)</small>', re.S)
over = []
for m in LABEL.finditer(out):
    text = re.sub(r"<[^>]+>", " ", next(g for g in m.groups() if g is not None))
    words = [w for w in text.split() if re.search(r"[A-Za-z0-9]", w)]
    if len(words) > 4:
        over.append(" ".join(words))
assert not over, f"text budget: labels over 4 words: {over}"
open("index.html", "w").write(out)
# motion assertions: one per element id (HyperFrames requires an unambiguous selector)
ids = re.findall(r'<(?:div|svg)[^>]*class="(?:panel[^"]*|chip|num[^"]*|lbl|ttl|step|called|evcard[^"]*)"[^>]*id="([^"]+)"|<(?:div|svg)[^>]*id="([^"]+)"[^>]*class="(?:panel[^"]*|chip|num[^"]*|lbl|ttl|step|called|evcard[^"]*)"', out)
ids = sorted({a or b for a, b in ids} | {f"cg{i}" for i in range(len(groups))})
assertions = [{"kind": "staysInFrame", "selector": f"#{i}"} for i in ids] + [{"kind": "appearsBy", "selector": "#term1", "bySec": T["open"] + 0.5}]
json.dump({"assertions": assertions}, open("index.motion.json", "w"), indent=1)
print(f"built index.html: {len(groups)} caption groups, end {END:.2f}s, anchors {len(T)}")
