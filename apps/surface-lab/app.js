'use strict';
const $=id=>document.getElementById(id), E=SurfaceExpression, canvas=$('view');
const gl=canvas.getContext('webgl2',{antialias:false,preserveDrawingBuffer:true});
let program=null,ast=null,lastState=null,timer,yaw=.55,pitch=.28,zoom=1,drag=null;
const presets=[{name:'Esfera',equation:'x^2+y^2+z^2=a',a:1,bound:1.6},{name:'Toro',equation:'(x^2+y^2+z^2+0.64-0.09*a)^2-2.56*(x^2+y^2)',a:1,bound:1.5},...SURFACE_CATALOG.surfaces];
for(const [i,p] of presets.entries()){$('preset').add(new Option(p.name,i));}
const vertex=`#version 300 es
in vec2 position;out vec2 uv;void main(){uv=position;gl_Position=vec4(position,0,1);}`;
function fragment(expr){return `#version 300 es
precision highp float;
in vec2 uv;out vec4 color;uniform float uA,uBound,uYaw,uPitch,uAspect,uZoom;
${Array.from({length:11},(_,i)=>{let n=i+2;return 'float pow'+n+'(float v){return '+Array(n).fill('v').join('*')+';}';}).join('\n')}
float F(vec3 p){return ${expr};}
vec3 rotate(vec3 p){float c=cos(uYaw),s=sin(uYaw);p=vec3(c*p.x+s*p.z,p.y,-s*p.x+c*p.z);c=cos(uPitch);s=sin(uPitch);return vec3(p.x,c*p.y-s*p.z,s*p.y+c*p.z);}
void main(){
 vec3 bg=vec3(.032,.059,.085);color=vec4(bg,1);
 vec3 origin=rotate(vec3(uv.x*uAspect,uv.y,3.5)*uBound/uZoom);vec3 ray=rotate(vec3(0,0,-1));
 vec3 inv=1.0/(ray+vec3(1e-8));vec3 v0=(-vec3(uBound)-origin)*inv,v1=(vec3(uBound)-origin)*inv;
 vec3 near3=min(v0,v1),far3=max(v0,v1);float lo=max(max(near3.x,near3.y),near3.z),hi=min(min(far3.x,far3.y),far3.z);
 if(hi<=lo)return;float delta=(hi-lo)/192.0;float before=F(origin+lo*ray);float hit=-1.;
 for(int i=1;i<=192;i++){float t=lo+float(i)*delta;float value=F(origin+t*ray);
 if((value<0.)!=(before<0.)||value==0.){float a=t-delta,b=t;for(int j=0;j<12;j++){float m=(a+b)*.5;float fm=F(origin+m*ray);if((fm<0.)==(before<0.))a=m;else b=m;}hit=(a+b)*.5;break;}before=value;}
 if(hit<0.)return;vec3 p=origin+hit*ray;float e=uBound*.0006;
 vec3 n=vec3(F(p+vec3(e,0,0))-F(p-vec3(e,0,0)),F(p+vec3(0,e,0))-F(p-vec3(0,e,0)),F(p+vec3(0,0,e))-F(p-vec3(0,0,e)));
 n=normalize(n+vec3(1e-14));if(dot(n,ray)>0.)n=-n;vec3 light=rotate(normalize(vec3(-.5,.8,1.3)));
 float diffuse=max(0.,dot(n,light));float rim=pow(1.-abs(dot(n,ray)),3.);
 color=vec4(vec3(.19,.67,.62)*(.25+.75*diffuse)+vec3(.23,.32,.35)*rim,1.);
}`;}
function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){const log=gl.getShaderInfoLog(s);gl.deleteShader(s);throw Error('No se pudo compilar esta ecuación: '+log.slice(0,180));}return s;}
function compile(expr){const vs=shader(gl.VERTEX_SHADER,vertex),fs=shader(gl.FRAGMENT_SHADER,fragment(expr)),p=gl.createProgram();gl.attachShader(p,vs);gl.attachShader(p,fs);gl.linkProgram(p);gl.deleteShader(vs);gl.deleteShader(fs);if(!gl.getProgramParameter(p,gl.LINK_STATUS)){gl.deleteProgram(p);throw Error('No se pudo preparar el render');}return p;}
function status(text,error=false){$('status').textContent=text;$('status').className='status'+(error?' error':'');}
function validate(tree,a,bound){if(!E.spatial(tree))throw Error('La ecuación debe contener x, y o z');if(!Number.isFinite(a)||!Number.isFinite(bound)||bound<.2||bound>5)throw Error('Dominio permitido: 0.2 a 5');let magnitude=0;for(const p of [[0,0,0],[.31,.47,.73],[-.83,.19,-.51]])magnitude+=Math.abs(E.evaluate(tree,{x:p[0]*bound,y:p[1]*bound,z:p[2]*bound,a}));if(magnitude===0)throw Error('La ecuación se anula en todas las muestras; revisá los coeficientes');}
function apply(){if(!gl){status('Este navegador no ofrece WebGL 2. Probá Chrome actualizado.',true);return;}try{const equation=$('equation').value,a=Number($('parameter').value),bound=Number($('bound').value),tree=E.parse(equation);validate(tree,a,bound);const next=compile(E.glsl(tree));if(program)gl.deleteProgram(program);program=next;ast=tree;lastState={schema:1,equation,a,bound};render();status('Vista actualizada. Arrastrá para explorar.');window.surfaceLabState={valid:true,...lastState};}catch(e){status(e.message+' · Conservamos la última vista válida.',true);window.surfaceLabState={valid:false,error:e.message};}}
function render(){if(!program||!lastState)return;const rect=canvas.getBoundingClientRect();canvas.width=Math.min(1050,Math.round(rect.width));canvas.height=Math.min(850,Math.round(rect.height));gl.viewport(0,0,canvas.width,canvas.height);gl.useProgram(program);const loc=gl.getAttribLocation(program,'position');gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
 for(const [name,value] of Object.entries({uA:lastState.a,uBound:lastState.bound,uYaw:yaw,uPitch:pitch,uAspect:canvas.width/canvas.height,uZoom:zoom}))gl.uniform1f(gl.getUniformLocation(program,name),value);
 gl.drawArrays(gl.TRIANGLES,0,6);}
