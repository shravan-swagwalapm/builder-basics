# Research dossier: "Your chatbot answers from memory, not from your docs" (RAG)

Compiled 2026-11-06. Primary sources only. Every quote below was matched character-for-character against the raw page fetched on 2026-11-06 (curly quotes, en dashes and typos kept as the page has them).

**Capture notes for tools/capture**
- Moffatt: the CRT page `decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do` is a shell; the decision text loads in an iframe. Photograph the iframe URL directly: `https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do?iframe=true`. CanLII returned HTTP 403 to scripted fetches, so its rendering is unverified.
- Mata: the CourtListener page shows the opinion inside a `<pre>` block with the PDF's original line breaks. Quotes marked ↵ cross a line break on the page. Use the single-line fragments given in the ledger when an exact match is needed.
- Anthropic docs URLs (`docs.claude.com/...`) now redirect to `platform.claude.com/docs/...`. `anthropic.com/news/contextual-retrieval` redirects (308) to `anthropic.com/research/contextual-retrieval`. Use the final URLs.
- PDFs: only the Mata court PDF and the arXiv PDF. Everything else is HTML.

## 1. Hook case: Moffatt v. Air Canada, 2024 BCCRT 149

Source: BC Civil Resolution Tribunal, Small Claims, file SC-2023-005609, Tribunal Member Christopher C. Rivers, issued **February 14, 2024** ([CRT decision, iframe text](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do?iframe=true)). The decision uses they/them for Jake Moffatt and spells the name both "Moffatt" and "Moffat".

**Timeline (all from the decision)**

| Date | Event | Para |
|---|---|---|
| Nov 11 2022 | Grandmother dies in Ontario. Same day Moffatt uses the chatbot on Air Canada's site, and books Vancouver→Toronto for $794.98 (departing Nov 12). | 13, 18 |
| Nov 16 2022 | Books Toronto→Vancouver for $845.38 (departing Nov 18). | 18 |
| Nov 17 2022 | Submits first bereavement-fare application, "well within the 90 days requested by the chatbot." | 20 |
| Feb 5 2023 | Emails Air Canada the chatbot screenshot. | 21 |
| Feb 8 2023 | Air Canada rep admits the chatbot "had provided “misleading words.”" and says it noted the issue "so it could update the chatbot". | 22 |
| Feb 14 2024 | Decision issued. | header |

**What the chatbot said** (para 15, quoting the screenshot):
> Air Canada offers reduced bereavement fares if you need to travel because of an imminent death or a death in your immediate family.
> …
> If you need to travel immediately or have already travelled and would like to submit your ticket for a reduced bereavement rate, kindly do so within 90 days of the date your ticket was issued by completing our Ticket Refund Application form. (emphasis in original)

**What the policy page said.** The decision does NOT quote the page verbatim. It paraphrases (para 17): "The webpage says, in part, the bereavement policy does not apply to requests for bereavement consideration after travel has been completed." The page title was “Bereavement travel” (para 16).

**Key detail: the bot linked the right page.** Para 16: "It is undisputed the words “bereavement fares” were a highlighted and underlined hyperlink to a separate Air Canada webpage titled “Bereavement travel”". So the bot's wrong answer pointed at the correct source. See section 8.

**The "separate legal entity" line.** These are the tribunal's words describing the effect of Air Canada's argument, NOT Air Canada's own words (para 27):
- Air Canada's argument: "Air Canada argues it cannot be held liable for information provided by one of its agents, servants, or representatives – including a chatbot." (en dash)
- Tribunal's gloss: "In effect, Air Canada suggests the chatbot is a separate legal entity that is responsible for its own actions. This is a remarkable submission."
- Finding: "It should be obvious to Air Canada that it is responsible for all the information on its website. It makes no difference whether the information comes from a static page or a chatbot."
- Para 28: "I find Air Canada did not take reasonable care to ensure its chatbot was accurate." and it "does not explain why customers should have to double-check information found in one part of its website on another part of its website."
- Legal basis: negligent misrepresentation (para 24, 32).

