// Prueba opcional de navegador; requiere Chrome y Node con WebSocket global.
const {spawn}=require('node:child_process'),fs=require('node:fs'),os=require('node:os'),path=require('node:path');
(async()=>{
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'surface-browser-'));
const child=spawn(process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--use-angle=swiftshader','--enable-unsafe-swiftshader','--user-data-dir='+profile,'about:blank'],{stdio:'ignore'});
let ws;try{
let port;for(let i=0;i<100;i++){try{port=fs.readFileSync(path.join(profile,'DevToolsActivePort'),'utf8').split('\n')[0];break;}catch{}await new Promise(r=>setTimeout(r,100));}if(!port)throw Error('Chrome no inició');
const targets=await(await fetch('http://127.0.0.1:'+port+'/json')).json();ws=new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);
let id=0,pending=new Map();ws.onmessage=e=>{const m=JSON.parse(e.data);if(pending.has(m.id)){const {resolve,reject}=pending.get(m.id);pending.delete(m.id);m.error?reject(Error(JSON.stringify(m.error))):resolve(m.result);}};
const send=(method,params={})=>new Promise((resolve,reject)=>{let n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
await send('Page.enable');await send('Emulation.setDeviceMetricsOverride',{width:1400,height:950,deviceScaleFactor:1,mobile:false});
await send('Page.navigate',{url:require('node:url').pathToFileURL(path.resolve(__dirname,'../experiments/016-superficies-diversas/index.html')).href});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result;};
for(let i=0;i<100;i++){let r=await evaluate('window.xyzStageState');if(r.value)break;await new Promise(r=>setTimeout(r,100));}
let initial=await evaluate('window.xyzStageState');if(initial.value?.error!==0||!initial.value.depth)throw Error(JSON.stringify(initial));
for(const mode of ['solo']){
 await evaluate(`document.getElementById('mode').value='${mode}';document.getElementById('mode').onchange();document.getElementById('focus').value='all';time=35;draw(performance.now());`);
 let result;for(let i=0;i<5;i++){await new Promise(r=>setTimeout(r,100));result=await evaluate('window.xyzStageState');if(result.value.mode===mode)break;}if(result.value.mode!==mode||result.value.error!==0||result.value.assignments.length!==1)throw Error(JSON.stringify(result));console.log(mode,result.value);
}
await evaluate("document.getElementById('mode').value='solo';document.getElementById('mode').onchange();assignments[0]='roman';draw(performance.now());");await new Promise(r=>setTimeout(r,300));
let before=await evaluate('canvas.toDataURL()');await evaluate('yaw+=.9;pitch+=.4;draw(performance.now());');await new Promise(r=>setTimeout(r,300));let after=await evaluate('canvas.toDataURL()');if(before.value===after.value)throw Error('Camara no cambia vista');console.log('Rotación de cámara cambia la vista 3D');
for (const id of ['toro','roman','cono','cassini']) {
 await evaluate(`document.querySelector('#choices select').value='${id}';document.querySelector('#choices select').onchange();draw(performance.now());`);
 const result=await evaluate('window.xyzStageState');
 if(result.value.error!==0||result.value.assignments[0]!==id)throw Error(JSON.stringify(result));
 console.log('Galería',id,'OK');
}
const shot=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(os.tmpdir(),'diverse-gallery.png'),Buffer.from(shot.data,'base64'));
console.log(await evaluate('window.xyzStageState'));
}finally{if(ws)ws.close();child.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
