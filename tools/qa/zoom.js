// node tools/qa/zoom.js out.png <outfit id | JSON list of pieces> "rotY,camY,camZ,lookY;..." [bg hex] : close-up renders of one outfit
// QA_BODY=slim|average|athletic|heavier|close|loose renders on another of Edit Dave's body types or cloth fits (tools/qa/body.js)
// node zoom.js out.png fitId "rotY,camY,camZ,lookY;rotY,..." [bg hex]
const {chromium}=require('playwright');
(async()=>{const out=process.argv[2],id=process.argv[3],views=process.argv[4].split(';').map(v=>v.split(',').map(Number)),bg=process.argv[5]||'3355ff';
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1000,height:800}});if(process.env.QA_BODY){const ch=require('./body').charFor(require('fs').readFileSync(require('path').join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const urls=await p.evaluate(async(a)=>{await window.__dw.loadThree();const T=window.THREE,W=460,H=460;const f=a.id.startsWith("[")?{pieces:JSON.parse(a.id)}:window.__dw.fitById[a.id];
 const rd=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});rd.setSize(W,H);rd.setClearColor(parseInt(a.bg,16));if(T.sRGBEncoding)rd.outputEncoding=T.sRGBEncoding;rd.toneMapping=T.ACESFilmicToneMapping;
 const ps0=f.pieces.length&&!f.id?f.pieces:window.__dw.effPieces(f);await new Promise(r=>{window.__dw.trueFor(ps0,r);setTimeout(r,4000);});const o=window.__dw.make3D(ps0);o.scene.background=null;const out=[];
 for(const v of a.views){const cam=new T.PerspectiveCamera(24,W/H,0.05,50);cam.position.set(0,v[1],v[2]);cam.lookAt(0,v[3],0);o.man.rotation.y=v[0];rd.render(o.scene,cam);out.push(rd.domElement.toDataURL('image/png'));}
 return out;},{id,views,bg});
const q=await b.newPage({viewport:{width:470*urls.length,height:470}});await q.setContent('<body style="margin:0;display:flex;gap:4px">'+urls.map(u=>'<img src="'+u+'">').join('')+'</body>');await q.screenshot({path:out});console.log('errors',errs.slice(0,3));await b.close();})();
