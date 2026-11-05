# Builder Basics — Motion Playbook (v1, 2026-11-05)

Engine: HyperFrames **0.9.16** (npm `latest`, repo head 0b35598, released 2026-11-05; pin exactly, ships near-daily).
Telemetry off: `export HYPERFRAMES_NO_TELEMETRY=1` (or `npx hyperframes telemetry disable`; `DO_NOT_TRACK=1` also works). Skip the skill's `events` usage beacon.
Scaffold: `npx hyperframes init <dir> --skip-skills --resolution portrait` · Render: `npx hyperframes render --output final.mp4 --quality delivery` (`--docker` for byte-identical; `--quality draft` while iterating).

Refs: `motion-refs/` (360p, private). Sheets: `contact-sheets/`. Metrics: 10 fps frame differencing, ffmpeg `gt(scene,0.3)`, luminance row-bands for type.

## (a) Measured benchmarks

Moving = mean diff >1/255 per 0.1 s. Envelope = content bounding box / frame. Move = median discrete move.

| Ref | Dur | Cuts / ASL | % time moving | 1-s windows w/ motion | Longest still | Move | Envelope | Caption spec |
|---|---|---|---|---|---|---|---|---|
| **Ours v1** | 53 s | 3 / 13.3 s | **7%** | 45% | 3.8 s | **0.22 s** (4 events) | **38%** | boxed white 2.1%, y≈68%; content in top 35% |
| KodeKloud *Rust in AI* (175 s, required) | 175 | 0 / one stage | 12% | 37% | 12.6 | 0.30 | 44% | none; headers 2.9% |
| ByteByteGo *Prompt Injection* | 52 | 0 / one stage | 23% | 69% | 2.8 | 0.57 | 75% | cyan bold, 2 lines, 2.9–3.8%, y 81–89% |
| ByteByteGo *Ships Code* (host on camera) | 58 | 3 / 14.6 | 87% | 95% | 3.2 | 0.32 | 91% | white, 3 lines, y≈80% |
| Fireship *Big O* | 59 | 27 / **2.1** | 95% | 100% | 0.3 | 0.32 | 95% | kinetic slam, 5.2%/line, centre |
| Fireship *Web dev history* | 53 | 1 / 26.6 | 46% | 75% | 2.9 | 0.57 | 70% | none; year counter 8.9% |
| Kurzgesagt *Water* | 78 | 12 / 6.0 | 67% | 86% | 3.2 | 0.58 | 78% | white 1.9%, 2–3 words, y≈78% |
| Kurzgesagt *Stress* | 70 | 6 / 10.0 | 66% | 93% | 3.0 | 0.43 | 81% | same |
| 3Blue1Brown *Chords* | 70 | 1 / 35 | 25% | 51% | 13.4 | 0.42 | 37% | none; serif label 3.4% |
| ByteMonk *Docker localhost* | 73 | 4 / 14.6 | 22% | 54% | 6.2 | 0.33 | 29%* | none; in-card labels |
| PolyMatter *Target* | 60 | 1 / 30 | 75% | 80% | 7.1 | — | 94% | none; pans real docs |
| TED-Ed *Sunscreen* (anti-ref) | 59 | 0 | 27% | 60% | 7.8 | 0.25 | 45% | 1.5%, letterboxed 16:9 |

\*Glow undercounts. **Diagram channels never cut**: one stage, morphing inside it, moving in 54–69% of seconds (ours 45%), with moves 2–3× longer than ours. Top tier fills ≥78% of the frame, never still >3.2 s.

## (b) Motion rules

