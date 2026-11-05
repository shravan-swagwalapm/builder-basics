# Builder Basics: topic backlog (15, ranked)

Pulled 2026-11-05. Raw data: `research/topic-data.json` (1,929 Shorts with multiples, autocomplete responses, comments, per-topic matches, scores).

## What the evidence says, in five lines

1. **His own best lane is "plumbing that costs money or leaks"**: ENV file 13k (6.2x his 2.1k median), Input/Output Tokens 11k (5.2x), API key 9.4k (4.5x), Context Window 9.2k (4.4x). The same "What is X" format on lower-stakes words did not travel: Terminal 1.5k/1.7k, claude.md 1.6k, What is an LLM 1.9k, What is an AI Agent 1.3k.
2. **"X vs Y" works for him**: /loop vs /goal 11k (5.2x), Terminal vs App 6.8k (3.2x). The only comment pattern on his top 5 is "finally understood the difference".
3. **Competitors' pure concept explainers mostly sit near 1x.** ByteByteGo "What is Prompt Injection?" 0.10x, KodeKloud "What Are AI Guardrails" 0.77x, Tina Huang "Tokens Explained" 1.15x, HelloPM "How RAG Works in 60 Seconds" 2.25x. The outliers that do carry concept words have **stakes or a frame**: Jeff Su "AI Agents explained in 3 steps" 34x, Simon Scrapes "Hackers are stealing your api keys on N8N" 8.75x, Jeff Su "When to use ChatGPT, Gemini, and Claude" 8.92x.
4. **Search demand is strongest for RAG and agents.** "what is rag" is the #1 completion for the whole prefix "what is r". "what is ai agent" is #3 for "what is ai". "what is agentic ai" (#4) and "what is api" (#5) both rank in "what is a". "chatbot vs ai agent" is #1 for "chatbot vs", "localhost vs production" is #1 for "localhost vs" and "n8n vs claude code" is #1 for "n8n vs".
5. **Comments gave no topic signal.** 35 comments across his top 5 Shorts (counting his replies), no questions. Recurring commenters (the same two or three accounts appear on several videos) make it weaker still. One useful line: "This is basic bro" on the ENV Short, a reminder that the hook has to promise a consequence, not a definition.

## Evidence score (0–9)

| Part | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| **A. Competitor outlier**: best on-concept Short in the 1,929-video set, as a multiple of its own channel's median | <1.5x or none | ≥1.5x | ≥3x | ≥8x |
| **B. Search demand**: YouTube autocomplete (gl=IN, hl=en) | nothing on-concept | a few on-concept completions | the seed returns ≥5 on-concept completions incl. "explained", Hindi or PM variants | appears in the top 10 of a broad prefix ("what is r", "what is ai", "chatbot vs") |
| **C. His own data**: his closest Short vs his 2.1k median. Same concept takes the tier, adjacent concept one tier lower | <1.5x | ≥1.5x | ≥2.5x | ≥4x |

Comments aren't scored: none asked a question. Ties are broken by lower freshness risk first, then by topics he hasn't covered.

**Caveats:**
- Autocomplete shows that people search for a term and roughly how it ranks within a prefix. It doesn't give volume.
- Multiples on low-median channels swing hard. Pragati Kunwer's median is 273, so 34k = 124x. Aakash Gupta's median is 715.
- Two Shorts sit at their multiple partly for reasons other than the topic:
  - Cole Medin's 23.8x RAG Short is a free-template giveaway.
  - Jeff Su's 34x agents Short is a talking head with a large channel behind it.

## The backlog