let buffer;if(gl){buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);}
$('equation').oninput=()=>{clearTimeout(timer);timer=setTimeout(apply,280);};
$('parameter').oninput=()=>{$('aval').textContent=Number($('parameter').value).toFixed(3);if(!ast||!lastState)return;try{const a=Number($('parameter').value);validate(ast,a,lastState.bound);lastState.a=a;render();status('Parámetro actualizado.');}catch(e){status(e.message+' · Conservamos la última vista válida.',true);}};
$('bound').onchange=apply;
$('preset').onchange=()=>{const p=presets[Number($('preset').value)];$('equation').value=p.equation;$('parameter').value=p.a;$('aval').textContent=p.a;$('bound').value=p.bound;apply();};
$('reset').onclick=()=>{yaw=.55;pitch=.28;zoom=1;render();};
canvas.onpointerdown=e=>{drag=[e.clientX,e.clientY];canvas.setPointerCapture(e.pointerId);};canvas.onpointerup=canvas.onpointercancel=()=>drag=null;
canvas.onpointermove=e=>{if(!drag)return;yaw+=(e.clientX-drag[0])*.007;pitch+=(e.clientY-drag[1])*.007;drag=[e.clientX,e.clientY];render();};
canvas.onwheel=e=>{e.preventDefault();zoom=Math.max(.5,Math.min(2.5,zoom*Math.exp(-e.deltaY*.001)));render();};
$('save').onclick=()=>{if(!lastState)return;const blob=new Blob([JSON.stringify({...lastState,camera:{yaw,pitch,zoom}},null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='superficie.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('load').onclick=()=>$('file').click();$('file').onchange=async()=>{try{const file=$('file').files[0];if(!file)return;if(file.size>20000)throw Error('Estado demasiado grande');const s=JSON.parse(await file.text());if(s.schema!==1||typeof s.equation!=='string'||!Number.isFinite(s.a)||s.a<0||s.a>2)throw Error('Estado no compatible');validate(E.parse(s.equation),s.a,s.bound);$('equation').value=s.equation;$('parameter').value=s.a;$('aval').textContent=s.a;$('bound').value=s.bound;apply();if(s.camera&&[s.camera.yaw,s.camera.pitch,s.camera.zoom].every(Number.isFinite)){({yaw,pitch,zoom}=s.camera);zoom=Math.max(.5,Math.min(2.5,zoom));render();}}catch(e){status(e.message,true);}finally{$('file').value='';}};
window.addEventListener('resize',render);$('preset').onchange();
