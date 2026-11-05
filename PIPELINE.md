# Builder Basics pipeline — spec (decided in /grill-me, 2026-11-05)

Command: `/builder-basics [topic]`. One folder per Short in shorts/<date>-<slug>/; each stage writes a file the next reads; any stage can resume.

| # | Stage | Agent / tool | Output | Gate |
|---|---|---|---|---|
| 1 | Topic finder | **research agent**: weekly niche scan (yt-viral outlier multiples across ~40 channels + YouTube autocomplete + own-channel data), tools/topic-research | research/topic-backlog.md, top 3 with evidence | ① Shravan picks |
| 2 | Dossier | research agent: primary sources only, claims ledger, do-not-use list | dossier.md | shown with ② |
| 3 | Script | **script agent**: research/script-playbook.md (16 rules: plain words = 15, open loop + intensifier + rehook = 16), 45–120s flexed by story | script.md + vo.txt | ② Shravan approves |
| 3b | Evidence capture | `node tools/capture/capture.mjs <short>` from `evidence/shots.json` (dossier URLs + verbatim quotes). Real pages photographed logged-out in headless Chrome (PDFs via pdftoppm). Guards fail loud: identity, key-shaped strings masked + re-scanned, phrase found + inside the photo + not covered. Only where a viewer might doubt a claim: ≤ 4 body cards + the opening flash | evidence/*.png + manifest.json | shown with ② (the quotes are the claims) |
| 4 | Voice | tools/tts.py (config/voice.json) → master.py → align.py on FINAL audio; 2 seeds | voice/FINAL.wav + FINAL.align.json | ③ Shravan picks take |
| 5a | Storyboard | visual grammar picked from the script (differs from the last Short); every caption phrase gets a component + real page + motion; contextual opening at frame 0 | storyboard.md | — |
| 5b | Build | HyperFrames via tools/hf; `Board` engine (nodes, labelled edges + packets, pages as nodes, scrolling board, flow spine); build FAILS if a caption phrase has no event; stills at every phrase → storyboard/storyboard.html | comp/ + storyboard/ | shown at ⑤ |
| 6 | Sound | ElevenLabs SFX + Music, cached house library, ducked under VO | audio/ | — |
| 7 | Render + QA | hf lint + check --at-transitions (0 errors) → render → **`tools/framecheck/framecheck.py <short> <mp4>`** (every frame: container, decode, black/frozen, WCAG 2.3.1 flash ≤ 3/s, −14 LUFS/−1 dBTP, A/V sync, caption lit on every spoken word, motion benchmarks, safe zones, evidence sha; contact sheet every 0.5 s) → cold reviewer agent reads report + sheets vs dossier until SHIP | final.mp4 + qa/framecheck/report.html | ⑤ Shravan approves **the sha256 in the report** |
| 8 | Package | /yt-package, /yt-seo, /ig-caption | upload.md | Shravan uploads |

Local-only QA: no video leaves the machine before Shravan uploads (the claude-video Gemini check was declined for that reason, 2026-11-06).
Locked: voice = config/voice.json (D-tag). Budget ₹300–500/Short API spend, ElevenLabs key capped at 60k credits. Never auto-charge, never publish.

Invoke: `/builder-basics [topic]` (~/.claude/skills/builder-basics/SKILL.md).
