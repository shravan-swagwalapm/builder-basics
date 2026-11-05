# Principles

Every principle here is enforced by something — a tool, a guard, a gate — or it is labelled *judgement*. A rule nobody checks is a wish.

## 1. Prove it: trust the artifact, not the log

| Principle | Enforced by |
|---|---|
| "Build succeeded" proves it compiles, not that it works. Open the rendered file. | `tools/framecheck` decodes **every frame** of the MP4; stills from the real composition at every caption phrase (`hf snapshot`) |
| Approval binds to one exact file. | framecheck report carries the sha256; gate ⑤ approves that hash; a re-render needs a new check |
| A guard you have never seen fail proves nothing. | every guard was red-probed on a known-bad input before its green was trusted (see LESSONS) |
| A checker's expectation is part of the system under test. | read the producer before writing the assertion (LESSONS 12, 16) |
| Fail loud. A missing quote, a covered phrase, an uncovered caption stops the build. | `assert`/`die` in capture, build.py, framecheck — no silent fallbacks |

## 2. Truth: primary sources, real pages, no implied claims

| Principle | Enforced by |
|---|---|
| Primary sources only; every claim in a ledger with a verbatim quote; a "do not use" list. | Stage 2 dossier; cold reviewer fails any unsupported claim |
| Show the source, not a picture of an idea. Real pages beat generated images. | `tools/capture`: real pages, logged out; no generated illustrations (style guide) |
| A quote on screen must exist on the page, inside the photo, and not be covered. | capture guards: identity check, in-photo bounds, `elementFromPoint` occlusion (red-probed) |
| Visuals make claims too. Check what each picture *implies*. | cold reviewer brief: "what does each visual IMPLY?" (caught: a wrong-way PAYS arrow, ✓ on wrong answers) |
| Never say how a system works unless a source says so. | dossier "do not use" (e.g., Air Canada's bot technology is unknown) |

## 3. Privacy and safety

| Principle | Enforced by |
|---|---|
| Nothing leaves the machine before the human uploads. | `tools/hf` allowlist refuses publish/cloud; no cloud video models in QA; incognito captures |
| Keys are read from a file, never printed, never in the repo. | `~/.config/builder-basics/elevenlabs-key.txt` (chmod 600); key-shaped strings masked on captured pages and re-scanned |
| Private people are not named on screen. | `shots.json` `redact` → black bars, re-scan must find 0 |
| Flashes stay under the seizure threshold. | framecheck: WCAG 2.3.1, ≤ 3 flashes/s on the whole frame and 16 blocks (5 Hz probe → FAIL) |
| The human decides; the pipeline never spends or publishes on its own. | three gates; budget caps on the API key; never upgrade a plan; the human uploads |

## 4. Craft

| Principle | Enforced by |
|---|---|
| Plain words for AI-native builders, not engineers. | script-playbook rule 15; cold reviewer |
| Open loop → intensifier → rehook, all closed, all calm. No CTA. | script-playbook rule 16; reviewer quotes loop and closure |
| Each Short picks its visual grammar from its subject; two in a row never share one. | Stage 5a; style guide "Visual grammar per Short" (*judgement* + reviewer) |
| Every caption phrase owns a visual event. | `build.py` fails if a phrase has none (red-probed) |
| The opening is the first spoken fact on its real page at frame 0. | Stage 5a; framecheck "no black frames" + still at 0 s |
| No heavy text: labels ≤ 4 words. | `build.py` text-budget assert |
| No overlapping text, ever. | `tools/framecheck/textscan.mjs` — DOM text boxes on every frame (red-probed on a real collision) |
| One-line karaoke captions, lit while each word is spoken. | caption grouping breaks *before* 26 chars; framecheck "caption lit on every spoken word" |
| Motion has a cause (data travelling, a page being read), never decoration loops. | motion playbook; framecheck motion ≥ 60% of seconds |
| Calm, consistent voice. | one config file (`config/voice.json`), no emotion tags, −14 LUFS mastering |

## 5. Engineering

| Principle | Enforced by |
|---|---|
| One fact, one place. | voice settings only in `config/voice.json`; all timing from the alignment file; repo = the working folder |
| Every stage writes a file the next reads; reuse, never pay twice. | stage outputs; backlog freshness rule (> 7 days → refresh) |
| The best part is no part. Prefer what exists over a new dependency. | headless Chrome from HyperFrames reused for capture and text scan; no extra services |
| A scar that fires twice becomes a mechanical guard. | LESSONS.md → each entry names its guard |
| Private by default. | allowlist `.gitignore`: nothing is published unless named |
