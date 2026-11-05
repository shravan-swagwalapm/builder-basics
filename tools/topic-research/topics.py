"""Match candidate topics against the merged Shorts set; multiples use swipe.py's method
(views / channel median, channels with >=4 videos only)."""
import json, re, statistics, sys

rows = json.load(open(sys.argv[1]))
by = {}
for r in rows:
    by.setdefault(r['channel'], []).append(r)
med = {c: statistics.median([v['views'] or 0 for v in vs]) for c, vs in by.items() if len(vs) >= 4}
for r in rows:
    m = med.get(r['channel'])
    r['channel_median'] = m
    r['multiple'] = round(r['views'] / m, 2) if m else None

TOPICS = {
    'rag': r'\brag\b|retrieval',
    'prompt_injection': r'prompt injection|injection',
    'mcp': r'\bmcp\b|model context protocol|utcp',
    'agent_vs_workflow': r'agentic ai|ai agents? (vs|explained|work)|agents? explained|gen ?ai .*agents?|workflow',
    'evals': r'\bevals?\b|evaluat|llm.as.a.judge',
    'embeddings_vectordb': r'embedding|vector',
    'hallucination': r'halluc|as source|accurate ai|99\.5',
    'finetune_vs_rag': r'fine.?tun',
    'tool_calling': r'tool.?call|function.?call',
    'api': r'\bapis?\b',
    'webhook': r'webhook',
    'prompt_caching_cost': r'cach|cheaper|save tokens|cost',
    'tokens_context': r'token|context window|context engineering',
    'system_prompt': r'system prompt',
    'localhost_deploy': r'localhost|deploy|production|ships? code',
    'frontend_backend_db': r'backend|frontend|database|postgres|redis|\bdb\b',
    'secrets_security': r'api keys?|\.?env\b|hack|secret|leak|stealing',
    'model_choice': r'opus|sonnet| vs claude|when to use|chatgpt, |which (ai|model)|gemini, and',
    'n8n_vs_code': r'n8n',
    'vibe_spec': r'vibe cod|spec.driven|\bspec\b|prd',
    'guardrails_hitl': r'guardrail|human.in.the.loop|approval',
    'memory': r'memory|forget',
    'skills_subagents': r'\bskills?\b|subagent|sub-agent',
    'knowledge_graph': r'knowledge graph',
}
out = {}
for t, p in TOPICS.items():
    rx = re.compile(p, re.I)
    hits = [r for r in rows if r['title'] and rx.search(r['title']) and r['multiple'] is not None]
    hits.sort(key=lambda r: -r['multiple'])
    out[t] = hits
    ms = [h['multiple'] for h in hits]
    print(f"\n### {t}: n={len(hits)} max={max(ms) if ms else '-'} median={statistics.median(ms) if ms else '-'}")
    for h in hits[:7]:
        print(f"   {h['multiple']:6.2f}x {h['views']:>9} vs {int(h['channel_median']):>8}  {h['channel'][:18]:18} | {h['title'][:80]}")
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
json.dump({t: [{k: h[k] for k in ('channel', 'title', 'views', 'channel_median', 'multiple', 'url')} for h in hs]
           for t, hs in out.items()}, open(sys.argv[3], 'w'), ensure_ascii=False, indent=1)
