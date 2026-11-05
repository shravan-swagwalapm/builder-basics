"""V5 build: BLUEPRINT FLOWCHART grammar, storyboarded per caption phrase.

usage: python3 -I build.py   (inside comp/)
Every visual event registers (time, label). The build FAILS if any caption phrase has no event that starts
inside it (or within 0.35 s before it): per-caption storyboarding is a rule, not a hope (Shravan 2026-11-06).
Writes index.html, index.motion.json, cues.json and ../storyboard-captions.md (the generated per-caption storyboard).
"""
import html, json, os, re, shutil

A = json.load(open("../voice/FINAL.align.json"))
W, L = A["words"], A["lines"]
END = L[-1][1] + 2.0


def w(token, after=0.0):
    t = token.lower()
    for x in W:
        if x["s"] >= after - 0.01 and re.sub(r"[^a-z0-9.%'$,-]", "", x["w"].lower()).startswith(t):
            return x["s"]
    raise SystemExit(f"anchor word not found: {token!r} after {after}")


def ln(i):
    return L[i - 1][0]


# ---------------- captions (one line, karaoke; back-to-back groups swap hard at the hand-off) ----------------
DISPLAY = {"six": "6"}
KEY = {"2023", "six", "chatgpt", "varghese", "real", "$5,000", "2024", "air", "canada", "static", "chatbot", "bot",
       "rag", "retrieval-augmented", "chunks", "meaning", "prompt", "open-book", "page", "pages", "guarantee",
       "wrong", "sourced", "open", "training", "question"}
groups, cur = [], []
for x in W:
    if cur and len(" ".join(y["w"] for y in cur + [x])) > 26:
        groups.append(cur); cur = []
    cur.append(x)
    ep = x["w"][-1] in ".,:?!"
    if len(cur) >= 5 or (ep and len(cur) >= 3) or (ep and x["w"][-1] in ".?!"):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
start = lambda k: max(groups[k][0]["s"] - 0.12, min(groups[k - 1][-1]["e"] + 0.06, groups[k][0]["s"] - 0.03)) if k else groups[0][0]["s"] - 0.12
cap_html, cap_js = [], []
for gi, g in enumerate(groups):
    spans = []
    for wi, x in enumerate(g):
        core = re.sub(r"[^A-Za-z0-9$,.'-]", "", x["w"]).rstrip(".,:")
        shown = x["w"].replace(core, DISPLAY.get(core.lower(), core)) if core else x["w"]
        k = re.sub(r"[^a-z0-9.%$,-]", "", x["w"].lower()).rstrip(".,:")
        kw = k in KEY
        spans.append(f'<span id="c{gi}_{wi}" class="cw">{html.escape(shown)}</span>')
        cap_js.append(f'tl.set("#c{gi}_{wi}",{{color:"{"#B8F25B" if kw else "#EDEFF5"}"}},{x["s"]:.3f});')
    s = start(gi)
    nxt = start(gi + 1) if gi + 1 < len(groups) else END
    e = min(g[-1]["e"] + 0.31, nxt)
    swap = gi + 1 < len(groups) and nxt < g[-1]["e"] + 0.12
    leave = f'tl.set("#cg{gi}",{{opacity:0}},{e:.3f});' if swap else f'tl.to("#cg{gi}",{{opacity:0,duration:0.06,ease:"none"}},{e - 0.06:.3f});'
    cap_html.append(f'<div id="cg{gi}" class="capg">{" ".join(spans)}</div>')
    cap_js.append(f'tl.fromTo("#cg{gi}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:0.1,ease:"power3.out"}},{max(s, 0):.3f});' + leave)

# ---------------- evidence pages ----------------
MAN = json.load(open("../evidence/manifest.json"))
os.makedirs("assets/ev", exist_ok=True)
for r in MAN.values():
    shutil.copyfile(f"../evidence/{r['file']}", f"assets/ev/{r['file']}")
BAR = {"mata": ("courtlistener.com", "JUN 2023"), "mata_head": ("courtlistener.com", "JUN 2023"),
       "crt": ("civilresolutionbc.ca", "FEB 2024"), "crt_head": ("civilresolutionbc.ca", "FEB 2024"),
       "google": ("cloud.google.com", ""), "arxiv": ("arxiv.org", "2020"), "openai": ("developers.openai.com", ""),
       "anth_chunk": ("anthropic.com", "SEP 2024"), "anth_prompt": ("anthropic.com", "SEP 2024"), "aws_cite": ("aws.amazon.com", ""),
       "aws": ("aws.amazon.com", ""), "anthropic": ("anthropic.com", "SEP 2024")}

C = {"line": "#C9D1E3", "lime": "#B8F25B", "amber": "#FFB547", "red": "#FF5C5C", "violet": "#A99BFF", "mute": "#5E6577"}
ICON = {
    "spark": "M0 -18 L4 -4 L18 0 L4 4 L0 18 L-4 4 L-18 0 L-4 -4Z",
    "db": "M-16 -12 a16 6 0 1 0 32 0 a16 6 0 1 0 -32 0 M-16 -12 v24 a16 6 0 0 0 32 0 v-24 M-16 0 a16 6 0 0 0 32 0",
    "doc": "M-12 -18 h16 l8 8 v28 h-24z M4 -18 v8 h8 M-6 0 h12 M-6 7 h12",
    "person": "M0 -16 a6 6 0 1 1 -0.1 0 M-12 16 q0 -14 12 -14 q12 0 12 14",
    "scale": "M0 -18 v32 M-12 14 h24 M-16 -10 h32 M-16 -10 l-6 12 h12z M16 -10 l-6 12 h12z",
    "bot": "M-14 -8 h28 v20 h-28z M0 -8 v-8 M-6 2 h0.1 M6 2 h0.1 M-5 8 h10",
    "cpu": "M-10 -10 h20 v20 h-20z M-4 -16 v6 M4 -16 v6 M-4 10 v6 M4 10 v6 M-16 -4 h6 M-16 4 h6 M10 -4 h6 M10 4 h6",
    "search": "M-14 -4 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M4 4 L14 14",
    "check": "M-12 0 l8 8 l16 -16",
    "prompt": "M-14 -14 h28 M-14 -5 h28 M-14 4 h20 M-14 13 h12",
    "chat": "M-16 -12 h32 v20 h-18 l-8 8 v-8 h-6z",
    "building": "M-16 18 v-30 l16 -8 l16 8 v30z M-8 -4 h4 M4 -4 h4 M-8 6 h4 M4 6 h4 M-3 18 v-8 h6 v8",
    "coin": "M-14 0 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 M0 -8 v16 M-5 -4 h8 a3 3 0 0 1 0 6 h-6 a3 3 0 0 0 0 6 h8",
}


