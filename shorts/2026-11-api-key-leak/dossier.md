# Research dossier: "Your API key goes public the moment you push it"

Compiled 2026-11-05. Primary sources only.

## 1. How fast leaked keys are found and used

| Study | Method, sample | Finding | Age |
|---|---|---|---|
| Meli et al., NDSS 2019 ([PDF](https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf)) | GitHub Search API polled Oct 2017 to Apr 2018; 201,642 unique secrets | "the median time to discovery was 20 seconds, with times ranging from half a second to over 4 minutes" | data ~8.5 yrs |
| Comparitech ([link](https://comparitech.com/blog/information-security/github-honeypot)) | AWS keys planted in public repos; sample size not stated | "It took just one minute for attackers to find and start abusing the exposed AWS secret key." | updated Jul 2022 |
| Orca Security ([PDF](https://orca.security/wp-content/uploads/2023/06/orca-security-2023-honeypotting-in-the-cloud-report-attacker-tactics-and-techniques-revealed.pdf)) | Honeypots, Jan to May 2023; 1 public repo, AWS key in a .py file | "It took only 2 minutes for an attacker to use the leaked key." (verbatim; checked by tools/capture 2026-11-06) | Jun 2023 |
| Unit 42 "EleKtra-Leak" ([link](https://unit42.paloaltonetworks.com/malicious-operations-of-exposed-iam-keys-cryptojacking/)) | Exposed AWS keys; tracked a live campaign | "detect and launch a full-scale mining operation within five minutes"; 474 likely miner EC2s | Oct 30 2023 |

These measure different things. NDSS's 20 s is the researchers' own scanner, not attackers. Every attacker-speed study used AWS keys; none exists for OpenAI, Anthropic or Gemini keys.

## 2. Scale

- **28.65M** new hardcoded secrets in public GitHub commits in 2025, up 34%. AI-service secrets: 1,275,105, up 81%. Source: GitGuardian, *State of Secrets Sprawl 2026*, Mar 17 2026 ([link](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/)).
- **39M+** secrets "leaked across GitHub in 2024". Source: GitHub, Apr 1 2025 ([link](https://github.blog/security/application-security/next-evolution-github-advanced-security/)). This has a different scope: GitHub's own detections, public and private. Don't compare it with GitGuardian's figure.
- **Validity:** GitGuardian retested the secrets that were valid in 2022: "When we retested that same dataset in January 2026, the validity rate was still above 64%." NDSS: "81% of the secrets we discover were not removed."
- **AI coding (vendor stat):** "Claude Code-assisted commits showed a 3.2% secret-leak rate, versus a 1.5% baseline" (GitGuardian). Correlation, not cause.

## 3. Documented incidents

**A. Toyota T-Connect. Disclosed Oct 7 2022** ([Toyota, JP](https://global.toyota/jp/newsroom/corporate/38095972.html)).
- A contracted web developer uploaded source code to a GitHub account set to public.
- The code held a data-server access key. It stayed public from Dec 2017 to Sep 15 2022.
- Toyota found it Sep 15 and changed the key Sep 17.
- Exposed: up to **296,019** emails and customer IDs. No misuse was confirmed.
- PM angle: a vendor's mistake, unnoticed for five years.

**B. $82,314.44 Gemini bill. Feb 11–12 2026** ([The Register, Mar 3 2026](https://www.theregister.com/2026/03/03/gemini_api_key_82314_dollar_charge/)).
- The team: three developers in Mexico. They "usually spend $180 a month."
- A stolen key ran up about $82K in roughly 48 hours. Google cited shared responsibility. No outcome was reported.
- **The leak vector is unknown** ("somehow compromised").
- Context: Truffle Security ([Feb 25 2026](https://trufflesecurity.com/blog/google-api-keys-werent-secrets-but-then-gemini-changed-the-rules)) found "2,863 live Google API keys" on public webpages that could call Gemini.

**C. xAI keys on GitHub, 2025.**
- May 1 ([Krebs](https://krebsonsecurity.com/2025/05/xai-dev-leaks-api-key-for-private-spacex-tesla-llms/)): a staffer's public repo exposed a key with access to "at least 60 fine-tuned and private LLMs". GitGuardian flagged it Mar 2. It was still valid Apr 30.
- Jul 14 ([Krebs](https://krebsonsecurity.com/2025/07/doge-denizen-marko-elez-leaked-api-key-for-xai/)): Marko Elez committed `agent.py` with an xAI key that could reach 52 LLMs. The key was "not yet been revoked."

**D. Uber 2016, for the misconception beat** ([FTC complaint, Apr 2018](https://www.ftc.gov/system/files/documents/cases/1523054_uber_technologies_revised_complaint_0.pdf)).
- "the key was in plain text in code that was posted to a private GitHub repository."
- Intruders used reused passwords, took 25M+ names and emails, and Uber paid them "$100,000" ([FTC release](https://www.ftc.gov/news-events/news/press-releases/2018/04/uber-agrees-expanded-settlement-ftc-related-privacy-security-claims)).

## 4. What GitHub does today (checked 2026-11-05)

- **Secret scanning:** "Public repositories: Secret scanning runs automatically for free." It covers the "entire Git history on all branches", plus issues, PRs, wikis and gists ([docs](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning)).
- **Push protection for users:** "Is enabled by default." It "Stops you from pushing secrets to public repositories". You can bypass it ([docs](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)). It was rolled out to free accounts from Feb 29 2024, and you can opt out ([changelog](https://github.blog/changelog/2024-02-29-push-protection-is-enabled-for-free-users-on-github/)).
- **Repo-level push protection:** "Is disabled by default." The exception is new public repos on personal accounts, which have it since Mar 11 2024 ([changelog](https://github.blog/changelog/2024-03-11-secret-scanning-and-push-protection-are-enabled-by-default-on-new-public-repositories/)).
- **Partner program** ([patterns table](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns)). "Partner" means GitHub reports the leaked key to the provider.

| Key type | Partner | Push protection |
|---|---|---|
| OpenAI | ✓ | ✓ |
| Anthropic | ✓ | ✓ |
| xAI, AWS, Stripe | ✓ | ✓ |
| Google API key | ✓ | ✗ |
| **Gemini API key** | **✗** | **✗** |

- **What providers do with partner reports:**
  - Anthropic "automatically deactivates the exposed API key" and emails the owner ([support](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure)).
  - OpenAI will "automatically disable them and notify their owners" ([GitHub 2021](https://github.blog/changelog/2021-06-08-rubygems-adobe-and-openai-are-now-github-secret-scanning-integrators/)).
- **Gaps:** known key formats only; one-click bypass.

## 5. Misconceptions

1. **"Deleting the commit fixes it."** No.
   - GitHub: "as a first step you need to revoke and/or rotate that secret."
   - Old commits stay reachable "via their SHA-1 hashes in cached views". In forks, the commit "will continue to be accessible there" ([docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)).
   - Truffle Security, Jul 2024: "the only way to securely remediate a leaked key on a public GitHub repository is through key rotation" ([link](https://trufflesecurity.com/blog/anyone-can-access-deleted-and-private-repo-data-github)).
2. **"A private repo is safe."** Uber's key was in a private repo. GitGuardian: "Internal repos are roughly 6× more likely than public ones to contain hardcoded secrets."
3. **"I'll rotate later."** Attackers act within minutes (section 1).
4. **"The provider will auto-revoke it."** This holds only for partner key types. Gemini keys are not covered. The xAI key stayed live for 2 months.
5. **"`NEXT_PUBLIC_` is fine for a key."** Vercel: "Next.js inlines `NEXT_PUBLIC_` variables into the client bundle at build time" ([docs](https://vercel.com/docs/environment-variables)).

## 6. The fix: a PM checklist

1. **Add `.env` to `.gitignore` before the first commit.** Anthropic says to add .env files to your ignore file ([support](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure)). GitHub: "you must untrack the file before you add a rule to ignore it" ([docs](https://docs.github.com/en/get-started/git-basics/ignoring-files)).
2. **Store keys in platform env vars, not in code.**
   - OpenAI: "Avoid exposing the API keys in your code or in public repositories" ([docs](https://developers.openai.com/api/docs/guides/production-best-practices)).
   - Vercel env vars are "encrypted at rest", and the Secret type is "write-only" ([docs](https://vercel.com/docs/environment-variables)).
3. **Keep push protection on.** Never click bypass on a real key ([docs](https://docs.github.com/en/code-security/concepts/secret-security/push-protection)).
4. **If a key leaks, rotate it first.** Clean the git history after that, if at all (GitHub docs above).
5. **Set hard spend caps.**
   - OpenAI hard limits return 429 errors. "Enforcement is not instantaneous" ([docs](https://developers.openai.com/api/docs/guides/spend-limits)).
   - Anthropic spend limits guard against "unexpected usage due to leaked keys".
   - A Google alerts-only budget "doesn't automatically cap" spending ([docs](https://docs.cloud.google.com/billing/docs/how-to/budgets)). Spend-cap budgets, GA since Oct 13 2026, do cover the Gemini API ([docs](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)).

## 7. Claims ledger

| # | Claim | Source | Quote | Conf. | Caveat |
|---|---|---|---|---|---|
| 1 | 28.65 million secrets leaked in public GitHub commits in 2025. | [GitGuardian](https://blog.gitguardian.com/the-state-of-secrets-sprawl-2026/) | "28.65 million new hardcoded secrets were added to public GitHub commits in 2025 alone" | High | Vendor detection |
| 2 | Leaked AI-service keys rose 81% in a year. | same | "AI service secrets reached 1,275,105, up 81% year over year." | High | Vendor |
| 3 | A key leaked on GitHub was used within 2 minutes. | [Orca](https://orca.security/wp-content/uploads/2023/06/orca-security-2023-honeypotting-in-the-cloud-report-attacker-tactics-and-techniques-revealed.pdf) | "It took only 2 minutes for an attacker to use the leaked key." (verbatim; checked by tools/capture 2026-11-06) | High | AWS key, 1 repo |
| 4 | Within five minutes, a leaked key can be mining crypto. | [Unit 42](https://unit42.paloaltonetworks.com/malicious-operations-of-exposed-iam-keys-cryptojacking/) | "detect and launch a full-scale mining operation within five minutes" | High | AWS, 2023 |
| 5 | Scanners can see a pushed secret in about 20 seconds. | [NDSS](https://www.ndss-symposium.org/wp-content/uploads/2019/02/ndss2019_04B-3_Meli_paper.pdf) | "the median time to discovery was 20 seconds" | Medium | Researchers' scanner; 2018 data |
| 6 | Years later, most leaked keys still work. | GitGuardian | "the validity rate was still above 64%" | High | Keys valid in 2022, retested 2026 |
| 7 | Deleting the commit isn't enough; rotate the key. | [GitHub](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) | "as a first step you need to revoke and/or rotate that secret." | High | — |
| 8 | Uber's key sat in a private repo. | [FTC](https://www.ftc.gov/system/files/documents/cases/1523054_uber_technologies_revised_complaint_0.pdf) | "posted to a private GitHub repository." | High | Entry was via reused passwords |
| 9 | Toyota's key was public for almost five years. | [Toyota](https://global.toyota/jp/newsroom/corporate/38095972.html) | 「2017年12月～2022年9月15日まで…アクセス可能な状態」 | High | JP source; no misuse confirmed |
| 10 | A stolen Gemini key cost a small team $82,314 in two days. | [Register](https://www.theregister.com/2026/03/03/gemini_api_key_82314_dollar_charge/) | "usually spends $180 a month" | Medium | Vector unknown; no outcome |
| 11 | GitHub blocks secret pushes to public repos by default. | [GitHub](https://docs.github.com/en/code-security/concepts/secret-security/push-protection) | "Is enabled by default." | High | Known patterns only; bypassable |
| 12 | Leaked Anthropic keys are switched off automatically. | [Anthropic](https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure) | "Anthropic automatically deactivates the exposed API key." | High | Only where GitHub scans |
| 13 | Gemini keys get no GitHub push protection. | [Patterns](https://docs.github.com/en/code-security/secret-scanning/introduction/supported-secret-scanning-patterns) | Gemini row: Partner ✗, Push protection ✗ | High | As of 2026-11-05 |
| 14 | A Google budget alert won't stop the bill. | [Google](https://docs.cloud.google.com/billing/docs/how-to/budgets) | "Setting an alerts-only budget doesn't automatically cap … usage or spending." | High | Spend caps exist since Oct 2026 |

## Do not use

- **"Bots find keys in 20 seconds."** That figure is NDSS's own polling latency, not attacker timing.
- **"$46K/day" LLMjacking losses** ([Sysdig, May 2024](https://www.sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack)): a modeled worst case ("can be over $46,000 per day"), not a real bill; credentials came from a Laravel CVE, not GitHub.
- **Clutch Security "6.6-min average":** original not found.
- **"OpenAI auto-rotates leaked keys."** This appears only in forum posts. OpenAI's help center returned 403 when I tried to fetch it.
- **"The $82K key leaked via GitHub."** The vector is unknown. Victim details also conflict: one outlet says a solo dev in Vietnam, The Register says a Mexican startup.
- **AI chat logs or screenshots as leak sources:** no primary data; narrate only as a possibility.

## Story options

1. **Toyota (most visual):** a vendor's public repo, five years on the calendar, then 296,019 emails. Primary source, exact dates.
2. **$180 → $82,314 in 48 hours:** the most visceral number for an indie builder. Say "stolen key", never "pushed to GitHub".
3. **xAI key live for 2 months:** a famous AI lab, flagged by a scanner and still not revoked. Shows that auto-revoke won't save you.
4. **Cold-open alternative, Orca honeypot:** push, 2-minute timer, key used. No victim needed.
5. **Close on Uber's private repo** to kill "private = safe".
