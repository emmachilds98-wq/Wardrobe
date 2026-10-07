// node tools/qa/smoke.js : loads the Outfits view in 2D and 3D and reports cards, renders and any page errors
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for(const mode of ['2d','3d']){const ctx=await b.newContext({viewport:{width:1280,height:900}});
await ctx.addInitScript(m=>{try{localStorage.setItem('dw-fig',m);localStorage.setItem('dw-view','fits');}catch(e){}},mode);
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push('pageerror '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push('console '+m.text())});
await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/#fits',{waitUntil:'networkidle'});await p.waitForTimeout(mode==='3d'?20000:6000);
const n=await p.$$eval('#fit-grid .fit',x=>x.length).catch(()=>-1);const imgs=await p.$$eval('#fit-grid image[href^="data:image"]',x=>x.length).catch(()=>-1);
console.log(mode,JSON.stringify({cards:n,renders:imgs,errs:errs.slice(0,5)}));await ctx.close();}
await b.close();})();
