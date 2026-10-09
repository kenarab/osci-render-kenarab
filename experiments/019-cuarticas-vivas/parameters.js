'use strict';
// LOB-04: reconstrucción sólo al editar a, fuera del bucle de dibujo/audio.
const values=LobedSurfaces.families.map(f=>f.initial);
function selectedFamily(){return LobedSurfaces.families.findIndex(f=>f.id===assignments[0]);}
function syncParameter(){
 const i=selectedFamily(),f=LobedSurfaces.families[i];
 $('deform').max=f.max;$('deform').value=values[i];$('parameter').value=values[i].toFixed(3);
 $('equation').textContent=f.equation;
}
function replaceGeometry(i,a){
 const m=LobedSurfaces.model(i,a),b=buffers.get(m.id),data=[];
 for(const face of m.faces)for(const v of face)data.push(...m.vertices[v]);
 models[i]=m;values[i]=a;
 gl.bindBuffer(gl.ARRAY_BUFFER,b.mesh);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(data),gl.DYNAMIC_DRAW);b.count=data.length/3;
 gl.bindBuffer(gl.ARRAY_BUFFER,b.trace);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(m.trace.flat()),gl.DYNAMIC_DRAW);b.traces=m.trace.length;
 window.lobedViewerState={id:m.id,a,vertices:m.vertices.length,faces:m.faces.length};
}
const familyChoice=document.querySelector('#choices select'),choose=familyChoice.onchange;
familyChoice.onchange=()=>{choose();syncParameter();};
$('deform').oninput=()=>{replaceGeometry(selectedFamily(),Number($('deform').value));syncParameter();};
syncParameter();
