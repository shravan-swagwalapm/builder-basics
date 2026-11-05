import json,glob,os,sys
base=json.load(open(sys.argv[1]))
new=[];meta={}
for f in sorted(glob.glob('ch/*.json')):
    try: d=json.load(open(f))
    except Exception: continue
    if not d: continue
    ch=d.get('channel'); meta[ch]={'handle':'@'+os.path.basename(f)[:-5],'subs':d.get('channel_follower_count'),'n':len(d.get('entries') or [])}
    for e in d.get('entries') or []:
        if e.get('view_count') is None: continue
        new.append({'channel':ch,'title':e.get('title'),'views':e['view_count'],'url':'https://www.youtube.com/shorts/'+e['id'],'duration':e.get('duration'),'source':'2026-11-05 backlog pull'})
for x in base: x.setdefault('source','2026-11-05 niche-swipe pull')
json.dump(base+new,open('collected_merged.json','w'),ensure_ascii=False,indent=0)
json.dump(meta,open('new_channel_meta.json','w'),indent=1)
print(len(base),len(new),len(base+new))