### 1. Your API key goes public the moment you push it. Score 8 (A3 B2 C3) · ✅ MADE 2026-11-06 (research/made.json)
- **Concept:** a key pasted into code travels with `git push`. Bots scan public repos and spend it, so it belongs in `.env`, listed in `.gitignore`, and gets rotated if it ever leaked.
- **Evidence:**
  - Simon Scrapes, "Hackers are stealing your api keys on N8N": 8.75x (21k vs 2.4k).
  - His "What is an API key?" got 9.4k (4.5x) and "What is an ENV file?" 13k (6.2x).
  - Autocomplete: "what is api key" is #2 for "what is api", and "api key kya hai" is #2 for "api key". The leak angle itself barely autocompletes: "api key leak" and "exposed api key" return one suggestion each, and "what is gitignore" two.
- **Diagram:** laptop → `.env` (locked) vs `app.js` (key in plain text) → `git push` → public GitHub → scanner bot → bill counter spinning. Then replay the same flow with `.gitignore` blocking the arrow.
- **Freshness:** low. It won't date.
- **Coverage:** a sequel to two covered Shorts (API key, ENV).
  - It also overlaps with today's prompt-injection Short ("Your AI agent can lose your API keys"). Space them at least 2 weeks apart, and keep this one about git, not agents.

### 2. What is RAG? Score 7 (A3 B3 C1) · ✅ MADE 2026-11-06 (research/made.json)
- **Concept:** before answering, the AI looks up the right pages from your documents and reads them, so it answers from your data instead of from memory.
- **Evidence:**
  - Cole Medin, "Introducing RAG 2.0: Agentic RAG + Knowledge Graphs": 23.8x (169k vs 7.1k). Confound: it's a free-template giveaway.
  - HelloPM, "How RAG Works in 60 Seconds": 2.25x.
  - Autocomplete: **"what is rag" is #1 for "what is r"**, and "rag vs" completes to "rag vs fine tuning" and "rag vs agentic ai".
  - His "I Build Prabhupada AI" (a real RAG product) got 6k (2.9x), counted as adjacent.
- **Diagram:** question → search box → 3 document chunks light up → chunks + question go into the model → answer with citation. A natural 4-node pipeline.
- **Freshness:** low.
- **Coverage:** ⚠ **a draft already exists** at `scratchpad/short/v1-rag/` (script_en.txt, lines.json). Confirm its status before scheduling.

### 3. Localhost vs production: why it works on your laptop and breaks online. Score 6 (A2 B2 C2)
- **Concept:** your laptop has your files, keys and database. The deployed app has none of them until you give them to it. That gap is where most "it broke" moments live.
- **Evidence:**
  - ByteByteGo, "How Big Tech Ships Code to Production": 5.25x (2.0M vs 381k).
  - Fireship, "It works on localhost": 0.85x (1.1M on a 1.3M median).
  - Autocomplete: **"localhost vs production" is #1 for "localhost vs"**. "what is localhost" returns 8 completions, including "in hindi" and "3000".
  - Adjacent to his ENV Short, 13k (6.2x). Environment variables are the usual culprit.
- **Diagram:** two machines side by side (laptop / server) with matching boxes (code, `.env`, database, domain). On the server, the `.env` and DB boxes are empty → red error → fill them → green.
- **Freshness:** low.
- **Coverage:** new.

### 4. AI agent vs workflow vs chatbot. Score 6 (A3 B3 C0)
- **Concept:** a chatbot answers. A workflow follows the steps you drew. An agent picks its own next step in a loop until the goal is met.
- **Evidence:**
  - **Jeff Su, "AI Agents explained in 3 steps": 34x (884k vs 26k).**
  - Autocomplete:
    - "what is ai agent" is #3 for "what is ai", and "what is agentic ai" is #4 for "what is a".
    - "chatbot vs ai agent" is #1 for "chatbot vs".
    - "ai agent vs" completes to "…ai workflow", "…chatbot" and "…agentic ai".
    - "how ai agents work" completes to "…animation", which is this exact format.
  - His own "What is an AI Agent?" got 1.3k (0.6x).
