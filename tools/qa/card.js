// node tools/qa/card.js out.png id1,id2,... : the 3D card pictures of outfits as the page draws them (snap3D: the light
// build, soft shadows, turned 0.32, 240 x 490 shown at 1.5x), each beside a 3x crop of the hips and thighs
// QA_BODY=slim|average|athletic|heavier|close|loose renders on another of Edit Dave's body types or cloth fits (tools/qa/body.js)
const {chromium}=require('playwright');
(async()=>{const out=process.argv[2],ids=process.argv[3].split(',');
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1000,height:800}});if(process.env.QA_BODY){const ch=require('./body').charFor(require('fs').readFileSync(require('path').join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}
const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const urls=await p.evaluate(async(a)=>{await window.__dw.loadThree();const T=window.THREE,out=[];
 const rd=new T.WebGLRenderer({antialias:true,alpha:true,preserveDrawingBuffer:true});rd.setPixelRatio(1);rd.setSize(360,735);if(T.sRGBEncoding)rd.outputEncoding=T.sRGBEncoding;
 rd.toneMapping=T.ACESFilmicToneMapping;rd.toneMappingExposure=1.08;rd.shadowMap.enabled=true;rd.shadowMap.type=T.PCFSoftShadowMap;
 for(const id of a.ids){const f=window.__dw.fitById[id];if(!f){out.push(null);continue;}const ps=window.__dw.effPieces(f);await new Promise(r=>{window.__dw.trueFor(ps,r);setTimeout(r,4000);});
  window.__dw.setLite(true);let o;try{o=window.__dw.make3D(ps);}finally{window.__dw.setLite(false);}
  const k=Math.max(1,o.k||1),cam=new T.PerspectiveCamera(13,240/490,0.1,50);cam.position.set(0,0.95*k,8.7*k);cam.lookAt(0,0.93*k,0);o.man.rotation.y=0.32;rd.render(o.scene,cam);
  out.push(rd.domElement.toDataURL('image/png'));}
 return out;},{ids});
const W=360,H=735;const q=await b.newPage({viewport:{width:(W+2*W)*ids.length,height:H}});
await q.setContent('<body style="margin:0;display:flex;background:#f3efe6">'+urls.map(u=>u?'<div style="display:flex"><img src="'+u+'" style="width:'+W+'px;height:'+H+'px"><div style="width:'+W*2+'px;height:'+H+'px;overflow:hidden;position:relative"><img src="'+u+'" style="position:absolute;width:'+W*3+'px;left:-'+W*0.5+'px;top:-'+H*1.3+'px"></div></div>':'<div>missing</div>').join('')+'</body>');
await q.waitForTimeout(300);await q.screenshot({path:out});console.log('errors',errs.slice(0,3));await b.close();})();
