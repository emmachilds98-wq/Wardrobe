// node tools/qa/drape_survey.js [shape regex] : every outfit piece of those shapes (default all tops), the draped
// template it gets (drapeArch, null = make3Dcore's shapes) and the outfits it is in. Serve a test copy first
// (sh tools/qa/serve.sh); QA_PORT as the other scripts. The work list for the next template: the null rows.
const {chromium}=require('playwright');
const re=process.argv[2]||'^(tee|polo|shirt|sshirt|vest|jumper|hoodie|halfzip|rollneck|cardigan|jacket|coat|blazer|gilet|waistcoat)$';
(async()=>{const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});const p=await b.newPage();
await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const out=await p.evaluate(async(re)=>{const D=window.__dw;await D.loadThree();await new Promise(r=>setTimeout(r,4000));const R=new RegExp(re),o={};
 Object.values(D.fitById).forEach(f=>D.effPieces(f).forEach(q=>{if(!R.test(q.shape))return;const it=D.byId[q.item]||{},n=((it.name||"")+" "+(q.what||"")).toLowerCase(),k=q.item;
  o[k]=o[k]||{name:it.name||k,shape:q.shape,arch:D.drapeArch(q),hood:!!D.hoodOn(q,n),fits:[]};o[k].fits.push(f.id);}));return o;},re);
const rows=Object.values(out).sort((a,c)=>(a.arch===null)-(c.arch===null)||a.shape.localeCompare(c.shape)||c.fits.length-a.fits.length);
for(const r of rows)console.log([r.arch||'-',r.shape,r.fits.length,(r.hood?'hood ':'')+r.name,r.fits.slice(0,4).join(' ')].join('\t'));
await b.close();})();
