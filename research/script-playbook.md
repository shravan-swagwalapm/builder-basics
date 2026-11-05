# Builder Basics: Script Playbook

**Evidence base.**
- **Listings:** 1,440 Shorts from 12 channels, ranked by multiple of each channel's median. Channels: Fireship, KodeKloud, ByteByteGo, Jeff Su, Varun Mayya, Ali Abdaal, Vox, Kurzgesagt, Krish Naik, codebasics, CodeWithHarry, Think School. Full ranking in `scripts-corpus/outliers.txt`.
- **Transcripts:** 3 full ones, all Fireship outliers: *computers suck at math* (6.7x), *RGB not RBY* (2.8x), *yottabyte* (1.9x). YouTube returned 429 on subtitle requests 4 and 5, so I stopped there. A transcript-mirror fallback was permission-blocked.
- Treat the rules as directional.

**The surprise.** On titles, outliers (3x or more, n=181) and below-median Shorts (n=262) look the same:
- question form: 29% vs 27%
- a number: 19% vs 19%
- "you": 11% vs 17%

The hook *formula* doesn't separate winners. What happens inside the script has to.

## (a) Rules

1. **Open on a concrete thing.** Sentence 1 has a name, date, figure or quoted artifact. Fireship: "add 0.1 to 0.2"; "in the year 1956 the cutting edge IBM 350".
2. **Real beats hypothetical.** Use a documented event or a demo the viewer can repeat. All 3 Fireship cases are checkable. *Check: source link in the notes.*
3. **One question, closed in the title's words.** Fireship ends: "that's why your computer sucks at math". *Check: last 2 sentences reuse a key noun from the hook.*
4. **Name the concept as the answer, not the intro.** Fireship's first mentions land at 36%, 84% and 89% of the words. *Check: first mention after 30%.*
5. **Chain the beats; don't list them.** Each beat follows from the last through *but*, *so* or *because*. Fireship: 4.0–4.7 causal connectors per 100 words. The current script: 1.9. *Check: at least 3 per 100 words, and at most 2 fragments under 4 words in a row.*
6. **One idea. A list only if it's the spine.** Jeff Su's *AI Agents explained in 3 steps* (38x) promises the list up front. A list tacked on after the payoff is a second Short.
7. **No CTA.** 0 of 3 Fireship transcripts ask for a save, follow or comment. They end on the payoff.
8. **Numbers are sourced and anchored.** "3.5 megabytes", then "one photo from your iPhone" (Fireship).
9. **Names beat nouns.** At least 3 proper nouns (IBM 350, Newton, JavaScript).
10. **An authority must hand over a tool.** "OWASP ranks it #1" is a citation the viewer can't use. Willison's three-part test is something they keep.
11. **Claims say exactly what the source says.** OWASP lists prompt injection as LLM01 but doesn't say the list is ranked by risk.
12. **Calm register.** Fragments make a calm clone swing up and down, which voice.md bans. *Check: median sentence 7–14 words; at most 1 rhetorical question; no hype words.*
13. **Budget words to pace.** Fireship runs 3.5–3.85 words/s, too fast for this voice. Shravan's last take ran 179 wpm. Plan at 165: 96–137 words for 35–50s.
14. **Every sentence changes the diagram.** Each line names the node or edge that appears, lights or breaks.

**vs the installed skills.**
- **What they get right:** no intro, one idea, numbers over adjectives, never fabricate, separate on-screen text, change the frame every beat, a loop line (ig-reel).
- **What they miss:** rules 2, 4, 5, 10, 11 and 14.
- **Where they work against this format:**
  - Both require a closing ask.
  - ig-reel's "short lines" rule and its 4-second beat flag produce staccato.
  - hookscore.py scores the regex form of the hook. It gave the hook below 59.6 and docked it for no "you", but "you" is *rarer* in outliers.
  - yt-script is shaped for long-form (a 15-second hook, 150 wpm).

## (b) Beat template (35–50s at 165 wpm ≈ 2.75 words/s)

| Beat | Time | Words | Job |
|---|---|---|---|
| 1 Hook | 0–4s | 8–12 | Concrete case, belief or question |
| 2 Setup | 4–10s | 15–20 | Who, when, the innocent action |
| 3 Turn | 10–18s | 18–25 | *But*: the hidden thing and what it caused |
| 4 Mechanism | 18–28s | 20–28 | *Because*: why; concept named here |
| 5 Payoff | 28–42s | 25–35 | The one test the viewer keeps |
| 6 Callback | 42–48s | 8–12 | Reframe the hook's object; no CTA |

## (c) Hook archetypes for a calm voice

