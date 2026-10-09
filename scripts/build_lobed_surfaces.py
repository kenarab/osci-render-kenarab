"""LOB-01…04: genera solamente el nuevo experimento 019, sin OBJ ni repertorio."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'experiments/019-cuarticas-vivas'
FAMILIES=[('seis-lobulos',1,.96,.92),('ocho-lobulos',2,.94,.88)]

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 template=(ROOT/'library/algebraic_surfaces/lobed.lua.in').read_text()
 geometry=(ROOT/'library/algebraic_surfaces/lobed.lua').read_text()
 for name,kind,maximum,initial in FAMILIES:
  for live in (False,True):
   code=template
   for key,value in dict(NAME=name,KIND=kind,MAX=maximum,INITIAL=initial,NORMAL=initial/maximum,LIVE=str(live).lower(),GEOMETRY=geometry).items():
    code=code.replace('@'+key+'@',str(value))
   (OUT/(name+('-control' if live else '')+'.lua')).write_text(code)
 # Copia independiente del visor conocido; se regeneran sólo archivos de 019.
 stage=(ROOT/'apps/xyz-stage/stage.js').read_text().replace("['esfera']","[models[0].id]")
 stage=stage.replace('Recorrido del Lua y malla de la misma ecuación.','Caras y barrido calculados con la misma ecuación; sin conexión al host.')
 (OUT/'gallery.js').write_text(stage)
 print('019: cuatro Lua; visor usa ecuaciones directamente, sin mallas precalculadas')

if __name__=='__main__':main()
