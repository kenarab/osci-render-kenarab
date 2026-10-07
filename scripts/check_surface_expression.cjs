const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),E=require('../library/algebraic_surfaces/expression.js');
for(const s of JSON.parse(fs.readFileSync(path.join(root,'library/algebraic_surfaces/catalog.json'))).surfaces){
 const ast=E.parse(s.equation);assert(Number.isFinite(E.evaluate(ast,{x:.3,y:-.7,z:.9,a:s.a})));assert(E.glsl(ast).length<10000);
}
assert.equal(E.evaluate(E.parse('-x^2+2*x=1'),{x:2}),-1);
assert.equal(E.evaluate(E.parse('x^2+y^2+z^2=a'),{x:1,y:2,z:2,a:9}),0);
assert.throws(()=>E.evaluate(E.parse('x/(a-1)'),{x:1,a:1}));
for(const text of ['alert(1)','x;window.foo=1','x^-1','x^13','1/x','sin(x)','x=0=1','sqrt(-1)','x.constructor','x +','2x'])assert.throws(()=>E.parse(text),text);
console.log('ALG-R09: catálogo, evaluación, precedencia y entradas inválidas OK');