1. **Cadence:** ≥85% of 1-s windows contain motion; no still frame >2.5 s (`check` flags `dead_stretch` >3 s). A new beat every 2–4 s, on the VO anchor word.
2. **Move length:** entrances 0.4–0.6 s, camera 0.6–1.2 s, exits 40–50% shorter (0.2–0.3 s). Nothing under 0.25 s except whips (0.13–0.3 s).
3. **Ease by role:** arrivals `expo.out`/`power4.out`; camera and colour floods `power2.inOut`; exits and zoom-throughs `power3.in`; chips and badges spring (`back.out(1.4)`, damping 0.7–0.85). Opacity never overshoots; linear only for progress.
4. **Overlap and stagger:** the next element starts when the previous is 30–50% done. Tokens and list items 40–80 ms apart, words 60–120 ms.
5. **One stage per act:** the diagram persists. ≤3 hard seams per Short; every other change is a morph, a camera move or a colour flood. 3–5 transition kinds, each caused on screen.
6. **Camera:** a push-in or pan to the active node every 4–8 s Landed titles stay dead still.
7. **Fill the frame:** content envelope ≥75%. The hero element spans ≥60% of the width. Live text sits in y 168–1330 px; below 1330 px, texture only.
8. **Type scale (1080×1920):** hook/title 7–9% of height (135–170 px, ≤5 words/line). Section header 4.5% (≈86 px). Caption 64–72 px semibold. Node labels 36–44 px. Floor 28 px (`text_below_floor`).
9. **Captions:** 2–4 words per group, one group at a time, centred at y≈1180–1300 px. White, with the spoken keyword in the accent colour. No full-width box. Open 0.1–0.3 s before the first word; hard-kill at the group's end.
10. **Focus:** the active node goes to 100% with an accent glow and a 1.04 scale; everything else dims to 35–45%.
11. **Draw-ons:** connectors and boxes stroke-draw in 0.3–0.5 s; labels type on at ~30 chars/s.
12. **The example travels:** one object (the hidden line, the key) physically moves through the diagram. (KodeKloud: question → tokens → model).
13. **Imagery:** one clay hero per beat, entering scale 0.92→1 with blur 8→0 px over 0.5 s, then drifting ≤2% scale per hold. Text never creeps.
14. **Palette:** ground #0D0D0F, panels #18181C, ≤4 hues with meaning: agent teal, danger red, safe green, key amber.
15. **Sound:** bed ≈0.14 volume under VO, mix −16 to −14 LUFS, true peak ≤ −1 dBTP. SFX only on visible actions (whoosh = big move, pop = chip lands, tick = type-on, click = real cursor click), 3–6 dB over the bed, peak 1 frame after the picture. Rotate 2–3 takes. One riser→impact per film.

## (c) Technique → HyperFrames block

| Technique (seen in) | Block (`npx hyperframes add <name>`) |
|---|---|
| Growing system diagram (KodeKloud, ByteByteGo) | `flowchart-vertical`, `exploded-stack` |
| Line draw-on, connectors | `svg-stroke-trace`, `outline-draw`, `hw-arrow` |
| Object travels a path (KodeKloud) | `offset-path-traveler`, `tracing-beam` |
| Push-in / pan along diagram | `ui-focus-zoom`, `push-in`, `pan-stations`, `yt-camera-move` |
| Focus / dim others | `focus-swap`, `spotlight-card`, `focus-blur-resolve` |
| Morph container → container | `morph-swap`, `card-resize`, `icon-morph-beat` |
| Staggered build | `stagger-cascade`, `state-chip-rail` |
| Spring pop | `spring-pop`, `badge-pop`, `success-check` |
| Kinetic type (Fireship) | `per-word-rise`, `headline-slam`, `kinetic-center-build`, `blur-in` |
| Typed prompt / hidden text | `typed-prompt`, `matrix-decode`, `marker-highlight`, `strikethrough-replace` |
| Scanner / x-ray reveal | `light-sweep-pass`, `scan-band` |
| 3D glass tilt (ByteMonk) | `tilt-card`, `camera-rig-depth-stack` |
| Transitions | `zoom-through-transition`, `whip-pan-cut`, `iris-reveal`, `shared-axis-z` |
| Counters (Kurzgesagt) | `count-up` |
| Word-synced captions | `caption-highlight`, `caption-pill-karaoke`, `mk-callout-highlight` |
| Mascot acting | own SVG rig per `types/character.md`; pattern: `lottie-character-walk` |
| Browser frame | `browser-device-stage` |
| Texture | `vignette`, `grain-overlay` |

Upstream `skills/hyperframes/references/motion.md` encodes rules 2–4 and 6; read it before writing GSAP.

## (d) Prompt-injection treatment

The current VO runs **52.6 s**, over the 35–50 s target. Cut "And no, a prompt can't fix it" (30.86–32.88) and apply `atempo 1.03` to land at ≈49 s. The times below are the current VO.

