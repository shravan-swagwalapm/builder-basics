# Script v1: "Your API key goes public the moment you push it"

Builder Basics · target 65–80s · claims map to dossier.md §7 ledger (L#) or section (§)

## Spoken lines (VO) with on-screen state

| # | Beat | VO | On screen | Source |
|---|---|---|---|---|
| 1 | HOOK | In 2023, researchers at Orca Security pushed a real cloud key to a public GitHub repo, on purpose. | Laptop → `git push` arrow → GitHub repo node; a gold key chip rides the arrow | L3 (Orca honeypot, AWS key) |
| 2 | HOOK | Two minutes later, someone was using it. | Timer ticks 0:00 → 2:00; red "unknown" node lights and pulls the key | L3 |
| 3 | SETUP | That wasn't a rare event. | Camera pulls back: one repo becomes a wall of repos | — |
| 4 | SETUP | GitGuardian counted 28.65 million secrets in public GitHub commits last year, and leaked AI keys grew 81%. | Counter rolls to 28.65M; an "AI keys" slice grows, +81% chip | L1, L2 |
| 5 | TURN | Because a public commit is searchable, and scanners search all day for anything shaped like a key. | Commit tiles stream past; a scanner beam sweeps; the key-shaped tile flags red | §1 (NDSS polled GitHub Search continuously), L3–L4 |
| 6 | TURN | So deleting the commit doesn't save you. | Delete icon wipes the tile… | L7 |
| 7 | TURN | The key still lives in git history, in forks, and in caches. | …but copies stay lit in three nodes: History, Fork, Cache | L7, §5.1 |
| 8 | TURN | Toyota learned this slowly: a contractor's public repo exposed its server key for almost five years. | Calendar flips Dec 2017 → Sep 2022; "296,019 emails" counter | L9, §3A |
| 9 | MECHANISM | That's why GitHub built push protection. | A shield drops between laptop and GitHub; label "push protection" (concept named ~55%) | L11 |
| 10 | MECHANISM | By default, it stops a push that contains an OpenAI or Anthropic key, and both companies switch reported keys off. | OpenAI + Anthropic key chips bounce off the shield; "disabled" stamp | L11, L12, §4 |
| 11 | MECHANISM | But Gemini API keys aren't on that list. | A Gemini key chip passes straight through the shield | L13 (as of 2026-11-05) |
| 12 | PAYOFF | So keep one rule: your dot env file goes in dot gitignore before your first commit. | `.env` slides into `.gitignore` wall *before* the first commit tile | §6.1 |
| 13 | PAYOFF | And if a key ever leaks, rotate it first. Clean the history later. | Rotate icon (1) lights first, broom over history (2) second | L7, §6.4 |
| 14 | CALLBACK | In that test, two minutes was the whole head start. | Timer returns: 2:00, laptop + key, quiet | L3 |

## Do-not-use guardrails applied
- No "bots find keys in 20 seconds" (NDSS scanner latency, not attackers).
- $82K Gemini bill NOT used: leak vector unknown, would imply GitHub falsely.
- "Before it leaves your laptop" removed: push protection rejects the push at GitHub, so "stops a push" is the accurate phrasing.
- "Both companies switch keys off": Anthropic per its own support page; OpenAI per GitHub's 2021 changelog (medium confidence, its help centre was unreachable).
