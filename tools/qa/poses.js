// node tools/qa/poses.js out.png <outfit ids, comma separated> [poses] ["rotY,camY,camZ,lookY;..."] : the live views' poses
// (POSES in page.html), one row per outfit and pose, and for each piece how many of its triangles a pose stretches to over
// 2.5 times their length (cloth tearing where its weights change: a seam, a layer bound apart from the one over it).
// poses: stand,ease,walk,arms (the default). Serve a test copy first (sh tools/qa/serve.sh); QA_BODY as zoom.js;
// QA_SIZE the width of each picture (300).
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const out=process.argv[2],ids=process.argv[3].split(','),poses=(process.argv[4]||'stand,ease,walk,arms').split(',').map(x=>x==='stand'?'':x);
const views=(process.argv[5]||"0.35,1.0,4.75,0.93;1.5708,1.0,4.75,0.93;2.8,1.0,4.75,0.93").split(';').map(v=>v.split(',').map(Number));
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1000,height:800}});
if(process.env.QA_BODY){const ch=require('./body').charFor(fs.readFileSync(path.join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const S=Number(process.env.QA_SIZE||300),H=Math.round(S*1.9/1.2),rows=[];
for(const id of ids){
 const res=await p.evaluate(async(a)=>{await window.__dw.loadThree();const T=window.THREE,P=window.__dw.pose;if(!P)return {err:'no poses in this build'};
  const f=window.__dw.fitById[a.id];if(!f)return {err:'no outfit '+a.id};const ps0=window.__dw.effPieces(f);await new Promise(r=>{window.__dw.trueFor(ps0,r);setTimeout(r,4000);});
  const rd=window.__rd||(window.__rd=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true}));rd.setSize(a.S,a.H);rd.setClearColor(0xd9dccf);rd.toneMapping=T.ACESFilmicToneMapping;rd.shadowMap.enabled=true;
  const o=window.__dw.make3D(ps0),R=P.rig(o.man);if(!R)return {err:'no rig (body.json without "rig")'};const rows=[];
  for(const k of a.poses){const t0=performance.now();P.apply(R,P.solve(R,k));const ms=Math.round(performance.now()-t0),bad={};
   R.recs.forEach(rc=>{if(!rc.P||!rc.o.visible)return;const g=rc.o.geometry,pa=g.attributes.position.array,I=g.index?g.index.array:null,nt=I?I.length/3:pa.length/9;let n=0;
    for(let t=0;t<nt;t++){let m0=0,m1=0;for(let e=0;e<3;e++){const u=I?I[t*3+e]:t*3+e,w=I?I[t*3+(e+1)%3]:t*3+(e+1)%3;
      m0=Math.max(m0,Math.hypot(rc.P[u*3]-rc.P[w*3],rc.P[u*3+1]-rc.P[w*3+1],rc.P[u*3+2]-rc.P[w*3+2]));m1=Math.max(m1,Math.hypot(pa[u*3]-pa[w*3],pa[u*3+1]-pa[w*3+1],pa[u*3+2]-pa[w*3+2]));}
     if(m1>2.5*m0+0.01)n++;}
    if(n){const w=rc.o.userData.what||rc.o.userData.kind||'mesh';bad[w]=(bad[w]||0)+n;}});
   const urls=[];for(const v of a.views){const cam=new T.PerspectiveCamera(24,a.S/a.H,0.05,50);cam.position.set(0,v[1],v[2]);cam.lookAt(0,v[3],0);o.man.rotation.y=v[0];rd.render(o.scene,cam);urls.push(rd.domElement.toDataURL('image/png'));}
   rows.push({id:a.id,pose:k||'stand',ms,bad,urls});}
  return {rows,rig:R.ms};},{id,poses,views,S,H});
 if(res.err){console.log(id,res.err);continue;}
 res.rows.forEach(r=>{console.log(r.id,r.pose,'rig '+res.rig+' ms, pose '+r.ms+' ms, stretched:',JSON.stringify(r.bad));rows.push(r);});}
const q=await b.newPage({viewport:{width:(S+4)*views.length+130,height:(H+4)*Math.max(1,rows.length)}});
await q.setContent('<body style="margin:0;font:12px sans-serif">'+rows.map(r=>'<div style="display:flex;gap:4px;align-items:center;margin-bottom:4px"><div style="width:126px">'+r.id+'<br>'+r.pose+'</div>'+r.urls.map(u=>'<img src="'+u+'">').join('')+'</div>').join('')+'</body>');
await q.screenshot({path:out,fullPage:true});console.log('errors',errs.slice(0,5));await b.close();})();
