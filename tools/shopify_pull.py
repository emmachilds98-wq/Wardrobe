import urllib.request,json,sys,concurrent.futures as cf,time,os
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
def pull(h):
  out=[]
  for page in range(1,13):
    try:
      r=urllib.request.Request(f"https://{h}/products.json?limit=250&page={page}",headers={"User-Agent":UA,"Accept":"application/json"})
      with urllib.request.urlopen(r,timeout=30) as f: ps=json.load(f).get("products",[])
    except Exception as e: break
    if not ps: break
    out+=ps; time.sleep(0.5)
  json.dump(out,open(f"cat/{h}.json","w"))
  return h,len(out)
hosts=sys.argv[1].split(",")
with cf.ThreadPoolExecutor(8) as ex:
  for h,n in ex.map(pull,hosts): print(h,n,flush=True)
