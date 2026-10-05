#!/usr/bin/env python3
"""Fetch ASOS listing photos for picks that have none.

ASOS refuses connections from cloud servers, including its image server. The
public image-resizing service wsrv.nl can still fetch ASOS photos. The photo
address needs the product number (from the /prd/ link) and a colour code,
such as 205189664-1-white. This script guesses the colour from the link and the
pick's name, then tries common colours, and saves each hit to asosraw/<id>.jpg.
Check the photos by eye, then shrink and pack them with fetch_photos.shrink.

Reads missing.json: [[itemId, kind, host, url], ...]. Needs export/items/<id>.json
for the names. Run from the folder that holds both.
"""
ctx=ssl.create_default_context()
m=json.load(open('missing.json'))
a=[x for x in m if 'asos' in x[2]]
COMMON="black white navy grey stone brown khaki green blue cream ecru beige charcoal tan olive multi darkgrey lightgrey greymarl midblue lightblue darkblue washedblack burgundy sand camel chocolate darknavy offwhite silver gold red orange pink lilac purple yellow".split()
def cands(k,url,name):
    c=[]
    s=re.search(r'-in-([a-z-]+)/prd/',url)
    if s: c.append(s.group(1).replace('-',''))
    col=name.split(',')[-1].strip().lower() if ',' in name else ''
    if col:
        c.append(re.sub(r'[^a-z]','',col))
        for w in re.findall(r'[a-z]+',col): c.append(w)
    for w in COMMON:
        if w not in c: c.append(w)
    out=[];[out.append(x) for x in c if x and x not in out]
    return out
def fetch(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=30,context=ctx)
        return r.read() if r.status==200 and r.headers.get_content_type().startswith('image') else None
    except Exception: return None
def one(x):
    k,_,_,url=x
    if os.path.exists('asosraw/%s.jpg'%k): return k,'cached'
    pid=re.search(r'/prd/(\d+)',url)
    if not pid: return k,'no id'
    name=json.load(open('export/items/%s.json'%k))['name']
    for c in cands(k,url,name):
        b=fetch("https://wsrv.nl/?url=images.asos-media.com/products/p/%s-1-%s&w=600"%(pid.group(1),c))
        if b:
            open('asosraw/%s.jpg'%k,'wb').write(b); return k,c
    return k,None
res={}
with cf.ThreadPoolExecutor(6) as ex:
    for k,c in ex.map(one,a): res[k]=c; print(k,c,flush=True)
json.dump(res,open('asos_res.json','w'),indent=0)
print(sum(1 for v in res.values() if v), 'of', len(res))
