/* Parser algebraico compartido: AST evaluable y GLSL, sin eval ni Function. */
(function(root){
'use strict';
function parse(text){
 if(text.length>8000)throw Error('Ecuación demasiado larga');
 const tokens=text.match(/(?:\d*\.\d+|\d+\.?\d*)(?:[eE][+-]?\d+)?|[A-Za-z_]+|\*\*|[^\s]/g)||[];
 let i=0,count=0;
 const node=(op,...args)=>{if(++count>700)throw Error('Expresión demasiado compleja');return {op,args};};
 function atom(){const t=tokens[i++];
  if(t==='('){const n=add();if(tokens[i++]!==')')throw Error('Falta )');return n;}
  if(/^(?:\d|\.\d)/.test(t||'')){const v=Number(t);if(!Number.isFinite(v))throw Error('Número no finito');return node('n',v);}
  if(['x','y','z','a'].includes(t))return node('v',t);
  if(t==='pi')return node('n',Math.PI);
  if(['sqrt','sin','cos'].includes(t)){if(tokens[i++]!=='(')throw Error('Falta (');const n=add();if(tokens[i++]!==')')throw Error('Falta )');if(depends(n))throw Error(t+' sólo admite constantes numéricas');return node('n',checked(Math[t](evaluate(n,{}))));}
  throw Error('Símbolo no admitido: '+(t||'fin'));
 }
 function power(){let n=atom();if(tokens[i]==='^'||tokens[i]==='**'){i++;const t=tokens[i++];const k=Number(t);if(!/^\d+$/.test(t||'')||k>12)throw Error('Potencia entera entre 0 y 12');n=node('pow',n,k);}return n;}
 function unary(){if(tokens[i]==='-'){i++;return node('neg',unary());}if(tokens[i]==='+'){i++;return unary();}return power();}
 function mul(){let n=unary();while(['*','/'].includes(tokens[i])){const op=tokens[i++],r=unary();if(op==='/'&&spatial(r))throw Error('El denominador no puede contener x, y o z');n=node(op,n,r);}return n;}
 function add(){let n=mul();while(['+','-'].includes(tokens[i])){const op=tokens[i++];n=node(op,n,mul());}return n;}
 let n=add();if(tokens[i]==='='){i++;n=node('-',n,add());}if(i!==tokens.length)throw Error('Revisá el símbolo '+tokens[i]);return n;
}
function depends(n){return n.op==='v'||n.args.some(a=>a&&typeof a==='object'&&depends(a));}
function spatial(n){return n.op==='v'&&n.args[0]!=='a'||n.args.some(a=>a&&typeof a==='object'&&spatial(a));}
function checked(v){if(!Number.isFinite(v))throw Error('Resultado no finito');return v;}
function evaluate(n,p){const a=n.args;switch(n.op){case'n':return a[0];case'v':return checked(p[a[0]]);case'neg':return -evaluate(a[0],p);case'pow':return checked(evaluate(a[0],p)**a[1]);default:{const x=evaluate(a[0],p),y=evaluate(a[1],p);return checked(n.op==='+'?x+y:n.op==='-'?x-y:n.op==='*'?x*y:x/y);}}}
function glsl(n){const a=n.args;switch(n.op){case'n':return a[0].toExponential(12);case'v':return a[0]==='a'?'uA':'p.'+a[0];case'neg':return '(-'+glsl(a[0])+')';case'pow':return a[1]===0?'1.0':a[1]===1?glsl(a[0]):'pow'+a[1]+'('+glsl(a[0])+')';default:return '('+glsl(a[0])+n.op+glsl(a[1])+')';}}
const api={parse,evaluate,glsl,spatial};if(typeof module!=='undefined')module.exports=api;else root.SurfaceExpression=api;
})(typeof globalThis!=='undefined'?globalThis:this);
