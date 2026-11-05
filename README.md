# Builder Basics

An open pipeline that turns one idea into a sourced, faceless, motion-graphics Short (YouTube Shorts / Instagram Reels), driven by Claude Code — and that **checks its own work frame by frame before a human approves it**.

Built for [@TheSwagWalaPM](https://www.youtube.com/@TheSwagWalaPM)'s *Builder Basics* series: plain-English explainers for people who build with AI but are not engineers. The first two Shorts made with it:

| Short | Visual grammar | Real sources on screen | Frame check |
|---|---|---|---|
| *A leaked key got used in 2 minutes* (API keys on GitHub) | journey: neon panels, travelling key, icon stepper | Orca honeypot report, GitGuardian, GitHub docs, Toyota disclosure | 15/15 |
| *What is RAG? 6 fake court cases explain it* | blueprint flowchart: nodes, labelled edges with packets, pages as nodes | the Avianca sanctions order, the Air Canada tribunal ruling, the 2020 RAG paper, OpenAI, Anthropic, AWS, Google Cloud | 16/16 incl. text-overlap scan of all 2,102 frames |

Their sources live in [`shorts/`](shorts/) as worked examples (script, research dossier, storyboard, build script). The videos, voice and captured pages are not in the repo — see *Not included*.

## How it works

`/builder-basics [topic]` in Claude Code runs eight stages. Every stage writes a file the next one reads, so any stage can be re-run without paying for the others. A human approves at three gates.

| # | Stage | What happens | Output |
|---|---|---|---|
| 1 | Topic | Reuse the topic backlog if < 7 days old, else a research agent refreshes it (outlier views vs each channel's median, search suggestions, own-channel data). Topics already made are skipped. | top 3 with evidence |
| 2 | Dossier | A research agent collects **primary sources only**: claims ledger with verbatim quotes + a "do not use" list. | `dossier.md` |
| 3 | Script | 16 writing rules: real case first, plain words, open loop → intensifier → rehook (all closed, all calm), no CTA. A cold reviewer checks every line against the dossier. | `script.md`, `vo.txt` |
| 3b | Evidence | `tools/capture` photographs the real source pages (logged out), masks key-shaped strings, redacts private names, and **fails if a quote is not on the page, outside the photo, or covered**. | `evidence/*.png` |
| | **Gate ①+②** | Human approves topic, script and evidence. | |
| 4 | Voice | ElevenLabs TTS from one config file, two seeds → mastering (−14 LUFS) → forced alignment. | `voice/FINAL.*` |
| | **Gate ③** | Human picks the take. | |
| 5a | Storyboard | Pick this Short's **visual grammar from its subject** (never the previous Short's), then storyboard **every caption phrase**. Opening is the first spoken fact on its real page at frame 0. | `storyboard.md` |
| 5b | Build | [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP) via a local-only wrapper. `build.py` times everything from the alignment; **the build fails if any caption phrase has no visual event**; stills at every phrase → `storyboard/storyboard.html`. | `comp/`, storyboard |
| 6 | Sound | Cached SFX + bed, cues from the same events as the picture. | `mix.wav` |
| 7 | Render + QA | `hf lint` → `hf check` → render → **`tools/framecheck`**: container, every frame decodes, black/frozen, WCAG 2.3.1 flash safety, loudness, A/V sync, caption lit on every spoken word, motion benchmarks, safe zones, evidence hashes, **text overlap on every frame (DOM scan)**, contact sheets → a cold reviewer → fix until SHIP. | `qa/framecheck/report.html` |
| | **Gate ⑤** | Human approves **the sha256 in the report** — a re-render needs a new check. | |
| 8 | Package | Title, description, tags, Instagram caption (linted, AI-tell scan). The human uploads. | `upload.md` |

Nothing leaves the machine before the human uploads: no cloud video models, captures are incognito, the HyperFrames wrapper refuses publish/cloud commands.

## Principles

The rules this pipeline is built on, and the guard that enforces each one: **[PRINCIPLES.md](PRINCIPLES.md)**. The mistakes that produced those guards: **[LESSONS.md](LESSONS.md)**.

## Setup

Requirements: macOS or Linux, Node 18+, Python 3.11+ with `numpy` and `Pillow`, `ffmpeg`, `pdftoppm` (poppler), [Claude Code](https://claude.com/claude-code), an ElevenLabs account (voice clone + API key).

```bash
git clone <this repo> && cd builder-basics
(cd engine && npm ci)                                   # HyperFrames 0.9.16 (pinned) + its headless Chrome
cp config/voice.example.json config/voice.json          # put your ElevenLabs voice_id in it
mkdir -p ~/.config/builder-basics && chmod 700 ~/.config/builder-basics
# paste your ElevenLabs key into ~/.config/builder-basics/elevenlabs-key.txt, then: chmod 600 it
python3 -I tools/sfx.py                                 # build the cached sound library (uses your key)
ln -s "$PWD/skill/builder-basics" ~/.claude/skills/builder-basics
```

Then in Claude Code: `/builder-basics` (or `/builder-basics <topic>`). Set `CHROME_PATH` if the headless Chrome is not under `~/.cache/puppeteer`.

Useful directly:

```bash
node tools/capture/capture.mjs shorts/<slug> --dump           # photograph the sources in evidence/shots.json
python3 -I tools/framecheck/framecheck.py shorts/<slug> <mp4>  # the frame-by-frame approval report
node tools/framecheck/textscan.mjs shorts/<slug>/comp/index.html out.json   # text-overlap scan only
tools/hf lint | check --at-transitions | render | snapshot     # HyperFrames, local-only allowlist
```

## Layout

```
PIPELINE.md            stage table (the spec)
skill/builder-basics/  the Claude Code skill (/builder-basics)
config/                voice.example.json (your voice.json stays local)
tools/                 tts · master · align · mix · sfx · capture · framecheck · motion-qa · topic-research · hf
research/              style guide · script playbook · motion playbook · topic backlog · made.json
shorts/<slug>/         per-Short sources: script, dossier, storyboard, evidence/shots.json, comp/build.py + template
engine/                pinned HyperFrames dependency (npm ci)
```

## Not included (and why)

| Left out | Why | How to regenerate |
|---|---|---|
| Voice takes, `config/voice.json` | a personal voice clone and its ID | your own clone + `tools/tts.py` |
| Rendered videos, storyboards, QA reports | the channel's content; large | the pipeline re-renders them |
| Captured source pages (`evidence/*.png`) | third-party pages | `tools/capture/capture.mjs` from `shots.json` |
| Sound library | generated audio | `tools/sfx.py` |
| Reference reels used for the style study | third-party videos | — |

## Status

Two Shorts shipped. Known gaps: the topic-research scripts in `tools/topic-research/` are one-off agent scripts, not yet a tested tool; each Short's `build.py` still carries its own copy of the shared engine (the `Board` class in the RAG Short is the current kit — extract it once a third Short uses it).

## License

MIT for this repository's code and docs ([LICENSE](LICENSE)). HyperFrames (Apache-2.0) and GSAP are dependencies under their own licenses.