- **Diagram:** three lanes. Chatbot: Q → A. Workflow: fixed boxes A→B→C. Agent: goal → think → tool → observe → loop back, then done.
- **Freshness:** low.
- **Coverage:** ⚠ **covered** by "What is an AI Agent?" (1.3k), "AI Agent is like a human…?" (2.2k) and "AI Agent Is a Dumb Human!" (3k). Only the three-way comparison is new; the definition alone underperformed for him.

### 5. Prompt caching: why your repeat questions cost less. Score 6 (A2 B2 C2)
- **Concept:** when the start of your prompt (instructions, documents) is the same every time, the provider can reuse the work and bill those tokens at a discount, so put the stable text first.
- **Evidence:**
  - Nate Herk, "How to Use Claude Code for 99% CHEAPER": 3.84x (123k vs 32k).
  - Gaurav Sen, "What is Prompt Caching in LLMs?": 1.44x.
  - Autocomplete: "prompt caching" returns 10 completions, including "hindi" and "claude". "llm cost" completes to "llm api cost" and "llm token cost". "what is prompt caching" returns only itself.
  - His Input/Output Tokens Short got 11k (5.2x), and a viewer commented on the token concept. Counted as adjacent.
- **Diagram:** a prompt bar split into stable prefix + new question. The first call pays full price on the whole bar. The second call shows the prefix grayed "cached" with a smaller price tag.
- **Freshness:** medium. The concept is stable, but discount rates and cache lifetimes change. Prices: **not verified**. Check the current provider pricing page before you put a number in the script.
- **Coverage:** new. "How to Save Tokens in Claude?" (2.8k) is near it.

### 6. MCP vs API. Score 6 (A2 B2 C2)
- **Concept:** an API is one app's door, and every AI tool has to learn each door separately. MCP is one standard plug, so any AI can use any tool that speaks it.
- **Evidence:**
  - KodeKloud, "MCP vs UTCP": 3.64x (282k vs 77.5k).
  - Cole Medin, "These are My 3 Must-Have MCP Servers": 4.08x.
  - Autocomplete: "api vs mcp" returns 8 completions, including Hindi. "mcp vs" completes to "…skills", "…claude skills" and "…a2a". "what is mcp" is *not* in the top 10 for "what is m".
  - His "What is MCP in Claude?" got 5.4k (2.6x).
- **Diagram:** before: one AI with N custom wires to N apps. After: the AI with one socket, an MCP hub, and the apps. Classic N×M → N+M.
- **Freshness:** medium. The MCP spec is still moving, and "MCP vs Skills" is the fresher fight.
- **Coverage:** ⚠ **MCP covered**. The "vs API" angle is new.

### 7. Webhook vs API: pull vs push. Score 5 (A2 B2 C1)
- **Concept:** with an API you keep asking "anything new?". With a webhook the other app calls you the moment something happens. That's how payments, forms and n8n flows trigger.
- **Evidence:**
  - Piyush Garg, "What Are Webhooks?": 3.45x (69k vs 20k).
  - Kamran AI Insights, a webhooks Short: 3.11x on a 707 median.
  - Autocomplete: "what is webhook" returns 10 completions, including "in hindi", "in n8n" and "in razorpay". "webhook vs api" returns 5, including "in hindi".
  - His old "APIs for Product Managers Explained" got 5.6k (2.7x). Counted as adjacent.
- **Diagram:** left: your app knocking on Razorpay's door every 5 s ("paid yet?"). Right: Razorpay ringing your app's bell once, "paid ✓".
- **Freshness:** low.
- **Coverage:** new.

### 8. Model routing: the cheap model does, the smart model decides. Score 5 (A3 B2 C0)
- **Concept:** don't run every step on the biggest model. Route routine work to a fast, cheap one and keep the expensive one for judgment calls.
- **Evidence:**
  - **Jeff Su, "When to use ChatGPT, Gemini, and Claude": 8.92x (232k vs 26k).**
  - Pragati Kunwer, "Opus 5 vs Sonnet 5: Let the Cheap One Do the Work, the Smart One Decide": 3.66x on a 273 median.
  - Autocomplete: "claude vs" completes to "…chatgpt vs gemini" and "…codex", and "codex vs claude code" returns 10 completions, including Hindi.
  - His "Opus vs Sonnet" got 1.5k (0.7x) and "Claude Code vs Codex as a PM" 1.3k.
