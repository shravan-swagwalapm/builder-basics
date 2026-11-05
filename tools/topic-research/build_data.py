import os
import json, glob

S = lambda f: json.load(open(f))
rows = S('rows_with_multiples.json')
comments = {}
for f in sorted(glob.glob('comments/*.info.json')):
    d = S(f)
    comments[d['id']] = {'title': d['title'], 'views_at_fetch': d.get('view_count'), 'upload_date': d.get('upload_date'),
                         'comments': [{'author': c.get('author'), 'is_reply': c.get('parent') != 'root', 'text': c.get('text')}
                                      for c in d.get('comments') or []]}

# A = best on-concept competitor Short multiple (>=8x 3, >=3x 2, >=1.5x 1, else 0)
# B = autocomplete (3 broad-prefix top-10 hit, 2 seed returns on-concept explainer/Hindi/PM variants, 1 weak, 0 none)
# C = his own Shorts vs 2.1k median (same concept: >=4x 3, >=2.5x 2, >=1.5x 1; adjacent concept: one tier lower)
scores = [
    ('api-key-leak', 3, 2, 3, 'adjacent-covered'), ('rag', 3, 3, 1, 'draft-in-scratchpad'),
    ('localhost-vs-production', 2, 2, 2, 'new'), ('agent-vs-workflow-vs-chatbot', 3, 3, 0, 'covered-remake'),
    ('prompt-caching', 2, 2, 2, 'new'), ('mcp-vs-api', 2, 2, 2, 'covered-new-angle'),
    ('webhook-vs-api', 2, 2, 1, 'new'), ('model-routing', 3, 2, 0, 'covered-remake'),
    ('frontend-backend-database', 1, 2, 1, 'new'), ('hallucination', 2, 2, 0, 'new'),
    ('context-vs-prompt-engineering', 0, 2, 2, 'new'), ('evals', 1, 2, 0, 'new'),
    ('rag-vs-finetune-vs-prompt', 0, 2, 1, 'new'), ('embeddings-vector-db', 0, 2, 1, 'new'),
    ('tool-calling-agent-loop', 0, 2, 1, 'adjacent-covered'),
]
out = {
    'generated': '2026-11-05',
    'method': {
        'multiple': 'views / channel median over the collected Shorts (yt-viral swipe.py method); channels with <4 Shorts skipped',
        'own_median_note': 'His median is 2,100 over all 352 Shorts (own_shorts.json); 1,800 over the 50 in this swipe set',
        'evidence_score': 'A outlier 0-3 + B autocomplete 0-3 + C own data 0-3 = 0-9; comments not scored (no questions found)',
    },
    'sources': {'existing_swipe_rows': 878, 'new_rows': len(rows) - 878, 'total_rows': len(rows)},
    'new_channels': S('new_channel_meta.json'),
    'scores': [{'topic': t, 'A_outlier': a, 'B_search': b, 'C_own': c, 'total': a + b + c, 'coverage': cov}
               for t, a, b, c, cov in scores],
    'topic_matches': S('topic_matches.json'),
    'autocomplete': {'seeds': S('suggest_seeds.json'), 'targeted': S('suggest_seeds3.json'), 'broad_prefix': S('suggest_alpha.json')},
    'own_top5_comments': comments,
    'rows': rows,
}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'research', 'topic-data.json'), 'w'), ensure_ascii=False, indent=1)
print('rows', len(rows), 'topics', len(scores))
