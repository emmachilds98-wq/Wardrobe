// node tools/qa/ray.js <outfit id> "[[x,y],...]" : which meshes a ray from the front meets at each point, and how deep (find what pokes through what)
// QA_BODY=slim|average|athletic|heavier|close|loose renders on another of Edit Dave's body types or cloth fits (tools/qa/body.js)
// QA_WEAR=tuck=in,turn=up,zip=up renders it as the fitting room's "How it's worn" toggles set it; THREE_JS=<three.min.js> serves Three.js locally
const {chromium}=require('playwright');
const WEAR=Object.fromEntries((process.env.QA_WEAR||'').split(',').filter(Boolean).map(kv=>kv.split('=')));
(async()=>{const id=process.argv[2],pts=JSON.parse(process.argv[3]);
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage();if(process.env.QA_BODY){const ch=require('./body').charFor(require('fs').readFileSync(require('path').join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}if(process.env.THREE_JS)await p.route('**/three.js/r128/three.min.js',r=>r.fulfill({path:process.env.THREE_JS,contentType:'text/javascript'}));await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const r=await p.evaluate(async(a)=>{await window.__dw.loadThree();const T=window.THREE;const f=window.__dw.fitById[a.id];const ps0=window.__dw.effPieces(f);
 await new Promise(r=>{window.__dw.trueFor(ps0,r);setTimeout(r,4000);});if(a.wear)window.__dw.wear(a.wear);let o;try{o=window.__dw.make3D(ps0);}finally{window.__dw.wear(null);}o.man.rotation.y=0;o.scene.updateMatrixWorld(true);
 const rc=new T.Raycaster();const out=[];for(const q of a.pts){rc.set(new T.Vector3(q[0],q[1],2),new T.Vector3(0,0,-1));
  const h=rc.intersectObjects(o.scene.children,true).slice(0,5).map(x=>{const u=x.object.userData;return [x.point.z.toFixed(4),x.object.type,x.object.geometry.type,JSON.stringify({it:u.item||u.it,k:u.kind,w:u.what}).slice(0,90),x.object.material&&x.object.material.transparent?'T':'',x.object.material&&x.object.material.polygonOffset?'PO':''].join(' ');});out.push(q.join(',')+' -> '+h.join(' | '));}
 return out;},{id,pts,wear:WEAR});console.log(r.join('\n'));await b.close();})();
