// Prueba opcional de navegador; requiere Chrome y Node con WebSocket global.
const {spawn}=require('node:child_process'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const surfaces=require('../library/algebraic_surfaces/lobed.js');
for(let kind=0;kind<2;kind++){
 const family=surfaces.families[kind];let residual=0;
 for(const a of [0,family.initial,family.max]){
  const model=surfaces.model(kind,a);
  for(const p of model.vertices){
   residual=Math.max(residual,Math.abs(surfaces.field(kind,p,a)));
   if(!p.every(Number.isFinite)||Math.hypot(...p)>model.bound+1e-10)throw Error('Punto inválido');
  }
  for(const face of model.faces){
   const [p,q,r]=face.map(i=>model.vertices[i]),u=q.map((v,i)=>v-p[i]),v=r.map((x,i)=>x-p[i]);
   const area=Math.hypot(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]);
   if(area<1e-12)throw Error('Cara degenerada');
  }
 }
 if(residual>1e-10)throw Error('F != 0');
 const axis=Math.hypot(...surfaces.point(kind,0,0,family.initial));
 const diagonal=Math.hypot(...surfaces.point(kind,Math.PI/4,Math.asin(1/Math.sqrt(3)),family.initial));
 const ratio=kind===0?axis/diagonal:diagonal/axis;if(ratio<1.7)throw Error('Lóbulos poco diferenciados');
 console.log(family.id,'F=0',residual,'relieve radial',ratio);
}
if(process.argv.includes('--math-only'))process.exit(0);

(async()=>{
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'surface-browser-'));
const child=spawn(process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--use-angle=swiftshader','--enable-unsafe-swiftshader','--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});
let ws;try{
let port;for(let i=0;i<100;i++){try{port=fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').split('\n')[0];break;}catch{}await new Promise(r=>setTimeout(r,100));}if(!port)throw Error('Chrome no inició');
const targets=await(await fetch('http://127.0.0.1:'+port+'/json')).json();ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0,pending=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(pending.has(m.id)){const {resolve,reject}=pending.get(m.id);pending.delete(m.id);m.error?reject(Error(JSON.stringify(m.error))):resolve(m.result);}};
const send=(method,params={})=>new Promise((resolve,reject)=>{let n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1400,height:950,deviceScaleFactor:1,mobile:false});
await send('Page.navigate',{url:require('node:url').pathToFileURL(path.resolve(__dirname,'../experiments/019-cuarticas-vivas/index.html')).href});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result;};
for(let i=0;i<100;i++){let r=await evaluate('window.xyzStageState');if(r.value)break;await new Promise(r=>setTimeout(r,100));}
let initial=await evaluate('window.xyzStageState');if(initial.value?.error!==0||!initial.value.depth)throw Error(JSON.stringify(initial));
for (const id of ['seis-lobulos','ocho-lobulos']) {
 await evaluate(`document.querySelector('#choices select').value='${id}';document.querySelector('#choices select').onchange();`);
 await new Promise(r=>setTimeout(r,100));
 const result=await evaluate('window.xyzStageState');
 if(result.value.error!==0||result.value.assignments[0]!==id)throw Error(JSON.stringify(result));
 const before=await evaluate('canvas.toDataURL()');
 await evaluate("document.getElementById('deform').value='0';document.getElementById('deform').oninput();");
 await new Promise(r=>setTimeout(r,150));
 const round=await evaluate('canvas.toDataURL()');if(before.value===round.value)throw Error('Deformación no cambia vista');
 const state=await evaluate('window.lobedViewerState');if(state.value.a!==0||state.value.id!==id)throw Error(JSON.stringify(state));
 await evaluate("document.getElementById('deform').value=LobedSurfaces.families[selectedFamily()].initial;document.getElementById('deform').oninput();");
 await new Promise(r=>setTimeout(r,150));
 const restored=await evaluate('canvas.toDataURL()');if(restored.value!==before.value)throw Error('Deformación no es reproducible');
 await evaluate('yaw+=.9;pitch+=.4;');await new Promise(r=>setTimeout(r,150));
 const rotated=await evaluate('canvas.toDataURL()');if(restored.value===rotated.value)throw Error('Cámara no cambia vista');
 await evaluate('yaw=.5;pitch=.3;');await new Promise(r=>setTimeout(r,100));
 const shot=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.resolve(__dirname,'../recordings/019-'+id+'.png'),Buffer.from(shot.data,'base64'));
 const res=await evaluate('window.xyzStageState');if(res.value.error!==0)throw Error(JSON.stringify(res));
 console.log(id,'WebGL / deformación / cámara / restauración OK');
}
await evaluate("document.getElementById('faces').checked=false;document.getElementById('trace').checked=true;");
await new Promise(r=>setTimeout(r,100));
const trace=await evaluate('window.xyzStageState');if(trace.value.error!==0)throw Error(JSON.stringify(trace));
}finally{if(ws)ws.close();child.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