1. **Documented Incident.** "[Date/name] did [specific, unexpected thing]." Like Fireship's math open (6.7x). *"One hidden line in a Reddit comment took over an AI browser."*
2. **Broken Belief.** State what they were taught, then correct it calmly. Fireship's RGB Short sets up "in kindergarten they taught us…" and breaks it about 3 seconds in. *"Most people think RAG retrains the model. It never touches the model."*
3. **Skeptic's Question.** Ask the objection a smart viewer already has. Examples: KodeKloud *Why We Need MCP When APIs Already Exist* (7.8x), ByteByteGo *Why is Redis so FAST* (3.4x). *"Why does Claude charge more for output tokens than input?"* (Check pricing first.)

## (d) Prompt injection, rewritten

**Critique of the original** (157 words, 52.6s):
- A hypothetical case, when a real one has the same shape.
- Two ideas: the threat, then a 3-fix list from about 33s.
- Staccato: median sentence 4 words, 11 of 33 sentences are 3 words or fewer.
- The OWASP claim overstates the source.
- Two endings: a CTA, then the callback.
- **Kept:** "just text", "a prompt can't fix it", "the fix is design".

**Rewrite:** 136 words, ~49s at 165 wpm, ~46s at 179.

```
[1 HOOK] One hidden line in a Reddit comment took over an AI browser.
   ON SCREEN: Reddit comment, one line glowing → browser node
[2 SETUP] In August 2025, Brave's researchers had Perplexity's Comet summarize that page.
   ON SCREEN: user → "Summarize" → Comet agent
[3 TURN] But under a spoiler tag, the comment held orders for the agent.
So it pulled the user's email, read a login code from Gmail, and posted both on Reddit.
   ON SCREEN: agent → account page → Gmail → Reddit (red edge)
[4 MECHANISM] Why obey a stranger?
Because to the model, your request and that comment are one block of text.
That's prompt injection.
A warning in your prompt won't fix it, because it's just more text.
   ON SCREEN: two text blocks merge; label "prompt injection"
[5 PAYOFF] Simon Willison, who named it, has a test: private data, untrusted content, a way to send things out.
Give an agent all three, and it can be turned against you. So remove one.
That's not a prompt fix. It's a product decision.
   ON SCREEN: the Gmail, Reddit and Reply nodes from beat 3 relabel as the three; one edge cut
[6 CALLBACK] Every page your agent reads, someone else wrote.
   ON SCREEN: back to the Reddit comment
```

**Sources:**
- Brave security blog on Comet, 20 Aug 2025: brave.com/blog/comet-prompt-injection/ (Perplexity disputed the severity).
- Willison, "The lethal trifecta", 16 Jun 2025: simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- Willison coined "prompt injection" on 12 Sep 2022.

## (e) Reviewer rubric (0/1/2 each; ship at ≥17/20; a 0 on R5 or R6 blocks)

- R1 Concrete open in sentence 1.
- R2 Real, sourced case.
- R3 One idea; a list only as the spine.
- R4 Concept named after 30%.
- R5 Every number and claim matches its source.
- R6 96–137 words, and the TTS take ≤50s.
- R7 At least 3 causal connectors per 100 words; at most 2 fragments in a row.
- R8 No CTA; the last line calls back to the hook's object.
- R9 Median sentence 7–14 words, at most 1 rhetorical question, no hype.
- R10 Every line has an on-screen state change.

## (f) Audience language rule (added 2026-11-05 by Shravan)
15. **Plain words for AI-native builders, not engineers.** The viewer builds with Claude Code / Cursor / Lovable but may never have read a git manual. Use everyday words ("your code goes online", "a password for an AI service") and keep a technical term only when it IS the concept — then explain it in the same sentence, in under 10 words. *Check: every term outside a 'common builder words' list (key, prompt, app, AI, model, GitHub, code) is either the named concept or explained inline; reviewer fails the script otherwise.*

## (g) Copy mechanics (added 2026-11-06, Shravan's ask; Claude's judgement on limits)
16. **Open loop → intensifier → rehook, all closed and all calm.**
    - *Open loop:* the first 3 s leave one concrete question the viewer wants answered (API-key Short: a key pushed "on purpose" → what happened?). The last line closes it in the hook's words (rule 3). An unanswered loop is bait: banned.
    - *Intensifier:* the line right after the first answer makes the stakes bigger with a sourced number or a second case ("That wasn't a rare event. 28.65 million…"). One only.
    - *Rehook:* at 40–70% of the runtime, one turn that re-opens curiosity with *so / but* ("So deleting the commit doesn't save you." "But Gemini keys aren't on that list."). At most 2, stated flat — no "but wait", no question stacks (rule 12, calm clone).
    *Check: reviewer quotes the loop line, its closing line, the intensifier and each rehook with its % position; fails the script if the loop is not closed or a rehook is a question.*

