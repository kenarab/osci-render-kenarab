"""Una voz por pieza, XYZ completo y sin mezcla; resultados musicales fuera de Git."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'library'))
from algebraic_surfaces.timbres import lua
s=(ROOT/'recordings/012-repertoire.js').read_text();data=json.loads(s[len('window.XYZ_REPERTOIRE='):-2])
template=(ROOT/'library/algebraic_surfaces/solo_xyz.lua.in').read_text();report={};solos={}
for name in ['bach','oblivion']:
 events=[];offset=30 if name=='bach' else 0
 for a,b,voice,pitch,velocity in data[name]['events']:
  if voice==0 and b>offset and a<offset+40:
   events.append([max(0,a-offset),min(40,b-offset),pitch,round(velocity*127)])
 events.sort()
 assert all(events[i][1]<=events[i+1][0]+1e-8 for i in range(len(events)-1)), 'La voz elegida debe ser monofonica'
 for live in [False,True]:
  code=template.replace('@TITLE@',name).replace('@ID@',name+'-solo-cuartica-v1').replace('@LIVE@',str(live).lower()).replace('@NOTES@',lua(events))
  (ROOT/'recordings'/f'012-{name}-solo-xyz{"-control" if live else ""}.lua').write_text(code)
 # Verificación Nyquist no se afirma: el recorrido sin filtrar no está limitado a 12 armónicos.
 report[name]=dict(notes=len(events),seconds=40,voice=data[name]['names'][0],source_excerpt=[30,70],geometry='X^4+3Y^4+6Z^4+k*(X^2+Y^2+Z^2)=1',filter='none',aliasing='No se elimina aliasing: filtrar alteraría el recorrido; prueba diagnóstica, escucha pendiente')
 solos[name]=dict(duration=40,names=[data[name]['names'][0]],defaults=['cuartica'],events=[[a,b,0,p,v/127] for a,b,p,v in events])
(ROOT/'recordings/012-solos.js').write_text('window.XYZ_SOLOS='+json.dumps(solos,separators=(',',':'))+';\n')
(ROOT/'experiments/012-superficies-xyz/solos.json').write_text(json.dumps(report,indent=2)+'\n')
print(report)
