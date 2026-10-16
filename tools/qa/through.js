// node tools/qa/through.js <outfit id> [more ids] : how much of the layers under the outermost draped top shows through it.
// Renders each outfit with every item in its own flat colour from 8 directions round him (torso framed) and counts the
// pixels of the small blobs (under 4000 px) of any other colour lying wholly inside the outermost top's colour: a
// layer coming through it in patches. What shows between an open front's edges, at its hem or its cuffs touches the
// background or other colours and is not counted. The 3D check (check_3d.js) does not count a poke under an open
// front, so this is the measure for layers under an open jacket (UPGRADE_PLAN, open-over-open layering).
// A drawn detail (buttons, a zip, a placket) is counted apart as "<item>#detail".
// Prints, per outfit: the pixels, the blobs, the pixels by view (front first, turning 45 degrees each) and by item.
// Single outfits are noisy (a small change moves the crumples); compare totals over several outfits and the five bodies.
// QA_PORT, QA_BODY, QA_WEAR and QA_INIT as zoom.js. THROUGH_SAVE=<png> saves the first outfit's front and 45-degree
// views with the counted blobs in red. Controls with one open layer over a closed one count 0 to 80 on dave.
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');
const WEAR=Object.fromEntries((process.env.QA_WEAR||'').split(',').filter(Boolean).map(kv=>kv.split('=')));
(async()=>{const ids=process.argv.slice(2);if(!ids.length){console.log('usage: node tools/qa/through.js <outfit id> [more ids]');process.exit(1);}
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for(const id of ids){const p=await b.newPage();if(process.env.QA_INIT)await p.addInitScript(process.env.QA_INIT);
 if(process.env.QA_BODY){const ch=require('./body').charFor(fs.readFileSync(path.join(__dirname,'../../docs/index.html'),'utf8'),process.env.QA_BODY);if(ch)await p.addInitScript(c=>localStorage.setItem('dw-char',JSON.stringify(c)),ch);}
 await p.goto('http://localhost:'+(process.env.QA_PORT||8770)+'/',{waitUntil:'networkidle'});await p.waitForTimeout(1500);
 const out=await p.evaluate(async(a)=>{const D=window.__dw;await D.loadThree();const T=window.THREE;const f=D.fitById[a.id];if(!f)return null;const ps=D.effPieces(f);await new Promise(r=>{D.trueFor(ps,r);setTimeout(r,4000);});
  if(a.wear)D.wear(a.wear);let o;try{o=D.make3D(ps);}finally{D.wear(null);}const man=o.man;
  // the outermost draped top: the highest "upN" among the draped garments
  let top=null,tk=-1;man.traverse(m=>{if(m.isMesh&&m.userData.draped&&m.userData.sleeveMask&&/^up/.test(m.userData.kind||'')){const k=+m.userData.kind.slice(2);if(k>tk){tk=k;top=m.userData.item;}}});
  if(top==null)return {top:null,res:[],tal:{}};
  const ids={},col=c=>[(c*37)%256,(c*91)%256,(c*53)%256];let nid=1;
  man.traverse(m=>{if(!m.isMesh)return;let it=m.userData.item||(m.userData.isBody?'body':'other');if(it!==top&&m.userData.item&&!m.userData.sleeveMask)it+='#detail';if(!(it in ids))ids[it]=nid++;const c=col(ids[it]);
    const mat=new T.MeshBasicMaterial({color:new T.Color(c[0]/255,c[1]/255,c[2]/255),side:T.DoubleSide});m.material=Array.isArray(m.material)?m.material.map(()=>mat):mat;});
  const byKey={};Object.keys(ids).forEach(k=>{const c=col(ids[k]);byKey[(c[0]<<16)|(c[1]<<8)|c[2]]=k;});
  const W=600,H=720,rd=new T.WebGLRenderer({antialias:false,preserveDrawingBuffer:true});rd.setSize(W,H);rd.setClearColor(0xffffff);o.scene.background=null;rd.toneMapping=T.NoToneMapping;if(T.LinearEncoding)rd.outputEncoding=T.LinearEncoding;
  const tc=col(ids[top]),tal={},res=[];
  for(let v=0;v<8;v++){const cam=new T.PerspectiveCamera(24,W/H,0.05,50);cam.position.set(0,1.3,2.6);cam.lookAt(0,1.2,0);man.rotation.y=v*Math.PI/4;rd.render(o.scene,cam);
    const gl=rd.getContext(),px=new Uint8Array(W*H*4);gl.readPixels(0,0,W,H,gl.RGBA,gl.UNSIGNED_BYTE,px);
    const isTop=new Uint8Array(W*H);for(let i=0;i<W*H;i++)isTop[i]=Math.abs(px[i*4]-tc[0])<3&&Math.abs(px[i*4+1]-tc[1])<3&&Math.abs(px[i*4+2]-tc[2])<3?1:0;
    const lab=new Int32Array(W*H).fill(-1),hit=new Set();let n0=0,nb=0;
    for(let s=0;s<W*H;s++){if(isTop[s]||lab[s]>=0)continue;const st=[s];lab[s]=s;let n=0,inside=true;
      while(st.length){const q=st.pop();n++;const x=q%W,y=(q/W)|0;if(x===0||y===0||x===W-1||y===H-1)inside=false;
        for(const d of [1,-1,W,-W]){const r=q+d;if(r<0||r>=W*H||(d===1&&x===W-1)||(d===-1&&x===0)||isTop[r]||lab[r]>=0)continue;lab[r]=s;st.push(r);}}
      if(inside&&n<4000){n0+=n;nb++;hit.add(s);const k=byKey[(px[s*4]<<16)|(px[s*4+1]<<8)|px[s*4+2]]||'?';tal[k]=(tal[k]||0)+n;}}
    let img=null;if(a.save&&v<2){const cv=document.createElement('canvas');cv.width=W;cv.height=H;const cx=cv.getContext('2d'),im=cx.createImageData(W,H);
      for(let y=0;y<H;y++)for(let x=0;x<W;x++){const si=(H-1-y)*W+x,di=(y*W+x)*4,red=hit.has(lab[si]);im.data[di]=red?255:px[si*4];im.data[di+1]=red?0:px[si*4+1];im.data[di+2]=red?0:px[si*4+2];im.data[di+3]=255;}
      cx.putImageData(im,0,0);img=cv.toDataURL();}
    res.push([n0,nb,img]);}
  return {top,res,tal};},{id,wear:WEAR,save:!!process.env.THROUGH_SAVE&&id===ids[0]});
 await p.close();
 if(!out){console.log(id.padEnd(22),'no such outfit');continue;}
 if(!out.top){console.log(id.padEnd(22),'no draped top');continue;}
 const tot=out.res.reduce((s,r)=>s+r[0],0),bl=out.res.reduce((s,r)=>s+r[1],0);
 console.log(id.padEnd(22),'through px',String(tot).padStart(6),'blobs',String(bl).padStart(4),' by view',out.res.map(r=>r[0]).join(','),' |',Object.entries(out.tal).map(([k,v])=>k+':'+v).join(' '));
 if(process.env.THROUGH_SAVE&&id===ids[0]){const q=await b.newPage({viewport:{width:1204,height:720}});await q.setContent('<body style="margin:0;display:flex;gap:4px">'+out.res.slice(0,2).map(r=>'<img src="'+r[2]+'">').join('')+'</body>');await q.screenshot({path:process.env.THROUGH_SAVE});await q.close();}}
await b.close();})();