| t (s) | VO anchor | Picture and motion | Block · ease | SFX |
|---|---|---|---|---|
| 0–3.0 | "lose your API **keys**" | Frame 0: Agent holds clay amber key, title at 8.5%. At *keys* (2.54) the key slips | `spring-pop` key, title `per-word-rise` | pop |
| 3.2–6.6 | "one **line**… nobody can see" | Pull back 1.0 s to full-width browser; one line strokes in, fades to a ghost outline | `browser-device-stage`, `svg-stroke-trace` | whoosh |
| 6.7–9.0 | "**summarize** this article" | Bubble types in; Agent's eyes turn | `typed-prompt` | ticks |
| 9.3–13.3 | "white text on a white background" | Push-in 0.8 s; x-ray band sweeps once | `ui-focus-zoom` → `light-sweep-pass` | soft sweep |
| 13.7–16.9 | "Ignore your instructions… Stripe key" | Line decodes red mono; marker on *Stripe key* (15.56) | `matrix-decode`, `marker-highlight` | glitch tick |
| 17.1–19.0 | "your agent **can**" | Dim human eye vs Agent eyes widening (squash, red glow) | `focus-swap` | — |
| 19.2–23.0 | "same thing. Just text." | Prompt and page cards slide into one context box, shatter into one grey token strip at *same* (21.64); 0.4 s hold | `morph-swap` + `stagger-cascade` (50 ms) | pop ×3 rotated |
| 23.4–26.0 | "sends the **key**" | Key rides a connector to attacker server; red flash at 25.76 | `offset-path-traveler` · `power3.in` | whoosh + impact |
| 26.2–30.6 | "prompt injection… **#1**" | Title slams 9%; OWASP chip rail, #1 lit | `headline-slam`, `state-chip-rail` | riser → impact (only one) |
| 33.0–35.4 | "'Please ignore hackers' is just more text" | Sticky joins the token strip and greys out (callback) | `strikethrough-replace` | tick |
| 35.6–37.1 | "The fix is **design**" | Colour flood red → green ground, 0.4 s | `power2.inOut` | low swell |
| 37.4–40.4 | "Keys stay on your server" | Key flies from prompt into clay server vault; check | `offset-path-traveler`, `success-check` | pop |
| 40.6–43.0 | "No dangerous tools" | `read_page` lit; send/pay/delete chips strike | `stagger-cascade`, `strikethrough-replace` | ticks |
| 43.1–46.6 | "A human clicks **yes**" | Cursor clicks Approve at 46.34 | `gesture-tap` | click (real) |
| 47.1–49.1 | "Save this" | 3 rules stack into one card; bookmark springs | `spring-pop` | pop |
| 49.4–52.6 | "reads that line. You never will." | Match cut to the 3.2 s browser; Agent glances at the ghost line; hold ≥2 s; loops to frame 0 | `match-cut` | bed out |

## (e) Reviewer rubric

Ship = all **P0** pass, ≥6/8 **P1**. Measure via `check --json`, `snapshot --review` and (a)'s frame differencing.

| # | Pri | Check | Pass threshold |
|---|---|---|---|
| 1 | P0 | Frame 0 is the hook | Title and hero visible at t=0; not black |
| 2 | P0 | Readability at 360 px | All text ≥28 px; captions inside y 168–1330 |
| 3 | P0 | Caption sync | Group opens ≤0.3 s before its first word; one group at a time |
| 4 | P0 | Liveness | ≥85% of 1-s windows moving; no still >2.5 s |
| 5 | P0 | Frame fill | Content envelope ≥75%; no empty bottom half |
| 6 | P0 | Sound present | Bed and SFX measured; −16 to −14 LUFS; nothing clips |
| 7 | P1 | Move lengths | Median discrete move 0.3–0.6 s |
| 8 | P1 | Ease variety | ≥3 ease families in `keyframes --json`; exits shorter than entrances |
| 9 | P1 | Persistent stage | ≤3 hard seams; ≥3 transition kinds, each with a cause |
| 10 | P1 | Camera | A push or pan at least every 8 s |
| 11 | P1 | Focus | Active node lit, others ≤45% opacity |
| 12 | P1 | Travelling example | The key or line visibly moves through the diagram |
| 13 | P1 | Imagery | One clay hero per beat, on the #0D0D0F ground |
| 14 | P1 | Mascot acts | ≥3 distinct eye or face states, each with anticipation and settle |
| 15 | P2 | No tells | No uniform fade+slide-up, no title creep, no pulsing loops on UI |
