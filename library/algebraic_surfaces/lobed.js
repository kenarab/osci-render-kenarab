'use strict';
// LOB-02/04: ecuación evaluada directamente, sin OBJ ni extracción implícita.
(function(root){
 const families=[
  {id:'seis-lobulos',name:'Seis lóbulos',max:.96,initial:.92,equation:'(x²+y²+z²)² − a(x⁴+y⁴+z⁴) = 1'},
  {id:'ocho-lobulos',name:'Ocho lóbulos',max:.94,initial:.88,equation:'x⁴+y⁴+z⁴ − a(x²y²+y²z²+z²x²) = 1'}
 ];
 function bound(kind,a){return Math.pow((kind===0?1:3)/(1-a),.25);}
 function point(kind,u,v,a){
  const cv=Math.cos(v),x=cv*Math.cos(u),y=cv*Math.sin(u),z=Math.sin(v);
  const xx=x*x,yy=y*y,zz=z*z,q=xx*xx+yy*yy+zz*zz;
  const d=kind===0?1-a*q:q-a*(xx*yy+yy*zz+zz*xx),r=Math.pow(d,-.25);
  return [r*x,r*y,r*z];
 }
 function field(kind,[x,y,z],a){
  const xx=x*x,yy=y*y,zz=z*z,q=xx*xx+yy*yy+zz*zz;
  return (kind===0?(xx+yy+zz)**2-a*q:q-a*(xx*yy+yy*zz+zz*xx))-1;
 }
 function model(kind,a,n=48,m=96){
  if(!Number.isInteger(kind)||!families[kind]||!Number.isFinite(a)||a<0||a>families[kind].max)throw Error('Familia o parámetro fuera de rango');
  const vertices=[],faces=[];
  for(let i=0;i<=n;i++)for(let j=0;j<m;j++)vertices.push(point(kind,2*Math.PI*j/m,-Math.PI/2+Math.PI*i/n,a));
  for(let i=0;i<n;i++)for(let j=0;j<m;j++){
   const p=i*m+j,q=i*m+(j+1)%m,r=(i+1)*m+j,s=(i+1)*m+(j+1)%m;
   // Evitar triángulos degenerados en los polos.
   if(i>0)faces.push([p,q,r]);if(i<n-1)faces.push([q,s,r]);
  }
  const trace=[];
  for(let j=0;j<2304;j++)trace.push(point(kind,2*Math.PI*110*j/16000,2*Math.PI*7*j/16000,a));
  return {id:families[kind].id,vertices,faces,trace,bound:bound(kind,a),source:families[kind].equation};
 }
 const api={families,point,field,bound,model};root.LobedSurfaces=api;
 if(typeof module!=='undefined')module.exports=api;
})(globalThis);
