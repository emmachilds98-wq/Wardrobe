// node tools/qa/garments.js [shard/n] [zip] : each outfit fetches only the templates garmentsFor names (speed fix 1).
// Draws every outfit with all the templates loaded and again with only garmentsFor's, and reports any outfit whose
// meshes differ (a template make3D reads that garmentsFor does not name), and how often each template is named.
// zip: "up" or "open" to draw them done up or open. Serve a test copy first: sh tools/qa/serve.sh
const {chromium}=require('playwright');
(async()=>{const [k,n]=(process.argv[2]||'0/1').split('/').map(Number),zip=process.argv[3]||'';
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});const p=await b.newPage();
await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/');await p.waitForFunction(()=>window.__dw&&Object.keys(window.__dw.fitById||{}).length>0,null,{timeout:120000});
if(!await p.evaluate(()=>!!window.__dw.garmentsFor)){console.log('no garmentsFor in this build');await b.close();return;}
await p.evaluate(()=>window.__dw.loadThree());
const ids=(await p.evaluate(()=>Object.keys(window.__dw.fitById))).filter((_,i)=>i%n===k);let bad=0;const cnt={};
for(let i=0;i<ids.length;i++){const r=await p.evaluate(([id,zip])=>{const D=window.__dw,ps=D.effPieces(D.fitById[id]),G=D.GTPL,need=D.garmentsFor(ps);
  /* the meshes' piece, kind and point count, and two sums of their points */
  function fp(){const o=D.make3D(ps),out=[];o.scene.traverse(m=>{const a=m.isMesh&&m.geometry&&m.geometry.attributes.position;if(!a)return;let s=0,w=0;const A=a.array;
    for(let j=0;j<A.length;j++){s+=A[j];w+=A[j]*((j%7)+1);}const u=m.userData||{};out.push([u.item||'',u.kind||'',u.draped?1:0,A.length,s.toFixed(3),w.toFixed(3)].join('|'));});return out.sort().join('\n');}
  let all,sub;D.wear&&zip&&D.wear({zip:zip});
  try{all=fp();const S={};need.forEach(a=>{if(G[a])S[a]=G[a];});D.GTPL=S;sub=fp();}finally{D.GTPL=G;D.wear&&zip&&D.wear(null);}
  return {id,need,same:all===sub};},[ids[i],zip]);
  r.need.forEach(a=>cnt[a]=(cnt[a]||0)+1);if(!r.same){bad++;console.log('DIFF',r.id,r.need.join(','));}}
console.log(JSON.stringify({outfits:ids.length,differ:bad,named:cnt}));await b.close();})();
