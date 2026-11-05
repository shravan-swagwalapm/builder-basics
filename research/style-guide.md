# Builder Basics — visual style guide (v4, 2026-11-06)

Source of truth for the look. Derived from Shravan's two references, measured, not eyeballed:
- **Rethink Systems program film** (`style-ref/shravan-ref.mp4`, 16:9, 60 s) — indigo ground, gradient numerals, dot matrix "this is you.", heavy/light type pairing, tilted glass-chip wall, glowing line chart, word-blur transitions.
- **Algo Reels · System Design 18** (`style-ref/ig-ref/ig-ref.mp4`, 9:16, 71.5 s) — header bar + progress, section tag, persistent stepper, neon hairline panels colour-coded by meaning, "THIS IS CALLED →" concept callouts, karaoke captions mid-frame.
- **Reels reference** (`style-ref/ig-ref2/ig-ref2.mp4`, Instagram DfH6Z5NzECg, 9:16, 89 s) — real GitHub pages as the visuals, inverted marker wiping at speaking pace, digit-roll counter, items popping on the word that names them, crossfade-zoom between cards. Made faceless here.
Rejected (Shravan, 2026-11-05): **isometric clay 3D renders and the cartoon mascot read as kiddish.** Do not reintroduce generated illustrations or characters.

## Measured benchmarks (tools/motion-qa/analyze.py)

| | Rethink film | Algo Reels | Rubric target |
|---|---|---|---|
| (Reels ref) | | | 73% windows · 4.4 s still · 12 cuts · 52% envelope |
| 1-s windows with motion | 90% | 59% | ≥ 60% (aim 85%) — v4 API-key: 75% |
| Longest still | 3.0 s | 6.7 s | ≤ 3.0 s in the first 5 s; ≤ 4.5 s elsewhere (final hold exempt) |
| Hard cuts | 20 (blur cuts) | 0 (one stage) | flash hits + card swaps are the cuts; blur swaps between acts |
| Frame-fill envelope | 32% | 30% | ≥ 30% (airy is the look — do NOT chase 75%) |
| Mean luma | 23 | 13 | dark ground |

## Tokens
- Ground `#07090F`; soft indigo glows `rgba(43,63,158,.5)` / `rgba(30,44,100,.6)` as radial gradients (no CSS blur — it renders blocky under zoom + motion blur). Background lives **outside** the camera layer.
- Ink `#F4F6FF`, mute `#7D86A8`, faint `#3A4160`. Accent periwinkle `#7C8CFF`. Meaning colours: good `#4ADE9A`, warn/secret `#F5B94A`, bad `#FF5A6E`. One accent word per title.
- Type: **Plus Jakarta Sans** 800 (heavy) paired with 300 (light) for titles; **JetBrains Mono** for every label, chip, terminal. Floor **28 px** for anything that carries information (check `text_below_floor`).
- Numerals: Plus Jakarta 800, gradient `#EEF1FF → #7C8CFF`, tabular figures.

## Layout v3 (1080×1920) — Shravan feedback 2026-11-05: "too much text on top, bottom too open"
| y | Element | Layer |
|---|---|---|
| 120 | progress line only — **no header, no series name, no section tags, no episode number** | HUD |
| 162–266 | **icon stepper**: 4 circular icon nodes (no labels) joined by flowing dashed arrows; active node glows in the scene colour | HUD |
| 280–316 | travelling-object lane (the key rides under its node) | HUD |
| 360–440 | title, one line, 2–4 words | HUD |
| 560–1360 | stage (wrapper shifted as ONE block — never shift child `top:` values) | world |
| behind stage | **rotating rings**: 3 dashed orbits (≈4°/s, −2.5°/s, 1.5°/s), stroke-only, recoloured per scene | world |
| 1400 | karaoke caption, one line | HUD |

