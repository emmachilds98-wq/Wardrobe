// node multi.js out.png shape item1,item2,... [view]  : one close-up per item, with its shop photo under it
//   view: chest (default), legs (trousers, shorts, skirts), or feet (shoes and boots, turned to show the side as shop photos do)
// QA_BODY=slim|average|athletic|heavier|close|loose renders on another of Edit Dave's body types or cloth fits (tools/qa/body.js)
const {chromium}=require('playwright');
(async()=>{const out=process.argv[2],shape=process.argv[3],ids=process.argv[4].split(','),view=process.argv[5]||'chest';
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
const p=await b.newPage({viewport:{width:1000,height:800}});if(process.env.QA_BODY){const ch=require('./body').charFor(require('fs').readFileSync(require('path').join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(2500);
const urls=await p.evaluate(async(a)=>{await window.__dw.loadThree();const T=window.THREE,W=300,H=300;
 const rd=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});rd.setSize(W,H);rd.setClearColor(0xe8e2d6);if(T.sRGBEncoding)rd.outputEncoding=T.sRGBEncoding;rd.toneMapping=T.ACESFilmicToneMapping;const out=[];
 for(const id of a.ids){const ps0=[{item:id,shape:a.shape,col:'white',what:'x'},{item:'sw-tailored-grey',shape:'trousers',col:'grey',what:'t'}];
  await new Promise(r=>{window.__dw.trueFor(ps0,r);setTimeout(r,20000);});const o=window.__dw.make3D(ps0);o.scene.background=null;
  const V={chest:[0,1.3,1.5,1.25,0],legs:[0,0.75,3.2,0.62,0],feet:[0,0.3,1.05,0.07,-1.25]}[a.view]||[0,1.3,1.5,1.25,0];
  const cam=new T.PerspectiveCamera(24,1,0.05,50);cam.position.set(0,V[1],V[2]);cam.lookAt(0,V[3],0);o.man.rotation.y=V[4];o.scene.updateMatrixWorld(true);rd.render(o.scene,cam);
  const ph=(window.__dw.photoOf&&window.__dw.photoOf(id))||'';out.push([rd.domElement.toDataURL('image/png'),ph]);}
 return out;},{ids,shape,view});
const q=await b.newPage({viewport:{width:304*urls.length,height:640}});await q.setContent('<body style="margin:0;display:flex;gap:4px;background:#fff">'+urls.map(u=>'<div><img src="'+u[0]+'"><br><img src="'+u[1]+'" style="width:300px;height:330px;object-fit:contain"></div>').join('')+'</body>');await q.waitForTimeout(500);await q.screenshot({path:out});await b.close();})();
