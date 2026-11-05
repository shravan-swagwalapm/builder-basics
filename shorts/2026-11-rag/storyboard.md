# Storyboard V5: RAG ("Which page is this from?")

**Visual grammar for this Short: BLUEPRINT FLOWCHART** (chosen from the script: RAG *is* a pipeline, so every beat is a flow that builds node by node).
It must not look like Short #1 (indigo glow ground, rings, neon panels, top icon stepper, full-screen cards only). Differences, by rule:

| | Short #1 (API key) | V5 RAG |
|---|---|---|
| Ground | indigo glows + rotating rings | graphite + blueprint grid (48 px), no glow |
| Unit | neon panel / full-screen card | flowchart node (drawn on, corner ticks) + labelled orthogonal edges with packets |
| Progress | top icon stepper + bar | left "flow spine": one station per scene, a dot travels down |
| Transitions | blur swaps in one stage | the board scrolls: each scene slides up and the next arrives from below |
| Real pages | 3 full cards + flash | 10 sources: flash + pages as **nodes inside the flow** (zoomed to the quote, marker at speaking pace) |
| Accent | periwinkle | lime = grounded/correct, amber = question/prompt, red = fake/wrong, violet = model |

## Beats (times from voice/FINAL.align.json)

| # | Time | VO | Component(s) | Real page (quote marked as spoken) | Motion |
|---|---|---|---|---|---|
| S0 | 0–1.5 | "In 2023," | flash stack (frame 0 = a page, not a wash) | court order · tribunal · RAG paper · Google | 4 hits, 0.35 s apart (≤ 3 flashes/s) |
| S1 | 1.5–7.6 | two lawyers… cited 6 cases that ChatGPT found… None of them existed. | nodes: COURT FILING, 6 citation chips, CHATGPT; then CASE LAW db | — | FILING draws on "court"; chips pop on "six"; CHATGPT draws on "ChatGPT", edge to chips with packets; "None": dashed lookups to CASE LAW each end in red ✕, chips struck |
| S2 | 7.6–12.5 | asked ChatGPT if Varghese was real. It said yes. | chat transcript window | — | user line typed verbatim ("Is Varghese a real case"); reply "“real”" pops on "yes"; red stamp DOES NOT EXIST |
| S3 | 12.5–16.9 | They stood by those cases. So the court fined them $5,000. | flow strip FILING → COURT → $5,000 + court order page node | court order: fake names, then "$5,000 penalty" | strip nodes draw on "stood / court / fined"; page zooms to quote |
| S4 | 16.9–24.0 | a tribunal made Air Canada pay for a wrong refund rule its chatbot gave a grieving customer. | flowchart TRIBUNAL ⚖ → AIR CANADA CHATBOT → ANSWER "…within 90 days" ≠ POLICY PAGE "not after travel"; CUSTOMER → BOT | — | nodes draw on their words; ≠ shakes on "wrong"; packets on "pay" |
| S5 | 24.0–29.6 | The ruling said: it makes no difference… | tribunal decision node | "It makes no difference whether…" | marker wipes word by word |
| S6 | 29.6–32.0 | So whatever your bot says, you said it. | YOUR BOT node; boundary box YOU draws around it | — | containment = ownership |
| S7 | 32.0–41.0 | If you build one… training… read your pages first… That's called RAG, retrieval-augmented generation. | two-path flowchart: Q → MODEL(training) → ANSWER (dashed, struck) vs Q → YOUR PAGES → MODEL → ANSWER (lime); RAG tag | RAG paper (2020): "retrieval-augmented generation (RAG)" | path A greys + ✕ on "don't"; path B draws on "read your pages"; RAG tag on "RAG"; paper marker on "retrieval-augmented generation" |
| S8 | 41.0–45.1 | Your documents get cut into small chunks, so you can search them by meaning. | DOCUMENT node → chunk tiles → meaning map (3 labelled clusters) | Anthropic primer: "Break down the knowledge base" → "…embeddings that encode meaning" | page marker on "cut", tiles fly into clusters on "meaning" |
| S9 | 45.1–49.5 | When a question comes in, the closest chunks are found and go into the prompt with it. | QUESTION chip drops into the map; radius ring; 3 nearest go lime; PROMPT stack node (3 chunk rows + question row) | — | ring on "closest"; chunks fly up into PROMPT rows on "prompt" |
| S10 | 49.5–55.0 | Now the model answers from your pages, like an open-book exam, and it can show you the page it used. | flow PROMPT → MODEL → ANSWER [1] → PAGE 12 | OpenAI: "You have the textbook with you…" then AWS: "The output can include citations…" | footnote edge draws on "show you the page" |
| S11 | 55.0–61.1 | But it's not a guarantee. If search brings back the wrong page, you get a wrong answer that looks sourced. | flow QUESTION → SEARCH → PAGE 31 (red) → MODEL → ANSWER [1] (footnote still green = looks sourced) | Google Cloud: "grounded but off-topic or incorrect" | wrong node flips red on "wrong page" |
| S12 | 61.1–70.0 | Those 6 cases had no page behind them. So for every AI answer, ask which page it's from, and open that page. | 6 citation chips each with an empty red page slot; cursor clicks VARGHESE → page frame opens empty ∅ | — | slots appear on "no page"; click on "open"; holds 2 s |

## Guardrails carried from the script review
- Air Canada scene never names the bot's technology; the ≠ is between the bot's answer and its own policy page only.
- The green footnote in S11 stays green: the answer *looks* sourced; the error lives outside it.
- Fake-case slots stay red to the end (green would read as "passed").
- Private names stay redacted on every page; text labels ≤ 4 words.
