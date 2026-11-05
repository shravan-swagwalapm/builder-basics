import json, time, urllib.request, urllib.parse, sys

seeds = [l.strip() for l in open(sys.argv[1]) if l.strip()]
out = {}
for s in seeds:
    u = ('https://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=en&gl=IN&q='
         + urllib.parse.quote(s))
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=10)
        raw = r.read()
        try:
            txt = raw.decode('utf-8')
        except UnicodeDecodeError:
            txt = raw.decode('latin-1')
        out[s] = json.loads(txt)[1]
    except Exception as e:
        out[s] = {'error': str(e)}
    time.sleep(1)
json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print(len(out), sum(1 for v in out.values() if isinstance(v, dict)), 'errors')