- **Diagram:** a router node splitting a task stream: many small arrows to a small model, a few to a big model, with a cost meter on each.
- **Freshness:** **high if it names models** (they turn over every few weeks). Low if it teaches the routing principle with generic "small/big" boxes.
- **Coverage:** ⚠ **covered** twice, and both underperformed. Only the principle framing is new.

### 9. Frontend, backend, database: every app is three boxes. Score 4 (A1 B2 C1)
- **Concept:** what you see (frontend), the logic and secrets (backend), and the memory (database). AI tools build all three, and the PM has to know which one broke.
- **Evidence:**
  - KodeKloud, "How Database Indexing Works": 2.59x. That's database-adjacent; no on-concept "frontend vs backend" Short is in the set.
  - Autocomplete: "frontend vs backend" returns 10 completions, including "…vs database" and "explained". "what is backend" completes to "what is backend and frontend". "what is a database" returns 10.
  - His "APIs for PMs" got 5.6k, counted as adjacent.
- **Diagram:** three stacked boxes with a request travelling down and back up, and a key icon that lives only in the middle box.
- **Freshness:** low.
- **Coverage:** new.

### 10. Why AI confidently makes things up. Score 4 (A2 B2 C0)
- **Concept:** the model predicts likely next words, not true ones. With no source to look at, "sounds right" wins, which is why grounding (RAG) and evals exist.
- **Evidence:**
  - Neeraj Walia, "STOP using AI as SOURCE in 2026": 5.2x (273k vs 52.5k).
  - Jeff Su, "Why I Want My AI to Hallucinate": 0.96x.
  - Autocomplete: "ai hallucination" completes to "…explained", "…examples" and "…hindi". "why ai hallucinate" returns 2.
  - His "Why 99.5% accurate AI still fails?" got 1.1k (0.5x), counted as adjacent.
- **Diagram:** a word-probability bar chart picking the next token. One path goes to a fabricated citation; the same question plus a document source goes to the right citation.
- **Freshness:** low.
- **Coverage:** new. It pairs with #2 (RAG) as a setup and payoff.

### 11. Context engineering vs prompt engineering. Score 4 (A0 B2 C2)
- **Concept:** a prompt is the one message. Context is everything the model sees: instructions, files, memory, tool results. Most quality comes from choosing what goes in the window.
- **Evidence:**
  - Peter Yang, "The 3 layers of context engineering…": 1.0x. No outlier.
  - Autocomplete: "context engineering vs prompt engineering" and "what is context engineering in hindi", plus "…why it matters for ai agents".
  - His Context Window Short got 9.2k (4.4x), counted as adjacent.
- **Diagram:** the context window as a box filling with labelled blocks (system, CLAUDE.md, files, chat, tool output). The prompt is the smallest block.
- **Freshness:** medium. It's a 2025–26 buzzword, but the mechanism is stable.
- **Coverage:** new. Adjacent to "loop engineering" and "harness".

### 12. Evals: unit tests for AI. Score 3 (A1 B2 C0)
- **Concept:** you can't eyeball an AI feature. Write the questions and expected answers once, then score every model or prompt change against them, sometimes with another AI as the judge.
- **Evidence:**
  - Gaurav Sen, "Evals are the hottest topic in 2026": 1.56x.
  - Peter Yang, "How Linear runs evals on its AI agent": 1.1x.
  - Neel Sikdar, "AI Evals in Flipkart": 0.81x.
  - Autocomplete: **"ai evals" completes to "ai evals for product managers"**, plus "…explained". "llm as a judge" returns 10.
  - His "Why 99.5% accurate AI still fails?" got 0.5x.