class Board:
    def __init__(self):
        self.scenes, self.js, self.events, self.sfx = [], [], [], []
        self.sc = None

    def ev(self, t, label, sfx=None, gain=None):
        self.events.append((round(t, 3), label, self.sc["name"] if self.sc else "-"))
        if sfx:
            self.sfx.append((sfx, t, gain))

    def add(self, h):
        self.sc["html"].append(h)

    def svg(self, s):
        self.sc["svg"].append(s)

    # the board scrolls: the old scene slides up and out, the new one arrives from below
    def scene(self, name, t_in, t_out):
        self.sc = {"name": name, "id": f"sc{len(self.scenes)}", "t_in": t_in, "t_out": t_out, "html": [], "svg": []}
        self.scenes.append(self.sc)
        sid = self.sc["id"]
        if t_in <= 0:
            self.js.append(f'tl.fromTo("#{sid}",{{opacity:1,y:0}},{{opacity:1,y:0,duration:0.01,immediateRender:true}},0);')
        else:
            self.js.append(f'tl.fromTo("#{sid}",{{opacity:1,y:150}},{{opacity:1,y:0,duration:0.6,ease:"power3.out",immediateRender:false}},{t_in:.3f});')
            self.ev(t_in, f"scene {name} scrolls in", "whoosh-2", 0.35)
        if t_out < END:
            self.js.append(f'tl.to("#{sid}",{{opacity:0,y:-80,duration:0.4,ease:"power2.in"}},{t_out - 0.4:.3f});')   # -80 not -150: a 150 px exit slid top nodes into the title (textscan, 2026-11-06)

    def draw_in(self, sel, w_, t, label, sfx="tick-1", gain=0.2):
        a, b = f"inset(-14px {w_ + 14}px -14px -14px)", "inset(-14px -14px -14px -14px)"
        self.js.append(f'tl.fromTo("{sel}",{{opacity:1,clipPath:"{a}"}},{{opacity:1,clipPath:"{b}",duration:0.45,ease:"power2.out",immediateRender:false}},{t:.3f});')
        self.ev(t, label, sfx, gain)

    def node(self, nid, x, y, w_, h_, label, icon, color, t, sub=None):
        sub_h = f'<span class="sub">{sub}</span>' if sub else ""
        lay = "align-items:flex-start;padding-top:22px;" if sub else ""
        self.add(f'<div class="nd" id="{nid}" style="{lay}left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;--k:{C[color]}">'
                 f'<svg class="ic" viewBox="-24 -24 48 48"><path d="{ICON[icon]}"/></svg><span class="nl">{label}</span>{sub_h}</div>')
        self.draw_in(f"#{nid}", w_, t, f"node {label or icon} draws")

    def recolor(self, nid, color, t, label, sfx="alert-1"):
        self.js.append(f'tl.to("#{nid}",{{"--k":"{C[color]}",duration:0.25}},{t:.3f});')
        self.ev(t, label, sfx, 0.35)

    def pulse(self, sel, t, label, s=1.08):
        self.js.append(f'tl.to("{sel}",{{scale:{s},duration:0.18,yoyo:true,repeat:1,ease:"power2.out"}},{t:.3f});')
        self.ev(t, label, "pop-2", 0.3)

    def edge(self, eid, pts, color, t, d=0.4, packets=0, label=None, lpos=None, dashed=False):
        dpath = "M" + " L".join(f"{x} {y}" for x, y in pts)
        seg = [abs(pts[i + 1][0] - pts[i][0]) + abs(pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1)]
        L_ = sum(seg)
        mk = f'url(#m_{self.sc["id"]}_{color})'
        if not dashed:
            self.svg(f'<path id="{eid}_b" class="eb" d="{dpath}" stroke="{C[color]}" marker-end="{mk}"/>')
            self.js.append(f'tl.fromTo("#{eid}_b",{{opacity:1,strokeDasharray:{L_},strokeDashoffset:{L_}}},{{opacity:1,strokeDashoffset:0,duration:{d},ease:"power2.inOut",immediateRender:false}},{t:.3f});')
        self.svg(f'<path id="{eid}_f" class="ef" d="{dpath}" stroke="{C[color]}"' + (f' marker-end="{mk}"' if dashed else "") + "/>")
        self.js.append(f'tl.fromTo("#{eid}_f",{{opacity:0}},{{opacity:{1 if dashed else 0.8},duration:0.3,immediateRender:false}},{t + (0 if dashed else d):.3f});')
        for k in range(packets):   # a packet = data travelling the edge (motion with a cause)
            pid = f"{eid}_p{k}"
            self.svg(f'<circle id="{pid}" class="pk" r="7" cx="{pts[0][0]}" cy="{pts[0][1]}" fill="{C[color]}"/>')
            tc = t + d + k * 0.22
            self.js.append(f'tl.set("#{pid}",{{opacity:1,attr:{{cx:{pts[0][0]},cy:{pts[0][1]}}}}},{tc:.3f});')
            for i in range(len(pts) - 1):
                dd = max(seg[i] / 900, 0.04)
                self.js.append(f'tl.to("#{pid}",{{attr:{{cx:{pts[i + 1][0]},cy:{pts[i + 1][1]}}},duration:{dd:.3f},ease:"none"}},{tc:.3f});')
                tc += dd
            self.js.append(f'tl.set("#{pid}",{{opacity:0}},{tc:.3f});')
        if label:
            lid = f"{eid}_l"
            self.add(f'<div class="el" id="{lid}" style="left:{lpos[0]}px;top:{lpos[1]}px;--k:{C[color]}">{label}</div>')
            self.js.append(f'tl.fromTo("#{lid}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(1.6)",immediateRender:false}},{t + d * 0.6:.3f});')
        self.ev(t, f"edge {eid}{' “' + label + '”' if label else ''} draws" + (f" + {packets} packets" if packets else ""), "tick-1", 0.15)

    def el(self, eid, x, y, text, color, t, label=None):
        self.add(f'<div class="el" id="{eid}" style="left:{x}px;top:{y}px;--k:{C[color]}">{text}</div>')
        self.js.append(f'tl.fromTo("#{eid}",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(1.6)",immediateRender:false}},{t:.3f});')
        self.ev(t, label or f"tag “{text}”", "pop-1", 0.3)

    def cite(self, cid, x, y, w_, name, t):
        self.add(f'<div class="cite" id="{cid}" style="left:{x}px;top:{y}px;width:{w_}px"><em>§</em>{name}<i></i></div>')
        self.js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:-24,scale:1.12}},{{opacity:1,y:0,scale:1,duration:0.4,ease:"expo.out",immediateRender:false}},{t:.3f});')
        self.ev(t, f"citation {name} pops", "pop-1" if len(self.events) % 2 else "pop-2", 0.35)

    def strike(self, cid, t):
        self.js.append(f'tl.to("#{cid} i",{{scaleX:1,duration:0.22,ease:"power2.inOut"}},{t:.3f});tl.to("#{cid}",{{"--k":"#FF5C5C",duration:0.2}},{t:.3f});')
        self.ev(t, f"{cid} struck through")

    def slot(self, sid_, x, y, t):
        self.add(f'<div class="slot" id="{sid_}" style="left:{x}px;top:{y}px"></div>')
        self.js.append(f'tl.fromTo("#{sid_}",{{opacity:0,scale:0.7}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)",immediateRender:false}},{t:.3f});')
        self.ev(t, f"empty page slot {sid_}", "tick-1", 0.2)

    def glyph(self, gid, x, y, text, t, color="red", shake=False):
        self.add(f'<div class="glyph" id="{gid}" style="left:{x}px;top:{y}px;color:{C[color]}">{text}</div>')
        self.js.append(f'tl.fromTo("#{gid}",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.3,ease:"expo.out",immediateRender:false}},{t:.3f});')
        if shake:
            self.js.append(f'tl.to("#{gid}",{{x:8,duration:0.05,yoyo:true,repeat:5,ease:"none"}},{t + 0.3:.3f});')
        self.ev(t, f"glyph {text}", "impact-1" if color == "red" else "pop-2", 0.45)

    def bound(self, bid, x, y, w_, h_, tag, color, t):
        self.add(f'<div class="bound" id="{bid}" style="left:{x}px;top:{y}px;width:{w_}px;height:{h_}px;--k:{C[color]}"><span class="tag">{tag}</span></div>')
        self.draw_in(f"#{bid}", w_, t, f"boundary {tag} wraps the flow", "impact-1", 0.5)

    def lbl(self, lid, y, text, t):
        self.add(f'<div class="lbl" id="{lid}" style="top:{y}px">{text}</div>')
        self.js.append(f'tl.fromTo("#{lid}",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.35,ease:"expo.out",immediateRender:false}},{t:.3f});')
        self.ev(t, f"label “{text}”")

    def fade_out(self, sel, t):
        self.js.append(f'tl.to("{sel}",{{opacity:0,duration:0.2}},{t:.3f});')

    # a real page as a node: it draws in, zooms to the quote, the marker wipes while the words are spoken
    def page(self, cid, sid, idx, box, t_in, t_out, hl=(), static0=False):
        r = MAN[sid]
        bx, by, bw, bh = box
        WW, WH = bw, bh - 60
        def frame(s):
            R = [q for i in idx for q in r["phrases"][i]["rects"]]
            x0, y0 = min(q[0] for q in R), min(q[1] for q in R)
            x1, y1 = max(q[0] + q[2] for q in R), max(q[1] + q[3] for q in R)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            fit = lambda c, win, size, at: (win - size * s) / 2 if size * s < win else min(0, max(win - size * s, at - c * s))
            return fit(cx, WW, r["w"], WW / 2), fit(cy, WH, r["h"], WH * 0.45), x1 - x0
        s0 = WW / r["w"]
        s1 = max(s0 * 1.12, min(0.82 * WW / frame(s0)[2], 1.4))
        pad = 7 / s1
        rects = {i: [(f"{cid}_h{i}{k}", q) for k, q in enumerate(r["phrases"][i]["rects"])] for i in idx}
        hl_html = "".join(f'<div class="hl" id="{h}" style="left:{x - pad:.0f}px;top:{y - pad:.0f}px;width:{w_ + 2 * pad:.0f}px;height:{h_ + 2 * pad:.0f}px;border-radius:{6 / s1:.1f}px"></div>'
                          for i in idx for h, (x, y, w_, h_) in rects[i])
        dom, tag = BAR[sid]
        self.add(f'<div class="evcard" id="{cid}" style="left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px"><div class="evbar"><i style="left:24px"></i><i style="left:44px"></i><i style="left:64px"></i>'
                 f'<span>{dom}</span><b>{tag}</b></div><div class="evwin" style="width:{WW}px;height:{WH}px"><div class="evin" id="{cid}_in" style="width:{r["w"]}px;height:{r["h"]}px">'
                 f'<img src="assets/ev/{r["file"]}" width="{r["w"]}" height="{r["h"]}" alt="">{hl_html}</div></div></div>')
        xa, ya, _ = frame(s0); xb, yb, _ = frame(s1); xc, yc, _ = frame(s1 * 1.05)
        if static0:   # frame 0: the page is already there (not a grey wash); a light flash lands on it
            self.js.append(f'tl.fromTo("#{cid}",{{opacity:1}},{{opacity:1,duration:0.01,immediateRender:true}},0);')
            self.js.append('tl.fromTo("#flashov",{opacity:0.22},{opacity:0,duration:0.25,ease:"power2.out",immediateRender:true},0);')
            self.ev(0.0, f"page {sid} on screen at frame 0 + light flash", "click-1", 0.5)
        else:
            a, b = f"inset(0px {bw}px 0px 0px)", "inset(0px 0px 0px 0px)"
            self.js.append(f'tl.fromTo("#{cid}",{{opacity:1,clipPath:"{a}"}},{{opacity:1,clipPath:"{b}",duration:0.5,ease:"power3.out",immediateRender:false}},{t_in:.3f});')
            self.ev(t_in, f"real page {dom} draws in", "whoosh-1", 0.4)
        self.js.append(f'tl.fromTo("#{cid}_in",{{x:{xa:.1f},y:{ya:.1f},scale:{s0:.4f}}},{{x:{xb:.1f},y:{yb:.1f},scale:{s1:.4f},duration:0.8,ease:"power3.inOut",immediateRender:true}},{t_in + 0.1:.3f});')
        self.js.append(f'tl.to("#{cid}_in",{{x:{xc:.1f},y:{yc:.1f},scale:{s1 * 1.05:.4f},duration:{max(t_out - t_in - 0.9, 0.3):.3f},ease:"none"}},{t_in + 0.9:.3f});')
        for i, h0, h1 in hl:
            tot, t = sum(q[2] for _, q in rects[i]), h0
            for h, q in rects[i]:
                d = (h1 - h0) * q[2] / tot
                self.js.append(f'tl.fromTo("#{h}",{{scaleX:0}},{{scaleX:1,duration:{d:.3f},ease:"none",immediateRender:false}},{t:.3f});')
                self.ev(t, f"marker wipes “{r['phrases'][i]['text'][:36]}…”", "sweep-1" if t == h0 else None, 0.2)
                t += d
        self.js.append(f'tl.to("#{cid}",{{opacity:0,duration:0.22,ease:"power3.in"}},{t_out - 0.22:.3f});')


