// Browser fallback for sitemap_sweep.py: shops that refuse plain requests (bot protection) are read in
// headless Chromium. For each host: open the home page (so its cookies and checks are passed), read the
// sitemaps through the same browser session, pick men's product pages, and read each page's schema.org
// Product data, price meta, photo and sizes. Writes <out>/<host>.ld.json (ld_reader.py's record shape);
// `python3 tools/sitemap_sweep.py --from-ld <out>` turns those into catalogue files for sweep_filter.py.
// Usage: node browser_sweep.js host1,host2,... outdir [pagesPerHost]   (needs the playwright package)
const {chromium}=require('playwright');const fs=require('fs');const zlib=require('zlib');
const hosts=process.argv[2].split(',').filter(Boolean),out=process.argv[3],N=Number(process.argv[4]||60);
fs.mkdirSync(out,{recursive:true});
const MEN=/(^|[\/_\-.])(men|mens|man|male|menswear|gents)([\/_\-.]|$)/i,WOMEN=/(women|womens|ladies|girls|boys|kids|baby|junior|child)/i;
const CLOTHES=/(shirt|tee|t-shirt|polo|jumper|sweat|hood|knit|cardigan|jacket|coat|parka|gilet|trouser|jean|chino|cord|short|jogger|boot|shoe|trainer|sneaker|loafer|slipper|sock|belt|cap|hat|beanie|scarf|blazer|suit|fleece|overshirt|swim)/i;
const NOTP=/\/(blog|stores?|help|pages?|about|journal|stories|c|category|categories|collections?|search)\//i;
function pick(urls){
  const sc=[];
  for(const u of urls){let path;try{path=new URL(u).pathname;}catch(e){continue;}
    if(NOTP.test(path)||WOMEN.test(path))continue;
    const prod=/\/(p|pd|product|products|prd|item|style)\/|\d{5,}|\.html?$|_[A-Z0-9]{6,}/.test(path);
    if(!prod&&path.includes('/l/'))continue;
    const s=(prod?3:0)+(MEN.test(path)?2:0)+(CLOTHES.test(path)?2:0)+(/sale|outlet|clearance|offer/i.test(u)?1:0);
    if(s>=3)sc.push([s,u]);}
  sc.sort((a,b)=>b[0]-a[0]||a[1].length-b[1].length);return sc.slice(0,N).map(x=>x[1]);
}
(async()=>{
 const b=await chromium.launch({args:['--disable-blink-features=AutomationControlled']});
 async function sweep(host){
  const ctx=await b.newContext({userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',locale:'en-GB',viewport:{width:1280,height:900}});
  const recs=[];
  try{
   const home=await ctx.newPage();
   try{await home.goto('https://'+host+'/',{waitUntil:'domcontentloaded',timeout:40000});await home.waitForTimeout(2500);}catch(e){}
   async function text(u){try{const r=await ctx.request.get(u,{timeout:40000});if(!r.ok())return '';let buf=await r.body();if(buf[0]===0x1f&&buf[1]===0x8b){buf=zlib.gunzipSync(buf);}return buf.toString('utf8');}catch(e){return '';}}
   let roots=((await text('https://'+host+'/robots.txt')).match(/^sitemap:\s*(\S+)/gim)||[]).map(l=>l.replace(/^sitemap:\s*/i,''));
   if(!roots.length)roots=['https://'+host+'/sitemap.xml','https://'+host+'/sitemap_index.xml'];
   const seen=new Set(),q=roots.slice(),pages=[];
   while(q.length&&seen.size<40){const sm=q.shift();if(seen.has(sm))continue;seen.add(sm);const body=await text(sm);if(!body)continue;
     const locs=[...body.matchAll(/<loc>\s*([^<\s]+)\s*<\/loc>/g)].map(m=>m[1].replace(/&amp;/g,'&'));
     if(body.includes('<sitemapindex')){q.push(...locs.filter(l=>!/image|blog|store|content|page|categor|brand|video/i.test(l)).sort((a,b2)=>(/product|pdp|item/i.test(b2)?1:0)-(/product|pdp|item/i.test(a)?1:0)));}
     else pages.push(...locs);}
   const urls=pick(pages);
   const queue=urls.slice();
   await Promise.all(Array.from({length:4},async()=>{
    const p=await ctx.newPage();
    while(queue.length){const u=queue.shift();
     try{await p.goto(u,{waitUntil:'domcontentloaded',timeout:35000});await p.waitForTimeout(1200);
      const r=await p.evaluate(()=>{
        const prods=[];function walk(o){if(Array.isArray(o)){o.forEach(walk);return;}if(o&&typeof o==='object'){const t=[].concat(o['@type']);if(t.includes('Product')||t.includes('ProductGroup'))prods.push(o);['@graph','hasVariant','mainEntity'].forEach(k=>{if(o[k])walk(o[k]);});}}
        document.querySelectorAll('script[type="application/ld+json"]').forEach(s=>{try{walk(JSON.parse(s.textContent));}catch(e){}});
        const meta=n=>{const e=document.querySelector('meta[property="'+n+'"],meta[name="'+n+'"],meta[itemprop="'+n+'"]');return e&&e.getAttribute('content');};
        let name=(prods[0]&&prods[0].name)||meta('og:title')||document.title,price=null,was=null,img=null,sizes={};
        for(const pr of prods){let offs=[].concat(pr.offers||[]);for(const o of offs){const list=o['@type']==='AggregateOffer'?[].concat(o.offers||[]):[o];if(o.lowPrice&&!price)price=Number(o.lowPrice);
          for(const x of list){const v=Number(x.price);if(v&&(!price||v<price))price=v;const sz=pr.size||x.size||(x.itemOffered&&x.itemOffered.size);if(sz){sizes[String(sz)]=(sizes[String(sz)]||false)||/InStock|LimitedAvailability/.test(String(x.availability));}}}
          if(!img){let im=pr.image;im=[].concat(im||[])[0];img=typeof im==='string'?im:(im&&(im.url||im.contentUrl));}}
        if(!price){const m=meta('product:price:amount')||meta('price');if(m)price=Number(m);}
        const wasEl=document.querySelector('[class*="was" i] , [class*="original-price" i], [class*="strike" i], s, del');
        if(wasEl){const m=/£\s*(\d+(?:\.\d+)?)/.exec(wasEl.textContent||'');if(m)was=Number(m[1]);}
        if(!Object.keys(sizes).length){document.querySelectorAll('[data-size],[aria-label*="size" i] button, select[name*="size" i] option, button[class*="size" i], li[class*="size" i]').forEach(e=>{const t=(e.getAttribute('data-size')||e.textContent||'').trim();if(t&&t.length<12){const off=e.disabled||/disabled|unavailable|out-of-stock|soldout|sold-out/i.test(e.className+' '+(e.getAttribute('aria-disabled')||''));sizes[t]=(sizes[t]||false)||!off;}});}
        return {name,price,was:(was&&price&&was>price*1.04&&was<price*6)?was:null,img:img||meta('og:image'),sizes,url:location.href,color:prods[0]&&prods[0].color};
      });
      if(r&&r.name&&r.price)recs.push(r);
     }catch(e){}}
    await p.close();}));
   console.log(host,urls.length,'pages',recs.length,'products');
  }catch(e){console.log(host,'failed',String(e.message).slice(0,60));}
  fs.writeFileSync(out+'/'+host+'.ld.json',JSON.stringify(recs));
  await ctx.close();
 }
 const q=hosts.slice();await Promise.all(Array.from({length:3},async()=>{while(q.length){await sweep(q.shift());}}));
 await b.close();
})();
