# Script v1: "Which page is this from?" (RAG)

Builder Basics · v2 after cold review (FIX → applied) · est. 75 s · claims map to dossier.md §7 ledger (L#) or section (§)

## Spoken lines (VO) with on-screen state

| # | Beat | VO | On screen | Source |
|---|---|---|---|---|
| 1 | HOOK (open loop) | In 2023, two lawyers in a New York court cited 6 cases that ChatGPT found for them. | 6 case chips (VARGHESE, MILLER, PETERSEN, SHABOON, MARTINEZ, DURDEN) drop into an "IN THEIR FILING" panel | §2, L9 |
| 2 | HOOK | None of them existed. | Each chip flips to a red ✕; proof card: court order, marker on "submitted non-existent judicial opinions" | L9 |
| 3 | HOOK | One lawyer asked ChatGPT if a case called Varghese was real. It said yes. | Chat panel types the record's own words "Is Varghese a real case" → reply chip "“real”" | L11, §2 Finding 45 |
| 4 | SETUP | They stood by those cases. So the court fined them $5,000. | Slot-roll $5,000; tag "NEW YORK COURT · JUN 2023" | L10 (fine followed bad faith: "stood by") |
| 5 | INTENSIFIER | In February 2024, a tribunal made Air Canada pay for a wrong refund rule its chatbot gave a grieving customer. | Bot bubble "within 90 days" → company node turns red; tag "BC TRIBUNAL · FEB 2024" | L1, L2, L6 |
| 6 | INTENSIFIER | The ruling said: it makes no difference whether the information comes from a static page or a chatbot. | Proof card: CRT decision, marker wipes the sentence as spoken | L5 |
| 7 | REHOOK 1 (41%) | So whatever your bot says, you said it. | Bot bubble → arrow → your app icon; title "Your bot = you." | L5 |
| 8 | MECHANISM (named at 45%) | If you build one, don't let it answer from what it learned in training. Make it read your pages first. That's called RAG, retrieval-augmented generation. | Brain/memory node greys out; pages node lights; "THIS IS CALLED → RAG" | L12, L14 |
| 9 | MECHANISM | Your documents get cut into small chunks, so you can search them by meaning. | Page panel splits into chunk tiles → tiles settle into the dot field ("meaning space") | L20, §6 |
| 10 | MECHANISM | When a question comes in, the closest chunks are found and go into the prompt with it. | Question chip enters; scan beam; 3 nearest dots light and fly into a PROMPT panel beside the question | L21, §6 |
| 11 | MECHANISM | Now the model answers from your pages, like an open-book exam, and it can show you the page it used. | Answer types out with a source chip "→ page 12" | L12, §6 ("can include citations") |
| 12 | FINAL TURN (80%) | But it's not a guarantee. If search brings back the wrong page, you get a wrong answer that looks sourced. | Beam picks a wrong dot (red); answer still shows a source chip, now red; proof card: Google Cloud "grounded but off-topic or incorrect" | L15, L16 |
| 13 | CALLBACK (loop closed) | Those 6 cases had no page behind them. So for every AI answer, ask which page it's from, and open that page. | The 6 chips return, each with an empty source slot; title "Which page? Open it." holds 2 s | L9 |

## Rule 16 audit
- **Open loop:** lines 1–3 ("ChatGPT found cases… none existed… it said yes" → how does that happen, and how do you stop it?). **Closed** in line 13 in the hook's words ("Those 6 cases… which page is this from?").
- **Intensifier:** lines 5–6, one second case that raises the stakes from "embarrassing" to "you pay for it".
- **Rehook:** line 7 at 41% ("So whatever your bot says, you said it."), stated flat. Line 12 at 80% is the honest final turn ("But it's not a guarantee"), not a question; 2 turns total.

## Do-not-use guardrails applied
- Never says how Air Canada's bot was built, or that it "hallucinated" / needed RAG (dossier: tribunal had "no information about the nature of its chatbot"; the bot even linked the right page). Air Canada is used only for "the company owns what the bot says".
- "Separate legal entity" not attributed to Air Canada (tribunal's words) — not used at all.
- The $5,000 is framed after "They stood by those cases" (the fine followed bad faith, not AI use).
- No "RAG guarantees accuracy"; line 12 says the opposite (Google Cloud card).
- Callback says "ask which page, and open that page": ChatGPT named sources for the fake cases (Finding 45), so asking alone would not have caught them.
- Line 8 is conditional ("If you build one…") so it never implies Air Canada's bot answered from training data.
- No 67% / 49% Contextual Retrieval numbers (retrieval metric, easy to misread as accuracy).
- Cut for length, kept for a later Short: "under ~500 pages, Anthropic says skip RAG and paste it all" (L18).

## Measured
- 199 words; median sentence 12 words; human score 74.8 PASS (ig-human detect.py; Short #1 was 69.6).
- Names private people never: case chips are the fake case names from the order; capture redacts the parties' and lawyers' names.
