// node tools/qa/dump.js out.json : every outfit piece's photo reading (colour, pattern, photo front, cloth square),
// read by the page being served. Run it on the old and the new build and compare, to see what a sampler change moved.
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const out=process.argv[2],port=process.env.QA_PORT||8770;
const o=JSON.parse(fs.readFileSync(path.join(__dirname,'../../docs/data/outfits.json')));const seen={},pairs=[];
for(const f of Object.values(o))for(const p of f.pieces||[])if(p.item&&!seen[p.item+'|'+p.shape]){seen[p.item+'|'+p.shape]=1;pairs.push([p.item,p.shape,p.col||'',p.what||'']);}
const b=await chromium.launch();const p=await b.newPage();await p.goto('http://localhost:'+port+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const r=await p.evaluate(async(pairs)=>{const res={};for(let i=0;i<pairs.length;i+=40){const ps=pairs.slice(i,i+40).map(a=>({item:a[0],shape:a[1],col:a[2],what:a[3]}));
  await new Promise(r=>{window.__dw.trueFor(ps,r);setTimeout(r,20000);});
  for(const q of ps){const L=window.__dw.LOOK[q.item]||q.look||{};res[q.item+'|'+q.shape]={c1:L.c1,c2:L.c2,pat:L.pat,front:!!L.front,sw:!!L.swatch,named:L.named||''};}}
 return res;},pairs);fs.writeFileSync(out,JSON.stringify(r));console.log(Object.keys(r).length+' pieces read');await b.close();})();