- **Diagram:** test set → model v1 / v2 → judge → scoreboard (v2 drops 12%, ship blocked).
- **Freshness:** low.
- **Coverage:** new.
- **Note:** the weakest view evidence of the top 12, but the most PM-specific topic on the list. It's the one to make if the goal is AI-PM authority rather than reach.

### 13. RAG vs fine-tuning vs prompting. Score 3 (A0 B2 C1)
- **Concept:** three ways to make AI know your stuff. Prompting means paste it in. RAG means look it up each time. Fine-tuning means retrain the habits. Start with prompting, add RAG for facts, and fine-tune last, for style.
- **Evidence:**
  - No Short in the set covers it.
  - Autocomplete: **"fine tuning vs" completes first to "fine tuning vs rag"**, then "rag vs fine tuning vs prompt engineering" and "rag vs fine tuning hindi".
  - His Prabhupada AI Short (2.9x) counts as adjacent.
- **Diagram:** three doors to the same model, each with a cost/time/when-to-use tag.
- **Freshness:** low.
- **Coverage:** new. Schedule it after #2.

### 14. Embeddings: how AI searches by meaning. Score 3 (A0 B2 C1)
- **Concept:** text becomes a list of numbers (a point on a map), and similar meanings land close together. That's how RAG finds "refund policy" when you typed "money back".
- **Evidence:**
  - Gaurav Sen, "Google's vector compression algorithm explained": 1.33x. No outlier.
  - Autocomplete: "what is vector database" completes to "…and rag" and "…in hindi". "what is embedding" completes to "…in llm" and "…in rag".
  - His Prabhupada AI Short counts as adjacent.
- **Diagram:** a 2D map where words drop in as dots and cluster. A query dot lands and its 3 nearest neighbours light up.
- **Freshness:** low.
- **Coverage:** new. It's the third of a RAG trilogy (#2 → #14 → #13).

### 15. Tool calling: how a chatbot gets hands. Score 3 (A0 B2 C1)
- **Concept:** the model doesn't run anything. It writes a request ("call weather(Delhi)"), your code runs it and hands back the result, and the model continues. Repeat that and you have an agent loop.
- **Evidence:**
  - No Short in the set covers it.
  - Autocomplete: "agent loop" completes to "…claude", "…claude code" and "…explained". "tool calling" completes to "…in llm". "function calling" completes to "…in ai". "tool calling explained" returns 1.
  - His MCP Short (2.6x) counts as adjacent.
- **Diagram:** a ping-pong between "Model" and "Your code" with a JSON card passing back and forth, then a loop arrow.
- **Freshness:** low.
- **Coverage:** adjacent to "What is loop engineering?" (3k) and "/loop vs /goal" (11k).

## Scored but left out

