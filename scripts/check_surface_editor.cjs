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
await send('Page.navigate',{url:require('node:url').pathToFileURL(path.resolve(__dirname,'../apps/surface-lab/index.html')).href});
const evaluate=async expression=>(await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result;
for(let i=0;i<100;i++){let r=await evaluate('window.surfaceLabState');if(r.value)break;await new Promise(r=>setTimeout(r,100));}
for(let i=0;i<6;i++){
let r=await evaluate(`document.getElementById('preset').value=${i};document.getElementById('preset').onchange();window.surfaceLabState`);if(!r.value?.valid)throw Error(JSON.stringify(r));console.log('preset',i,'OK');
}
await evaluate("document.getElementById('preset').value=2;document.getElementById('preset').onchange()");
let r=await evaluate("(()=>{let before=canvas.toDataURL();$('equation').value='x^';apply();return {state:window.surfaceLabState,retained:before===canvas.toDataURL()}})()");if(r.value.state.valid||!r.value.retained)throw Error('No conservó vista inválida');console.log('Invalid edit preserves pixels OK');
await evaluate("$('equation').value=presets[2].equation;apply();$('parameter').value=.9;$('parameter').oninput()");
const shot=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(os.tmpdir(),'surface-lab.png'),Buffer.from(shot.data,'base64'));
console.log(await evaluate("({error:gl.getError(),status:$('status').textContent,width:canvas.width,height:canvas.height})"));
}finally{if(ws)ws.close();child.kill();}
})().catch(e=>{console.error(e);process.exitCode=1});