## Visual grammar per Short (Shravan 2026-11-06: "the RAG one has very similar animations like v1")
- Each Short picks its grammar from its subject; two Shorts in a row never share one. The tokens (fonts, karaoke captions, text budget, real-page cards) are the series identity; the scene language is not.
- Catalogue so far: **journey** (API key: neon panels, rotating rings, top icon stepper, travelling key, glow ground) · **blueprint flowchart** (RAG V5: graphite + 48 px grid, nodes drawn on with registration ticks, labelled orthogonal edges with packets, the board scrolls scene to scene, left flow spine, lime/amber/red/violet meaning colours).
- **Storyboard per caption phrase:** every phrase owns a visual event that starts inside it (build guard). Real pages appear as nodes inside the flow, wherever a claim, date or definition has a primary source.
- **Contextual opening:** frame 0 is the first spoken fact on its real page (RAG: "In 2023" → the docket's filing date marked), never a montage of unrelated sources.

## Opening (Shravan 2026-11-06: "should come on the screen as a flash")
- Nothing static at frame 0. 0–1.2 s: the Short's real source pages deal in as a flash stack (one hit per 0.2 s, slight tilt, pale flash overlay ≤ 0.34, hard cut to the next page), each with its quote already marked. Then the HUD, title and first scene build in.
- Flash safety is measured, not assumed: framecheck fails > 3 flashes/s (WCAG 2.3.1). v4: max 2/s.
- Brands appear only as their own real pages (evidence), never as generated logos.

## Evidence cards (tools/capture → build.py `card()`)
- Only where a viewer might doubt the claim (the hook number, the scale number, the surprising fact): ≤ 4 per Short. Everything else stays motion graphics.
- Card = neon hairline frame + fake browser bar (domain left, date/scope tag right, ≤ 4 words) over the real page, outside the camera layer.
- Motion: blur-in 0.45 s → page pushes from the whole page to the quote (0.8 s, power3.inOut) → slow 4% read-drift → leaves with blur 0.22 s. Hand-offs finish before the card lands (framecheck/`hf check` flag overlaps).
- Marker: white box with `mix-blend-mode: difference` = inverted text, as in the reference. It wipes left→right **across the words while they are spoken** (start = first spoken word of the claim, end = the payoff word).
- Slot-roll numeral for the big scale number: each digit is a strip that rolls two turns and lands (power4.out, stagger 0.05 s).

## Text budget (enforced — build fails otherwise)
- Every label/chip/panel header/tag ≤ **4 words**. `build.py` asserts it and asserts the removed header/section text never returns (probe-tested red on 2026-11-05).
- Meaning comes from icons, arrows, motion and colour; text only names. No sentences on screen except the karaoke caption and the 2–4 word title.
- Sources: one short line ("SOURCE: GITGUARDIAN"), never a sentence.

## Components (kit)
neon hairline panel with mono header · terminal panel with typed lines (authored frame rows) · gradient numeral + mono label + source line · chip (meaning colour) · "THIS IS CALLED" callout (names the concept at ~55%) · dot matrix with one hot dot + mono tag · tilted glass-chip wall (masked values only) · glowing line chart with growing area fill · icon stepper + flowing arrows + travelling object · rotating rings (stroke-only) · arrows between graphics (terminal→cards, A→shield→B, step→step) · two-step timeline · flat timeline bar for durations (never a rising curve unless the data rises).

## Motion rules (HyperFrames motion.md, measured on their films)
- Arrive slow (`expo.out` 0.4–0.5 s, blur 6→0), leave clean (0.2 s, blur out). No bounce on UI; springs only on physical objects (shield, key).
- Vary title entrances within a film: per-word blur, whole-line blur, per-word rise, slot-roll for a reveal word. Landed titles stay dead still.
- Every continuous motion has a cause: the UI working (typing, upload bar, scan beam), the example travelling (key → copies), the world turning (chip wall ≤ 3°/s), impacts (ripples). No pulsing/breathing loops.
- 3–5 transition kinds with a cause: blur swap, colour flood (stolen = red, shield = green, exception = red), camera push, object travel.
- Captions: a group breaks BEFORE the word that would pass 26 characters (one line, always); the next group may arrive early only into silence, never over a word still being spoken. framecheck proves "caption lit on every spoken word".
- Captions: karaoke — grey `#6A7396` until spoken, then ink; keywords periwinkle. One line max.
- Last line holds ≥ 2 s. Every fade-in states its visible end value (`opacity: 1`) — cold render workers seek mid-film.

## Gates (all mechanical, run every render)
`tools/framecheck/framecheck.py` → qa/framecheck/report.html (Shravan approves its sha256) · `tools/hf lint` (0 errors) · `tools/hf check --at-transitions` (0 errors; `index.motion.json` asserts every chip/numeral/panel/title/caption stays in frame) · `tools/motion-qa/analyze.py` vs the table above · frames from the rendered MP4 read by eye · cold reviewer agent vs dossier.