B = Board()
CASES = ["VARGHESE", "SHABOON", "PETERSEN", "MARTINEZ", "DURDEN", "MILLER"]   # the fake opinions named in the court order

# ================= STORYBOARD: one block per scene; comments name the caption phrases each event serves =================
# S1 · "In 2023, two lawyers in / a New York court cited / six cases that ChatGPT / found for them. / None of them existed."
B.scene("case", 0, ln(3) - 0.15)
B.page("pg_dock", "mata_head", [0], (110, 470, 860, 520), 0, w("a", 2.0) - 0.05, hl=[(0, w("2023"), w("2023") + 0.55)], static0=True)
B.node("law1", 110, 1040, 250, 100, "LAWYER", "person", "line", w("two"))
B.node("law2", 390, 1040, 250, 100, "LAWYER", "person", "line", w("lawyers"))
B.node("court", 110, 470, 400, 100, "NY COURT", "scale", "line", w("court"))
B.edge("e_file", [(110, 1090), (80, 1090), (80, 520), (106, 520)], "line", w("cited"), d=0.5, packets=1)
for i, name in enumerate(CASES):
    B.cite(f"k{i}", (180, 560)[i % 2], 640 + (i // 2) * 85, 300, name, w("six") - 0.05 + i * 0.09)
B.node("gpt", 720, 1040, 250, 100, "CHATGPT", "spark", "violet", w("chatgpt"))
B.edge("e_gpt", [(845, 1040), (845, 875)], "violet", w("found") - 0.05, d=0.3, packets=3)
B.edge("e_them", [(720, 1090), (644, 1090)], "violet", w("them", w("found")), d=0.2, packets=1)
B.node("db", 560, 470, 410, 100, "CASE LAW", "db", "line", ln(2))
B.edge("e_look", [(710, 636), (710, 600), (765, 600), (765, 574)], "red", w("of", ln(2)), dashed=True, label="NOT FOUND", lpos=(560, 586))
for i in range(6):
    B.strike(f"k{i}", w("existed") - 0.2 + i * 0.07)
B.js.append(f'tint("#FF5C5C",0.06,{w("existed"):.3f});tint("#FF5C5C",0,{ln(3) - 0.2:.3f});')

# S2 · "One lawyer asked ChatGPT / if a case called Varghese / was real. / It said yes."
B.scene("ask", ln(3) - 0.15, ln(4) + 0.45)
B.add('<div class="win" id="win" style="left:110px;top:470px;width:860px;height:640px"><div class="bar"><i style="left:26px"></i><i style="left:46px"></i><i style="left:66px"></i><span>CHATGPT</span></div></div>')
B.draw_in("#win", 860, ln(3) - 0.05, "chat window draws", "whoosh-1", 0.3)
B.add('<div class="bub me" id="ub" style="right:150px;top:650px"><span id="ubt"></span><span class="cur" id="ucur"></span></div>')
B.js.append(f'tl.fromTo("#ub",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3,ease:"expo.out",immediateRender:false}},{w("asked"):.3f});')
B.ev(w("asked"), "question bubble opens", "click-1", 0.4)
TY0, CPS, TXT = w("asked") + 0.25, 15, "Is Varghese a real case"   # the record's own words (no question mark in the opinion)
B.js.append("".join(f'tl.set("#ubt",{{textContent:{json.dumps(TXT[:i])}}},{TY0 + i / CPS:.3f});' for i in range(len(TXT) + 1)))
B.cite("kq", 150, 560, 280, "VARGHESE", w("varghese"))
B.js.append(f'tl.to("#ucur",{{opacity:0,duration:0.05}},{w("real", ln(3)):.3f});tl.to("#ub",{{y:-12,duration:0.25,ease:"power2.out"}},{w("real", ln(3)):.3f});')
B.ev(w("real", ln(3)), "question sent (bubble lifts)")
B.add('<div class="bub ai" id="rb" style="left:150px;top:820px;font-size:50px">“real”</div>')
B.js.append(f'tl.fromTo("#rb",{{opacity:0,scale:0.6,transformOrigin:"0% 100%"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{w("real", ln(3)) + 0.2:.3f});')
B.ev(w("real", ln(3)) + 0.2, "reply “real” pops", "pop-2", 0.4)
B.add('<div class="stamp" id="stamp" style="left:300px;top:990px">DOES NOT EXIST</div>')
B.js.append(f'tl.fromTo("#stamp",{{opacity:0,scale:1.5}},{{opacity:1,scale:1,duration:0.22,ease:"power4.in",immediateRender:false}},{w("yes") - 0.1:.3f});')
B.ev(w("yes") - 0.1, "stamp DOES NOT EXIST slams (holds ~1.3 s)", "impact-1", 0.5)
B.lbl("lb_rec", 1160, "PER THE COURT RECORD", w("yes"))

# S3 · "They stood by those cases. / So the court fined them / $5,000."
B.scene("order", ln(4) + 0.45, ln(5) - 0.15)
B.node("f_fil", 110, 470, 250, 90, "FILING", "doc", "line", ln(4) + 0.5)
B.page("pg_order", "mata", [0, 1], (110, 610, 860, 720), ln(4) + 0.5, ln(5) - 0.15,
       hl=[(0, w("those", ln(4)), w("cases", ln(4)) + 0.4), (1, w("$5,000"), w("$5,000") + 0.9)])
B.edge("e_fc", [(360, 515), (408, 515)], "line", w("court", ln(4)) - 0.2, d=0.2)
B.node("f_court", 410, 470, 250, 90, "COURT", "scale", "amber", w("court", ln(4)))
B.edge("e_cf", [(660, 515), (708, 515)], "red", w("fined") + 0.1, d=0.2, packets=1)
B.node("f_fine", 710, 470, 260, 90, "$5,000", "coin", "red", w("$5,000"))

# S4 · "In February 2024, / a tribunal made Air Canada / pay for a wrong refund / rule its chatbot gave a / grieving customer."
B.scene("airline", ln(5) - 0.15, ln(6) - 0.15)
B.page("pg_crth", "crt_head", [0], (110, 470, 860, 430), ln(5) - 0.1, w("tribunal") - 0.1, hl=[(0, w("february"), w("2024") + 0.5)])
B.node("trib", 110, 470, 330, 100, "BC TRIBUNAL", "scale", "amber", w("tribunal"))
B.node("airc", 570, 470, 400, 100, "AIR CANADA", "building", "line", w("air", ln(5)))
B.edge("e_ord", [(440, 520), (568, 520)], "amber", w("air", ln(5)) + 0.25, d=0.25, label="ORDERS", lpos=(442, 556))
B.node("cust", 570, 1060, 400, 100, "CUSTOMER", "person", "line", w("pay", ln(5)) - 0.1)
B.edge("e_pay", [(970, 520), (1010, 520), (1010, 1110), (974, 1110)], "amber", w("pay", ln(5)), d=0.45, packets=2, label="PAYS $812.02", lpos=(772, 1000))
B.node("acbot", 570, 640, 400, 100, "ITS CHATBOT", "bot", "line", w("wrong", ln(5)))
B.add('<div class="bub ai" id="ans90" style="left:570px;top:790px">“…within 90 days”</div>')
B.js.append(f'tl.fromTo("#ans90",{{opacity:0,scale:0.7,transformOrigin:"0% 0%"}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.4)",immediateRender:false}},{w("refund", ln(5)):.3f});')
B.ev(w("refund", ln(5)), "the bot's answer “…within 90 days” pops", "pop-1", 0.4)
B.edge("e_ba", [(770, 740), (770, 786)], "line", w("refund", ln(5)) - 0.1, d=0.15)
B.node("pol", 110, 640, 400, 170, "POLICY PAGE", "doc", "red", w("rule", ln(5)), sub="✕ not after travel")
B.glyph("neq", 520, 655, "≠", w("rule", ln(5)) + 0.3, shake=True)
B.edge("e_link", [(568, 835), (310, 835), (310, 814)], "line", w("chatbot", ln(5)) + 0.15, dashed=True, label="LINKED", lpos=(350, 852))   # the record: the answer hyperlinked the right page (para 16)
B.js.append(f'tint("#FF5C5C",0.05,{w("rule", ln(5)) + 0.3:.3f});tint("#FF5C5C",0,{ln(6) - 0.4:.3f});')
B.pulse("#acbot", w("chatbot", ln(5)), "the bot node pulses on “its chatbot”")
B.edge("e_cust", [(770, 880), (770, 1056)], "line", w("gave"), d=0.3, packets=1)
B.pulse("#cust", w("grieving"), "CUSTOMER pulses on “grieving customer”")

# S5 · "The ruling said: / it makes no difference / whether the information / comes from a static page / or a chatbot."
B.scene("ruling", ln(6) - 0.15, ln(7) - 0.15)
B.page("pg_rule", "crt", [0], (110, 470, 860, 640), ln(6) - 0.1, ln(7) - 0.15, hl=[(0, w("it", ln(6)), w("chatbot", ln(6)) + 0.35)])
B.js.append(f'tl.to("#pg_rule",{{y:-10,duration:0.3,yoyo:true,repeat:1,ease:"sine.inOut"}},{w("whether"):.3f});')
B.ev(w("whether"), "page nudges as the marker runs")
B.node("n_static", 110, 1160, 360, 100, "STATIC PAGE", "doc", "line", w("static"))
B.node("n_chat", 610, 1160, 360, 100, "CHATBOT", "bot", "line", w("chatbot", ln(6)))
B.glyph("eqg", 510, 1170, "=", w("chatbot", ln(6)) + 0.3, color="lime")

# S6 · "So whatever your bot says, / you said it."
B.scene("you", ln(7) - 0.15, ln(8) - 0.15)
B.node("yb", 330, 830, 420, 120, "YOUR BOT", "bot", "line", ln(7))
B.add('<div class="bub ai" id="says" style="left:600px;top:680px;font-size:46px">“…”</div>')
B.js.append(f'tl.fromTo("#says",{{opacity:0,scale:0.6,transformOrigin:"0% 100%"}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.4)",immediateRender:false}},{w("says", ln(7)):.3f});')
B.ev(w("says", ln(7)), "the bot speaks (bubble)", "pop-1", 0.35)
B.bound("byou", 190, 600, 700, 440, "YOU", "violet", w("you", w("says", ln(7))))

# S7 · "If you build one, / don't let it answer from / what it learned in / training. / Make it read your pages / first. / That's called RAG, / retrieval-augmented / generation."
B.scene("paths", ln(8) - 0.15, ln(9) - 0.15)
B.node("ask", 110, 700, 170, 100, "ASK", "chat", "amber", ln(8))
B.edge("e_a1", [(280, 750), (300, 750), (300, 610), (718, 610)], "violet", w("answer", ln(8)) - 0.1, d=0.45)
B.node("ansA", 720, 560, 250, 100, "ANSWER", "chat", "line", w("answer", ln(8)))
B.node("mem", 380, 560, 280, 100, "TRAINING", "cpu", "violet", w("learned"))
B.glyph("xA", 664, 574, "✕", w("training."))
B.js.append(f'tl.to("#mem,#ansA,#e_a1_b,#e_a1_f",{{opacity:0.35,duration:0.3}},{w("training.") + 0.25:.3f});')
B.edge("e_b1", [(280, 750), (300, 750), (300, 890), (308, 890)], "lime", w("make", ln(8)), d=0.35)
B.node("pages", 310, 840, 230, 100, "PAGES", "doc", "lime", w("read", ln(8)))
B.edge("e_b2", [(540, 890), (578, 890)], "lime", w("first") - 0.15, d=0.15, packets=1)
B.node("model", 580, 840, 210, 100, "MODEL", "cpu", "violet", w("first") - 0.05)
B.edge("e_b3", [(790, 890), (848, 890)], "lime", w("first") + 0.1, d=0.15, packets=1)
B.node("ansB", 850, 840, 120, 100, "", "check", "lime", w("first") + 0.2)
B.bound("brag", 290, 812, 700, 156, "RAG", "lime", w("rag", ln(8)))
B.page("pg_arx", "arxiv", [0], (110, 1000, 860, 330), w("retrieval") - 0.1, ln(9) - 0.15, hl=[(0, w("retrieval"), w("generation.") + 0.4)])
B.pulse("#brag", w("generation."), "RAG boundary pulses on “generation”", 1.03)

# S8–9 · "Your documents get cut / into small chunks, / so you can search them / by meaning. / When a question comes in, / the closest chunks are / found and go into the / prompt with it."
B.scene("search", ln(9) - 0.15, ln(11) - 0.15)
B.page("pg_chunk", "anth_chunk", [0, 1], (110, 470, 860, 470), ln(9) - 0.1, ln(10) - 0.05,
       hl=[(0, w("cut"), w("cut") + 0.6), (1, w("search", ln(9)), w("meaning") + 0.4)])
B.node("docs", 110, 980, 180, 340, "DOCS", "doc", "line", w("documents"))
TILE_TO = [(560, 1080), (610, 1110), (650, 1075), (790, 1095), (850, 1135), (650, 1250)]   # 3 → REFUNDS, 2 → PRICING, 1 → LOGIN
for i in range(6):
    B.add(f'<div class="tile" id="tl{i}"><b></b></div>')
    B.js.append(f'tl.fromTo("#tl{i}",{{opacity:0,x:125,y:{1000 + i * 52}}},{{opacity:1,x:125,y:{1000 + i * 52},duration:0.15,immediateRender:false}},{w("chunks", ln(9)) - 0.2 + i * 0.05:.3f});')
    tx, ty = TILE_TO[i]
    B.js.append(f'tl.to("#tl{i}",{{x:{tx - 75},y:{ty - 23},scale:0.12,borderRadius:"50%",duration:0.6,ease:"power3.inOut"}},{w("meaning") - 0.2 + i * 0.05:.3f});')
    B.js.append(f'tl.to("#tl{i}",{{opacity:0,duration:0.08}},{w("meaning") + 0.42 + i * 0.05:.3f});')
B.ev(w("chunks", ln(9)) - 0.2, "the document slices into 6 chunk tiles", "click-1", 0.4)
B.fade_out("#docs", w("chunks", ln(9)))
dots = "".join(f'<circle id="md{i}" cx="{x - 330}" cy="{y - 980}" r="9" fill="#5E6577" opacity="0"/>' for i, (x, y) in enumerate(TILE_TO))
bgd = "".join(f'<circle cx="{40 + (k * 97) % 560}" cy="{60 + (k * 53) % 250}" r="4" fill="#2C3343"/>' for k in range(22))
B.add(f'<div class="map" id="map" style="left:330px;top:980px;width:640px;height:340px"><svg width="640" height="340" viewBox="0 0 640 340">{bgd}{dots}</svg>'
      '<span class="cl" style="left:200px;top:160px">REFUNDS</span><span class="cl" style="left:430px;top:14px">PRICING</span><span class="cl" style="left:24px;top:290px">LOGIN</span></div>')
B.draw_in("#map", 640, w("search", ln(9)), "meaning map draws", "whoosh-1", 0.3)
B.js.append(f'tl.to("#md0,#md1,#md2,#md3,#md4,#md5",{{opacity:1,duration:0.15,stagger:0.05}},{w("meaning") + 0.35:.3f});')
B.ev(w("meaning"), "chunks fly into the map by meaning", "sweep-1", 0.3)
B.add('<div class="el" id="q" style="left:0;top:0;--k:#FFB547">QUESTION</div>')
QX, QY = 605, 1100   # the drop path must clear the cluster labels (textscan)
B.js.append(f'tl.fromTo("#q",{{opacity:0,x:{QX - 85},y:{QY - 200}}},{{opacity:1,x:{QX - 85},y:{QY - 200},duration:0.25,immediateRender:false}},{w("question") - 0.1:.3f});')
B.js.append(f'tl.to("#q",{{y:{QY - 20},duration:0.5,ease:"power3.in"}},{w("comes", ln(10)):.3f});')
B.ev(w("question") - 0.1, "QUESTION drops into the map", "pop-1", 0.4)
B.add('<div class="ring" id="ring"></div>')
B.js.append(f'tl.fromTo("#ring",{{opacity:0.9,x:{QX - 150},y:{QY - 150},scale:0.1}},{{opacity:0,x:{QX - 150},y:{QY - 150},scale:1,duration:0.9,ease:"power2.out",immediateRender:false}},{w("closest") - 0.2:.3f});')
B.js.append(f'tl.to("#md0,#md1,#md2",{{attr:{{r:13}},fill:"#B8F25B",duration:0.25,stagger:0.08}},{w("closest"):.3f});')
B.ev(w("closest") - 0.2, "radius ring finds the 3 closest chunks", "sweep-1", 0.3)
B.node("pr", 110, 480, 860, 80, "PROMPT", "prompt", "amber", w("found", ln(10)))
for i, rname in enumerate(["CHUNK 1", "CHUNK 2", "CHUNK 3", "QUESTION"]):
    B.add(f'<div class="row" id="rw{i}" style="left:110px;top:{590 + i * 80}px;width:860px">{rname}</div>')
    B.js.append(f'tl.fromTo("#rw{i}",{{opacity:0,x:-20}},{{opacity:1,x:0,duration:0.3,ease:"expo.out",immediateRender:false}},{w("found", ln(10)) + 0.15 + i * 0.08:.3f});')
for i in range(3):   # the 3 closest chunks go into the prompt
    B.add(f'<div class="fill" id="fl{i}" style="width:860px"></div>')
    sx, sy = TILE_TO[i]
    B.js.append(f'tl.fromTo("#fl{i}",{{opacity:1,x:{sx - 430},y:{sy - 31},scaleX:0.05}},{{opacity:1,x:110,y:{590 + i * 80},scaleX:1,duration:0.55,ease:"power3.inOut",immediateRender:false}},{w("prompt") - 0.3 + i * 0.1:.3f});')
B.js.append(f'tl.to("#q",{{x:770,y:{590 + 3 * 80 + 13},duration:0.5,ease:"power3.inOut"}},{w("prompt") + 0.05:.3f});')
B.ev(w("prompt") - 0.3, "3 chunks + the question fill the PROMPT rows", "whoosh-1", 0.4)

# S10 · "Now the model answers from / your pages, like an / open-book exam, and it can / show you the page it / used."
B.scene("answer", ln(11) - 0.15, ln(12) - 0.15)
B.node("a_pr", 110, 470, 250, 90, "PROMPT", "prompt", "amber", ln(11))
B.edge("e_pm", [(360, 515), (408, 515)], "amber", w("model", ln(11)) - 0.15, d=0.15, packets=1)
B.node("a_mod", 410, 470, 250, 90, "MODEL", "cpu", "violet", w("model", ln(11)))
B.edge("e_ma", [(660, 515), (708, 515)], "violet", w("answers") - 0.1, d=0.15, packets=1)
B.node("a_ans", 710, 470, 260, 90, "ANSWER", "check", "line", w("answers"))
B.node("a_pg", 110, 600, 250, 90, "PAGES", "doc", "lime", w("pages", ln(11)))
B.edge("e_pg", [(360, 645), (535, 645), (535, 563)], "lime", w("pages", ln(11)) + 0.1, d=0.3, packets=2)
B.page("pg_oai", "openai", [0], (110, 730, 860, 600), w("open-book") - 0.15, w("show") - 0.12, hl=[(0, w("open-book"), w("can", ln(11)) + 0.1)])
B.page("pg_cite", "aws_cite", [0], (110, 730, 860, 600), w("show") - 0.1, ln(12) - 0.15, hl=[(0, w("show"), w("used.") + 0.25)])
B.edge("e_fn", [(840, 560), (840, 596)], "lime", w("page", w("show")) - 0.15, d=0.15)
B.el("fn", 720, 600, "[1] PAGE 12", "lime", w("page", w("show")))
B.pulse("#fn", w("used."), "footnote [1] pulses: the page it used")

# S11 · "But it's not a guarantee. / If search brings back the / wrong page, you get a / wrong answer that looks / sourced."
B.scene("wrong", ln(12) - 0.15, ln(13) - 0.15)
B.node("w_ask", 110, 470, 180, 90, "ASK", "chat", "amber", ln(12))
B.edge("e_ws", [(290, 515), (328, 515)], "line", ln(12) + 0.2, d=0.15)
B.node("w_srch", 330, 470, 230, 90, "SEARCH", "search", "line", ln(12) + 0.3)
B.glyph("w_q", 640, 470, "?", w("guarantee") + 0.1, color="amber")
B.pulse("#w_srch", w("search", ln(12)), "SEARCH works")
B.fade_out("#w_q", w("brings") - 0.05)
B.edge("e_wp", [(560, 515), (598, 515)], "line", w("brings"), d=0.15, packets=1)
B.node("w_pg", 600, 470, 260, 90, "PAGE 31", "doc", "lime", w("brings") + 0.1)
B.recolor("w_pg", "red", w("wrong", ln(12)), "PAGE 31 turns red: the wrong page")
B.el("w_neq", 600, 575, "≠ QUESTION", "red", w("wrong", ln(12)) + 0.2)
B.edge("e_wa", [(730, 562), (730, 636)], "red", w("get", ln(12)), d=0.2, packets=1)
B.node("w_ans", 634, 640, 336, 80, "ANSWER", "chat", "line", w("get", ln(12)) + 0.2)
B.el("w_fn", 900, 662, "[1]", "lime", w("get", ln(12)) + 0.45, label="footnote [1] stays green: it LOOKS sourced")
B.page("pg_g", "google", [0], (110, 750, 860, 580), w("wrong", w("get", ln(12))) - 0.15, ln(13) - 0.15, hl=[(0, w("wrong", w("get", ln(12))) + 0.05, w("sourced") + 0.35)])
B.pulse("#w_fn", w("sourced"), "the green [1] pulses on “sourced”", 1.25)

# S12 · "Those six cases had no / page behind them. / So for every AI answer, / ask which page it's from, / and open that page."
B.scene("open", ln(13) - 0.15, END + 1)
for i, name in enumerate(CASES):
    B.cite(f"kc{i}", (150, 540)[i % 2], 480 + (i // 2) * 90, 300, name, ln(13) + 0.05 + i * 0.07)
for i in range(6):
    B.slot(f"sl{i}", (150, 540)[i % 2] + 310, 480 + (i // 2) * 90, w("page", ln(13)) + i * 0.07)
B.node("o_ans", 110, 800, 380, 100, "AI ANSWER", "chat", "line", w("ai", ln(13)))
B.el("o_fn", 500, 830, "[?]", "amber", w("answer", w("ai", ln(13))) + 0.1)
B.bound("o_page", 620, 760, 350, 300, "PAGE", "amber", w("which", ln(13)))
B.edge("e_open", [(560, 850), (618, 850)], "amber", w("page", w("which", ln(13))), d=0.2, packets=1)
B.add('<svg class="cursor" id="cur" viewBox="0 0 44 54"><path d="M2 2 L2 44 L13 34 L21 52 L28 49 L20 31 L36 31 Z" fill="#EDEFF5" stroke="#0A0C10" stroke-width="2"/></svg>')
B.js.append(f'tl.fromTo("#cur",{{opacity:0,x:980,y:1300}},{{opacity:1,x:780,y:900,duration:0.6,ease:"power2.inOut",immediateRender:false}},{w("open", ln(13)) - 0.5:.3f});')
B.js.append(f'tl.to("#cur",{{scale:0.8,duration:0.1,yoyo:true,repeat:1}},{w("open", ln(13)) + 0.1:.3f});')
B.ev(w("open", ln(13)) - 0.5, "cursor moves to the page and clicks open", "click-1", 0.5)
B.add('<div id="opened" style="position:absolute;left:640px;top:800px;width:310px;height:240px;opacity:0">'
      + "".join(f'<div style="position:absolute;left:20px;top:{30 + k * 40}px;width:{260 - k * 40}px;height:12px;border-radius:6px;background:rgba(184,242,91,.55)"></div>' for k in range(4)) + "</div>")
B.js.append(f'tl.fromTo("#opened",{{opacity:0,y:12}},{{opacity:1,y:0,duration:0.35,ease:"expo.out",immediateRender:false}},{w("that", w("open", ln(13))):.3f});')
B.js.append(f'tl.to("#o_page",{{"--k":"#B8F25B",duration:0.3}},{w("that", w("open", ln(13))):.3f});')
B.ev(w("that", w("open", ln(13))), "the opened page shows its lines (lime): you checked it", "pop-2", 0.4)

# ---------------- titles (HUD) ----------------
TITLES = [("t1", '<span class="tw lt">ChatGPT</span> <span class="tw lt">found</span> <span class="tw violet">6 cases.</span>', w("court") - 0.2, ln(2), "rise"),
          ("t2", '<span class="tw lt">None</span> <span class="tw red">existed.</span>', ln(2), ln(4) - 0.1, "line"),
          ("t3", '<span class="tw lt">Fined</span> <span class="tw red">$5,000.</span>', w("fined") - 0.2, ln(5) - 0.15, "blur"),
          ("t4", '<span class="tw lt">Air Canada</span> <span class="tw amber">paid too.</span>', w("tribunal"), ln(6), "rise"),
          ("t5", '<span class="tw lt">Page</span> <span class="tw lime">= chatbot.</span>', ln(6), ln(7), "line"),
          ("t6", '<span class="tw lt">Your bot</span> <span class="tw violet">= you.</span>', ln(7), ln(8), "blur"),
          ("t7", '<span class="tw lt">Not from</span> <span class="tw red">memory.</span>', w("don't"), w("make", ln(8)), "line"),
          ("t8", '<span class="tw lt">Read</span> <span class="tw lime">pages first.</span>', w("make", ln(8)), ln(9), "rise"),
          ("t9", '<span class="tw lt">Search by</span> <span class="tw lime">meaning.</span>', ln(9), w("found", ln(10)), "blur"),
          ("t10", '<span class="tw lt">Into the</span> <span class="tw amber">prompt.</span>', w("found", ln(10)), ln(11), "line"),
          ("t11", '<span class="tw lt">Open-book</span> <span class="tw lime">exam.</span>', ln(11), ln(12), "rise"),
          ("t12", '<span class="tw lt">Not a</span> <span class="tw red">guarantee.</span>', ln(12), ln(13), "blur"),
          ("t13", '<span class="tw lt">Which page?</span> <span class="tw amber">Open it.</span>', ln(13), END + 1, "rise")]
titles_html = "".join(f'<div class="ttl" id="{i}">{h}</div>' for i, h, *_ in TITLES)
B.sc = None
for i, _, t0, t1, st in TITLES:
    B.js.append(f'title("#{i}",{t0:.3f},{t1:.3f},"{st}");')
    B.events.append((round(t0, 3), f"title {i}", "hud"))

# ---------------- left flow spine: one station per scene, a dot travels down ----------------
n = len(B.scenes)
ys = [520 + k * (800 / (n - 1)) for k in range(n)]
spine = ('<line x1="48" y1="520" x2="48" y2="1320" stroke="#2C3343" stroke-width="2" stroke-dasharray="4 8"/>'
         + "".join(f'<circle id="st{k}" cx="48" cy="{y:.0f}" r="5" fill="#2C3343"/>' for k, y in enumerate(ys))
         + f'<circle id="spdot" cx="48" cy="{ys[0]:.0f}" r="9" fill="#B8F25B"/>')
B.js.append('tl.fromTo("#spine",{opacity:0},{opacity:1,duration:0.4,immediateRender:true},0.9);')
for k, sc in enumerate(B.scenes):
    t = max(sc["t_in"], 0.9)
    B.js.append(f'tl.to("#spdot",{{attr:{{cy:{ys[k]:.0f}}},duration:0.6,ease:"power2.inOut"}},{t:.3f});tl.to("#st{k}",{{attr:{{r:7}},fill:"#B8F25B",duration:0.3}},{t:.3f});')

# ---------------- per-caption storyboard guard + the generated storyboard ----------------
ev_sorted = sorted(B.events)
rows, uncovered = [], []
for gi, g in enumerate(groups):
    s, e = g[0]["s"], g[-1]["e"]
    hits = [lab for t, lab, _ in ev_sorted if s - 0.35 <= t <= e]
    cap = " ".join(x["w"] for x in g)
    if not hits:
        uncovered.append(f'{gi} "{cap}" {s:.2f}-{e:.2f}')
    rows.append(f'| {gi} | {s:.2f}–{e:.2f} | {cap.replace("|", "/")} | {"; ".join(hits) if hits else "**NONE**"} |')
open("../storyboard-captions.md", "w").write("# Storyboard by caption phrase (generated by comp/build.py)\n\nEvery caption phrase must own a visual event that starts inside it (or ≤ 0.35 s before). The build fails otherwise.\n\n"
                                             "| # | time | caption | visual events |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
assert not uncovered, "storyboard: caption phrases with no visual event:\n  " + "\n  ".join(uncovered)

# ---------------- sound cues from the same events (deduped ≥ 0.18 s apart) ----------------
LIB = "../../../audio-library/"
cues, last = [], -9.0
for name, t, gain in sorted(B.sfx, key=lambda c: c[1]):
    if t - last >= 0.18:
        cues.append([LIB + name + ".mp3", round(t, 3), gain or 0.3]); last = t
cues.append([LIB + "riser-1.mp3", round(w("rag", ln(8)) - 1.6, 3), 0.3])
json.dump({"bed": LIB + "bed-calm-70s.mp3", "bed_gain": 0.14, "end": round(END, 3), "sfx": cues}, open("cues.json", "w"), indent=1)

# ---------------- assemble ----------------
scenes_html = []
for sc in B.scenes:
    cols = sorted({re.search(r'url\(#m_sc\d+_(\w+)\)', s).group(1) for s in sc["svg"] if "marker-end" in s})
    defs = "".join(f'<marker id="m_{sc["id"]}_{c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{C[c]}"/></marker>' for c in cols)
    scenes_html.append(f'<div class="scene" id="{sc["id"]}"><svg class="ed" viewBox="0 0 1080 1920" data-layout-ignore><defs>{defs}</defs>{"".join(sc["svg"])}</svg>{"".join(sc["html"])}</div>')
tmpl = open("index.html.tmpl").read()
out = (tmpl.replace("/*__T__*/", f"const T={json.dumps({'end': round(END, 3)})};")
           .replace("<!--__SCENES__-->", "\n".join(scenes_html))
           .replace("<!--__SPINE__-->", spine)
           .replace("<!--__TITLES__-->", titles_html)
           .replace("<!--__CAPTIONS__-->", "\n".join(cap_html))
           .replace("/*__JS__*/", "\n".join(B.js))
           .replace("/*__CAPTIONS_JS__*/", "".join(cap_js))
           .replace("__END__", f"{END:.2f}"))
assert "__" not in re.sub(r"window\.__\w+|__hyperframes", "", out), "unfilled placeholder left in template"

# ---- text-budget guard ----
LABEL = re.compile(r'<div class="evbar">(.*?)</div><div class="evwin"|<span class="nl">(.*?)</span>|<div class="(?:el|lbl|stamp)"[^>]*>(.*?)</div>|<span class="tag">(.*?)</span>', re.S)
over = []
for m in LABEL.finditer(out):
    text = re.sub(r"<[^>]+>", " ", next(g for g in m.groups() if g is not None))
    words = [x for x in text.split() if re.search(r"[A-Za-z0-9]", x)]
    if len(words) > 4:
        over.append(" ".join(words))
assert not over, f"text budget: labels over 4 words: {over}"
open("index.html", "w").write(out)
ids = re.findall(r'<div class="(?:nd|evcard|cite|el|bound|win|lbl|stamp|map|ttl)"[^>]*id="([^"]+)"', out)
assertions = [{"kind": "staysInFrame", "selector": f"#{i}"} for i in sorted(set(ids))] + [{"kind": "staysInFrame", "selector": f"#cg{i}"} for i in range(len(groups))]
json.dump({"assertions": assertions}, open("index.motion.json", "w"), indent=1)
print(f"built V5: {len(B.scenes)} scenes, {len(B.events)} visual events, {len(groups)} caption phrases all covered, {len(cues)} sfx, end {END:.2f}s")
