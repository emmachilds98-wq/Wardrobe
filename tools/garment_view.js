// node tools/garment_view.js in.json out.png ["rotY,camY,camZ,lookY;..."]: renders a debug file from tools/build_garments.py --debug
// (his body, the garment and any sewing lines) from each view, for looking at a drape without the page.
const {chromium}=(()=>{try{return require('playwright');}catch(e){return require('/opt/node22/lib/node_modules/playwright');}})();const fs=require('fs');
(async()=>{const data=fs.readFileSync(process.argv[2],'utf8'),out=process.argv[3],views=(process.argv[4]||"0,1.2,3.2,1.1;0.785,1.2,3.2,1.1;1.5708,1.2,3.2,1.1;3.14159,1.2,3.2,1.1").split(';').map(v=>v.split(',').map(Number));
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});const p=await b.newPage({viewport:{width:400*views.length,height:500}});
await p.setContent('<body style="margin:0"></body>');await p.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'});
const urls=await p.evaluate(({data,views})=>{const D=JSON.parse(data),T=window.THREE;function dec(s,A){const b=atob(s),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return new A(u.buffer);}
 const sc=new T.Scene();sc.add(new T.HemisphereLight(0xffffff,0x888877,0.7));const l=new T.DirectionalLight(0xffffff,0.8);l.position.set(-2,3,3);sc.add(l);const l2=new T.DirectionalLight(0xffffff,0.35);l2.position.set(2,1,-3);sc.add(l2);const g=new T.Group();sc.add(g);
 function mesh(m,col,op){const ge=new T.BufferGeometry();ge.setAttribute('position',new T.BufferAttribute(dec(m.pos,Float32Array),3));ge.setIndex(new T.BufferAttribute(dec(m.idx,Uint32Array),1));ge.computeVertexNormals();const me=new T.Mesh(ge,new T.MeshStandardMaterial({color:col,roughness:0.85,side:T.DoubleSide,transparent:op<1,opacity:op}));g.add(me);
   const w=new T.LineSegments(new T.WireframeGeometry(ge),new T.LineBasicMaterial({color:0x000000,transparent:true,opacity:0.08}));if(D.wire)g.add(w);}
 mesh(D.body,'#e2b08f',1);D.meshes.forEach(m=>mesh(m,m.col,1));
 if(D.lines){const L=dec(D.lines,Float32Array);if(L.length){const ge=new T.BufferGeometry();ge.setAttribute('position',new T.BufferAttribute(L,3));g.add(new T.LineSegments(ge,new T.LineBasicMaterial({color:0x00aa00})));}}
 const rd=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});rd.setSize(400,500);rd.setClearColor(0xeeeeee);const out=[];
 for(const v of views){const cam=new T.PerspectiveCamera(30,0.8,0.05,50);cam.position.set(0,v[1],v[2]);cam.lookAt(0,v[3],0);g.rotation.y=v[0];rd.render(sc,cam);out.push(rd.domElement.toDataURL());}return out;},{data,views});
const q=await b.newPage({viewport:{width:404*urls.length,height:500}});await q.setContent('<body style="margin:0;display:flex;gap:4px">'+urls.map(u=>'<img src="'+u+'">').join('')+'</body>');await q.screenshot({path:out});await b.close();})();