| Topic | Score | Why it's out |
|---|---|---|
| Agent memory / why AI forgets | 7 (A3 Simon Scrapes memory system 10.83x · B2 · C2 Stateless 5.7k) | **Saturated on his channel**: memory.md 3.8k, Auto-memory 2.8k, Second Brain 4.9k, Why AI Forgets 2.4k, Stateless 5.7k, Agent Gets Dumber 1.4k |
| Prompt injection | 4 (A0: ByteByteGo "What is Prompt Injection?" **0.10x**, Cole Medin 0.37x · B2 · C2) | **Already produced** today (shorts/2026-11-05-prompt-injection). The low competitor multiples are worth knowing before judging its numbers |
| n8n vs Claude Code | 3 (A1 · B2: "n8n vs claude code" #1 for "n8n vs" · C0) | The n8n outliers (AI Learners India, 41x) are build demos, not comparisons. Freshness medium |
| Spec-driven development | 2 (A0 · B2: "spec driven development claude code" · C0) | No view evidence yet. A strong PM fit, so revisit it |
| Guardrails / human-in-the-loop | 2 (A0: KodeKloud 0.77x · B2 · C0) | Partly covered by prompt injection fix #3 |
| System prompt vs user prompt | 1 | Autocomplete is polluted with phone-settings results. He covered "two personality files" (2.2k) |

## Channels added (22 attempted, 21 returned Shorts, 20 ranked)

The existing set had 878 Shorts from 20 channels. This pull added 1,051 Shorts from 21 channels; total 1,929. Pulled with `yt-dlp --flat-playlist --playlist-end 60 --sleep-requests 2`. **Zero HTTP 429s.**

| Channel | Handle | Subs | Shorts | Median | Top multiple |
|---|---|---|---|---|---|
| Malay Krishna (IN, AI PM) | @malay4product | 14.9k | 60 | 8,400 | 36.9x salary-negotiation story |
| Kamran AI Insights (IN, Hindi) | @kamranaiinsights | 12.8k | 23 | 707 | 3.11x webhooks |
| Neel Sikdar (IN, AI PM) | @GeekyBaller | 31.6k | 60 | 1,100 | 7.91x "How to Become an AI PM" |
| Aakash Gupta | @growproduct | 47.4k | 60 | 715 | 44.72x (science trivia; off-niche) |
| Vivek Mishra (IN, Hindi) | @vivekmishrayt | 57.8k | 8 | 3,700 | 2.65x |
| Mayank Aggarwal (IN) | @tech.mayankagg | 74.9k | 32 | 4,550 | 6.37x |
| Pragati Kunwer (IN-origin, Claude Code) | @pragatikunwer | 113k | 60 | 273 | 124.54x "Build Your First AI Agent in 35 Minutes" |
| Peter Yang (AI PM) | @PeterYangYT | 115k | 60 | 1,000 | 2.6x |
| Marina Wyss | @MarinaWyssAI | 158k | 60 | 5,350 | 11.4x career story |
| AI Learners India (Hindi) | @AILearnersbyabhijeet | 182k | 60 | 7,850 | 41.27x n8n agent demo |
| Aishwarya Srinivasan (IN-origin) | @aishwaryasrinivasan | 192k | 60 | 18,500 | 4.05x |
| TrainWithShubham (IN, Hinglish) | @TrainWithShubham | 200k | 60 | 5,850 | 4.44x |
| Cole Medin | @ColeMedin | 231k | 60 | 7,100 | 23.8x RAG 2.0 |
| Piyush Garg (IN, Hinglish) | @piyushgargdev | 427k | 60 | 20,000 | 12.45x |
| Neeraj Walia (IN, Hinglish) | @ezsnippat | 859k | 60 | 52,500 | 12.27x |
| Chai aur Code (IN, Hindi) | @chaiaurcode | 949k | 60 | 37,000 | 35.14x channel announcement |
| Ayushman Pandita (IN, Hindi) | @AyushmanPandita | 1.04M | 60 | 17,500 | 131.43x "Real vs AI Challenge" |
| Nate Herk | @nateherk | 1.11M | 60 | 32,000 | 7.75x |
| ByteByteGo | @ByteByteGo | 1.44M | 27 | 381,000 | 6.3x |
| IBM Technology | @IBMTechnology | 1.84M | 60 | 6,850 | 5.4x |
| Pankaj Shukla (IN) | @pankajjicom | 25.7k | 1 | — | skipped: only 1 Short |

Dave Ebbelaar (@daveebbelaar) returned no Shorts tab.

**Pattern across the Indian channels:** their biggest outliers are career/money stories (Malay's salary negotiations, 13–37x; Marina's income Short) or spectacle (Ayushman's "Real vs AI"). That matches his own 2023 breakouts (405k/292k story Shorts). Concept explainers win on search, not on the feed.

## Not verified

- Current prompt-caching discount rates and cache lifetimes (#5).
- Whether the `v1-rag` draft is finished or abandoned (#2).
- Search *volume* for any term. Autocomplete gives presence and rank only.
- Why any outlier worked. The multiple ranks the video; thumbnail, timing and promotion aren't visible in listings.
