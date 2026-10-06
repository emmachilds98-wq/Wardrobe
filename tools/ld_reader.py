"""Read schema.org Product / ProductGroup JSON-LD from product pages: name, price, image, stock per size."""
import json,re,sys,urllib.request,ssl,html,concurrent.futures as cf
ctx=ssl.create_default_context()
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def get(u):
  r=urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":UA,"Accept-Language":"en-GB"}),timeout=40,context=ctx)
  return r.read().decode('utf8','replace'),r.geturl()
def walk(o,out):
  if isinstance(o,list):
    for x in o: walk(x,out)
  elif isinstance(o,dict):
    t=o.get('@type');t=t if isinstance(t,list) else [t]
    if 'Product' in t or 'ProductGroup' in t: out.append(o)
    for k in ('@graph','hasVariant','mainEntity'):
      if k in o: walk(o[k],out)
def parse(u):
  try: s,final=get(u)
  except Exception as e: return {'url':u,'err':str(e)[:80]}
  prods=[]
  for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>',s,re.S):
    try: walk(json.loads(html.unescape(m.group(1).strip())),prods)
    except Exception: pass
  if not prods: return {'url':u,'err':'no ld'}
  top=prods[0];name=top.get('name','');img=top.get('image')
  sizes={};price=None
  for p in prods:
    offs=p.get('offers') or []
    offs=offs if isinstance(offs,list) else [offs]
    for o in offs:
      if o.get('@type')=='AggregateOffer':
        price=price or float(o.get('lowPrice') or 0); offs2=o.get('offers') or []
      else: offs2=[o]
      for x in offs2:
        pr=x.get('price')
        try: pr=float(pr)
        except Exception: pr=None
        if pr and (price is None or pr<price): price=pr
        sz=p.get('size') or x.get('size') or (x.get('itemOffered') or {}).get('size') if isinstance(x.get('itemOffered'),dict) else p.get('size') or x.get('size')
        if not sz:
          m2=re.search(r'(?:-|\s)(XXS|XS|S|M|L|XL|XXL|3XL|\d{2}(?:[RSL]|W)?|\d{1,2}(?:\.5)?)\s*$',str(x.get('sku') or p.get('name') or ''))
          sz=m2.group(1) if m2 else None
        if sz: sizes[str(sz)]=sizes.get(str(sz),False) or ('InStock' in str(x.get('availability')) or 'LimitedAvailability' in str(x.get('availability')))
    if not img: img=p.get('image')
  if not sizes:
    for m in re.finditer(r'class="availability">(\w+)</span>\s*<span class="custom_fields">\s*<span class="size">([^<]+)</span>',s):
      sizes[m.group(2).strip()]=sizes.get(m.group(2).strip(),False) or m.group(1)=='InStock'
  if isinstance(img,list): img=img[0] if img else None
  if isinstance(img,dict): img=img.get('url') or img.get('contentUrl')
  og=re.findall(r'property="og:image"\s+content="([^"]+)"',s)
  was=None
  m3=re.search(r'strike-through[^>]*>\s*<span class="value" content="([\d.]+)"',s) or re.search(r'"inStock":true,"price":"([\d.]+)","value":"[\d.]+"',s)
  if m3:
    try: was=float(m3.group(1))
    except Exception: pass
  if was and price and was<=price: was=None
  return {'was':was,'url':final,'name':name,'price':price,'img':img or (og[0] if og else None),'og':og[0] if og else None,'sizes':sizes,'color':top.get('color')}
if __name__=='__main__':
  urls=[l.strip() for l in open(sys.argv[1]) if l.strip()]
  with cf.ThreadPoolExecutor(6) as ex: res=list(ex.map(parse,urls))
  json.dump(res,open(sys.argv[2],'w'),indent=1)
  for r in res: print(r.get('price'),r.get('name','')[:60],'|',' '.join(k+('+' if v else '-') for k,v in list(r.get('sizes',{}).items())[:10]),r.get('err',''))