**Money (para 34–44).** The decision writes "$"; it is a BC tribunal, so these are Canadian dollars.

| Item | Amount |
|---|---|
| Claimed | $880 (para 3) |
| Paid for two flights | $1,630.36 |
| Would have paid at bereavement fare (incl. taxes/charges) | $979.48 |
| **Damages** | **$650.88** |
| Pre-judgment interest | $36.14 |
| CRT fees | $125 |
| **Total ordered** | **$812.02**, within 14 days (para 44) |
| $200 goodwill coupon | not accepted by Moffatt; no set-off (para 41) |

**How the chatbot was built: the decision says nothing.** Para 14: "While Air Canada did not provide any information about the nature of its chatbot, generally speaking, a chatbot is an automated system that provides information to a person using a website in response to that person’s prompts and input." The words "AI", "LLM", "generative", "model" and "retrieval" do not appear in the decision. → do-not-use list.

## 2. Intensifier case: Mata v. Avianca, Inc., No. 22-cv-1461 (PKC) (S.D.N.Y.)

Source: Opinion and Order on Sanctions, Judge P. Kevin Castel, ECF No. 54, filed **June 22, 2023**, 43 pages ([CourtListener HTML](https://www.courtlistener.com/docket/63107798/54/mata-v-avianca-inc/); [PDF](https://storage.courtlistener.com/recap/gov.uscourts.nysd.575368/gov.uscourts.nysd.575368.54.0.pdf)). Justia returned 403.

- **Who:** "Peter LoDuca, Steven A. Schwartz and the law firm of Levidow, Levidow & Oberman P.C." (p.1).
- **What:** they "submitted non-existent judicial opinions with fake quotes and citations created by the artificial intelligence tool ChatGPT, then continued to stand by the fake opinions after judicial orders called their existence into question." (p.1)
- **Six fake cases** (Finding 36): "Respondents have now acknowledged that the “Varghese”, “Miller”, “Petersen”, “Shaboon”, “Martinez” and “Durden” decisions were generated by ChatGPT and do not exist."
- **First filed** March 1, 2023 (p.2).
- **The fake "Varghese" opinion** (Finding 27): "Its legal analysis is gibberish." ... "The “Varghese” decision abruptly ends without a conclusion."
- **Why he used it** (Finding 37, hearing testimony): "I falsely assumed was like a super search engine called ChatGPT".
- **He asked ChatGPT if the cases were real** (Finding 45): he asked "“Is Varghese a real case”" and "ChatGPT responded that it had supplied “real” authorities that could be found through Westlaw, LexisNexis and the Federal Reporter."
- **Sanction:** "A penalty of $5,000 is jointly and severally imposed on Respondents" (order, item d), plus letters to Mr. Mata and to each judge falsely named as an author of a fake opinion. Rationale: "$5,000 paid into the Registry of the Court is sufficient but not more than necessary to advance the goals of specific and general deterrence."
- The court did not fault AI use itself: "there is nothing inherently improper about using a reliable artificial intelligence tool for assistance." (p.1)
- Caveat: the sanction was for bad faith (standing by the cases after being challenged), not only for the hallucination: "the Court finds bad faith on the part of the individual Respondents based upon acts of conscious avoidance and false and misleading statements to the Court." (p.2)

## 3. What RAG is

**The original paper.** Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", Facebook AI Research / UCL / NYU. Submitted 22 May 2020 (v1); current v4 revised 12 Apr 2021; "Accepted at NeurIPS 2020" ([arXiv abs](https://arxiv.org/abs/2005.11401); [PDF](https://arxiv.org/pdf/2005.11401)).
- Defining sentence (abs page, HTML; note the double hyphen): "We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) -- models which combine pre-trained parametric and non-parametric memory for language generation."
- In the paper the "non-parametric memory" was "a dense vector index of Wikipedia, accessed with a pre-trained neural retriever." (abs page)
- PDF-only, intro: "We endow pre-trained, parametric-memory generation models with a non-parametric memory through a general-purpose fine-tuning approach which we refer to as retrieval-augmented generation (RAG)."
- PDF-only, conclusion: "the retrieval index can be hot-swapped to update the model without requiring any retraining."
- Caveat: the 2020 paper DID fine-tune the retriever and generator together ("both the generator and retriever are jointly learned"). What needs no retraining is updating the knowledge (swapping the index). Today's product-style RAG (bolting search onto an off-the-shelf API model) is a later usage of the name.

**Plain-words vendor definitions (all HTML)**

| Vendor | Quote | URL |
|---|---|---|
| AWS | "Retrieval-Augmented Generation (RAG) is the process of optimizing the output of a large language model, so it references an authoritative knowledge base outside of its training data sources before generating a response." | [aws.amazon.com/what-is/retrieval-augmented-generation](https://aws.amazon.com/what-is/retrieval-augmented-generation/) |
| Anthropic | "RAG is a method that retrieves relevant information from a knowledge base and appends it to the user's prompt, significantly enhancing the model's response." | [anthropic.com/research/contextual-retrieval](https://www.anthropic.com/research/contextual-retrieval) |
| OpenAI | "RAG is the process of Retrieving content to Augment your LLM’s prompt before Generating an answer." | [developers.openai.com/.../optimizing-llm-accuracy](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) |
| OpenAI (analogy) | "You have the textbook with you, and can look up the right information to answer the question with." | same |
| Google Cloud | "RAG, which stands for Retrieval-Augmented Generation, is an AI framework that combines the strengths of traditional information retrieval systems (such as search and databases) with the capabilities of generative large language models (LLMs)." | [cloud.google.com/use-cases/retrieval-augmented-generation](https://cloud.google.com/use-cases/retrieval-augmented-generation) |

The OpenAI "textbook" line is the most builder-friendly: an open-book exam.

## 4. Anthropic Contextual Retrieval (Sep 19, 2024)

Source: [anthropic.com/research/contextual-retrieval](https://www.anthropic.com/research/contextual-retrieval) (page shows "Published Sep 19, 2024", team "Engineering").

- **Why plain RAG misses:** "traditional RAG solutions remove context when encoding information, which often results in the system failing to retrieve the relevant information from the knowledge base."
- **The fix:** "prepending chunk-specific explanatory context to each chunk before embedding". The generated context is "usually 50-100 tokens".
- **Headline:** "This method can reduce the number of failed retrievals by 49% and, when combined with reranking, by 67%."
- **What the number measures:** "We use 1 minus recall@20 as our evaluation metric, which measures the percentage of relevant documents that fail to be retrieved within the top 20 chunks." Averaged across domains (codebases, fiction, ArXiv papers, science papers) with the best embedding setup (Gemini Text 004), top 20 chunks.

| Setup | Top-20 retrieval failure rate | Reduction |
|---|---|---|
| Baseline as stated on the page (the post doesn't spell out its exact setup in the text I quote) | 5.7% | — |
| Contextual Embeddings | 3.7% | 35% |
| Contextual Embeddings + Contextual BM25 | 2.9% | 49% |
| + Reranking | 1.9% | 67% |

Exact lines: "Contextual Embeddings reduced the top-20-chunk retrieval failure rate by 35% (5.7% → 3.7%)." / "Combining Contextual Embeddings and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 49% (5.7% → 2.9%)." / "Reranked Contextual Embedding and Contextual BM25 reduced the top-20-chunk retrieval failure rate by 67% (5.7% → 1.9%)."

Caveats: these are relative reductions in a retrieval metric, not answer accuracy. The 5.7% baseline is Anthropic's best-case setup on its own test sets. Even the best result still misses 1.9%. Cost line: "$1.02 per million document tokens" one-time, with prompt caching and stated assumptions.

## 5. Misconceptions

1. **"RAG retrains the model."** No.
   - AWS: RAG works "all without the need to retrain the model."
   - The paper: the index "can be hot-swapped to update the model without requiring any retraining." (PDF)
   - OpenAI frames retrieval as "in-context memory" vs fine-tuning as "learned memory".
2. **"RAG guarantees correct answers."** No.
   - Google Cloud: "If your retrieved information is irrelevant, your generation could be grounded but off-topic or incorrect."
   - OpenAI: "You can supply the wrong context, so the model can’t possibly answer, or you can supply too much irrelevant context, which drowns out the real information and causes hallucinations."
   - OpenAI: "The model can also get the right context and do the wrong thing with it."
   - Anthropic (retrieval misses): "often results in the system failing to retrieve the relevant information from the knowledge base."
   - Anthropic hallucination guide, about grounding/citation techniques generally (not RAG specifically): "although these techniques significantly reduce hallucinations, they don’t eliminate them entirely."
3. **"Just paste the whole PDF into the prompt."** It depends on size. Do not overstate this one.
   - Anthropic says pasting is the right move for small sets: "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt that you give the model, with no need for RAG or similar methods." (Sep 2024; context windows have since grown.)
   - Anthropic, when it doesn't fit: "For larger knowledge bases that don't fit within the context window, RAG is the typical solution."
   - Limits today ([context windows doc](https://platform.claude.com/docs/en/build-with-claude/context-windows)): current Claude models "have a 1M-token context window", and "A single request can include up to 600 images or PDF pages (100 for models with a 200k-token context window)."
   - More isn't better: "more context isn’t automatically better. As token count grows, accuracy and recall degrade, a phenomenon known as context rot." (same doc)
   - Cost: Google Cloud: "you can use a RAG approach that will reduce the number of tokens, saving you time and cost."
   - OpenAI on long context: "it promises a much simpler retrieval process where you can dump everything in context, but at a cost in accuracy."

## 6. Diagram facts (one source for the whole flow)

Anthropic, Contextual Retrieval ([link](https://www.anthropic.com/research/contextual-retrieval)), "A primer on RAG", verbatim steps:
1. "Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens;"
2. "Use an embedding model to convert these chunks into vector embeddings that encode meaning;"
3. "Store these embeddings in a vector database that allows for searching by semantic similarity."
4. "At runtime, when a user inputs a query to the model, the vector database is used to find the most relevant chunks based on semantic similarity to the query. Then, the most relevant chunks are added to the prompt sent to the generative model."

Second phrasing on the same page: "Add the top-K chunks to the prompt to generate the response."

The **"answer with source"** step is not in Anthropic's flow. Source for it: AWS: "The output can include citations or references to sources." Note "can": citations are optional, not automatic.

AWS mirrors the same flow (embedding → vector database → "relevancy search" → "Augment the LLM prompt"). Use it as a backup.

## 7. Claims ledger

| # | Claim | Source | Quote (verbatim) | Conf. | Caveat |
|---|---|---|---|---|---|
| 1 | Air Canada's chatbot told a grieving customer he could claim the bereavement fare after travel, within 90 days. | [CRT](https://decisions.civilresolutionbc.ca/crt/crtd/en/item/525448/index.do?iframe=true) | "If you need to travel immediately or have already travelled and would like to submit your ticket for a reduced bereavement rate, kindly do so within 90 days of the date your ticket was issued" | High | Screenshot text as quoted in para 15 |
| 2 | Air Canada's own policy page said the opposite. | same | "the bereavement policy does not apply to requests for bereavement consideration after travel has been completed" | High | Tribunal's paraphrase of the page, not the page itself |
| 3 | Air Canada argued it wasn't liable for what its chatbot said. | same | "Air Canada argues it cannot be held liable for information provided by one of its agents, servants, or representatives – including a chatbot." | High | En dash on page |
| 4 | The tribunal called that treating the bot as "a separate legal entity" and rejected it. | same | "In effect, Air Canada suggests the chatbot is a separate legal entity that is responsible for its own actions. This is a remarkable submission." | High | Tribunal's words, not Air Canada's |
| 5 | Static page or chatbot: the company owns the answer. | same | "It makes no difference whether the information comes from a static page or a chatbot." | High | — |
| 6 | Air Canada had to pay $812.02. | same | "I order Air Canada to pay Mr. Moffatt a total of $812.02" | High | CAD; $650.88 damages + $36.14 interest + $125 fees |
| 7 | Air Canada's own rep admitted the bot gave "misleading words". | same | "admitted the chatbot had provided “misleading words.”" | High | Feb 8 2023 email, as reported in para 22 |
| 8 | The ruling says nothing about how the bot worked. | same | "Air Canada did not provide any information about the nature of its chatbot" | High | Kills any "it was RAG/LLM" claim |
| 9 | Lawyers filed six court cases ChatGPT made up. | [CourtListener](https://www.courtlistener.com/docket/63107798/54/mata-v-avianca-inc/) | "decisions were generated by ChatGPT and do" ↵ "not exist." | High | Spans a line break; single-line fragment: "submitted non-existent judicial opinions with fake quotes and citations" |
| 10 | They were fined $5,000. | same | "A penalty of $5,000 is jointly and severally imposed on Respondents" | High | Docket-entry text (one line); also order item d, p.34 (crosses a line break there); rationale on p.33. Sanction was for bad faith, not only the error |
| 11 | ChatGPT told the lawyer the fake cases were real. | same | "ChatGPT" ↵ "responded that it had supplied “real” authorities" | High | Spans a line break; single-line fragment: "responded that it had supplied “real” authorities that could be found through Westlaw," |
| 12 | RAG = look it up first, then answer. | [AWS](https://aws.amazon.com/what-is/retrieval-augmented-generation/) | "references an authoritative knowledge base outside of its training data sources before generating a response" | High | — |
| 13 | RAG doesn't retrain the model. | same | "all without the need to retrain the model" | High | 2020 paper did fine-tune; see §3 |
| 14 | RAG was named in a 2020 paper. | [arXiv](https://arxiv.org/abs/2005.11401) | "We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG)" | High | Facebook AI/UCL/NYU; NeurIPS 2020 |
| 15 | Wrong chunk retrieved → wrong answer, even with RAG. | [Google Cloud](https://cloud.google.com/use-cases/retrieval-augmented-generation) | "If your retrieved information is irrelevant, your generation could be grounded but off-topic or incorrect." | High | — |
| 16 | Even with the right page, the model can still botch it. | [OpenAI](https://developers.openai.com/api/docs/guides/optimizing-llm-accuracy) | "The model can also get the right context and do the wrong thing with it." | High | — |
| 17 | Better chunking cut retrieval misses by 49%, 67% with reranking. | [Anthropic](https://www.anthropic.com/research/contextual-retrieval) | "This method can reduce the number of failed retrievals by 49% and, when combined with reranking, by 67%." | High | Relative cut in 1−recall@20 (5.7% → 2.9% / 1.9%); retrieval metric, not answer accuracy |
| 18 | Under ~500 pages, just paste it in. | same | "If your knowledge base is smaller than 200,000 tokens (about 500 pages of material), you can just include the entire knowledge base in the prompt" | High | Sep 2024; windows now up to 1M tokens |
| 19 | Stuffing more in makes the model worse. | [Anthropic docs](https://platform.claude.com/docs/en/build-with-claude/context-windows) | "As token count grows, accuracy and recall degrade, a phenomenon known as context rot." | High | — |
| 20 | Diagram: docs → chunks. | [Anthropic](https://www.anthropic.com/research/contextual-retrieval) | "Break down the knowledge base (the “corpus” of documents) into smaller chunks of text, usually no more than a few hundred tokens;" | High | — |
| 21 | Diagram: top chunks go into the prompt. | same | "the most relevant chunks are added to the prompt sent to the generative model." | High | — |

## Do not use

- **"Air Canada's chatbot used RAG / an LLM / generative AI / ChatGPT."** No primary source says this. The tribunal says Air Canada gave no information about the bot's nature (para 14). Narrate it as "a chatbot", never as a specific technology.
- **"Air Canada's bot wasn't grounded in its docs, so RAG would have fixed it."** Unsupported, and the record cuts against it: the bot's answer hyperlinked the correct policy page (para 16). Use Air Canada only for "the company owns what the bot says".
- **"Air Canada said the chatbot is a separate legal entity."** Those are the tribunal's words ("In effect, Air Canada suggests..."). Say "Air Canada argued it wasn't liable for its chatbot" or quote the tribunal.
- **A verbatim quote of Air Canada's bereavement page as of Nov 2022.** The decision only paraphrases it. The Wayback Machine was offline on 2026-11-06, so the 2022 page could not be checked. Today's page is not evidence of the 2022 wording.
- **"The bot invented a policy" / "hallucinated."** The decision never uses "hallucinat*", "AI" or "invented". Say "the chatbot gave the wrong rule" or "misleading words" (Air Canada's own rep).
- **"Air Canada paid $880."** That was the claim. The order was $812.02 total, $650.88 in damages.
- **"The chat happened before ChatGPT existed."** ChatGPT's public launch date (widely cited as Nov 30, 2022, after Moffatt's Nov 11, 2022 chat) could not be verified: openai.com returned 403. Even if true, it doesn't show what Air Canada's bot was.
- **"Lawyers were fined for using ChatGPT."** The court said AI use is not "inherently improper"; the fine followed bad faith (standing by fake cases after being challenged). Say "fined after filing cases ChatGPT made up, then standing by them."
- **"Mata's ChatGPT had no retrieval / was a plain LLM."** The opinion doesn't describe ChatGPT's internals. Fine to say it "made up" cases; don't call it a "no-RAG" case as if from the record.
- **"Contextual Retrieval makes answers 67% more accurate."** It cut the retrieval-failure rate by 67%, relative (5.7% → 1.9%), on Anthropic's own tests.
- **"Never paste the whole PDF."** Anthropic recommends pasting for knowledge bases under 200,000 tokens. Frame it as "past a few hundred pages, or for a whole company wiki, you need RAG."
- **CanLII as the capture URL.** It returned 403 to scripts; use the CRT iframe URL.

## 8. Things that cut against the "Air Canada → RAG" framing

1. **The technology is unknown.** The bot could have been scripted, keyword-matched, or an LLM. The record is silent.
2. **The bot linked the right document.** Its answer hyperlinked the correct "Bereavement travel" page and still contradicted it. That looks closer to OpenAI's failure mode ("The model can also get the right context and do the wrong thing with it.") than to a bot with no access to the docs, though the record can't confirm either. RAG with citations does not by itself stop this.
3. **The legal lesson is about liability, not architecture.** The tribunal ruled on negligent misrepresentation: the company is responsible for every answer on its site, whatever produces it.

**Safe framing:** "Air Canada's chatbot gave a grieving customer the wrong refund rule. A tribunal made Air Canada pay: what your bot says, you said. If you build a bot on your own docs, here's how to make it answer from them (RAG), and why even that isn't a guarantee." Mata is the cleaner "AI made it up, confidently" intensifier.

## Story options

1. **Air Canada cold open → liability line → RAG explainer → "even RAG can grab the wrong chunk."** Strongest legal hook, honest if the bot's tech is never named.
2. **Mata cold open:** “Is Varghese a real case” (no question mark in the opinion) → ChatGPT says real → $5,000 penalty. The cleanest "the model answers from memory" setup for introducing RAG as the open-book fix.
3. **Open-book exam metaphor** (OpenAI's "textbook" line) as the visual spine: chunks = index cards, search = finding the right card, model = writing the answer from the card.
4. **Close on the 5.7% → 1.9% chart:** even Anthropic's best setup misses some, so show the source and keep a human check on high-stakes answers.
