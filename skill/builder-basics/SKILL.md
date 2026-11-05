---
name: builder-basics
description: Make one "Builder Basics" Short for @TheSwagWalaPM end to end — topic research, sourced script, real-page evidence capture, ElevenLabs voice, HyperFrames motion graphics, render, frame-by-frame check — stopping at Shravan's gates. User-invoked: /builder-basics [topic].
disable-model-invocation: true
---

# /builder-basics

Pipeline root: `~/swagwalapm-shorts/`. Spec: `PIPELINE.md`. One folder per Short: `shorts/<YYYY-MM>-<slug>/`. Every stage writes a file the next reads; if a stage's output exists, reuse it — never pay twice.

Read before working: `research/script-playbook.md`, `research/motion-playbook.md`, `research/style-guide.md` (the look is decided — do not reintroduce clay renders or a mascot), `~/.claude/youtube/voice.md`, `config/voice.json`.

## Stages

1. **Topic** — no topic given:
   - **Freshness rule (mechanical):** read the `Pulled YYYY-MM-DD` date on line 3 of `research/topic-backlog.md`. If it is **more than 7 days old**, or Shravan asks for new topics, dispatch a research agent to refresh it (method: `tools/topic-research/`, yt-viral outlier multiples + autocomplete + own-channel data). Otherwise reuse it and say its age.
   - **Skip made topics:** drop every backlog number listed in `research/made.json`; present the top 3 of what remains, with evidence.
2. **Dossier** — research agent, primary sources only → `dossier.md` with a claims ledger and a "do not use" list.
3. **Script** — script agent follows the playbook's 16 rules (plain words for AI-native builders; real case first; open loop → intensifier → rehook, all closed and calm; no CTA). 45–120 s set by the story. → `script.md` + `vo.txt`.
3b. **Evidence** — photograph a real page for every claim, date and definition that has a primary source (V5 used 12: the docket's date, the order, the ruling, the paper, OpenAI, Anthropic ×2, AWS, Google…); write `evidence/shots.json` (dossier URL, `expect` title text, the verbatim quote); run `node tools/capture/capture.mjs shorts/<slug> --dump`. A guard failure means the dossier and the page disagree: fix the dossier quote (it happened: Orca), never loosen the guard. Read `evidence/` photos by eye.
   **Gate ①+② — Shravan approves topic, hook, script and the evidence photos together. Stop and wait.**
4. **Voice** — `tools/tts.py vo.txt` with seeds 42 and 7 → `tools/master.py` → `tools/align.py` on the MASTERED file. Show the cost estimate (characters ≈ credits).
   **Gate ③ — Shravan picks the take. Stop and wait.** Copy the pick to `voice/FINAL.wav` + `FINAL.align.json`.
5a. **Storyboard (per caption phrase)** — read the script and pick this Short's **visual grammar** from its subject (RAG = a pipeline → blueprint flowchart; API key = a journey → stepper + travelling key). It must differ from the previous Short's grammar (style-guide "Visual grammar per Short"). Then storyboard **every caption phrase**: the component, the real page (as a node in the scene, zoomed to its quote, marker wiping as it is spoken) and the motion. The opening is contextual — the first spoken fact on its own real page at frame 0 — never a generic montage.
5b. **Build** — copy the latest Short's `comp/` (RAG V5: `Board` engine = nodes drawn on, labelled orthogonal edges with packets, pages as nodes, scrolling board, flow spine) and write the scenes in `build.py`. Every event registers; **the build fails if any caption phrase has no visual event** (probe-tested). It writes `storyboard-captions.md`; then `tools/hf snapshot --at <every phrase midpoint>` → `storyboard/storyboard.html` (one row per phrase: still + events). Read every still and fix layout before the full render. Assets only from the kit + `evidence/`. No generated illustrations.
6. **Sound** — `audio-library/` (cached SFX + bed); cues come from the same anchors in `build.py` → `tools/mix.py` (−14 LUFS).
7. **Render + QA** — all via `tools/hf` (local-only allowlist): `lint` 0 errors → `check --at-transitions` 0 errors → `render --quality delivery` → `python3 -I tools/framecheck/framecheck.py shorts/<slug> <mp4>` (exit 0 required; every frame checked) → cold reviewer agent gets ONLY `qa/framecheck/report.html` + sheets + `dossier.md` (correctness, what visuals imply, overlaps) → fix and re-run until SHIP.
   **Gate ⑤ — open the MP4, `storyboard/storyboard.html` AND `qa/framecheck/report.html` for Shravan; he approves the sha256 shown. Stop and wait.**
   On approval: set that Short's entry in `research/made.json` to `"status": "approved"` with the sha256, and tag its backlog heading `✅ MADE <date>` (add the entry at stage 3 as `"status": "in progress"` so a half-made topic is never offered twice).
8. **Package** — `/yt-package`, `/yt-seo`, `/ig-caption` → `upload.md`. Shravan uploads. Never publish.

## Hard rules
- Credentials: ElevenLabs key is read from `~/.config/builder-basics/elevenlabs-key.txt`; never print it. Never reuse the PrabhupadaAI key.
- Budget ₹300–500 API spend per Short; key capped at 60k credits/period; never upgrade a plan.
- Never claim a number that is not in the dossier's ledger. Never use anything on its "do not use" list.
- "Build succeeded" is not proof: open frames from the rendered file before showing Shravan.
- Nothing leaves the machine before Shravan uploads: capture is logged-out and incognito; QA is local (no cloud video models).
- Never photograph a page that shows a live secret or a private person's data; the masker is a backstop, not permission.
